#!/usr/bin/env python3

my_list = [120, 330, 431, 113, 13, 2, 1123]


def highest_even(number_list):
    highest = 0
    for number in number_list:
        if not(number % 2) and number > highest:
            highest = number
    return(highest)


print(highest_even(my_list))
