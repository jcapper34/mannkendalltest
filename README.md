# mannkendalltest
Simple Python functions for Mann Kendall and Seasonal Kendall Tests
## **Dependencies**
You must have the following installed:
- [numpy](https://github.com/numpy/numpy)
- [scipy](https://github.com/scipy/scipy)

## **Functions**
All functions return a named tuple containing:
- *s*: the S statistic
- *var_s*: the variance of S
- *z*: the Z-score associated with S statistic. 
- *p*: the probability value. Area under normal curve

**Mann Kendall Test**  
*mk_test(vals)*
- Parameters:
    - *vals*: set of data to analyze. Must be in chronological order


**Seasonal Kendall Test**  
*sk_test(vals)*
- Parameters:
    - *vals*: set of data to analyze. Must be in chronological order
    - *period*: number of seasons contained in data. Default is 12 (Eg 12 months in a year)