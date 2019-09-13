#!/usr/bin/env python
import os
import sys
os.environ['DISPLAY']=":0.0"
os.chdir(os.path.dirname(sys.argv[0]))
pname = sys.argv[0]
home = os.environ['HOME']
sys.path.append("sibcommon")
defaultSpecPath = "%s/%s"%("specs","raspmus.json")
import datetime
import time
import argparse
from hosts import Hosts
import subprocess
from asoundConfig import setVolume
from utils import print_dbg
from utils import setDebug
from server import Server
from specs import Specs
import json

numGardenThreads=1
gardenExit = 0
isMasterFlag = False;

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
    parser = argparse.ArgumentParser() 
    parser.add_argument('-d','--debug', action = 'store_true',help='set debug')
    parser.add_argument('-c','--config',nargs=1,type=str,default=[defaultSpecPath],help='specify different config file')
    args = parser.parse_args()
    setDebug(args.debug)
    print_dbg("config path %s"%args.config[0])
    specs = Specs(args.config[0]).s
  except Exception, e:
    print("config error:"+str(e))
    exit(5)


  if "masterVolume" in specs:
    setVolume(specs['masterVolume'])
  isMasterFlag =Hosts().getLocalAttr('isMaster')
  print_dbg("isMaster: %s"%(isMasterFlag))
  sst = Server(8080)
  sst.registerCommand("Probe",doProbe)
  sst.setDaemon(True)
  sst.start()
#  soundTrack.setup()
#  gardenTrack.changeNumGardenThreads(numGardenThreads)
#  speakThread = gardenSpeak.gardenSpeakThread()
#  speakThread.setDaemon(True)
#  speakThread.start()
#  if isMasterFlag:
#    print("starting player")
#    pt = player.playerThread()
#    pt.setDaemon(True)
#    pt.start()
  while gardenExit == 0:
    try:
      time.sleep(5)
    except KeyboardInterrupt:
      print("%s: keyboard interrupt"%pname)
      gardenExit = 5
      break
    except Exception as e:
      print("%s"%e)
      break

  print("%s exiting"%pname)
  exit(gardenExit)

