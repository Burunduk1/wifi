import sys, os, subprocess
import logging
import re
from termcolor import colored

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO) # default is warning

def get_stdout(cmd):
	return subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE).stdout.read().decode('utf-8')
def run(cmd):
	return os.system(cmd) == 0

def str2essid(s):
	result = re.search("ESSID:\"(.*)\"$", s)
	return None if result == None else result.group(1)

def have_internet():
	return run("ping -c 1 -W 1 8.8.8.8 >/dev/null")

def wifi_essid():
	return str2essid(get_stdout("iwgetid"))

def have_wifi():
	return wifi_name() == None

def wifi_interface():
	return get_stdout('nmcli d status | grep wifi | head -n 1 | awk \'{print $1}\'').strip()

def list_of_networks(interface, force=False):
	if force:
		run("nmcli d wifi rescan")
	return [str2essid(s) for s in get_stdout("iwlist %s s | grep -i essid" % interface).strip().split('\n')]

def connect(name):
	return run('nmcli connection up id "%s"' % name)

def restart_wifi():
	return run('service network-manager restart')

known_networks = [
	"at1-home",
	"Burunduk1 wifi",
]

wlan = wifi_interface()
if wlan == None or len(wlan) == 0:
	logging.error("can not detect name of wifi interface")
	sys.exit(1)

wifi = wifi_essid()
wifi_list = list_of_networks(wlan, True)

def marked(s):
	return colored(s, 'green')

print("Your interface %s" % marked(wlan))
print("You are connected to %s" % marked(wifi))
print(wifi_list)
for name in known_networks:
	print("what about '%s'?" % name)
	if name == wifi:
		print('already connected to %s' % marked(name))
		break
	elif name in wifi_list:
		print('try to connect to %s' % marked(name))
		if connect(name):
			print("success")
			break

#print(connect('"at1-home"'))
#restart_wifi()
#print(have_internet())
#print(wifi_interface())
