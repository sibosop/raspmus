#!/usr/bin/env python
import os
import sys
os.environ['DISPLAY']=":0.0"
os.chdir(os.path.dirname(sys.argv[0]))
pname = sys.argv[0]
home = os.environ['HOME']
sys.path.append("sibcommon")
defaultSpecPath = "%s/%s"%("speclib","raspmus.json")
import datetime
import time
import argparse
import json
import subprocess
import traceback
import signal
import pygame

from hosts import Hosts
from asoundConfig import setVolume
from debug import Debug
from server import Server
from specs import Specs
from iAltarPlayer import iAltar
from displayHandler import DisplayHandler
from soundTrack import SoundTrackManager
from musicPlayer import MusicPlayer
from shutdown import Shutdown
from phraseHandler import PhraseHandler
from musicPlayer import MusicPlayer
from watchdog import Watchdog
from voice import Voice

gardenExit = 0


  
class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

def service_shutdown(signum, frame):
    Debug().p('Caught signal %d' % signum)
    raise ServiceExit

if __name__ == '__main__':
  try:
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    print("%s at %s"%(pname,datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.init()
    parser = argparse.ArgumentParser() 
    parser.add_argument('-c','--config',nargs=1,type=str,default=[defaultSpecPath],help='specify different config file')
    parser.add_argument('-s','--soundDir',nargs=1,help='specify sound file directory')
    args = parser.parse_args()
    Debug(['specs',"__main__"])
    Debug().p("config path %s"%args.config[0])
    specs = Specs(args.config[0]).s
    Debug().enable(specs['debug'])
    soundDir = specs['defaultSoundDir']
    if args.soundDir is not None:
      soundDir = args.soundDir[0]
      
    if "masterVolume" in specs:
      setVolume(specs['masterVolume'])
    
    if Hosts().getLocalAttr('hasServer'):
      sst = Server(8080)
      sst.setDaemon(True)
      sst.start()
      
    if Hosts().getLocalAttr('hasDisplay'):
      dht = DisplayHandler()
      dht.setDaemon(True)
      dht.start()
      
    
      
    if Hosts().getLocalAttr('hasMusic'):
      SoundTrackManager(soundDir).changeNumSoundThreads(specs['numMusicThreads'])
      
    if Hosts().getLocalAttr('hasPowerCheck'):
      pct = Shutdown()
      pct.setDaemon(True)
      pct.start()
      
    if Hosts().getLocalAttr('hasPhrase'):
      pht = PhraseHandler()
      pht.setDaemon(True)
      pht.start()
      
    if Hosts().getLocalAttr('hasVoice'):
      vt = Voice()
      vt.setDaemon(True)
      vt.start()
       
    if Hosts().getLocalAttr('hasiAltarPlayer'):
      iat = iAltar()
      iat.setDaemon(True)
      iat.start()

    gardenExit = 6
    if Hosts().getLocalAttr('hasMusicPlayer'):
      mpt = MusicPlayer()
      mpt.setDaemon(True)
      mpt.start()
      
    while True:
      time.sleep(1)

  except Exception as e:
    print("%s"%e)
    traceback.print_exc()
    gardenExit = 5

  print("%s exiting"%pname)
  exit(gardenExit)

