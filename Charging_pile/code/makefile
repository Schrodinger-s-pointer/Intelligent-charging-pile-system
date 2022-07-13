main:main.c sjk.c sjk.h sqlite3.c sqlite3.h
	gcc -o main main.c sjk.h sjk.c sqlite3.c -lpthread -ldl `pkg-config --cflags --libs gtk+-2.0  gthread-2.0`
	./main
clean:
	rm -rf main

