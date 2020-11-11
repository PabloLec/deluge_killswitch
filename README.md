# What is it ?
This python script is meant to be used a Deluge kill switch. It verifies that your public IP is not the same as the one used on Deluge.
If your IP is not protected, it will pause all your torrents. Deluge daemon is not really killed in order to preserve the data you didn't send to the trackers yet. This way, if you wish to fix your IP issue you can easily resume your torrenting.


# Requirements
- Python 3+
- Deluge 2+
- deluge-console 2+
- dnsutils

To install dependencies:
```
sudo apt install python3 deluge deluged deluge-console dnsutils
```


# How to use it ?
You'll need a torrent that returns your IP in the tracker status. There is a few different working ones, consider using http://checkmytorrentip.net.
Add the torrent to your client, then, grab its hexadecimal hash (e.g 2fa71a2dbb7d53a39373a9c4e2c9d89aaa7a6db1) in your client or deluge-console.
In the GUI you have to click on the torrent and you will find the hash in the "Details" tab.


Open the script and replace the "TORRENT_ID" value in the beginning with your hash.
You may also change "DELUGE_PATH" if you need to.
If you don't want to start the Deluge daemon if it is currently stopped, change "START_DAEMON_IF_STOPPED" to False.


Finally, simply run the script. You'd probably want to make it a cron job.


# Troubleshooting
If you have deluge-console related exceptions, try adding "sudo -u [your system user]" before every "deluge-console" in the script. All users do not have access to the deluge daemon.
