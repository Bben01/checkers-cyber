MY_COLOR = False
WIN = float("inf")
LOSS = float("-inf")


def length_squared(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def farther_from_center(h_size, x, y):
    vx = abs(x - h_size)
    vy = abs(y - h_size)
    return vx + vy


def fortify_youserlf(pieces, piece_number):
    count = 0
    for i in range(piece_number):
        for j in range(i+1, piece_number):
            count += length_squared(pieces[i][0], pieces[i][1], pieces[j][0], pieces[j][1])
    return count


def closer_better(pieces1, piece1number, pieces2, piece2number, size, board):
    count = 0
    for i in range(piece1number):
        minLen = size * size * 10
        for j in range(piece2number):
            length = length_squared(pieces1[i][0], pieces1[i][1], pieces2[j][0], pieces2[j][1])
            if board[pieces2[j][0]][pieces2[j][1]].isKing:
                if length < minLen:
                    minLen = length
            count += length
        count += minLen
    return count


def evaluate_position(state):
    my_rating = 0
    his_rating = 0
    size = state.plateau.taillePlateau
    h_size = size / 2

    my_pieces = [[None for x in range(2)] for y in range(size * size)]
    my_piece_number = 0
    my_king_number = 0
    his_pieces = [[None for x in range(2)] for y in range(size * size)]
    his_piece_number = 0
    his_king_number = 0

    PAWN_VAL = 4 * size ** 3
    KING_VAL = 4 * PAWN_VAL
    CRITICAL_PIECE_NUMBER = size / 2
    POSITION_VS_PIECE_VAL = 10

    for i in range(size):
        for j in range(i % 2, size, 2):
            piece = state.plateau.board[i][j]
            if piece is not None:
                if piece.isWhite == MY_COLOR:
                    my_pieces[my_piece_number][0] = i
                    my_pieces[my_piece_number][1] = j
                    my_piece_number += 1
                    if piece.isKing:
                        my_king_number += 1
                else:
                    his_pieces[his_piece_number][0] = i
                    his_pieces[his_piece_number][1] = j
                    his_piece_number += 1
                    if piece.isKing:
                        his_king_number += 1

    for i in range(my_piece_number):
        my_rating += farther_from_center(h_size, my_pieces[i][0], my_pieces[i][1]) / POSITION_VS_PIECE_VAL

    for i in range(his_piece_number):
        his_rating += farther_from_center(h_size, his_pieces[i][0], his_pieces[i][1]) / POSITION_VS_PIECE_VAL

    my_rating += fortify_youserlf(his_pieces, his_piece_number)
    his_rating += fortify_youserlf(my_pieces, my_piece_number)

    hisPawnNumber = his_piece_number - his_king_number
    myPawnNumber = my_piece_number - my_king_number
    his_rating += his_king_number * KING_VAL + hisPawnNumber * PAWN_VAL
    my_rating += my_king_number * KING_VAL + myPawnNumber * PAWN_VAL

    if his_piece_number < CRITICAL_PIECE_NUMBER and my_piece_number >= his_piece_number:
        his_rating += closer_better(his_pieces, his_piece_number, my_pieces, my_piece_number, size, state.plateau.board)
    elif my_piece_number < CRITICAL_PIECE_NUMBER:
        my_rating += closer_better(my_pieces, my_piece_number, his_pieces, his_piece_number, size, state.plateau.board)

    if my_rating == 0:
        return LOSS
    elif his_rating == 0:
        return WIN
    else:
        return my_rating - his_rating
