from calendar import c
import pygame
import time
import math
from cmath import inf
from pygame.locals import *
from naive import thicken, single_array, base_x, printBoard, complementary
from eca import match

WIDTH = 500
HEIGHT = 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

"""
the way a knight moves:
i+2, j+1
i+2, j-1
i+1,j+2
i+1,j-2
i-1,j+2
i-1,j-2
i-2,j+1
i-2,j-1
"""

knight_movement = [
    [2, 1],
    [2, -1],
    [1, 2],
    [1, -2],
    [-1, 2],
    [-1, -2],
    [-2, 1],
    [-2, -1],
]

# WE WILL IMPLEMENT SOME WEIRD VERSION OF A*
# g(x) --> distance away from the goals: in this case, it is the distance that each knight is away from their respective goals
# p(x) --> priority function that tells a knight how much it needs to move to make space for other knights
# p(x) = Σ (change g(x) for each other knight when the given knight exists or not)
# * IF SHORTEST PATH IS LONGER THAN CERTAIN THRESHOLD, WE JUST SAY IT IS int(ln(n)), where is the number of nodes
# This latter function is not usually associated with A star, but it feels necessary
# p'(x) --> same as p(x) but is for square that knight can move to
# g(x) = Σ (distances from each goal)^2
# note that p(x) takes way higher precidence than g(x) and f(x)
# minimize h(x) = g(x) + p(x) + p'(x)
# note THAT THERE IS NO f(X)

# takes in board and knights, returns the best move at any given instance
def run_heurestic(board, limit):
    start_end = []
    knights = find_knights(board)
    for i in range(len(knights)):
        pos = []
        for j in range(len(knights[i])):
            pos.append(knights[i][j])
        start_end.append(pos)
    # white knights
    white_distances = BFS(board, knights[1],-1)
    # black knights
    black_distances = BFS(board, knights[0],-1)
    real_knights = single_array(knights[0], knights[1])
    end_values = []
    end = complementary(real_knights)
    print("hello")
    
    for e in end:
        end_values.append(base_x(e, len(board)*len(board[0])))

    value = -1

    # BLACK KNIGHT STARTS --> WHITE GOALS:
    # USE BLACK DISTANCES

    # WHITE KNIGHT STARTS --> BLACK GOALS
    # USE WHITE DISTANCES

    # knights = [white, black]

    path = []
    count = 0
    repeat_table = []
    
    c = []
    position = []
    for i in range(len(real_knights)):
        coordinates = thicken(len(board[0]), real_knights[i])
        c.append(real_knights[i])
        position.append(coordinates)
    path.append(position) 

    while count_array(end,real_knights) != 1 and count < limit:
        position = []
        # A, knights, white_distances, black_distances, down_map, up_map
        move = best_first_search(
            board,
            knights,
            white_distances,
            black_distances,
            start_end,
            repeat_table
        )

        real_knights[move[0]] = move[1]
        #update knights:
        if move[0] < int(len(real_knights)/2):
            knights[0][move[0]] = move[1]
        else:
            knights[1][move[0]%int(len(real_knights)/2)] = move[1]
        count += 1
        
        #update repeats
        repeat_table.append(real_knights.copy())   

        #update paths
        c = []
        for i in range(len(real_knights)):
            coordinates = thicken(len(board[0]), real_knights[i])
            c.append(real_knights[i])
            position.append(coordinates)
        path.append(position) 

    if count < limit:
        print("I found a solution!")
        print("Length of path is ", len(path))
    else:
        print("I can't find a solution :(")
    printBoard(board, path)


