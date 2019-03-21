# Codegate 2019 Beaconflooding

코드게이트 2019 부스운영을 위한 Repo입니다.

## Menual

1. Git clone or download and extract of this repo
2. If you want to see facebook comment in wifi list, download this repo : https://github.com/bobbf/fbcrawler
3. In the beaconflood directory, execute deps.sh. **(./deps.sh)** If you have error, give permission. (ex : 'chmod 777 deps.sh')
4. After librarys are installed, open the command shell.
5. Type ''**iwconfig**'' to know your nework device name. You have to prepare wireless network device which support  **Monitor** mode.
6. Save your network device name, and open **monset.sh**. This file change mode of wireless network device from Managed to Monitor. If your network device name is different with **wlan0**, please change content of **monset.sh**. Change from **wlan0** to your network device name at all part.
7. We all ready! Type in your command shell ''**python3 beacon.py**.''
8. If you want to function of '2', execute the other command shell and change directory to fbcrawler.
9. Execute ''**python3 crawler.py <your facebook token>**''.
10. Now you can see facebook page comment in your wifi list!

## Environment

Python 3.6, scapy3k, Kali Linux

## Version

### Prototype(2019/02/24)
* Python Dictionary 형태의 Value값을 읽어 출력
* 객체지향 X, 멀티프로세싱 적용 X
* 아이폰에서 정상작동 되는지

### Prototype-1(2019/02/26)

* 객체지향 적용
* 멀티프로세싱 일부 적용
* 아이폰 정상작동 여부 해결 바람

### Prototype-2(2019/03/16~17)

* 시작할 때 ssid.json 파일에서 ssid list를 읽어옴
* multiprocessing 적용. 총 6개 프로세스
* packet을 5개 프로세스에서 보냄
* 한 프로세스에서 UDP 서버를 띄우고 1234 port에서 message 받음
* 본 코드에서 ip는 localhost이나 실제 환경에 맞처서 변경예정
* 서버가 받은 message를 ssid list에 더함
* 사용자 종료 요구(시그널 발생)시 현재 사전(ssid list) ssid.json에 저장

### <issue>
1. 아이폰 정상작동 여부 해결 바람
