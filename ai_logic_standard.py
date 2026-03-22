import bulletchess
import bulletchess.utils  # for evaluate

def evaluate_board(board):
    """Return a score from White's perspective (positive = better for White)."""
    # Use bulletchess's built-in evaluation
    try:
        # evaluate returns a value in centipawns (positive = White advantage)
        return bulletchess.utils.evaluate(board)
    except AttributeError:
        # Fallback: simple material count
        # We'll compute manually using piece bitboards
        piece_values = {
            bulletchess.PAWN: 100,
            bulletchess.KNIGHT: 300,
            bulletchess.BISHOP: 300,
            bulletchess.ROOK: 500,
            bulletchess.QUEEN: 900,
            bulletchess.KING: 0
        }
        score = 0
        for piece_type, value in piece_values.items():
            white_count = (bulletchess.piece_bitboard(board, bulletchess.Piece(bulletchess.WHITE, piece_type)).count())
            black_count = (bulletchess.piece_bitboard(board, bulletchess.Piece(bulletchess.BLACK, piece_type)).count())
            score += (white_count - black_count) * value
        # Check for checkmate/stalemate
        if len(board.legal_moves()) == 0:
            # No legal moves – check if the side to move is in check
            turn = board.turn
            king_sq = (bulletchess.king_bitboard(board) & (board[turn])).to_squares()
            if king_sq:
                king_sq = king_sq[0]
                opponent = turn.opposite
                attacked = bulletchess.attack_mask(board, opponent)
                if king_sq in attacked:
                    # Checkmate – losing side loses
                    return -9999 if turn == bulletchess.WHITE else 9999
                else:
                    # Stalemate – draw
                    return 0
        return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or len(board.legal_moves()) == 0:
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves():
            board.apply(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.undo()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves():
            board.apply(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.undo()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(fen_string, depth=4):
    print(f"[bulletchess] Received FEN: {fen_string}")
    try:
        board = bulletchess.Board.from_fen(fen_string)
        print("[bulletchess] Board created successfully")
    except Exception as e:
        print(f"[bulletchess] Failed to create board: {e}")
        return None

    best_move = None
    best_eval = float('inf')
    move_count = 0

    legal_moves = board.legal_moves()
    print(f"[bulletchess] Found {len(legal_moves)} legal moves")

    for move in legal_moves:
        move_count += 1
        try:
            board.apply(move)
            # After black moves, White's turn (maximizing)
            board_eval = minimax(board, depth - 1, -float('inf'), float('inf'), True)
            print(f"[bulletchess] Move {move_count}/{len(legal_moves)}: {move.uci()} eval {board_eval}")
        except Exception as e:
            print(f"[bulletchess] Error processing move {move.uci()}: {e}")
        finally:
            board.undo()  # ensure undo is always called

        if board_eval < best_eval:
            best_eval = board_eval
            best_move = move

    if best_move is None:
        print("[bulletchess] No best move found")
        return None

    best_move_str = best_move.uci()
    print(f"[bulletchess] Best move: {best_move_str} with eval {best_eval}")
    return best_move_str