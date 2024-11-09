import math

class Matrix:
    def __init__(self, row: int, col: int, data=[]):
        self.row = row
        self.col = col
        self.data = data

    def get_row(self, index: int) -> list[type[int]]:
        """
        Returns appropriate row in type of array
        """
        return self.data[index]
    
    def get_col(self, index: int) -> list[type[int]]:
        """
        Returns appropriate column in type of array
        """
        col = []
        for i in range(self.row):
            col.append(self.data[i][index])
        return col
    
    def transpose(self) -> None:
        """
        Transposes matrix
        """
        new_data = []
        for i in range(self.col):
            new_data.append(self.get_col(i))
        self.row, self.col = self.col, self.row
        self.data = new_data

    def get(self, row: int, col: int) -> int:
        """
        Returns value at appropriate position
        """
        return self.data[row][col]
    
    def set(self, row: int, col: int, val: int) -> None:
        """
        Sets value at appropriate position
        """
        self.data[row][col] = val

    def copy(self):
        """
        Returns copy of matrix
        """
        new_matrix = Matrix(self.row, self.col, self.data.copy())
        return new_matrix

    # Helpful methods for Vogel and Russel

    def get_minimum_difference(self, geom: int, index: int):
        """
        This method returns the value of difference between two smallest elements in row/column
        geom: 0 for row, 1 for column
        """
        if geom == 0:
            row = sorted(self.get_row(index))
            if row[0] == math.inf:
                return -math.inf
            elif row[1] == math.inf:
                return 0
            else:
                return row[1] - row[0]
        else:
            col = sorted(self.get_col(index))
            if col[0] == math.inf:
                return -math.inf
            elif col[1] == math.inf:
                return 0
            else:
                return col[1] - col[0]
    
    def get_minimum(self, geom: int, index: int):
        """
        Returns indeces of minimum element in appropriate row/column
        """
        if geom == 0:
            row = min(self.get_row(index))
            index2 = self.get_row(index).index(row)
            return [index, index2]
        else:
            col = min(self.get_col(index))
            index2 = self.get_col(index).index(col)
            return [index2, index]
            
    def get_maximum(self, geom: int, index: int):
        """
        Returns indeces of maximum element in appropriate row/column
        """
        if geom == 0:
            row = max(self.get_row(index))
            index2 = self.get_row(index).index(row)
            return [index, index2]
        else:
            col = max(self.get_col(index))
            index2 = self.get_col(index).index(col)
            return [index2, index]
        
    def get_max_cell_in_row(self, index: int):
        maximum_value = max(self.get_row(index))
        return index, self.get_row(index).index(maximum_value), maximum_value

    def get_max_cell_in_col(self, index: int):
        maximum_value = max(self.get_col(index))
        return self.get_col(index).index(maximum_value), index, maximum_value

    def compute_delta_for_cells(self, cell: list, max_row: int, max_col: int):
        return self.get_row(cell[0]).index(cell[1]) - max_row - max_col

class Vector(Matrix):
    def __init__(self, row: int, col: int, data=[]):
        self.row = row
        self.col = col
        self.data = data
    
    def get(self, index: int):
        """
        Returns value at appropriate position
        """
        if self.col == 1:
            return self.get_row(index)[0]
        else:
            return self.get_col(index)[0]
    
    def set(self, index: int, value: int):
        """
        Sets value at appropriate position
        """
        if self.col == 1:
            self.data[index][0] = value
        else:
            self.data[0][index] = value

    def copy(self):
        """
        Returns copy of vector
        """
        new_vector = Vector(self.row, self.col, self.data.copy())
        return new_vector

