from scapy.all import *
from time import sleep
from multiprocessing import Process

crawl = {"comment" : ["gilgil", "hyejin", "minwoo", "kyeongsu", "dohoon"], "interface":"wlan0"}
br = "ff:ff:ff:ff:ff:ff"

class makebeacon:
	dot11 = Dot11(addr1=br, addr2 = str(RandMAC()), addr3=str(RandMAC()))
	beacon11 = Dot11Beacon(cap="ESS+privacy") #option : ESS or ESS+privacy

	def __init__(self, count, interface):
		self.count = count
		self.interface = interface

	def sendbeacon(self):
		essid = Dot11Elt(ID="SSID", info=crawl["comment"][self.count])
		sendp(RadioTap()/self.dot11/self.beacon11/essid, iface=self.interface, loop=0,verbose=False)

class Multibeacon(Process):

	def __init__(self, beaconobj):
		Process.__init__(self)
		self.beaconobj = beaconobj

	def run(self):
		self.beaconobj.sendbeacon()
		sleep(slptime)


if __name__ == "__main__":
	slptime = input("write sleep time: ")

	beaconlist = []
	p_list = []

	for i in range(len(crawl["comment"])):
		beaconlist.append(makebeacon(i, crawl["interface"]))

	print("sending packets")
	while(1):
		for i in range(len(beaconlist)):
			p = Multibeacon(beaconlist[i])
			p.start()
		for p in p_list:
			p.join()
