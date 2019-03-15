from scapy.all import *
from time import sleep
from multiprocessing import Process
import json
import sys
import signal

json_data = open("ssid.json").read()
crawl = json.loads(json_data)
br = "ff:ff:ff:ff:ff:ff"

class makebeacon:
	dot11 = Dot11(addr1=br, addr2 = str(RandMAC()), addr3=str(RandMAC()))
	beacon11 = Dot11Beacon(cap="ESS+privacy") #option : ESS or ESS+privacy

	def __init__(self, count, interface):
		self.count = count
		self.interface = interface

	def sendbeacon(self):
		essid = Dot11Elt(ID="SSID", info=crawl["comment"][-1*self.count])
		sendp(RadioTap()/self.dot11/self.beacon11/essid, iface=self.interface, loop=0,verbose=False)

class Multibeacon(Process):

	def __init__(self, beaconobj):
		Process.__init__(self)
		self.beaconobj = beaconobj

	def run(self):
		self.beaconobj.sendbeacon()
		sleep(slptime)

def handler(signum, f):
	with open("./ssid.json","w",encoding="UTF8") as json_file:
		json.dump(crawl, json_file, ensure_ascii=False, indent="\t")
	sys.exit()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, handler)
	slptime = float(input("write sleep time: "))

	beaconlist = []
	p_list = []

	for i in range(5):
		beaconlist.append(makebeacon(i+1, crawl["interface"]))
	crawl["comment"].append("새로운프레임")
	print("sending packets")
	while(1):
		for i in range(len(beaconlist)):
			p = Multibeacon(beaconlist[i])
#			p_list.append(p)
			p.start()

