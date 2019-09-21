# raspmus
Step by step installation of raspmus

## get projects
* `mkdir -p ~/GitProjects`
* `cd !$`
* `git clone git@github.com:sibosop/bashenv.git`
* `git -C bashenv checkout raspi`
* `git clone git@github.com:sibosop/sibcommon.git`
* `git clone git@github.com:sibosop/speclib.git`
* `git clone git@github.com:sibosop/raspmus.git`
* `rm -rf ~/bashrc.d ~/.vimrc`
* `cd bashenv; ./onetimesetup.sh`

## setting up autoboot
* `crontab -e`

enter:
* `MAILTO=""`
* `@reboot sleep 5;/home/pi/GitProjects/sibcommon/asoundConfig.py 2>&1 | logger -t asoundConfig`
* `@reboot sleep 20; /home/pi/GitProjects/raspmus/raspmusWrap.sh 2>&1 | logger -t raspmus`

