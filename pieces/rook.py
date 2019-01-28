from pieces.piece import Piece

class Rook(Piece):
    
    def __init__(self,side,piece,pos,castle):
        move = None
        super().__init__(side,piece,pos,move)
        
        if castle == 0:
            self.castle = False
        else:
            self.castle = True
            
    
    def validMoves(self,board):
        validMoves = []
        
        validMoves.extend(self.validLine(board,self,1,0))
        validMoves.extend(self.validLine(board,self,-1,0))
        validMoves.extend(self.validLine(board,self,1,1))
        validMoves.extend(self.validLine(board,self,-1,1))
            
        return validMoves
    
    def toString(self):
        return self.side+self.piece+Piece.convertBoolToString(self.castle)
    
    def update(self,pos):
        self.pos = pos
        self.castle = False