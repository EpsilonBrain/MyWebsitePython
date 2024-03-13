#!/usr/bin/env python
# coding: utf-8

# In[235]:


import numpy as np
from math import *


# In[236]:


def make_grid(n):
    non_arr = [0] * n
    for i in range(n):
        non_arr[i] = "?"
        non_arr = np.array(non_arr)
    non_grid = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        k = 0
        for j in range(n):
            non_grid[i][j] = non_arr[k]
            k += 1
    return non_grid


# In[237]:


def column(matrix, i):
    return [row[i] for row in matrix]


def replace_col(matrix, i, new_col):
    for j in range(len(new_col)):
        matrix[j][i] = new_col[j]
    return matrix


# In[240]:


def is_good(group_list, n):
    dim = len(group_list)
    good_nums = [False] * dim
    for i in range(dim):
        num = group_list[i]
        test = n - sum(group_list) + num - dim + 1
        if num > floor(test / 2):
            good_nums[i] = True
    return good_nums


# In[241]:


def whats_left_list(group_list, n):
    # see which numbers are good
    dim = len(group_list)
    good_list = is_good(group_list, n)
    space_list = [(0, 0)] * dim
    # get the space needed for each one
    for i in range(dim):
        if good_list[i]:
            x = group_list[i]
            rem = n - (sum(group_list) - x + dim - 1)
            # make a coordinate with the entries being
            # how much is on the edges
            # how much is guaranteed)
            space_list[i] = (rem - x, 2 * x - rem)
    return space_list


# In[242]:


def sum_ind(a_list, ind):
    run_sum = 0
    for i in range(ind):
        run_sum += a_list[i]
    return run_sum + ind


# In[243]:


def fill_in_row(in_row, group_list, n):
    dim = len(group_list)
    space_list = whats_left_list(group_list, n)
    if space_list == [(0, 0)] * dim:
        return in_row
    else:
        for i in range(dim):
            if space_list[i] != (0, 0):
                (space, amt) = space_list[i]
                # if it is first in the list then you only need to go over the space
                if i == 0:
                    over_this_much = space
                else:
                    over_this_much = sum_ind(group_list, i) + space
                for j in range(amt):
                    in_row[over_this_much + j] = "*"
    return in_row


# In[244]:


def guaranteed_squares(row_col_list):
    # row col list will have length 2n where n is the dimension
    n = len(row_col_list) // 2
    # make the grid
    grid = make_grid(n)
    # run each row and each column through the fill in row
    # first do the rows
    for i in range(n):
        grid[i] = fill_in_row(grid[i], row_col_list[i], n)
    for j in range(n):
        # Get the current column from grid
        col = column(grid, j)
        # get the group information for that column
        group_list = row_col_list[j + n]
        # run that through fill in row
        replace_col(grid, j, fill_in_row(col, group_list, n))
    return grid


# In[245]:


# reindeer = [[1, 1, 1, 1], [7], [1], [9], [4, 5], [9], [9], [9], [5], [4],
# [3], [5], [5], [2, 5], [1, 1, 3], [2, 6], [1, 7], [10], [1, 7], [2, 2, 3]
# ]


# In[246]:


def check_grid(grid, row_col_list):
    new_grid = grid.copy()
    prev_grid = 0
    n = len(row_col_list) // 2
    k = 0
    while new_grid != prev_grid:
        prev_grid = new_grid.copy()
        for i in range(n):
            new_grid[i] = is_done(new_grid[i], row_col_list[i])[0]
        for j in range(n):
            new_col = column(new_grid, j)
            replace_col(new_grid, j, is_done(new_col, row_col_list[j + n])[0])
        k += 1
        if k > 20:
            return "Too Big, Oh no"
    return new_grid


# In[247]:


# read stuff in between x's as if it is its own row
# look at if there is anything shaded in there.
# figure out which group it is a part of
# section out the part of that group
# figure out what else could possibly go there


