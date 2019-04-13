import numpy as np
from pearlProblem.backgroundprogram import *

def pearlGame(input):
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
        for i in range(1,N+1):
            dwarf = [] # törpe

            line = infile.readline().strip()
            data = line.split(" ")

            color = int(data[0]) # törpe színe
            lengthB = int(data[1]) # fekete lista hossza
            lengthW = int(data[lengthB+2]) # fehér lista hossza
            Blist = [] # fekete lista
            Wlist = [] # fehér lista

            for k in range(2, lengthB+2):
                Blist.append(int(data[k]))
            for k in range(lengthB+3, lengthB+3+lengthW):
                Wlist.append(int(data[k]))

            dwarf.append(i)
            dwarf.append(color)
            dwarf.append(Blist)
            dwarf.append(Wlist)
            BWlists.append(dwarf)

        # mátrix, mikor melyik törpeklán győz
        matrix = np.random.randint(-1,0,(N+1,L+1))

        for j in range(L, 0, -1):
            for i in range(1, N+1):
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
                            if matrix[l, j+1] == 0:
                                matrix[i, j] = 0
                                break
                            else:
                                matrix[i, j] = 1
                    else:
                        for l in list:
                            if matrix[l, j+1] == 1:
                                matrix[i, j] = 1
                                break
                            else:
                                matrix[i, j] = 0

        for pearl in range(1,L+1): # melyik törpe kinek adja tovább
            if necklace[pearl] == 'D': # utolsó törpe esetén
                finish()

            elif necklace[pearl] == 'B': # fekete vagy fehér gyöngy esetén
                list = BWlists[F][2]
            else:
                list = BWlists[F][3]

            if BWlists[F][1] == 0: # ha zöld törpénél van a gyöngy
                for d in list:
                    if matrix[d, pearl+1] == 0:
                        setNext(d)
                        F = d
                        pearl += 1
                        break
                    else:
                        setNext(list[0])
                        F = list[0]
                        pearl += 1
            else:
                F = getNext()
                pearl += 1


def main():
    pearlGame("input.txt")

if __name__ == "__main__":
    main()