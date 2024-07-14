# from munkres import Munkres, make_cost_matrix
# import math
# import munkres

import numpy as np
from munkres import Munkres, make_cost_matrix


class CustomMunkres(Munkres):
    def __init__(self):
        super().__init__()
        self.steps = []

    def compute(self, cost_matrix):
        matrix = self._copy_matrix(cost_matrix)
        self.steps.append(self._format_matrix(matrix))

        # Subtract row minima
        self.subtract_row_minimum(matrix)
        self.steps.append(self._format_matrix(matrix))

        # Subtract column minima
        self.subtract_column_minimum(matrix)
        self.steps.append(self._format_matrix(matrix))

        # Cover zeros and add additional lines if necessary
        while True:
            covered_rows, covered_columns = self.cover_zeros(matrix)
            self.steps.append(self._format_matrix(matrix))
            if len(covered_rows) + len(covered_columns) >= len(matrix):
                break
            else:
                self.add_additional_lines(
                    matrix, covered_rows, covered_columns)
                self.steps.append(self._format_matrix(matrix))

        indices = self._find_assignments(matrix)
        return indices

    def subtract_row_minimum(self, matrix):
        for row in matrix:
            minval = min(row)
            for j in range(len(row)):
                row[j] -= minval

    def subtract_column_minimum(self, matrix):
        for j in range(len(matrix[0])):
            col = [matrix[i][j] for i in range(len(matrix))]
            minval = min(col)
            for i in range(len(matrix)):
                matrix[i][j] -= minval

    def cover_zeros(self, matrix):
        row_covered = [False] * len(matrix)
        col_covered = [False] * len(matrix[0])

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0 and not row_covered[i] and not col_covered[j]:
                    row_covered[i] = True
                    col_covered[j] = True

        return row_covered, col_covered

    def add_additional_lines(self, matrix, row_covered, col_covered):
        minval = float('inf')
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if not row_covered[i] and not col_covered[j]:
                    minval = min(minval, matrix[i][j])

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if row_covered[i] and not col_covered[j]:
                    matrix[i][j] += minval
                elif not row_covered[i] and not col_covered[j]:
                    matrix[i][j] -= minval

    def _find_assignments(self, matrix):
        assignments = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    assignments.append((i, j))
                    break
        return assignments

    def _copy_matrix(self, matrix):
        return [row[:] for row in matrix]

    def _format_matrix(self, matrix):
        return "\n".join(["\t".join(map(str, row)) for row in matrix])

    def print_steps(self, text_widget=None):
        for step_number, matrix_str in enumerate(self.steps, start=1):
            step_text = f"Paso {step_number}:\n{matrix_str}\n"
            if text_widget:
                text_widget.insert("end", step_text + "\n")
            else:
                print(step_text)


def Aplicar_Metodo(matriz, modo='min'):

    m = Munkres()

    if modo == 'max':
        matriz = make_cost_matrix(matriz)

    asignaciones = m.compute(matriz)

    asignacionOptima = []
    total = 0

    for row, col in asignaciones:
        valor = matriz[row][col]
        asignacionOptima.append((row, col))
        total += valor

    if modo == 'max':
        # If maximizing, the total should be recalculated from the original profit matrix
        total = sum(matriz[row][col] for row, col in asignaciones)

    return asignacionOptima, total


def make_cost_matrix_from_max(profit_matrix):
    max_value = np.max(profit_matrix)
    cost_matrix = [[max_value - cell for cell in row] for row in profit_matrix]
    return cost_matrix


def Aplicar_Metodo_Pasos(matriz, modo='min', text_widget=None):
    m = CustomMunkres()

    if modo == 'max':
        matriz = make_cost_matrix_from_max(matriz)

    asignaciones = m.compute(matriz)
    asignacionOptima = []
    cost_total = 0

    for row, col in asignaciones:
        costo = matriz[row][col]
        asignacionOptima.append((row, col))
        cost_total += costo

    # Recalculate total if maximizing using the original profit matrix
    if modo == 'max':
        cost_total = sum(matriz[row][col] for row, col in asignaciones)

    # Show the steps in the text widget if provided
    if text_widget:
        text_widget.insert(
            "end", "Matrices intermedias durante el algoritmo:\n")
        m.print_steps(text_widget)

    return asignacionOptima, cost_total
