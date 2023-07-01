from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/bacterias/")
def read_item(p: Union[int, None] = None,e: Union[int, None] = None,t: Union[int, None] = None,d: Union[int, None] = None,bacterias: Union[str, None] = None):
    try:
        bacterias = [abs(int(char)) for char in bacterias.split(',')]
        periodo_maduracion = abs(int(p))
        esperanza_vida = abs(int(e))
        taza_reproduccion = abs(int(t))
        dias_iteracion = abs(int(d))
        bacterias = bacterias_inicial(bacterias,esperanza_vida, periodo_maduracion)
        return {
            'total_bacterias':nro_total_bacterias(bacterias,periodo_maduracion, taza_reproduccion, esperanza_vida, dias_iteracion),
            'maturation_period':periodo_maduracion,
            'life_expectancy':esperanza_vida,
            'reproduction_rate':taza_reproduccion,
            'days':dias_iteracion
        }
    except ValueError:
        return {
            'error': "Arguments p:maturation_period, e:life_expectancy, t: reproduction_rate, d: days, and initial bacterias state must be integers"
        }
    except AttributeError:
        return {
            'error': "Check if the parameters have the correct name: p: maturation_period, e: life_expectancy, t:reproduction_rate,d:days, bacterias: initial bacterias state. For example: p=1&e=3&d=60&t=2&bacterias=2,3,3,1,2"
        }
        
def iteracion(bacterias, dias_maduracion, taza, esperanza_vida):
    """Dado un estado inicial de bacterias nos devuelve el estado de dichas bacterias al día siguiente, por ejemplo si el estado inicial es [{0: 0}, {1: 1}, {2: 2}, {3: 2}] esta funcion nos 
       devolverá [{0: 1}, {1: 2}, {2: 2}], omitiendo los dias en los que no existe ninguna bacteria

    Args:
        bacterias (arreglo[{:}]): Arreglo que representa el estado inicial de las bacterias en un día determinado
        dias_maduracion (int): Días de maduración de una bacteria
        taza (int): Taza de reproducción de una bacteria
        esperanza_vida (int): Esperanza de vida de una bacteria

    Returns:
        arreglo[{:}]: Estado de las bacterias al siguiente día
    """
    dia_siguiente = []
    for objeto in bacterias:
        for clave, valor in objeto.items():
            if valor > 0 and clave != 0:
                obj = {clave-1:valor}
                dia_siguiente.append(obj)
            else:
                if clave == 0 and valor > 0:
                    object_0 = {
                        esperanza_vida + dias_maduracion : valor*2
                    }
                    dia_siguiente.append(object_0)
                    object_0 = {
                        esperanza_vida : valor
                    }
                    dia_siguiente.append(object_0)
    return dia_siguiente

def completar_dias(arreglo, esperanza_vida, periodo_maduracion):
    """Dado un arreglo inicial [{4: 4}, {3: 2}, {0: 2}, {2: 1}, {3: 2}] verifica si alguna clave, que representa a los dias de una bacteria, no 
       existe en el arreglo, si no existe dicha clave agrega un elemento "{nro_dia:0}" con nro_dia -> número de día faltante y con valor "0" que
       significa que en dicho día no existe ninguna bacteria y nos devuelve [{4: 4}, {3: 2}, {0: 2}, {2: 1}, {3: 2}, {1: 0}]

    Args:
        arreglo (arreglo[{:}]): Arreglo inicial que contiene diccionarios que representan los cuantas bacterias hay en un día
        esperanza_vida (int): Esperanza de vida de una bacteria
        periodo_maduracion (int): Pediodo que le toma a una bacteria en llegar a su edad adulta

    Returns:
        arreglo (arreglo[{:}]): Arreglo con todos los dias y cantidades de bacterias que hay en dicho día
    """
    arreglo_claves = list(range(esperanza_vida+periodo_maduracion))
    for a in arreglo_claves:
        encontrada = False
        for objeto in arreglo:
            if a in objeto:
                encontrada = True
        if encontrada == False:
            arreglo.append({a:0})
    return arreglo

def sumar_bacterias_dia(arreglo):
    """Verifica so hay elementos repetidos en un arreglo de diccionarios, si hay suma los valores de los elementos que tienen la misma clave, por ejemplo
       [{4: 4}, {3: 2}, {0: 2}, {2: 1}, {3: 2}, {1: 0}] nos devuelve [{0: 2}, {1: 0}, {2: 1}, {3: 4}, {4: 4}]

    Args:
        arreglo (arreglo[{:}]): Arreglo inicial con o sin elementos duplicados

    Returns:
        arreglo (arreglo[{:}]): Arreglo final sin elementos duplicados y con valores de la misma clave sumados
    """
    resultado = []
    claves = set()
    for diccionario in arreglo:
        for clave, valor in diccionario.items():
            claves.add(clave)
    for clave in claves:
        suma = 0
        for diccionario in arreglo:
            if clave in diccionario:
                suma += diccionario[clave]
        resultado.append({clave: suma})
    return resultado

def nro_total_bacterias(bacterias, periodo_maduracion, taza_reproduccion, esperanza_vida, dias_iteracion):
    """Dado un arreglo con el estado incial de las bacterias, un perdiodo de maduracion, taza de reproduccion, esperanza de vida u dias de iteración, esta función calcula el número
    total de bacterias despues de n dias, donde "n" representa el numero total de dias de iteración

    Args:
        bacterias (arreglo[{:}]): Arreglo con el estado inicial de las bacterias
        periodo_maduracion (_type_): Periodo en el que una bacteria pasa a su edad adulta
        taza_reproduccion (_type_): Taza de reproducción de las bacterias
        esperanza_vida (_type_): Esperanza de vida de las bacterias
        dias_iteracion (_type_): Dias de iteración

    Returns:
        int: Suma de todos los valores de los elementos del arreglo que representa la cantidad total de bacterias
    """
    for dia in range(dias_iteracion):
        bacterias = sumar_bacterias_dia(completar_dias(iteracion(bacterias,periodo_maduracion,taza_reproduccion,esperanza_vida),esperanza_vida, periodo_maduracion))
    suma = 0
    for diccionario in bacterias:
        for valor in diccionario.values():
            suma += valor
    return suma

def bacterias_inicial(bacterias, dias_vida, dias_maduracion):
    """Dado un arreglo inicial del tipo [2, 3, 3, 1, 2] que representan a las bacterias en su estado inicial, devuelve un arreglo
       de diccionarios del tipo [{0: 0}, {1: 1}, {2: 2}, {3: 2}], con clave:valor {nro_dia:nro_bacterias}, con nro_dia -> el día de vida de
       la bacteria y nro_bacterias -> número de bacterias que están en el mismo día

    Args:
        bacterias (arreglo[int]): Arreglo de enteros que representan a las bacterias en su estado inicial
        dias_vida (int): Número de dias de vida que tiene una bacteria
        dias_maduracion (int): Número de dias que tiene que pasar para que una bacteria llegue a su edad adulta

    Returns:
        arreglo[{:}]: Retorna un arreglo de diccionarios con clave: dia de vida de la bacteria y valor: número de bacterias que se encuentran en 
        el mismo día
    """
    dias_vida = list(range(dias_vida+dias_maduracion))
    contador = {}
    for elemento in dias_vida:
        contador[elemento] = 0
    for elemento in bacterias:
        if elemento in dias_vida:
            contador[elemento] += 1
    resultado = [{clave: valor} for clave, valor in contador.items()]
    return resultado
