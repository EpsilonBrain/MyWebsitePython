#!/usr/bin/env python
# coding: utf-8

# In[1]:


def primelist(n):
    A = [True] * (n + 1)
    plist = []
    for i in range(2, int(n ** .5) + 1):
        if A[i]:
            k = 0
            j = i ** 2
            while j <= n:
                A[j] = False
                k += 1
                j = i ** 2 + i * k
    for i in range(2, n + 1):
        if A[i]:
            plist.append(i)
    return(plist)


# In[2]:


def ndig(num):
    return len(str(num))


def get_dig(num):
    num_str = str(num)
    n = len(num_str)
    dig_list = [0] * n
    for i in range(n):
        dig_list[i] = int(num_str[i])
    return dig_list


def list_to_int(dig_list):
    m = len(dig_list)
    run_str =''
    for i in range(m):
        run_str += str(dig_list[i])
    return int(run_str)


def last_dig(num):
    return get_dig(num)[len(get_dig(num)) - 1]


def not_last(num):
    if len(str(num)) == 1:
        return num
    return list_to_int(get_dig(num)[0:len(get_dig(num)) - 1])


def rest_and_last(num):
    digs = get_dig(num)
    L = len(digs)
    if L == 1:
        return (0, num)
    else:
        return (list_to_int(digs[0:L - 1]), get_dig(num)[L - 1])


# In[3]:

def rule_end(p):
    strp = str(p)
    return " If this number is divisble by " + strp + " then the original is divisble by " + strp + "."


def rule_make(num, op, p):
    if op == "add":
        long_str = "Multiply the last digit by " + str(num) + ", " + op + " it to the rest of the number"
    if op == "subtract":
        long_str = long_str = "Multiply the last digit by " + str(num) + ", " + op + " it from the rest of the number"
    return long_str + '. ' + rule_end(p)


def div_rule_gen(p):
    #this assumes p prime is greater than 7
    #dig_list = get_dig(p)
    #get the last digit
    #last = dig_list.pop()
    #get the rest of the digits
    #it is either 1, 3, 7, or 9
    (num, op) = get_special(p)
    return rule_make(num, op, p)


def get_special(num):
    #it is assumed that num is prime
    digs = get_dig(num)
    last = digs[len(digs) - 1]
    spec = 3 * num
    if num in [3, 9]:
        return (1, "add")
    if last == 1:
        return (not_last(num), "subtract")
    if last == 3:
        return (not_last(spec) + 1, "add")
    if last == 7:
        return(not_last(spec), "subtract")
    if last == 9:
        return (not_last(num) + 1, "add")


plist = primelist(10 ** 6)


# In[7]:


def last_dig_op(n, mult, op, p):
    (rest, last) = rest_and_last(n)
    return abs(what_op(op, rest, mult * last))


# In[8]:


def nice_str(truth):
    if not truth:
        return "not"
    else:
        return ""


# In[9]:


def what_op(op, a, b):
    if op == "add":
        return a + b
    else:
        return a - b


# In[10]:


def spec_three(n):
    tot = n
    while ndig(tot) > 1:
        tot = sum(get_dig(tot))
    while tot >= 3:
        tot -= 3
    return tot


# In[13]:


def is_div(n, p):
    l = last_dig(n)
    if p == 2:
        return l in [0, 2, 4, 6, 8]
    if p == 3:
        return spec_three(n) == 0
    if p == 5:
        return l in [0, 5]
    (spec, op) = get_special(p)
    x0 = last_dig_op(n, spec, op, p)
    roll = [x0] * 3
    if x0 < p:
        return False
    count = 0
    while True:
        roll[0] = roll[2]
        for i in range(2):
            roll[i + 1] = last_dig_op(roll[i], spec, op, p)
            if 0 < roll[i + 1] < p:
                return False
        if roll[2] == roll[0]:
            return True
        count += 1
        if count > 10:
            return False


