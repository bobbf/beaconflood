
from scapy.all import *
from time import sleep
from multiprocessing import Process, Manager
import json
import sys
from socket import *
import signal

PORT = 1234
IPA = "localhost"
json_data = open("ssid.json").read()
crawl = json.loads(json_data)
br = "ff:ff:ff:ff:ff:ff"
RUNNING = 1

class makebeacon:
    dot11 = Dot11(addr1=br, addr2 = str(RandMAC()), addr3=str(RandMAC()))
    beacon11 = Dot11Beacon(cap="ESS+privacy") #option : ESS or ESS+privacy

    def __init__(self, interface, mssid):
        self.interface = interface
        self.mssid = mssid

    def sendbeacon(self):
        essid = Dot11Elt(ID="SSID", info=self.mssid)
        sr = Dot11Elt(ID="Rates", info="\x01\x08\x82\x84\x8b\x96\x0c\x12\x18\x23")
        ds = Dot11Elt(ID="DSset", info="\x03")
        tim = Dot11Elt(ID="TIM", info="\x00\x01\x00\x00")
        erp = Dot11Elt(ID="ERPinfo", info="\x2a")
        rsn = Dot11Elt(ID='RSNinfo', info=(
        '\x01\x00'                 #RSN Version 1
        '\x00\x0f\xac\x02'         #Group Cipher Suite : 00-0f-ac TKIP
        '\x02\x00'                 #2 Pairwise Cipher Suites (next two lines)
        '\x00\x0f\xac\x04'         #AES Cipher
        '\x00\x0f\xac\x02'         #TKIP Cipher
        '\x01\x00'                 #1 Authentication Key Managment Suite (line below)
        '\x00\x0f\xac\x02'         #Pre-Shared Key
        '\x00\x00'))
        #sendp(RadioTap()/self.dot11/self.beacon11/essid, iface=self.interface, loop=0, verbose=False)
        sendp(RadioTap()/self.dot11/self.beacon11/essid/sr/ds/tim/erp/rsn, iface=self.interface, loop=0, verbose=False)
class Multibeacon(Process):
    global RUNNING
    def __init__(self):
        Process.__init__(self)

    def run(self):
        while(RUNNING):
            for i in range(5):
                beacon_list[(i+1)*-1].sendbeacon()
                sleep(slptime)


def handler(signum, f):

#    with open("./ssid.json","w",encoding="UTF8") as json_file:
#        json.dump(crawl, json_file, ensure_ascii=False, indent="\t")
    sys.exit()

class messagesender(Process):
    def run(self):
        while(1):
            svrsock = socket(AF_INET, SOCK_DGRAM)
            svrsock.bind( (IPA, PORT) )
            msg, addr = svrsock.recvfrom(0xffff)
            tmp_crawl = json.loads(msg.decode())
            rec_msg = tmp_crawl["data"]
#            beacon_list.append(makebeacon(crawl["interface"],msg.decode()))

            list_lock.acquire()
            for i in range(len(rec_msg)):
                if rec_msg[i]["message"] in crawl_list:
                    pass
                else:
                    crawl["comment"].append(rec_msg[i]["message"])
                    crawl_list.append(rec_msg[i]["message"])
                    beacon_list.append(makebeacon(crawl["interface"],rec_msg[i]["message"]))
                    print(crawl["comment"])
                    with open("./nsid.txt","at",encoding="UTF8") as tfile:
                        tfile.write(rec_msg[i]["message"])
                        tfile.write(" ")
            list_lock.release()

#            with open("./nsid.txt","at",encoding="UTF8") as json_file:
#                json_file.write(msg.decode())
#                json_file.write("\n")
#            print(msg.decode(), addr)
            svrsock.sendto(msg, addr)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    slptime = float(crawl["sleeptime"])

    manager = Manager()
    crawl_list = manager.list()
    list_lock = manager.Lock()

    manager2 = Manager()
    beacon_list = manager2.list()

    for i in range(len(crawl["comment"])):
        crawl_list.append(crawl["comment"][i])

    print("sending packets")

    for i in range(5):
        beacon_list.append(makebeacon(crawl["interface"],crawl["comment"][i*-1]))

    ms = messagesender()
    ms.start()

    p = Multibeacon()
    p.start()

    ms.join()
    p.join()
