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
    return list_to_int(get_dig(num)[0:len(get_dig(num)) - 1])


def rest_and_last(num):
    digs = get_dig(num)
    L = len(digs)
    if L == 1:
        return (0, num)
    else:
        return list_to_int(digs[0:L - 1]), digs[L - 1]


# In[3]:


def div_rule_gen(p):
    # this assumes p prime is greater than 7
    dig_list = get_dig(p)
    # get the last digit
    last = dig_list.pop()
    # get the rest of the digits
    # it is either 1, 3, 7, or 9
    (num, op) = get_special(p)
    return rule_make(num, op, p)


# In[4]:


def rule_make(num, op, p):
    if op == "add":
        long_str = "Multiply the last digit by " + str(num) + ", " + op + " it to the rest of the number"
    if op == "subtract":
        long_str = long_str = "Multiply the last digit by " + str(num) + ", " + op + " it from the rest of the number"
    return long_str


# In[ ]:


# In[5]:


def get_special(num):
    # it is assumed that num is prime
    digs = get_dig(num)
    last = digs[len(digs) - 1]
    spec = 3 * num
    if last == 1:
        return (not_last(num), "subtract")
    if last == 3:
        return (not_last(spec) + 1, "add")
    if last == 7:
        return (not_last(spec), "subtract")
    if last == 9:
        return (not_last(num) + 1, "add")


# In[ ]:


# In[7]:


a_plist = primelist(1000)
plist = a_plist[4: len(a_plist) - 1]


# In[8]:


def last_dig_op(n, mult, op, p):
    (rest, last) = rest_and_last(n)
    return red_mod_p(abs(what_op(op, rest, mult * last)), p)


# In[9]:


def red_mod_p(n, p):
    k = 0
    while n - k * p >= p:
        k += 1
    return n - k * p


# In[10]:


def what_op(op, a, b):
    if op == "add":
        return a + b
    else:
        return a - b


# In[93]:


def div_rule(n, p):
    if n < p:
        return False
    (spec, op) = get_special(p)
    # make a while condition to stop if it cycles or if it gets back to the original number
    x0 = last_dig_op(n, spec, op, p)
    roll = x0
    if x0 == 0:
        return True
    count = 0
    while last_dig_op(roll, spec, op, p) != x0:
        roll = last_dig_op(roll, spec, op, p)
        if roll == 0:
            return True
        count += 1
        if count >= p:
            # print("Got too big so", n // p == n / p)
            return False
    return False


# In[89]:


import random as r

# In[122]:

def nice_str(truth):
    if not truth:
        return "not"
    else:
        return ""


n = r.randint(1, 10000)
L = len(plist)
ind = r.randint(1, L - 1)
print("n = ", n)
p = plist[ind]
print("p = ", p)
print(str(n) + " is " + nice_str(div_rule(n, p)) + " divisible by " + str(p))