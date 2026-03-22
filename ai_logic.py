import chess

# Basic piece values for the Evaluation Function
PIECE_VALUES = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 9000
}

def evaluate_board(board):
    
    # Scores the board. Positive means White is winning, negative means Black is winning.
    
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    evaluation = 0
    for piece_type in PIECE_VALUES:
        evaluation += len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
        evaluation -= len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]
    
    return evaluation

def minimax(board, depth, alpha, beta, maximizing_player):
    
    # The core Search Algorithm with Alpha-Beta Pruning.
    
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break # Prune the tree
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break # Prune the tree
        return min_eval

def get_best_move(board, depth=3):
    
    #Finds the best move for Black (minimizing player).
    
    best_move = None
    best_eval = float('inf')
    
    for move in board.legal_moves:
        board.push(move)
        # White's turn next, so they are the maximizing player
        board_eval = minimax(board, depth - 1, -float('inf'), float('inf'), True)
        board.pop()
        
        if board_eval < best_eval:
            best_eval = board_eval
            best_move = move
            
    return best_move