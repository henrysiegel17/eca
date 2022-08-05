def D(input):
    x1 = abs(input[0] - input[1])
    x2 = abs(input[1] - input[2])
    x3 = abs(input[2] - input[3])
    x4 = abs(input[3] - input[0])
    output = [x1, x2, x3, x4]
    return output


count = 0
l = [200, 50, 20, 10]
while l[0] != 0 or l[1] != 0 or l[2] != 0 or l[3] != 0:
    count += 1
    l = D(l)
print(count)