class Table:
    def __init__(self, supply: Vector, demand: Vector, costs: Matrix):
        self.supply = supply
        self.demand = demand
        self.costs = costs
        self.final_cost = 0

    def fullfill(self, row: int, col: int, setinf: bool=False) -> int:
        """
        This method tries to transport as most supply as it can by using
        cost at cell (i, j)
        """
        supply = self.supply.get(row)
        demand = self.demand.get(col)

        cost = self.costs.get(row, col)

        if setinf:
            self.costs.set(row, col, math.inf)

        paid = cost * supply
        amounnt_diff = demand - supply

        if amounnt_diff < 0:
            paid -= -amounnt_diff * cost
            self.demand.set(col, 0)
            self.supply.set(row, -amounnt_diff)
            self.final_cost += paid
            if setinf:
                for i in range(self.costs.row):
                    self.costs.set(i, col, math.inf)
            return amounnt_diff
        else:
            self.demand.set(col, amounnt_diff)
            self.supply.set(row, 0)
            self.final_cost += paid
            if setinf:
                for i in range(self.costs.col):
                    self.costs.set(row, i, math.inf)
            return amounnt_diff

    def display(self) -> None:
        """
        This method displays whole table with current demands and supplies
        """
        print("The table:")
        for i in range(self.costs.row):
            print(self.costs.get_row(i) + self.supply.get_row(i))
        print(self.demand.get_row(0), "\n")
        

    def north_west(self) -> None:
        """
        Implementation of North-West algorithm
        """
        i, j = 0, 0
    
        while True:
            try:
                diff = self.fullfill(i, j)
                if diff < 0:
                    j += 1
                elif diff == 0:
                    i += 1
                    j += 1
                else:
                    i += 1
            except:
                break
        
        print("Final Cost:", self.final_cost)
    
    def vogel(self):
        """
        Implementation of Vogel's algorithm
        """
        for _ in range(self.costs.row + self.costs.col - 1):
            differences_row = []
            differences_col = []
            
            for i in range(self.costs.row):
                differences_row.append(self.costs.get_minimum_difference(0, i))

            for j in range(table.costs.col):
                differences_col.append(self.costs.get_minimum_difference(1, j))

            # print("Differences(row/col):", differences_row, differences_col)

            if max(differences_col) < max(differences_row):
                index = self.costs.get_minimum(0, differences_row.index(max(differences_row)))
                self.fullfill(index[0], index[1], True)
            else:
                index = self.costs.get_minimum(1, differences_col.index(max(differences_col)))
                self.fullfill(index[0], index[1], True)

            # print("Chosen index:", index)
            # self.display()

            # print("Current Cost:", self.final_cost, "\n")

        print("Final Cost:", self.final_cost)
    
    def russel(self):
        """
        Implementation of Russel's algorithm
        """
        maximum_row_values_arr = []
        maximum_col_values_arr = []

        visited_cells = set()
        delta_matrix = [[0 for i in range(len(self.demand.data[0]))] for j in range(len(self.supply.data))]

        for i in range(len(self.supply.data)):
            max_cell = self.costs.get_max_cell_in_row(i)
            maximum_row_values_arr.append(max_cell[2])
            visited_cells.add((max_cell[0], max_cell[1]))

        for i in range(len(self.demand.data[0])):
            max_cell = self.costs.get_max_cell_in_col(i)
            maximum_col_values_arr.append(max_cell[2])
            visited_cells.add((max_cell[0], max_cell[1]))

        for i in range(len(self.supply.data)):
            for j in range(len(self.demand.data[0])):
                if (i, j) not in visited_cells:
                    delta = self.costs.get_row(i)[j] - maximum_row_values_arr[i] - maximum_col_values_arr[j]
                    delta_matrix[i][j] = delta
                    
        while True:
            min_value = 0
            min_index = (0,0)
            for i in range(len(self.supply.data)):
                for j in range(len(self.demand.data[0])):
                    if delta_matrix[i][j] < min_value:
                        min_value = delta_matrix[i][j]
                        min_index = (i,j)
            if min_value == 0:
                break
            else:
                self.fullfill(min_index[0], min_index[1])
                if self.supply.data[min_index[0]][0] == 0:
                    for i in range(len(self.demand.data[0])):
                        delta_matrix[min_index[0]][i] = 0
                if self.demand.data[0][min_index[1]] == 0:
                    for i in range(len(self.supply.data)):
                        delta_matrix[i][min_index[1]] = 0

        print("Final Cost:", self.final_cost)
    
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



table.display()

while True:
    algo = int(input("""Plese, enter the number of algorithm to use: 
(0 - North-West, 1 - Vogel's, 2 - Russel's)\n"""))
    if algo == 0:
        table_nw = Table(supply, demand, costs)
        # Correct answer for North-West algorithm: 1380

        print("Answer done by North-West algorithm:")
        table_nw.north_west()
        input()
        break
    elif algo == 1:
        table_v = Table(supply, demand, costs)
        # Correct answer for Vogel's algorithm: 1260

        print("Answer done by Vogel's algorithm:")
        table_v.vogel()
        input()
        break
    elif algo == 2:
        table_r = Table(supply, demand, costs)
        # Correct answer for Russel's algorithm: 900

        print("Answer done by Russel's algorithm:")
        table_r.russel()
        input()
        break
    else:
        print("Please, enter either 1, 2, or 3\n")
