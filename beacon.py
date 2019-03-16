from scapy.all import *
from time import sleep
from multiprocessing import Process, Pool, Manager
import json
import sys
import signal
from socket import *

PORT = 1234
IPA = "localhost"
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
        essid = Dot11Elt(ID="SSID", info=crawler["comment"][-1*self.count])
        sendp(RadioTap()/self.dot11/self.beacon11/essid, iface=self.interface, loop=0,verbose=False)
        sleep(slptime)

class Multibeacon(Process):

    def __init__(self, beaconobj):
        Process.__init__(self)
        self.beaconobj = beaconobj

    def run(self):
        self.beaconobj.sendbeacon()
        sleep(slptime)

def handler(signum, f):
    with open("./ssid.json","w",encoding="UTF8") as json_file:
        json.dump(crawler, json_file, ensure_ascii=False, indent="\t")
    sys.exit()

class messagesender(Process):
    def run(self):
        while(1):
            svrsock = socket(AF_INET, SOCK_DGRAM)
            svrsock.bind( (IPA, PORT) )
            msg, addr = svrsock.recvfrom(1024)
            crawler["comment"].append(str(msg.decode()))
            print(msg.decode(), addr)
            svrsock.sendto(msg, addr)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    slptime = float(input("write sleep time: "))

    manager = Manager()
    crawler = manager.dict()
    crawler = crawl
    beaconlist = []
    p_list = []


    print("sending packets")
    ms = messagesender()
    ms.start()
    while(1):
        for i in range(5):
            beaconlist.append(makebeacon(i+1,crawl["interface"]))

        for i in range(len(beaconlist)):
            p = Multibeacon(beaconlist[i])
            p.start()
#            p_list.append(p)
#        for x in p_list:
#            x.join()

        beaconlist = []
