import numpy as np
def main():
    print("Лабораторна робота №7 - теорія ігор. Варіант №10")

    # частина1
    print("\nЧастина 1: задача 10 -матриця 4х4")
    rows = int(input("Введіть кількість рядків (напр. 4): "))
    cols = int(input("Введіть кількість стовпчиків (напр. 4): "))
    print(f"\nВведіть значення матриці {rows}x{cols} по рядках через пробіл:")
    matrix_1 = []
    for i in range(rows):
        row = list(map(float, input(f"Рядок A{i + 1}: ").split()))
        while len(row) != cols:
            print(f"Помилка. Введіть рівно {cols} чисел")
            row = list(map(float, input(f"Рядок A{i + 1}: ").split()))
        matrix_1.append(row)
    A1 = np.array(matrix_1)
    row_mins_1 = np.min(A1, axis=1)
    col_maxs_1 = np.max(A1, axis=0)
    alpha_1 = np.max(row_mins_1)
    beta_1 = np.min(col_maxs_1)
    print("\nРезультати частини 1:")
    print(f"Мінімуми по рядках: {row_mins_1}")
    print(f"Максимуми по стовпцях: {col_maxs_1}")
    print(f"Нижня ціна гри (alpha) = {alpha_1}")
    print(f"Верхня ціна гри (beta) = {beta_1}")
    if alpha_1 == beta_1:
        print(f"-> Є сідлова точка у чистих стратегіях. Ціна гри V = {alpha_1}")
    else:
        print("-> Сідлова точка відсутня (alpha != beta). Потрібен перехід до змішаних стратегій")

    # частина 2
    print("\nЧастина 2: задача 10 - маршрути Джека")
    fine = float(input("Введіть розмір штрафу ($): "))  # 100
    extra_gas = float(input("Введіть додаткові витрати на бензин для В ($): "))  # 15
    prob_b3_a = float(input("Ймовірність штрафу на А при поліції 50/50 (наприклад, 0.5): "))  # 0.5
    prob_b3_b = float(input("Ймовірність штрафу на В при поліції 50/50 (наприклад, 0.3): "))  # 0.3

    # матриця витрат
    cost_A_B1 = fine
    cost_A_B2 = 0.0
    cost_A_B3 = prob_b3_a * fine
    cost_B_B1 = extra_gas
    cost_B_B2 = fine + extra_gas
    cost_B_B3 = prob_b3_b * fine + extra_gas
    print("\nСформована матриця витрат ($):")
    print(f"Маршрут А: [{cost_A_B1:.1f}, {cost_A_B2:.1f}, {cost_A_B3:.1f}]")
    print(f"Маршрут В: [{cost_B_B1:.1f}, {cost_B_B2:.1f}, {cost_B_B3:.1f}]")
    a11 = -cost_A_B1
    a12 = -cost_A_B2
    a21 = -cost_B_B1
    a22 = -cost_B_B2
    denom = (a11 + a22) - (a12 + a21)
    p1 = (a22 - a21) / denom
    p2 = 1 - p1
    exp_cost = p1 * cost_A_B1 + p2 * cost_B_B1
    print("\nРезультати частини 2:")
    print(f"Оптимальна ймовірність вибору маршруту А = {p1:.2f} ({p1 * 100:.0f}%)")
    print(f"Оптимальна ймовірність вибору маршруту В = {p2:.2f} ({p2 * 100:.0f}%)")
    print(f"Мінімальні очікувані середні витрати = {exp_cost:.2f} $")
if __name__ == "__main__":
    main()