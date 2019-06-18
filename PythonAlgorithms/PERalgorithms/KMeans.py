
import sys
import math
import operator
import pandas as pd
import matplotlib.pyplot as plt

muestras1 = {}
muestrasActivas1={}
muestras2 = {}
muestrasActivas2={}
vDimension=0

def introducirMuestra():
    global vDimension
    nombre = input("Nombre de la muestra: ")
    nuevaMuestra = {}
    i = 1
    while i<=vDimension:
        nuevoValor= float(input(("Valor para "+str(i)+": ")))
        nuevaMuestra["z"+str(i)]=nuevoValor
        i+=1
    clase = int(input("Introduzca clase(+1,-1)"))
    nuevaMuestra["clase"]=clase
    return nuevaMuestra
    if clase==-1:
        muestras2[nombre]=nuevaMuestra
    else:
        muestras1[nombre]=nuevaMuestra

def introducirDatos():
    global muestras1,muestras2,clasificadores,muestrasActivas1,muestrasActivas2,vDimension
    vDimension= int(input("Dimension de los vectores: "))
    continuar=True
    while continuar:
        nuevaMuestra=introducirMuestra()
        clase=nuevaMuestra["clase"]
        if clase==-1:
            muestras2[nombre]=nuevaMuestra
        else:
            muestras1[nombre]=nuevaMuestra
        
        continuarQuery= input("Y si quiere introducir otra muestra: ")
        if continuarQuery.lower()!='y':
            continuar=False
        muestrasActivas1=dict(muestras1)
        muestrasActivas2=dict(muestras2)

def plotear(extra=None):
    global muestrasActivas1,muestrasActivas2
    plotearClase(muestrasActivas1,'bo')
    plotearClase(muestrasActivas2,'co')
    plotearFrontera(muestrasActivas1,muestrasActivas2)
    if extra!=None:
        valorX=extra["z1"]
        valorY=extra["z2"]
        claseM = extra["clase"]
        strClas = 'bo'
        if claseM==1:
            strClas='co'
        plt.plot(valorX,valorY,strClas)
        plt.annotate("clas",(valorX,valorY))
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

def CalculoMahalanobisDiagonal(muestra1,muestra2):
    global muestrasActivas1,muestrasActivas2
    muestrasCombinadas = {**muestrasActivas1, **muestrasActivas2}
    df=pd.DataFrame.from_dict(muestrasCombinadas,orient='index')
    varianza = df.var()
    i=1
    resultado=0
    while i<len(muestra1):
        valor1 = muestra1["z"+str(i)]
        valor2 = muestra2["z"+str(i)]
        peso= 1/varianza["z"+str(i)]
        resultado+=peso*((valor2-valor1)**2)
        i+=1
    resultado=math.sqrt(resultado)
    return resultado

def CalculoMahalanobisDiagonalPorClase(muestra1,muestra2,clase):
    global muestrasActivas1,muestrasActivas2
    if clase==-1:
        df=pd.DataFrame.from_dict(muestrasActivas1,orient='index')
    else:
        df=pd.DataFrame.from_dict(muestrasActivas2,orient='index')
    varianza = df.var()
    i=1
    resultado=0
    while i<len(muestra1):
        valor1 = muestra1["z"+str(i)]
        valor2 = muestra2["z"+str(i)]
        peso= 1/varianza["z"+str(i)]
        resultado+=peso*((valor2-valor1)**2)
        i+=1
    resultado=math.sqrt(resultado)
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


def Menu():
    print("1 Condensado Hart")
    print("2 Edicion Wilson")
    print("3 Clasificar")
    print("5 salir")
    seleccion=int(input("Seleccion: "))
    return seleccion


