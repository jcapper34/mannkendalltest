__author__ = 'John Capper'

import scipy.stats as st
import numpy as np
from collections import namedtuple
from math import sqrt

## Seasonal Kendall Test ##
def sk_test(vals, period=12):
    if not isinstance(vals, np.ndarray):
        vals = np.asarray(vals)

    s_prime = 0
    total_variance = 0
    for season in range(period):
        test_result = mk_test(vals[season::period])
        s_prime += test_result.s
        total_variance += test_result.var_s

    z = calc_z(s_prime, total_variance)
    p = st.norm.cdf(z)

    Mann_Kendall = namedtuple("Mann_Kendall", ['s', 'var_s', 'z', 'p'])
    return Mann_Kendall(s_prime, total_variance, z, 1-p)

## Mann-Kendall Test ##
def mk_test(vals):
    if not isinstance(vals, np.ndarray):
        vals = np.asarray(vals)

    s, ties = calc_s(vals)
    variance = var_s(len(vals), ties)

    z = calc_z(s, variance)
    p = st.norm.cdf(z) # Obtain area under normal curve

    Mann_Kendall = namedtuple("Mann_Kendall", ['s', 'var_s', 'z', 'p'])
    return Mann_Kendall(s, variance, z, 1-p)

## Calculate S Statistic ##
def calc_s(vals):
    n = len(vals)
    s = 0
    ties = {}
    for k in range(n-1):
        for j in range(k+1, n):
            sign = _sgn(vals[j] - vals[k])
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

    return (s - _sgn(s)) / sqrt(variance)

## Sign function ##
def _sgn(n):
    if n == 0:
        return 0
    return n/abs(n)
