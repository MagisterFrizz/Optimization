class Matrix:
    def __init__(self, row: int, col: int, data=[]):
        self.row = row
        self.col = col
        self.data = data

    def get_row(self, index: int) -> list[type[int]]:
        return self.data[index]
    
    def get_col(self, index: int) -> list[type[int]]:
        col = []
        for i in range(self.row):
            col.append(self.data[i][index])
        return col
    
    def transpose(self) -> None:
        new_data = []
        for i in range(self.col):
            new_data.append(self.get_col[i])
        self.data = new_data

def transposed(matrix: Matrix):
    new_matrix = Matrix(matrix.col, matrix.row)
    new_data = []
    for i in range(matrix.col):
        new_data.append(matrix.get_col(i))
    new_matrix.data = new_data
    return new_matrix

class Vector(Matrix):
    def __init__(self, row: int, col: int, data=[]):
        self.row = row
        self.col = col
        self.data = data

class Table:
    def __init__(self, supply: Vector, demand: Vector, costs: Matrix):
        self.supply = supply
        self.demand = demand
        self.costs = costs

    def display(self) -> None:
        for i in range(self.costs.row):
            print(self.costs.get_row(i) + self.supply.get_row(i))
        print(self.demand.get_row(0))

    def north_west():
        return ...
    
    def vogel():
        return ...
    
    def russel():
        return ...
    
# For Testing
supply_data = [[140, 180, 160]]
supply = transposed(Vector(1, 3, supply_data))

demand_data = [[60, 70, 120, 130, 100]]
demand = Vector(1, 5, demand_data)

costs_data = [[2, 3, 4, 2, 4], 
              [8, 4, 1, 4, 1], 
              [9, 7, 3, 7, 2]]
costs = Matrix(3, 5, costs_data)

table = Table(supply, demand, costs)

# Correct answer for North-West algorithm: 3230

# print("Answer done by North-West algorithm:")
# table.north_west()


# Correct answer for Vogel's algorithm: 1330

# print("Answer done by Vogel's algorithm:")
# table.vogel()


# Correct answer for Russel's algorithm: idk

# print("Answer done by Russel's algorithm:")
# table.russel()

table.display()