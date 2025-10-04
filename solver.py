import scipy
import sys

import scipy.optimize


def get_data(data):
    data = data.split('\n') 
    data_obj = data[0]
    data_cons = data[1:]
    
    # Get all variables
    obj_neg = (-1 if data_obj.strip().partition("=")[0] == 'max' else 1)
    data_obj_processed = data_obj.strip().partition("=")[2].split("+")
    variables = [item.partition("*")[2] if ("*" in item) else item for item in data_obj_processed]
    
    # Get coefficients of variables in objective function
    obj_coefficients = [float(item.partition("*")[0])*obj_neg if ("*" in item) else obj_neg for item in data_obj_processed]
    
    # Get coefficients of variables and bounds in constraints
    cons_coefficients = list()
    cons_bounds = list()
    for data_con in data_cons:
        if ">=" in data_con:
            deli = ">="
        elif "<=" in data_con:
            deli = "<="
        else:
            raise "Illegal constraint format"
        
        data_con_processed = data_con.strip().partition(deli)
        
        # Bound 
        bound = float(data_con_processed[2])
        
        # Coefficients
        coefficients = list()
        data_con_processed2 = data_con_processed[0].split("+")
        temp_dict = {item.split("*")[-1]: float(item.split("*")[0]) if "*" in item 
                     else 1 
                     for item in data_con_processed2}
        for var in variables:
            coefficient = 0
            if var not in temp_dict:
                coefficient = 0
            else:
                coefficient = temp_dict[var]
            
            coefficients.append(coefficient)
        
        # Multiply -1 when it is ">="
        if deli == ">=":
            bound *= -1
            for i in range(len(coefficients)):
                coefficients[i] *= -1
        
        
        cons_bounds.append(bound)
        cons_coefficients.append(coefficients)
    
    return (obj_coefficients, cons_coefficients, cons_bounds)


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
            print(f"x{i}={round(x, 2)}", end="")
        print(f", min z={round(result.fun, 2) * (-1 if my_str[:3]=='max' else 1)}")

def main():
    global my_str
    obj_ce, cons_ce, cons_b = get_data(my_str)
    result = solve(obj_ce, cons_ce, cons_b)
    show(result)
    
            
if __name__ == "__main__":
    main()
