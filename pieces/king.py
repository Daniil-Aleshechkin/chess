from pieces.piece import Piece

class King(Piece):
    def __init__(self,side,piece,pos,castle):
        move = None
        super().__init__(side,piece,pos,move)
        if castle == "1":
            self.castle = True
        else:
            self.castle = False
        
    def validMoves(self,board,**keyword_parameters):
        validMoves = []
        
        if "castle" in keyword_parameters:
            castle = False
        else:
            castle = True
        
        if self.castle == True and castle == True:
            validMoves.extend(self.validCastle(board,self,2))
            validMoves.extend(self.validCastle(board,self,-2))
            
        validMoves.extend(self.firstValue(self.validLine(board,self,1,0)))
        validMoves.extend(self.firstValue(self.validLine(board,self,-1,0)))
        validMoves.extend(self.firstValue(self.validLine(board,self,1,1)))
        validMoves.extend(self.firstValue(self.validLine(board,self,-1,1)))
         
        validMoves.extend(self.firstValue(self.validDiagonal(board,self,1,1)))
        validMoves.extend(self.firstValue(self.validDiagonal(board,self,-1,1)))
        validMoves.extend(self.firstValue(self.validDiagonal(board,self,1,-1)))
        validMoves.extend(self.firstValue(self.validDiagonal(board,self,-1,-1)))
        
        return validMoves
    
    def toString(self):
        return self.side+self.piece+Piece.convertBoolToString(self.castle)
    
    @staticmethod
    def firstValue(l):
        if l == []:
            return []
        else:
            return [l[0]]
    
    def update(self,pos):
        self.pos = pos
        self.castle = False
        