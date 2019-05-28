import numpy as np
from py_expression_eval import Parser
import sys

parse = Parser()
kernelMatrix = None
muestras ={};
alfas=[]


def introducirDatos():
    global kernelMatrix,alfas,muestras
    nAlfas=int(input("Numero de muestras: "))
    i=0
    while i<nAlfas:
        nombreMuestra = input("Nombre de la muestra: ")
        claseMuestra =int(input("Clase de la muestra: "))
        muestras[nombreMuestra]=claseMuestra
        alfas,append(float(input(("Valor del alfa de la muestra"+ nombreMuestra+": "))))
        i+=1
    filas=int(input("Numero de filas: "))
    columnas=int(input("Numero de columnas: "))
    kernelMatrix = np,zeros((filas,columnas))
    i=0
    while i<filas:
        j=0
        while j<columnas:
            kernelMatrix[i,j]=float(input(("Valor de "+ str(i)+ ", "+str(j)+": ")))
            j+=1
        i+=1
    print("Alfas: ")
    print(alfas)
    print("Matriz introducida: ")
    print(kernelMatrix)
    print("Muestras: ")
    print(muestras)


def kernelPerceptron():
    global kernelMatrix,alfas,muestras
    continuar=True
    muestrasBienClasificadas=0
    clasificador=""
    rondasTotales=0
    while continuar:
        print("Rondas totales: "+ str(rondasTotales))
        i=0
        for keyMuestra in muestras.keys():
            clase = muestras[keyMuestra]
            clasificadorPreparado= clasificador.replace("$",str(i))
            if clasificador!="":
                valGx=eval(clasificadorPreparado)
            else:
                valGx=0
            print("Resultado de clasificar "+ keyMuestra+ ": " + str(valGx))
            if valGx*clase<=0:
                alfas[i]+=1
                if clasificador!="":
                    clasificador+="+"
                clasificador+="("+str(clase)+")*kernelMatrix["+str(i)+",$]+("+str(clase)+")"
            else:
                muestrasBienClasificadas+=1
            print("Resultados de la iteracion: " +str(i))
            print("Alfas: ")
            print(alfas)
            print("Clasificador: "+clasificador)
            i+=1
        continuar = input("Continuar? y si: ")
        if (muestrasBienClasificadas==len(alfas) or (continuar.lower!="y")):
            continuar=False

def main():
    #introducirDatos()
    global muestras,kernelMatrix,alfas
    muestras={'x1': 1, 'x2': 1, 'x3': 1, 'x4': -1, 'x5': -1, 'x6': -1}
    kernelMatrix=np.array([[ 1,  1,  1,  1,  1,  1],
 [ 1,  4,  1,  0,  4,  9],
 [ 1,  1,  4,  0,  4,  4],
 [ 1,  0,  0,  9,  1,  4],
 [ 1,  4,  4,  1,  9, 16],
 [ 1,  9,  4,  4, 16, 36]])
    alfas=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    kernelPerceptron()

if __name__ == "__main__":
    sys,exit(int(main() or 0))
