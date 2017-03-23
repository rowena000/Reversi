
import sys

def withinRange(i, j):
    return i >= 0 and i < 8 and j >= 0 and j < 8

def isValidMove(board, player, i, j):
    if board[i][j] != '*' or not withinRange(i, j):
        return False
    for dir in directions:
        p = i + dir[0]
        q = j + dir[1]
        while withinRange(p, q):
            if board[p][q] == "*" or board[p][q] == player and board[p - dir[0]][q - dir[1]] == "*":
                break
            elif board[p][q] == player and board[p - dir[0]][q - dir[1]] != player and board[p - dir[0]][q - dir[1]] != "*":
                return True
            p += dir[0]
            q += dir[1]
    return False

def getValidMoves(board, player):
    v_moves = list()
    for x in range(8):
        for y in range(8):
            if isValidMove(board, player, x, y):
                v_moves.append([x, y])
    return v_moves

def flip(board, startX, startY, endX, endY, player, dir):
    i = endX - dir[0]
    j = endY - dir[1]
    while i >= startX and j >= startY:
        board[i][j] = player
        i -= dir[0]
        j -= dir[1]

def getNextState(board, move, player):
    new_board = list(board)
    if move is None:
        return new_board
    for dir in directions:
        x = move[0] + dir[0]
        y = move[1] + dir[1]
        while withinRange(x, y):
            if new_board[x][y] == "*":
                break
            elif new_board[x][y] == player:
                flip(new_board, move[0], move[1], x, y, player, dir)
            x += dir[0]
            y += dir[1]
    return new_board

def getOpponent(player):
    opp = "O"
    if player == "O":
        opp = "X"
    return opp

def getIndex(move):
    if move is None:
        return "root"
    return columnName[move[1]] + (move[0] + 1)

def printLog(index, depth, value, a, b):
    if value == sys.maxint:
        value = "Infinity"
    elif value == -sys.maxint - 1:
        value = "-Infinity"
    print index + ", " + depth + ", " + value + ", " + a + ", " + b

def getMax(board, player, a, b, depth, maxDepth, move):
    if depth == maxDepth:
        a = v = matrix[move[0]][move[1]]
        return v
    v = -sys.maxint - 1

    new_board = getNextState(board, move, player)
    v_moves = getValidMoves(new_board, getOpponent(player))
    if not v_moves:
        v = max(v, getMin(new_board, getOpponent(player), a, b, depth + 1, None))
        printLog("pass", depth, v, a, b)
    else:
        for v_move in v_moves:
            v = max(v, getMin(new_board, getOpponent(player), a, b, depth + 1, v_move))
            printLog(getIndex(move), depth, v, a, b)
            if v > b:
                return v
            a = max(a, v)
    return v

def getMin(board, player, a, b, depth, maxDepth, move):
    v = sys.maxint
    if depth == maxDepth:
        b = v = matrix[move[0]][move[1]]
        return v
    new_board = getNextState(board, move, player)
    printLog(getIndex(move), depth, v, a, b)
    if not v_moves:
        v = min(v, getMax(new_board, getOpponent(player), a, b, depth + 1, maxDepth, v_move))
        printLog("pass", depth, v, a, b)
    else:
        for v_move in v_moves:
            v = min(v, getMax(new_board, getOpponent(player), a, b, depth + 1, maxDepth, v_move))
            printLog(getIndex(move), depth, v, a, b)
            if v <= a:
                return v
            b = min(b, v)
    return v

def alphaBetaSearch(board, player, maxDepth):
    getMax(board, getOpponent(player), -sys.maxint - 1, sys.maxint, 0, maxDepth, None)





filename = raw_input("Please enter file name: ")

f = open(filename, "r")

print "Here's your file %r:" % filename
lines = f.read().splitlines()
matrix = [[99, -8, 8, 6, 6, 8, -8, 99],
         [-8, -24, -4, -3, -3, -4, -24, -8],
         [8, -4, 7, 4, 4, 7, -4, 8],
         [6, -3, 4, 0, 0, 4, -3, 6],
         [6, -3, 4, 0, 0, 4, -3, 6],
         [8, -4, 7, 4, 4, 7, -4, 8],
         [-8, -24, -4, -3, -3, -4, -24, -8],
         [99, -8, 8, 6, 6, 8, -8, 99]]

directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
columnName = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
board = []
player = '*'
depth = 0
i = 0
for line in lines:
    if i == 0:
        player = line

    elif i == 1:
        depth = int(line)
    else:
        l = list(line)
        board.append(l)
    i += 1

if player != "O" and player != "X":
    print "Invalid player, program terminated."
    exit(1);
else:
    print "Player is %r:" % player
if depth <= 0:
    print "Invalid depth, program terminated."
    exit(1);
else:
    print "Depth is %r:" % depth
print "Board:"
for p in range(8):
    print ''.join(board[p])

f.close()



v_moves = getValidMoves(board, player)

