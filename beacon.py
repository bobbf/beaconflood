from scapy.all import *
from time import sleep
from multiprocessing import Process, Manager
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
        essid = Dot11Elt(ID="SSID", info=crawl_list[-1*self.count])
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
    for i in range(len(crawl["comment"]),len(crawl_list)):
        crawl["comment"].append(crawl_list[i])
    with open("./ssid.json","w",encoding="UTF8") as json_file:
        json.dump(crawl, json_file, ensure_ascii=False, indent="\t")
    sys.exit()

class messagesender(Process):
    def run(self):
        while(1):
            svrsock = socket(AF_INET, SOCK_DGRAM)
            svrsock.bind( (IPA, PORT) )
            msg, addr = svrsock.recvfrom(1024)
            list_lock.acquire()
            crawl_list.append(str(msg.decode()))
            list_lock.release()
            print(msg.decode(), addr)
            svrsock.sendto(msg, addr)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    slptime = float(crawl["sleeptime"])

    manager = Manager()
    crawl_list = manager.list()
    list_lock = manager.Lock()

    for i in range(len(crawl["comment"])):
        crawl_list.append(crawl["comment"][i])
    beaconlist = []
    p_list = []


    print("sending packets")
    ms = messagesender()
    ms.start()
    while(1):
        for i in range(5):
            beaconlist.append(makebeacon(i+1,crawl["interface"]))
        print(crawl_list[-1])
        for i in range(len(beaconlist)):
            p = Multibeacon(beaconlist[i])
            p.start()

        beaconlist = []
