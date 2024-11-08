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
            new_data.append(self.get_col(i))
        self.row, self.col = self.col, self.row
        self.data = new_data

    def get(self, row: int, col: int) -> int:
        return self.data[row][col]
    
    def copy(self):
        new_matrix = Matrix(self.row, self.col, self.data.copy())
        return new_matrix

    # Helpful methods for Vogel

    def get_minimum_difference(self, geom: int, index: int):
        if geom == 0:
            row = self.get_row(index).sort()
            return row[1] - row[0]
        else:
            col = self.get_col(index).sort()
            return col[1] - col[0]

class Vector(Matrix):
    def __init__(self, row: int, col: int, data=[]):
        self.row = row
        self.col = col
        self.data = data
    
    def get(self, index: int):
        if self.col == 1:
            return self.get_row(index)[0]
        else:
            return self.get_col(index)[0]
    
    def set(self, index: int, value: int):
        if self.col == 1:
            self.data[index][0] = value
        else:
            self.data[0][index] = value

    def copy(self):
        new_vector = Vector(self.row, self.col, self.data.copy())
        return new_vector

class Table:
    def __init__(self, supply: Vector, demand: Vector, costs: Matrix):
        self.supply = supply
        self.demand = demand
        self.costs = costs
        self.final_cost = 0

    def fullfill(self, row: int, col: int) -> int:
        supply = self.supply.get(row)
        demand = self.demand.get(col)

        cost = self.costs.get(row, col)

        paid = cost * supply
        amounnt_diff = demand - supply

        if amounnt_diff < 0:
            paid -= amounnt_diff * cost
            self.demand.set(col, 0)
            self.supply.set(row, -amounnt_diff)
            self.final_cost += paid
            return -amounnt_diff
        else:
            self.demand.set(col, amounnt_diff)
            self.supply.set(row, 0)
            self.final_cost += paid
            return amounnt_diff

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
supply = Vector(1, 3, supply_data)
supply.transpose()

demand_data = [[60, 70, 120, 130, 100]]
demand = Vector(1, 5, demand_data)

costs_data = [[2, 3, 4, 2, 4], 
              [8, 4, 1, 4, 1], 
              [9, 7, 3, 7, 2]]
costs = Matrix(3, 5, costs_data)

table = Table(supply, demand, costs)

table_nw = Table(supply, demand, costs)
table_nw.fullfill(0, 0)
table_nw.display()
# Correct answer for North-West algorithm: 3230

# print("Answer done by North-West algorithm:")
# table_nw.north_west()

table_v = Table(supply, demand, costs)
# Correct answer for Vogel's algorithm: 1330

# print("Answer done by Vogel's algorithm:")
# table_v.vogel()

table_r = Table(supply, demand, costs)
# Correct answer for Russel's algorithm: idk

# print("Answer done by Russel's algorithm:")
# table_r.russel()
