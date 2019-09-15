#!/usr/bin/env python
import os
import sys
import pygame
os.environ['DISPLAY']=":0.0"
os.chdir(os.path.dirname(sys.argv[0]))
pname = sys.argv[0]
home = os.environ['HOME']
sys.path.append("sibcommon")
defaultSpecPath = "%s/%s"%("speclib","raspmus.json")
import datetime
import time
import argparse
from hosts import Hosts
import subprocess
import traceback
from asoundConfig import setVolume
from utils import print_dbg
from utils import setDebug
from server import Server
from specs import Specs
import json
from soundTrack import SoundTrackManager
from musicPlayer import MusicPlayer

gardenExit = 0

def doProbe(args):
  state = {}
  state['status'] = "ok"
  attr = Hosts().getHost(Hosts.getLocalHost())
  for k in attr.keys():
    state[k]=attr[k]
  return json.dumps(state)



if __name__ == '__main__':
  try:
    print("%s at %s"%(pname,datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.init()
    parser = argparse.ArgumentParser() 
    parser.add_argument('-v','--verbose', action = 'store_true',help='set debug')
    parser.add_argument('-c','--config',nargs=1,type=str,default=[defaultSpecPath],help='specify different config file')
    parser.add_argument('-s','--soundDir',nargs=1,help='specify sound file directory')
    args = parser.parse_args()
    setDebug(args.verbose)
    print_dbg("config path %s"%args.config[0])
    specs = Specs(args.config[0]).s
    soundDir = specs['defaultSoundDir']
    if args.soundDir is not None:
      soundDir = args.soundDir[0]
      
    if "masterVolume" in specs:
      setVolume(specs['masterVolume'])
    
    if Hosts().getLocalAttr('hasServer'):
      sst = Server(8080)
      sst.registerCommand("Probe",doProbe)
      sst.setDaemon(True)
      sst.start()
      if Hosts().getLocalAttr('hasMusic'):
        SoundTrackManager(soundDir).changeNumSoundThreads(specs['numMusicThreads'])

    if Hosts().getLocalAttr('hasMusicPlayer'):
      print("starting Music Player")
      pt = MusicPlayer()
      pt.setDaemon(True)
      pt.start()
    
    while gardenExit == 0:
      try:
        time.sleep(5)
      except KeyboardInterrupt:
        print("%s: keyboard interrupt"%pname)
        gardenExit = 5
        break
  except Exception as e:
    print("%s"%e)
    traceback.print_exc()
    gardenExit = 5

  print("%s exiting"%pname)
  exit(gardenExit)

