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
import copy

class ep():
    def __init__(self, ranges):
        self.msgs = Series()
        self.ranges = ranges
        
class chatmsg():
    def __init__(self, dt, n, m):
        self.dt = dt
        self.n = n
        self.m = m
        self.c = Color(pick_for = self.n, saturation = 0.7, luminance = uniform(0.3, 0.7)).hex
        self.ttvGEmotes = []
        self.bttvGEmotes = []
        self.ttvCEmotes = []
        self.isprimeorturbo = random() < 0.33
        self.isprimevsturbo = random() < 0.2
        self.badges = [self.isprimeorturbo and self.isprimevsturbo, self.isprimeorturbo and not self.isprimevsturbo, random() < 0.2]
    def toJSON(self):
        return [self.n, self.c, self.m, self.ttvGEmotes, self.bttvGEmotes, self.ttvCEmotes, self.badges]
        
class show():
    def __init__(self, name, short, offset = timedelta(seconds = 0)):
        self.name = name
        self.episodes = []
        self.short = short
        self.offset = offset
            
class showEncoder(json.JSONEncoder):
    def default(self, obj):
        return [obj.name, len(obj.episodes), obj.short]
        return json.JSONEncoder.default(self, obj)
            
            
dir = os.path.dirname(os.path.realpath(__file__)) + '\\'
dataSubDir = 'TwitchChatReplay\\src\\common\\data\\'
fNames = ['2017-07-27.txt', '2017-07-28.txt', '2017-07-29.txt', '2017-07-30.txt', '2017-07-31.txt', '2017-08-01.txt']
#fNames = ['2017-07-27.txt', '2017-07-28.txt']
overrustleFormat = '%Y-%m-%d %H:%M:%S %Z'

#------------------Show Init
shows = []
shows.append(show('Mob Psycho 100', 'mob')) #ep start, b4 snacks, after snacks, b4 crunchyend
shows[len(shows) - 1].episodes.append(ep([['2017-07-27 22:31:23 UTC', '2017-07-27 22:40:46 UTC'], ['2017-07-27 22:42:22 UTC', '2017-07-27 22:57:09 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-27 22:57:13 UTC', '2017-07-27 23:09:00 UTC'], ['2017-07-27 23:10:36 UTC', '2017-07-27 23:22:57 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-27 23:23:02 UTC', '2017-07-27 23:28:58 UTC'], ['2017-07-27 23:30:32 UTC', '2017-07-27 23:48:46 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-27 23:48:51 UTC', '2017-07-28 00:01:03 UTC'], ['2017-07-28 00:02:39 UTC', '2017-07-28 00:14:36 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 00:14:40 UTC', '2017-07-28 00:25:00 UTC'], ['2017-07-28 00:26:36 UTC', '2017-07-28 00:40:24 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 00:40:29 UTC', '2017-07-28 00:51:08 UTC'], ['2017-07-28 00:52:43 UTC', '2017-07-28 01:06:13 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 01:06:18 UTC', '2017-07-28 01:17:59 UTC'], ['2017-07-28 01:19:33 UTC', '2017-07-28 01:32:02 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 01:32:07 UTC', '2017-07-28 01:45:28 UTC'], ['2017-07-28 01:47:03 UTC', '2017-07-28 01:57:51 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 01:57:57 UTC', '2017-07-28 02:09:48 UTC'], ['2017-07-28 02:11:24 UTC', '2017-07-28 02:23:40 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 02:23:46 UTC', '2017-07-28 02:34:01 UTC'], ['2017-07-28 02:35:35 UTC', '2017-07-28 02:49:29 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 02:49:35 UTC', '2017-07-28 03:00:27 UTC'], ['2017-07-28 03:02:02 UTC', '2017-07-28 03:15:19 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 03:15:23 UTC', '2017-07-28 03:30:13 UTC'], ['2017-07-28 03:31:19 UTC', '2017-07-28 03:40:37 UTC']]))

