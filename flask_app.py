from flask import Flask, render_template, request
from chess_engine import *
from minmaxchess import * 
import chess.pgn
import pandas as pd

app = Flask(__name__)
previousgames = pd.read_csv("mastergames.csv")

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    print(depth)
    print("Calculating...")
    engine = Engine(fen)
    move = engine.iterative_deepening(depth - 1)
    print("Move found!", move)
    print()
    return move

@app.route('/move/bot2/<int:depth>/<path:fen>/')
def get_bot2_move(depth, fen):
    
    previousmoves = request.args.get('pm')
    previousmoves = previousmoves.split(',')
    board = chess.Board()
    board.set_fen(fen)

    chessbot2 = ChessBot(depth,previousgames, previousmoves)
    move = chessbot2.get_best_move(board)
    return move.uci()


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester

@app.route('/test/botvsbot')
def test_bot():
    board = chess.Board()
    
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            chessbot2 = ChessBot(4,previousgames, list(board.move_stack))
            best_move = chessbot2.get_best_move(board)
            #evaluation, best_move = chessbot1.minimax(board, depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
            #print(type(best_move))
        else:
            engine = Engine(board.fen())
            move = engine.iterative_deepening(5 - 1)
            best_move = chess.Move.from_uci(move)
            #best_move = chessbot2.get_best_move(board)
            #evaluation, best_move = chessbot2.minimax(board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
        board.push(best_move)
        
    game = chess.pgn.Game()

    # set up the game header information
    game.headers["Event"] = "Example Game"
    game.headers["Site"] = "Somewhere"
    game.headers["Date"] = "2022.03.23"
    game.headers["Round"] = "1"
    game.headers["White"] = "Player 1"
    game.headers["Black"] = "Player 2"
    game.headers["Result"] = "1-0"

    # add the moves to the game object
    node = game.add_variation(board.move_stack[0])
    for move in board.move_stack[1:]:
        node = node.add_variation(move)

    # print the PGN string
    print(game)

    return "hello"



""" if __name__ == '__main__':
    app.run(debug=True) """