def factor(n, plist):
    bound = n ** .5
    i = 0
    p_fac = []
    if n not in plist:
        while plist[i] <= bound:
            p = plist[i]
            i += 1
            if is_div(n, p):
                p_fac.append(p)
                return p_fac + factor(n // p, plist)
    else:
        return [n]


def prime_fac(n, plist):
    n = abs(n)
    if n == 1:
        return 1
    p_facs = factor(n, plist)
    dist_ps = len(set(p_facs))
    pow_list = [0] * dist_ps
    #count how many p's there are in p_facs
    j = 0
    i = 0
    while i < len(p_facs):
        p = p_facs[i]
        #that will be the exponent
        count = p_facs.count(p)
        pow_list[j] = [p, count]
        i += count
        j += 1
    return pow_list
        #put it in pow_list and move on to the next prime that is not p
        # keep doing this till the end of the list



def nice_latex(fact):
    run_str = ''
    for pairs in fact:
        run_str += print_exp(pairs)
    return run_str[:-5]


# In[21]:


def print_exp(pair):
    (p, a) = pair
    return str(p) + '^' + str(a) + '\cdot'

plist = primelist(10 ** 6)


def pow_of(n, fac):
    power = 0
    while is_div(n, fac):
        n //= fac
        power += 1
    return (power, n)



def fac_two_five(n):
    two_pow = 0
    five_pow = 0
    (five_pow, new_n) = pow_of(n, 5)
    (two_pow, odd_n) = pow_of(new_n, 2)
    return (two_pow, five_pow, odd_n)


def two_or_five_rule(n, two_or_five):
    #n is a pure power of 2 or 5 that is not 1
    (two_pow, odd) = pow_of(n, two_or_five)
    strn = str(n)
    return 'If the last ' + str(two_pow) + ' digits are divisible by ' + strn + ' then the number is divisible by ' + strn + '.'


#check if two or five go into it
def better_gen(n):
    n = abs(n)
    if n == 1:
        return 'Every integer is divisible by 1'
    #get the powers
    (two_pow, odd_n) = pow_of(n, 2)
    #you need cases for if it is a straight power of two or if it is a straight power of 5
    #if it is one of these then you just call the method gives you the rule for 2 or 5
    strn = str(n)
    rule = ''
    if two_pow != 0:
        two_part = 2 ** two_pow
        two_part_str = str(two_part)
        rule += 'To be divisible by ' + two_part_str + ': ' + two_or_five_rule(two_part, 2)
        if odd_n != 1:
            rule += '\n'
        else:
            return rule
    (five_pow, odd_n) = pow_of(odd_n, 5)
    if five_pow != 0:
        five_part = 5 ** five_pow
        five_part_str = str(five_part)
        rule += 'To be divisible by ' + five_part_str + ': ' + two_or_five_rule(five_part, 5)
        if odd_n != 1:
            rule += '\n'
        else:
            return rule
    rule += 'To be divisible by ' + str(odd_n) + ': ' + div_rule_gen(odd_n)
    #we are going to have cases
    #In order to be divisible by n, the number needs to be divisible by
        #two power
        #five power
        #and odd power
    #if we have made it this far either
        #the number has no factors of 2 or 5
    start = 'In order to be divisible by ' + strn + ' the number must be divisible by '
    if two_pow == 0 and five_pow == 0:
        return rule
    #the number has factors of 2 and 5 and something else
    if two_pow != 0 and five_pow != 0:
        start += two_part_str + ', ' + five_part_str + ','
    #the number has factors of exactly one of 2 or 5 and something else
    elif two_pow != 0:
        start += two_part_str
    elif five_pow != 0:
        start += five_part_str
    start += ' and ' + str(odd_n)
    return start + '.\n' + rule
    #get the rule associated for the powers of two or five (write a method for this)
    #get what is left if there is anything left
    #run the normal rule generator on it
    #boom you have your division rule
