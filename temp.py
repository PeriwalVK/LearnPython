print("Try programiz.pro")
import sys

def prints(x):
    print(f"for x {x}: number occupies {sys.getsizeof(1<<x)} bytes")
    print(f"for x {x}: list occupies {sys.getsizeof([True for _ in range(x)])} bytes")
    print("=========================================================")
    



x = 1
prints(x)

x = 10
prints(x)

x = 100
prints(x)

x = 1000
prints(x)

x = 10000
prints(x)

x = 100000
prints(x)