# In[248]:
def row_reader(row):
    # takes in a row and looks at how many groups there are
    # probably a lot of the code in is_done will help
    m = len(row)
    cur_group_info = []
    # find the first * and store that
    star_count = row.count("*")
    # make sure there are actually stars
    if star_count == 0:
        return [0]
    else:
        # find the first place a star occurs
        star_ind = row.index("*")
        # fill out cur_group_info with j as the runnning index
        # initialize running total to count the total number of stars
        run_total = 0
        while star_ind < m:
            # run groupsize to count the number of stars in a group
            # put this number into cur_group_info
            size = OG_groupsize(star_ind, row)
            cur_group_info.append(size)
            # increase the running total to make sure we don't get too big
            run_total += size
            # move star index over to the next star after this group ends
            if run_total == star_count:
                break
            else:
                star_ind = row.index("*", star_ind + size)
        return cur_group_info


# Check to see if a row is done
def is_done(row, group_info):
    # get the length of the row so you don't go out of range
    m = len(row)
    # initialize the list you'll compare in the end
    cur_group_info = [0] * len(group_info)
    # find the first * and store that
    star_count = row.count("*")
    # make sure there are actually stars
    cur_group_info = row_reader(row)
    # compare to see if the two lists are the same (they won't be the same likely,
    # I don't know how to deal with this right now
    final_bool = cur_group_info == group_info
    # if they are the same return true and fill in the ? with X's
    if final_bool:
        row = ["X" if x == "?" else x for x in row]
    # if they are not the same, return false and X out the ones that are complete.
    return row, final_bool


# In[249]:


# def a count after function to count the number of elements after a certain index
def count_after(alist, ind, element):
    splice_list = alist[0: ind + 1]
    return alist.count(element) - splice_list.count(element)


# get the groupsize by counting the question marks that surround it
def groupsize(start, row):
    # assume start is the index of the 'first' star
    # the last question mark is then right before start i.e. ques_ind = start - 1
    # get index of first question mark after the star
    dim = len(row)
    star_ind = row.index("*", start)
    # see if there are any ? or X's after this star
    is_ques = count_after(row, star_ind, "?") != 0
    is_X = count_after(row, star_ind, "X") != 0
    if not is_X and not is_ques:
        return dim - star_ind
    else:
        if is_X and is_ques:
            fin_ques = min(row.index("X", star_ind), row.index("?", star_ind))
            return fin_ques - star_ind
        if is_X:
            fin_ques = row.index("X", star_ind)
        if is_ques:
            fin_ques = row.index("?", star_ind)
        # count how many stars there are in that range
        # this amount is fin_ques - (ques_ind + 1) = fin_ques - start
        return fin_ques - star_ind


# In[250]:


def OG_groupsize(start, row):
    dim = len(row)
    star_ind = row.index("*", start)
    i = star_ind
    while row[i] == "*":
        i += 1
        if i >= dim:
            break
    return i - star_ind


# In[251]:


# horse = [
# [1, 1], [4], [2, 1, 1], [3, 1], [10], [7], [7], [8], [1, 1, 1, 1], [1, 1, 1, 1],
# [2, 1], [5, 3], [1, 5], [10], [4], [4], [6], [4], [5], [3, 1]
# ]

# In[252]:


# a method to fill in a row if it is backed against a wall
def border(grid, row_col_list):
    # first is the case where it is a top row
    n = len(grid)
    dim = len(row_col_list) // 2
    toprow = grid[0]
    botrow = grid[dim - 1]
    firstcol = column(grid, 0)
    lastcol = column(grid, dim - 1)
    # get index of the first shaded
    # assuming there is a star in the border
    star_change = toprow.index("*")
    run_star = 0
    star_count = toprow.count("*")
    while run_star < star_count:
        # get the size of the shaded group in the row
        # write a for loop to do that group
        size = OG_groupsize(star_change, toprow)
        for i in range(size):
            # get the group info and get the amount that needs to be shaded
            over = star_change + i
            # how much it needs to go down for top row
            amt = get_grouplist(over, row_col_list, True)[0]
            # get the column
            col = column(grid, over)
            # fill in the column using fix fill
            replace_col(grid, over, fill_fix(col, 0, amt, True))
            # move on to the next one
        run_star += size
        if run_star < star_count:
            star_change = toprow.index("*", star_change + size)
    return grid


# In[253]:


# a method to fill in a row if it is backed against a wall
def new_border(grid, row_col_list):
    # first is the case where it is a top row
    dim = len(grid)
    toprow = grid[0]
    botrow = grid[dim - 1]
    firstcol = column(grid, 0)
    lastcol = column(grid, dim - 1)
    # get index of the first shaded
    # assuming there is a star in the border
    grid1 = something(grid, toprow, True, True, row_col_list)
    grid2 = something(grid1, botrow, False, True, row_col_list)
    # transpose and run the two again
    trans_grid = trans(grid2)
    tgrid1 = something(trans_grid, firstcol, True, False, row_col_list)
    tgrid2 = something(tgrid1, lastcol, False, False, row_col_list)
    return trans(tgrid2)


