
# Pycala - a Mancala game just for fun1

# Initialize game board
def initGameBoard():
    global mancalaBoard
    numPebbles = 4
    mancalaBoard = [numPebbles,numPebbles,numPebbles,numPebbles,numPebbles,numPebbles,0,numPebbles,numPebbles,numPebbles,numPebbles,numPebbles,numPebbles,0]

# Steal the opposing player's cala
def steal(fromIndex, toIndex):
    global mancalaBoard
    # Take that pebble
    mancalaBoard [fromIndex] = 0
    mancalaBoard[toIndex] = mancalaBoard[toIndex] + 1
    # Steal opposing pebbles
    opposingIndex = 12 - fromIndex
    mancalaBoard[toIndex] = mancalaBoard[toIndex] + mancalaBoard[opposingIndex]
    mancalaBoard[opposingIndex] = 0

# Count pebbles remaining
def countPebblesRemaining(index):
    global mancalaBoard
    total = 0
    for x in range (index, index + 6):
        total = total + mancalaBoard[x]
    return total

# Sweep pebbles remaining
def sweepPebblesRemaining(index):
    global mancalaBoard
    total = 0
    for x in range (index, index + 6):
        total = total + mancalaBoard[x]
        mancalaBoard[x] = 0
    if index == 0:
        mancalaBoard[6] = mancalaBoard[6] + total
    if index == 7:
        mancalaBoard[13] = mancalaBoard[13] + total
    return

# Check if the game is complete
def checkFinishingConditions():
    # The game is won if the player to play next has no moves remaining
    global playerTurn
    playerARemaining = countPebblesRemaining(0)
    playerBRemaining = countPebblesRemaining(7)
    if playerARemaining == 0:
        sweepPebblesRemaining(7)
        return 0
    if playerBRemaining == 0:
        sweepPebblesRemaining(0)
        return 0
    return 1

# Process a game turn
def gameTurn(moveCala):
    global mancalaBoard
    global playerTurn
    result = 1
    nextPlayer = "Yes"
    inHand = 0
    # If the move is off the board, return error
    if int(moveCala) < 0 or int(moveCala) > 12:
        result = -1
        return result
    if int(moveCala) > 0 and int(moveCala) < 7:
        if playerTurn == "Not Selected":
            playerTurn = "A"
        if playerTurn == "B":
            result = -2
            return result
        index = int(moveCala) - 1
    if int(moveCala) > 6 and int(moveCala) < 13:
        if playerTurn == "Not Selected":
            playerTurn = "B"
        if playerTurn == "A":
            result = -2
            return result
        index = int(moveCala)
    # If the player selected an empty cala, return error
    if mancalaBoard[index] == 0:
        result = -3
        return result
    # Pick up the pebbles in that cala into your hand
    inHand = mancalaBoard[index]
    mancalaBoard[index] = 0
    while inHand > 0:
        # Move to the next cala
        index = index + 1
        # If player A and the next cala is player B's, skip it and turn the corner
        if playerTurn == "A" and index == 13:
            index = 0
        # If player B and the next cala is player A's, skip it and turn the corner
        if playerTurn == "B" and index == 6:
            index = 7
        # if player B and the next cala is off the end of the board, turn the corner
        if playerTurn == "B" and index == 14:
            index = 0
        # Take a pebble out of your hand and put it in the cala
        inHand = inHand - 1
        mancalaBoard[index] = mancalaBoard[index] + 1
    # Special rules
    if playerTurn == "A":
        # Drop in own cala, receive free turn
        if index == 6:
            print("")
            print("Free turn!")
            print("")
            nextPlayer = "No"
        # Drop on own side in empty cala, steal opposing cala
        if index > -1 and index < 6:
            if mancalaBoard[index] == 1 and mancalaBoard[12-index] != 0:
                stealIndex = 12 - index
                print("")
                print("Steal cala %s!" % stealIndex)
                print("")
                steal(index,6)
    if playerTurn == "B":
        # Drop in own cala, receive free turn
        if index == 13:
            print("")
            print("Free turn!")
            print("")
            nextPlayer = "No"
        # Drop on own side in empty cala, steal opposing cala
        if index > 6 and index < 13:
            if mancalaBoard[index] == 1 and mancalaBoard[12-index] != 0:
                stealIndex = 12 - index
                print("")
                print("Steal cala %s!" % stealIndex)
                print("")
                steal(index,13)
    # Advance to next player
    if nextPlayer == "Yes":
        if playerTurn == "A":
            playerTurn = "B"
        else:
            playerTurn = "A"
    result = checkFinishingConditions()
    return result

# Print game board
def printGameBoard():
    global mancalaBoard
    boardSide = "/-------6----5----4----3----2----1------\\"
    print(boardSide)
    p1Board = "|    | "
    for x in range(5, -1, -1):
        if mancalaBoard[x] < 10: p1Board = p1Board + " " 
        p1Board = p1Board + "%s" % mancalaBoard[x] + " | "
    p1Board = p1Board + "   |"
    print(p1Board)
    scoreBoard = "| "
    if mancalaBoard[6] < 10: scoreBoard = scoreBoard + " "
    scoreBoard = scoreBoard + "%s" % mancalaBoard[6] + " |"
    scoreBoard = scoreBoard + "-----"*5
    scoreBoard = scoreBoard + "----| "
    if mancalaBoard[13] < 10: scoreBoard = scoreBoard + " "
    scoreBoard = scoreBoard + "%s" % mancalaBoard[13] + " |"
    boardSide = "\\-------7----8----9---10---11---12------/"
    print(scoreBoard)
    p2Board = "|    | "
    for x in range(7,13):
        if mancalaBoard[x] < 10: p2Board = p2Board + " " 
        p2Board = p2Board + "%s" % mancalaBoard[x] + " | "
    p2Board = p2Board + "   |"
    print(p2Board)
    print(boardSide)

# Gameplay loop
lastMancalaBoard = []
mancalaBoard = []
initGameBoard()
turn = 1
playerTurn = "Not Selected"
playerInput = "X"
result = 1
while result != 0:
    printGameBoard()
    print("")
    print("Turn: %s" % turn)
    print("Player: %s" % playerTurn)
    if playerTurn == "Not Selected":
        print("Select cala to play (1-12) or X to exit")
    elif playerTurn == "A":
        print("Select cala to play (1-6), U to undo, or X to exit")
    else:
        print("Select cala to play (7-12), U to undo, or X to exit")
    playerInput = input()
    if playerInput == "X":
        # Exit game
        print("Exiting game")
        break
    if playerInput == "U" and playerTurn != "Not Selected":
        break
    # Save the last board in case of undo
    lastMancalaBoard = mancalaBoard
    result = gameTurn(playerInput)
    if result == 0:
        # Current player has won the game
        break
    # Illegal move
    elif result < 0:
        print("")
        print("Illegal move, try again.")
    # Next turn
    else:
        turn = turn + 1
if playerTurn != "Not Selected":
    print("")
    printGameBoard()
    print("")
    if mancalaBoard[6] > mancalaBoard[13]:
        print("Player A wins!")
    elif mancalaBoard[13] > mancalaBoard [6]:
        print("Player B wins!")
    else:
        print("Game ends in a tie!")
    