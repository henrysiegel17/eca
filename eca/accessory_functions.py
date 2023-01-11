import naive
import heurestic
import copy
import random

# TAKES IN A BOARD B, and returns all squares that have MORE than two adjacent squares


def get_junction_points(B):
    junction_points = []
    A = get_primitive_board(B, -1)

    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j] == 'Y':
                coordinate = len(A[0])*i + j
                if len(heurestic.find_adjacent_moves(A, coordinate, [])) > 2:
                    junction_points.append(coordinate)
    return junction_points, A


def j_function(distances, square):
    return distances[square]

# Change everything to "Y" except where the knight is


def get_primitive_board(A, knight):
    board = copy.deepcopy(A)
    for i in range(0, len(A)):
        for j in range(0, len(A[0])):
            if A[i][j] != "N" and i * len(A[0]) + j != knight:
                board[i][j] = "Y"
    return board


def final_best_first_search(
    board,
    white_knights,
    black_knights,
    white_distances,
    black_distances,
    individual_repeat_table,
    repeat_table,
    individual_distance_map,
    paired_knights,
    p_size_limit
):
    total_knights = heurestic.single_array(white_knights, black_knights)

    # p_scoreboard adds up the number of knights that require a certain knight to move
    p_scoreboard = [0 for i in range(len(total_knights))]

    # p_size_limit caps the number of knights that are considered for the p_function
    # First, generate a random sample
    num_knights = len(total_knights)
    if p_size_limit > num_knights:
        p_size_limit = num_knights

    p_sample_indices = random.sample(range(0, num_knights), p_size_limit)

    for knight_num in range(p_size_limit):
        legal_moves = heurestic.find_adjacent_moves(
            board, total_knights[p_sample_indices[knight_num]], total_knights)
        all_possible_moves = heurestic.find_adjacent_moves(
            board, total_knights[p_sample_indices[knight_num]], [])

        # THE SET MINUS CORRESPONDS TO ALL SQUARES THAT HAVE AN OCCUPIED KNIGHT
        # CHECK THESE SQUARES TO ADD UP p_scoreboard
        knight_squares = set(all_possible_moves) - set(legal_moves)
        for p_square in knight_squares:
            p_score = p_function(p_square, all_possible_moves, total_knights[knight_num], knight_num, len(
                total_knights), white_distances, black_distances)
            p_knight_num = total_knights.index(p_square)
            p_scoreboard[p_knight_num] += p_score

    min_score = float('inf')
    possible_moves = []
    for knight_num in range(0, len(total_knights)):
        legal_moves = heurestic.find_adjacent_moves(
            board, total_knights[knight_num], total_knights)
        for legal_move_num in range(len(legal_moves)):

            # hypothetical_knights --> position after knight moves
            hypothetical_knights = total_knights.copy()
            hypothetical_knights[knight_num] = legal_moves[legal_move_num]

            # FIRST THE INDIVIDUAL REPEAT PENALTY:
            individual_repeat_penalty = 0
            if legal_moves[legal_move_num] in individual_repeat_table[knight_num].keys():
                individual_repeat_penalty = individual_repeat_table[knight_num][legal_moves[legal_move_num]]/len(
                    total_knights)

            # THEN THE COMBINED REPEAT PENALTY:
            repeat_penalty = heurestic.count_array(
                repeat_table, hypothetical_knights)

            # NOW THE GOOD O'l g_function
            g_score = g_function(legal_moves[legal_move_num], total_knights[knight_num], knight_num, len(
                total_knights), white_distances, black_distances)/len(total_knights)

            # AND THE UGLY i_function
            i_score = i_function(legal_moves[legal_move_num], total_knights[knight_num],
                                 knight_num, paired_knights, individual_distance_map)

            # THE THEORETICAL p_function (looks one move ahead)
            p_prime = 0

            # BUT ONLY DO THIS IF THE KNIGHT NUMBER IS IN THE P_SAMPLE
            if knight_num in p_sample_indices:
                hypothetical_all_adjacent_moves = heurestic.find_adjacent_moves(
                    board, hypothetical_knights[knight_num], [])
                hypothetical_legal_adjacent_moves = heurestic.find_adjacent_moves(
                    board, hypothetical_knights[knight_num], hypothetical_knights)
                hypothetical_conflicting_squares = set(
                    hypothetical_all_adjacent_moves) - set(hypothetical_legal_adjacent_moves)

                for p_prime_square in hypothetical_conflicting_squares:
                    p_prime -= p_function(p_prime_square, hypothetical_all_adjacent_moves, hypothetical_knights[knight_num], knight_num, len(
                        hypothetical_knights), white_distances, black_distances)

            score = individual_repeat_penalty + repeat_penalty + \
                g_score + i_score + p_scoreboard[knight_num] + p_prime

            if score < min_score:
                min_score = score
                possible_moves = []
                possible_moves.append(
                    (knight_num, legal_moves[legal_move_num]))
            elif score == min_score:
                possible_moves.append(
                    (knight_num, legal_moves[legal_move_num]))

    rand_index = random.randint(0, len(possible_moves)-1)
    return possible_moves[rand_index]


