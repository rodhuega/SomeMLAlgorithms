import sys
import numpy as np
import math

def main():
    matriz = np.zeros((4,4));
    
    X=[[1,0],[1,1],[-1,0],[0,0]]
    i=0
    while i<len(X):
        j=0
        Vi=np.array(X[i])
        while j<len(X):
            Vj=np.array(X[j])
            resta= Vi-Vj
            mult= np.dot(resta.transpose(),resta)
            matriz[i][j]=(-1)*mult
            j+=1
        i+=1
    print(matriz)

if __name__ == "__main__":
    sys.exit(int(main() or 0))
