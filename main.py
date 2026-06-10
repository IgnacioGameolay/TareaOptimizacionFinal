import math
import random
import time

universo = {1, 2, 3, 4, 5, 6, 7, 8} # Todos los espacios dentro del SCP. Editable a gusto de quien lo pruebe.
max_iteraciones = 1000 # Máximo de iteraciones del Simulated Annealing
alpha = 0.98 # Valor de enfriamiento

# Subconjuntos que contienen ciertos n° de espacios del universo junto a los costos al ser usados
# Editable a gusto de quien lo pruebe
subconjuntos = [ 
    ("S1", {1, 2, 3}, 3),
    ("S2", {2, 4, 5}, 4),
    ("S3", {1, 6, 7}, 5),
    ("S4", {3, 4, 6}, 2),
    ("S5", {5, 7, 8}, 3),
    ("S6", {6, 8},    1),
]

# Función para calcular el enfriamiento concorde avancemos en las iteraciones
def enfriamiento(temperatura_actual):
    return temperatura_actual * alpha

# Generación de solución inicial mediante una solución aleatoria válida
def generar_solucion_inicial():
    solucion = generar_solucion_aleatoria()

    while not cubre_universo(solucion):
        solucion = generar_solucion_aleatoria()

    return solucion

# Generación de solución aleatoria con el uso de la biblioteca Random
def generar_solucion_aleatoria():
    solucion = []

    for _ in range(len(subconjuntos)):
        if (random.random() < 0.5):
            solucion.append(0)
        else:
            solucion.append(1)

    return solucion


# Generación de vecino mediante la selección aleatoria de una de las soluciones pasandola de 1->0 o 0->1
def generar_vecino(solucion_actual):
    vecino = solucion_actual.copy()

    indice = random.randrange(len(vecino))
    vecino[indice] = 1 - vecino[indice]

    return vecino

# Calculo de costo total de una solución
def calcular_costo(solucion): 
    cost = 0

    for i in range(len(subconjuntos)):
        if solucion[i] == 1:
            cost += subconjuntos[i][2]
    
    return cost

# Función para verificar que los subconjuntos cubran el universo
def cubre_universo(solucion):
    cobertura = set()

    for i in range(len(subconjuntos)):
        if solucion[i] == 1:
            elementos = subconjuntos[i][1]
            cobertura.update(elementos)

    return universo.issubset(cobertura)

# Función que usa Criterio de Metropolis visto en clase, con un rechazo automático si es que no cubre el universo
def criterio_aceptacion(solucion_nueva, solucion_antigua, temperatura):

    if not cubre_universo(solucion_nueva):
        return False
        
    diferencia_costos = calcular_costo(solucion_nueva) - calcular_costo(solucion_antigua)

    if (diferencia_costos < 0):
        return True
    
    if (temperatura == 0):
        return False

    p = math.exp(-diferencia_costos/temperatura)

    if (random.random() < p):
        return True
    
    return False

# Función simulated_annealing para la búsqueda de la mejor solución
def simulated_annealing(solucion_inicial, temperatura_inicial):
    iteracion_actual = 1
    iteracion_mejor_solucion = 1

    solucion_actual = solucion_inicial.copy()
    mejor_solucion = solucion_inicial.copy()

    temperatura_actual = temperatura_inicial

    while iteracion_actual <= max_iteraciones:
        vecino = generar_vecino(solucion_actual)

        aceptar_solucion = criterio_aceptacion(vecino, solucion_actual, temperatura_actual)

        if aceptar_solucion:
            solucion_actual = vecino.copy()

            if calcular_costo(solucion_actual) < calcular_costo(mejor_solucion):
                mejor_solucion = solucion_actual.copy()
                iteracion_mejor_solucion = iteracion_actual

        temperatura_actual = enfriamiento(temperatura_actual)
        iteracion_actual += 1
    
    return mejor_solucion, iteracion_mejor_solucion

tiempo_inicio = time.time()

solucion_inicial = generar_solucion_inicial()
mejor_solucion, iteracion_mejor = simulated_annealing(solucion_inicial, 100)

tiempo_fin = time.time()
tiempo_total = tiempo_fin - tiempo_inicio

subconjuntos_seleccionados = []
cobertura = set()

for i in range(len(subconjuntos)):
    if mejor_solucion[i] == 1:
        subconjuntos_seleccionados.append(subconjuntos[i][0])
        cobertura.update(subconjuntos[i][1])

print("========== Resultado SCP - Simulated Annealing ==========")
print("Vector binario:", mejor_solucion)
print("Subconjuntos seleccionados:", subconjuntos_seleccionados)
print("Costo total:", calcular_costo(mejor_solucion))
print("Cobertura:", cobertura)
print("Elementos cubiertos:", len(cobertura), "/", len(universo))
print("Factible:", cubre_universo(mejor_solucion))
print("Iteración mejor solución:", iteracion_mejor)
print("Iteraciones totales:", max_iteraciones)
print("Tiempo de ejecución:", round(tiempo_total, 6), "segundos")
print("=========================================================")