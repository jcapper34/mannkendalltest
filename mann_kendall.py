import scipy.stats as st
from collections import namedtuple
from math import sqrt

## Seasonal Kendall Test ##
def sk_test(vals, alpha=0.05, period=12):
    s_prime = 0
    total_variance = 0
    for season in range(period):
        s, variance = mk_test(vals[season::period], alpha=alpha, get_z=False)
        s_prime += s
        total_variance += variance

    z = calc_z(s_prime, total_variance)
    p = st.norm.cdf(z)

    Mann_Kendall = namedtuple("Mann_Kendall", ['s', 'var_s', 'z', 'p'])
    return Mann_Kendall(s_prime, total_variance, z, 1-p)

## Mann-Kendall Test ##
def mk_test(vals, alpha=0.05, get_z=True):
    s, ties = calc_s(vals)
    variance = var_s(len(vals), ties)

    if not get_z:
        return s, variance

    z = calc_z(s, variance)
    p = st.norm.cdf(z) # Obtain area under normal curve
    conclusion = interpret_z(z, p, alpha)

    Mann_Kendall = namedtuple("Mann_Kendall", ['s', 'var_s', 'z', 'p', 'conclusion'])
    return Mann_Kendall(s, variance, z, 1-p, conclusion)

## Calculate S Statistic ##
def calc_s(vals):
    n = len(vals)
    s = 0
    ties = {}
    for k in range(n-1):
        for j in range(k+1, n):
            sign = sgn(vals[j] - vals[k])
            if sign == 0:
                ties[vals[k]] = ties.get(vals[k], 0) + 1
            s += sign

    return s, list(ties.values())

## Calculate Variance of S statistic ##
def var_s(n, ties):
    def v(x):
        return x*(x-1)*(2*x+5)
    total = v(n)
    for tie in ties:
        total += v(tie)

    return total/18

## Calculate Z Score from S and VAR(S) ##
def calc_z(s, variance):
    if not s:
        return 0

    return (s-sgn(s))/sqrt(variance)

## Form a conclusion ##
def interpret_z(z, p, alpha):
    conclusion = "No"
    if p > 1-alpha:
        if z > 0:
            conclusion = 'an increasing'
        else:
            conclusion = 'a decreasing'
    return "There is %s Trend" % conclusion

## Sign function ##
def sgn(n):
    if n == 0:
        return 0
    return n/abs(n)