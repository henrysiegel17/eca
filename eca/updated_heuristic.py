import heurestic
import copy
import random
import accessory_functions
from naive import thicken, single_array, base_x, printBoard, complementary

# takes in board and knights, returns the best move at any given instance


def updated_hueristic(board, small_limit, big_limit, p_size_limit, rand_limit):
    start_end = []
    knights = heurestic.find_knights(board)
    for i in range(len(knights)):
        pos = []
        for j in range(len(knights[i])):
            pos.append(knights[i][j])
        start_end.append(pos)
    # white knights
    white_distances = heurestic.BFS(board, knights[1], -1)
    # black knights
    black_distances = heurestic.BFS(board, knights[0], -1)
    real_knights = heurestic.single_array(knights[0], knights[1])
    start_values = copy.deepcopy(real_knights)
    start_white_knights = copy.deepcopy(knights[0])
    start_black_knights = copy.deepcopy(knights[1])

    # BLACK KNIGHT STARTS --> WHITE GOALS:
    # USE BLACK DISTANCES

    # WHITE KNIGHT STARTS --> BLACK GOALS
    # USE WHITE DISTANCES

    # knights = [white, black]

    path = []
    count = 0
    repeat_table = []
    # IF repeat_indices[i] != i, then we know we have a repeat.
    # SPECIFICALLY, the element repeat_indices[i] points to the index where the repetition started
    repeat_indices = []

    c = []
    position = []
    individual_distances_maps = []
    paired_knights = []
    available_white_knights = []
    available_black_knights = []
    i_weights = [0 for z in range(len(real_knights))]
    total_white_distances = 0
    total_black_distances = 0
    # We have a white knight, so it must be paired up with a black knight
    for k in range(len(knights[0])):
        available_white_knights.append(True)
        paired_knights.append(k + len(knights[0]))
    # We have a black knight, so it must be paired up with a white knight
    for m in range(len(knights[1])):
        available_black_knights.append(True)
        paired_knights.append(m)

    for i in range(len(real_knights)):
        # GET INDIVIDUAL DISTANCES
        primitive_board = get_primitive_board(board, real_knights[i])
        individual_distances_maps.append(
            heurestic.BFS(primitive_board, real_knights[i], -1))

        # NOW GET MINIMUM DISTANCE --> THIS IS THE "PAIRED" KNIGHT
        # We also want to add up all pairwise distances
        paired_knight, distances = heurestic.pair_knight(individual_distances_maps[i], i, len(
            real_knights), knights[0], knights[1], available_white_knights, available_black_knights)

        # compute i_weights
        i_weights[i] = distances

        if paired_knight != -1:
        # If paired_knight is less than the number of white knights, we know the paired knight is a white_knight
            if paired_knight < len(knights[0]):
                total_white_distances += distances
                available_white_knights[paired_knight] = False
            else:
                available_black_knights[paired_knight -
                    len(knights[0])] = False
                total_black_distances += distances
            paired_knights[i] = paired_knight
        else:
            if paired_knights[i] < len(knights[0]):
                total_white_distances += distances
                available_white_knights[paired_knights[i]] = False
            else:
                available_black_knights[paired_knights[i] -
                    len(knights[0])] = False
                total_black_distances += distances

        coordinates = thicken(len(board[0]), real_knights[i])
        c.append(real_knights[i])
        position.append(coordinates)
    path.append(position)

    '''
    if total_white_distances != 0:
        for w in range(len(real_knights)):
            if w < len(knights[0]):
                i_weights[w] = (total_white_distances -
                                i_weights[w])/total_white_distances
            else:
                i_weights[w] = (total_black_distances -
                                i_weights[w])/total_black_distances
    '''
    # GET JUNCTION POINTS
    junction_points, basic_board = accessory_functions.get_junction_points(
        board)
    junction_distances = heurestic.BFS(basic_board, junction_points, -1)
    individual_junction_distances = []
    for i in range(len(junction_points)):
        individual_junction_distances.append(
            heurestic.BFS(basic_board, junction_points[i], -1))

    individual_repeat_table = [{real_knights[i]: 1} for i in range(len(real_knights))]

    # THIS VARIABLE INDICATES WHETHER THE ALGORITHM IS FAILING OR NOT
    crisis_mode = False
    # WHILE WE ARE NOT DONE:
    bigcount = 0
    crisis_success = False
    while bigcount < big_limit:
        while accessory_functions.check_ending(start_values, real_knights) == False and count < small_limit:
            if crisis_mode == False:
                position = []
                # A, knights, white_distances, black_distances, down_map, up_map
                '''
                move = best_first_search(
                    board,
                    knights,
                    white_distances,
                    black_distances,
                    start_end,
                    repeat_table,
                    individual_distances_maps,
                    paired_knights,
                    i_weights,
                    junction_distances,
                    individual_junction_distances
                )
                '''
                
                move = accessory_functions.final_best_first_search(
                board,
                knights[0],
                knights[1],
                white_distances,
                black_distances,
                individual_repeat_table,
                repeat_table,
                individual_distances_maps,
                paired_knights,
                p_size_limit
                )

                real_knights[move[0]]=move[1]
                # update knights:
                if move[0] < int(len(real_knights)/2):
                    knights[0][move[0]]=move[1]
                else:
                    knights[1][move[0] % int(len(real_knights)/2)]=move[1]
                count += 1

                # update repeats
                repeat_table.append(real_knights.copy())

                # update paths
                c=[]
                for i in range(len(real_knights)):
                    coordinates=thicken(len(board[0]), real_knights[i])
                    c.append(real_knights[i])
                    position.append(coordinates)
                path.append(position)

                
                # CHECK REPEATS:
                real_knights=heurestic.single_array(knights[0], knights[1])
                repeat_index=heurestic.repetition(path, position)
                if repeat_index != len(path)-1:
                    # GET RID OF PATH
                    repeat=True
                    path=path[:repeat_index+1]
                # ELSE WE DON'T HAVE A REPEAT AND WE'RE GOOD
                

                # UPDATE PAIRED_KNIGHTS:
                '''
                if len(path) % len(real_knights) == len(real_knights)-1:


                    paired_knights = update_paired_knights(
                        paired_knights, real_knights, individual_distances_maps)

                '''

                # UPDATE INDIVIDUAL REPEAT DISTANCES
                if move[1] in individual_repeat_table[move[0]].keys():
                    individual_repeat_table[move[0]][move[1]] += 1
                else:
                    individual_repeat_table[move[0]][move[1]] = 1
            else:
                path, crisis_success = accessory_functions.crisis(
                board,
                knights[0],
                knights[1],
                p_size_limit,
                individual_junction_distances,
                rand_limit,
                small_limit
                )
                count = small_limit

        # IF WE ARE DONE
        if crisis_success or accessory_functions.check_ending(start_values, real_knights) == True or bigcount == big_limit-1:
            break
        else:
            # RESET EVERYTHING AND START AGAIN
            count = 0
            knights = (copy.deepcopy(start_white_knights), copy.deepcopy(start_black_knights))
            real_knights = copy.deepcopy(start_values)
            repeat_table = []
            repeat_table.append(start_values)
            individual_repeat_table = []
            individual_repeat_table = [{real_knights[t]: 1} for t in range(len(real_knights))]

            path=[]
            position = []
            for q in range(len(real_knights)):
                coordinates = thicken(len(board[0]), real_knights[q])
                position.append(coordinates)
            path.append(position)

            
            if bigcount > int(big_limit/2):
                # WE HAVE A SERIOUS PROBLEM
                crisis_mode = True

        if bigcount > 0:
            print("Number of failed attempts: ", bigcount)
        bigcount+=1

    if bigcount < big_limit -1:
        print("I found a solution!")
        print("Length of path is ", len(path))
    else:
        print("Sorry I can't find a solution")
    printBoard(board, path)

