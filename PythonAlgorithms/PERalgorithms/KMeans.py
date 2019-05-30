
import sys
import math
import operator
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
    print("2 Condensado Wilson")
    print("3 Error")
    print("4 Clasificar")
    print("5 salir")
    seleccion=int(input("Seleccion: "))
    return seleccion


def knn(keyMuestraClas,muestraClas,muestras,k,tipoDistancias):
    muestraAClasificar = muestraClas
    resClas={}
    for keyMuestra in muestras:
        muestraActual = muestras[keyMuestra]
        if keyMuestraClas!=keyMuestra:
            resCalculo = -1;
            if tipoDistancias=='L1':
                resCalculo=CalculoL1(muestraAClasificar,muestraActual)
            elif tipoDistancias=='L2':
                resCalculo=CalculoL2(muestraAClasificar,muestraActual)
            else:
                resCalculo=CalculoL0(muestraAClasificar,muestraActual)
            resClas[keyMuestra]=resCalculo
    resClasOrdenado = sorted(resClas.items(), key=operator.itemgetter(1))
    resClas1=0
    resClasMenos1=0
    i=0
    while i<len(resClasOrdenado):
        KnnResKey=resClasOrdenado[i][0]
        nTotal = resClas1+resClasMenos1
        if nTotal>=k:
            break;
        claseKey=muestras[KnnResKey]["clase"]
        if claseKey==1:
            resClas1+=1
        else:
            resClasMenos1+=1
    resClaseFinal =1
    if resClasMenos1>resClas1:
        resClaseFinal= -1
    elif resClasMenos1==resClas1:
        resClaseFinal= 0
    return resClaseFinal,resClasOrdenado

def CondensadoHart(orden,k,tipoDistancia):
    global muestrasActivas1,muestrasActivas2
    muestrasCombinadas = {**muestrasActivas1, **muestrasActivas2}
    error=continuar=True
    muestrasOrdenadas=sorted(muestrasCombinadas.keys(), key=NuevoOrden)
    if orden==2:
        muestrasOrdenadas.reverse()
    muestrasSalida= list(muestrasOrdenadas)
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
        resKnn=knn(keyMuestraClas,muestraAClas,nuevoDic,k,tipoDistancia)
        if resKnn[0]!=claseReal:
            Store.append(keyMuestraClas)
        else:
            Garbage.append(keyMuestraClas)
        i+=1
    #Segunda fase
    while(len(Garbage)!=0 and error and continuar):
        error = False
        i=0
        while i< len(Garbage):
            keyMuestraClas=Garbage[i]
            muestraAClas= muestrasCombinadas[keyMuestraClas]
            claseReal=muestraAClas["clase"]
            nuevoDic = rehacerDicSalida(Store)
            resKnn=knn(keyMuestraClas,muestraAClas,nuevoDic,k,tipoDistancia)
            if resKnn[0]!=claseReal:
                Store.append(keyMuestraClas)
                Garbage.remove(keyMuestraClas)
                error=True
            i+=1
        conString= input("Y para continuar")
        if conString.lower()!='y':
            continuar=False
    print("Store")
    print(Store)
    print("Garbage")
    print(Garbage)
    plotear()

def Wilson(orden,k,tipoDistancia):
    global muestrasActivas1,muestrasActivas2
    muestrasCombinadas = {**muestrasActivas1, **muestrasActivas2}
    error=continuar=True
    muestrasOrdenadas=sorted(muestrasCombinadas.keys(), key=NuevoOrden)
    if orden==2:
        muestrasOrdenadas.reverse()
    muestrasSalida= list(muestrasOrdenadas)
    print(muestrasOrdenadas)
    pasadasTotales=0
    while continuar and error:
        error=False
        i=0
        while i<len(muestrasOrdenadas):
            keyMuestraClas=muestrasOrdenadas[i]
            muestraAClas= muestrasCombinadas[keyMuestraClas]
            claseReal=muestraAClas["clase"]
            nuevoDic = rehacerDicSalida(muestrasSalida)
            resKnn=knn(keyMuestraClas,muestraAClas,nuevoDic,k,tipoDistancia)
            if resKnn[0]!=claseReal:
                error=True
                muestrasSalida.remove(keyMuestraClas)
            i+=1
        conString= input("Y para continuar")
        if conString.lower()!='y':
            continuar=False
    print(muestrasSalida)
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

def NuevoOrden(item):
    num = item[1:]
    return int(num)

def main():
    global muestras1,muestrasActivas1,muestras2,muestrasActivas2,vDimension
    vDimension=2
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
    continuar=True
    while continuar:
        resSeleccion = Menu()
        if resSeleccion==1:
            CondensadoHart(1,1,"L2")
        elif resSeleccion==2:
            Wilson(1,1,"L2")
        elif resSeleccion==4:
            k = int(input("Numero k de vecino: "))
            muestraAClasificar= introducirMuestra()
            muestrasCombinadas = {**muestrasActivas1, **muestrasActivas2}
            res=knn("",muestraAClasificar,muestrasCombinadas,1,"L2")
            print("La muestra pertenece a la clase: " + str(res[0]))
            print("Orden knn: ")
            print(res[1])
            muestraAClasificar["clase"]=res[0]
            plotear(muestraAClasificar)


if __name__ == "__main__":
    main()