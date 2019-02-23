from scapy.all import *
from multiprocessing import Process

crawl = {"comment" : ["gilgil", "hyejin", "minwoo", "kyeongsu", "dohoon"]}

def dotmake():
	br = "ff:ff:ff:ff:ff:ff"
	dot11 = Dot11(addr1=br, addr2 = str(RandMAC()), addr3=str(RandMAC()))
	dot22 = Dot11(addr1=br, addr2 = str(RandMAC()), addr3=str(RandMAC()))
	dot33 = Dot11(addr1=br, addr2 = str(RandMAC()), addr3=str(RandMAC()))
	dot44 = Dot11(addr1=br, addr2 = str(RandMAC()), addr3=str(RandMAC()))
	dot55 = Dot11(addr1=br, addr2 = str(RandMAC()), addr3=str(RandMAC()))

	beacon1= Dot11Beacon(cap="ESS+privacy")
	beacon2= Dot11Beacon(cap="ESS")
	beacon3= Dot11Beacon(cap="ESS")
	beacon4= Dot11Beacon(cap="ESS+privacy")
	beacon5= Dot11Beacon(cap="ESS")

	essid1 = Dot11Elt(ID="SSID", info=crawl["comment"][0])
	essid2 = Dot11Elt(ID="SSID", info=crawl["comment"][1])
	essid3 = Dot11Elt(ID="SSID", info=crawl["comment"][2])
	essid4 = Dot11Elt(ID="SSID", info=crawl["comment"][3])
	essid5 = Dot11Elt(ID="SSID", info=crawl["comment"][4])

	return dot11, dot22, dot33, dot44, dot55, beacon1, beacon2, beacon3, beacon4, beacon5, essid1, essid2, essid3, essid4, essid5

def sendbeacon(dot11,dot22,dot33,dot44,dot55,beacon1,beacon2,beacon3,beacon4,beacon5,essid1,essid2,essid3,essid4,essid5):
	sendp(RadioTap()/dot11/beacon1/essid1, iface="wlan0", loop=0)
	sendp(RadioTap()/dot22/beacon2/essid2, iface="wlan0", loop=0)
	sendp(RadioTap()/dot33/beacon3/essid3, iface="wlan0", loop=0)
	sendp(RadioTap()/dot44/beacon4/essid4, iface="wlan0", loop=0)
	sendp(RadioTap()/dot55/beacon5/essid5, iface="wlan0", loop=0)


if __name__ == "__main__":

	dot11, dot22, dot33, dot44, dot55, beacon1, beacon2, beacon3, beacon4, beacon5, essid1, essid2, essid3, essid4, essid5 = dotmake()
	while(1):
		sendbeacon(dot11,dot22,dot33,dot44,dot55,beacon1,beacon2,beacon3,beacon4,beacon5,essid1,essid2,essid3,essid4,essid5)

