import copy
import random
import numpy as np
from read import readInput
from write import writeOutput
from util import  getEulerScore, getStepNumber

BOARD_SIZE = 5
KOMI = 2.5

class MyPlayer:
    def __init__(self, piece, previous_board, board):
        self.piece = piece
        self.opponent_piece = 3-self.piece
        self.previous_board = previous_board
        self.board = board


    def score(self,board, piece_type):
        cnt = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == piece_type:
                    cnt += 1
        return cnt


    def getSideCounts(self,board,piece):
        opponent_piece=3-piece
        side_edge_count = 0
        opponent_side_edge_count = 0
        for j in range(BOARD_SIZE):
            if board[0][j] == piece:
                side_edge_count += 1
            if board[BOARD_SIZE - 1][j] == piece:
                side_edge_count += 1
            if board[BOARD_SIZE - 1][j] == opponent_piece:
                opponent_side_edge_count += 1
            if board[0][j] == opponent_piece:
                opponent_side_edge_count += 1

        for j in range(1, BOARD_SIZE - 1):
            if board[j][BOARD_SIZE - 1] == piece:
                side_edge_count += 1
            if board[j][0] == piece:
                side_edge_count += 1
            if board[j][0] == opponent_piece:
                opponent_side_edge_count += 1
            if board[j][BOARD_SIZE - 1] == opponent_piece:
                opponent_side_edge_count += 1
        return side_edge_count,opponent_side_edge_count


    def getCenterCount(self,board):
        center_unoccupied_count = 0
        for i in range(1, BOARD_SIZE - 1):
            for j in range(1, BOARD_SIZE - 1):
                if board[i][j] == 0:
                    center_unoccupied_count += 1
        return center_unoccupied_count

    def getLiberty(self,board,piece):
        side_liberty,opponent_liberty = set(),set()
        opponent_side = 3-piece
        xindex = [1, 0, -1, 0]
        yindex = [0, 1, 0, -1]

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 0:
                    for index in range(len(xindex)):
                        newi, newj = i + xindex[index], j + yindex[index]
                        if 0 <= newi < BOARD_SIZE and 0 <= newj < BOARD_SIZE:
                            if board[newi][newj] == piece:
                                side_liberty.add((i, j))
                            elif board[newi][newj] == opponent_side:
                                opponent_liberty.add((i, j))
        return side_liberty,opponent_liberty


    def evaluateHeuristic(self, board, piece):
        # Define heuristic here
        # Count number of sides stones - opponent stones
        opponent_piece = 3-piece

        side_count,opponent_count=self.score(board,piece),self.score(board,opponent_piece)

        side_liberty,opponent_liberty= self.getLiberty(board,piece)

        center_unoccupied_count=self.getCenterCount(board)

        side_edge_count,opponent_side_edge_count = self.getSideCounts(board,piece)

        eulerScore=getEulerScore(board, piece)
        sideScore=(side_count - opponent_count)
        sideLibertyScore=(len(side_liberty) - len(opponent_liberty))
        score = min(max(sideLibertyScore, -8), 8)  - 4 * eulerScore + (5 * sideScore) - (9 * side_edge_count * (center_unoccupied_count / 9))
        if self.piece == 2:
            score += KOMI
        return score

    def move(self, board, piece, move):
        new_board=copy.deepcopy(board)
        new_board[move[0]][move[1]] = piece
        new_board, died_pieces = self.remove_died_pieces(new_board,3 - piece)
        return new_board

    def Max_Move(self, board, piece,alpha, beta, max_depth, current_depth, branch, isEnd, isEndPass,step_number):
        if max_depth == current_depth or step_number + current_depth == 24:
            return self.evaluateHeuristic(board, piece)
        if isEndPass:
            return self.evaluateHeuristic(board, piece)

        valid_moves=[]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.valid_place_check(board,i, j, piece, test_check = True):
                    valid_moves.append((i,j))

        valid_moves.append("end")

        isEndPass = False
        maxi_value, maxi_move = -np.inf,None

        if isEnd == "end":
            isEndPass = True
        for valid_move in valid_moves[:branch]:
            # Create new game state
            opponent_piece = 3-piece
            if valid_move == "end":
                new_board = copy.deepcopy(board)
            else:
                new_board = self.move(board, piece, valid_move)
            minScore = self.Min_Move(new_board, opponent_piece,alpha, beta, max_depth, current_depth + 1,
                                            branch,  valid_move, isEndPass,step_number)
            if maxi_value < minScore:
                maxi_move = valid_move
                maxi_value = minScore

            if maxi_value >= beta:
                if current_depth == 0:
                    return maxi_move, maxi_value
                else:
                    return maxi_value

            if maxi_value>alpha:
                alpha=maxi_value

        if current_depth == 0:
            return maxi_move, maxi_value
        else:
            return maxi_value

    def Min_Move(self, board, piece,alpha, beta, max_depth, current_depth, branch,  isEnd, isEndPass, step_number):
        if max_depth == current_depth:
            return self.evaluateHeuristic(board, piece)
        if step_number + current_depth == 24 or isEndPass:
            return self.evaluateHeuristic(board, self.piece)

        valid_moves=[]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.valid_place_check(board,i, j, piece, test_check = True):
                    valid_moves.append((i,j))

        valid_moves.append("end")

        mini_value, isEndPass = np.inf, False

        if isEnd == "end":
            isEndPass = True

        for valid_move in valid_moves[:branch]:
            # Create new game state
            opponent_piece = 3-piece
            if valid_move == "end":
                new_board = copy.deepcopy(board)
            else:
                new_board = self.move(board, piece, valid_move)
            maxi_score = self.Max_Move(new_board, opponent_piece, alpha, beta, max_depth, current_depth + 1,
                                            branch, valid_move, isEndPass, step_number)
            if maxi_score < mini_value:
                mini_value = maxi_score
            if mini_value <= alpha:
                return mini_value
            if mini_value<beta:
                beta = mini_value

        return mini_value


    def find_died_pieces(self,board, piece_type):
        died_pieces = []
        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == piece_type:
                    # The piece die if it has no liberty
                    if not self.find_liberty(board,i, j):
                        died_pieces.append((i,j))
        return died_pieces

    def remove_certain_pieces(self,board, positions):
        for piece in positions:
            board[piece[0]][piece[1]] = 0
        return board

    def remove_died_pieces(self,board, piece_type):
        died_pieces = self.find_died_pieces(board,piece_type)
        if not died_pieces: return board,[]
        board=self.remove_certain_pieces(board,died_pieces)
        return board,died_pieces

    def compare_board(self, board1, board2):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

    def valid_place_check(self,board, i, j, piece_type, test_check=False):

        # Check if the place is in the board range
        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False

        # Check if the place already has a piece
        if board[i][j] != 0:
            return False

        # Copy the board for testing
        test_board = copy.deepcopy(board)

        # Check if the place has liberty
        test_board[i][j] = piece_type
        if self.find_liberty(test_board,i, j):
            return True

        # If not, remove the died pieces of opponent and check again
        test_board,died_pieces = self.remove_died_pieces(test_board,3 - piece_type)
        if not self.find_liberty(test_board,i, j):
            return False

        # Check special case: repeat placement causing the repeat board state (KO rule)
        else:
            if died_pieces and self.compare_board(self.previous_board, test_board):
                return False
        return True


    def detect_neighbor(self,board, i, j):
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

    def detect_neighbor_ally(self,board, i, j):
        neighbors = self.detect_neighbor(board,i, j)  # Detect neighbors
        group_allies = []
        # Iterate through neighbors
        for piece in neighbors:
            # Add to allies list if having the same color
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies

    def ally_dfs(self,board, i, j):

        stack = [(i, j)]  # stack for DFS serach
        ally_members = []  # record allies positions during the search
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(board,piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

    def find_liberty(self,board, i, j):
        ally_members = self.ally_dfs(board,i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(board,member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    return True
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return False

if __name__ == '__main__':
    N = 5
    piece, previous_board, board = readInput(N)
    step_number = getStepNumber(previous_board, board)
    #print(step_number)
    my_player = MyPlayer(piece, previous_board, board)
    max_depth = 4
    flag=0
    '''
    if step_number < 2:
        flag=1
        if my_player.valid_place_check(my_player.current_game_state,2,2,my_player.side):
            writeOutput((2,2))
        if my_player.valid_place_check(my_player.current_game_state,1, 1, my_player.side):
            writeOutput((1,1))
        elif my_player.valid_place_check(my_player.current_game_state,3, 1, my_player.side):
            writeOutput((3,1))
        elif my_player.valid_place_check(my_player.current_game_state,1, 3, my_player.side):
            writeOutput((1,3))
        elif my_player.valid_place_check(my_player.current_game_state,3, 3, my_player.side):
            writeOutput((3,3))
    elif step_number == 2 and my_player.side == 1:
        if my_player.current_game_state[3][1]==2 or my_player.current_game_state[3][3]==2:
            flag=1
            writeOutput((3,2))
        elif my_player.current_game_state[1][1] == 2 or my_player.current_game_state[1][3] == 2:
            flag=1
            writeOutput((1,2))
    elif step_number==5 or step_number==6:
        moves=[(3,4),(4,4),(4,3),(3,2),(0,0),(0,4),(4,0)]
        for i in range(len(moves)):
            m=random.choice(moves)
            if my_player.valid_place_check(my_player.current_game_state,m[0],m[1],my_player.side):
                flag=1
                writeOutput(m)
    '''
    #if flag!=1:
    if step_number<4:
        branch = 25
    elif step_number < 18:
        branch = 20
    else:
        branch = 25

    maxi_move, maxScore = my_player.Max_Move(my_player.board, my_player.piece, -np.inf, np.inf, max_depth, 0, branch, None, False,step_number)
    if maxi_move is None or maxi_move=="end":
        writeOutput("PASS")
    else:
        writeOutput(maxi_move)