def knn(keyMuestraClas,muestraClas,muestras,k,tipoDistancias,tipoDeDesempate=None):
    muestraAClasificar = muestraClas
    resClas={}
    for keyMuestra in muestras:
        muestraActual = muestras[keyMuestra]
        if keyMuestraClas!=keyMuestra:
            resCalculo = -1;
            if tipoDistancias=='L1':
                resCalculo=CalculoL1(muestraActual,muestraAClasificar,)
            elif tipoDistancias=='L2':
                resCalculo=CalculoL2(muestraActual,muestraAClasificar,)
            elif tipoDistancias=="L0":
                resCalculo=CalculoL0(muestraActual,muestraAClasificar,)
            elif tipoDistancias=="MD":
                resCalculo=CalculoMahalanobisDiagonal(muestraActual,muestraAClasificar)
            elif tipoDistancias=="MDC":
                claseDeLaMuestraAClasificar=muestraActual["clase"]
                resCalculo=CalculoMahalanobisDiagonalPorClase(muestraActual,muestraAClasificar,claseDeLaMuestraAClasificar)
            resClas[keyMuestra]=resCalculo
    resClasOrdenado = sorted(resClas.items(), key=operator.itemgetter(1))
    resClas1=0
    resClasMenos1=0
    i=0
    #para desemapteRaro
    minDVecino=100000
    while i<len(resClasOrdenado):
        KnnResKey=resClasOrdenado[i][0]
        if i==0:
            minDVecino=resClasOrdenado[i][1]
        nTotal = resClas1+resClasMenos1
        if nTotal>=k:
            break;
        claseKey=muestras[KnnResKey]["clase"]
        if claseKey==1:
            resClas1+=1
        else:
            resClasMenos1+=1
    resClaseFinal =None
    continuar=True
    if tipoDeDesempate!=None and (tipoDeDesempate=='m' or tipoDeDesempate=='c'):
        i=0
        claseReal=muestraClas["clase"]
        while i< len(resClasOrdenado) and continuar:
            KnnResKey=resClasOrdenado[i][0]
            distanciaActual=resClasOrdenado[i][1]
            claseKey=muestras[KnnResKey]["clase"]
            if distanciaActual>minDVecino:
                continuar=False
            elif claseKey!=claseReal and tipoDeDesempate=='m':
                resClaseFinal =claseKey
                continuar=False
            elif claseKey==claseReal and tipoDeDesempate=='c':
                resClaseFinal =claseKey
                continuar=False
            i+=1
    if resClasMenos1>resClas1 and resClaseFinal==None:
        resClaseFinal= -1
    elif resClasMenos1<resClas1 and resClaseFinal==None:
        resClaseFinal= 1
    return resClaseFinal,resClasOrdenado

def CondensadoHart(orden,k,tipoDistancia,tipoClasificado):
    global muestrasActivas1,muestrasActivas2
    muestrasCombinadas = {**muestrasActivas1, **muestrasActivas2}
    error=continuar=True
    muestrasOrdenadas=sorted(muestrasCombinadas.keys(), key=NuevoOrden)
    if orden==2:
        muestrasOrdenadas.reverse()
    muestrasSalida= list(muestrasOrdenadas)
    print("Orden de recorrido:")
    print(muestrasOrdenadas)
    pasadasTotales=0
    #Primera fase
    i=1
    Store=[]
    Garbage=[]
    Store.append(muestrasOrdenadas[0])
    while i<len(muestrasOrdenadas):
        keyMuestraClas=muestrasOrdenadas[i]
        muestraAClas= muestrasCombinadas[keyMuestraClas]
        claseReal=muestraAClas["clase"]
        nuevoDic = rehacerDicSalida(Store)
        resKnn=knn(keyMuestraClas,muestraAClas,nuevoDic,k,tipoDistancia,tipoClasificado)
        print("Resultado de la clasificacion de " + keyMuestraClas+ ": "+ str(resKnn[1]))
        if resKnn[0]!=claseReal:
            Store.append(keyMuestraClas)
        else:
            Garbage.append(keyMuestraClas)
        i+=1
    print("Fin de la primera fase: ")
    print("Store")
    print(Store)
    print("Garbage")
    print(Garbage)
    #Segunda fase
    print("Empezamos segunda parte:")
    while(len(Garbage)!=0 and error and continuar):
        error = False
        i=0
        while i< len(Garbage):
            keyMuestraClas=Garbage[i]
            muestraAClas= muestrasCombinadas[keyMuestraClas]
            claseReal=muestraAClas["clase"]
            nuevoDic = rehacerDicSalida(Store)
            resKnn=knn(keyMuestraClas,muestraAClas,nuevoDic,k,tipoDistancia,tipoClasificado)
            if resKnn[0]!=claseReal:
                Store.append(keyMuestraClas)
                Garbage.remove(keyMuestraClas)
                error=True
            else:
                i+=1
        print("Store")
        print(Store)
        print("Garbage")
        print(Garbage)
        conString= input("Y para continuar")
        if conString.lower()!='y':
            continuar=False
    if(not error):
        print("Algoritmo finalizado con error 0")
    print("Store")
    print(Store)
    print("Garbage")
    print(Garbage)
    reAsignarMuestrasActivas(Store)
    plotear()

