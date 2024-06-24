# Chess_Engine
This project is an implementation of a Chess Engine that evaluates the given board position
and generates a line of the best moves up to a given depth.
The program efficiently explores the vast
tree of move possibilities using the minimax algorithm, further optimized by alpha-beta pruning.
It also includes a simple move ordering heuristic to prune maximum branches as early
as possible. The integration of an opening book as a pattern database further enhances
the engine's capabilities. The engine utilizes a simple piece table heuristic to evaluate the
value of leaf nodes

# Implementation Approach
## 1. Parsing the position
The standard for communicating a chess position to a
computer is the Forsyth Edward Notation or the FEN
string. This string provides all relevant information
required to recreate the game, such as
- The configuration of the board.
- The color of the side to move.
- Availability of castling rights.
- Possibility of en passant captures.
- The number of half-moves since the last pawn
move or capture.
Our Engine is built on the Python chess library. The
library has built-in functions to parse the FEN string
and construct a board object.

## 2. Evaluation
To search for good positions, it is necessary
to understand what makes a good position good. The
most simplistic way of describing a position’s strength
is to simply compare the total material value of each side. But
total piece value on its own does not give the complete idea
about a position. Hence, it is important to include the
position of the pieces in the evaluation as well. For this, we
use piece square tables, which alter the value of a piece
depending on which square it sits on. For example,
pawns should progress up the board, and knights should
be near the center of the board.


![image](https://github.com/An-Aeonic-Ant/Chess_Engine/assets/136352381/73e5daa9-10a0-4860-a95c-0d80d7e0111d)


## 3. Searching
Minimax is a search algorithm that finds the next optimal move by minimizing the potential loss in the worst-case scenario. 
The Chess game can be visualized as a search tree, where each node represents a board position and each branch represents a possible move. The minimax algorithm is a recursive method used to choose the optimal move for a player, assuming that the opponent is also playing optimally. Thus minimizing the max potential loss


Our engine uses alpha-beta pruning as an improvement
over the naive minimax algorithm — which does not
fare well against the exponential nature of chess. The
idea is simple: branches of the search tree can be eliminated when it is clear that another branch shows more
promise. This significantly reduces the number of positions required to be explored. By reducing the depth of
branches that will not bear fruit we can search deeper
down the better, more fruitful parts of the tree. The
speed of alpha-beta pruning can be further increased
by applying move ordering. By this, the more promising branches of the tree are searched first. This helps
in pruning off maximum branches as early as possible.
Move ordering cannot be 100% accurate, but it’s a powerful optimization. In our engine, we order the
exploration of moves by the following priority:
1. Checks.
2. Capturing a higher-value piece with a lower-value
piece.
3. Capturing a lower-value piece with a higher-value
piece
4. All other moves.

![image](https://github.com/An-Aeonic-Ant/Chess_Engine/assets/136352381/4631fdc4-1464-4bbf-9986-30446b3fe252)


## 4. Openings Database
One glaring limitation the engine faced was its inability
to look ahead far enough to navigate the tricky opening
phase of the game and reach “theoretically” good positions. To address this, we’ve integrated a text database
into our project, containing hundreds of opening board
positions in the FEN format and their “theoretically” optimal moves. Hence in the opening, we first
search the database for the current board position. If
a match is found, the engine immediately returns the
move associated with that position from the database.
However, if the position is not found in the database,
the engine proceeds with its Minimax search algorithm
to determine the best move. To avoid wasting unnecessary compute time, the engine does not search the text
database for future moves once it does not find the
current position. The intuition behind this is simple;
since it is an opening database, if the board position
did not exist in the database on move 5, it is very unlikely the position will exist on say, move 7

## 5. Handling Incomplete Evaluations
Despite all the mentioned optimizations implemented,
the engine could only search up to a depth of 4-half
moves in a reasonable time. However, there remained a risk of returning incomplete evaluations at such a shallow depth. The inherent volatility of chess positions meant that a seemingly favorable position at the end of the fourth half move could drastically change by the
fifth half move due to a captures or even a checkmate. To
handle this, upon reaching depth 0 (the base position
being depth 4), the engine searches for an extra 2 "negative" depths. For these negative depths however, the
engine only examines the forcing moves ie checks, and
captures. This modification handles the issue of incomplete evaluations by smartly finding a middle ground
by searching beyond 4 half-moves but faster than the
full 6 half-move search

## References
- “Python chess library,” https://pypi.org/project/chess/
- O. Healey, “Building my own chess engine,” https://healeycodes.com/building-my-own-chess-engine
- “Chess programming wiki,” https://www.chessprogramming.org/Main_Page.
- Sebastian Lague, "Coding Adventure: Chess", https://www.youtube.com/watch?v=U4ogK0MIzqk



