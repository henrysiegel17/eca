# f(x) = x*x + 1 mod 10
def f(x):
    return (x * x + 1) % 10


# g(x) = x*x + 2 mod 17
def g(x):
    return (x * x + 2) % 17


def compute_pt(x, path):
    pt = [0, 0]
    while pt[1] == 0:
        x = g(x)
        i = found(path, x)
        # we did NOT find match
        if i == -1:
            path.append(x)
        # we FOUND match
        else:
            return [i, len(path) - i]


def found(list, element):
    i = len(list) - 1
    while len(list) != 0 and i > -1 and list[i] != element:
        i = i - 1
    return i


def meetingtime(pt):
    transient = pt[0]
    period = pt[1]
    time = 1
    pos1 = 2
    pos2 = 3
    while (((pos2 - pos1) % period != 0) and pos1 > transient and pos2 > transient) or (
        pos1 <= transient or pos2 <= transient
    ):
        pos1 += 1
        pos2 += 2
        time += 1
    return time


for x in range(0, 10):
    path = [x]
    pt = [0, 0]
    pt = compute_pt(x, path)
    print(x, pt[0], pt[1])
    x = x + 1
pt2 = [67, 11]
time = meetingtime(pt2)
print(time)