# In[254]:


def something(grid, row, is_down, is_row, row_col_list):
    run_star = 0
    star_count = row.count("*")
    if star_count != 0:
        star_change = row.index("*")
        while run_star < star_count:
            # get the size of the shaded group in the row
            # write a for loop to do that group
            size = OG_groupsize(star_change, row)
            for i in range(size):
                # get the group info and get the amount that needs to be shaded
                over = star_change + i
                # how much it needs to go down for top row
                group_list = get_grouplist(over, row_col_list, is_row)
                # if we are filling downward we need the first element of the grouplist
                if is_down:
                    el = 0
                else:
                    el = len(group_list) - 1
                amt = group_list[el]
                # get the column
                col = column(grid, over)
                # fill in the column using fix fill
                replace_col(grid, over, fill_fix(col, el, amt, is_down))
                # move on to the next one
            run_star += size
            if run_star < star_count:
                star_change = row.index("*", star_change + size)
        else:
            return grid
    return grid


# In[255]:


def trans(sq_matrix):
    trans_mat = []
    dim = len(sq_matrix)
    for i in range(dim):
        trans_mat.append(column(sq_matrix, i))
    return trans_mat


# In[256]:


# something to fill in a set amount of squares then adds an x
def fill_fix(in_row, start, amt, is_down):
    dim = len(in_row)
    if is_down:
        start_amt = start + amt
        for i in range(start, start_amt):
            in_row[i] = "*"
        if start_amt < dim:
            in_row[start_amt] = "X"
    else:
        for i in range(amt):
            in_row[dim - i - 1] = "*"
        qty = dim - amt - 1
        if qty >= 0:
            in_row[qty] = "X"
    return in_row


# In[257]:


