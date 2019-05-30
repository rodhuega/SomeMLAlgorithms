
import sys
import math
import matplotlib.pyplot as plt

muestras = {}
muestrasActivas={}


def introducirDatos():
    global muestras,clasificadores,muestrasActivas
    vDimension= int(input("Dimension de los vectores: "))
    continuar=True
    while continuar:
        nombre = input("Nombre de la muestra: ")
        nuevaMuestra = {}
        i = 1
        while i<=vDimension:
            nuevoValor= float(input(("Valor para "+str(i)+": ")))
            nuevaMuestra["z"+str(i)]=nuevoValor
            i+=1
        clase = int(input("Introduzca clase(+1,-1)"))
        nuevaMuestra["clase"]=clase
        muestras[nombre]=nuevaMuestra
        continuarQuery= input("Y si quiere introducir otra muestra: ")
        if continuarQuery.lower()!='y':
            continuar=False
        muestrasActivas=dict(muestras)

def plotear():
    global muestrasActivas
    plt.show()
    for keyMuestra in muestrasActivas:
        valorX=muestrasActivas[keyMuestra]["z1"]
        valorY=muestrasActivas[keyMuestra]["z2"]
        clase=muestrasActivas[keyMuestra]["clase"]
        strClase = 'go'
        if clase == -1:
            strClase='bo'
        plt.plot(valorX,valorY,strClase)
        plt.annotate(keyMuestra,(valorX,valorY))
    plt.show()

def CalculoL1(muestra1, muestra2):
    i=1
    resultado=0
    while i<len(muestra1):
        valor1 = muestra1["z"+str(i)]
        valor2 = muestra2["z"+str(i)]
        resultado+=math.fabs(valor2-valor1)
        i+=1
    print(resultado)
    return resultado

def CalculoL2(muestra1, muestra2):
    i=1
    resultado=0
    while i<len(muestra1):
        valor1 = muestra1["z"+str(i)]
        valor2 = muestra2["z"+str(i)]
        resultado+=(valor2-valor1)**2
        i+=1
    resultado=math.sqrt(resultado)
    print(resultado)
    return resultado

def CalculoL0(muestra1, muestra2):
    i=1
    resultado=0
    while i<len(muestra1):
        valor1 = muestra1["z"+str(i)]
        valor2 = muestra2["z"+str(i)]
        resultadoProvisional=math.fabs(valor2-valor1)
        if resultadoProvisional>resultado:
            resultado=resultadoProvisional
        i+=1
    print(resultado)
    return resultado

def main():
    global muestras,muestrasActivas
    muestras = {'x1': {'z1': 3.0, 'z2': 3.0, 'clase': -1}, 'x2': {'z1': 1.0, 'z2': 1.0, 'clase': 1}}
    muestrasActivas=dict(muestras)
    #introducirDatos()
    print(muestras)
    plotear()

if __name__ == "__main__":
    main()