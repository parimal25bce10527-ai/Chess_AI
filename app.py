from flask import Flask, render_template, request, jsonify
import chess
import ai_logic          # python‑chess engine (standard)
import ai_logic_standard  # bulletchess engine

app = Flask(__name__)
board = chess.Board()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    move_uci = data.get('move')
    color = data.get('color')   # 'white' or 'black'
    engine_choice = data.get('engine', 'standard')  # 'standard' or 'bullet'

    if not move_uci or not color:
        return jsonify({'error': 'Missing move or color'}), 400

    try:
        move = chess.Move.from_uci(move_uci)
    except ValueError:
        return jsonify({'error': 'Invalid move format'}), 400

    # Check that it's the correct player's turn
    if (color == 'white' and board.turn != chess.WHITE) or \
       (color == 'black' and board.turn != chess.BLACK):
        return jsonify({'error': 'Not your turn'}), 400

    # Apply the move if legal
    if move in board.legal_moves:
        board.push(move)
    else:
        return jsonify({'error': 'Illegal move'}), 400

    response = {
        'fen': board.fen(),
        'game_over': board.is_game_over(),
        'suggested_move': None
    }

    # After white moves, compute a suggestion for black (if game not over)
    if color == 'white' and not board.is_game_over():
        try:
            if engine_choice == 'bullet':
                # bulletchess engine expects a FEN string
                suggestion = ai_logic_standard.get_best_move(board.fen())
            else:
                # python‑chess engine expects a board object
                suggestion = ai_logic.get_best_move(board)

            # suggestion is a chess.Move object for the standard engine,
            # and a UCI string for bulletchess. Convert to UCI if needed.
            if engine_choice == 'standard' and suggestion is not None:
                suggestion = suggestion.uci()
            response['suggested_move'] = suggestion
        except Exception as e:
            print(f"Engine error: {e}")   # log but don't crash
            response['suggested_move'] = None

    return jsonify(response)

@app.route('/reset', methods=['POST'])
def reset_game():
    board.reset()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False for production