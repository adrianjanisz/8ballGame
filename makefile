CC = clang
CFLAGS = -Wall -std=c99 -pedantic 

all: libphylib.so _phylib.so

clean:
	rm -f *.o *.so phylib_wrap.c phylib.py

phylib.o: phylib.c
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm

phylib_wrap.c phylib.py: phylib.i
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so 

