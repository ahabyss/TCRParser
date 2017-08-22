from datetime import datetime, time, timedelta
from pandas import Series, date_range
from pytz import timezone
from colour import Color
import numpy as np
import pytz
import json
import jsonpickle
import re
from random import random, uniform
from math import floor
import os 

class ep():
	def __init__(self, ranges):
		self.msgs = Series()
		self.ranges = ranges
		
class chatmsg():
	def __init__(self, dt, n, m):
		self.dt = dt
		self.n = n
		self.m = m
		self.c = Color(pick_for=self.n, saturation=0.7, luminance=uniform(0.3, 0.7)).hex
		self.ttvGEmotes = []
		self.bttvGEmotes = []
		self.ttvCEmotes = []
		self.isprimeorturbo = random() < 0.33
		self.isprimevsturbo = random() < 0.2
		self.badges = [self.isprimeorturbo and self.isprimevsturbo, self.isprimeorturbo and not self.isprimevsturbo, random() < 0.2]
	def toJSON(self):
		return [self.n, self.c, self.m, self.ttvGEmotes, self.bttvGEmotes, self.ttvCEmotes, self.badges]
		
class show():
	def __init__(self, name, short):
		self.name = name
		self.episodes = []
		self.short = short
			
class showEncoder(json.JSONEncoder):
	def default(self, obj):
		return [obj.name, len(obj.episodes), obj.short]
		return json.JSONEncoder.default(self, obj)
			
			
dir = os.path.dirname(os.path.realpath(__file__)) + '\\'
#fNames = ['2017-07-27.txt', '2017-07-28.txt', '2017-07-29.txt', '2017-07-30.txt', '2017-07-31.txt', '2017-08-01.txt']
fNames = ['2017-07-27.txt', '2017-07-28.txt']
overrustleFormat = '%Y-%m-%d %H:%M:%S %Z'

#------------------Show Init
shows = []

shows.append(show('Mob Psycho 100', 'mob')) #ep start, b4 snacks, after snacks, b4 crunchyend
shows[0].episodes.append(ep([['2017-07-27 22:31:23 UTC', '2017-07-27 22:40:46 UTC'], ['2017-07-27 22:42:22 UTC', '2017-07-27 22:57:09 UTC']]))
shows[0].episodes.append(ep([['2017-07-27 22:57:13 UTC', '2017-07-27 23:09:00 UTC'], ['2017-07-27 23:10:36 UTC', '2017-07-27 23:22:57 UTC']]))
shows[0].episodes.append(ep([['2017-07-27 23:23:02 UTC', '2017-07-27 23:28:58 UTC'], ['2017-07-27 23:30:32 UTC', '2017-07-27 23:48:46 UTC']]))
shows[0].episodes.append(ep([['2017-07-27 23:48:51 UTC', '2017-07-28 00:01:03 UTC'], ['2017-07-28 00:02:39 UTC', '2017-07-28 00:14:36 UTC']]))
shows[0].episodes.append(ep([['2017-07-28 00:14:40 UTC', '2017-07-28 00:25:00 UTC'], ['2017-07-28 00:26:36 UTC', '2017-07-28 00:40:24 UTC']]))
shows[0].episodes.append(ep([['2017-07-28 00:40:29 UTC', '2017-07-28 00:51:08 UTC'], ['2017-07-28 00:52:43 UTC', '2017-07-28 01:06:13 UTC']]))
shows[0].episodes.append(ep([['2017-07-28 01:06:18 UTC', '2017-07-28 01:17:59 UTC'], ['2017-07-28 01:19:33 UTC', '2017-07-28 01:32:02 UTC']]))
shows[0].episodes.append(ep([['2017-07-28 01:32:07 UTC', '2017-07-28 01:45:28 UTC'], ['2017-07-28 01:47:03 UTC', '2017-07-28 01:57:51 UTC']]))
shows[0].episodes.append(ep([['2017-07-28 01:57:57 UTC', '2017-07-28 02:09:48 UTC'], ['2017-07-28 02:11:24 UTC', '2017-07-28 02:23:40 UTC']]))
shows[0].episodes.append(ep([['2017-07-28 02:23:46 UTC', '2017-07-28 02:34:01 UTC'], ['2017-07-28 02:35:35 UTC', '2017-07-28 02:49:29 UTC']]))
shows[0].episodes.append(ep([['2017-07-28 02:49:35 UTC', '2017-07-28 03:00:27 UTC'], ['2017-07-28 03:02:02 UTC', '2017-07-28 03:15:19 UTC']]))
shows[0].episodes.append(ep([['2017-07-28 03:15:23 UTC', '2017-07-28 03:30:13 UTC'], ['2017-07-28 03:31:19 UTC', '2017-07-28 03:40:37 UTC']]))