def best_first_search(
    A,
    knights,
    white_distances,
    black_distances,
    start_end,
    repeat_table,
):
    # **************** adjacent moves = {total_knights i : adjacent squares}
    # **************** knights = [white, black]
    # **************** move = [i, j] --> knight i, and square j
    white_knights = knights[0]
    black_knights = knights[1]
    total_knights = single_array(white_knights, black_knights)
    adjacent_moves = {}
    for i in range(len(total_knights)):
        reachable_squares = find_adjacent_moves(A, total_knights[i], total_knights)
        adjacent_moves[i] = reachable_squares
    lowest_move = [0,0]
    for m in range(len(adjacent_moves)):
        for k in range(len(adjacent_moves[m])):
            lowest_move = [m, adjacent_moves[m][k]]
    low = float('inf')
    for knight_num, squares in adjacent_moves.items():
        p_considerations = []
        for s in range(len(squares)):
            move = (knight_num, squares[s])
            g_value = 100*((g(move, white_distances,
                        black_distances, int(len(total_knights) / 2)) - g([knight_num, total_knights[knight_num]], white_distances,
                                                                    black_distances, int(len(total_knights) / 2))))
            if g([knight_num, total_knights[knight_num]], white_distances, black_distances, int(len(total_knights) / 2)) != 0:
                g_value = ((g(move, white_distances,
                        black_distances, int(len(total_knights) / 2)) - g([knight_num, total_knights[knight_num]], white_distances,
                                                                    black_distances, int(len(total_knights) / 2))))/g([knight_num, total_knights[knight_num]], white_distances,
                                                                    black_distances, int(len(total_knights) / 2))

            # A,move, white_distances, black_distances, knights, size
            p_value = p(
                A,
                [knight_num,total_knights[knight_num]],
                white_distances,
                black_distances,
                knights,
                int(len(total_knights) / 2),
                start_end
            )
            # While p is the priority of the knight moving, pn is an estimate of the priority after n iterations
            p_considerations.append(p)
            '''p_value_prime = p(A,
                move,
                white_distances,
                black_distances,
                knights,
                int(len(knights) / 2)
                )
                '''
            """
                Check if p is the same

                add 1*p1
                + 1/2 * p2
                + 1/6 * p3
            """
            """
            planning code:
                used = knights.copy()
            
            for i in range(0, len(p_considerations))
                while all p(i) are the same:
                # compute ANOTHER iteration 
                    position[i] = find_adjacent_moves(A, position, used)[0]
                    used.append(position[i])
            """
            #pn = pn()
            hypothetical_knights = total_knights.copy()
            hypothetical_knights[move[0]] = move[1]
            # DISCOURAGE ALGORITHM FROM REPEATING MOVES
            repeat_penalty = count_array(repeat_table, hypothetical_knights)*100000000*(len(total_knights)/2-1)
            score = g_value + p_value + repeat_penalty
            if score < low:
                low = score
                lowest_move = move
    print("hello")
    return lowest_move


# returns all squares that are reachable by knight

def find_adjacent_moves(A, knight, repeat):
    adjacent_moves = []
    for k in range(len(knight_movement)):
        coordinate = thicken(len(A[0]), knight)
        # check that the square we're searching for is within the range of the grid
        condition1 = (
            coordinate[0] + knight_movement[k][0] >= 0
            and coordinate[0] + knight_movement[k][0] < len(A)
            and coordinate[1] + knight_movement[k][1] >= 0
            and coordinate[1] + knight_movement[k][1] < len(A[0])
        )
        # check that the adjacent square is a valid square
        condition2 = False
        if condition1:
            condition2 = (
                A[coordinate[0] + knight_movement[k][0]][
                    coordinate[1] + knight_movement[k][1]
                ]
                != "N"
            )
        # check that the square we're looking at is not in repeat:
        new_position = (coordinate[0] + knight_movement[k][0]) * len(A[0]) + (
            coordinate[1] + knight_movement[k][1]
        )
        condition3 = False
        if condition1 and condition2:
            condition3 = new_position not in repeat
        if condition3:
            adjacent_moves.append(new_position)
    return adjacent_moves

def g(move, white_distances, black_distances, size):
    if move[0] < size:
        # white knight moving
        return white_distances[move[1]]
    return black_distances[move[1]]


# p(x) = Σ (change g(x) for each other knight when the given knight exists or not)
# index i --> which knight we want to consider


# BY CHANGING NODE n's DISTANCE TO INFINITY, THAT MAY OR MAY NOT CHANGE EVERY OTHER NODE'S DISTANCE
def propagate_graph(n, down_map, up_map, distances, size):

    used = []
    queue = []
    queue.append(n)
    distances_copy = distances.copy()
    distances_copy[n] = 10000000

    while len(queue) > 0:
        u = queue[0]
        queue.pop(0)

        # u is the node we are exploring, and we are determining whether the
        # distances of the parents of u depend on the distance of u
        for v in up_map[u]:
            # look at all nodes v one level above
            if v not in used and len(down_map[v]) == 1:
                # in other words, distance[v] is fully dependent on distance[u]
                used.append(v)
                queue.append(v)

    return distances_copy


# We want to pre-compute every square's distance away from the origins,
# as well as creating a map that stores all adjacent nodes to any given node
# very useful for computing g(x), p(x), pp(x)

