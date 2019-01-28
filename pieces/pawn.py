from pieces.piece import Piece

#Oooh boy.... Pawns are complicated....

class Pawn(Piece):
    def __init__(self,side,piece,pos,firstMove):
        move = None
        super().__init__(side,piece,pos,move)
        self.enpassant = False #Value to determine if its vulnerable to an enpassant
        
        if firstMove == "1":
            self.firstMove = True
        else:
            self.firstMove = False
    
    def validMoves(self,board):
        validMoves = []
        
        if self.side == "W":
            validMoves.extend(self.validPawnMove(board,-1))
            if self.firstMove == True and len(validMoves)!=0:
                validMoves.extend(self.validPawnMove(board,-2))
            
            validMoves.extend(self.validPawnAttack(board,self,-1,1))
            validMoves.extend(self.validPawnAttack(board,self,-1,-1))
        else:
            validMoves.extend(self.validPawnMove(board,1))
            if self.firstMove == True and len(validMoves)!=0:
                validMoves.extend(self.validPawnMove(board,2))
            
            validMoves.extend(self.validPawnAttack(board,self,1,1))
            validMoves.extend(self.validPawnAttack(board,self,1,-1))
        
        return validMoves
    
    #Method to allow allAttacks() to count the pawns manuvers
    def validAttack(self,board):
        validMoves = []
        
        if self.side == "W":
            validMoves.extend(self.grabValues(self.validDiagonal(board,self,-1,1),0))
            validMoves.extend(self.grabValues(self.validDiagonal(board,self,-1,-1),0))
        else:   
            validMoves.extend(self.grabValues(self.validDiagonal(board,self,1,1),0))
            validMoves.extend(self.grabValues(self.validDiagonal(board,self,1,-1),0))
        
        return validMoves
    
    @staticmethod
    def grabValues(l,amount):
        values = []
        for x in range(amount+1):
            try:
                value = l[x]
                values.append(value)
            except IndexError:
                pass
        return values
    
    def toString(self):
        return self.side+self.piece+Piece.convertBoolToString(self.firstMove)
    
    def update(self,pos):
        self.pos = pos
        
        #Update the firstmove and the enpassant vulerability
        if self.firstMove == True:    
            self.firstMove = False
            self.enpassant = True