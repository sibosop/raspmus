# raspmus
Step by step installation of raspmus

## sd card setup
* reformat card with sdformatter app on mac
* put latest noobs on sdcard
* Make a NOOBS Directory and unzip it there since the unzip doesn't spec a top dir
* Copy NOOBS contents to sdcard
* start up with ethernet cable 
* make sure to specify US keyboard on install screen
* select preferemces->Rasberry Pi Configuration->interfaces and enable ssh
* for linksys router got to connectivity->local networks and hardwire dhcp settings for the raspi wifi
* ifconfig will show the current wlan number

## ssh and network setup
* on raspi `ssh-keygen` to generate a ssh key for github and also create a .ssh dir
* cut and paste .ssh/id_rsa.pub contents into raspi .ssh/authorized_keys
* cut and paste the rasp id_ras.pub into the git hub keys
* The wifi config file: `sudo vi /etc/wpa_supplicant/wpa_supplicant.conf`
## afp (file sharing)
* https://pimylifeup.com/raspberry-pi-afp/

## fixing the wi-fi on older machines with dongles
* `sudo vi /etc/modprobe.d/8192cu.conf`
* add the line `options 8192cu rtw_power_mgnt=0 rtw_enusbss=0`
* reboot
### update the os use apt-get since apt tends to screw up terminal screens
* `sudo apt-get update`
* `sudo apt-get purge wolfram-engine`
* `sudo apt-get upgrade`
### do this if you are already screwed by wolfram
* `sudo dpkg --remove --force-remove-reinstreq wolfram-engine`
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
## update the bashrc
* put theses lines at the bottom of ~/.bashrc:
*
* export PATH=$PATH:~/bin
* bashdir=bashrc.d
* pushd $HOME > /dev/null
* for f in `` `ls $bashdir` ``; do
*   source $bashdir/$f
* done
* popd > /dev/null
### fix the fstab
* `cd $sibcommon`
* `sudo cp fstab /etc/fstab`
### make sure the syslog rotation is daily not weekly
check the log file daily since the directory is now smaller, change weekly to daily
keep only two days
* `sudo vi /etc/logrotate.conf`
### get rid of user messages log which are redundant
`sudo cp $sibcommon/rsyslog.conf /etc/rsyslog.conf`
### update the support packages (fix swap)
* `cd $sibcommon`
* `./packageSetup.sh`

### if thumbdrive has wrong name
* `sudo dosfslabel /dev/sda1 ARCHIVE`

#### Monitor setup information
* stop screen blanking by going to preferences->xscreensaver and default it to off
* configure small screen (hdmi_drive=1 has been added here to remove purple line on left side of screen which
* began to appear on versions after 3/01/2017)
  * `sudo vi /boot/config.txt`
  * add lines
     * `hdmi_force_hotplug=1`
     * `hdmi_group=2`
     * `hdmi_mode=1`
     * `hdmi_drive=1`
     * `hdmi_mode=87`
     * `hdmi_cvt 800 480 60 6 0 0 0`
* if using large screen then
  * add lines 
    * `hdmi_force_hotplug=1`
    * `hdmi_group=2`
    * `hdmi_mode=1`
    * `hdmi_drive=1`
    * `hdmi_mode=82`
* if the HDMI screen does not fill out to the edges then
* uncomment this line
  * disable_overscan=1

## setting up autoboot
### first time setup
* `crontab -e`
* Note: use -c with relative path (speclib/<json file) if it's not raspmus.json
* `MAILTO=""`
* `@reboot sleep 10;/home/pi/GitProjects/sibcommon/asoundConfig.py 2>&1 | logger -t asoundConfig`
* `@reboot sleep 20; /home/pi/GitProjects/raspmus/raspmusWrap.sh 2>&1 | logger -t raspmus`

## Manual upgrade
* `git -C ~/GitProjects/bashenv pull origin raspi`
* `cd $raspmus`
* `git pull origin master`
* `git -C sibcommon pull origin master`
* `git -C speclib pull origin master`

### Midi (mido) setup
* `import mido`
* `mido.set_backend('mido.backends.pygame')`
* `mido.mido.get_input_names()`
  * _[u'Midi Through Port-0', u'nanoKONTROL2 MIDI 1'_
* `port = mido.open_input('nanoKONTROL2 MIDI 1')`
* `message = port.receive()`
* `print message`
  * _control_change channel=0 control=5 value=84 time=0_
  
### Speech Recog notes
The versions from pip are old.

The latest version is here:

https://pypi.org/project/pyalsaaudio/

download the tar file, untar it and do
`sudo ./setup.py install`
#### credential install location
* `cd ~` 
* `mkdir apiKeys`
* `cd !$`
* ln -s ~/.config/gcloud/application_default_credentials.json` recog.json