# node n will be excluded
def BFS(A, origins, n):

    # BFS
    # we start with a Queue that stores all adjacent configurations that should be explored
    Queue = []

    # used_moves contains all moves that we already checked
    used_moves = []

    if n != -1:
        used_moves.append(n)

    # distance counter --> indicates every node's distance from origin
    dist = {}

    # in the beginning, we assume every node's distance from the origin is "infinity"
    for i in range(len(A)):
        for j in range(len(A[0])):
            dist[i * len(A[0]) + j] = 10000000

    # In the beginning, all origins are of 0 distance, Queue and used_moves contains all origins

    if isinstance(origins, int) == False:
        for o in origins:
            if o not in used_moves:
                dist[o] = 0
                Queue.append(o)
                used_moves.append(o)
    else: 
        dist[origins] = 0
        Queue.append(origins)
        used_moves.append(origins)

    while (len(Queue)) != 0:
        u = Queue[0]
        Queue.pop(0)
        # explore u --> IS AN INTEGER

        # find adjacent vertices
        adjacent_moves = find_adjacent_moves(A, u, used_moves)

        # append to queue and used_moves list
        # update distances accordingly
        for move in adjacent_moves:
            dist[move] = dist[u] + 1
            Queue.append(move)
            used_moves.append(move)

    return dist


# We need to define one more function, an actual Astar algorithm
# that determines if a given node is reachable from another node
# very useful for p(x) and pp(x)

def Astar(map, computed_distances):
    return 0

# delta g function
# size = int(len(knights)/2)
# move --> [knight number, position]
# knights --> [white_knights, black_knights]
def p(A,exclude, white_distances, black_distances, knights, size,start_end):
    p = 0
    updated_white_distances = BFS(A, start_end[1], exclude[1])
    updated_black_distances = BFS(A, start_end[0], exclude[1])

    total_knights = single_array(knights[0], knights[1])

    for i in range(0, len(total_knights)):
        if i != exclude[0]:
            # KNIGHT IS NOT THERE
            p += g((i,total_knights[i]), white_distances, black_distances, size)
            # KNIGHT IS THERE
            p -= g((i,total_knights[i]), updated_white_distances, updated_black_distances, size)
            # KNIGHT IS NOT THERE - KNIGHT IS THERE
    return p

def find_knights(A):
    # first pre-scan grid to find all white and black knights
    w = []
    b = []

    for i in range(0, len(A)):
        for j in range(0, len(A[0])):
            if A[i][j] == "B":
                b.append(i * len(A[0]) + j)
            if A[i][j] == "W":
                w.append(i * len(A[0]) + j)

    return (w, b)

# count number of times 1D array B occurs in 2D array A
def count_array(A,B):
    count = 0
    for a in A:
        if match(a,B):
            count+=1
    return count

# determines index of when 1D array B first occurs in 2D array A
def repetition(A,B):
    index = -1
    for i in range(len(A)):
        if match(A[i], B):
            return i
    return index

# Takes in a map M, an index i, and a size of the array n
# Returns the index of the knight that is of the smallest distance in M
# ALSO returns the sum of all pairwise distances
def pair_knight(M, i, n, white_knights, black_knights, available_white_knights, available_black_knights):
    lowest_distance=float('inf')
    lowest_knight=-1
    distances=0
    if i < n and i > 0:
        # White Knight distance so look at all of black knights
        if i < int(n/2):
            lowest_knight=minIndex(available_black_knights) + int(n/2)
            for j in range(len(black_knights)):
                distances += M[black_knights[j]]
                if M[black_knights[j]] < lowest_distance and available_black_knights[j]:
                    lowest_distance=M[black_knights[j]]
                    lowest_knight=j + len(black_knights)
        # Else do the same but for white knights
        else:
            lowest_knight=minIndex(available_white_knights)
            for j in range(len(white_knights)):
                distances += M[white_knights[j]]
                if M[white_knights[j]] < lowest_distance and available_white_knights[j]:
                    lowest_distance=M[white_knights[j]]
                    lowest_knight=j
    return lowest_knight, distances

    # returns to minimum element in B that is true
def minIndex(B):
    for i in range(len(B)):
        if B[i] == True:
            return i
    return -1

board = [
    ["B", "B", "B", "B", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "N", "N", "N", "Y", "Y", "Y"],
    ["N", "Y", "Y", "Y", "Y", "N", "Y", "Y", "Y"],
    ["N", "Y", "Y", "N", "N", "N", "Y", "Y", "Y"],
    ["W", "W", "W", "W", "Y", "Y", "Y", "Y", "Y"],
]


