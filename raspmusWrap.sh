#!/bin/bash

while true; do
  args=""
  for i in $@
  do
    args="$args $i "
  done
  /home/pi/GitProjects/raspmus/raspmus.py $args
  rc=$?
  case $rc in
    3) echo doing poweroff; sudo poweroff
    ;;
    4) echo doing reboot; sudo reboot
    ;;
    5) echo doing stop; exit 0
    ;;
    6) echo doing restart
    ;;
    *)
    ;;
  esac
done
