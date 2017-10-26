from datetime import datetime, time, timedelta
from pandas import Series, date_range
from pytz import timezone
from colour import Color
import numpy as np
import pytz
import json
import jsonpickle
import re
import pickle
from random import random, uniform
from math import floor
import os 
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import colors as mcolors

class marathon():
    def __init__(self, title, chatLogFiles, badgeFiles):
        
        self.shows = []
        
        self.title = title        
        self.chatLogFiles = chatLogFiles
        self.badgeFiles = badgeFiles
        self.badgeNames = {}
        self.msgSeries = None

class show():
    def __init__(self, title, jsonName, anchorTime, offsetDelta, altArray, regex):
        
        self.episodes = []
        
        self.title = title
        self.jsonName = jsonName
        self.anchorTime = datetime.strptime(anchorTime, overrustleFormat)
        self.offsetDelta = timedelta(seconds = offsetDelta)
        self.altArray = altArray
        self.regex = regex
        
        self.plotEnd = None

class ep():
    def __init__(self, startDelta, delayDelta, periods):
        
        self.msgs = Series()
        
        self.startDelta = timedelta(seconds = startDelta)
        self.delayDelta = timedelta(seconds = delayDelta)
        self.periods = [[timedelta(seconds = period[0]), period[1]] for period in periods]
        self.periodsJSON = periods
        
        self.periodPlot = []

class chatmsg():
    def __init__(self, dt, n, m):
        self.dt = dt
        self.n = n
        self.m = m
        self.c = Color(pick_for = self.n, saturation = 0.7, luminance = uniform(0.3, 0.7)).hex
        self.ttvGEmotes = []
        self.bttvGEmotes = []
        self.ttvCEmotes = []
        self.badges = [[],[]]
    def toJSON(self):
        return [self.n, self.c, self.m, self.ttvGEmotes, self.bttvGEmotes, self.ttvCEmotes, self.badges]
    def buildBadge(self):
        tempBadge = []
        if random() < 27/360:
            tempBadge.append(2)
        if random() < 8/36:
            if random() < 9/73:
                tempBadge.append(0)
            else:
                tempBadge.append(1)
        self.badges = [tempBadge, []]

        
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
overrustleFormat = '%Y-%m-%d %H:%M:%S %Z'
badgeIds = {'turbo' : 0, 'premium' : 1, 'subscriber' : 2, 'moderator' : 3, 'bits' : 4, 'staff' : 5, 'global_mod' : 6, 'partner' : 7, 'admin' : 8, 'broadcaster' : 9}

dir = os.path.dirname(os.path.realpath(__file__)) + '\\'
logsSubDir = 'Logs\\'
dataSubDir = 'OutputData\\'
plotSubDir = 'PlotData\\'

marathons = []
marathons.append(marathon('crunchyroll', ['2017-07-27.txt', '2017-07-28.txt', '2017-07-29.txt', '2017-07-30.txt', '2017-07-31.txt', '2017-08-01.txt'], []))
marathons.append(marathon('RWBY', ['2017-10-09.txt', '2017-10-10.txt', '2017-10-11.txt', '2017-10-12.txt', '2017-10-13.txt', '2017-10-14.txt'], ['1b1.json', '1b2.json', '1b3.json']))
                          
#-----Load Emotes and Emoji
ttvGlobal = {}
with open(dir + logsSubDir + 'ttvGlobal2.json', 'r') as jd: #https://twitchemotes.com/api_cache/v3/global.json
    ttvGlobalJSON = json.load(jd)
    for emoteCode in ttvGlobalJSON:
        ttvGlobal[ttvGlobalJSON[emoteCode]['code']] = ttvGlobalJSON[emoteCode]['id']
    
bttvGlobal = {}
with open(dir + logsSubDir + 'bttvGlobal2.json', 'r') as jd: #https://api.betterttv.net/2/emotes
    bttvGlobalJSON = json.load(jd)
    for emote in bttvGlobalJSON['emotes']:
        bttvGlobal[emote['code']] = emote['id']

