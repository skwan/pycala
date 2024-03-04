
#
# Pycala - a Mancala game just for fun
#
# by Stuart Kwan
# Copyright 2024
#

#
# Initialize game board
#
def initGameBoard(mancalaBoard, numPebbles):
    #
    # Gameboard index values:
    # [0]-[5]: Player 1's game pods
    # [6]: Player 1's score pod
    # [7]-[12]: Player 2's game pods
    # [13]: Player 2's score pod
    # [14]: Game turn number, initialized to 1
    # [15]: Current player, initialized to 0
    # [16]: Error result from last turn, negative values are errors, 0 is play next turn, 1 is game is complete
    #
    mancalaBoard = [numPebbles,numPebbles,numPebbles,numPebbles,numPebbles,numPebbles,0,numPebbles,numPebbles,numPebbles,numPebbles,numPebbles,numPebbles,0,1,0,0]
    return mancalaBoard

#
# Steal the opposing player's pod
#
def steal(mancalaBoard, fromIndex, toIndex):
    # Take that pebble
    mancalaBoard[fromIndex] = 0
    mancalaBoard[toIndex] = mancalaBoard[toIndex] + 1
    # Steal opposing pebbles
    opposingIndex = 12 - fromIndex
    mancalaBoard[toIndex] = mancalaBoard[toIndex] + mancalaBoard[opposingIndex]
    mancalaBoard[opposingIndex] = 0
    return mancalaBoard

#
# Count pebbles remaining
#
def countPebblesRemaining(mancalaBoard, player):
    total = 0
    if player == 1:
        index = 0
    if player == 2:
        index = 7
    for x in range (index, index + 6):
        total = total + mancalaBoard[x]
    return total

#
# When a player has no moves left, sweep pebbles remaining for other player
#
def sweepPebblesRemaining(mancalaBoard, player):
    total = 0
    if player == 1:
        index = 0
    if player == 2:
        index = 7
    for x in range (index, index + 6):
        total = total + mancalaBoard[x]
        mancalaBoard[x] = 0
    if player == 1:
        mancalaBoard[6] = mancalaBoard[6] + total
    if player == 2:
        mancalaBoard[13] = mancalaBoard[13] + total
    return mancalaBoard

#
# Check if the game is complete
#
def checkFinishingConditions(mancalaBoard):
    # The game is won if the player to play next has no moves remaining
    player1Remaining = countPebblesRemaining(mancalaBoard, 1)
    player2Remaining = countPebblesRemaining(mancalaBoard, 2)
    if player1Remaining == 0:
        sweepPebblesRemaining(mancalaBoard, 2)
        mancalaBoard[16] = 1
    if player2Remaining == 0:
        sweepPebblesRemaining(mancalaBoard, 1)
        mancalaBoard[16] = 1
    return mancalaBoard

