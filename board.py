import pygame
import copy
import tkinter as tk
import os
from tkinter import messagebox as tkMessageBox
from pieces.piece import Piece
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.king import King

#Class which handles all the functionality of the board
class Chess_Board:
    #pos
    colours = {"R":((179, 0, 0),(255, 102, 0),(255,50,50)),"G":((0, 102, 34),(73, 193, 87),(0,255,0)),"B":((0, 0, 255),(51, 153, 255),(0,235,255)),"Y":((153, 153, 0),(255, 255, 0),(255, 255, 100))}#(201,209,0)
    
    rel_path = os.path.abspath(__file__)
    reverseDir = r"pieces\Assets\icons8-return-16.png"
    reversePath = os.path.join(os.path.split(rel_path)[0],reverseDir)
    
    def __init__(self,board,turn,boards):
        self.turn = turn
        
        objBoard = []
        kings = []
        
        #Define a board filled with piece objects
        y_Pos = 0
        for y in board:
            x_ObjBoard = []
            
            x_Pos = 0
            for x in y:    
                if x != "":
                    piece = Piece(x[0],x[1],(y_Pos,x_Pos),None) #Why did I define it as (y,x)? I have no idea... But I regret doing so... deeply....
                    x_ObjBoard.append(piece)
                    if x[1] == "R":
                        movement = Rook(x[0],x[1],(y_Pos,x_Pos),x[2])
                    elif x[1] == "B":
                        movement = Bishop(x[0],x[1],(y_Pos,x_Pos))
                    elif x[1] == "Q":
                        movement = Queen(x[0],x[1],(y_Pos,x_Pos))
                    elif x[1] == "k":
                        movement = Knight(x[0],x[1],(y_Pos,x_Pos))
                    elif x[1] == "P":
                        movement = Pawn(x[0],x[1],(y_Pos,x_Pos),x[2])
                    elif x[1] == "K":
                        movement = King(x[0],x[1],(y_Pos,x_Pos),x[2])
                        kings.append(piece)
                    piece.setMove(movement) #Append the unique movement code to the piece object
                        
                else:
                    x_ObjBoard.append("")
                x_Pos += 1
            objBoard.append(x_ObjBoard)
            y_Pos += 1
        self.promote = [False,False] #If a pawn is promoting (White,Black)
        self.colour = "R"
        self.boards = boards
        self.board = objBoard
        self.kings = kings #King objects stored for checking checks
    
    def flipPos(self,posY,posX):
        if self.turn=="B":
            return (7-posY,7-posX)
        else:
            return (posY,posX)
        
    #Strictly for debug. Prints the game history
    def printBoards(self):
        for board in self.boards:
            for y in board:
                for x in y:
                    if x == "":
                        print("00",end=" ")
                    else:
                        print(x[:2],end=" ")
                print()
            print("=================")
    
    #Simple function to remove a piece for the board
    def deletePiece(self,x_Pos,y_Pos):
        y_FPos = self.flipPos(y_Pos,x_Pos)[0]
        x_FPos = self.flipPos(y_Pos,x_Pos)[1]
        self.board[y_FPos][x_FPos] = ""
    
    #Returns a 2D array of the board in strings
    def toBoardList(self):
        stringBoard = []
        
        for y in self.board:
            yList = []
            for x in y:
                if x == "":
                    yList.append("")
                else:
                    yList.append(x.move.toString())
            stringBoard.append(yList)
        
        return stringBoard
   
    #Give the opposite colour
    @staticmethod
    def switchColour(colour):
        if colour == "W":
            return "B"
        else:
            return "W"
    
    #Thx Palmarin
    def setColour(self,x1,y1):
        
        if (x1 + y1) % 2 == 0:
            return Chess_Board.colours[self.colour][1]
        else:
            return Chess_Board.colours[self.colour][0]
    
    #Convert the string its colour
    @staticmethod
    def getColour(colour):
        colours = {"W":(255, 255, 255),"B":(0,0,0)}
        return colours[colour]
    
    #Get the individual piece (useful to save some space)
    def getPiece(self,pos):
        return self.board[pos[0]][pos[1]]
    
    #Draw the board
    def drawBoard(self,win,movement):
        
        if movement != None:
            moves = movement.validMoves(self)
            validMoves = []
            for move in moves:
                if self.checkCheck(movement,move) == True:
                    if self.checkCastle(movement,move,False) == (True,True,True) or self.checkCastle(movement,move,False) == (True,False,False) or self.checkCastle(movement,move,False) == (False,False,False):
                        validMoves.append(move)
        else:
            validMoves = []
        
        size = 60
        y_Pos = 0
        for y in range(8):
            x_Pos = 0
            for x in range(8):
                y_FPos = self.flipPos(y_Pos,x_Pos)[0]
                x_FPos = self.flipPos(y_Pos,x_Pos)[1]
                
                if (y_Pos,x_Pos) in validMoves:
                    pygame.draw.rect(win, self.colours[self.colour][2], (x_FPos*size,(y_FPos)*size,size,size))
                else:
                    pygame.draw.rect(win, self.setColour(x_FPos,y_FPos), (x_FPos*size,(y_FPos)*size,size,size))
    
                piece = self.board[y_Pos][x_Pos]
                if piece != "":
                    image = pygame.image.load(piece.path)
                    image.convert()
                    win.blit(image,(x_FPos*size,(y_FPos)*size))
                x_Pos += 1  
            y_Pos += 1
        
        #Draw the promotion GUI
        pygame.draw.rect(win,self.getColour(self.turn),(size*8,0,size*2,size*8)) #Turn indicator
        if self.promote[0] == True or self.promote[1] == True:
            
            #Index the paths
            if self.promote[0] == True:
                options = ["Wk","WB","WR","WQ"]
            else:
                options = ["Bk","BB","BR","BQ"]
            
            #Draw the options
            count = 0
            for piece in options:
                pygame.draw.circle(win,self.getColour(self.switchColour(self.turn)),(size*9,size//2+count+size//2+5),size*5//8) #Draw the opposite colour for readability
                image = pygame.image.load(Piece.chessdirs[piece])
                image.convert()
                win.blit(image,(size*8+size//2,size//2+count+5))
                count += size*2
        
        myColours = ["R","G","B","Y"]
        
        #Draw the reverse icon
        reverseImage = pygame.image.load(self.reversePath)
        reverseImage.convert()
        win.blit(reverseImage,(size*10-16,size*8-16))
        
        #Draw the colour buttons
        for x in range(0,size*2,size*2//4):
            pygame.draw.rect(win, Chess_Board.colours[myColours[int(x//(size*2//4))]][1], (size*8+x,0,size*2//4,10))
    
    #Change turn
    def swapTurn(self):
        if self.turn == "W":
            self.turn = "B"
        else:
            self.turn = "W"
        self.boards.append(self.toBoardList())
        #Update Enpassant vulnerability
        for y in self.board:
            for x in y:
                if x != "":
                    if x.piece == "P":
                        if x.side == self.turn:
                            x.move.enpassant = False
    
    #Move a piece (with all the checks for special moves)
    def checkMove(self,startPiece,pos,win):
        if pos in startPiece.move.validMoves(self):
            if self.checkCheck(startPiece,pos) == True: #Check if king in Check
                castleCheck = self.checkCastle(startPiece,pos,True) #Check for castling nonsense
                if castleCheck[0] == True:
                    if castleCheck[1] == True:
                        if castleCheck[2] == True:
                            return True
                        else:
                            return False
                    else:
                        return True
                else:
                    self.checkPawn(startPiece,pos,win) #Check for pawn nonsence
                    return True
        return False
    
    #Check if the king is in check after a move
    def checkCheck(self,startPiece,pos):
        theoryBoard = copy.deepcopy(self) #Copy of board to decude if the king is attacked
        theoryBoard.board[pos[0]][pos[1]] = startPiece
        
        #Finds the king
        if startPiece.piece == "K":
            endPiece = copy.deepcopy(startPiece)
            endPiece.pos = pos
            king = [endPiece]
        else:
            king = [x for x in self.kings if x.side == self.turn]
        
        attacks = self.allAttacks(theoryBoard,startPiece.side)
        
        #Checks for ckeck
        if attacks[king[0].pos[0]][king[0].pos[1]] == "A":
            return False
        else:
            return True
    
    #Check for castles
    #Outputs a tuple: (If the piece is a King, If the piece is castling, If the piece's castle is valid)
    def checkCastle(self,startPiece,pos,rookMovement):
        if startPiece.side == "W":
            y_pos = 7
        else:
            y_pos = 0
        if startPiece.piece == "K":
            if startPiece.pos == (pos[0],pos[1]-2):
                rook = self.getPiece((y_pos,7))
                
                if rook != "":
                    if rook.piece == "R":
                        if rook.move.castle == True:
                            if rookMovement == True:
                                self.deletePiece(7,y_pos)
                                self.makeMove(rook,(y_pos,5),move = False)
                            return (True,True,True)
                        
                return (True,True,False)
                        
            elif startPiece.pos == (pos[0],pos[1]+2):
                rook = self.getPiece((y_pos,0))
                
                if rook != "":
                    if rook.piece == "R":
                        if rook.move.castle == True:
                            if rookMovement == True:
                                self.deletePiece(0,y_pos)
                                self.makeMove(rook,(y_pos,3),move = False)
                            return (True,True,True)
                
                return (True,True,False)
            else:
                return (True,False,False)
        else:
            return (False,False,False)
    
    #Check if the move is one of the special pawn moves and exicutes accordingly
    def checkPawn(self,startPiece,pos,win):
        size = 60
        
        #Move objects of the 
        promotions = [Knight(startPiece.side,"k",pos),Bishop(startPiece.side,"B",pos),Rook(startPiece.side,"R",pos,"0"),Queen(startPiece.side,"Q",pos)]
        
        #Values which alternate based on the side
        if startPiece.side == "W":
            end = 0
            side = 0
            direction = -1
        else:
            end = 7
            side = 1
            direction = 1
        
        if startPiece.piece == "P":
            if pos[0] == end:
                
                #Promotion handler
                self.promote[side] = True
                self.makeMove(startPiece,pos,move = False)
                
                #Running the options after a promotion (jank I know)
                run = True
                while run == True:
                    pygame.time.delay(10)
                    
                    self.drawBoard(win,None)
                    pygame.display.update()
                    
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mousePos = pygame.mouse.get_pos()
                            if mousePos[0] >= size*8+size//2 or mousePos[0] <= size*10-size//2:
                                for seperate in range(0,size*8,size*2):
                                    if mousePos[1] >= size//2+seperate+5 and mousePos[1] < size//2+seperate+size+5:
                                        promote = promotions[seperate//(size*2)]
                                        startPiece.promote(promote.piece,promote)
                                        run = False
                        
                        #Prevent the user from quitting a promote because I coded jank
                        if event.type == pygame.QUIT:
                            root = tk.Tk()
                            root.withdraw()
                            tkMessageBox.showinfo("WARNING", "FINISH YOUR PROMOTE! >.<")
                            root.destroy
                            
                self.promote[side] = False
            else:
                #Enpassant exicution
                behindPiece = self.getPiece((pos[0]-direction,pos[1]))
                
                if behindPiece != "":
                    if behindPiece.piece == "P":
                        if behindPiece.move.enpassant == True:
                            self.deletePiece(behindPiece.pos[1],behindPiece.pos[0])
        
    
    #Find all squares which the other side is attacking
    @staticmethod
    def allAttacks(board,side):
        attacks = [[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "],[" "," "," "," "," "," "," "," "]]
        
        for y in board.board:
            for x in y:
                if x != "":
                    if x.side != side:
                        
                        #Finds all the valid attacks
                        if x.piece == "P":
                            validMoves = x.move.validAttack(board) #To count the pawns attacks rather than its motion
                        elif x.piece == "K":
                            validMoves = x.move.validMoves(board,castle = False) #To prevent recursion hell
                        else:
                            validMoves = x.move.validMoves(board)
                        
                        #Converts the valid attacks into a matrix
                        for validPos in validMoves:
                            attacks[validPos[0]][validPos[1]] = "A"
        
        return attacks
                
    #Hard move that updates all info
    def makeMove(self,startPiece,pos,**keyword_parameters):
        self.replacePiece(startPiece,pos)
        startPiece.pos = pos
        startPiece.move.update(pos)
        if "move" in keyword_parameters:
            pass
        else:
            self.swapTurn()
           
    #Soft move that only updates board position
    def replacePiece(self,startPiece,pos):
        self.board[pos[0]][pos[1]] = startPiece
        startPiece.pos = pos