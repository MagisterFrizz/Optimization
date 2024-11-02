import numpy as np
from numpy.linalg import norm, inv
from simplex import preprocess_and_simplex

x_0 = np.array([1, 1, 6, 4], float) 
A = np.array([[1, 2, 1, 0] ,[2, 1, 0, -1]], float)  
c = np.array([1, 1, 0, 0], float)  

def IPA(A, c, x_0, alpha=0.5, e=1e-04):
    SHAPE = A.shape[1]

    x = x_0.copy()

    while True:
        D = np.diag(x)

        A_tild = np.dot(A, D)
        A_tild_t = np.transpose(A_tild)
        c_tild = np.dot(D, c)

        I = np.eye(SHAPE)

        try:
            # P = I - A^T(AA^T)^-1A
            P = I - np.dot((np.dot(A_tild_t, inv(np.dot(A_tild, A_tild_t)))), A_tild)
        except:
            print("The method is not applicable!")
            exit(0)

        cp = np.dot(P, c_tild)
        
        if (np.min(cp) < 0): 
            nu = np.abs(np.min(cp))
        else:
            print("The problem does not have solution!")
            exit(0)
        
        x_tild = np.add(np.ones(SHAPE, float), (alpha / nu) * cp)
        x_star = np.dot(D, x_tild)

        if norm(np.subtract(x_star, x), ord=2) < e: 
            break

        x = x_star

    print(f"\nVector x = {np.round(x, 2)}")
    return np.dot(c, x)

print("For alpha(0.5):", round(IPA(A, c, x_0, 0.5), 2))
print("For alpha(0.9):", round(IPA(A, c, x_0, 0.9), 2))
print("Answer of Simplex:")
preprocess_and_simplex()