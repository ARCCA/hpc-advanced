PROGRAM main

INTEGER, PARAMETER :: n = 100000000
INTEGER :: i
INTEGER :: a(n)

DO i = 1, n
  a(i) = SQRT(REAL(i))
  a(i) = a(i) + a(1)
END DO

PRINT *, a(1)

END PROGRAM main
