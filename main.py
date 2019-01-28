import pygame
from board import Chess_Board


win = pygame.display.set_mode((600,480))

pygame.display.set_caption("Chess")

board = [["BR1","Bk","BB","BQ","BK1","BB","Bk","BR1"],
         ["BP1","BP1","BP1","BP1","BP1","BP1","BP1","BP1"],
         ["","","","","","","",""],
         ["","","","","","","",""],
         ["","","","","","","",""],
         ["","","","","","","",""],
         ["WP1","WP1","WP1","WP1","WP1","WP1","WP1","WP1"],
         ["WR1","Wk","WB","WQ","WK1","WB","Wk","WR1"]]
turn = "W"

board = Chess_Board(board,turn,[board])
size = 60
dragPiece = None
movement = None

run = True
while run:
    pygame.time.delay(4)
    board.drawBoard(win,movement)
    
    #Draw draging piece
    if dragPiece != None:
        image = pygame.image.load(dragPiece.path)
        image.convert()
        mouse_X = pygame.mouse.get_pos()[0]-size//2
        mouse_Y = pygame.mouse.get_pos()[1]-size//2
        win.blit(image,(mouse_X,mouse_Y))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        #Drag a piece
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] < size*8 and mousePos[1] < size*8:
                y_Pos = board.flipPos(mousePos[1]//size,mousePos[0]//size)[0]
                x_Pos = board.flipPos(mousePos[1]//size,mousePos[0]//size)[1]
                
                print((y_Pos,x_Pos))
                piece = board.board[y_Pos][x_Pos]
                if piece != "":
                    if piece.side == board.turn: 
                        dragPiece = piece
                        movement = piece.move
                        board.deletePiece(mousePos[0]//size,mousePos[1]//size)   
                
            #Colour buttons...
            elif mousePos[1] <= 10:
                myColours = ["R","G","B","Y"]
                for x in range(0,size*2,size*2//4):
                    if mousePos[0] >= size*8+x and mousePos[0] < size*8+x+size*2//4:
                        board.colour = myColours[int(x//(size*2//4))]
                        break
                #board.printBoards()
            else:
                if mousePos[1] > size*8-16:
                    if mousePos[0] > size*8-16:
                        if len(board.boards) != 1:
                            oldStates = board.boards[:len(board.boards)-1]
                            newState = board.boards[-2]
                            boardColour = board.colour
                        
                            if board.turn == "W":
                                newTurn = "B"
                            else:
                                newTurn = "W"
                            
                            board = Chess_Board(newState,newTurn,oldStates)
                            board.colour = boardColour
                    
        #Release piece
        if event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            y_Pos = board.flipPos(mousePos[1]//size,mousePos[0]//size)[0]
            x_Pos = board.flipPos(mousePos[1]//size,mousePos[0]//size)[1]
            if dragPiece != None:
                if board.checkMove(dragPiece,(y_Pos,x_Pos),win) == False:
                    board.replacePiece(dragPiece,dragPiece.pos)
                else:
                    board.makeMove(dragPiece,(y_Pos,x_Pos))
                movement = None
            dragPiece = None
    pygame.display.update()
            

pygame.quit()