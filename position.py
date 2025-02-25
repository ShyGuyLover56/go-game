class Position:
    def __init__(self, row, col):
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError
        self.row = row
        self.col = col

    def __str__(self):
        output = f'Placed Go Game piece at [{self.row}, {self.col}]'
        return output	