# p_function determines the change in the minimum g_score of all_possible_moves when p_square is removed from it
def p_function(p_square, all_possible_moves, knight_position, knight_num, size, white_distances, black_distances):
    compared_to_moves = copy.deepcopy(all_possible_moves)
    compared_to_moves.remove(p_square)
    if len(compared_to_moves) > 0:
        original_g_scores = [g_function(all_possible_moves[i], knight_position, knight_num,
                                        size, white_distances, black_distances) for i in range(len(all_possible_moves))]
        final_g_scores = [g_function(compared_to_moves[i], knight_position, knight_num,
                                     size, white_distances, black_distances) for i in range(len(compared_to_moves))]
    if len(compared_to_moves) == 0:
        return -2
    else:
        return -1*(min(final_g_scores) - min(original_g_scores))

# determines the change in the knight's distance after it makes a move


def g_function(legal_move, knight_position, knight_num, size, white_distances, black_distances):

    # IF WHITE KNIGHT, USE WHITE DISTANCES
    if knight_num < int(size/2):
        return (white_distances[legal_move] - white_distances[knight_position])
    else:
        return (black_distances[legal_move] - black_distances[knight_position])

# returns paired knight distance


def i_function(legal_move, knight_position, knight_num, paired_knights, individual_distance_map):
    distance_index = paired_knights.index(knight_num)
    return individual_distance_map[distance_index][legal_move] - individual_distance_map[distance_index][knight_position]

# CHECK ENDING TAKES IN ARRAYS A and B and determines if B is an ending position of A


def check_ending(A, B):
    for i in range(0, int(len(A)/2)):
        if A[i] in B:
            b_index = B.index(A[i])
            if b_index < int(len(A)/2):
                return False
        else:
            return False

    for j in range(int(len(A)/2), len(A)):
        if A[j] in B:
            b_index = B.index(A[j])
            if b_index >= int(len(A)/2):
                return False
        else:
            return False
    return True

# THIS IS THE FUNCTION THAT REASSIGNS THE POSITIONS OF THE KNIGHTS TO RERUN HEURESTIC ON "HOPEFULLY" AN EASIER POSITION


