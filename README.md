# Set Covering Problem con Simulated Annealing

Proyecto desarrollado para resolver instancias del **Set Covering Problem (SCP)** mediante la metaheurística **Simulated Annealing**. El programa permite cargar instancias en formato `.txt`, ejecutar múltiples corridas por instancia, comparar resultados estadísticos y generar archivos de salida en formatos `.csv`, `.xlsx`, `.txt` y `.png`.

## Descripción del problema

El **Set Covering Problem** consiste en seleccionar un conjunto de subconjuntos de costo mínimo de forma que todos los elementos de un universo queden cubiertos al menos una vez.

En este proyecto, una solución se representa mediante un **vector binario**:

- `1`: el subconjunto es seleccionado.
- `0`: el subconjunto no es seleccionado.

El objetivo es minimizar el costo total de los subconjuntos seleccionados, manteniendo la factibilidad de la solución, es decir, que la unión de los subconjuntos elegidos cubra todo el universo.

## Enfoque utilizado

El algoritmo implementado utiliza **Simulated Annealing**, una metaheurística basada en búsqueda local estocástica que permite aceptar, bajo cierta probabilidad, soluciones peores durante el proceso de búsqueda. Esto ayuda a escapar de óptimos locales.

El programa utiliza:

- Generación aleatoria de una solución inicial factible.
- Movimiento por vecindario mediante cambio de un bit del vector solución.
- Criterio de aceptación de Metrópolis.
- Enfriamiento geométrico de la temperatura.
- Registro de convergencia por ejecución.
- Ejecuciones repetidas para análisis estadístico.

## Parámetros principales

| Parámetro | Valor por defecto | Descripción |
|---|---:|---|
| `max_iteraciones` | `1000` | Cantidad máxima de iteraciones por ejecución. |
| `alpha` | `0.98` | Factor de enfriamiento geométrico. |
| `temperatura_inicial` | `100` | Temperatura inicial del algoritmo. |
| `n_ejecuciones` | `10` | Cantidad de ejecuciones por instancia. |
| `SEMILLA` | `23` | Semilla base para reproducibilidad. |

## Instancias predefinidas

El código considera tres instancias complejas predefinidas:

| Nombre | Ruta en Google Colab |
|---|---|
| Pequeña | `/content/TareaOptimizacionFinal/Instancias/Complejas/01_facil.txt` |
| Mediana | `/content/TareaOptimizacionFinal/Instancias/Complejas/02_medio.txt` |
| Grande | `/content/TareaOptimizacionFinal/Instancias/Complejas/03_dificil.txt` |

También se dejan indicadas rutas para instancias simples:

```text
/content/TareaOptimizacionFinal/Instancias/Simples/SCP_simple1.txt
/content/TareaOptimizacionFinal/Instancias/Simples/SCP_simple2.txt
```

## Formato esperado de las instancias

Cada archivo de instancia debe seguir el siguiente formato:

```text
n m
costo_1 costo_2 ... costo_m
k_1 indices_de_subconjuntos_que_cubren_al_elemento_1
k_2 indices_de_subconjuntos_que_cubren_al_elemento_2
...
k_n indices_de_subconjuntos_que_cubren_al_elemento_n
```

Donde:

- `n` es la cantidad de elementos del universo.
- `m` es la cantidad de subconjuntos disponibles.
- Cada costo corresponde al costo de seleccionar un subconjunto.
- Para cada elemento, `k_i` indica cuántos subconjuntos lo cubren.
- Los índices de subconjuntos comienzan desde `1`.

Ejemplo conceptual:

```text
3 4
10 20 15 30
2 1 3
1 2
2 3 4
```

Esto representa un universo con 3 elementos y 4 subconjuntos candidatos.

## Requisitos

El programa fue preparado para ejecutarse en **Google Colab**, ya que contiene comandos propios de notebook, como:

```python
!git clone https://github.com/IgnacioGameolay/TareaOptimizacionFinal
!pip install openpyxl
```

Librerías utilizadas:

- `math`
- `random`
- `time`
- `matplotlib`
- `openpyxl`

Para ejecutar localmente, instala las dependencias necesarias:

```bash
pip install matplotlib openpyxl
```

> Nota: si se ejecuta como archivo `.py` local, se deben adaptar o eliminar las líneas que comienzan con `!`, ya que son comandos válidos en Colab/Jupyter, pero no en Python estándar.

## Modo de ejecución

Al ejecutar el programa se muestra un menú interactivo:

```text
Set Covering Problem - Simulated Annealing
Seleccione modo de ejecución:
1. Probar con una instancia específica
2. Probar con las 3 instancias predefinidas
```

### Opción 1: instancia específica

Permite ingresar manualmente la ruta de un archivo `.txt` con una instancia SCP.

El programa solicita:

```text
Ruta del archivo:
Nombre para identificar la instancia:
```

### Opción 2: instancias predefinidas

Ejecuta automáticamente las tres instancias configuradas en el código:

- Pequeña
- Mediana
- Grande

