def read_matrix(n, k): # Вибір університетської програми
    matrix = []
    for i in range(n):
        print(f"Альтернатива {i + 1}:")
        row = list(map(float, input().split()))
        while len(row) != k:
            print(f"Помилка: потрібно {k} оцінок. Спробуйте ще раз:")
            row = list(map(float, input().split()))
        matrix.append(row)
    return matrix

def calculate_risk_matrix(matrix, criteria_types):
    n = len(matrix)
    k = len(matrix[0])
    risk_matrix = []
    for i in range(n):
        row = []
        for j in range(k):
            col_values = [matrix[x][j] for x in range(n)]
            x_max, x_min = max(col_values), min(col_values)
            if x_max == x_min:
                r = 0
            else:
                if criteria_types[j] == 1:  # критерій максимізується
                    r = (matrix[i][j] - x_min) / (x_max - x_min)
                else:  # критерій мінімізується
                    r = (x_max - matrix[i][j]) / (x_max - x_min)
            row.append(r)
        risk_matrix.append(row)
    return risk_matrix


def calculate_utility(risk_matrix, weights):
    utilities = []
    for i in range(len(risk_matrix)):
        u = sum(risk_matrix[i][j] * weights[j] for j in range(len(weights)))
        utilities.append(u)
    return utilities

def main():
    try:
        n = int(input("Введіть кількість альтернатив n: "))
        k = int(input("Введіть кількість критеріїв k: "))
    except ValueError:
        print("Помилка: введіть ціле число.")
        return

    matrix = read_matrix(n, k)

    print("Введіть ваги критеріїв:")
    weights = list(map(float, input().split()))
    while len(weights) != k:
        print(f"Помилка: потрібно {k} ваг. Спробуйте ще раз:")
        weights = list(map(float, input().split()))
    print("Введіть тип критеріїв (1 – максимізується, 0 – мінімізується):")
    criteria_types = list(map(int, input().split()))
    while len(criteria_types) != k:
        print(f"Помилка: потрібно {k} значень. Спробуйте ще раз:")
        criteria_types = list(map(int, input().split()))

    # Розрахунок ризиків і функції корисності
    risk_matrix = calculate_risk_matrix(matrix, criteria_types)
    utilities = calculate_utility(risk_matrix, weights)
    best_index = utilities.index(max(utilities))

    # Вивід результатів
    print("\nМатриця ризиків:")
    for row in risk_matrix:
        print([round(x, 3) for x in row])
    print("\nФункції корисності:")
    for i, u in enumerate(utilities, 1):
        print(f"Альтернатива {i}: {round(u, 3)}")
    print(
        f"\nНайкраща альтернатива: {best_index + 1} (макс. корисність = {round(utilities[best_index], 3)})"
    )
if __name__ == "__main__":
    main()