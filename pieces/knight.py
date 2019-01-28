from pieces.piece import Piece

class Knight(Piece):
    def __init__(self,side,piece,pos):
        move = None
        super().__init__(side,piece,pos,move)
    
    def validMoves(self,board):
        validMoves = []
        
        validMoves.extend(self.validKnight(board,self,2,1))
        validMoves.extend(self.validKnight(board,self,2,-1))
        validMoves.extend(self.validKnight(board,self,-2,1))
        validMoves.extend(self.validKnight(board,self,-2,-1))
        validMoves.extend(self.validKnight(board,self,1,2))
        validMoves.extend(self.validKnight(board,self,1,-2))
        validMoves.extend(self.validKnight(board,self,-1,2))
        validMoves.extend(self.validKnight(board,self,-1,-2))
        
        return validMoves
    
    def toString(self):
        return self.side+self.piece
    
    def update(self,pos):
        self.pos = pos
        