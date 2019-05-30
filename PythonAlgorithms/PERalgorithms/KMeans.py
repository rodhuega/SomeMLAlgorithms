
import sys
import math
import matplotlib.pyplot as plt

muestras1 = {}
muestrasActivas1={}
muestras2 = {}
muestrasActivas2={}


def introducirDatos():
    global muestras1,muestras2,clasificadores,muestrasActivas1,muestrasActivas2
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
        if clase==-1:
            muestras2[nombre]=nuevaMuestra
        else:
            muestras1[nombre]=nuevaMuestra
        
        continuarQuery= input("Y si quiere introducir otra muestra: ")
        if continuarQuery.lower()!='y':
            continuar=False
        muestrasActivas1=dict(muestras1)
        muestrasActivas2=dict(muestras2)

def plotear():
    global muestrasActivas1,muestrasActivas2
    plotearClase(muestrasActivas1,'bo')
    plotearClase(muestrasActivas2,'co')
    plotearFrontera(muestrasActivas1,muestrasActivas2)
    plt.show()

def plotearFrontera(muestrasClase1,muestrasClase2):
    muestrasCombinadas = {**muestrasClase1, **muestrasClase2}
    listaX=[]
    listaY=[]
    for keyC1 in muestrasCombinadas:
        dMin=1000000
        cMin=""
        keyMin=""
        muestra1=muestrasCombinadas[keyC1]
        clase1 = muestra1["clase"]
        listaXTemporal=[]
        listaYTemporal=[]
        for keyC2 in muestrasCombinadas:
            if keyC1!=keyC2:
                muestra2=muestrasCombinadas[keyC2]
                clase2 = muestra2["clase"]
                distanciaActual = CalculoL2(muestra1,muestra2)
                if (distanciaActual<dMin and clase1!=clase2 ):
                    dMin=distanciaActual
                    keyMin=keyC2
                    (xp,yp)=CalculoPuntoMedio(muestra1,muestra2)
                    listaXTemporal=[]
                    listaYTemporal=[]
                    listaXTemporal.append(xp)
                    listaYTemporal.append(yp)
                elif (distanciaActual==dMin and clase1!=clase2 ):
                    (xp,yp)=CalculoPuntoMedio(muestra1,muestra2)
                    listaXTemporal.append(xp)
                    listaYTemporal.append(yp)
                elif (distanciaActual<dMin and clase1==clase2 ):
                    listaXTemporal=[]
                    listaYTemporal=[]
                    dMin=distanciaActual
                    keyMin=keyC2
        listaX.extend(listaXTemporal)    
        listaY.extend(listaYTemporal)    
        resMuestra = muestrasCombinadas[keyMin]
        #if clase1!=resMuestra["clase"]:
        #    (xp,yp)=CalculoPuntoMedio(muestra1,resMuestra)
        #    plt.plot(xp,yp,'ro')
    plt.plot(listaX,listaY,'ro')



def plotearClase(muestras,strClase):
        for keyMuestra in muestras:
            valorX=muestras[keyMuestra]["z1"]
            valorY=muestras[keyMuestra]["z2"]
            clase=muestras[keyMuestra]["clase"]
            strClase = 'go'
            if clase == -1:
                strClase='bo'
            plt.plot(valorX,valorY,strClase)
            plt.annotate(keyMuestra,(valorX,valorY))
def CalculoL1(muestra1, muestra2):
    i=1
    resultado=0
    while i<len(muestra1):
        valor1 = muestra1["z"+str(i)]
        valor2 = muestra2["z"+str(i)]
        resultado+=math.fabs(valor2-valor1)
        i+=1
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
    return resultado

def CalculoPuntoMedio(muestra1, muestra2):
    x1=muestra1["z1"]
    x2=muestra2["z1"]
    y1=muestra1["z2"]
    y2=muestra2["z2"]
    x= (x1+x2)/2
    y=(y1+y2)/2
    return x,y

def main():
    global muestras1,muestrasActivas1,muestras2,muestrasActivas2
    muestras1 = {'x1': {'z1': 0.0, 'z2': 0.0, 'clase': -1}, 'x3': {'z1': 1.0, 'z2': 2.0, 'clase': -1}
                , 'x5': {'z1': 0.0, 'z2': 1.0, 'clase': -1}, 'x7': {'z1': 2.0, 'z2': 3.0, 'clase': -1}, 'x8': {'z1': 3.0, 'z2': 2.0, 'clase': -1}
                , 'x10': {'z1': 4.0, 'z2': 0.0, 'clase': -1}, 'x12': {'z1': 4.0, 'z2': 1.0, 'clase': -1}}
    muestras2 = {'x2': {'z1': 1.0, 'z2': 0.0, 'clase': 1},'x4': {'z1': 1.0, 'z2': 1.0, 'clase': 1}
                , 'x6': {'z1': 2.0, 'z2': 2.0, 'clase': 1}
                , 'x9': {'z1': 3.0, 'z2': 0.0, 'clase': 1}, 'x11': {'z1': 3.0, 'z2': 1.0, 'clase': 1}
                , 'x13': {'z1': 2.0, 'z2': 0.0, 'clase': 1}, 'x14': {'z1': 2.0, 'z2': 1.0, 'clase': 1}}
    muestrasActivas1=dict(muestras1)
    muestrasActivas2=dict(muestras2)
    #introducirDatos()
    plotear()

if __name__ == "__main__":
    main()