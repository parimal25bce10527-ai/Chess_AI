# Project Report – Chess AI with Minimax and Dual Engines

## 1. Problem Statement
Many chess learners benefit from AI suggestions but still want to make their own moves to internalize ideas. This project delivers an interactive chess interface where the user plays as White, and an AI (based on minimax with alpha-beta pruning) suggests the best Black move after each White move. Two engines are offered: a standard python‑chess engine and a faster bulletchess engine.

## 2. Why This Matters
- Applies core AI concepts: search algorithms (minimax, alpha‑beta pruning) and evaluation functions.
- Demonstrates real‑world web integration: Flask backend, JavaScript frontend.
- Addresses a genuine user need: learning through AI suggestions while retaining manual control.

## 3. Approach and Solution
- **Search algorithm**: minimax with alpha‑beta pruning (depth 3 for standard, depth 4 for bullet).
- **Evaluation**: material balance plus checkmate/stalemate detection.
- **Frontend**: chessboard.js for drag‑and‑drop, chess.js for move validation.
- **Backend**: Flask receives moves, runs the chosen AI, returns suggested move in JSON.
- **User experience**: after a White move, a loading bar appears; a pop‑up shows the AI’s suggestion; the user then manually moves the Black piece.

## 4. Key Decisions
- **Why minimax?** It’s the standard for deterministic two‑player games.
- **Why two engines?** To compare performance and demonstrate flexibility.
- **Why manual Black moves?** To keep the user actively involved – the AI advises, but the player executes.

## 5. Implementation Details
- `app.py`: Flask routes, board state management, engine router.
- `ai_logic.py`: python‑chess minimax implementation.
- `ai_logic_standard.py`: bulletchess minimax implementation.
- `templates/index.html`: chessboard, JavaScript event handlers, loading bar, pop‑up.

## 6. Challenges and Solutions
- **Bulletchess API**: had to adjust to use `Board.from_fen()` and `legal_moves()`, plus proper undo after exceptions.
- **State consistency**: ensured board updates correctly via server‑returned FEN.
- **Loading bar**: added CSS progress bar that shows only during AI computation.

## 7. What I Learned
- Practical application of minimax with alpha‑beta pruning.
- Integrating two different chess libraries (python‑chess and bulletchess).
- Building a full‑stack web application with Flask and JavaScript.

## 8. Conclusion
The project successfully meets the BYOP criteria: a real‑world problem, meaningful AI implementation, and a polished interactive tool. It demonstrates core course concepts in a creative and usable way.

## 9. References
- bulletchess documentation: https://bulletchess.info
- python‑chess: https://python-chess.readthedocs.io
- chessboard.js: https://chessboardjs.com
- Flask: https://flask.palletsprojects.com
