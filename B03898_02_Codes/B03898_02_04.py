""""
README
======
This file contains Python codes.
======
"""

""" An example of implementing an IP model with binary conditions  """
import pulp

dealers = ["X", "Y", "Z"]
variable_costs = {"X": 500,
                  "Y": 350,
                  "Z": 450}
fixed_costs = {"X": 4000,
               "Y": 2000,
               "Z": 6000}

# Define PuLP variables to solve
quantities = pulp.LpVariable.dicts("quantity",
                                   dealers,
                                   lowBound=0,
                                   cat=pulp.LpInteger)
is_orders = pulp.LpVariable.dicts("orders", dealers,
                                  cat=pulp.LpBinary)

"""
This is an example of implementing an IP model with binary
variables the wrong way.
"""
# Initialize the model with constraints
model = pulp.LpProblem("A cost minimization problem", pulp.LpMinimize)
model += sum([(variable_costs[i] * quantities[i] +
               fixed_costs[i]) * is_orders[i] for i in dealers]), \
         "Minimize portfolio cost"
model += sum([quantities[i] for i in dealers]) == 150, \
         "Total contracts required"
model += 30 <= quantities["X"] <= 100, \
         "Boundary of total volume of X"
model += 30 <= quantities["Y"] <= 90, \
         "Boundary of total volume of Y"
model += 30 <= quantities["Z"] <= 70, \
         "Boundary of total volume of Z"
model.solve() # Will encounter an error