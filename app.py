"""
テトリスゲーム用 Flask Webサーバー
"""

from flask import Flask, render_template, jsonify
from game_logic import TetrisGame

app = Flask(__name__)
game = None

def init_game():
    """新しいゲームを初期化"""
    global game
    game = TetrisGame(10, 20)
    return game

@app.route('/')
def index():
    """メインゲームページを提供"""
    return render_template('index.html')

@app.route('/api/game/new', methods=['GET'])
def new_game():
    """新しいゲームを作成"""
    init_game()
    return get_game_state()

@app.route('/api/game/state', methods=['GET'])
def get_game_state():
    """現在のゲーム状態を取得"""
    if game is None:
        init_game()
    
    return jsonify({
        'board': game.get_board(),
        'piece': game.get_current_piece(),
        'piece_type': game.current_piece_type,
        'piece_x': game.current_piece_x,
        'piece_y': game.current_piece_y,
        'next_piece': game.get_next_piece(),
        'score': game.score,
        'level': game.level,
        'lines': game.lines_cleared,
        'game_over': False
    })

@app.route('/api/game/move/<direction>', methods=['POST'])
def move(direction):
    """指定された方向にピースを移動"""
    if game is None:
        init_game()
    
    if direction == 'left':
        game.move_piece_left()
    elif direction == 'right':
        game.move_piece_right()
    elif direction == 'down':
        game.move_piece_down()
    elif direction == 'rotate':
        game.rotate_piece()
    elif direction == 'drop':
        game.hard_drop()
    
    return get_game_state()

@app.route('/api/game/tick', methods=['POST'])
def tick():
    """ゲームを1ティック進める"""
    if game is None:
        init_game()
    
    game_over = False
    if not game.move_piece_down():
        if not game.spawn_next_piece():
            game_over = True
    
    return jsonify({
        'board': game.get_board(),
        'piece': game.get_current_piece(),
        'piece_type': game.current_piece_type,
        'piece_x': game.current_piece_x,
        'piece_y': game.current_piece_y,
        'next_piece': game.get_next_piece(),
        'score': game.score,
        'level': game.level,
        'lines': game.lines_cleared,
        'game_over': game_over
    })

if __name__ == '__main__':
    init_game()
    app.run(host='0.0.0.0', port=5000, debug=False)
