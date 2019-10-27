#!/usr/bin/env python

import mido

togLocs = [17,23]

def sysex_to_data(sysex):
  data = [None] * len(sysex)
  cnt2 = 0
  bits = 0
  for cnt in range(0,len(sysex)):
    if ((cnt % 8) == 0):
      bits = sysex[cnt]
    else:
      data[cnt2] = sysex[cnt] | ((bits & 1) << 7)
      cnt2 += 1
      bits >>= 1
  return data[0:cnt2]

def data_to_sysex(data):
    sysex = [0]
    idx = 0
    cnt7 = 0

    for x in data:
        c = x & 0x7F
        msb = x >> 7
        sysex[idx] |= msb << cnt7
        sysex += [c]

        if cnt7 == 6:
            idx += 8
            sysex += [0]
            cnt7 = 0
        else:
            cnt7 += 1

    if cnt7 == 0:
        sysex.pop()
        
    return sysex



mido.set_backend('mido.backends.pygame')
print(mido.get_output_names())
print(mido.get_input_names())
o = mido.open_output('nanoKONTROL2 MIDI 1')
i = mido.open_input('nanoKONTROL2 MIDI 1')




dm = mido.Message('sysex', data=[0x42,0x40,0x00,0x01,0x13,0x00,0x1F,0x10,0x00])
print("dm %s"%(dm))
o.send(dm)
m = i.receive()
md = m.data
o.send(mido.Message('sysex',data=m.data))
t = i.receive()

print("message from loopback %s"%t)
for c in t.data:
  print("0x%x %d"%(c,c))

print("header data")
first = True
for c in range(0,12):
  print("%d: 0x%x %d"%(c,md[c],md[c]))
scene = sysex_to_data(md[12:])
for c in range(0,len(scene)):
  print ("%d: 0x%x %d"%(c,scene[c],scene[c]))

for y in range(0,8):
  for x in togLocs:
    scene[x+(y*31)] = 1
test = data_to_sysex(scene)
header = []
for c in range(0,12):
  header.append(md[c])
for t in test:
  header.append(t)
print("testlen %d"%len(header))
for c in range(0,len(test)):
 print("%d: 0x%x %d 0x%x %d"%(c,md[c],md[c],header[c],header[c]))
 if md[c] != header[c]:
   print("diff at %d: 0x%x %d 0x%x %d"%(c,md[c],md[c],header[c],header[c]))
 

o.send(mido.Message('sysex',data=header))
t = i.receive()
print("message from write back %s"%t)
for c in t.data:
  print("0x%x %d"%(c,c))

o.close()
i.close()
