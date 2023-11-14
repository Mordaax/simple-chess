import chess
import random
import pandas as pd
import numpy as np

df2 = pd.read_csv("games/mastergames.csv")
class ChessBot:
    def __init__(self, depth, previousgames, previousmoves):
        
        self.depth = depth
        self.previousgames = previousgames
        self.previousmoves = previousmoves
        self.openingDone = False
        self.maxOpeningMoves = 30
        self.peices = {
            chess.PAWN:100,
            chess.KNIGHT:300,
            chess.BISHOP:310,
            chess.ROOK:500, 
            chess.QUEEN:900,
            chess.KING:99999
        }
        self.square_table = {
            chess.PAWN: [
                0, 0, 0, 0, 0, 0, 0, 0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5, 5, 10, 25, 25, 10, 5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
                5, -5, -10, 0, 0, -10, -5, 5,
                5, 10, 10, -20, -20, 10, 10, 5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            chess.KNIGHT: [
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50,
            ],
            chess.BISHOP: [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20,
            ],
            chess.ROOK: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, 10, 10, 10, 10, 5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ],
            chess.QUEEN: [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -5, 0, 5, 5, 5, 5, 0, -5,
                0, 0, 5, 5, 5, 5, 0, -5,
                -10, 5, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            chess.KING: [
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20, 20, 0, 0, 0, 0, 20, 20,
                20, 30, 10, 0, 0, 10, 30, 20
            ]
        }
        

    def run_opening(self,board, previous_moves):
        if self.maxOpeningMoves == 1:
            self.openingDone == False
        self.maxOpeningMoves -=1

        #previous_moves = list(board.move_stack)
        movelist = []
        '''
        print(previous_moves)
        if len(previous_moves[0] !='':
            board_temp = chess.Board()
            for move_uci in previous_moves:
                
                san_move = board_temp.san(move_uci)
                board_temp.push(move_uci)
                
                movelist.append(san_move)
#        print(previous_moves)
        '''
        movelist = previous_moves
        df3 = self.previousgames.copy()       
        if movelist == []:
            move = random.choice(self.previousgames['Move_ply_1'].unique())
        else:
            

            for i in range(1,len(movelist)+1):
                df3 = df3.loc[df3['Move_ply_'+str(i)]==movelist[i-1]]
            movechoices = df3['Move_ply_'+str(len(movelist)+1)].unique()

            if len(movechoices) >0 and not (type(movechoices[0])== float):
                move = random.choice(movechoices)
                
            else:
                if board.turn == chess.WHITE:
                    evaluation, best_move = self.minimax(board, depth=self.depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
                else:
                    evaluation, best_move = self.minimax(board, depth=self.depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
                self.openingDone = True
                print("openingdone")
                return best_move

        return board.parse_san(move)

    def minimax(self, position, depth, alpha, beta, maximizing_player):
        if depth == 0 or position.is_game_over():
            return self.evaluate(position), None

        if maximizing_player:
            max_evaluation = float('-inf')
            best_move = None
            for move in position.legal_moves:
                position.push(move)
                evaluation, _ = self.minimax(position, depth - 1, alpha, beta, False)
                position.pop()
                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if alpha >= beta:
                    break
            return max_evaluation, best_move
        else:
            min_evaluation = float('inf')
            best_move = None
            for move in position.legal_moves:
                position.push(move)
                evaluation, _ = self.minimax(position, depth - 1, alpha, beta, True)
                position.pop()
                if evaluation < min_evaluation:
                    min_evaluation = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_evaluation, best_move

    def evaluate(self, position):
        if position.is_checkmate():
            if position.turn:
                return -100000
            else:
                return 100000
        if position.is_stalemate():
            return 0
        if position.is_insufficient_material():
            return 0
        # evaluation function based on material count

        material_count = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            material_count += self.peices[piece_type] * (len(position.pieces(piece_type, chess.WHITE)) - len(position.pieces(piece_type, chess.BLACK)))
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            
            peice_squares = [square for square in position.pieces(piece_type, chess.WHITE)]# get the current square name of the zzzwhite king
            for square_index in peice_squares:
                material_count += self.square_table[piece_type][63-square_index]

            peice_squares = [square for square in position.pieces(piece_type, chess.BLACK)]# get the current square name of the zzzwhite king
            for square_index in peice_squares:
                material_count -= self.square_table[piece_type][square_index]


        return material_count*(random.randint(105,110)/100)

    def get_best_move(self, board):
        if board.turn == chess.WHITE:
            if (self.openingDone):
                evaluation, best_move = self.minimax(board, depth=self.depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
            else:
                best_move = self.run_opening(board, self.previousmoves)
        else:
            if (self.openingDone):
                evaluation, best_move = self.minimax(board, depth=self.depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
            else:
                best_move = self.run_opening(board, self.previousmoves)
        return best_move



'''
moves=0
# example usage
board = chess.Board()

chessbot1 = ChessBot(4)
chessbot2 = ChessBot(4)

while not board.is_game_over():
    if board.turn == chess.WHITE:
        best_move = chessbot1.get_best_move(board)
        #evaluation, best_move = chessbot1.minimax(board, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
        #print(type(best_move))
    else:
        best_move = chessbot2.get_best_move(board)
        #evaluation, best_move = chessbot2.minimax(board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
    board.push(best_move)
    print(board)
    moves+=1
    print(moves)
print(board.result())
'''