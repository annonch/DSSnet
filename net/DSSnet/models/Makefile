install:
	gcc -c -Wall -fpic pmu.c
	gcc -shared -o libpmu.so pmu.o

clean:
	rm pmu.o
	rm libpmu.so
