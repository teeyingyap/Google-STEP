import numpy, sys, time
import matplotlib.pyplot as plt

if (len(sys.argv) != 2):
    print("usage: python %s N" % sys.argv[0])
    quit()

n = int(sys.argv[1])

# Initialize the matrices to some values.
def dot_product(n):
    a = numpy.zeros((n, n)) # Matrix A
    b = numpy.zeros((n, n)) # Matrix B
    c = numpy.zeros((n, n)) # Matrix C
    for i in range(n):
        for j in range(n):
            a[i, j] = i * n + j
            b[i, j] = j * n + i
            c[i, j] = 0

    begin = time.time()
    for i in range(n):
        for j in range(n):
            sum = 0
            for k in range(n):
                sum += a[i][k] * b[k][j]
            c[i][j] = sum

    end = time.time()
    period = end - begin
    print("time: %.6f sec" % (period))
    return period


##dot_product(n)
# Print C for debugging. Comment out the print before measuring the execution time.
##total = 0
##for i in range(n):
##    for j in range(n):
##        print(c[i, j])
##        total += c[i, j]
# Print out the sum of all values in C.
# This should be 450 for N=3, 3680 for N=4, and 18250 for N=5.
##print("sum: %.6f" % total)


y = []
x = list(range(1, 201))
for i in x:
    y.append(dot_product(i))


plt.title("N vs. Execution Time") 
plt.xlabel("N") 
plt.ylabel("Execution time (sec)") 
plt.plot(x, y)
plt.grid()
plt.show() 






