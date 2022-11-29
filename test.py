digit_pos = {
    7: (1, 1), 
    8: (1, 2), 
    9: (1, 3),
    4: (2, 1), 
    5: (2, 2), 
    6: (2, 3),
    1: (3, 1), 
    2: (3, 2), 
    3: (3, 4),
    0: (4, 2), 
    '.': (4, 1),
    'c': (4, 3)
}
# find the largest row and filter to get the highest column in that row
max_row = max([x[0] for x in digit_pos.values()])
max_col = max([x[1] for x in digit_pos.values() if x[0] == max_row])


print(max_row, max_col)