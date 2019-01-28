import os

#Class that handles basic piece functionality
class Piece:
    
    script_path = os.path.abspath(__file__)
    script_dir =  os.path.join(os.path.split(script_path)[0],r"Assets")
    
    #Paths to images
    names = ["BB","WB","BK","WK","Bk","Wk","BP","WP","BQ","WQ","BR","WR"]
    dirs = ["Chess_bdt60.png","Chess_blt60.png","Chess_kdt60.png","Chess_klt60.png","Chess_ndt60.png","Chess_nlt60.png","Chess_pdt60.png","Chess_plt60.png","Chess_qdt60.png","Chess_qlt60.png","Chess_rdt60.png","Chess_rlt60.png"]    
    chessdirs = {}
    
    count = 0
    for name in names:
        chessdirs[name] = os.path.join(script_dir,dirs[count])
        count += 1
    
    def __init__(self,side,piece,pos,move):
        self.side = side
        self.piece = piece[0]
        self.pos = pos
        self.path = Piece.chessdirs[side+piece[0]]
        self.move = move #Subclass which handles the special functions of pieces (jank maybe... It made sense in my head -.-)
    
        """These subclasses have two main methods:
            validMoves(): Outputs the possible moves that a piece can make
            update(): Updates the possition
            
            Addtionelly, some pieces have extra methods and data to perform speciel manuvers"""
    
    #Updates the piece (In theory I could have used a setter but whatever)
    def promote(self,piece,move):
        self.piece = piece
        self.path = Piece.chessdirs[self.side+piece[0]]
        self.move = move
    
    #DOutputs a single line of points from a position in the board. 
    #Stops once it finds a piece with the same side or reaches the end
    def validLine(self,board,piece,direction,axis):
        validMoves = []
        
        relPos = self.pos[axis]+direction
        if axis == 0: #Handles left and right
            while relPos >=0 and relPos <= 7:
                if board.getPiece((relPos,self.pos[1])) != "":
                    if board.getPiece((relPos,self.pos[1])).side == piece.side:
                        break
                    else:
                        validMoves.append((relPos,self.pos[1]))
                        break
                else:
                    validMoves.append((relPos,self.pos[1]))
                    relPos += direction
        else: #Handles up and down
            while relPos >=0 and relPos <= 7:
                if board.getPiece((self.pos[0],relPos)) != "":
                    if board.getPiece((self.pos[0],relPos)).side == piece.side:
                        break
                    else:
                        validMoves.append((self.pos[0],relPos))
                        break
                else:
                    validMoves.append((self.pos[0],relPos))
                    relPos += direction
        return validMoves
    
    #Outputs a single diagnol of points from a position in the board
    #Stops once it finds a piece with the same side or reaches the end 
    def validDiagonal(self,board,piece,direction1,direction2):
        validMoves = []
        
        relPos = [self.pos[0]+direction1,self.pos[1]+direction2]
        
        while relPos[0] >=0 and relPos[0] <= 7 and relPos[1] >= 0 and relPos[1] <= 7:
            if board.getPiece(relPos) != "":
                if board.getPiece(relPos).side == piece.side:
                    break
                else:
                    validMoves.append((relPos[0],relPos[1]))
                    break
            else:
                validMoves.append((relPos[0],relPos[1]))
                relPos[0] += direction1
                relPos[1] += direction2
        
        return validMoves
    
    #Outputs a single point on the board relative to a position
    #Doesn't output if the point is outside the board or occupied by a friendly piece
    def validKnight(self,board,piece,direction1,direction2):
        newPos = (self.pos[0]+direction1,self.pos[1]+direction2)
        
        if newPos[0] >=0 and newPos[0] <= 7 and newPos[1] >= 0 and newPos[1] <= 7:
            if board.getPiece(newPos):
                if board.getPiece(newPos).side == piece.side:
                    return []
                else:
                    return [newPos]
            else:
                return [newPos]
        else:
            return []
    
    #Outputs a point two squares away from a piece
    #Does not output if the position of the piece, the position if betweemn, or the postion are under attack or occupied by a piece
    def validCastle(self,board,piece,direction):
        newPos = (self.pos[0],self.pos[1]+direction)
        
        if newPos[0] >=0 and newPos[0] <= 7 and newPos[1] >= 0 and newPos[1] <= 7:
            direction = int(direction//2)
            castlePos = [piece.pos,(self.pos[0],self.pos[1]+direction),newPos] #Positions from the movemeent to the piece
            
            if direction < 0:
                castlePos.append((self.pos[0],self.pos[1]+direction*3))
            
            attacks = board.allAttacks(board,piece.side) #Find all the pieces that are under attack
            
            #Chech for occupation or attack
            count = 0
            for pos in castlePos:
                if attacks[pos[0]][pos[1]] == "A" and count != 3:
                    return []
                elif board.getPiece(pos) != "":
                    return []
                count += 1
            return [newPos]
        else:
            return []
    
    #Outputs a single point on the board relative to a single y transformation
    #Does not output if the postion is occupied by a piece
    def validPawnMove(self,board,direction):
        newPos = (self.pos[0]+direction,self.pos[1])
        
        if newPos[0] >=0 and newPos[0] <= 7 and newPos[1] >= 0 and newPos[1] <= 7:
            if board.getPiece(newPos) == "":
                return [newPos]
            else:
                return []
        else:
            return []
    
    #Outputs a single point on the board relative to a single a and y transformation
    #Only outputs if the possition is occupied by an enemy piece
    #UNLESS the position behind is occupied by a pawn which is vulnerable to enpassant
    def validPawnAttack(self,board,piece,direction1,direction2):
        newPos = (self.pos[0]+direction1,self.pos[1]+direction2)
       
        if newPos[0] >=0 and newPos[0] <= 7 and newPos[1] >= 0 and newPos[1] <= 7:
            if board.getPiece(newPos) == "":
                behindPiece = board.getPiece((newPos[0]-direction1,newPos[1]))
                
                if behindPiece != "":
                    if behindPiece.piece == "P":
                        if behindPiece.move.enpassant == True:
                            return [newPos]
                return []
            else:
                if board.getPiece(newPos).side == piece.side:
                    return []
                else:
                    return [newPos]
        else:
            return []
    
    #Set the special movement subclass
    def setMove(self,move):
        self.move = move
    
    @staticmethod
    def convertBoolToString(b):
        if b == True:
            return "1"
        else:
            return "0"