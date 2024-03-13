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
    return (plist)


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
    run_str = ''
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
        return list_to_int(digs[0:L - 1]), digs[L - 1]


def spec_three(n):
    tot = n
    while ndig(tot) > 1:
        tot = sum(get_dig(tot))
    while tot >= 3:
        tot -= 3
    return tot

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


def rule_end(p):
    strp = str(p)
    return " If this number is divisble by " + strp + " then the original is divisble by " + strp + "."


def div_rule_gen(p):
    if p == 2:
        return "If the last digit is 0, 2, 4, 6, or 8 then the number is divisible by 2. Equivalently, if the last digit is divisble by 2 then the number is divisble by 2."
    if p == 3:
        return "Add all the digits." + rule_end(p)
    if p == 5:
        return "If the last digit is 5 or 0 then the number is divisble by 5. Equivalently, if the last digit is divisble by 5 then the number is divisble by 5."
    if p < 11 or int(p) != p or is_div(p, 2) or is_div(p, 5):
        return str(p) + " is not a prime number."
    #dig_list = get_dig(p)
    # get the last digit
    #last = dig_list.pop()
    # get the rest of the digits
    # it is either 1, 3, 7, or 9
    try:
        (num, op) = get_special(p)
    except:
        return "Error"
    return rule_make(num, op, p)
divisible

# In[4]:


def rule_make(num, op, p):
    if op == "add":
        long_str = "Multiply the last digit by " + str(num) + ", " + op + " it to the rest of the number."
    if op == "subtract":
        long_str = "Multiply the last digit by " + str(num) + ", " + op + " it from the rest of the number."
    return long_str + rule_end(p)


# In[ ]:


# In[5]:


def get_special(num):
    # it is assumed that num is prime
    digs = get_dig(num)
    last = digs[len(digs) - 1]
    spec = 3 * num
    nl = not_last(num)
    nl_spec = not_last(spec)
    if last == 1:
        return (nl, "subtract")
    if last == 3:
        return (nl_spec + 1, "add")
    if last == 7:
        return (nl_spec, "subtract")
    if last == 9:
        return (nl + 1, "add")

# In[ ]:


# In[7]:


plist = primelist(10 ** 6)


# In[8]:


def last_dig_op(n, mult, op, p):
    (rest, last) = rest_and_last(n)
    return abs(what_op(op, rest, mult * last))


# In[10]:


def what_op(op, a, b):
    if op == "add":
        return a + b
    else:
        return a - b

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
        # keep doing this till the end of the list]


def print_exp(pair):
    (p, a) = pair
    return str(p) + '^' + str(a) + ' '


def nice_latex(fact):
    run_str = ''
    for pairs in fact:
        run_str += print_exp(pairs)
    return run_str[:-1]

def whole_ass_generator(n):
    p_fact = prime_fac(n, plist)
    run_str = ''
    start = 'In order to be divisible by ' + str(n) + ' the number must be divisible by '
    dist_ps = len(p_fact)
    is_small = False
    if dist_ps == 2:
        is_small = True
        start += str(p_fact[0][0] ** p_fact[0][1]) + ' and ' + str(p_fact[1][0] ** p_fact[1][1]) + '.'
    for pairs in p_fact:
        (p, a) = pairs
        if not is_small:
            if p_fact.index(pairs) != len(p_fact) - 1:
                start += str(p ** a) + ', '
            else:
                start += 'and ' + str(p ** a) + '.'
        run_str += 'To be divisible by ' + str(p ** a) + ': ' + div_rule_gen(p ** a) + '\n'
    run_str = run_str[:-1]
    if dist_ps == 1:
        return run_str
    else:
        return start + '\n' + run_str