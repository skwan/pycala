
#
# Pycala - a Mancala game just for fun
#
# by Stuart Kwan
# Copyright 2024
#

import constants

#
# Initialize game board
#
def initGameBoard(mancalaBoard, numPebbles):
    #
    # Gameboard index values:
    # [0]-[5]: Player 1's game pods
    # [7]-[12]: Player 2's game pods
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
        mancalaBoard[constants.TURN_RESULT] = constants.GAME_COMPLETE
    if player2Remaining == 0:
        sweepPebblesRemaining(mancalaBoard, 1)
        mancalaBoard[constants.TURN_RESULT] = constants.GAME_COMPLETE
    return mancalaBoard

#
# Check for a free turn
#
def checkFreeTurn(mancalaBoard, index):
    freeTurn = constants.NO_FREE_TURN
    # Drop in own score pod, receive free turn
    if mancalaBoard[constants.CURRENT_PLAYER] == 1 and index == constants.P1_SCORE:
        freeTurn = constants.FREE_TURN
    if mancalaBoard[constants.CURRENT_PLAYER] == 2 and index == constants.P2_SCORE:
        freeTurn = constants.FREE_TURN
    if freeTurn == constants.FREE_TURN:
        print("Free turn!")
        print("")
    return freeTurn

#
# Check for a steal
#
def checkSteal(mancalaBoard, index):
    stealIndex = 12 - index
    # If the last pebble was dropped into an empty pod and the pod opposite is not empty
    if mancalaBoard[index] == 1 and mancalaBoard[stealIndex] > 0:
        # If player 1 dropped into a pod on their side, steal
        if mancalaBoard[constants.CURRENT_PLAYER] == 1 and index < 6:
            print("Steal pod %s!" % stealIndex)
            print("")
            mancalaBoard = steal(mancalaBoard, index, constants.P1_SCORE)
        # if player 2 dropped into a pod on their side, steal
        if mancalaBoard[constants.CURRENT_PLAYER] == 2 and index > 6:
            # Because on player 1 side of the board the pod index starts at 0
            visibleStealIndex = stealIndex + 1
            print("Steal pod %s!" % visibleStealIndex)
            print("")
            mancalaBoard = steal(mancalaBoard, index, constants.P2_SCORE)
    return mancalaBoard

# Process a game turn
def gameTurn(mancalaBoard, podIndex):
    # Reset game state to 0
    mancalaBoard[constants.TURN_RESULT] = 0
    freeTurn = constants.NO_FREE_TURN
    inHand = 0
    # If the move is off the board, return error
    if podIndex < 0 or podIndex > 12:
        mancalaBoard[constants.TURN_RESULT] = -1
        return mancalaBoard
    # If no player is yet selected, the initialize the current player
    if mancalaBoard[constants.CURRENT_PLAYER] == 0:
        if podIndex < 7:
            mancalaBoard[constants.CURRENT_PLAYER] = 1
        elif podIndex > 6:
            mancalaBoard[constants.CURRENT_PLAYER] = 2
    # If this is player 1's turn
    if mancalaBoard[constants.CURRENT_PLAYER] == 1:
        # Check if they are trying to move player 2's pod
        if podIndex > 6:
            mancalaBoard[constants.TURN_RESULT] = -2
            return mancalaBoard
        # Otherwise set the index to move down by one because python arrays start with 0
        else:
            index = podIndex - 1
    # If this is player 2's turn
    if mancalaBoard[constants.CURRENT_PLAYER] == 2:
        # Check if they are trying to move player 1's pod
        if podIndex < 7:
            mancalaBoard[constants.TURN_RESULT] = -2
            return mancalaBoard
        # Otherwise set the index to be played
        else:
            index = podIndex
    # If the player selected an empty pod, return error
    if mancalaBoard[index] == 0:
        mancalaBoard[constants.TURN_RESULT] = -3
        return mancalaBoard
    # Pick up the pebbles in that pod into your hand
    inHand = mancalaBoard[index]
    mancalaBoard[index] = 0
    # Drop pebbles in each next pod until your hand is empty
    while inHand > 0:
        # Move to the next pod
        index = index + 1
        # If player 1 and the next pod is player 2's, skip it and turn the corner
        if mancalaBoard[constants.CURRENT_PLAYER] == 1 and index == 13:
            index = 0
        # If player 2 and the next pod is player 1's, skip it and turn the corner
        if mancalaBoard[constants.CURRENT_PLAYER] == 2 and index == 6:
            index = 7
        # if player 2 and the next pod is off the end of the board, turn the corner
        if mancalaBoard[constants.CURRENT_PLAYER] == 2 and index == 14:
            index = 0
        # Take a pebble out of your hand and put it in the pod
        inHand = inHand - 1
        mancalaBoard[index] = mancalaBoard[index] + 1
    # Special rules
    freeTurn = checkFreeTurn(mancalaBoard, index)
    mancalaBoard = checkSteal(mancalaBoard, index)
    # Advance to next player
    if freeTurn == constants.NO_FREE_TURN:
        if mancalaBoard[constants.CURRENT_PLAYER] == 1:
            mancalaBoard[constants.CURRENT_PLAYER] = 2
        else:
            mancalaBoard[constants.CURRENT_PLAYER] = 1
    # Increment turn number
    mancalaBoard[constants.GAME_TURN] = mancalaBoard[constants.GAME_TURN] + 1
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
lastMancalaBoard = []
numPebbles = 4
debug = 1
mancalaBoard = initGameBoard(mancalaBoard, numPebbles)
lastMancalaBoard = mancalaBoard
# Loop until the game is over
while mancalaBoard[constants.TURN_RESULT] != constants.GAME_COMPLETE:
    print("")
    printGameBoard(mancalaBoard)
    if debug == 1:
        print("Game state: %s" % mancalaBoard[constants.TURN_RESULT])
        print("")
    print("Turn: %s" % mancalaBoard[constants.GAME_TURN])
    if mancalaBoard[constants.CURRENT_PLAYER] == 0:
        print("Player: Not Selected")
        print("Select pod to play (1-12) or X to exit")
    else:
        print("Player: %s" % mancalaBoard[constants.CURRENT_PLAYER])
        if mancalaBoard[constants.CURRENT_PLAYER] == 1:
            print("Select pod to play (1-6), U to undo, or X to exit")
        if mancalaBoard[constants.CURRENT_PLAYER] == 2:
            print("Select pod to play (7-12), U to undo, or X to exit")
    playerInput = input()
    print("")
    if playerInput == "X" or playerInput == "x":
        # Exit game
        print("Exiting game")
        break
    if playerInput == "U" or playerInput == "u":
        # Undo last move
        # BUGBUG this isn't working yet
        mancalaBoard = lastMancalaBoard
    else:
        lastMancalaBoard = mancalaBoard
        mancalaBoard = gameTurn(mancalaBoard, int(playerInput))
        if mancalaBoard[constants.TURN_RESULT] < 0:
            print("Illegal move, try again.")
if mancalaBoard[constants.TURN_RESULT] == constants.GAME_COMPLETE:
    printGameBoard(mancalaBoard)
    print("")
    if mancalaBoard[constants.P1_SCORE] > mancalaBoard[constants.P2_SCORE]:
        print("Player 1 wins!")
    elif mancalaBoard[constants.P2_SCORE] > mancalaBoard [constants.P1_SCORE]:
        print("Player 2 wins!")
    else:
        print("Game ends in a tie!")
    