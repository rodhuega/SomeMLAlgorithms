
import sys
import math
from py_expression_eval import Parser

parse = Parser()
muestras = {}
clasificadores={}
pesos={}
alfas={}
epsilons={}

def introducirDatos():
    global muestras,clasificadores
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
    continuar=True
    print("Introduccion de clasificadores")
    while continuar:
        clasificador={}
        nombre = input("Nombre del clasificador: ")
        clase1 = int(input("Clase de la frontera1: "))
        stringEcuacion1 = input("Ecuacion frontera1: ")
        clase2 = int(input("Clase de la frontera2: "))
        stringEcuacion2 = input("Ecuacion frontera2: ")
        clasificador[clase1]=stringEcuacion1
        clasificador[clase2]=stringEcuacion2
        clasificadores[nombre]=clasificador
        continuarQuery= input("Y si quiere introducir otra muestra: ")
        if continuarQuery.lower()!='y':
            continuar=False

def clasificar(claveClasificador,muestra):
    global clasificadores
    clasificadorActual = clasificadores[claveClasificador]
    ClasPositivo = clasificadorActual[1]
    ClasNegativo = clasificadorActual[-1]
    dicParaParser={};
    for keyMuestra in muestra.keys():
        if keyMuestra!="clave":
            dicParaParser[keyMuestra]=muestra[keyMuestra]
    resPositivo=parse.parse(ClasPositivo).evaluate(dicParaParser)
    resNegativo=parse.parse(ClasNegativo).evaluate(dicParaParser)
    if resPositivo:
        return 1
    elif resNegativo:
        return -1
    else:
        print("Error")

def clasificadorMinimoepsilon(pesosIteracion):
    global clasificadores,muestras
    minepsilon = 100000
    minClasificador = ""
    pesosUltimaIteracion=pesos["w"+str(pesosIteracion)]
    clasificadorConSuEpsilon={}
    for keyClasificadores in clasificadores.keys():
        epsilonClasificador = 0
        for keyMuestra in muestras.keys():
            valores = muestras[keyMuestra];
            resClas = clasificar(keyClasificadores,valores)
            #recuperar ultimo peso para sumar
            epsilonMuestra=pesosUltimaIteracion[keyMuestra]
            #ver valor del epsilon
            if (resClas == valores["clase"]):
                epsilonMuestra=0
            epsilonClasificador+=epsilonMuestra
        clasificadorConSuEpsilon[keyClasificadores]=epsilonClasificador
        #if epsilonClasificador<minepsilon:
        #    minepsilon=epsilonClasificador
        #    minClasificador=keyClasificadores
    print(clasificadorConSuEpsilon)
    minClasificador=input("Selecciona un clasificador: ")
    minepsilon=clasificadorConSuEpsilon[minClasificador]
    return minClasificador,minepsilon

def RecalcularPesos(alfa,nuevaIteracion,clasificador):
    global pesos,muestras,clasificadores
    viejaIteracion = nuevaIteracion-1
    viejosPesos = pesos["w"+str(viejaIteracion)]
    nuevosPesos={}
    sumandoPesos=0
    for keyMuestra in muestras.keys():
        muestra = muestras[keyMuestra]
        pesoAntiguo = viejosPesos[keyMuestra]
        claseReal=muestra["clase"]
        claseCalculada=clasificar(clasificador,muestra)
        nuevoPeso = pesoAntiguo*math.exp((-1)*claseReal*claseCalculada*alfa)
        nuevosPesos[keyMuestra]=nuevoPeso
        sumandoPesos+=nuevoPeso
    print("Pesos sin normalizar")
    print(nuevosPesos)
    for keyMuestra in nuevosPesos.keys():
        nuevosPesos[keyMuestra]=nuevosPesos[keyMuestra]/sumandoPesos
    pesos["w"+str(nuevaIteracion)]=nuevosPesos

def AdaBoost():
    global pesos,muestras,clasificadores
    N= 1/len(muestras)
    peososIteracion={};
    for key in muestras.keys():
        peososIteracion[key]=N
    pesos["w1"]=peososIteracion
    i=1
    clasificadorFinal=""
    while i<100:
        (clasificador,epsilon)=clasificadorMinimoepsilon(i)
        if epsilon>0.5:
            break
        dentroLn=(1-epsilon)/epsilon
        alfaActual = 1/2*math.log(dentroLn)
        RecalcularPesos(alfaActual,i+1,clasificador)
        print("Iteracion " +str(i)+"-----------")
        print("Alfa: "+  str(alfaActual))
        print("Clasificador elegido " + clasificador + " con epsilon " + str(epsilon))
        print("Pesos")
        print(pesos)
        #falta imprimir el clasificador y los epsilon
        clasificadorFinal+=str(alfaActual)+clasificador+"+"
        print("El clasificador actual es: " +clasificadorFinal)
        i+=1


def main():
    global muestras,clasificadores
    introducirDatos()
    #muestras={'x1': {'z1': 0.0, 'z2': 0.0, 'clase': 1}, 'x2': {'z1': 2.0, 'z2': 2.0, 'clase': -1}, 'x3': {'z1': 1.0, 'z2': 2.0, 'clase': 1}, 'x4': {'z1': 0.0, 'z2': 1.0, 'clase': -1}, 'x5': {'z1': -1.0, 'z2': 1.0, 'clase': 1}}
    #clasificadores={'g1': {1: 'z1>0', -1: 'z1<=0'}, 'g2': {1: 'z2>1', -1: 'z2<=1'}, 'g3': {1: 'z2-z1>0', -1: 'z2-z1<=0'}, 'g4': {1: 'z1+z2<=3', -1: 'z1+z2>3'}}
    print(muestras)
    print(clasificadores)
    AdaBoost()

if __name__ == "__main__":
    sys.exit(int(main() or 0))