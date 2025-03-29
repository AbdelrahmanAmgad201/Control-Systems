import numpy as np

def routh_criteria(coeffs, n):
    """
    Determines system stability using Routh-Hurwitz Criterion.
    
    Parameters:
        coeffs (list): Coefficients of the characteristic polynomial (highest power first).
        n (int): Order of the polynomial.
        
    Returns:
        dict: 
            - 'message': Indicates if the system is stable or not.
            - 'matrix': Routh array.
            - 'poles': Unstable poles (if system is not stable).
    """
    
    cols = (n + 1) // 2 +1
    routh_array = np.zeros((n+1, cols))
    
    
    for j in range(cols):
        if 2*j < len(coeffs):
            routh_array[0, j] = coeffs[2*j]
        if 2*j+1 < len(coeffs):
            routh_array[1, j] = coeffs[2*j+1]
    

    for i in range(2, n+1):
        
        if abs(routh_array[i-1, 0]) < 1e-10 and np.any(abs(routh_array[i-1, 1:]) > 1e-10):   
            routh_array[i-1, 0] = 1e-10
        
        elif np.all(abs(routh_array[i-1, :]) < 1e-10):
           
            degree = n - i + 2  
            aux_poly = []
            for j in range(cols):
                if abs(routh_array[i-2, j]) > 1e-10:
                    power = degree - 2*j
                    if power >= 0:
                        aux_poly.append((power, routh_array[i-2, j]))
            
            
            aux_poly.sort(reverse=True)
            
           
            der_coeffs = []
            for power, coef in aux_poly:
                if power > 0:  
                    der_coeffs.append((power-1, power * coef))
            
            for j in range(len(der_coeffs)):
                if j < cols:
                    idx = (degree - 1 - der_coeffs[j][0]) // 2
                    if 0 <= idx < cols:
                        routh_array[i-1, idx] = der_coeffs[j][1]
        
        for j in range(cols-1):
            a = routh_array[i-2, 0]
            b = routh_array[i-2, j+1] if j+1 < cols else 0
            c = routh_array[i-1, 0]
            d = routh_array[i-1, j+1] if j+1 < cols else 0
            
            if abs(c) >= 1e-10:
                routh_array[i, j] = -(a*d - b*c)/c
    
  
    first_column = routh_array[:, 0]
    
    nonzero_elems = [elem for elem in first_column if abs(elem) > 1e-10]
    
    
    sign_changes = 0
    for i in range(1, len(nonzero_elems)):
        if nonzero_elems[i-1] * nonzero_elems[i] < 0:
            sign_changes += 1
    
    if sign_changes == 0:
        return {"message": "The system is stable.", "matrix": routh_array, "poles": []}
    else:
        poles = np.roots(coeffs)
        unstable_poles = [p for p in poles if np.real(p) > 0]
        return {"message": "The system is unstable.", "matrix": routh_array, "poles": unstable_poles}