shows.append(show("Miss Kobayashi's Dragon Maid", 'koba'))
shows.append(show("Bungo Stray Dogs", 'bungo'))
shows.append(show("Sound! Euphonium", 'sndeu'))
shows.append(show("Yuri!!! on Ice", 'yuri'))
shows.append(show("Space Patrol Luluco", 'luluc'))
shows.append(show("Anne Happy!", 'anne'))
shows.append(show("Saga of Tanya the Evil", 'tanya'))
shows.append(show("JOKER GAME", 'joker'))
shows.append(show("ReLife", 'relif'))
shows.append(show("Kemono Friends", 'kemon'))
shows.append(show("Rokka-Braves of Six Flowers", 'rokka'))
shows.append(show("NEW GAME!", 'newgm'))
shows.append(show("Gabriel DropOut", 'gabrl'))
shows.append(show("Ojisan & Marshmallow", 'marsh'))
shows.append(show("Wooser's Hand-to-Mouth Life: Phantasmagoric Arc", 'woose'))
shows.append(show("World End: What are you doing at the end of the world? Are you busy? Will you save us?", 'world'))
shows.append(show("Akashic Records of Bastard Magic Instructor", 'akash'))
shows.append(show("Free! Iwatobi Swim Club", 'free'))

#shows.append(show("Mob Psycho 100", 'mob2'))
#shows.append(show("Miss Kobayashi's Dragon Maid", 'koba2'))
#shows.append(show("Yuri!!! on Ice", 'yuri2'))

#-----emote jsons
ttvGlobal = {}
with open(dir + 'ttvGlobal.json') as jd:
	ttvGlobalJSON = json.load(jd)
	for emoteCode in ttvGlobalJSON:
		ttvGlobal[emoteCode] = ttvGlobalJSON[emoteCode]['id']
	
bttvGlobal = {}
with open(dir + 'bttvGlobal.json') as jd:
	bttvGlobalJSON = json.load(jd)
	for emote in bttvGlobalJSON['emotes']:
		bttvGlobal[emote['code']] = emote['id']

ttvCh = {}
with open(dir + 'ttvChannels.json') as jd:
	ttvChJSON = json.load(jd)
	for emoteID in ttvChJSON:
		emote = ttvChJSON[emoteID]
		ttvCh[emote['code']] = emote['id']

#---------------------Load Chat
msgsRaw = []
times = {}
for fName in fNames:
	print(fName)
	for line in np.genfromtxt(dir+fName, delimiter='\n', dtype=None):
		tempdata = line[26:].decode('utf-8').split(':', 1)
		time = datetime.strptime(line[1:24].decode('utf-8'), overrustleFormat)
		time -= timedelta(seconds = (1 - time.second % 2)) #2 second smoothing
		if time in times:
			times[time][0] += 1
		else:
			times[time] = [1, 0, time+timedelta(seconds = 1)]
			if len(times) > 1:
				times[prevtime][2] = time
			prevtime = time
		msgsRaw.append(chatmsg(time, tempdata[0], tempdata[1][1:]))

for msgInd, msg in enumerate(msgsRaw):
	time = msg.dt
	msg.dt += timedelta(milliseconds = floor(((times[time][2] - time).seconds*1000) * times[time][1] / times[time][0]))
	times[time][1] += 1
		
msgSeries = Series((chatmsgitem for chatmsgitem in msgsRaw), (chatmsgitem.dt for chatmsgitem in msgsRaw))	
	
for show in shows:
	for ep in show.episodes:
		rangeGap = timedelta(0);
		for trInd, timeRange in enumerate(ep.ranges):
			ep.msgs = ep.msgs.append(msgSeries[timeRange[0]:timeRange[1]].rename(lambda x: x - rangeGap))
			timeEnd = datetime.strptime(timeRange[1], overrustleFormat)
			if trInd < (len(ep.ranges) - 1):
				ep.msgs = ep.msgs.append(Series([chatmsg((timeEnd - rangeGap) + timedelta(seconds = 1), "_TCRMSG", "SNACK TIME"), chatmsg("0", "", "")], [(timeEnd - rangeGap) + timedelta(seconds = 1), 0]).drop(0))
				rangeGap += (datetime.strptime(ep.ranges[trInd+1][0], overrustleFormat) - timeEnd) - timedelta(seconds = 1) #adjust the next range by the gap
			else: 
				ep.msgs = ep.msgs.append(Series([chatmsg(timeEnd - rangeGap + timedelta(seconds = 1), "_TCRMSG", "FIN"), chatmsg("0", "", "")], [timeEnd - rangeGap + timedelta(seconds = 1), 0]).drop(0))

for show in shows:
	for ep in show.episodes:
		for msg in ep.msgs:
			parts = [(m.group(0), (m.start(), m.end()-1)) for m in re.finditer(r'\S+', msg.m)]
			for part in parts:
				if part[0] in ttvGlobal:
					msg.ttvGEmotes.append([ttvGlobal[part[0]], part[1]])
				elif part[0] in bttvGlobal:
					msg.bttvGEmotes.append([bttvGlobal[part[0]], part[1]])
				elif part[0] in ttvCh:
					msg.ttvCEmotes.append([ttvCh[part[0]], part[1]])
					
for show in shows:
	for epInd, ep in enumerate(show.episodes):
		with open(dir + show.short + str(epInd+1) + '.json', 'w', encoding='utf-8') as outfile:
			ep.msgs.to_json(outfile, orient='split', force_ascii=False, default_handler=chatmsg.toJSON)
			
with open(dir + 'shows.json', 'w', encoding='utf-8') as outfile:
	json.dump(shows, outfile, cls = showEncoder)
		