# something that gets the grouplist from a certain element in a border row
def get_grouplist(ind, row_col_list, is_row):
    # it is assumed the index is the index of the star
    # if it is in a row then go to that index and return in it in row_col_list
    if is_row:
        return row_col_list[ind + len(row_col_list) // 2]
    else:
        return row_col_list[ind]
    # if it is in a column, add the dimension to the index and return that


# In[258]:


# rein = check_grid(guaranteed_squares(reindeer), reindeer)

# In[259]:


# santa_hat = [
# [3], [2, 1], [5], [4], [6], [8], [8], [1, 1], [1, 6, 1], [8],
# [2], [2, 1], [3, 2], [5, 2], [6, 2], [7, 2], [1, 5, 2], [3, 3, 2], [2, 1], [2]
# ]

# In[260]:


# santa = guaranteed_squares(santa_hat)

# In[261]:


# check_grid(new_border(santa, santa_hat), santa_hat)

# In[262]:


# lmao = check_grid(guaranteed_squares(reindeer), reindeer)


# In[263]:


# something that takes out a chunk and replaces it


# In[384]:


def print_nice(grid):
    # run list_to_nice on all the rows to get nice strings
    # make a string with \n at the end of each row
    n = len(grid)
    long_str = "  "
    for i in range(n):
        long_str += " " + str(i) + " "
    long_str += "\n"
    for j in range(len(grid)):
        long_str += str(j) + " " + list_to_nice(grid[j])
    return print(long_str)


# In[265]:


def list_to_nice(row):
    # row either has x's, *'s, or ?'s.
    # If it is a question mark, replace it with a space
    # If it is an X, leave it
    # If it is a star, fill it with your favorite unicode symbol
    run_str = ""
    for i in range(len(row)):
        if row[i] == "?":
            run_str += "   "
        if row[i] == "X":
            run_str += " X "
        if row[i] == "*":
            run_str += " ■ "
    run_str += "\n"
    return run_str


# In[266]:


# print_nice(rein)

# In[267]:


# print_nice(check_grid(new_border(rein, reindeer), reindeer))


# In[268]:


# in order to understand X's I need
# something that reads in a row, looks at the group information,
def what_could_it_be(row, group_info):
    if row.count("*") == 0:
        return row
    else:
        # get the index
        first_ind = row.index("*")
        size = OG_groupsize(0, row)
        # get the group size and compare it to the group info


# then sees what filled in squares could be/what it is
# once it knows what that group is take that snippet between X's
# run fill in row as if the whole row was just that chunk


# In[269]:


# a method to check and see if the first shaded square is part of the first group in that row
def is_first(row, group_info):
    len_row = len(row)
    len_group = len(group_info)
    first = group_info[0]
    if row.count("*") == 0:
        return (row, False)
    else:
        first_star = row.index("*")
        size = OG_groupsize(0, row)
        # see if there is only one number in that row,
        # if there is, x around it and return the row
        if len_group == 1:
            return group_of_one(row, group_info)
        # else, see if that group could be the second number by seeing if there is room for
        # one more than the first group (to account for the x) can fit behind the star
        else:
            # this means that it could be the first one or not
            if first + 1 <= first_star:
                return (row, False)
            else:
                # this means it is the first one for sure
                # if the first element is a one, X around it
                if first == 1:
                    if first_star - 1 >= 0:
                        row[first_star - 1] = "X"
                    if first_star + 1 < len_row:
                        row[first_star + 1] = "X"
                # if it is not a one then X what you can before it
                else:
                    leftover = first - size
                    down_ind = first_star - leftover - 1
                    return x_down
                    # hush
        # it may be useful to have an is_connected method to see if two groups
        # side by side can be connected


# In[270]:


# write something that makes the puzzle
# takes in the dimension
# gets some random numbers and uses it to fill in rows with stugg
# stick the rows together to make a grid
# now write something that reads the row and column information
# then returns it
# boom, infinite examples
# ok but some of them mught not have unique answers I don't know how to deal with that quite yet


# In[271]:


def group_of_one(row, group_info):
    if row.count("*") == 0:
        return (row, False)
    else:
        first = group_info[0]
        first_star_ind = row.index("*")
        size = OG_groupsize(0, row)
        whats_left = first - size
        # go up whats left and then X everything above that
        down_ind = first_star_ind - whats_left - 1
        if down_ind >= 0:
            row = x_down(row, down_ind)
        # go down whats left and X everything below that
        up_ind = first_star_ind + whats_left + 1
        if up_ind < len(row):
            row = x_up(row, up_ind)
        return (row, True)


# In[272]:


def x_down(row, ind):
    mov_ind = ind
    while mov_ind >= 0:
        row[mov_ind] = "X"
        mov_ind -= 1
    return row


def x_up(row, ind):
    row.reverse()
    new_ind = len(row) - ind - 1
    filled = x_down(row, new_ind)
    filled.reverse()
    return filled


# In[ ]:


# In[ ]:


# In[273]:


import random as r


# In[363]:


def rand_row(n):
    # takes in the length of the row and
    # returns it filled in with the row information
    row = ["?"] * n
    # pick a certain amount of space over to start at
    space_over = r.randint(0, n)
    # if it is n, return the empty row with [0]
    group = []
    # if space_over == n then space_left = -1 which is not > 0
    space_left = n - (space_over + 1)
    if space_left <= 0:
        return (row, [0])
    while space_left > 0:
        # pick a size for the group
        group_size = r.randint(1, space_left)
        group.append(group_size)
        # fill it in
        for j in range(group_size):
            row[space_over + j] = "*"
        space_over = group_size + 1 + space_over
        space_left = n - (space_over)
        # see whats left and repeat
    return (row, group)


# In[294]:


def puzzle_gen(n):
    grid = make_grid(n)
    group_info = [[]] * (2 * n)
    for i in range(n):
        # generate n random rows
        # get their group info into a list
        (grid[i], group_info[i]) = rand_row(n)
    for j in range(n):
        # strip the columns
        col = column(grid, j)
        group_info[j + n] = row_reader(col)
        # put the columns in the same list
    # return the picture and the group information
    print_nice(grid)
    return group_info


# In[475]:


# puzzle = puzzle_gen(10)
# print_nice(all_meths(puzzle))


# In[467]:


# the next thing is to get the spaces and look at them
# either spaces between X's or just space in general
# see if something can go there
# or identify which numbers can go where


# In[468]:


def all_meths(group_info):
    return new_border(check_grid(guaranteed_squares(group_info), group_info), group_info)

# In[ ]:
