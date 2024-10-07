import math


class Matrix:
    def __init__(self, r, c, iden=0) -> None:
        self.data = [[] for i in range(r)]

        for i in range(r):
            for j in range(c):
                if iden == 1 and i == j:
                    self.data[i].append(1)
                else:
                    self.data[i].append(0)

        self.r = r
        self.c = c

    def getRow(self, r) -> list:
        return self.data[r]
    
    def setRow(self, r, val) -> None:
        self.data[r] = val

    def getCol(self, c) -> list:
        out = []
        for i in range(self.r):
            out.append(self.data[i][c])
        return out
    
    def elum(self, r1, r2, mult=1, null=-1) -> None:
        new_row = [0 for i in range(self.c)]
        if null != -1:
            mult = self.data[r1][null] / self.data[r2][null]
        for i in range(self.c):
            new_row[i] = self.data[r1][i] - self.data[r2][i] * mult
        self.data[r1] = new_row
    
    def mulRow(self, r, mult) -> None:
        self.data[r] = [i * mult for i in self.data[r]]

    def hasNeg(self, r) -> int:
        check = self.data[r][0:-1]
        for i in check:
            if i < 0:
                return True
        return False
    
    def checkRatio(self, c) -> int:
        minimum = math.inf
        index = -1
        for i in range(self.r):
            if self.data[i][c] != 0:
                ratio = self.data[i][-1] / self.data[i][c]
            else:
                continue
            if ratio < minimum and ratio > 0:
                minimum = ratio
                index = i
        return index
    
    def findMin(self, r) -> int:
        maxInd = -1
        minimum = math.inf
        for i in range(self.c):
            if self.data[r][i] < minimum:
                minimum = self.data[r][i]
                minInd = i
        return minInd


def cat(Matrix1: Matrix, Matrix2: Matrix =None):
        if Matrix2 == None:
            for i in range(Matrix1.r):
                for j in Matrix1.data[i]:
                    print(round(j, 2), end=" ")
                print()
            return
        else:
            new_Matrix = Matrix(Matrix1.r, Matrix1.c + Matrix2.c)
            for i in range(Matrix1.r):
                new_Matrix.setRow(i, Matrix1.data[i] + Matrix2.data[i])
            return new_Matrix

def transpose(Matrix1: Matrix) -> Matrix:
        new_Matrix = Matrix(Matrix1.c, Matrix1.r)
        for i in range(Matrix1.c):
            new_Matrix.setRow(i, Matrix1.getCol(i))
        return new_Matrix

Ccounter = 0
Acounter = 0

C_arr = []
A_arr = []
d_arr = []

with open("input_data.txt", "r") as input:
    line = input.readline()

    while True:
        line = input.readline()
        if line == "A:\n":
            break
        C_arr.append(-int(line))
        Ccounter += 1

    while True:
        line = input.readline()
        if line == "d:\n":
            break
        A_arr.append([int(i) for i in line.split()])
        Acounter += 1

    for i in range(Acounter):
        line = input.readline()
        d_arr.append(int(line))

    d = Matrix(1, Acounter)
    A = Matrix(Acounter, Ccounter)
    Identity = Matrix(Acounter, Acounter, iden=1)

    for i in range(Acounter):
        A.setRow(i, A_arr[i])

    d.setRow(0, d_arr)
    d = transpose(d)

    PreSim = cat(cat(A, Identity), d)
    
    for i in range(Acounter + 1):
        C_arr.append(0)

    Sim = Matrix(1 + Acounter, Ccounter + Acounter + 1)
    Sim.setRow(0, C_arr)

    for i in range(Acounter):
        Sim.setRow(i + 1, PreSim.getRow(i))

    while Sim.hasNeg(0):
        index = Sim.findMin(0)
        rat_ind = Sim.checkRatio(index)

        Sim.mulRow(rat_ind, 1/Sim.data[rat_ind][index])

        cat(Sim)
        print()

        for i in range(Acounter + 1):
            if i != rat_ind:
                Sim.elum(i, rat_ind, null=index)
                cat(Sim)
                print()

    ans = Sim.getCol(-1)
    x_arr = [0 for i in range(Ccounter)]

    for i in range(Ccounter):
        col = Sim.getCol(i)
        if sum(col) == 1:
            x_arr[i] = ans[col.index(1)]
            
    print("x*:", end=" ")
    for i in x_arr:
        print(round(i, 2), end=" ")

    print()
    print(f"z: {round(ans[0], 2)}")
