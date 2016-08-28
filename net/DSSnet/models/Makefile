install:
	gcc -c -Wall -fpic pmu.c
	gcc -shared -o libpmu.so pmu.o
	gcc -c -Wall -fpic gtod.c
	gcc -shared -o libgtod.so gtod.o
clean:
	rm pmu.o
	rm libpmu.so
	rm ptod.o
	rm libgtod.so
