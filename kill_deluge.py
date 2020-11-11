import os, sys, re, subprocess, time
from datetime import datetime

#############################################################################
# ENTER THE HEXADECIMAL HASH OF THE TORRENT YOU USE TO VERIFY YOUR SEEDING IP
# Consider using http://checkmytorrentip.net
# You can find the hash on your client GUI or with deluge-console
# Below hash is, of course, only an example.
TORRENT_ID = "2fa71a2dbb7d53a39373a9c4e2c9d89aaa7a6db1"
# Modify the daemon path if needed
DELUGE_PATH = "/usr/bin/deluged"
# Change if you do not want to start the daemon if it is currently stopped
START_DAEMON_IF_STOPPED = True
#############################################################################

def is_deluge_started():
    '''Checks through grep if deluge daemon is started'''
    processes = str(subprocess.check_output("ps -aux | grep '"+DELUGE_PATH+"'", shell = True).decode('utf-8')).splitlines()
    for process in processes:
        if "grep" not in process: return True
    return False

def restart_torrent():
    '''Pauses and starts the verification torrent given as a global'''
    time.sleep(1)
    print(" - Restarting torrent - ")
    os.system("deluge-console pause "+TORRENT_ID)
    time.sleep(2)
    os.system("deluge-console resume "+TORRENT_ID)
    time.sleep(5)
    print(" - Torrent restarted - ")

def check_ip():
    '''Parse your public IP through dig
    Parse your proxy IP with the response of the verification tracker'''
    restart_torrent()
    public_raw = str(subprocess.check_output('dig +short myip.opendns.com @resolver1.opendns.com',shell=True))
    proxy_raw = str(subprocess.check_output("deluge-console 'info -v "+TORRENT_ID+"'", shell=True))

    public_IP = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', public_raw)
    proxy_IP = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', proxy_raw)

    return (public_IP, proxy_IP)
 
if __name__ == "__main__":
    if not is_deluge_started():
        # Consider changing the boolean var at the top 
        # if you don't want the daemon to auto-start.
        print(" - Deluge not started - ")
        if START_DAEMON_IF_STOPPED:
            print(" - Starting Deluge - ")
            os.system(DELUGE_PATH+" -d &")
            time.sleep(20)
        else:
            print(" - Exiting - ")
            sys.exit()
        
    check_output = check_ip()
    public_IP = check_output[0]
    proxy_IP = check_output[1]

    # If an IP is missing, retry max 5 times.
    if public_IP == [] or proxy_IP == []:
        trial_count = 1
        while trial_count < 5:
            if public_IP == []: 
                print(" - ! - Cannot get you public IP, trial n°"+str(trial_count))
            else:
                print(" - ! - Cannot get you proxy IP, trial n°"+str(trial_count))
            check_output = check_ip()
            public_IP = check_output[0]
            proxy_IP = check_output[1]
            if proxy_IP != [] and public_IP != []: break
            trial_count += 1
        if trial_count == 5:
            print(" - ! - Error retrieving your IP, exiting")
            sys.exit()


    print("\n - Your public IP: "+public_IP[0]+" - ")
    print(" - Your proxy IP: "+proxy_IP[0]+" - ")

    # If both IPs are equal, all torrents are paused.
    # Daemon is not killed in order to preserve the data 
    # you did not send to the trackers yet.
    # However sharing and tracker announcing will cease from now on.
    if proxy_IP[0] == public_IP[0]:
        os.system('deluge-console "pause *";')
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("\n - ! - Your IP is not protected, all torrents paused. Time: "+date_time)
    else:
        print("\n - Your IP is protected")
