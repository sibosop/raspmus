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
    3) logger doing poweroff; sudo poweroff
    ;;
    4) logger doing reboot; sudo reboot
    ;;
    5) logger doing stop; exit 0
    ;;
    6) logger doing restart
    ;;
    *)
    ;;
  esac
done
