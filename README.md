# raspmus
Step by step installation of raspmus

## get projects
* `mkdir ~/GitProjects`
* `cd !$`
* `git clone git@github.com:sibosop/sibcommon.git`
* `git clone git@github.com:sibosop/speclib.git`
* `git clone 

## setting up autoboot
* `crontab -e`

enter:
* `MAILTO=""`
* `@reboot sleep 5;/home/pi/GitProjects/netGarden/utils/asoundConfig.py 2>&1 | logger -t asoundConfig`
* `@reboot sleep 20; /home/pi/GitProjects/raspmus/raspmusWrap.sh 2>&1 | logger -t raspmus`

