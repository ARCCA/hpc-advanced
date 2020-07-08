FC=ifort
FCFLAGS=-g
LDFLAGS=-g

main: main.o
	$(FC) $(LDFLAGS) -o $@ $^

main.o: main.f90
	$(FC) -c $(FCFLAGS) -o $@ $^

clean:
	rm *.o main core.*