ttvCh = {}
with open(dir + logsSubDir + 'ttvChannels2.json', 'r') as jd: #https://twitchemotes.com/api_cache/v3/images.json
    ttvChJSON = json.load(jd)
    for emoteID in ttvChJSON:
        emote = ttvChJSON[emoteID]
        ttvCh[emote['code']] = emote['id']
        
emojiGlobal = {}
with open(dir + logsSubDir + 'emoji.json', encoding='utf-8') as jd: #https://www.npmjs.com/package/emoji.json
    emojiJSON = json.load(jd)
    for emoji in emojiJSON:
        emojiGlobal[':' + emoji['name'].replace(' ', '_') + ':'] = emoji['char']

#-----Load marathon specific items (chat and badges)
for marathon in marathons:
    #-----Load Badge Info
    for badgeFile in marathon.badgeFiles:
        if os.path.exists(dir + logsSubDir + badgeFile):
            with open(dir + logsSubDir + badgeFile) as jd:
                badgesJSON = json.load(jd)
                for name in badgesJSON:
                    if name not in marathon.badgeNames:
                        marathon.badgeNames[name] = [[], []]
                    if len(badgesJSON[name]) > len(marathon.badgeNames[name][0]): #if this has a new badge remake the badges
                        marathon.badgeNames[name] = [[], []]
                        for badge in badgesJSON[name]:
                            if badge['id'] in badgeIds:
                                marathon.badgeNames[name][0].append(badgeIds[badge['id']])
                                if badge['id'] == 'bits':
                                    marathon.badgeNames[name][1] = badge['version']
        
    #-----Load Chat & Get Sorted Msg Log
    if not os.path.exists(dir + logsSubDir + 'totalLog' + marathon.title + '.bin'):
        timeSmoothing = 2 #seconds
        msgsRaw = []
        count = 0
        prevTimes = {}
        
        for chatLogFile in marathon.chatLogFiles:
            print(chatLogFile)
            with open(dir + logsSubDir + chatLogFile, 'r', encoding='utf-8') as jd:
                for line in jd:
                
                    timeStamp = datetime.strptime(line[1:24], overrustleFormat)
                    timeStamp -= timedelta(seconds = (timeSmoothing - timeStamp.second % timeSmoothing) - 1)
                
                    if timeStamp not in prevTimes:
                        if len(msgsRaw) > 0:
                            prevTimes[timeStamp] = [timeStamp, 0]       #needed to keeptrack if we got to a new time (will be overwritten unless this is the last block total)
                            prevTimes[msgsRaw[-1][0].dt][0] = timeStamp #we finished prev block so set their 'next-time' to be this time
                            prevTimes[msgsRaw[-1][0].dt][1] = count     #and we now know the count of that block
                        else:
                            prevTimes[timeStamp] = [timeStamp, 0]
                        count = 0 #keeps track of the index this message should have after we bunch them

                    userAndMsg = line[26:].split(':', 1)
                    msgsRaw.append([chatmsg(timeStamp, userAndMsg[0], userAndMsg[1][1:]), count])
                    count += 1
                prevTimes[msgsRaw[-1][0].dt][1] = count
                    
        for msgInfo in msgsRaw: #Perform smoothing
            msgInfo[0].dt += timedelta(seconds = ((prevTimes[msgInfo[0].dt][0] - msgInfo[0].dt).total_seconds()) * (msgInfo[1] / prevTimes[msgInfo[0].dt][1]))

        marathon.msgSeries = Series((msgInfo[0] for msgInfo in msgsRaw), (msgInfo[0].dt for msgInfo in msgsRaw))    
        
        with open(dir + logsSubDir + 'totalLog' + str(marathon.title) + '.bin', 'wb') as jd:
            pickle.Pickler(jd).dump(marathon.msgSeries)
    else:
        print('Loading Marathon ' + str(marathon.title))
        with open(dir + logsSubDir + 'totalLog' + str(marathon.title) + '.bin', 'rb') as jd:
            marathon.msgSeries = pickle.Unpickler(jd).load()