shows.append(show("Miss Kobayashi's Dragon Maid", 'koba', timedelta(seconds = 6.5)))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 04:01:07 UTC', '2017-07-28 04:13:02 UTC'], ['2017-07-28 04:15:07 UTC', '2017-07-28 04:26:50 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 04:26:53 UTC', '2017-07-28 04:38:26 UTC'], ['2017-07-28 04:40:30 UTC', '2017-07-28 04:52:37 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 04:52:40 UTC', '2017-07-28 05:03:58 UTC'], ['2017-07-28 05:06:02 UTC', '2017-07-28 05:18:24 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 05:18:27 UTC', '2017-07-28 05:28:34 UTC'], ['2017-07-28 05:30:38 UTC', '2017-07-28 05:44:11 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 05:44:14 UTC', '2017-07-28 05:53:35 UTC'], ['2017-07-28 05:55:39 UTC', '2017-07-28 06:09:58 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 06:10:01 UTC', '2017-07-28 06:25:06 UTC'], ['2017-07-28 06:27:10 UTC', '2017-07-28 06:35:45 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 06:35:48 UTC', '2017-07-28 06:47:14 UTC'], ['2017-07-28 06:49:20 UTC', '2017-07-28 07:01:32 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 07:01:35 UTC', '2017-07-28 07:15:08 UTC'], ['2017-07-28 07:17:14 UTC', '2017-07-28 07:27:19 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 07:27:22 UTC', '2017-07-28 07:37:13 UTC'], ['2017-07-28 07:39:19 UTC', '2017-07-28 07:53:06 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 07:53:09 UTC', '2017-07-28 08:03:55 UTC'], ['2017-07-28 08:06:01 UTC', '2017-07-28 08:18:53 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 08:18:56 UTC', '2017-07-28 08:30:53 UTC'], ['2017-07-28 08:32:57 UTC', '2017-07-28 08:44:40 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 08:44:43 UTC', '2017-07-28 08:53:53 UTC'], ['2017-07-28 08:55:57 UTC', '2017-07-28 09:10:28 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-28 09:10:31 UTC', '2017-07-28 09:18:42 UTC'], ['2017-07-28 09:20:17 UTC', '2017-07-28 09:35:44 UTC']]))

#shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))

shows.append(show("Bungo Stray Dogs", 'bungo'))

shows.append(show("Sound! Euphonium", 'sndeu'))

shows.append(show("Yuri!!! on Ice", 'yuri'))

shows.append(show("Space Patrol Luluco", 'luluc'))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 08:01:07 UTC', '2017-07-29 08:08:57 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 08:10:04 UTC', '2017-07-29 08:17:54 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 08:18:58 UTC', '2017-07-29 08:26:52 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 08:27:58 UTC', '2017-07-29 08:35:48 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 08:36:54 UTC', '2017-07-29 08:44:45 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 08:45:52 UTC', '2017-07-29 08:53:43 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 08:54:50 UTC', '2017-07-29 09:02:40 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 09:03:47 UTC', '2017-07-29 09:11:37 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 09:12:43 UTC', '2017-07-29 09:20:34 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 09:21:42 UTC', '2017-07-29 09:29:32 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 09:30:39 UTC', '2017-07-29 09:38:30 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 09:39:38 UTC', '2017-07-29 09:47:28 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 09:48:06 UTC', '2017-07-29 09:55:56 UTC']]))

