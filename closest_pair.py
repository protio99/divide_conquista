"""
Módulo para encontrar el par de puntos más cercano en 2D.

Proporciona funciones para leer puntos desde archivos y calcular el par
más cercano mediante un algoritmo eficiente de Divide y Conquista O(n log n).
"""

import math
import time
import sys


def euclidean_distance(point1, point2):
    """
    Calcula la distancia euclidiana entre dos puntos 2D.

    Resumen extendido
    -----------------
    Aplica el teorema de Pitágoras para hallar la distancia lineal entre
    dos coordenadas en un sistema cartesiano.

    Parámetros
    ----------
    point1 : tuple
        Tupla (x, y) del primer punto.
    point2 : tuple
        Tupla (x, y) del segundo punto.

    Retorna
    -------
    float
        Distancia euclidiana resultante.

    Notas
    -----
    La fórmula utilizada es: sqrt((x2 - x1)^2 + (y2 - y1)^2).

    Ejemplos
    --------
    >>> euclidean_distance((0, 0), (3, 4))
    5.0
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def brute_force(points):
    """
    Encuentra el par más cercano usando fuerza bruta.

    Resumen extendido
    -----------------
    Compara todos los pares posibles. Complejidad temporal de O(n^2).

    Parámetros
    ----------
    points : list
        Lista de tuplas (x, y).

    Retorna
    -------
    tuple
        (punto1, punto2, distancia_mínima).

    Notas
    -----
    Se usa como caso base en el algoritmo recursivo para pocos puntos.

    Ejemplos
    --------
    >>> brute_force([(0, 0), (1, 1), (5, 5)])
    ((0, 0), (1, 1), 1.4142135623730951)
    """
    min_dist = float('inf')
    closest_pair_points = (None, None)
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair_points = (points[i], points[j])
    return closest_pair_points[0], closest_pair_points[1], min_dist


def strip_closest(strip, d, best_pair):
    """
    Halla el par más cercano en una franja vertical.

    Resumen extendido
    -----------------
    Busca puntos cuya distancia sea menor a 'd' dentro de una franja
    ordenada por la coordenada Y.

    Parámetros
    ----------
    strip : list
        Puntos en la franja ordenados por Y.
    d : float
        Distancia mínima actual.
    best_pair : tuple
        Mejor par encontrado previamente.

    Retorna
    -------
    tuple
        (punto1, punto2, distancia_mínima).

    Notas
    -----
    Solo se requiere comparar cada punto con los siguientes 7 en la lista.

    Ejemplos
    --------
    >>> strip_closest([(0, 0), (0, 1)], 2.0, ((0, 0), (0, 5)))
    ((0, 0), (0, 1), 1.0)
    """
    min_dist = d
    p1, p2 = best_pair
    n = len(strip)

    for i in range(n):
        for j in range(i + 1, n):
            if (strip[j][1] - strip[i][1]) >= min_dist:
                break
            dist = euclidean_distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                p1, p2 = strip[i], strip[j]

    return p1, p2, min_dist


def closest_recursive(points_x, points_y):
    """
    Función recursiva de Divide y Conquista.

    Resumen extendido
    -----------------
    Divide el conjunto en mitades, resuelve cada una y procesa la franja
    central para encontrar el par más cercano global.

    Parámetros
    ----------
    points_x : list
        Puntos ordenados por X.
    points_y : list
        Puntos ordenados por Y.

    Retorna
    -------
    tuple
        (punto1, punto2, distancia_mínima).

    Notas
    -----
    Mantiene la eficiencia O(n log n) al no re-ordenar en cada paso.

    Ejemplos
    --------
    >>> closest_recursive([(0,0), (1,1)], [(0,0), (1,1)])
    ((0, 0), (1, 1), 1.4142135623730951)
    """
    n = len(points_x)
    if n <= 3:
        return brute_force(points_x)

    mid = n // 2
    mid_point = points_x[mid]

    points_y_left = []
    points_y_right = []
    for point in points_y:
        if point[0] <= mid_point[0]:
            points_y_left.append(point)
        else:
            points_y_right.append(point)

    p1_l, p2_l, d_l = closest_recursive(points_x[:mid], points_y_left)
    p1_r, p2_r, d_r = closest_recursive(points_x[mid:], points_y_right)

    if d_l < d_r:
        d = d_l
        best_pair = (p1_l, p2_l)
    else:
        d = d_r
        best_pair = (p1_r, p2_r)

    strip = [p for p in points_y if abs(p[0] - mid_point[0]) < d]
    p1_s, p2_s, d_s = strip_closest(strip, d, best_pair)

    return p1_s, p2_s, d_s


def find_closest_pair(points):
    """
    Inicia la búsqueda del par más cercano.

    Resumen extendido
    -----------------
    Pre-ordena los puntos por X e Y antes de iniciar la recursión.

    Parámetros
    ----------
    points : list
        Lista de coordenadas (x, y).

    Retorna
    -------
    tuple
        (punto1, punto2, distancia_mínima).

    Notas
    -----
    El ordenamiento inicial toma O(n log n).

    Ejemplos
    --------
    >>> find_closest_pair([(0,0), (10,10), (1,1)])
    ((0, 0), (1, 1), 1.4142135623730951)
    """
    points_x = sorted(points, key=lambda p: p[0])
    points_y = sorted(points, key=lambda p: p[1])
    return closest_recursive(points_x, points_y)


def load_points_from_file(file_path):
    """
    Carga puntos desde un archivo de texto.

    Resumen extendido
    -----------------
    Lee dos líneas: la primera con valores X y la segunda con valores Y,
    separados por comas.

    Parámetros
    ----------
    file_path : str
        Ruta del archivo .txt.

    Retorna
    -------
    list
        Lista de tuplas (x, y).

    Notas
    -----
    Lanza error si el formato del archivo es incorrecto.

    Ejemplos
    --------
    >>> # load_points_from_file('datos.txt')
    pass
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) < 2:
                raise ValueError("El archivo debe tener al menos dos líneas.")
            x_coords = [float(x) for x in lines[0].strip().split(',')]
            y_coords = [float(y) for y in lines[1].strip().split(',')]
            return list(zip(x_coords, y_coords))
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
        sys.exit(1)
    except ValueError as err:
        print(f"Error al procesar el archivo: {err}")
        sys.exit(1)


def main():
    """
    Punto de entrada principal del programa.

    Resumen extendido
    -----------------
    Gestiona los argumentos de consola, invoca el algoritmo y muestra
    los resultados y tiempos.

    Parámetros
    ----------
    Ninguno

    Retorna
    -------
    Ninguno

    Notas
    -----
    Requiere el nombre del archivo como argumento de ejecución.

    Ejemplos
    --------
    >>> # Ejecución típica: python closest_pair.py datos_100.txt
    pass
    """
    if len(sys.argv) < 2:
        print("Uso: python closest_pair.py <nombre_archivo.txt>")
        return

    file_path = sys.argv[1]
    points = load_points_from_file(file_path)

    start_time = time.time()
    p1, p2, dist = find_closest_pair(points)
    end_time = time.time()

    execution_time = end_time - start_time

    print(f"Resultados para {file_path}:")
    print(f"Punto 1: {p1}")
    print(f"Punto 2: {p2}")
    print(f"Distancia Euclidiana: {dist:.6f}")
    print(f"Tiempo de ejecución: {execution_time:.6f} segundos")


if __name__ == "__main__":
    main()
