import scipy
import sys

import scipy.optimize
from functools import reduce

variables = []
is_minimize = bool()

def parse(data):
    def parse_expression(expr: str) -> dict:
        ''' Parse out the coefficients and variables of an expression.
            e.g. '2*x1-3*x2-x3+x4' -> {'x1': 2, 'x2': -3, 'x3': -1, 'x4': 1}
        '''
        expr = expr.replace('-', '+-')
        partitions = expr.split('+')
        result = dict()
        for partition in partitions:
            if '*' in partition: # Conditions like 2*x, -2*y
                coefficient, variable = partition.split('*')
                coefficient = float(coefficient)
            else:
                if '-' in partition: # Conditions like -x, -y
                    variable = partition.replace('-', '')
                    coefficient = -1
                else: # Conditions like x, y
                    variable = partition
                    coefficient = 1
            result[variable] = coefficient
        return result

    global variables, is_minimize
    data = data.split('\n') 
    data_obj = data[0]
    data_cons = data[1:]
    
    # Get coefficients and variables in object expression
    direction, obj_expr = data_obj.strip().split('=')
    is_minimize = (direction == 'min')
    obj_negative = (1 if is_minimize else -1)
    obj_dict = parse_expression(obj_expr)

    variables = list(obj_dict)
    obj_coefficients = list( map(lambda x: obj_negative*x, obj_dict.values()) )
    
    # Get coefficients of variables and bounds in constraints
    all_constraint_coefficients = list()
    all_constraint_bounds = list()
    for data_con in data_cons:
        if ">=" in data_con:
            deli = ">="
        elif "<=" in data_con:
            deli = "<="
        elif ">" in data_con:
            deli = ">"
        elif "<" in data_con:
            deli = "<"
        else:
            raise "Illegal constraint format"
        
        constraint_expr, bound = data_con.strip().split(deli)
        
        # Bound 
        bound = float(bound)
        
        # Coefficients
        coefficients = list()
        constraint_dict = parse_expression(constraint_expr)
        coefficients = [
            constraint_dict[var] if var in constraint_dict else 0
            for var in variables
        ]

        # Multiply -1 when it is ">=" or ">"
        if deli in (">=", ">"):
            bound *= -1
            coefficients = [-x for x in coefficients]
        
        
        all_constraint_bounds.append(bound)
        all_constraint_coefficients.append(coefficients)
    
    return (obj_coefficients, all_constraint_coefficients, all_constraint_bounds)


def solve(obj_ce, constraint_ce, constraint_b):
    result = scipy.optimize.linprog(
        obj_ce,
        A_ub=constraint_ce,
        b_ub=constraint_b
    )
    return result

def show(result):
    if result.success:
        count = 0
        for i, x in enumerate(result.x):
            count += x
            if i != 0:
                print("; ", end="")
            print(f"{variables[i]}={round(x, 2)}", end="")
        print(f", {'min' if is_minimize else 'max'} z={round(result.fun, 2) * (1 if is_minimize else -1)}")
    else:
        print('There\'s no solution to this problem')

def main():
    global my_str
    obj_ce, cons_ce, cons_b = parse(my_str)
    result = solve(obj_ce, cons_ce, cons_b)
    show(result)
    
            
if __name__ == "__main__":
    main()
