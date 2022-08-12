import math
from tracemalloc import start
'''
the way a knight moves:
i+2, j+1
i+2, j-1
i+1,j+2
i+1,j-2
i-1,j+2
i-1,j-2
i-2,j+1
i-2,j+1
'''

knight_movement = [[2, 1], [2, -1], [1, 2],
                   [1, -2], [-1, 2], [-1, -2], [-2, 1], [-2, 1]]


def naive_optimal_solution(A):
    # first pre-scan grid to find all white and black knights
    w = []
    b = []

    for i in range(0, len(A)):
        for j in range(0, len(A[0])):
            if A[i][j] == 'B':
                b.append(i*len(A[0])+j)
            if A[i][j] == 'W':
                w.append(i*len(A[0])+j)

    knights = single_array(w, b)
    end = complementary(knights)
    path = find_shortest_path(A, knights, end)
    if len(path) == 0:
        print("sorry, I can't find a solution")
    else:
        print(path)
        answer = []
        # ONE FINAL DETOUR --> WE MUST CONVERT OUR
        # "FLATTENED" INTEGERS TO ACTUAL COORDINATES
        for i in range(len(path)-1, -1, -1):
            a = path[i]
            x = thicken(len(A[0]), a[0])
            y = thicken(len(A[0]), a[1])
            position = [x, y]
            answer.append(position)
        print(answer)


def complementary(A):
    possible_states = []
    arr1 = []
    arr2 = []
    half = int(len(A)/2)
    for i in range(0, half):
        arr1.append(A[i])
    for i in range(half, len(A)):
        arr2.append(A[i])
    state = single_array(arr1, arr2).copy()
    for first in range(0, half):
        state[first] = A[first+half]
        state[first+half] = A[first]

    first_half = heapPermutation(arr2, half, [])
    second_half = heapPermutation(arr1, half, [])
    for f in first_half:
        for s in second_half:
            state = single_array(f, s).copy()
            possible_states.append(state)
    return possible_states

# Generating permutation using Heap Algorithm


def heapPermutation(a, size, answer):

    # if size becomes 1 then returns the obtained
    # permutation
    if size == 1:
        answer.append(a)

    for i in range(size):
        heapPermutation(a, size-1, answer)

        # if size is odd, swap 0th i.e (first)
        # and (size-1)th i.e (last) element
        # else If size is even, swap ith
        # and (size-1)th i.e (last) element
        if size & 1:
            a[0], a[size-1] = a[size-1], a[0]
        else:
            a[i], a[size-1] = a[size-1], a[i]

    return answer
 # Thank you https://www.geeksforgeeks.org/heaps-algorithm-for-generating-permutations/


def single_array(A, B):
    C = []
    for i in range(0, len(A)):
        C.append(A[i])
    for j in range(0, len(B)):
        C.append(B[j])
    return C

# end is an array that contains all possible ending configurations
# USES BREADTH FIRST SEARCH


