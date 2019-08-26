# SKVS-Library 0.0.1
SKVS Library

## 구현환경
* CENTOS 7.5

## 라이브러리 사용 방법
### 1. C++(CPP)
* 사용 조건 : Only Linux, g++ 7 이상, C++17, google protocol buffer 3.7.0 이상
* 사용 방법 : 
  * cpp폴더를 다운받습니다.
  * make lib를 실행합니다.
  * libskvsclient.so를 원하는 위치에 저장합니다.
  * sudo vim /etc/ld.so.conf를 실행하여 맨 하단에 라이브러리를 저장한 위치를 입력합니다.
  * sudo ldconfig를 실행합니다.
  * 라이브러리를 사용합니다. (사용방법은 Makefile의 make test부분을 참고하세요
  * [Manual](https://gist.github.com/Re-Coma/a0eb1b16731d0ef8357b0391f0eeffc8)
  

