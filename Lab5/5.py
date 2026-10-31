import numpy as np
from scipy.optimize import linear_sum_assignment

def read_data():
    try:
        n = int(input("Введіть кількість працівників n: "))
        k = int(input("Введіть кількість змін k: "))
    except ValueError:
        print("Потрібно ввести ціле число ")
        return None, None, None, None, None

    print(f"\nВведіть тривалість для {k} змін через пробіл (наприклад: 8 6 10):")
    shift_durations = list(map(float, input().split()))
    while len(shift_durations) != k:
        print(f"Потрібно ввести точно {k} значень. Спробуйте ще раз: ")
        shift_durations = list(map(float, input().split()))

    worker_names = []
    worker_limits = []
    print(f"\nВведіть назву працівника та його макс. робочий час через пробіл (наприклад: Працівник_A 10):")
    for i in range(n):
        entry = input(f"Працівник {i + 1}: ").split()
        while len(entry) < 2:
            print("Введіть назву і допустимий час. Спробуйте ще раз:")
            entry = input(f"Працівник {i + 1}: ").split()
        worker_names.append(entry[0])
        worker_limits.append(float(entry[1]))

    return n, k, shift_durations, worker_names, worker_limits


def build_cost_matrix(n, k, shift_durations, worker_limits):
    M = 999999.0  # штрафне значення для заборонених варіантів
    cost_matrix = np.zeros((n, k))

    for i in range(n):
        for j in range(k):
            if shift_durations[j] > worker_limits[i]:
                cost_matrix[i][j] = M
            else:
                cost_matrix[i][j] = shift_durations[j]

    return cost_matrix, M


def main():
    print("Лабораторна робота №5. Задача про призначення (варіант10, задача10)")

    n, k, shift_durations, worker_names, worker_limits = read_data()
    if n is None:
        return

    # матриця вартостей
    cost_matrix, M = build_cost_matrix(n, k, shift_durations, worker_limits)

    print("\nСформована матриця навантажень (з урахуванням штрафу M):")
    for i in range(n):
        row_view = [f"{cost_matrix[i][j]:.0f}" if cost_matrix[i][j] < M else "M (Заборонено)" for j in range(k)]
        print(f"{worker_names[i]} (макс {worker_limits[i]:.0f}г):", row_view)

    # угорський метод
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    print("\nРезультати оптимізації: ")
    total_load = 0
    max_load = 0

    for r, c in zip(row_ind, col_ind):
        w_name = worker_names[r]
        shift_dur = shift_durations[c]
        limit = worker_limits[r]
        if cost_matrix[r][c] >= M:
            print("Неможливо розподілити зміни без порушення лімітів ")
            return

        total_load += shift_dur
        if shift_dur > max_load:
            max_load = shift_dur
        print(f"• {w_name} -> Зміна {c + 1} ({shift_dur:.0f} год) [Макс. ліміт: {limit:.0f} год] — OK")
    print(f"\nЗагальне сумарне навантаження: {total_load:.0f} годин")
    print(f"Максимальне навантаження серед працівників: {max_load:.0f} годин")

if __name__ == "__main__":
    main()

