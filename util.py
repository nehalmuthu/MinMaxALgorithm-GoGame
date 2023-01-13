import numpy as np

BOARD_SIZE=5

def getStepNumber(previous_board, board):
    flag1=flag2=0
    cnt = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if previous_board[i][j]!=0:
                flag1=1
                break

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j]!=0:
                flag2=1
                break

    if flag1==0 and flag2==0:
        step_number = 0
    elif flag1==0 and flag2!=0:
        step_number=1
    else:
        with open('step_num.txt') as step_number_file:
            step_number = int(step_number_file.readline())
            step_number += 2

    with open('step_num.txt', 'w') as step_number_file:
        step_number_file.write(f'{step_number}')

    return step_number


def getEulerScore(board, piece):
    opponent_piece = 3-piece

    type1,type2,type3 = 0,0,0
    type1_opponent,type2_opponent ,type3_opponent = 0,0,0

    new_board = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
    # First copy the original game_state

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            new_board[i + 1][j + 1] = board[i][j]

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            new_board_window = new_board[i: i + 2, j: j + 2]
            type1 += nQ1(new_board_window, piece)
            type2 += nQ2(new_board_window, piece)
            type3 += nQ3(new_board_window, piece)
            type1_opponent += nQ1(new_board_window, opponent_piece)
            type2_opponent += nQ2(new_board_window, opponent_piece)
            type3_opponent += nQ3(new_board_window, opponent_piece)


    return (type1 - type3 + 2 * type2 - (type1_opponent - type3_opponent + 2 * type2_opponent)) / 4


def nQ1(board, piece):
    p1=(board[0][0] == piece and board[0][1] != piece and board[1][0] != piece and board[1][1] != piece)
    p2=(board[0][0] != piece and board[0][1] == piece and board[1][0] != piece and board[1][1] != piece)
    p3=(board[0][0] != piece and board[0][1] != piece and board[1][0] == piece and board[1][1] != piece)
    p4=(board[0][0] != piece and board[0][1] != piece and board[1][0] != piece and board[1][1] == piece)
    return int(p1 or p2 or p3 or p4)

def nQ2(board, piece):
    p1=(board[0][0] == piece and board[0][1] != piece and board[1][0] != piece and board[1][1] == piece)
    p2=(board[0][0] != piece and board[0][1] == piece and board[1][0] == piece and board[1][1] != piece)
    return int(p1 or p2)

def nQ3(board, piece):
    p1= (board[0][0] == piece and board[0][1] == piece and board[1][0] == piece and board[1][1] != piece)
    p2= (board[0][0] != piece and board[0][1] == piece and board[1][0] == piece and board[1][1] == piece)
    p3= (board[0][0] == piece and board[0][1] != piece and board[1][0] == piece and board[1][1] == piece)
    p4= (board[0][0] == piece and board[0][1] == piece and board[1][0] != piece and board[1][1] == piece)
    return int(p1 or p2 or p3 or p4)
