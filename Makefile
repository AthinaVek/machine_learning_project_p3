all: search

search: search.o help_functions.o calculations.o calculations_lsh.o
	g++ search.o help_functions.o calculations.o calculations_lsh.o -o search

search.o: search.cpp
	g++ -c search.cpp

help_functions.o: help_functions.cpp
	g++ -c help_functions.cpp

calculations.o: calculations.cpp
	g++ -c calculations.cpp
	
calculations_lsh.o: calculations_lsh.cpp
	g++ -c calculations_lsh.cpp

clean:
	rm -f search help_functions calculations calculations_lsh search.o help_functions.o calculations.o calculations_lsh.o
