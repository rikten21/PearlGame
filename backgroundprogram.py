import sys
import numpy as np

# globalis változók
_initialization = False
_matrix = []
_necklace = []
_BWlists = []
_L = 0
_N = 0
_F = 0
_position = 1

def _data(input): # adatok beolvasása input fájlból
    infile = open(input, "r")
    while True:
        line = infile.readline().strip()
        if line == "":
            break

        datas = line.split(" ")
        L, N, F = int(datas[0]), int(datas[1]), int(datas[2]) # nyaklánc hossza(L), törpék száma(N), első törpe IDja(F)

        line = infile.readline().strip()
        necklace = [''] # nyaklánc
        for i in line:
            necklace.append(i)

        BWlists = [] # törpék [ID, szín, fekete lista, fehér lista]
        BWlists.append([])
        for i in range(1, N + 1):
            dwarf = [] # törpe

            line = infile.readline().strip()
            data = line.split(" ")

            color = int(data[0]) # törpe színe
            lengthB = int(data[1]) # fekete lista hossza
            lengthW = int(data[lengthB + 2]) # fehér lista hossza
            Blist = [] # fekete lista
            Wlist = [] # fehér lista

            for k in range(2, lengthB + 2):
                Blist.append(int(data[k]))
            for k in range(lengthB + 3, lengthB + 3 + lengthW):
                Wlist.append(int(data[k]))

            dwarf.append(i)
            dwarf.append(color)
            dwarf.append(Blist)
            dwarf.append(Wlist)

            BWlists.append(dwarf)
    return L, N, F, necklace, BWlists

def _winnerMatrix(input):
    L, N, F, necklace, BWlists = _data(input) # nyaklánc hossza(L), törpék száma(N), első törpe IDja(F), törpék [ID, szín, fekete lista, fehér lista]
    matrix = np.random.randint(-1, 0, (N + 1, L + 1))

    for j in range(L, 0, -1):
        for i in range(1, N + 1):
            if necklace[j] == 'D': # utolsó gyöngyszem
                if BWlists[i][1] == 0:
                    matrix[i, j] = 0
                else:
                    matrix[i, j] = 1
            else: # fekete vagy fehér lista
                if necklace[j] == 'B':
                    list = BWlists[F][2]
                else:
                    list = BWlists[F][3]

                if BWlists[i][1] == 0: # zöld törpe esetén
                    for l in list:
                        if matrix[l, j + 1] == 0:
                            matrix[i, j] = 0
                            break
                        else:
                            matrix[i, j] = 1
                else:
                    for l in list:
                        if matrix[l, j + 1] == 1:
                            matrix[i, j] = 1
                            break
                        else:
                            matrix[i, j] = 0

    return matrix, L, N, F, necklace, BWlists




def setNext(d):
    global _initialization, _matrix, _L, _N, _F, _necklace, _BWlists, _position

    if not _initialization: # az adatok be lettek-e már olvasva
        _matrix, _L, _N, _F, _necklace, _BWlists = _winnerMatrix("input.txt")
        _initialization = True

    if _BWlists[_F][1] == 1: # ha a törpe vörös
        print("Something is wrong.")
        sys.exit(0)

    if _position >= _L: # ha már elfogytak a gyöngyszemek
        print("Something is wrong.")
        sys.exit(0)

    if _necklace[_position] == 'B': # fekete vagy fehér gyöngy
        list = _BWlists[_F][2]
    else:
        list = _BWlists[_F][3]

    if d not in list: # ha a választott törpe ID-ja nem szerepel az adott törpe listáján
        print("Something is wrong.")
        sys.exit(0)

    _position += 1
    _F = d
    print("setNext({0})".format(d))


def getNext():
    global _initialization, _matrix, _L, _N, _F, _necklace, _BWlists, _position

    if not _initialization: # az adatok be lettek-e már olvasva
        _matrix, _L, _N, _F, _necklace, _BWlists = _winnerMatrix("input.txt")
        _initialization = True

    if _BWlists[_F][1] == 0: # ha a törpe zöld
        print("Something is wrong.")
        sys.exit(0)

    if _position >= _L: # ha már elfogytak a gyöngyszemek
        print("Something is wrong.")
        sys.exit(0)

    if _necklace[_position] == 'B': # fekete vagy fehér gyöngy
        list = _BWlists[_F][2]
    else:
        list = _BWlists[_F][3]

    for i in list:
        if _matrix[i,_position+1] == 1:
            _F = i
            break
        else:
            _F = list[0]

    _position += 1
    print("getNext() = {0}".format(_F))
    return _F

def finish():
    global _initialization, _matrix, _L, _N, _F, _necklace, _BWlists, _position

    if not _initialization: # az adatok be lettek-e már olvasva
        _matrix, _L, _N, _F, _necklace, _BWlists = _winnerMatrix("input.txt")
        _initialization = True

    if _position == _L and _BWlists[_F][1] == 0:
        print("You won.")

    else:
        print("Something is wrong.")

    sys.exit(0)