def BFS(A, knights, end):
    # we start with a Queue that stores all adjacent configurations that should be explored
    Queue = []
    length = len(knights)

    # defining a couple other variables that will be helpful later
    used_positions = []
    base = len(A)*len(A[0])

    # define our goals: we must first convert the end array of arrays to an array of integers
    goals = []
    for i in range(0, len(end)):
        temp = base_x(end[i], base)
        goals.append(temp)

    # LET EACH POSITION BE UNIQUELY DEFINED BY A NUMBER, LIKE A TAG
    tag = base_x(knights, base)
    # ADD TAG TO USED_POSITIONS, BECAUSE WE'VE SEEN IT BEFORE
    used_positions.append(tag)
    # ALSO ADD TAG TO QUEUE
    Queue.append(tag)

    # ONE MORE THING: LET'S DEFINE A MAP,
    # SO WE CAN BACKTRACK FROM ANY GIVEN POSITION BACK TO THE START
    # map: current position (int) --> previous position (int)
    map = {}

    # NOW READ OFF ALL ELEMENTS FROM THE QUEUE AND MARK THEM OFF ONE BY ONE
    count = 0
    while(len(Queue)) != 0:
        u = Queue[0]
        Queue.pop(0)
        # explore u

        # ADDING ALL ADJACENT POSITIONS TO QUEUE
        knights = reversebase(u, length, base).copy()
        for i in range(len(knights)):
            for k in range(len(knight_movement)):
                coordinate = thicken(len(A[0]), knights[i])
                # check that the square we're searching for is within the range of the grid
                condition1 = coordinate[0]+knight_movement[k][0] >= 0 and coordinate[0]+knight_movement[k][0] < len(
                    A) and coordinate[1]+knight_movement[k][1] >= 0 and coordinate[1]+knight_movement[k][1] < len(A[0])
                # check that the adjacent square is a valid square
                condition2 = False
                if condition1:
                    condition2 = A[coordinate[0]+knight_movement[k][0]
                                   ][coordinate[1]+knight_movement[k][1]] != 'N'
                # check that the square we're looking at is not currently occupied:
                new_position = (coordinate[0]+knight_movement[k][0]) * \
                    len(A[0])+(coordinate[1]+knight_movement[k][1])
                condition3 = True
                condition4 = True
                if condition1 and condition2:
                    condition3 = new_position in knights
                # check that the resulting new position is not already in used_positions
                test = knights.copy()
                test[i] = new_position
                temp_tag = base_x(test, base)

                # WIN CONDITION: IF WE SPOT AN END CONFIGURATION WE STOP
                if temp_tag in goals:
                    map[temp_tag] = u
                    return (temp_tag, map)

                if condition3 == False:
                    # ONLY EXPLORE IF WE DIDN'T EXPLORE THE POSITION ALREADY
                    condition4 = temp_tag in used_positions

                # IF WE HAVE A CONNECTION
                if condition4 == False:
                    # ADD TO QUEUE
                    Queue.append(temp_tag)
                    # ADD TO USED VERTICIES
                    used_positions.append(temp_tag)
                    # FINALLY UPDATE MAP:
                    map[temp_tag] = u
        count += 1
    return (0, temp_tag)


def find_shortest_path(A, knights, end):
    path = []
    tag_and_map = BFS(A, knights, end)
    goal = tag_and_map[0]
    if goal == 0:
        return []
    map = tag_and_map[1]
    start = base_x(knights, len(A)*len(A[0]))
    # BACKTRACK OUR WAY TO THE START
    path.append(reversebase(goal, len(knights), len(A)*len(A[0])))
    while goal != start:
        goal = map[goal]
        # PATH PRINTS OUT A SEQUENCE OF ARRAYS
        # must convert the integers back to arrays first
        path.append(reversebase(goal, len(knights), len(A)*len(A[0])))

    # THE ACTUAL PATH IS IN REVERSE ORDER
    return path

# convert array A to number in base x


def base_x(A, x):
    num = 0
    for i in range(0, len(A)):
        num += A[i] * math.pow(x, len(A)-i-1)
    return num


def reversebase(quantity, length, base):
    A = [0 for i in range(length)]
    starting_index = 0
    while quantity >= math.pow(base, starting_index):
        starting_index += 1
    q = quantity
    for i in range(starting_index-1, -1, -1):
        if q >= math.pow(base, i):
            A[len(A)-1-i] = int(q/(math.pow(base, i)))
            q = q - A[len(A)-1-i]*math.pow(base, i)
    return A


def thicken(width, num):
    times = 0
    val = num
    while val >= width:
        val = val-width
        times += 1
    return (times, val)


board = [['N', 'Y', 'W', 'N', 'N'],
         ['Y', 'N', 'Y', 'N', 'B'],
         ['Y', 'N', 'Y', 'N', 'N'],
         ['N', 'N', 'Y', 'N', 'N']]

naive_optimal_solution(board)
