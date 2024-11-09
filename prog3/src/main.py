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
        
    def get_russel_number(self, row: int, col: int, taboo_rows: list, taboo_cols: list):
        """
        Returns cost of cell - max cost in row - max cost in col
        (For Russel's algorithm implementation)
        """
        chosen_row = self.get_row(row)
        for taboo_col in taboo_cols:
            chosen_row[taboo_col] = 0

        chosen_col = self.get_col(col)
        for taboo_row in taboo_rows:
            chosen_col[taboo_row] = 0

        row_maxima = max(chosen_row)
        col_maxima = max(chosen_col)

        cell_cost = self.get(row, col)
        return cell_cost - row_maxima - col_maxima
    

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
        self.points = []

    def fullfill(self, row: int, col: int, setval: int=-1) -> int:
        """
        This method tries to transport as most supply as it can by using
        cost at cell (i, j)
        """
        supply = self.supply.get(row)
        demand = self.demand.get(col)

        cost = self.costs.get(row, col)

        if setval != -1:
            self.costs.set(row, col, setval)

        paid = cost * supply
        amounnt_diff = demand - supply

        self.points.append([row, col, min([demand, supply])])

        if amounnt_diff < 0:
            paid -= -amounnt_diff * cost
            self.demand.set(col, 0)
            self.supply.set(row, -amounnt_diff)
            self.final_cost += paid

            if setval != -1:
                for i in range(self.costs.row):
                    self.costs.set(i, col, setval)
            return amounnt_diff
        elif amounnt_diff > 0:
            self.demand.set(col, amounnt_diff)
            self.supply.set(row, 0)
            self.final_cost += paid
            if setval != -1:
                for i in range(self.costs.col):
                    self.costs.set(row, i, setval)
            return amounnt_diff
        else:
            self.demand.set(col, 0)
            self.supply.set(row, 0)
            if setval != -1:
                for i in range(self.costs.col):
                    self.costs.set(row, i, setval)
                for i in range(self.costs.row):
                    self.costs.set(i, col, setval)
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

        if sum(self.supply.get_col(0)) != sum(self.demand.get_row(0)):
            print("The problem is not balanced!")
            input()
            exit(0)

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
        print("Points used (row, col, amount):", self.points)
    
    def vogel(self):
        """
        Implementation of Vogel's algorithm
        """

        if sum(self.supply.get_col(0)) != sum(self.demand.get_row(0)):
            print("The problem is not balanced!")
            input()
            exit(0)

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
                self.fullfill(index[0], index[1], math.inf)
            else:
                index = self.costs.get_minimum(1, differences_col.index(max(differences_col)))
                self.fullfill(index[0], index[1], math.inf)

            # print("Chosen index:", index)
            # self.display()

            # print("Current Cost:", self.final_cost, "\n")

        print("Final Cost:", self.final_cost)
        print("Points used (row, col, amount):", self.points)
    
    def russel(self):
        """
        Implementation of Russel's algorithm
        """

        if sum(self.supply.get_col(0)) != sum(self.demand.get_row(0)):
            print("The problem is not balanced!")
            input()
            exit(0)

        taboo_rows = []
        taboo_cols = []

        for _ in range(self.costs.row + self.costs.col - 1):
            minimal_rn = math.inf
            minimal_ri = [0, 0]

            for row in range(self.costs.row):
                for col in range(self.costs.col):
                    if row not in taboo_rows and col not in taboo_cols:
                        russel_number = self.costs.get_russel_number(row, col, taboo_rows, taboo_cols)
                        if minimal_rn > russel_number:
                            minimal_rn = russel_number
                            minimal_ri = [row, col]
            
            var = self.fullfill(minimal_ri[0], minimal_ri[1])

            if var < 0:
                taboo_cols.append(minimal_ri[1])
            elif var > 0:
                taboo_rows.append(minimal_ri[0])
            else:
                taboo_cols.append(minimal_ri[1])
                taboo_rows.append(minimal_ri[0])

        print("Final Cost:", self.final_cost)
        print("Points used (row, col, amount):", self.points)


# For Testing
supply_data = [[140, 160, 120]]
supply = Vector(1, 3, supply_data)
supply.transpose()

demand_data = [[110, 150, 80, 80]]
demand = Vector(1, 4, demand_data)

costs_data = [[55, 30, 45, 25], 
              [65, 40, 35, 20], 
              [30, 60, 50, 40]]
costs = Matrix(3, 4, costs_data)

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
