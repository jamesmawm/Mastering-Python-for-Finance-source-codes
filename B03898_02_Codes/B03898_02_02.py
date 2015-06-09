"""
README
======
This is a Python code.
======
"""

""" Least squares regression with statsmodels """
import numpy as np
import statsmodels.api as sm

# Generate some sample data
num_periods = 9
all_values = np.array([np.random.random(8)
                       for i in range(num_periods)])

# Filter the data
y_values = all_values[:, 0]  # First column values as Y
x_values = all_values[:, 1:]  # All other values as X

x_values = sm.add_constant(x_values)  # Include the intercept
results = sm.OLS(y_values, x_values).fit()  # Regress and fit the model

print results.summary()
print results.params