def best_first_search(
        A,
        knights,
        white_distances,
        black_distances,
        start_end,
        repeat_table,
        individual_distances_maps,
        paired_knights,
        i_weights,
        junction_distances,
        individual_junction_distances
    ):
        # **************** adjacent moves = {total_knights i : adjacent squares}
        # **************** knights = [white, black]
        # **************** move = [i, j] --> knight i, and square j
    white_knights=knights[0]
    black_knights=knights[1]
    real_knights=single_array(knights[0], knights[1])
    total_knights=single_array(white_knights, black_knights)
    adjacent_moves={}
    for i in range(len(total_knights)):
        reachable_squares=heurestic.find_adjacent_moves(
            A, total_knights[i], total_knights)
        adjacent_moves[i]=reachable_squares
    lowest_move=[0, 0]
    best_moves=[]
    best_moves.append(lowest_move)
    for m in range(len(adjacent_moves)):
        for k in range(len(adjacent_moves[m])):
            lowest_move=[m, adjacent_moves[m][k]]
    low=float('inf')
    for knight_num, squares in adjacent_moves.items():
        for s in range(len(squares)):
            move=(knight_num, squares[s])

            # COMPUTE g_weight
            g_weight=1/len(real_knights)
            g_value=g_weight*(heurestic.g(move, white_distances,
                              black_distances, int(len(total_knights) / 2)) - heurestic.g([knight_num, total_knights[knight_num]], white_distances,
                                                                                black_distances, int(len(total_knights) / 2)))

            # A,move, white_distances, black_distances, knights, size
            p_value=heurestic.p(
                A,
                [knight_num, total_knights[knight_num]],
                white_distances,
                black_distances,
                knights,
                int(len(total_knights) / 2),
                start_end
            )

            # IF THE KNIGHT IS A ROADBLOCK, WE WANT IT TO MOVE TOWARDS A JUNCTION POINT
            j_cost=0
            if p_value < -1000:
                j_cost += -1*p_value*(accessory_functions.j_function(junction_distances,
                                      squares[s]) - accessory_functions.j_function(junction_distances, real_knights[knight_num]))
                rand_index=random.randint(
                    0, len(individual_junction_distances)-1)
                j_cost += -1*p_value*(accessory_functions.j_function(individual_junction_distances[rand_index], squares[s]) - accessory_functions.j_function(
                    individual_junction_distances[rand_index], real_knights[knight_num]))
                if j_cost > 0:
                    j_cost=0

            hypothetical_knights=total_knights.copy()
            hypothetical_knights[move[0]]=move[1]
            # DISCOURAGE ALGORITHM FROM REPEATING MOVES
            repeat_penalty=heurestic.count_array(
                repeat_table, hypothetical_knights)*100000000*(len(total_knights)/2-1)
            # individual_distance_function
            # Ideally want this to be negative: square - original

            '''
            For each knight, we want to find the ending position to compare the knight to
            ending_index = paired_knights.getIndex(knight_num)

            The knight moves:
            squares[s]

            Now the i_distance:
            i_cost = i(squares[s], individual_distances_maps[ending_index]) - \
                       i(knights[knight_num],
                         individual_distances_maps[ending_index])

            '''
            ending_index=paired_knights.index(knight_num)
            i_cost=0
            i_cost=i_function(squares[s], individual_distances_maps[ending_index], i_weights[knight_num]) - i_function(
                real_knights[knight_num], individual_distances_maps[ending_index], i_weights[knight_num])
            score=g_value + p_value + repeat_penalty + i_cost + j_cost
            if score < low:
                low=score
                lowest_move=move
                best_moves=[]
                best_moves.append(lowest_move)
            # NOW THE RANDOM MOVE_ASPECT
            elif score == low:
                best_moves.append(move)
    num=random.randint(0, len(best_moves)-1)
    return best_moves[num]


# Change everything to "Y" except where the knight is
def get_primitive_board(A, knight):
    board=copy.deepcopy(A)
    for i in range(0, len(A)):
        for j in range(0, len(A[0])):
            if A[i][j] != "N" and i * len(A[0]) + j != knight:
                board[i][j]="Y"
    return board

def i_function(square, distances, weight):
    return distances[square]