shows.append(show("Anne Happy!", 'anne'))
shows[len(shows) - 1].episodes.append(ep([['', '2017-07-29 10:48:53 UTC'], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
shows[len(shows) - 1].episodes.append(ep([['', ''], ['', '']]))
1

shows.append(show("Saga of Tanya the Evil", 'tanya'))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 16:30:58 UTC', '2017-07-29 16:44:10 UTC'], ['2017-07-29 16:45:15 UTC', '2017-07-29 16:55:41 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 16:55:44 UTC', '2017-07-29 17:07:42 UTC'], ['2017-07-29 17:08:46 UTC', '2017-07-29 17:20:29 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 17:20:32 UTC', '2017-07-29 17:30:47 UTC'], ['2017-07-29 17:31:51 UTC', '2017-07-29 17:45:16 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 17:45:19 UTC', '2017-07-29 17:56:18 UTC'], ['2017-07-29 17:57:23 UTC', '2017-07-29 18:10:03 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 18:10:06 UTC', '2017-07-29 18:23:02 UTC'], ['2017-07-29 18:24:05 UTC', '2017-07-29 18:34:50 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 18:34:53 UTC', '2017-07-29 18:45:04 UTC'], ['2017-07-29 18:46:08 UTC', '2017-07-29 18:59:37 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 18:59:40 UTC', '2017-07-29 19:08:53 UTC'], ['2017-07-29 19:09:57 UTC', '2017-07-29 19:24:25 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 19:24:28 UTC', '2017-07-29 19:35:48 UTC'], ['2017-07-29 19:36:52 UTC', '2017-07-29 19:49:11 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 19:49:14 UTC', '2017-07-29 19:59:17 UTC'], ['2017-07-29 20:00:21 UTC', '2017-07-29 20:13:59 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 20:14:02 UTC', '2017-07-29 20:25:35 UTC'], ['2017-07-29 20:26:39 UTC', '2017-07-29 20:38:46 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 20:38:49 UTC', '2017-07-29 20:50:22 UTC'], ['2017-07-29 20:51:26 UTC', '2017-07-29 21:03:33 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 21:03:36 UTC', '2017-07-29 21:16:30 UTC'], ['2017-07-29 21:17:05 UTC', '2017-07-29 21:27:49 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-29 21:27:52 UTC', '2017-07-29 21:37:53 UTC'], ['2017-07-29 21:38:27 UTC', '2017-07-29 21:52:06 UTC']]))

shows.append(show("JOKER GAME", 'joker'))

shows.append(show("ReLife", 'relif'))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 03:31:05 UTC', '2017-07-30 03:47:01 UTC'], ['2017-07-30 03:49:07 UTC', '2017-07-30 03:56:49 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 03:56:52 UTC', '2017-07-30 04:09:35 UTC'], ['2017-07-30 04:11:41 UTC', '2017-07-30 04:22:36 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 04:22:39 UTC', '2017-07-30 04:33:35 UTC'], ['2017-07-30 04:35:41 UTC', '2017-07-30 04:48:23 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 04:48:26 UTC', '2017-07-30 05:01:28 UTC'], ['2017-07-30 05:03:33 UTC', '2017-07-30 05:14:10 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 05:14:13 UTC', '2017-07-30 05:28:20 UTC'], ['2017-07-30 05:30:25 UTC', '2017-07-30 05:39:57 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 05:40:00 UTC', '2017-07-30 05:51:05 UTC'], ['2017-07-30 05:53:09 UTC', '2017-07-30 06:05:44 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 06:05:47 UTC', '2017-07-30 06:16:57 UTC'], ['2017-07-30 06:19:01 UTC', '2017-07-30 06:31:31 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 06:31:34 UTC', '2017-07-30 06:44:39 UTC'], ['2017-07-30 06:46:43 UTC', '2017-07-30 06:57:18 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 06:57:21 UTC', '2017-07-30 07:07:22 UTC'], ['2017-07-30 07:09:28 UTC', '2017-07-30 07:23:03 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 07:23:06 UTC', '2017-07-30 07:33:56 UTC'], ['2017-07-30 07:35:59 UTC', '2017-07-30 07:48:51 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 07:48:54 UTC', '2017-07-30 08:00:09 UTC'], ['2017-07-30 08:02:15 UTC', '2017-07-30 08:14:37 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 08:14:40 UTC', '2017-07-30 08:27:07 UTC'], ['2017-07-30 08:29:11 UTC', '2017-07-30 08:40:24 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 08:40:27 UTC', '2017-07-30 08:50:58 UTC'], ['2017-07-30 08:53:02 UTC', '2017-07-30 09:06:21 UTC']]))

shows.append(show("Kemono Friends", 'kemon'))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 09:30:58 UTC', '2017-07-30 09:40:50 UTC'], ['2017-07-30 09:44:54 UTC', '2017-07-30 09:58:58 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 09:59:01 UTC', '2017-07-30 10:12:05 UTC'], ['2017-07-30 10:15:39 UTC', '2017-07-30 10:26:32 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 10:26:35 UTC', '2017-07-30 10:37:30 UTC'], ['2017-07-30 10:41:04 UTC', '2017-07-30 10:54:06 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 10:54:09 UTC', '2017-07-30 11:05:06 UTC'], ['2017-07-30 11:08:40 UTC', '2017-07-30 11:21:40 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 11:21:43 UTC', '2017-07-30 11:31:56 UTC'], ['2017-07-30 11:35:30 UTC', '2017-07-30 11:49:14 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 11:49:17 UTC', '2017-07-30 12:02:29 UTC'], ['2017-07-30 12:06:03 UTC', '2017-07-30 12:16:50 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 12:16:53 UTC', '2017-07-30 12:27:28 UTC'], ['2017-07-30 12:31:02 UTC', '2017-07-30 12:44:22 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 12:44:25 UTC', '2017-07-30 12:53:41 UTC'], ['2017-07-30 12:57:15 UTC', '2017-07-30 13:11:56 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 13:11:59 UTC', '2017-07-30 13:23:39 UTC'], ['2017-07-30 13:27:12 UTC', '2017-07-30 13:39:29 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 13:39:32 UTC', '2017-07-30 13:45:12 UTC'], ['2017-07-30 13:48:46 UTC', '2017-07-30 14:07:02 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 14:07:05 UTC', '2017-07-30 14:12:47 UTC'], ['2017-07-30 14:16:20 UTC', '2017-07-30 14:34:37 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 14:34:40 UTC', '2017-07-30 14:45:41 UTC'], ['2017-07-30 14:49:15 UTC', '2017-07-30 15:01:55 UTC']]))

shows.append(show("Rokka-Braves of Six Flowers", 'rokka'))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 15:31:17 UTC', '2017-07-30 15:44:27 UTC'], ['2017-07-30 15:48:33 UTC', '2017-07-30 15:59:00 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 15:59:03 UTC', '2017-07-30 16:10:54 UTC'], ['2017-07-30 16:14:59 UTC', '2017-07-30 16:26:47 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 16:26:50 UTC', '2017-07-30 16:37:59 UTC'], ['2017-07-30 16:42:03 UTC', '2017-07-30 16:54:33 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 16:54:36 UTC', '2017-07-30 17:05:29 UTC'], ['2017-07-30 17:09:32 UTC', '2017-07-30 17:22:21 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 17:22:24 UTC', '2017-07-30 17:34:54 UTC'], ['2017-07-30 17:38:58 UTC', '2017-07-30 17:50:07 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 17:50:10 UTC', '2017-07-30 18:01:48 UTC'], ['2017-07-30 18:05:25 UTC', '2017-07-30 18:17:24 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 18:17:27 UTC', '2017-07-30 18:31:00 UTC'], ['2017-07-30 18:34:36 UTC', '2017-07-30 18:44:40 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 18:44:43 UTC', '2017-07-30 18:57:33 UTC'], ['2017-07-30 19:01:07 UTC', '2017-07-30 19:11:58 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 19:12:01 UTC', '2017-07-30 19:22:06 UTC'], ['2017-07-30 19:25:39 UTC', '2017-07-30 19:39:15 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 19:39:18 UTC', '2017-07-30 19:51:13 UTC'], ['2017-07-30 19:54:47 UTC', '2017-07-30 20:06:32 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 20:06:35 UTC', '2017-07-30 20:19:46 UTC'], ['2017-07-30 20:23:20 UTC', '2017-07-30 20:33:49 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 20:33:52 UTC', '2017-07-30 20:47:02 UTC'], ['2017-07-30 20:50:38 UTC', '2017-07-30 21:01:05 UTC']]))

shows.append(show("NEW GAME!", 'newgm'))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 21:30:59 UTC', '2017-07-30 21:44:06 UTC'], ['2017-07-30 21:46:11 UTC', '2017-07-30 21:56:42 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 21:56:45 UTC', '2017-07-30 22:09:06 UTC'], ['2017-07-30 22:10:08 UTC', '2017-07-30 22:22:30 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 22:22:33 UTC', '2017-07-30 22:34:49 UTC'], ['2017-07-30 22:37:05 UTC', '2017-07-30 22:48:19 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 22:48:22 UTC', '2017-07-30 22:58:40 UTC'], ['2017-07-30 23:00:46 UTC', '2017-07-30 23:14:06 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 23:14:09 UTC', '2017-07-30 23:21:54 UTC'], ['2017-07-30 23:23:58 UTC', '2017-07-30 23:39:53 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-30 23:39:56 UTC', '2017-07-30 23:50:19 UTC'], ['2017-07-30 23:52:25 UTC', '2017-07-31 00:05:40 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 00:05:43 UTC', '2017-07-31 00:18:22 UTC'], ['2017-07-31 00:20:27 UTC', '2017-07-31 00:31:27 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 00:31:30 UTC', '2017-07-31 00:42:00 UTC'], ['2017-07-31 00:44:04 UTC', '2017-07-31 00:57:14 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 00:57:17 UTC', '2017-07-31 01:08:27 UTC'], ['2017-07-31 01:10:31 UTC', '2017-07-31 01:23:01 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 01:23:04 UTC', '2017-07-31 01:34:40 UTC'], ['2017-07-31 01:36:44 UTC', '2017-07-31 01:48:48 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 01:48:51 UTC', '2017-07-31 02:01:56 UTC'], ['2017-07-31 02:04:00 UTC', '2017-07-31 02:14:35 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 02:14:38 UTC', '2017-07-31 02:24:48 UTC'], ['2017-07-31 02:26:22 UTC', '2017-07-31 02:39:36 UTC']]))

shows.append(show("Gabriel DropOut", 'gabrl'))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 03:01:08 UTC', '2017-07-31 03:14:18 UTC'], ['2017-07-31 03:16:23 UTC', '2017-07-31 03:26:51 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 03:26:54 UTC', '2017-07-31 03:40:15 UTC'], ['2017-07-31 03:42:21 UTC', '2017-07-31 03:52:38 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 03:52:41 UTC', '2017-07-31 04:05:14 UTC'], ['2017-07-31 04:07:20 UTC', '2017-07-31 04:18:25 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 04:18:28 UTC', '2017-07-31 04:27:54 UTC'], ['2017-07-31 04:29:58 UTC', '2017-07-31 04:44:12 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 04:44:15 UTC', '2017-07-31 04:55:53 UTC'], ['2017-07-31 04:57:59 UTC', '2017-07-31 05:09:58 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 05:10:01 UTC', '2017-07-31 05:22:35 UTC'], ['2017-07-31 05:24:37 UTC', '2017-07-31 05:35:46 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 05:35:49 UTC', '2017-07-31 05:50:19 UTC'], ['2017-07-31 05:52:23 UTC', '2017-07-31 06:01:34 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 06:01:37 UTC', '2017-07-31 06:16:42 UTC'], ['2017-07-31 06:18:49 UTC', '2017-07-31 06:27:21 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 06:27:24 UTC', '2017-07-31 06:42:31 UTC'], ['2017-07-31 06:44:04 UTC', '2017-07-31 06:52:38 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 06:52:41 UTC', '2017-07-31 07:07:05 UTC'], ['2017-07-31 07:08:39 UTC', '2017-07-31 07:17:55 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 07:17:58 UTC', '2017-07-31 07:28:13 UTC'], ['2017-07-31 07:29:48 UTC', '2017-07-31 07:43:12 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 07:43:15 UTC', '2017-07-31 07:56:09 UTC'], ['2017-07-31 07:57:45 UTC', '2017-07-31 08:08:29 UTC']]))

shows.append(show("Ojisan & Marshmallow", 'marsh')) #ep start, ep end
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 08:30:58 UTC', '2017-07-31 08:34:28 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 08:34:32 UTC', '2017-07-31 08:38:01 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 08:38:05 UTC', '2017-07-31 08:41:34 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 08:41:38 UTC', '2017-07-31 08:45:08 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 08:45:12 UTC', '2017-07-31 08:48:41 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 08:48:45 UTC', '2017-07-31 08:52:14 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 08:52:18 UTC', '2017-07-31 08:55:47 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 08:55:51 UTC', '2017-07-31 08:59:21 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 08:59:25 UTC', '2017-07-31 09:02:54 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 09:02:58 UTC', '2017-07-31 09:06:27 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 09:06:31 UTC', '2017-07-31 09:10:00 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 09:10:04 UTC', '2017-07-31 09:13:34 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 09:13:38 UTC', '2017-07-31 09:17:08 UTC']]))

shows.append(show("Wooser's Hand-to-Mouth Life: Phantasmagoric Arc", 'woose'))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 09:34:51 UTC', '2017-07-31 09:42:41 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 09:43:18 UTC', '2017-07-31 09:51:08 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 09:51:44 UTC', '2017-07-31 09:59:35 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 10:00:12 UTC', '2017-07-31 10:08:02 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 10:08:39 UTC', '2017-07-31 10:16:29 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 10:16:32 UTC', '2017-07-31 10:24:22 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 10:24:25 UTC', '2017-07-31 10:32:15 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 10:32:18 UTC', '2017-07-31 10:40:08 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 10:40:11 UTC', '2017-07-31 10:48:01 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 10:48:04 UTC', '2017-07-31 10:55:54 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 10:55:57 UTC', '2017-07-31 11:03:47 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 11:03:50 UTC', '2017-07-31 11:11:40 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 11:11:43 UTC', '2017-07-31 11:19:33 UTC']]))

shows.append(show("World End: What are you doing at the end of the world? Are you busy? Will you save us?", 'world'))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 11:30:54 UTC', '2017-07-31 11:42:35 UTC'], ['2017-07-31 11:44:11 UTC', '2017-07-31 11:56:38 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 11:56:41 UTC', '2017-07-31 12:07:33 UTC'], ['2017-07-31 12:09:06 UTC', '2017-07-31 12:22:25 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 12:22:28 UTC', '2017-07-31 12:33:56 UTC'], ['2017-07-31 12:35:30 UTC', '2017-07-31 12:48:12 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 12:48:15 UTC', '2017-07-31 12:59:22 UTC'], ['2017-07-31 13:00:57 UTC', '2017-07-31 13:13:59 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 13:14:02 UTC', '2017-07-31 13:25:36 UTC'], ['2017-07-31 13:27:11 UTC', '2017-07-31 13:39:46 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 13:39:49 UTC', '2017-07-31 13:51:07 UTC'], ['2017-07-31 13:52:41 UTC', '2017-07-31 14:05:33 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 14:05:36 UTC', '2017-07-31 14:18:27 UTC'], ['2017-07-31 14:20:02 UTC', '2017-07-31 14:31:19 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 14:31:22 UTC', '2017-07-31 14:42:49 UTC'], ['2017-07-31 14:44:24 UTC', '2017-07-31 14:57:07 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 14:57:10 UTC', '2017-07-31 15:07:23 UTC'], ['2017-07-31 15:08:57 UTC', '2017-07-31 15:22:54 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 15:22:57 UTC', '2017-07-31 15:34:06 UTC'], ['2017-07-31 15:35:41 UTC', '2017-07-31 15:48:41 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 15:48:44 UTC', '2017-07-31 16:01:17 UTC'], ['2017-07-31 16:02:51 UTC', '2017-07-31 16:14:27 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 16:14:30 UTC', '2017-07-31 16:24:14 UTC'], ['2017-07-31 16:25:48 UTC', '2017-07-31 16:40:14 UTC']]))

shows.append(show("Akashic Records of Bastard Magic Instructor", 'akash', timedelta(seconds = 6.5)))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 17:00:57 UTC', '2017-07-31 17:13:08 UTC'], ['2017-07-31 17:14:43 UTC', '2017-07-31 17:26:51 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 17:26:55 UTC', '2017-07-31 17:40:24 UTC'], ['2017-07-31 17:41:57 UTC', '2017-07-31 17:52:46 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 17:52:50 UTC', '2017-07-31 18:00:55 UTC'], ['2017-07-31 18:02:30 UTC', '2017-07-31 18:18:43 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 18:18:47 UTC', '2017-07-31 18:31:46 UTC'], ['2017-07-31 18:33:20 UTC', '2017-07-31 18:44:52 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 18:44:56 UTC', '2017-07-31 18:56:29 UTC'], ['2017-07-31 18:58:01 UTC', '2017-07-31 19:10:54 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 19:10:58 UTC', '2017-07-31 19:20:48 UTC'], ['2017-07-31 19:22:22 UTC', '2017-07-31 19:37:00 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 19:37:04 UTC', '2017-07-31 19:50:54 UTC'], ['2017-07-31 19:52:27 UTC', '2017-07-31 20:03:05 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 20:03:09 UTC', '2017-07-31 20:13:56 UTC'], ['2017-07-31 20:15:01 UTC', '2017-07-31 20:28:32 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 20:28:36 UTC', '2017-07-31 20:38:13 UTC'], ['2017-07-31 20:39:16 UTC', '2017-07-31 20:54:20 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 20:54:24 UTC', '2017-07-31 21:04:54 UTC'], ['2017-07-31 21:05:59 UTC', '2017-07-31 21:20:00 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 21:20:04 UTC', '2017-07-31 21:32:28 UTC'], ['2017-07-31 21:33:32 UTC', '2017-07-31 21:45:48 UTC']]))
shows[len(shows) - 1].episodes.append(ep([['2017-07-31 21:45:52 UTC', '2017-07-31 21:53:08 UTC'], ['2017-07-31 21:54:12 UTC', '2017-07-31 22:10:45 UTC']]))

shows.append(show("Free! Iwatobi Swim Club", 'free'))

#shows.append(show("Mob Psycho 100", 'mob2'))
#shows.append(show("Miss Kobayashi's Dragon Maid", 'koba2'))
#shows.append(show("Yuri!!! on Ice", 'yuri2'))

#-----Convert and offset the hard-coded episode start/break/end times
for show in shows:
    for ep in show.episodes:
        for timeRange in ep.ranges:
            for timeIndex, time in enumerate(timeRange):
                timeRange[timeIndex] = datetime.strptime(time, overrustleFormat) + show.offset

#-----Load and Setup Emotes
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

#-----Load Chat & Get Sorted Msg Log
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
            times[time] = [1, 0, time + timedelta(seconds = 1)]
            if len(times) > 1:
                times[prevtime][2] = time
            prevtime = time
        msgsRaw.append(chatmsg(time, tempdata[0], tempdata[1][1:]))

for msgInd, msg in enumerate(msgsRaw):
    time = msg.dt
    msg.dt += timedelta(milliseconds = floor(((times[time][2] - time).seconds*1000) * times[time][1] / times[time][0]))
    times[time][1] += 1
        
msgSeries = Series((chatmsgitem for chatmsgitem in msgsRaw), (chatmsgitem.dt for chatmsgitem in msgsRaw))    

#-----Build the episode message series'
for show in shows:
    for ep in show.episodes:
        rangeGap = timedelta(0);
        for trInd, timeRange in enumerate(ep.ranges):
            ep.msgs = ep.msgs.append(Series(copy.deepcopy((msgSeries[timeRange[0]:timeRange[1]].rename(lambda x: x - rangeGap)).values), copy.deepcopy((msgSeries[timeRange[0]:timeRange[1]].rename(lambda x: x - rangeGap)).index)))
            if trInd < (len(ep.ranges) - 1):
                ep.msgs = ep.msgs.append(Series([chatmsg((timeRange[1] - rangeGap) + timedelta(seconds = 1), "_TCRMSG", "SNACK TIME"), chatmsg("0", "", "")], [(timeRange[1] - rangeGap) + timedelta(seconds = 1), 0]).drop(0))
                rangeGap += (ep.ranges[trInd+1][0] - timeRange[1]) - timedelta(seconds = 1) #adjust the next range by the gap
            else: 
                ep.msgs = ep.msgs.append(Series([chatmsg(timeRange[1] - rangeGap + timedelta(seconds = 1), "_TCRMSG", "FIN"), chatmsg("0", "", "")], [timeRange[1] - rangeGap + timedelta(seconds = 1), 0]).drop(0))

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
        with open(dir + dataSubDir + show.short + str(epInd + 1) + '.json', 'w', encoding='utf-8') as outfile:
            ep.msgs.to_json(outfile, orient = 'split', force_ascii = False, default_handler = chatmsg.toJSON)
            
with open(dir + dataSubDir + 'shows.json', 'w', encoding = 'utf-8') as outfile:
    json.dump(shows, outfile, cls = showEncoder)
        