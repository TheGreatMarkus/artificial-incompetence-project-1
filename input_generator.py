from random import randrange

import numpy

from utils import flip_token, grid_to_string

n = 10
moves = 8
grid = numpy.zeros(shape=(n, n), dtype=int)
for row, col in numpy.ndindex(grid.shape):
    grid[row, col] = 0

for i in range(moves):
    row = randrange(n)
    col = randrange(n)
    flip_token(grid, row, col)

print(grid)
print('{} {} 5000 {}'.format(n, moves + 1, grid_to_string(grid).replace(' ', '')))
