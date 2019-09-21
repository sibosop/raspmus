# raspmus
Step by step installation of raspmus

## setting up autoboot
* `crontab -e`

enter:
* `MAILTO=""`
* `@reboot sleep 5;/home/pi/GitProjects/netGarden/utils/asoundConfig.py 2>&1 | logger -t asoundConfig`
* `@reboot sleep 20; /home/pi/GitProjects/raspmus/raspmusWrap.sh 2>&1 | logger -t raspmus`

