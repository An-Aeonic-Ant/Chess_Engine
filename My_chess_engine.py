import chess
import heapq

positions=0

#Define piece-table

pawnEvalWhite = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]
pawnEvalBlack = list(reversed(pawnEvalWhite))

knightEval = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishopEvalWhite = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishopEvalBlack = list(reversed(bishopEvalWhite))

rookEvalWhite = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
rookEvalBlack = list(reversed(rookEvalWhite))

queenEval = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

kingEvalWhite = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]
kingEvalBlack = list(reversed(kingEvalWhite))

kingEvalEndGameWhite = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]
kingEvalEndGameBlack = list(reversed(kingEvalEndGameWhite))

piece_value = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

piece_table={
    chess.PAWN: [pawnEvalWhite,pawnEvalBlack],
    chess.ROOK: [rookEvalWhite,rookEvalBlack],
    chess.KNIGHT: [knightEval,knightEval],
    chess.BISHOP: [bishopEvalWhite,bishopEvalBlack],
    chess.QUEEN: [queenEval,queenEval],
    chess.KING: [kingEvalWhite,kingEvalBlack,kingEvalEndGameWhite,kingEvalEndGameBlack]
}

def pieceeval(piece,square,endgame=False):
    index=0
    multiplier=1
    value=piece_value[piece.piece_type]
    if piece.color==chess.BLACK:
        index=1
        multiplier=-1
    if piece.piece_type==chess.KING and endgame:
        index+=2
    value+=piece_table[piece.piece_type][index][square]
    return(value*multiplier)

def checkendgame(board):
    queens = 0
    minors = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.QUEEN:
            queens += 1
        if piece and (
            piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT
        ):
            minors += 1

    if queens == 0 or (queens == 2 and minors <= 1):
        return True
    return False

def boardeval(board):
    global positions
    positions+=1
    total=0
    endgame=checkendgame(board)
    for square in chess.SQUARES:
        piece=board.piece_at(square)
        if piece:
            total+=pieceeval(piece,square,endgame)
    return total

def minimax(board, depth,alpha=-float("inf"),beta=float("inf"),txt=False):
    bestline=()
    if txt==True:
        i=0
        while i<len(lines):
            if lines[i].strip() in board.fen():
                move=lines[i+1].strip()
                return "book",(move,)
            i+=2

    if depth==-2:
        return boardeval(board),()
    
    if depth>0:
        ordered_moves=order_moves(board)
    else:
        stopeval=boardeval(board)
        ordered_moves=order_moves(board,True)
        if not ordered_moves:
            return stopeval,()
        
    if board.turn == chess.WHITE:
        while ordered_moves:
            move=heapq.heappop(ordered_moves)[2]
            board.push(move)
            if board.is_checkmate():
                cureval=float("inf")
                line=("mate",)
            elif board.is_stalemate():
                cureval=0
                line=("draw",)
            else:
                cureval,line=minimax(board,depth-1,alpha,beta)
            board.pop()
            if cureval>alpha or (cureval==-float("inf") and alpha==-float("inf")):
                alpha=cureval
                bestline=(move,)+line
                if alpha >=beta:
                    break
        if depth<=0 and stopeval>=alpha:
            return stopeval,()
        return alpha,bestline
    else:
        while ordered_moves:
            move=heapq.heappop(ordered_moves)[2]
            board.push(move)
            if board.is_checkmate():
                cureval=-float("inf")
                line=("mate",)
            elif board.is_stalemate():
                cureval=0
                line=("draw",)
            else:
                cureval,line=minimax(board,depth-1,alpha,beta)      
            board.pop()
            if cureval<beta or (cureval==float("inf") and beta==float("inf")):
                beta=cureval
                bestline=(move,)+line
                if alpha >=beta:
                    break
        if depth<=0 and stopeval<=beta:
            return stopeval,()
        return beta,bestline
    


def order_moves(board,ignore=False):
    ordered=[]
    counter=0 #we need this as second element in tuple so that the third element which is a move object need not be compared
    for i in board.legal_moves:
        priority=float('inf')
        captured=board.piece_at(i.to_square)
        from_piece=board.piece_at(i.from_square)
        if captured:
            priority=(pieceeval(from_piece,i.from_square)+pieceeval(captured,i.to_square))
            if board.turn != chess.WHITE:
                priority*=-1
        board.push(i)
        if board.is_check():
            priority=-float("inf")
        board.pop()
        if ignore and (priority==float('inf') or priority==-float("inf")):
            continue
        heapq.heappush(ordered,(priority,counter,i,))
        counter+=1
    return ordered
        

board=chess.Board()
with open(r"C:\Users\91937\Desktop\my_openings.txt", 'r') as file:
    lines = file.readlines()

print(board)

print(minimax(board,4,txt=True))
print("Evaluated positions:", positions)

    