Cada instancia se ejecuta `10` veces usando semillas deterministas para permitir reproducibilidad.

## Archivos generados

Al finalizar la ejecución, el programa genera archivos de resultados y gráficos.

### Resultados tabulares

| Archivo | Descripción |
|---|---|
| `resultados_detalle.csv` | Detalle de todas las ejecuciones realizadas. |
| `resultados_resumen.csv` | Resumen estadístico por instancia. |
| `boxplot_datos.csv` | Datos calculados para boxplot: mínimo, Q1, mediana, Q3 y máximo. |
| `convergencia_detalle.csv` | Historial de convergencia por iteración y ejecución. |
| `resultados_Pequeña.csv` | Resultados individuales de la instancia pequeña. |
| `resultados_Mediana.csv` | Resultados individuales de la instancia mediana. |
| `resultados_Grande.csv` | Resultados individuales de la instancia grande. |
| `resultados.xlsx` | Archivo Excel con hojas de detalle, resumen y datos de boxplot. |

### Análisis textual

| Archivo | Descripción |
|---|---|
| `analisis_resultados.txt` | Análisis automático de estabilidad, calidad de solución y comparación entre instancias. |

### Gráficos generados

| Archivo | Descripción |
|---|---|
| `convergencia_Pequeña.png` | Convergencia de las ejecuciones de la instancia pequeña. |
| `convergencia_Mediana.png` | Convergencia de las ejecuciones de la instancia mediana. |
| `convergencia_Grande.png` | Convergencia de las ejecuciones de la instancia grande. |
| `convergencia_promedio_instancias.png` | Comparación de convergencia promedio entre instancias. |
| `boxplot_costos_instancias.png` | Distribución de costos finales por instancia. |
| `resumen_costos_instancias.png` | Comparación de mejor costo, media y peor costo por instancia. |

## Métricas reportadas

Para cada instancia, el programa reporta:

- Mejor costo encontrado.
- Peor costo encontrado.
- Media de costos.
- Desviación estándar muestral.
- Tiempo promedio de ejecución.
- Tiempo total de ejecución.
- Iteración donde se encontró la mejor solución.
- Semilla que produjo la mejor solución.
- Vector binario de la mejor solución.
- Subconjuntos seleccionados.
- Factibilidad de la solución.

## Reproducibilidad

El programa usa una semilla base y offsets por instancia:

```python
SEMILLA = 23
OFFSET_INSTANCIA = {
    "Pequeña": 0,
    "Mediana": 1000,
    "Grande": 2000,
}
```

Cada combinación de instancia y ejecución recibe una semilla única. Esto permite repetir los experimentos y obtener resultados consistentes, sin depender del orden en que se ejecuten las instancias.

## Funcionamiento general del algoritmo

1. Se lee la instancia SCP desde archivo.
2. Se valida que la unión de todos los subconjuntos pueda cubrir el universo.
3. Se genera una solución inicial aleatoria factible.
4. En cada iteración se genera un vecino cambiando un bit del vector solución.
5. Si el vecino no cubre el universo, se rechaza automáticamente.
6. Si el vecino mejora el costo, se acepta.
7. Si el vecino empeora el costo, puede aceptarse según el criterio de Metrópolis.
8. La temperatura disminuye usando enfriamiento geométrico.
9. Se guarda el mejor costo encontrado y su historial de convergencia.
10. Se repite el proceso para varias ejecuciones e instancias.

## Criterio de aceptación

El algoritmo acepta automáticamente una solución factible si mejora el costo actual. Si la solución es peor, se acepta con probabilidad:

```text
p = exp(-Δ / T)
```

Donde:

- `Δ` es la diferencia entre el costo nuevo y el costo actual.
- `T` es la temperatura actual.

A medida que la temperatura disminuye, se reduce la probabilidad de aceptar soluciones peores.

## Estructura principal del código

| Sección | Propósito |
|---|---|
| Lectura de instancia | Carga y valida archivos SCP. |
| Generación de soluciones | Crea soluciones iniciales y vecinos. |
| Funciones auxiliares | Calcula costo, cobertura y factibilidad. |
| Simulated Annealing | Ejecuta la búsqueda metaheurística. |
| Métricas | Calcula media, desviación estándar, tiempos y mejores soluciones. |
| Exportación | Guarda resultados en CSV, Excel y TXT. |
| Gráficos | Genera gráficos de convergencia, boxplot y resumen de costos. |
| `main()` | Controla el flujo completo del programa. |

## Consideraciones

- El algoritmo no garantiza encontrar el óptimo global, ya que es una metaheurística aproximada.
- La calidad de los resultados puede depender de los parámetros `temperatura_inicial`, `alpha` y `max_iteraciones`.
- La comparación entre instancias debe interpretarse considerando que los costos y tamaños pueden variar entre archivos.
- Las soluciones infactibles son rechazadas automáticamente durante el criterio de aceptación.

## Autoría

Trabajo desarrollado en el contexto de la asignatura **ICI4151-1 - Optimización**.

