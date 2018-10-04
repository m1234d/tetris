

    from tkinter import *
    import random

    #initialize the data which will be used to draw on the screen
    def init(data):
        #load data as appropriate
        data['helpMenu'] = False
        data['timePassed'] = 0
        data['boardWidth'] = 12
        data['boardLength'] = 15
        data['blockSize'] = 30
        data['player'] = [[0,0], [0,0], [0,0], [0,0]]
        data['color'] = 'blue'
        data['score'] = 0
        data["x"] = data['blockSize']//2
        data["y"] = data['blockSize']//2
        data['speed'] = data['blockSize']
        data['xSpeed'] = 0
        data['ySpeed'] = 0
        data['width'] = data['boardWidth'] * data['blockSize']
        data['height'] = data['boardLength'] * data['blockSize']
        data['gameBoard'] = [] 
        data['onMenu'] = True 
        data['startup'] = True
        for i in range(data['boardLength']):
            tempList = []
            for j in range(data['boardWidth']):
                tempList.append('white')
            data['gameBoard'].append(tempList)
        generatePlayer(data)
        resetBoard(data)
        
    #these are the controllers
    #they do not draw, they only modify data
    def mousePressed(event, data):
        #use event.x and event.y
        pass

    def keyPressed(event, data):
        #use event.char and event.keysym
        char = event.char
        if char == 'd':
            data['xSpeed'] = 1
        elif char == 'a':
            data['xSpeed'] = -1
        elif char == 'j':
            rotatePlayer(data)
        elif char == 'k':
            rotateCounter(data)
        elif char == 'p':
            data['onMenu'] = not data['onMenu']
            data['startup'] = False
            data['helpMenu'] = False
        elif char == 'h':
            data['helpMenu'] = not data['helpMenu']
        elif char == ' ':
            dropPlayer(data)
            
        movePlayer(data['xSpeed'], data['ySpeed'], data)

    def keyReleased(event, data):
        char = event.char
        if char == 'w':      
            data['ySpeed'] = 0
        elif char == 's':
            data['ySpeed'] = 0
        elif char == 'd':
            data['xSpeed'] = 0
        elif char == 'a':
            data['xSpeed'] = 0


    #main loop
    def timerFired(data):
        data['timePassed'] += 1
        if data['onMenu']:
            return
        #printBoard(data)
        value = movePlayer(0, 1, data)
        if value == False:
            endRound(data)
        elif value == "Game Over":
            print("Game Over.")
            generatePlayer(data)
            resetBoard(data)
            data['startup'] = True
            data['onMenu'] = True
            
            
    def endRound(data):
        generatePlayer(data)
        calculateScore(data)

    def dropPlayer(data):
        while True:
            for i in range(len(data['player'])):
                data['player'][i][1] += 1
            if outOfBounds(data) or hitDetected(data):
                for i in range(len(data['player'])):
                    data['player'][i][1] -= 1
                return

    def calculateScore(data):
        for i in range(len(data['gameBoard'])):
            isFull = True
            for j in range(1, len(data['gameBoard'][i]) - 1):
                if data['gameBoard'][i][j] == "white":
                    isFull = False
                    break
            if isFull:
                addPoints(10, data)
                for j in range(len(data['gameBoard'][i])):
                    data['gameBoard'][i][j] = 'white'
                for i in range(i, 0, -1):
                    for j in range(len(data['gameBoard'][i])):
                        data['gameBoard'][i][j] = data['gameBoard'][i-1][j]
                calculateScore(data)
                return
                
    def rotateCounter(data):
        originX = data['player'][2][0]
        originY = data['player'][2][1]
        for i in range(len(data['player'])):
            x = data['player'][i][0]
            y = data['player'][i][1]
            tempX = x - originX
            tempY = y - originY
            
            data['player'][i][0] = -tempY + originX
            data['player'][i][1] = tempX + originY
        if hitDetected(data) or outOfBounds(data):
            for i in range(len(data['player'])):
                x = data['player'][i][0]
                y = data['player'][i][1]
                tempX = x - originX
                tempY = y - originY
                
                data['player'][i][0] = tempY + originX
                data['player'][i][1] = -tempX + originY

    def rotatePlayer(data):
        originX = data['player'][2][0]
        originY = data['player'][2][1]
        for i in range(len(data['player'])):
            x = data['player'][i][0]
            y = data['player'][i][1]
            tempX = x - originX
            tempY = y - originY
            
            data['player'][i][0] = tempY + originX
            data['player'][i][1] = -tempX + originY
        if hitDetected(data) or outOfBounds(data):
            for i in range(len(data['player'])):
                x = data['player'][i][0]
                y = data['player'][i][1]
                tempX = x - originX
                tempY = y - originY
                
                data['player'][i][0] = -tempY + originX
                data['player'][i][1] = tempX + originY
    def addPoints(amount, data):
        data['score'] += 10
            
    def movePlayer(x, y, data):
        for i in range(len(data['player'])):
            data['player'][i][0] += x
            data['player'][i][1] += y

        if hitDetected(data):
            for i in range(len(data['player'])):
                data['player'][i][0] -= x
                data['player'][i][1] -= y
                if data['player'][i][1] == 1:
                    return "Game Over"
            return False
        elif outOfBounds(data):
            for i in range(len(data['player'])):
                data['player'][i][0] -= x
                data['player'][i][1] -= y
        return True
        
    def outOfBounds(data):
        for i in range(len(data['player'])):
            x = data['player'][i][0]
            y = data['player'][i][1]
            if x < 1 or y < 0 or x >= data['boardWidth'] - 1:
                return True
        return False
        
    def hitDetected(data):
        for i in range(len(data['player'])):
            if data['player'][i][1] >= data['boardLength']:
                return True
            for g in range(len(data['gameBoard'])):
                for h in range(len(data['gameBoard'][g])):
                    if data['gameBoard'][g][h] != 'white':
                        if g == data['player'][i][1] and h == data['player'][i][0]:
                            return True
        pass #determine if player is intersecting a gameBoard object
        
    def getLocation(data):
        return data['player']
        
    def generatePlayer(data):
        addToBoard(data)
        data['color'] = generateColor()
        x1,x2,x3,x4 = 0,0,0,0
        y1,y2,y3,y4 = 0,0,0,0
        loc = random.randint(1, data['boardWidth']-6)
        if data['color'] == 'cyan':
            x1, x2, x3, x4 = 1,2,3,4
            y1, y2, y3, y4 = 1,1,1,1
        elif data['color'] == 'blue':
            x1, x2, x3, x4 = 1,1,2,3
            y1, y2, y3, y4 = 0,1,1,1
        elif data['color'] == 'orange':
            x1, x2, x3, x4 = 1,2,3,3
            y1, y2, y3, y4 = 1,1,1,0
        elif data['color'] == 'yellow':
            x1, x2, x3, x4 = 1,2,1,2
            y1, y2, y3, y4 = 0,0,1,1
        elif data['color'] == 'green':
            x1, x2, x3, x4 = 1,2,2,3
            y1, y2, y3, y4 = 1,1,0,0
        elif data['color'] == 'purple':
            x1, x2, x3, x4 = 1,2,2,3
            y1, y2, y3, y4 = 1,1,0,1
        elif data['color'] == 'red':
            x1, x2, x3, x4 = 1,2,2,3
            y1, y2, y3, y4 = 0,0,1,1
        x1 += loc
        x2 += loc
        x3 += loc
        x4 += loc
        data['player'][0] = [x1, y1]
        data['player'][1] = [x2, y2]
        data['player'][2] = [x3, y3]
        data['player'][3] = [x4, y4]


    def generateColor():
        colors = ['cyan','blue', 'orange', 'yellow', 'green', 'purple', 'red']
        return colors[random.randint(0, len(colors)-1)]
        
    def addToBoard(data):
        for i, j in data['player']:
            boardX = i
            boardY = j
            data['gameBoard'][int(boardY)][int(boardX)] = data['color']
        
    def resetBoard(data):
        data['gameBoard'] = []
        for i in range(data['boardLength']):
            tempList = []
            for j in range(data['boardWidth']):
                tempList.append('white')
            data['gameBoard'].append(tempList)

    def printBoard(data):
        for i in range(len(data['gameBoard'])):
            for j in range(len(data['gameBoard'][0])):
                print(data['gameBoard'][i][j][0], end='')
            print()
        print()
        
    #this is the view
    #data is not modified, it only draws on the canvas
    def redrawAll(canvas, data):
        if data['onMenu']:
            drawMenu(canvas, data)
            return
        #draw in canvas
        drawBoard(canvas, data)
        drawTetromino(canvas, data)
        drawScore(canvas, data)
        
    def drawMenu(canvas, data):
        if data['helpMenu']:
            canvas.create_text(data['boardWidth']*data['blockSize']/2 + 70, 150, font=("Lucida Console", 25), text="Controls:", fill='green')
            canvas.create_text(data['boardWidth']*data['blockSize']/2 + 70, 200, font=("Lucida Console", 15), text="Use A and D to move", fill='green')
            canvas.create_text(data['boardWidth']*data['blockSize']/2 + 70, 230, font=("Lucida Console", 15), text="Use J and K to rotate", fill='green')
            canvas.create_text(data['boardWidth']*data['blockSize']/2 + 70, 260, font=("Lucida Console", 15), text="Press Space to drop down", fill='green')
            canvas.create_text(data['boardWidth']*data['blockSize']/2 + 70, 290, font=("Lucida Console", 15), text="Press P during the game to pause", fill='green')
        elif data['startup']:
            canvas.create_text(data['boardWidth']*data['blockSize']/2 + 70, 150, font=("Lucida Console", 35), text="Tetris", fill='green')
            canvas.create_text(data['boardWidth']*data['blockSize']/2 + 70, 250, font=("Lucida Console", 25), text="Press P to Play", fill='green')
            canvas.create_text(data['boardWidth']*data['blockSize']/2 + 70, 350, font=("Lucida Console", 15), text="Press H for help", fill='green')
        else:
            canvas.create_text(data['boardWidth']*data['blockSize']/2 + 70, 200, font=("Lucida Console", 25), text="Paused", fill='green')
            
        
    def drawBoard(canvas, data):
        #draw gameBoard
        for i in range(len(data['gameBoard'])):
            for j in range(1, len(data['gameBoard'][i]) - 1):
                drawSquare(j*data['blockSize'], i*data['blockSize'], data['blockSize'], data['gameBoard'][i][j], canvas)
        #draw left edge
        canvas.create_rectangle(0, 0, data['blockSize'], data['boardLength']*data['blockSize'], fill="gold")
        #draw right edge
        canvas.create_rectangle(data['boardWidth']*data['blockSize'] - data['blockSize'], 0, data['boardWidth']*data['blockSize'], data['boardLength']*data['blockSize'], fill='gold')
        #draw scoreboard
        canvas.create_rectangle(data['boardWidth']*data['blockSize'], 0, data['width']*data['blockSize'], data['boardLength']*data['blockSize'], fill='lightgrey')
        
        
    def drawScore(canvas, data):
        canvas.create_text(data['boardWidth']*data['blockSize'] + data['blockSize']*2 + 27, 200, font=("Lucida Console", 20), text="Score \n" + str(data['score']))
        
    def drawTetromino(canvas, data):
        for i in range(len(data['player'])):
            drawSquare(data['player'][i][0]*data['blockSize'], data['player'][i][1]*data['blockSize'], data['blockSize'], data['color'], canvas)
        
    def drawSquare(x, y, width, color, canvas):
        canvasX = x
        canvasY = y
        if(color == "white"):
                canvas.create_rectangle(canvasX, canvasY, width + canvasX, width + canvasY)
                return
        canvas.create_rectangle(canvasX, canvasY, width + canvasX, width + canvasY, fill=color)
        
    def drawCircle(x, y, radius, color, canvas):
        canvasX = x - radius
        canvasY = y - radius0s
        canvas.create_oval(canvasX, canvasY, radius*2 + canvasX, radius*2 + canvasY, fill=color)




    def run(width=300, height=300):
        def redrawAllWrapper(canvas, data):
            canvas.delete(ALL)
            redrawAll(canvas, data)
            canvas.update()
        
        def mousePressedWrapper(event, canvas, data):
            mousePressed(event, data)
            redrawAllWrapper(canvas, data)
            
        def keyPressedWrapper(event, canvas, data):
            keyPressed(event, data)
            redrawAllWrapper(canvas, data)
            
        def keyReleasedWrapper(event, canvas, data):
            keyReleased(event, data)
            redrawAllWrapper(canvas, data)
            
        def timerFiredWrapper(canvas, data):
            timerFired(data)
            redrawAllWrapper(canvas, data)
            #pause
            canvas.after(data["timerDelay"], timerFiredWrapper, canvas, data)
        
        data = dict()

        data["width"] = width
        data["height"] = height
        data["timerDelay"] = 200
        init(data)
        
        root = Tk()
        root.wm_title("Tetris")
        canvas = Canvas(root, width=data["width"] + 5*data['blockSize'], height=data["height"])
        canvas.configure(background="black")
        canvas.pack()
        
        root.bind("<Button-1>", lambda event: mousePressedWrapper(event, canvas, data))
        root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas, data))
        root.bind("<KeyRelease>", lambda event: keyReleasedWrapper(event, canvas, data))
        data['root'] = root
        timerFiredWrapper(canvas, data)
        root.mainloop()


    run(400, 400)