# Process a game turn
def gameTurn(mancalaBoard, podIndex):
    # Reset game state to 0
    mancalaBoard[16] = 0
    nextPlayer = "Yes"
    inHand = 0
    # If the move is off the board, return error
    if int(podIndex) < 0 or int(podIndex) > 12:
        mancalaBoard[16] = -1
        return mancalaBoard
    if int(podIndex) > 0 and int(podIndex) < 7:
        # If the initial move, set player to player 1
        if mancalaBoard[15]== 0:
            mancalaBoard[15] = 1
        # Else if this is player 2, the move is illegal
        elif mancalaBoard[15] == 2:
            mancalaBoard[16] = -2
            return mancalaBoard
        # Set the index of the pod to be moved down by 1 since the pod 1 is index 0
        index = int(podIndex) - 1
    if int(podIndex) > 6 and int(podIndex) < 13:
        # If the initial move, set player to player 2
        if mancalaBoard[15] == 0:
            mancalaBoard[15] = 2
        # Else if this is player 1, the move is illegal
        elif mancalaBoard[15] == 1:
            mancalaBoard[16] = -2
            return mancalaBoard
        # For player 2, the index of the pod to be moved is the same as the input index
        index = int(podIndex)
    # If the player selected an empty cala, return error
    if mancalaBoard[index] == 0:
        mancalaBoard[16] = -3
        return mancalaBoard
    # Pick up the pebbles in that pod into your hand
    inHand = mancalaBoard[index]
    mancalaBoard[index] = 0
    while inHand > 0:
        # Move to the next pod
        index = index + 1
        # If player 1 and the next pod is player 2's, skip it and turn the corner
        if mancalaBoard[15] == 1 and index == 13:
            index = 0
        # If player 2 and the next pod is player 1's, skip it and turn the corner
        if mancalaBoard[15] == 2 and index == 6:
            index = 7
        # if player 2 and the next pod is off the end of the board, turn the corner
        if mancalaBoard[15] == 2 and index == 14:
            index = 0
        # Take a pebble out of your hand and put it in the cala
        inHand = inHand - 1
        mancalaBoard[index] = mancalaBoard[index] + 1
    # Special rules
    if mancalaBoard[15] == 1:
        # Drop in own score pod, receive free turn
        if index == 6:
            print("Free turn!")
            print("")
            nextPlayer = "No"
        # Drop on own side in empty pod, steal opposing pod
        if index > -1 and index < 6:
            if mancalaBoard[index] == 1 and mancalaBoard[12-index] != 0:
                stealIndex = 12 - index
                print("Steal pod %s!" % stealIndex)
                print("")
                mancalaBoard = steal(mancalaBoard, index, 6)
    if mancalaBoard[15] == 2:
        # Drop in own pod, receive free turn
        if index == 13:
            print("Free turn!")
            print("")
            nextPlayer = "No"
        # Drop on own side in empty pod, steal opposing pod
        if index > 6 and index < 13:
            if mancalaBoard[index] == 1 and mancalaBoard[12-index] != 0:
                stealIndex = 12 - index
                visibleStealIndex = stealIndex + 1
                print("Steal pod %s!" % visibleStealIndex)
                print("")
                mancalaBoard = steal(mancalaBoard, index, 13)
    # Advance to next player
    if nextPlayer == "Yes":
        # Increment turn number
        mancalaBoard[14] = mancalaBoard[14] + 1
        # Go to next player
        if mancalaBoard[15] == 1:
            mancalaBoard[15] = 2
        else:
            mancalaBoard[15] = 1
    # See if the game is won
    mancalaBoard = checkFinishingConditions(mancalaBoard)
    return mancalaBoard

# Print game board
def printGameBoard(mancalaBoard):
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
    print("")
    return

# Gameplay loop
mancalaBoard = []
numPebbles = 4
debug = 1
mancalaBoard = initGameBoard(mancalaBoard, numPebbles)
playerInput = "X"
# Loop until the game is over
while mancalaBoard[16] != 1:
    print("")
    printGameBoard(mancalaBoard)
    if debug == 1:
        print("Game state: %s" % mancalaBoard[16])
        print("")
    print("Turn: %s" % mancalaBoard[14])
    if mancalaBoard[15] == 0:
        print("Player: Not Selected")
        print("Select pod to play (1-12) or X to exit")
    else:
        print("Player: %s" % mancalaBoard[15])
        if mancalaBoard[15] == 1:
            print("Select cala to play (1-6), U to undo, or X to exit")
        if mancalaBoard[15] == 2:
            print("Select cala to play (7-12), U to undo, or X to exit")
    playerInput = input()
    print("")
    if playerInput == "X" or playerInput == "x":
        # Exit game
        print("Exiting game")
        break
    mancalaBoard = gameTurn(mancalaBoard, playerInput)
    if mancalaBoard[16] < 0:
        print("Illegal move, try again.")
if mancalaBoard[16] == 1:
    printGameBoard(mancalaBoard)
    print("")
    if mancalaBoard[6] > mancalaBoard[13]:
        print("Player 1 wins!")
    elif mancalaBoard[13] > mancalaBoard [6]:
        print("Player 2 wins!")
    else:
        print("Game ends in a tie!")
    