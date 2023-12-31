#  Connect Four clone


import random
import copy
import sys

boardWidth = 7
boardHeight = 6

def main():
    print('Four-In-A-Row')
    print()

    while True:
        humanTile, computerTile = enterHumanTile()
        turn = whoGoesFirst()
        print('The %s player will go first.' % (turn))
        mainBoard = getNewBoard()

        while True:
            if turn == 'human':
                drawBoard(mainBoard)
                move = getHumanMove(mainBoard)
                makeMove(mainBoard, humanTile, move)
                if isWinner(mainBoard, humanTile):
                    winner = 'human'
                    break
                turn = 'computer'
            else:
                drawBoard(mainBoard)
                print('The computer is thinking...')
                move = getComputerMove(mainBoard, computerTile)
                makeMove(mainBoard, computerTile, move)
                if isWinner(mainBoard, computerTile):
                    winner = 'computer'
                    break
                turn = 'human'

            if isBoardFull(mainBoard):
                winner = 'tie'
                break

        drawBoard(mainBoard)
        print('Winner is: %s' % winner)
        if not playAgain():
            break

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def enterHumanTile():
    # Let's the human player type which tile they want to be.
    # Returns a list with the human player's tile as the first item, and the computer's tile as the second.
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    # the first element in the tuple is the human player's tile, the second is the computer's tile.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def drawBoard(board):
    print()
    print(' ', end='')
    for x in range(1, boardWidth + 1):
        print(' %s  ' % x, end='')
    print()

    print('+---+' + ('---+' * (boardWidth - 1)))

    for y in range(boardHeight):
        print('|   |' + ('   |' * (boardWidth - 1)))

        print('|', end='')
        for x in range(boardWidth):
            print(' %s |' % board[x][y], end='')
        print()

        print('|   |' + ('   |' * (boardWidth - 1)))

        print('+---+' + ('---+' * (boardWidth - 1)))

def getNewBoard():
    board = []
    for x in range(boardWidth):
        board.append([' '] * boardHeight)
    return board


def getHumanMove(board):
    while True:
        print('Which column do you want to move on? (1-%s, or "quit" to quit game)' % (boardWidth))
        move = input()
        if move.lower().startswith('q'):
            sys.exit()
        if not move.isdigit():
            continue
        move = int(move) - 1
        if isValidMove(board, move):
            return move

def getComputerMove(board, computerTile):
    potentialMoves = getPotentialMoves(board, computerTile, 2)
    bestMoveScore = max([potentialMoves[i] for i in range(boardWidth) if isValidMove(board, i)])
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveScore:
            bestMoves.append(i)
    return random.choice(bestMoves)

def getPotentialMoves(board, playerTile, lookAhead):
    if lookAhead == 0:
        return [0] * boardWidth

    potentialMoves = []

    if playerTile == 'X':
        enemyTile = 'O'
    else:
        enemyTile = 'X'

    # Returns (best move, average condition of this state)
    if isBoardFull(board):
        return [0] * boardWidth

    # Figure out the best move to make.
    potentialMoves = [0] * boardWidth
    for playerMove in range(boardWidth):
        ComputerSimBoard = copy.deepcopy(board)
        if not isValidMove(ComputerSimBoard, playerMove):
            continue
        makeMove(ComputerSimBoard, playerTile, playerMove)
        if isWinner(ComputerSimBoard, playerTile):
            potentialMoves[playerMove] = 1
            break
        else:
            # do other player's moves and determine best one
            if isBoardFull(ComputerSimBoard):
                potentialMoves[playerMove] = 0
            else:
                for enemyMove in range(boardWidth):
                    ComputerSimBoard2 = copy.deepcopy(ComputerSimBoard)
                    if not isValidMove(ComputerSimBoard2, enemyMove):
                        continue
                    makeMove(ComputerSimBoard2, enemyTile, enemyMove)
                    if isWinner(ComputerSimBoard2, enemyTile):
                        potentialMoves[playerMove] = -1
                        break
                    else:
                        results = getPotentialMoves(ComputerSimBoard2, playerTile, lookAhead - 1)
                        potentialMoves[playerMove] += (sum(results) / boardWidth) / boardWidth
    return potentialMoves

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'human'

def makeMove(board, player, column):
    for y in range(boardHeight-1, -1, -1):
        if board[column][y] == ' ':
            board[column][y] = player
            return

def isValidMove(board, move):
    if move < 0 or move >= (boardWidth):
        return False

    if board[move][0] != ' ':
        return False

    return True

def isBoardFull(board):
    for x in range(boardWidth):
        for y in range(boardHeight):
            if board[x][y] == ' ':
                return False
    return True

def isWinner(board, tile):
    # check horizontal spaces
    for y in range(boardHeight):
        for x in range(boardWidth - 3):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True

    # check vertical spaces
    for x in range(boardWidth):
        for y in range(boardHeight - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True

    # check / diagonal spaces
    for x in range(boardWidth - 3):
        for y in range(3, boardHeight):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True

    # check \ diagonal spaces
    for x in range(boardWidth - 3):
        for y in range(boardHeight - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True

    return False

if __name__ == '__main__':
    main()
