CC=gcc
CXX=g++ -g
CXXFLAGS= -std=c++17 -lprotobuf -pthread 

TEST_TARGET=test

SERIAL=$(shell protoc -I=modules/packet --cpp_out=modules/packet modules/packet/PacketSerial.proto)

PACKET_SRC=$(wildcard modules/packet/*.cpp)
SOCK_SRC=$(wildcard modules/SockWrapper/*.cpp)
STRUCTURE_SRC=$(wildcard modules/structure/*.cpp)

TEST_SRC=test.cpp
SRCS=$(PACKET_SRC) $(SOCK_SRC) $(STRUCTURE_SRC)
OBJS=$(SRCS:.cpp=.o)
TEST_OBJ=$(TEST_SRC:.cpp=.o)

test: $(SERIAL) $(OBJS) modules/packet/PacketSerial.pb.o $(TEST_OBJ)
	g++ -o $(TEST_TARGET) $(OBJS) modules/packet/PacketSerial.pb.o $(TEST_OBJ) $(CXXFLAGS) 

clean_test:
	rm $(OBJS)
	rm $(TEST_OBJ)
	rm modules/packet/PacketSerial.pb.*
	rm $(TEST_TARGET)

#make protocol object file
modules/packet/PacketSerial.pb.o: modules/packet/PacketSerial.pb.cc
	g++ -g -c -std=c++17 -o modules/packet/PacketSerial.pb.o modules/packet/PacketSerial.pb.cc -lprotobuf -pthread