#-----Load show and episode info
with open(dir + 'animeData.json', encoding='utf-8') as jd:
    animeJSON = json.load(jd)
    for marathonJSONid in animeJSON:
        for showJSONid in animeJSON[marathonJSONid]:
            showJSON = animeJSON[marathonJSONid][showJSONid]
            newShow = show(showJSON[0][0], showJSON[0][1], showJSON[0][2], showJSON[0][3], showJSON[0][4], showJSON[0][5])
            for epiJSONid in showJSON[1]:
                newShow.episodes.append(ep(showJSON[1][epiJSONid][0], showJSON[1][epiJSONid][1], showJSON[1][epiJSONid][2]))
            marathons[int(marathonJSONid)].shows.append(newShow)

#-----Adjust msgs for emojis and emotes and badges
for marathon in marathons:
    #-----Build the episode message series
    for show in marathon.shows:
        print('Building ' + show.title)
        for ep in show.episodes:
            epStartCalculated = show.anchorTime + ep.startDelta + show.offsetDelta + ep.delayDelta #anchorTime = estimate show start, startDelta = how many seconds into the series, offsetDelta = how far off anchorTime is, delayDelta = specific epi delay
            periodStart = epStartCalculated
            skippedChatSegments = timedelta(0)
            for period in ep.periods:
                ep.periodPlot.append([[periodStart, periodStart + period[0]], period[1]])
                
                if period[1] == 0:      #regular section so append messages
                    ep.msgs = ep.msgs.append(copy.deepcopy(marathon.msgSeries[periodStart : periodStart + period[0]].rename(lambda timeIndex: ((timeIndex - epStartCalculated) - skippedChatSegments).total_seconds())))
                elif period[1] == 1:    #skipped anime part (this didn't exist for chat, but it does for us, we simply don't append chat) [pulling chat data is meaningless cuz chat wasn't watching this]
                    True #nothing
                else:                   #chatbreak (this doesn't exist for us (we don't watch breaks), but exists for chat, we cut it out by progressing without putting msgs and adding a skip to reindex future messages so we don't get minutes of nothing
                    skippedChatSegments += period[0]
                    
                periodStart += period[0]
                    
        show.plotEnd = periodStart + timedelta(minutes = 5) #just for plotting, doesn't matter we just wanna get past the end of the final ep
        
        #-----Here we edit messages for emojis, so we do this first
        for ep in show.episodes:
            for msg in ep.msgs:
                parts = [(m.group(0), (m.start(), m.end()-1)) for m in re.finditer(r'\S+', msg.m)]
                found = False
                reMsg = ''
                for part in parts:
                    if part[0] in emojiGlobal:
                        reMsg += emojiGlobal[part[0]] + ' '
                        found = True
                    else:
                        reMsg += part[0] + ' '
                if found:
                    msg.m = reMsg
        
        #-----Create the emote arrays
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
                #Generate badges
                if len(marathon.badgeNames) is 0:
                    msg.buildBadge()
                else:
                    if msg.n in marathon.badgeNames:
                        msg.badges = marathon.badgeNames[msg.n]
                    
#-----Output data files
showOutput = []
for marathon in reversed(marathons):
    for show in marathon.shows:
        for epInd, ep in enumerate(show.episodes):
            with open(dir + dataSubDir + show.jsonName + str(epInd + 1) + '.json', 'w', encoding='utf-8') as outfile:
                ep.msgs.to_json(outfile, orient = 'split', force_ascii = False, default_handler = chatmsg.toJSON) #orient = 'index'
                
    showOutput.extend([[show.title, len(show.episodes), show.altArray, [[j for j in i.periodsJSON if j[1] is not 2] for i in show.episodes], show.regex] for show in marathon.shows if show.regex is not None])

