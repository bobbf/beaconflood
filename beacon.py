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
        sendp(RadioTap()/self.dot11/self.beacon11/essid, iface=self.interface, loop=0, verbose=False)

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

    with open("./ssid.json","w",encoding="UTF8") as json_file:
        json.dump(crawl, json_file, ensure_ascii=False, indent="\t")
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
            try:
                for i in range(len(rec_msg)):
                    for rec_msg[i]["message"] in crawl_list:
                        pass
                    else:
                        crawl["comment"].append(rec_msg[i]["message"])
                        crawl_list.append(rec_msg[i]["message"])
                        beacon_list.append(makebeacon(rec_msg[i]["message"]))
            except:
                pass
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