def Wilson(orden,k,tipoDistancia,tipoDeDesempate):
    global muestrasActivas1,muestrasActivas2
    muestrasCombinadas = {**muestrasActivas1, **muestrasActivas2}
    error=continuar=True
    muestrasOrdenadas=sorted(muestrasCombinadas.keys(), key=NuevoOrden)
    if orden==2:
        muestrasOrdenadas.reverse()
    muestrasSalida= list(muestrasOrdenadas)
    print("Orden de recorrido:")
    print(muestrasOrdenadas)
    pasadasTotales=0
    while continuar and error:
        error=False
        i=0
        while i<len(muestrasSalida):
            keyMuestraClas=muestrasSalida[i]
            muestraAClas= muestrasCombinadas[keyMuestraClas]
            claseReal=muestraAClas["clase"]
            nuevoDic = rehacerDicSalida(muestrasSalida)
            resKnn=knn(keyMuestraClas,muestraAClas,nuevoDic,k,tipoDistancia,tipoDeDesempate)
            if resKnn[0]!=claseReal:
                error=True
                muestrasSalida.remove(keyMuestraClas)
            else:
                i+=1
        print("Muestras vivas: ")
        print(muestrasSalida)
        conString= input("Y para continuar")
        if conString.lower()!='y':
            continuar=False
    if(not error):
        print("Algoritmo finalizado con error 0")
    print(muestrasSalida)
    reAsignarMuestrasActivas(muestrasSalida)
    plotear()

def rehacerDicSalida(lista):
    global muestrasActivas1,muestrasActivas2
    i=0
    dicSalida={}
    while i<len(lista):
        key = lista[i]
        AInsertar = muestrasActivas1.get(key,None)
        if AInsertar==None:
            AInsertar = muestrasActivas2.get(key,None)
        dicSalida[key]=AInsertar
        i+=1
    return dicSalida

def reAsignarMuestrasActivas(seleccion):
    global muestrasActivas1,muestrasActivas2
    muestrasCombinadas = {**muestrasActivas1, **muestrasActivas2}
    muestrasActivas1={}
    muestrasActivas2={}
    i=0;
    while i<len(seleccion):
        keyActual=seleccion[i]
        muestraActual=muestrasCombinadas[keyActual]
        clase = muestraActual["clase"]
        if clase==-1:
            muestrasActivas1[keyActual]=muestraActual
        else:
            muestrasActivas2[keyActual]=muestraActual
        i+=1



def NuevoOrden(item):
    num = item[1:]
    return int(num)