with open(dir + dataSubDir + 'shows.json', 'w', encoding = 'utf-8') as outfile:
    json.dump(showOutput, outfile)
                
        
#-----Do Text/Plot Analysis
if True:
    for marathon in marathons:
        for show in marathon.shows:
            print('text show ' + show.title);
            plotXMax = floor((show.plotEnd - show.anchorTime).total_seconds()) + 1
            msgCountArray = {}
            
            msgCountArray['all'] = [[], 30, r'', colors['gray']]
            msgCountArray['ree'] = [[], 20, r'\b(r+e{2,})\b', 'b']
            msgCountArray['lul'] = [[], 30, r'l+u+l+|l+o+l+|r+o+f+l+|l+m+a+o+', colors['limegreen']]
            msgCountArray['bib'] = [[], 30, r'biblethump', colors['pink']]
            msgCountArray['pog'] = [[], 20, r'pogchamp', colors['brown']]
            
            for sec in [show.anchorTime + timedelta(seconds = x) for x in range(plotXMax)]:
                for msgType in msgCountArray:
                    msgTypeInfo = msgCountArray[msgType]
                    msgTypeInfo[0].append(len([msg for msg in marathon.msgSeries[sec - timedelta(seconds = msgTypeInfo[1] / 2) : sec + timedelta(seconds = msgTypeInfo[1] / 2)] if re.search(msgTypeInfo[2], msg.m, re.I) is not None]) / msgTypeInfo[1])
            
            show.plotSave = [msgCountArray, []]
            
            fig, ax = plt.subplots(1)
            ax.plot()
            lines = {}
            plotYMax = max(msgCountArray['all'][0])
            
            for msgType in msgCountArray:
                msgTypeInfo = msgCountArray[msgType]
                lines[msgType] = ax.plot(range(plotXMax), msgTypeInfo[0], msgTypeInfo[3], label = msgType);
            
            ax.axis([0, plotXMax, 0, plotYMax])
            ax.set_title(show.title)
            ax.set_xlabel('Play time (seconds)')
            ax.set_ylabel('Messages per second')

            for ep in show.episodes:
                ax.plot([(ep.periodPlot[0][0][0] - show.anchorTime).total_seconds(), (ep.periodPlot[0][0][0] - show.anchorTime).total_seconds()], [0, plotYMax], colors['green']);
                ax.plot([(ep.periodPlot[-1][0][1] - show.anchorTime).total_seconds(), (ep.periodPlot[-1][0][1] - show.anchorTime).total_seconds()], [0, plotYMax], colors['red']);
                
                plotProcess = [[[(period[0][0] - show.anchorTime).total_seconds(), (period[0][1] - period[0][0]).total_seconds()], period[1]] for period in ep.periodPlot]
                
                for period in plotProcess:
                    if period[1] == 0: #section
                        ax.add_patch(patches.Rectangle((period[0][0], 0), period[0][1], plotYMax, alpha=0.2, edgecolor='none', facecolor=colors['limegreen']))
                    elif period[1] == 1: #skip (actually part of the anime)
                        ax.add_patch(patches.Rectangle((period[0][0], 0), period[0][1], plotYMax, alpha=0.2, edgecolor='none', facecolor=colors['red']))
                    else:  #chatbreak (invisible, we cut it out)
                        ax.add_patch(patches.Rectangle((period[0][0], 0), period[0][1], plotYMax, alpha=0.2, edgecolor='none', facecolor=colors['yellow']))
                
                show.plotSave[1].append(plotProcess)
                
            with open(dir + plotSubDir + show.jsonName + 'plot.json', 'w') as outfile:
                json.encoder.FLOAT_REPR = lambda f: ("%.1f" % f)
                json.dump(show.plotSave, outfile)
                
    plt.show()

