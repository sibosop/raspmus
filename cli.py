#!/usr/bin/env python
import subprocess
import platform
import os
import sys
os.environ['DISPLAY']=":0.0"
os.chdir(os.path.dirname(sys.argv[0]))
pname = sys.argv[0]
home = os.environ['HOME']
sys.path.append("sibcommon")
defaultSpecPath = "%s/%s"%("speclib","raspmus.json")
from hosts import Hosts
from specs import Specs
import json
import argparse
import readline
import select
import time
import traceback
from debug import Debug

isRaspberry=platform.uname()[1] == 'raspberrypi'
defParse=None

def sendCargs(p,cargs):
  if len(p.name) + len(p.ip) + len(p.sub) == 0:
    Hosts().sendToHosts(cargs)
    return 0
  if len(p.name) != 0:
    Hosts().sendByName(p.name,cargs)
  if len(p.sub) != 0:
    Hosts().sendWithSubnet(p.sub,cargs)
  if len(p.ip) != 0:
    for h in parms.ip:
      print "h:",h
      Hosts().sendToHost(h,cargs)
  return 0

def doCmd(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parms=parse.parse_args(cmd[1:])
  sendCargs(parms,{'cmd' : cmd[0], 'args' : [""] })
  return 0

def doMasterCmd(cmd):
  Hosts().sendToMaster({'cmd' : cmd[0], 'args' : [""] })
  return 0

def doMasterArg(cmd):
  Hosts().sendToMaster({'cmd' : cmd[0], 'args' : [cmd[1]] })
  return 0

def doHaltMusic(cmd):
  hmcmd = { 'cmd' : 'HaltMusic', 'args' : [""] }
  hscmd = { 'cmd' : 'HaltSound', 'args' : [""] }
  hosts = Hosts().getHosts()
  for h in hosts:
    if h['hasMusicPlayer']:
      Hosts().sendToHost(h['ip'],hmcmd)
  for h in hosts:
    if h['hasMusic']:
      Hosts().sendToHost(h['ip'],hscmd)
  return 0

def doStartMusic(cmd):
  smcmd = { 'cmd' : 'StartMusic', 'args' : [""] }
  hosts = Hosts().getHosts()
  for h in hosts:
    if h['hasMusicPlayer']:
      Hosts().sendToHost(h['ip'],smcmd)
  return 0


  
def doNum(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('value',type=int,nargs=1)
  parms=parse.parse_args(cmd[1:])
  print parms.value
  args = {}
  args['value'] = parms.value[0]
  sendCargs(parms,{'cmd' : cmd[0], 'args' :  args})
  return 0

def doShow(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('words',nargs='*',default=[])
  parse.add_argument('-c','--color',nargs=1,default=["FFFF00"])
  parms=parse.parse_args(cmd[1:])
  phrase = ""
  for c in parms.words:
    phrase += c + " "
  args={}
  args['phrase'] = phrase
  args['color'] = parms.color[0]
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0
  
def doUpgrade(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parms=parse.parse_args(cmd[1:])
  args={}
  args['timeout'] = 30
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0
  
def doPlay(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('path',nargs='?',default="")
  parms=parse.parse_args(cmd[1:])
  print parms
  args={}
  args['path'] = parms.path
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0
  


langFile = "specs/lang_codes.json"
langs=[]
def getLangs():
  global langs
  if len(langs) == 0:
    with open(langFile) as f:
      langs = json.load(f)
  return langs

def doPhrase(cmd):
  parse=argparse.ArgumentParser(prog=cmd[0],parents=[defParse]) 
  parse.add_argument('words',nargs='*',default=[])
  parse.add_argument('-r','--reps',type=int,nargs=1,default=[1],help='set number of repititions (default 1)')
  parse.add_argument('-v','--vol',type=int,nargs=1,default=[100],help='set volume [default 100]')
  parse.add_argument('-l','--lang',type=str,nargs=1,default=["en"],help='set language',choices=getLangs())
  parse.add_argument('-d','--scat',action='store_true',help='set scatter')
  parse.add_argument('-f','--factor',nargs=1,type=float,default=[1.0],help='pitch factor x.x')
  parms=parse.parse_args(cmd[1:])
  phrase = ""
  for c in parms.words:
    phrase += c + " "
  args = {}
  args['phrase'] = phrase
  args['reps'] = parms.reps[0]
  args['scatter'] = parms.scat
  args['lang'] = parms.lang[0]
  args['vol'] = parms.vol[0]
  args['factor'] = parms.factor[0]
  sendCargs(parms,{'cmd' : cmd[0], 'args' : args })
  return 0

def doQuit(args):
  print "bye"
  readline.write_history_file()
  return -1
  
def kbfunc(): 
  i,o,e = select.select([sys.stdin],[],[],0.0001)
  for s in i:
     if s == sys.stdin:
       input = sys.stdin.readline()
       return True
  return False
  
def doTest(args):
  print "Hit return to stop test"
  hosts = Hosts().getHosts()
  loop = True
  while loop:
    for h in hosts:
      vs = h['ip'].split(".")
      cmd = []
      cmd.append("Phrase")
      cmd.append("%s"%(vs[3]))
      cmd.append("-r")
      cmd.append("0")
      cmd.append("-s")
      cmd.append("%s"%(vs[3]))
      stop = "Phrase -s %s"%(vs[3])
      print ("host %s sub %s cmd %s"%(h['ip'],vs[3],cmd))
      doPhrase(cmd)
      i,o,e = select.select([sys.stdin],[],[],5)
      cmd = []
      cmd.append("Phrase")
      cmd.append("-s")
      cmd.append("%s"%(vs[3]))
      doPhrase(cmd)
      if len(i):
        loop = False
        input = sys.stdin.readline()
        break
      
      
    

   
def printCmds(cmd):
  print "RaspMus Commands:"
  for c in cmds:
    print(c)
  print

cmds = {
  'Collection'      : doMasterArg
  ,'CollectionList' : doMasterCmd
  ,'HaltMusic'      : doHaltMusic
  ,'HaltSound'     : doCmd
  ,'Help'           : printCmds
  ,'MaxEvents'      : doNum
  ,'Phrase'         : doPhrase
  ,'Play'           : doPlay
  ,'Poweroff'       : doCmd
  ,'Probe'          : doCmd
  ,'Quit'           : doQuit
  ,'Reboot'         : doCmd
  ,'Restart'        : doCmd
  ,'StartMusic'     : doStartMusic
  ,'Show'           : doShow
  ,'SoundVol'       : doNum
  ,'Stop'           : doCmd
  ,'Test'           : doTest
  ,'Threads'        : doNum
  ,'Upgrade'        : doUpgrade
  ,'Volume'         : doNum
}


def completer(text, state):
  options = [i for i in cmds.keys() if i.upper().startswith(text.upper())]
  if state < len(options):
      return options[state]
  else:
      return None
    


  

if __name__ == '__main__':
  run=True
  try:
    readline.read_history_file()
  except:
    pass
  if isRaspberry:
    readline.parse_and_bind("tab: complete")
  else:
    readline.parse_and_bind("bind ^I rl_complete")
  readline.set_completer(completer)
  parser = argparse.ArgumentParser()
  parser.add_argument('-c','--config',nargs=1,type=str,default=[defaultSpecPath],help='specify different config file')
  args = parser.parse_args()
  print ("config path %s"%args.config)
  Debug(['specs'])
  Specs(args.config[0])
  Debug().enable(Specs().s['debug'])
  Debug().enable(['hosts'])
  Hosts().printHostList()
  printCmds("")
    
  cmdParser = argparse.ArgumentParser()
  cmdParser.add_argument('cmd',nargs=1,type=str,default=['Help'],choices=cmds.keys())
  
  while run:
    try:
      inp=raw_input("raspmus-> ").split()
      cmdargs = cmdParser.parse_args([inp[0]])
      defParse=argparse.ArgumentParser(add_help=False) 
      defParse.add_argument('-i','--ip',nargs='+',default=[],help='specify dest ip')
      defParse.add_argument('-s','--sub',nargs='+',default=[],help='specify dest ip using subnet')
      defParse.add_argument('-n','--name',nargs='+',default=[],help='specify dest ip by name')
      if cmds[cmdargs.cmd[0]](inp) == -1:
        break
    except KeyboardInterrupt:
      doQuit("")
      break
    except Exception, e:
      traceback.print_exc()
      continue
    except:
      print "parse error"
      continue
        

