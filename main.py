import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class OperationalPlanningProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=4,  # Adjust this according to the number of variables
                         n_obj=2,  # Two objectives: Minimize cost, Maximize coverage
                         n_constr=2,  # Two constraints: Production capacity, Demand satisfaction
                         xl=np.array([0, 0, 0, 0]),  # Lower bounds for each variable
                         xu=np.array([100, 100, 100, 100]))  # Upper bounds for each variable

    # x represents the array of decision variables
    def _evaluate(self, x, out, *args, **kwargs):
        production = x[0]
        purchasing = x[1]
        sales = x[2]
        inventory = x[3]
        # Example cost calculation (simplified)
        production_cost = production * 5
        purchasing_cost = purchasing * 4
        holding_cost = inventory * 2
        total_cost = production_cost + purchasing_cost + holding_cost

        # Example coverage (simplified)
        coverage = sales
        # Set objectives
        out["F"] = [total_cost, -coverage]  # Minimize cost, maximize coverage (hence -coverage)

        # Example constraints
        capacity_constraint = production - 80  # Example: plant capacity of 80
        demand_constraint = 100 - sales  # Example: demand of 100

        # Set constraints (must be <= 0)
        out["G"] = [capacity_constraint, demand_constraint]


problem = OperationalPlanningProblem()

algorithm = NSGA2(pop_size=100)

res = minimize(problem,
               algorithm,
               ('n_gen', 100),
               verbose=True,
               seed=1)

print("Solutions: ", res.X)
print("Objective values: ", res.F)