def main():
    #muestras1 siempre clase -1
    #muestras2 siempre clase 1
    global muestras1,muestrasActivas1,muestras2,muestrasActivas2,vDimension
    vDimension=2
    #muestras1 = {'x1': {'z1': 0.0, 'z2': 0.0, 'clase': -1}, 'x3': {'z1': 1.0, 'z2': 2.0, 'clase': -1}
    #            , 'x5': {'z1': 0.0, 'z2': 1.0, 'clase': -1}, 'x7': {'z1': 2.0, 'z2': 3.0, 'clase': -1}, 'x8': {'z1': 3.0, 'z2': 2.0, 'clase': -1}
    #            , 'x10': {'z1': 4.0, 'z2': 0.0, 'clase': -1}, 'x12': {'z1': 4.0, 'z2': 1.0, 'clase': -1}}
    #muestras2 = {'x2': {'z1': 1.0, 'z2': 0.0, 'clase': 1},'x4': {'z1': 1.0, 'z2': 1.0, 'clase': 1}
    #            , 'x6': {'z1': 2.0, 'z2': 2.0, 'clase': 1}
    #            , 'x9': {'z1': 3.0, 'z2': 0.0, 'clase': 1}, 'x11': {'z1': 3.0, 'z2': 1.0, 'clase': 1}
    #            , 'x13': {'z1': 2.0, 'z2': 0.0, 'clase': 1}, 'x14': {'z1': 2.0, 'z2': 1.0, 'clase': 1}}
    #muestras1={'x1': {'z1': 1.0, 'z2': 2.0, 'clase': -1}, 'x3': {'z1': 3.0, 'z2': 2.0, 'clase': -1}, 'x5': {'z1': 5.0, 'z2': 2.0, 'clase': -1}}
    #muestras2={'x2': {'z1': 2.0, 'z2': 1.0, 'clase': 1}, 'x4': {'z1': 2.0, 'z2': 4.0, 'clase': 1}, 'x6': {'z1': 2.0, 'z2': 5.0, 'clase': 1}}
    #muestras1={'x1': {'z1': 1.0, 'z2': 1.0, 'clase': -1}, 'x3': {'z1': 1.0, 'z2': 3.0, 'clase': -1}, 'x5': {'z1': 3.0, 'z2': 4.0, 'clase': -1}}
    #muestras2={'x2': {'z1': 3.0, 'z2': 1.0, 'clase': 1}, 'x4': {'z1': 4.0, 'z2': 2.0, 'clase': 1}, 'x6': {'z1': 3.0, 'z2': 2.0, 'clase': 1}, 'x7': {'z1': 5.0, 'z2': 4.0, 'clase': 1}}
    #muestras1={'x1': {'z1': 2.0, 'z2': 2.0, 'clase': -1}, 'x3': {'z1': 7.0, 'z2': 1.0, 'clase': -1}, 'x5': {'z1': 4.0, 'z2': 2.0, 'clase': -1}, 'x7': {'z1': 6.0, 'z2': 1.0, 'clase': -1}, 'x9': {'z1': 3.0, 'z2': 4.0, 'clase': -1}}
    #muestras2={'x2': {'z1': 6.0, 'z2': 4.0, 'clase': 1}, 'x4': {'z1': 8.0, 'z2': 2.0, 'clase': 1}, 'x6': {'z1': 8.0, 'z2': 3.0, 'clase': 1}, 'x8': {'z1': 5.0, 'z2': 2.0, 'clase': 1}, 'x10': {'z1': 7.0, 'z2': 5.0, 'clase': 1}}
    muestras1={'x1': {'z1': 2.0, 'z2': 4.0, 'clase': -1}, 'x4': {'z1': 2.0, 'z2': 1.0, 'clase': -1}, 'x7': {'z1': 1.0, 'z2': 3.0, 'clase': -1}, 'x8': {'z1': 3.0, 'z2': 3.0, 'clase': -1}}
    muestras2={'x2': {'z1': 2.0, 'z2': 3.0, 'clase': 1}, 'x3': {'z1': 2.0, 'z2': 0.0, 'clase': 1}, 'x5': {'z1': 3.0, 'z2': 1.0, 'clase': 1}, 'x6': {'z1': 1.0, 'z2': 1.0, 'clase': 1}}
    muestrasActivas1=dict(muestras1)
    muestrasActivas2=dict(muestras2)
    #introducirDatos()
    plotear()
    continuar=True
    while continuar:
        resSeleccion = Menu()
        if resSeleccion==1:
            opciones = PreguntasDeAlgoritmos(False)
            CondensadoHart(opciones[0],opciones[1],opciones[2],opciones[3])
        elif resSeleccion==2:
            opciones = PreguntasDeAlgoritmos(False)
            Wilson(opciones[0],opciones[1],opciones[2],opciones[3])
        elif resSeleccion==3:
            k = int(input("Numero k de vecino: "))
            muestraAClasificar= introducirMuestra()
            muestrasCombinadas = {**muestrasActivas1, **muestrasActivas2}
            opciones = PreguntasDeAlgoritmos(False)
            res=knn("",muestraAClasificar,muestrasCombinadas,opciones[0],opciones[1],opciones[2])
            print("La muestra pertenece a la clase: " + str(res[0]))
            print("Orden knn: ")
            print(res[1])
            muestraAClasificar["clase"]=res[0]
            plotear(muestraAClasificar)

def PreguntasDeAlgoritmos(clasificar):
    if not clasificar:
        resOrden=int(input("1 Orden ascendente, 2 orden descendente: "))
    kVecinos=int(input("numero de vecinos: "))
    tipoDistancia=input("Tipo de distancia L0,L1,L2,MD,MDC: ").upper()
    desempate=input("m desempate a clase erronea c a clase correcta, cualquier otro simbolo no se vigila: ").lower()
    return resOrden,kVecinos,tipoDistancia,desempate

if __name__ == "__main__":
    main()