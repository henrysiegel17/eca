#Euclidean Algorithm
# gcd(a,b) = gcd(a,r), a = qb + r

#recursive definition 
# Assume a > b
def gcd(a,b):
    if b == 0:
        return a
    elif b > 0:
        q = int(a/b)
        # if b > a, then switch inputs
        print(b, a - q*b)
        return gcd(b, a - q*b)

def main(): 
    print(gcd(221,299))

if "__main__" == __name__:
    main()