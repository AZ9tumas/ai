cc = g++
ccflags = -std=c++2b -Iinclude -Wall

target = test_setup
sources = src/main.cpp src/read_csv.cpp

all:
	$(cc) $(ccflags) $(sources) -o $(target)

clean:
	rm -f $(target)