board3 = [
    ["B", "B", "B", "B", "Y", "Y", "Y", "Y", "Y"],
    ["B", "B", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["W", "W", "W", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["W", "W", "Y", "Y", "Y", "W", "Y", "Y", "Y"],
]
board0 = [
    ["B", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["W", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
]
board4 = [
    ["Y", "B", "W", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "B", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "W", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "W", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "W", "Y", "B", "B", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ]
board7 = [
        ["W", "Y", "Y", "B", "Y", "B", "Y"],
        ["Y", "Y", "B", "Y", "N", "N", "Y"],
        ["Y", "Y", "W", "N", "N", "N", "W"],
        ["Y", "Y", "Y", "Y", "W", "N", "B"],
        ["Y", "B", "W", "Y", "Y", "Y", "Y"]
    ]

board2 = [
        ["N", "W", "N", "N"],
        ["N", "Y", "Y", "N"],
        ["N", "Y", "W", "Y"],
        ["B", "Y", "B", "Y"],
    ]

board6 = [
        ["B", "W", "Y", "Y"],
        ["W", "Y", "W", "Y"],
        ["Y", "B", "B", "Y"]
    ]

board7 = [
        ["N", "N", "N", "Y", "Y", "Y", "Y"],
        ["Y", "Y", "Y", "Y", "N", "N", "Y"],
        ["Y", "Y", "Y", "N", "N", "N", "Y"],
        ["B", "B", "W", "W", "N", "N", "Y"],
        ["B", "B", "W", "W", "Y", "Y", "Y"]
    ]


board1 = [
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "Y", "Y", "N", "Y", "Y", "Y"],
    ["Y", "N", "N", "N", "N", "N", "N", "Y", "B"],
    ["N", "Y", "N", "N", "N", "N", "N", "Y", "Y"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "Y", "N", "N", "N", "N", "N", "N"],
    ["Y", "Y", "Y", "N", "N", "Y", "N", "Y", "Y"],
    ["Y", "Y", "Y", "B", "Y", "Y", "N", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "W", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "N", "N", "N", "Y", "Y"],
    ["W", "Y", "Y", "B", "N", "N", "N", "W", "Y"]
    ]

board8 = [
    ["B", "Y", "Y", "Y", "Y", "Y", "B", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "B", "B", "Y", "Y", "Y", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "N", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "N", "N", "N", "Y", "Y", "Y"],
    ["N", "Y", "Y", "Y", "Y", "N", "Y", "Y", "Y"],
    ["W", "Y", "Y", "N", "N", "N", "Y", "Y", "Y"],
    ["W", "W", "W", "Y", "Y", "Y", "Y", "Y", "Y"],
]

board10 = [
    ["B", "Y", "N", "N", "N", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "N", "Y", "N", "N", "Y", "B", "Y"],
    ["Y", "Y", "N", "Y", "N", "N", "Y", "Y", "Y"],
    ["Y", "N", "Y", "Y", "N", "N", "N", "Y", "Y"],
    ["Y", "N", "Y", "Y", "N", "N", "N", "N", "B"],
    ["Y", "B", "B", "N", "N", "Y", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N", "Y", "N", "N"],
    ["Y", "N", "N", "Y", "Y", "Y", "Y", "N", "N"],
    ["Y", "N", "N", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "N"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "N"],
    ["Y", "N", "N", "N", "N", "N", "N", "Y", "N"],
    ["N", "N", "Y", "Y", "Y", "N", "N", "Y", "Y"],
    ["W", "N", "N", "N", "N", "N", "N", "N", "Y"],
    ["N", "W", "W", "N", "Y", "Y", "Y", "W", "W"],
]

board5 = [
    ["Y", "Y", "B", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "B", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "W", "W", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "W", "W", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "B", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "B", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ]

board11 = [
    ["B", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "W"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "W", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "B", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["W", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "B"],
    ]

board12 = [
        ["Y", "Y", "Y", "Y", "Y", "Y", "Y"],
        ["Y", "Y", "Y", "Y", "Y", "N", "Y"],
        ["Y", "Y", "Y", "Y", "N", "N", "Y"],
        ["Y", "Y", "Y", "N", "N", "N", "Y"],
        ["N", "N", "N", "N", "Y", "Y", "Y"],
        ["N", "N", "N", "Y", "Y", "Y", "Y"],
        ["N", "N", "N", "N", "N", "N", "Y"],
        ["N", "N", "N", "N", "N", "N", "Y"],
        ["B", "B", "W", "W", "Y", "Y", "Y"],
        ["B", "B", "W", "W", "Y", "Y", "Y"]
    ]

def main():
    limit = 800
    run_heurestic(board12, limit)


if "__main__" == __name__:
    main()
