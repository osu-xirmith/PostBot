#/usr/bin/env python3
import sys
import socket
import string
import os
import time
#could maybe find a better library for this, but it works and is easy o
import feedparser
	
userlist=[]

nick = 'ACRPostBot'
debug = True 
network = 'irc.freenode.net'
port = 6667
chan='#acreloaded-forum'
last = time.time()
rssurl = "http://forum.acr.victorz.ca/syndication2.php?limit=5"
posts = []

def sendMessage(message):
	irc.send(bytes('PRIVMSG ' + chan + ' :' + message + '\r\n', 'UTF-8'))

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((network,port))
print(irc.recv(4096))
irc.recv(4096)
irc.send(bytes('NICK ' + nick + '\r\n', 'UTF-8'))
irc.send(bytes('USER LEAP LEAPer LEAPer :LEAP IRC\r\n', 'UTF-8'))
while True:
	data = str(irc.recv(4096))
	if debug:
		print(data)
	if data.find('PING') != -1: 
		irc.send(bytes('PONG ' + data.split()[1] + '\r\n', 'UTF-8'))
	if data.find('End of /MOTD command.') != -1: #check for welcome message
		irc.send(bytes('JOIN ' + chan + '\r\n', 'UTF-8'))
	if data.find('!quit')!=-1 and data.find('ruler501')!=-1:
		break
	times = millis = time.time()
	if times-last > 8:
		last = times
		feed=feedparser.parse(rssurl)
		for ent in feed.entries:
			title = ent.title
			if title[:4] == "RE: ":
				title = ent.title[4:]
			if (title+','+str(time.mktime(ent.published_parsed))) not in posts:
				posts.append(title+','+str(time.mktime(ent.published_parsed))) #I think this is unique in practice, but theoretically could get duplicated
				if len(title) > 30:
					title = title[:26]+'...'#limits it to 30 characters(len(title[:26])==27)
				out = title+' '+ent.id
				if debug:
					print(out)
				sendMessage(out)
				while len(posts) > 5:
					posts.pop(0)