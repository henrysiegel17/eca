from cmath import inf
from pygame.locals import *
from naive import thicken

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


def best_first_search(
    A,
    knights,
    white_distances,
    black_distances,
    white_up_map,
    black_up_map,
    white_down_map,
    black_down_map,
):
    # **************** adjacent moves = {knight i : adjacent squares}
    # **************** knights = [white, black]
    # **************** move = [i, j] --> knight i, and square j
    adjacent_moves = {}
    for i in range(len(knights)):
        reachable_squares = find_adjacent_moves(A, knights[i], knights, [])
        adjacent_moves[i] = reachable_squares
    lowest_move = [0, adjacent_moves[0][0]]
    low = 1000000
    for knight_num, squares in adjacent_moves.keys():
        p_considerations = []
        for s in range(len(squares)):
            move = [knight_num, squares[s]]
            g = g(move, white_distances, black_distances, int(len(knights) / 2))
            # knights, i, down_map, up_map, white_distances, black_distances, size
            p = p(
                knights,
                s,
                white_up_map,
                black_up_map,
                white_down_map,
                black_down_map,
                white_distances,
                black_distances,
                knights[knight_num],
                int(len(knights) / 2),
            )
            # While p is the priority of the knight moving, pn is an estimate of the priority after n iterations
            p_considerations.append(p)
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
            pn = pn()
            score = g + p
            if score < low:
                low = score
                lowest_move = move

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
        # white knight
        return white_distances[move]
    return black_distances[move]


# p(x) = Σ (change g(x) for each other knight when the given knight exists or not)
# index i --> which knight we want to consider


def p(
    knights,
    i,
    white_down_map,
    black_down_map,
    white_up_map,
    black_up_map,
    white_distances,
    black_distances,
    move,
    size,
):
    p = 0

    updated_white_distances = propagate_graph(
        move, white_down_map, white_up_map, white_distances, size
    )
    updated_black_distances = propagate_graph(
        move, black_down_map, black_up_map, black_distances, size
    )

    for k in range(size):
        if k == i:
            continue
        elif k != i:
            # In order to compute Δg, we need to compute g' - g,
            # where g' is g([k,knight[k]], updated_white_distances, updated_black_distances, size of knights)
            # and g is g([k, knight[k]], white_distances, black_distances, size of knights)

            if k < size:
                p += g([k, knights[k]], updated_white_distances,
                       black_distances, size)
            elif k >= size:
                p += g([k, knights[k]], white_distances,
                       updated_black_distances, size)

    # note that p >= 0
    return p


# iteratively calls p


def pn(
    knights,
    i,
    down_map,
    up_map,
    white_distances,
    black_distances,
    adjacent_moves,
    size,
    n,
):
    return p(
        knights,
        i,
        down_map,
        up_map,
        white_distances,
        black_distances,
        adjacent_moves[n],
        size,
    )


# BY CHANGING NODE n's DISTANCE TO INFINITY, THAT MAY OR MAY NOT CHANGE EVERY OTHER NODE'S DISTANCE
def propagate_graph(n, down_map, up_map, distances, size):

    used = []
    queue = []
    queue.append(n)
    distances[n] = float("inf") / (2 * size)

    while len(queue) > 0:
        u = queue[0]
        queue.pop(0)

        # u is the node we are exploring, and we are determining whether the
        # distances of the parents of u depend on the distance of u
        for v in up_map[u] and v not in used:
            # look at all nodes v one level above
            if len(down_map[v] == 1):
                # in other words, distance[v] is fully dependent on distance[u]
                used.append(v)
                queue.append(distances)

    return distances


# We want to pre-compute every square's distance away from the origins,
# as well as creating a map that stores all adjacent nodes to any given node
# very useful for computing g(x), p(x), pp(x)


def BFS(A, origins):

    # BFS
    # we start with a Queue that stores all adjacent configurations that should be explored
    Queue = []

    # used_moves contains all moves that we already checked
    used_moves = []

    # distance counter --> indicates every node's distance from origin
    dist = {}

    # in the beginning, we assume every node's distance from the origin is "infinity"
    for i in range(len(A)):
        for j in range(len(A[0])):
            dist[i * len(A[0]) + j] = float("inf") / (2 * len(origins))

    # We store a map that points to all higher_up nodes (with distances 1 larger):
    up_map = {}

    # Similarly we'll make a down_map that points to all lower nodes (with distances 1 smaller):
    down_map = {}

    # In the beginning, all origins are of 0 distance, Queue and used_moves contains all origins
    for o in origins:
        dist[o] = 0
        Queue.append(o)
        used_moves.append(o)

    while (len(Queue)) != 0:
        u = Queue[0]
        Queue.pop(0)
        # explore u --> IS AN INTEGER

        # find adjacent vertices
        adjacent_moves = find_adjacent_moves(A, u, used_moves)

        # append to queue and used_moves list
        # update distances accordingly
        for move in adjacent_moves:
            down_map[move].append(u)
            dist[move] = dist[u] + 1
            Queue.append(move)
            used_moves.append(move)

        # Update up and down maps accordingly
        up_map[u] = adjacent_moves

        # I know this doubles the time of the algorithm, but I have no other choice
        all_possible_moves = find_adjacent_moves(A, u, [])
        for non_discriminatory_move in all_possible_moves:
            if dist[non_discriminatory_move] < dist[u]:
                down_map[u].append(non_discriminatory_move)

    return dist, up_map, down_map


# We need to define one more function, an actual Astar algorithm
# that determines if a given node is reachable from another node
# very useful for p(x) and pp(x)


def Astar(map, computed_distances):
    return 0


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


board = oneknight = [
    ["Y", "W", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
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
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
    ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "B"],
]


def main():
    knights = find_knights(board)
    # white knights
    white_distances = BFS(board, knights[1])
    # black knights
    black_distances = BFS(board, knights[0])

    # A, knights, white_distances, black_distances, down_map, up_map
    move = best_first_search(
        board,
        knights,
        white_distances[0],
        black_distances[0],
        white_distances[1],
        black_distances[1],
        white_distances[2],
        black_distances[2],
    )
    print(move)


if "__main__" == __name__:
    main()
