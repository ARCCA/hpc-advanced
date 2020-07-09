N=1000
a = []
for i in range(N):
  a.append([])
  for j in range(N):
    a[i].append(i*N+j)

def func1():
  x = 0
  for j in range(N):
    for i in range(N):
      x += a[i][j]
  
  print(x)

def func2():
  x = 0
  for i in range(N):
    for j in range(N):
      x += a[i][j]
  
  print(x)

func1()
func2()
