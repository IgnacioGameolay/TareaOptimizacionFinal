import math, random, time


# Parametros definidos
max_iteraciones = 1000  # Máximo de iteraciones del Simulated Annealing
alpha = 0.98  # Valor de enfriamiento
temperatura_inicial = 100  # Temperatura inicial
n_ejecuciones = 10  # Cantidad de ejecuciones para resultados estadísticos

universo = set()
subconjuntos = []


# Lectura de instancia SCP
def leer_instancia_scp(ruta_archivo):
    """
    Lee una instancia SCP desde archivo en formato tipo.

    Formato esperado:
    - n m
    - costos de los m subconjuntos
    - para cada elemento:
        k
        indices de subconjuntos que cubren al elemento

    Retorna:
    - universo: set con elementos {1, 2, ..., n}
    - subconjuntos: lista de tuplas (nombre, elementos, costo)
    """
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read().split()

    if len(contenido) == 0:
        raise ValueError("El archivo de instancia está vacío.")

    try:
        datos = list(map(int, contenido))
    except ValueError:
        raise ValueError("La instancia contiene valores no enteros.")

    pos = 0

    if len(datos) < 2:
        raise ValueError("Archivo incompleto: faltan n y m.")

    # Primera parte: n y m
    n = datos[pos]
    pos += 1

    m = datos[pos]
    pos += 1

    if n <= 0 or m <= 0:
        raise ValueError("Los valores n y m deben ser positivos.")

    # Segunda parte: costos de los m subconjuntos
    if pos + m > len(datos):
        raise ValueError("Archivo incompleto: faltan costos de subconjuntos.")

    costos = datos[pos:pos + m]
    pos += m

    # Inicializar subconjuntos vacíos
    subconjuntos_elementos = [set() for _ in range(m)]

    # Tercera parte: para cada elemento, leer cuántos subconjuntos lo cubren
    for elemento in range(1, n + 1):
        if pos >= len(datos):
            raise ValueError(
                f"Archivo incompleto al leer cobertura del elemento {elemento}."
            )

        k = datos[pos]
        pos += 1

        if k < 0:
            raise ValueError(
                f"Cantidad inválida de subconjuntos para el elemento {elemento}: {k}."
            )

        if pos + k > len(datos):
            raise ValueError(
                f"Archivo incompleto: el elemento {elemento} dice estar cubierto por {k} subconjuntos, "
                "pero no hay suficientes índices en el archivo."
            )

        indices_subconjuntos = datos[pos:pos + k]
        pos += k

        for idx in indices_subconjuntos:
            if idx < 1 or idx > m:
                raise ValueError(
                    f"Índice de subconjunto fuera de rango: {idx}. "
                    f"Debe estar entre 1 y {m}."
                )

            subconjuntos_elementos[idx - 1].add(elemento)

    universo_leido = set(range(1, n + 1))

    subconjuntos_leidos = [
        (f"S{i + 1}", subconjuntos_elementos[i], costos[i])
        for i in range(m)
    ]

    validar_instancia(universo_leido, subconjuntos_leidos)

    return universo_leido, subconjuntos_leidos


def validar_instancia(universo_leido, subconjuntos_leidos):
    """Verifica que la unión de todos los subconjuntos pueda cubrir el universo."""
    cobertura_total = set()

    for _, elementos, _ in subconjuntos_leidos:
        cobertura_total.update(elementos)

    elementos_no_cubiertos = universo_leido - cobertura_total

    if elementos_no_cubiertos:
        raise ValueError(
            "La instancia no tiene solución factible. "
            f"Elementos no cubiertos: {sorted(elementos_no_cubiertos)}"
        )


# Función para calcular el enfriamiento conforme avanzamos en las iteraciones
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
        if random.random() < 0.5:
            solucion.append(0)
        else:
            solucion.append(1)

    return solucion


# Generación de vecino mediante la selección aleatoria de un bit, pasándolo de 1->0 o 0->1
def generar_vecino(solucion_actual):
    vecino = solucion_actual.copy()

    indice = random.randrange(len(vecino))
    vecino[indice] = 1 - vecino[indice]

    return vecino


# Cálculo de costo total de una solución
def calcular_costo(solucion):
    costo = 0

    for i in range(len(subconjuntos)):
        if solucion[i] == 1:
            costo += subconjuntos[i][2]

    return costo


# Función para obtener la cobertura de una solución
def obtener_cobertura(solucion):
    cobertura = set()

    for i in range(len(subconjuntos)):
        if solucion[i] == 1:
            elementos = subconjuntos[i][1]
            cobertura.update(elementos)

    return cobertura


# Función para verificar que los subconjuntos cubran el universo
def cubre_universo(solucion):
    cobertura = obtener_cobertura(solucion)

    return universo.issubset(cobertura)


