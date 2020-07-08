FC=gfortran

main: main.o
	$(FC) -o $@ $^

main.o: main.f90
	$(FC) -c -o $@ $^

clean:
	rm *.o main
