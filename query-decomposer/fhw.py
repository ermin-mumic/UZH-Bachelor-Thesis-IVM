from scipy.optimize import linprog


def compute_fhw(bags, edges):
    table_names = list(edges.keys())
    k = len(table_names)

    c = [1.0] * k                  # objective: minimize sum of all lambdas (weight per relation/hyperedge)
    bounds = [(0.0, 1.0)] * k     #  0 <= lambda_i <= 1

    max_rho = 0.0 # max fractional edge cover number

    for bag_vars in bags.values(): # solve linprog for every bag to find its min fractional edge cover number
        # one constraint row per variable in this bag:
        # -sum of lambda_i where x in R_i <= -1   (negated >= 1 constraint)
        A_ub = []
        b_ub = []
        for var in bag_vars:
            row = [-1.0 if var in edges[t] else 0.0 for t in table_names]
            A_ub.append(row)
            b_ub.append(-1.0)

        result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)

        if result.success:
            max_rho = max(max_rho, result.fun)

    return round(max_rho, 4)
