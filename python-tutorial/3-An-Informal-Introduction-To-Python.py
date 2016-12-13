# -*- coding: utf-8 -*-


# this is the first comment
spam = 1  # and this is the second comment
          # ... and now a third!
text = "# This is not a comment because it's inside quotes."


# Arithmetic
1 + 1         # 2
1 + 2 * 3     # 7
(2 - 1) / 3   # 3
17 / 3        # 5.666666666666667 float number
17 // 3       # 5, floor division
17 % 3        # 2, remainder
2 ** 18       # 1024


# Variables
w = 20
h = 5 * 9
area = w * h  # 900


# Strings
single_qoutes = 'let\'s go "hiking"\n'
double_qoutes = "let's go 'hiking'\n"
single_or_double_qoutes_multi_line = """\
    Usage: ps [OPTIONS]
        -e
        -f\
"""
repeated_string = 3 * 'foo'  # foofoofoo
concated_string = 'hello,' + ' world'
multi_line_text = (
    'Put several strings within parentheses '
    'to have them joined together.'
)
get_char_by_index = 'hello'[0]  # h
out_of_range = 'hello'[99]      # raise exception


# Lists
squares = [1, 4, 9, 16, 25]
squares += [36, 49, 64, 81]
squares[:]   # copy
squares[0]   # 0
squares[-1]  # -1
squares[-3:] # -3, -2, -1

cubes = [1, 8, 27]
cubes.append(4 ** 3)

letters = ['a', 'b', 'c']
letters[1:2] = ['B', 'C']

len(letters)
