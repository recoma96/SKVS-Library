# SKVS-Library 0.0.1
SKVS Library

## 구현환경
* CENTOS 7.5

## 라이브러리 사용 방법
### 1. C++(CPP) [![Build Status](https://travis-ci.org/Re-Coma/SKVS-Library-CPP.svg?branch=master)](https://travis-ci.org/Re-Coma/SKVS-Library-CPP)
* 사용 조건 : Only Linux, g++ 7 이상, C++17
* 사용 방법 : 
  * cpp폴더를 다운받습니다.
  * make lib를 실행합니다.
  * libskvsclient.so를 원하는 위치에 저장합니다.
  * sudo vim /etc/ld.so.conf를 실행하여 맨 하단에 라이브러리를 저장한 위치를 입력합니다.
  * sudo ldconfig를 실행합니다.
  * 라이브러리를 사용합니다. (사용방법은 Makefile의 make test부분을 참고하세요
  * [Manual](https://gist.github.com/Re-Coma/a0eb1b16731d0ef8357b0391f0eeffc8)
### 2. Python [![Build Status](https://travis-ci.org/Re-Coma/SKVS-Library-Python.svg?branch=master)](https://travis-ci.org/Re-Coma/SKVS-Library-Python)
* 사용 조건 : python 3 이상
* python 폴더를 다운받습니다.
* 파이썬은 인터프리터 언어이므로 바로 사용 가능합니다.
* [Manual](https://gist.github.com/Re-Coma/811a90c2da3444b90c6686ea4bc0f2a6)
