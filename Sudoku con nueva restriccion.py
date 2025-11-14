import time

# Bandera para activar o desactivar la restriccion de diagonal
# Si es True, no se permite repetir valores en la anti diagonal (de derecha a izquierda).
REGLA_DIAGONAL_ANTI = True
contadorIntentos = 0  # Contador de intentos realizados

def encontrar_espacio_vacio(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None, None


def movimientoValido(tablero, fila, col, num):
    # Verificar fila
    for x in range(9):
        if tablero[fila][x] == num:
            return False

    # Verificar columna
    for x in range(9):
        if tablero[x][col] == num:
            return False

    # Verificar subgrilla 3x3
    fila_inicial, col_inicial = 3 * (fila // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tablero[i + fila_inicial][j + col_inicial] == num:
                return False

    # Verificar la anti diagonal (de derecha a izquierda).
    # Esta regla solo aplica si REGLA_DIAGONAL_ANTI es True y la celda esta en la anti diagonal.
    if REGLA_DIAGONAL_ANTI and (fila + col == 8):
        for r in range(9):
            c = 8 - r
            if tablero[r][c] == num:
                return False
    return True


def impresion(tablero):
    for fila in tablero:
        print(fila)


def solucion1_FB(tablero):
    global contadorIntentos
    fila, col = encontrar_espacio_vacio(tablero)

    if fila is None:  # Si no hay espacios vacios, el tablero esta completo
        return tablero

    for num in range(1, 10):  # Prueba del 1 al 9
        if movimientoValido(tablero, fila, col, num):
            tablero[fila][col] = num  # Intentamos colocar el número
            contadorIntentos += 1  # Contar intento

            resultado = solucion1_FB(tablero)  # Llamada recursiva
            if resultado:
                return resultado  # Si encuentra solución, la retorna

            tablero[fila][col] = 0  # Retrocede si no funciona

    return False  # No hay solución


def solucion2_BT(tablero):
    global contadorIntentos

    def obtenerPosibilidades(fila, col):
        posibilidades = set(range(1, 10))
        for x in range(9):
            posibilidades.discard(tablero[fila][x])
            posibilidades.discard(tablero[x][col])

        fila_inicial, col_inicial = 3 * (fila // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                posibilidades.discard(tablero[fila_inicial + i][col_inicial + j])

        # Verificar la anti diagonal: eliminar valores ya presentes en la anti diagonal si la celda esta en ella
        if REGLA_DIAGONAL_ANTI and (fila + col == 8):
            for r in range(9):
                val = tablero[r][8 - r]
                if val != 0:
                    posibilidades.discard(val)

        return list(posibilidades)

    def obtener_mejor_celda():
        mejor_fila, mejor_col = None, None
        mejor_opciones = 10
        for i in range(9):
            for j in range(9):
                if tablero[i][j] == 0:
                    opciones = obtenerPosibilidades(i, j)
                    if len(opciones) < mejor_opciones:
                        mejor_opciones = len(opciones)
                        mejor_fila, mejor_col = i, j
        return mejor_fila, mejor_col

    def backtrack():
        global contadorIntentos
        fila, col = obtener_mejor_celda()
        if fila is None:
            return True

        for num in obtenerPosibilidades(fila, col):
            contadorIntentos += 1
            tablero[fila][col] = num
            if backtrack():
                return True
            tablero[fila][col] = 0

        return False

    resultado = backtrack()
    return tablero if resultado else False



def solucion3_BT_FC(tablero):
    """
    Backtracking con comprobacion hacia adelante (Forward Checking).
    Mantiene contadorIntentos como global (si existe en el modulo).
    """
    try:
        global contadorIntentos
    except NameError:
        contadorIntentos = 0

    # Dominios iniciales: para cada celda vacía, conjunto de valores posibles
    dominios = [[set() for _ in range(9)] for _ in range(9)]
    for f in range(9):
        for c in range(9):
            if tablero[f][c] == 0:
                posibles = set(range(1, 10))
                for x in range(9):
                    posibles.discard(tablero[f][x])
                    posibles.discard(tablero[x][c])
                fi, ci = 3 * (f // 3), 3 * (c // 3)
                for i in range(3):
                    for j in range(3):
                        posibles.discard(tablero[fi + i][ci + j])
                # Eliminar valores presentes en la anti diagonal si la celda pertenece a ella
                if REGLA_DIAGONAL_ANTI and (f + c == 8):
                    for r in range(9):
                        val = tablero[r][8 - r]
                        if val != 0:
                            posibles.discard(val)
                dominios[f][c] = posibles

    def vecinos(fila, col):
        """Celdas vacías de la misma fila, columna y subcuadrícula."""
        for x in range(9):
            if x != col and tablero[fila][x] == 0:
                yield fila, x
            if x != fila and tablero[x][col] == 0:
                yield x, col
        fi, ci = 3 * (fila // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                rf, rc = fi + i, ci + j
                if (rf, rc) != (fila, col) and tablero[rf][rc] == 0:
                    yield rf, rc

        # Si la restriccion de diagonal esta activa y la celda esta en la anti diagonal,
        # incluir tambien como vecinos a las demas celdas de la anti diagonal.
        if REGLA_DIAGONAL_ANTI and (fila + col == 8):
            for r in range(9):
                c = 8 - r
                if (r, c) != (fila, col) and tablero[r][c] == 0:
                    yield r, c

    def seleccionarCeldaMrvDom():
        mejor, mf, mc = 10, None, None
        for f in range(9):
            for c in range(9):
                if tablero[f][c] == 0:
                    n = len(dominios[f][c])
                    if n < mejor:
                        mejor, mf, mc = n, f, c
        return mf, mc

    def esValido(fila, col, valor):
        # Fila y Columna
        for x in range(9):
            if tablero[fila][x] == valor or tablero[x][col] == valor:
                return False
        # Caja
        fi, ci = 3 * (fila // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if tablero[fi + i][ci + j] == valor:
                    return False
        # Verificar la anti diagonal para la regla opcional.
        if REGLA_DIAGONAL_ANTI and (fila + col == 8):
            for r in range(9):
                c = 8 - r
                # omite la celda actual (fila,col) porque aun no se ha asignado valor
                if tablero[r][c] == valor:
                    return False
        return True

    def asignarYPodar(fila, col, valor):
        """Elimina 'valor' de dominios de vecinos. Devuelve lista de (f,c,v) podados; None si inconsistencia."""
        podas = []
        for vf, vc in vecinos(fila, col):
            if valor in dominios[vf][vc]:
                dominios[vf][vc].remove(valor)
                podas.append((vf, vc, valor))
                if not dominios[vf][vc]:
                    # restaurar
                    for rf, rc, v in reversed(podas):
                        dominios[rf][rc].add(v)
                    return None
        return podas

    def restaurarPodas(podas):
        for f, c, v in reversed(podas):
            dominios[f][c].add(v)

    def bt():
        f, c = seleccionarCeldaMrvDom()
        if f is None:  # sin vacíos
            return True
        if f is None or c is None:
            return False
        for valor in sorted(dominios[f][c]):
            if not esValido(f, c, valor):
                continue
            tablero[f][c] = valor
            try:
                contadorIntentos += 1
            except Exception:
                pass
            podas = asignarYPodar(f, c, valor)
            if podas is not None and bt():
                return True
            # revertir
            tablero[f][c] = 0
            if podas is not None:
                restaurarPodas(podas)
        return False

    ok = bt()
    return tablero if ok else None

def probar_algoritmo(funcion, tablero):
    global contadorIntentos
    contadorIntentos = 0  # Resetear intentos antes de cada prueba

    # Copia del tablero para no modificar el original
    tablero_copia = [fila[:] for fila in tablero]

    # Medir tiempo de ejecución
    inicio = time.perf_counter()
    resultado = funcion(tablero_copia)
    fin = time.perf_counter()

    # Imprimir resultados
    print(f"\n {funcion.__name__}:")
    print(f"  Tiempo de ejecucion: {fin - inicio:.10f} segundos.")
    print(f"  Intentos realizados: {contadorIntentos}")
    if resultado:
        print("  Sudoku resuelto correctamente.")
    else:
        print("  No se encontro solucion.")


if __name__ == "__main__":
    # Tablero inicial para probar la solucion con la regla diagonal.
    # Esta configuracion cumple que los valores en la anti diagonal (de derecha a izquierda)
    # no se repitan y permite una solucion unica. Si desea resolver un Sudoku convencional
    # sin esta restriccion, establezca REGLA_DIAGONAL_ANTI = False y utilice otro tablero.
    tablero = [
        [0, 0, 0, 0, 0, 0, 4, 3, 5],
        [4, 0, 0, 0, 0, 0, 7, 6, 0],
        [0, 0, 0, 0, 3, 0, 1, 0, 2],
        [0, 0, 0, 3, 0, 2, 0, 0, 9],
        [0, 0, 0, 6, 4, 5, 0, 0, 0],
        [0, 0, 0, 9, 0, 8, 5, 0, 0],
        [0, 0, 8, 0, 5, 6, 0, 0, 0],
        [0, 7, 0, 4, 0, 0, 0, 0, 1],
        [3, 0, 0, 1, 0, 0, 0, 5, 0],
    ]

    probar_algoritmo(solucion1_FB, tablero)
    probar_algoritmo(solucion2_BT, tablero)
    probar_algoritmo(solucion3_BT_FC, tablero)

    print("\nSolucion:")
    resultado = solucion2_BT(tablero)
    if resultado is False:
        print("No se encontro solucion.")
    elif isinstance(resultado, str):
        print(resultado)
    else:
        for fila in resultado:
            print(fila)