# Función que usa Criterio de Metropolis visto en clase,
# con rechazo automático si la solución no cubre el universo
def criterio_aceptacion(solucion_nueva, solucion_antigua, temperatura):
    if not cubre_universo(solucion_nueva):
        return False

    diferencia_costos = calcular_costo(solucion_nueva) - calcular_costo(solucion_antigua)

    if diferencia_costos < 0:
        return True

    if temperatura == 0:
        return False

    p = math.exp(-diferencia_costos / temperatura)

    if random.random() < p:
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

        aceptar_solucion = criterio_aceptacion(
            vecino,
            solucion_actual,
            temperatura_actual
        )

        if aceptar_solucion:
            solucion_actual = vecino.copy()

            if calcular_costo(solucion_actual) < calcular_costo(mejor_solucion):
                mejor_solucion = solucion_actual.copy()
                iteracion_mejor_solucion = iteracion_actual

        temperatura_actual = enfriamiento(temperatura_actual)
        iteracion_actual += 1

    return mejor_solucion, iteracion_mejor_solucion


# Cálculo de media de los resultados
def calcular_media(resultados):
    return sum(resultados) / len(resultados)


# Cálculo de desviación estándar muestral de los resultados
def calcular_desviacion_estandar(resultados):
    if len(resultados) <= 1:
        return 0

    media = calcular_media(resultados)
    suma = 0

    for valor in resultados:
        suma += (valor - media) ** 2

    return math.sqrt(suma / (len(resultados) - 1))


# Función para ejecutar la metaheurística varias veces
def ejecutar_experimentos():
    resultados = []
    soluciones = []
    iteraciones_mejor = []

    mejor_solucion_global = None
    mejor_costo_global = None

    tiempo_inicio = time.time()

    for ejecucion in range(1, n_ejecuciones + 1):
        solucion_inicial = generar_solucion_inicial()

        mejor_solucion, iteracion_mejor = simulated_annealing(
            solucion_inicial,
            temperatura_inicial
        )

        costo = calcular_costo(mejor_solucion)

        resultados.append(costo)
        soluciones.append(mejor_solucion)
        iteraciones_mejor.append(iteracion_mejor)

        if mejor_costo_global is None or costo < mejor_costo_global:
            mejor_costo_global = costo
            mejor_solucion_global = mejor_solucion.copy()

        print(
            f"Ejecución {ejecucion}: "
            f"costo = {costo}, "
            f"solución = {mejor_solucion}, "
            f"iteración mejor = {iteracion_mejor}"
        )

    tiempo_total = time.time() - tiempo_inicio

    resumen = {
        "resultados": resultados,
        "soluciones": soluciones,
        "iteraciones_mejor": iteraciones_mejor,
        "mejor_solucion_global": mejor_solucion_global,
        "mejor_costo_global": mejor_costo_global,
        "media": calcular_media(resultados),
        "desviacion_estandar": calcular_desviacion_estandar(resultados),
        "tiempo_total": tiempo_total,
    }

    return resumen


# Función para obtener los nombres de los subconjuntos seleccionados
def obtener_subconjuntos_seleccionados(solucion):
    subconjuntos_seleccionados = []

    for i in range(len(subconjuntos)):
        if solucion[i] == 1:
            subconjuntos_seleccionados.append(subconjuntos[i][0])

    return subconjuntos_seleccionados


# Función para imprimir el resumen final
def imprimir_resumen_resultado(resumen):
    mejor_solucion = resumen["mejor_solucion_global"]
    cobertura = obtener_cobertura(mejor_solucion)

    print("\n========== Resumen SCP - Simulated Annealing ==========")
    print("Cantidad de elementos del universo:", len(universo))
    print("Cantidad de subconjuntos:", len(subconjuntos))
    print("Vector binario mejor:", mejor_solucion)
    print("Subconjuntos seleccionados:", obtener_subconjuntos_seleccionados(mejor_solucion))
    print("Mejor costo encontrado:", resumen["mejor_costo_global"])
    print("Cobertura:", sorted(cobertura))
    print("Elementos cubiertos:", len(cobertura), "/", len(universo))
    print("Factible:", cubre_universo(mejor_solucion))
    print("Valores obtenidos:", resumen["resultados"])
    print("Media:", round(resumen["media"], 4))
    print("Desviación estándar:", round(resumen["desviacion_estandar"], 4))
    print("Iteraciones por ejecución:", max_iteraciones)
    print("Temperatura inicial:", temperatura_inicial)
    print("Alpha/enfriamiento geométrico:", alpha)
    print("Tiempo total de ejecución:", round(resumen["tiempo_total"], 6), "segundos")
    print("=======================================================")


# Entrada por teclado
def limpiar_ruta(ruta):
    """Elimina espacios y comillas accidentales al pegar una ruta."""
    return ruta.strip().strip('"').strip("'")


def main():
    global universo
    global subconjuntos

    print("Set Covering Problem - Simulated Annealing")
    print("Ingrese la ruta del archivo .txt con la instancia SCP.\n")

    ruta_archivo = limpiar_ruta(input("Ruta del archivo: "))

    if ruta_archivo == "":
        raise ValueError("Debe ingresar una ruta de archivo.")

    universo, subconjuntos = leer_instancia_scp(ruta_archivo)

    print("\nInstancia cargada correctamente.")
    print("Elementos del universo:", len(universo))
    print("Cantidad de subconjuntos:", len(subconjuntos))
    print()

    resumen = ejecutar_experimentos()

    imprimir_resumen_resultado(resumen)


main()