def crisis(
        board,
        white_knights,
        black_knights,
        p_size_limit,
        individual_junction_distances,
        rand_limit,
        small_limit
):

    # ONE SIGN THAT THE ALGORITHM IS FAILING IS IF THE BIGCOUNT IS TOO HIGH

    # THIS IS NOT THE SAME AS THE PATH THAT IS PRINTED OUT: move_path = [[knight num, starting_square, ending_square], ...]
    move_path = []

    # NOW THIS IS THE ACTUAL_PATH, WHAT WE WILL RETURN:
    actual_path = []

    # FIRST STEP IS TO RANDOMIZE THE BOARD
    # BUT WE ALSO MUST SAVE THE PATH THE KNIGHTS TAKE, SO WE CAN RELAY IT BACK
    total_knights = heurestic.single_array(white_knights, black_knights)
    rand_counter = 0
        
    while rand_counter < rand_limit:

        # FIRST STEP IS ESSENTIALLY THE SAME AS computing only the g_score in best first search
        min_score = float('inf')
        possible_moves = []
        position = []

        # update actual_path
        for q in range(len(total_knights)):
            coordinates = naive.thicken(len(board[0]), total_knights[q])
            position.append(coordinates)
        actual_path.append(position)

        for knight_num in range(0, len(total_knights)):
            legal_moves = heurestic.find_adjacent_moves(
                board, total_knights[knight_num], total_knights)
            rand_i = random.randint(0, len(individual_junction_distances)-1)
            for legal_move_num in range(len(legal_moves)):
                score = g_function(
                    legal_moves[legal_move_num],
                    total_knights[knight_num],
                    knight_num,
                    len(total_knights),
                    individual_junction_distances[rand_i],
                    individual_junction_distances[rand_i])

                if score < min_score:
                    min_score = score
                    possible_moves = []
                    possible_moves.append(
                        (knight_num, legal_moves[legal_move_num]))
                elif score == min_score:
                    possible_moves.append(
                        (knight_num, legal_moves[legal_move_num]))

        rand_index = random.randint(0, len(possible_moves)-1)
        move = possible_moves[rand_index]


        # update move_path
        move_path.append((move[0], total_knights[move[0]]))
        rand_counter += 1

        # update knights
        if move[0] < int(len(total_knights)/2):
            white_knights[move[0]] = move[1]
        else:
            black_knights[move[0] % int(len(total_knights)/2)] = move[1]
        total_knights[move[0]] = move[1]
    
    position = []
    for q in range(len(total_knights)):
        coordinates = naive.thicken(len(board[0]), total_knights[q])
        position.append(coordinates)
    actual_path.append(position)

    # STEP 2: RUN BEST FIRST SEARCH ON OUR CURRENT POSITION OF KNIGHTS
    BFS_count = 0
    start_values = copy.deepcopy(total_knights)
    repeat_table = []
    repeat_table.append(start_values)
    individual_repeat_table = [{total_knights[t]: 1} for t in range(len(total_knights))]

    # COMPUTE NEW WHITE AND BLACK DISTANCES
    white_distances = heurestic.BFS(board, black_knights, -1)
    black_distances = heurestic.BFS(board, white_knights, -1)

    # COMPUTE NEW INDIVIDUAL DISTANCES
    individual_distances_maps = [heurestic.BFS(
        board, total_knights[i], -1) for i in range(0, len(total_knights))]

    # COMPUTE PAIRED KNIGHTS
    available_white_knights = []
    available_black_knights = []

    paired_knights = []
    # We have a white knight, so it must be paired up with a black knight
    for k in range(len(white_knights)):
        available_white_knights.append(True)
        paired_knights.append(k + len(white_knights))
    # We have a black knight, so it must be paired up with a white knight
    for m in range(len(black_knights)):
        available_black_knights.append(True)
        paired_knights.append(m)

    for i in range(len(total_knights)):
        paired_knight, distances = heurestic.pair_knight(individual_distances_maps[i], i, len(
            total_knights), white_knights, black_knights, available_white_knights, available_black_knights)

        if paired_knight != -1:
            # If paired_knight is less than the number of white knights, we know the paired knight is a white_knight
            if paired_knight < len(white_knights):
                available_white_knights[paired_knight] = False
            else:
                available_black_knights[paired_knight -
                                        len(black_knights)] = False
            paired_knights[i] = paired_knight
        else:
            if paired_knights[i] < len(white_knights):
                available_white_knights[paired_knights[i]] = False
            else:
                available_black_knights[paired_knights[i] -
                                        len(black_knights)] = False
    BFS_path = []
    print("start values: ", start_values)
    print("starting knight positions: ", total_knights)
    while check_ending(start_values, total_knights) == False and BFS_count < small_limit:
        position = []
        move = final_best_first_search(
            board,
            white_knights,
            black_knights,
            white_distances,
            black_distances,
            individual_repeat_table,
            repeat_table,
            individual_distances_maps,
            paired_knights,
            p_size_limit
        )

        total_knights[move[0]] = move[1]
        # update knights:
        if move[0] < int(len(total_knights)/2):
            white_knights[move[0]] = move[1]
        else:
            black_knights[move[0] % int(len(total_knights)/2)] = move[1]

        # update repeats
        repeat_table.append(total_knights.copy())

        # update paths
        for i in range(len(total_knights)):
            coordinates = naive.thicken(len(board[0]), total_knights[i])
            position.append(coordinates)
        actual_path.append(position)
        BFS_path.append(position)

        # CHECK REPEATS:
        repeat_index = heurestic.repetition(BFS_path, position)
        if repeat_index != len(BFS_path)-1:
            # GET RID OF PATH
            BFS_path = BFS_path[:repeat_index+1]
            actual_path = actual_path[:repeat_index+2+rand_limit]
        # ELSE WE DON'T HAVE A REPEAT AND WE'RE GOOD

         # UPDATE INDIVIDUAL REPEAT DISTANCES
        if move[1] in individual_repeat_table[move[0]].keys():
            individual_repeat_table[move[0]][move[1]] += 1
        else:
            individual_repeat_table[move[0]][move[1]] = 1

        BFS_count += 1

    print(total_knights)
    # WE HAVE FAILED UNFORTUNATELY, SO WE CANNOT CONTINUE
    if check_ending(start_values, total_knights) == False:
        return actual_path, False

    # NOW BECAUSE THE KNIGHTS HAVE SUCCESSFULLY SWAPPED, start_values will be a permutation of total_knights
    '''
        define changed_knights_mapping: start_values  --> total_knights
        such that changed_knights_mapping(i) 
        = the particular knight in total_knights for all i in start_values
    '''

    changed_knights_mapping = [total_knights.index(start_values[s]) for s in range(0, len(start_values))]
    print(changed_knights_mapping)

    # NOW WE REVERSE THE MOVE PATH
    for move_path_num in reversed(range(len(move_path))):
        random_moved_knight = move_path[move_path_num][0]
        moved_square = move_path[move_path_num][1]

        total_knights[changed_knights_mapping[random_moved_knight]] = moved_square

        position = []
        for i in range(len(total_knights)):
            coordinates = naive.thicken(len(board[0]), total_knights[i])
            position.append(coordinates)
        actual_path.append(position)
    return actual_path, True
