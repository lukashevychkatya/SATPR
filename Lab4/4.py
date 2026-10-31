import numpy as np
import pandas as pd
# Таблиця середніх значень індексу випадкової узгодженості за Сааті
RI_TABLE = {
    1: 0.0,
    2: 0.0,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
}
def calculate_ahp(matrix):
    n = matrix.shape[0]
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_index = np.argmax(np.real(eigvals))
    lambda_max = np.real(eigvals[max_index])
    # Власний вектор, нормований до суми 1
    weights = np.real(eigvecs[:, max_index])
    weights = weights / np.sum(weights)
    # Індекс узгодженості (CI) та відношення узгодженості (CR)
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri = RI_TABLE.get(n, 1.49)
    cr = ci / ri if ri > 0 else 0.0

    return weights, lambda_max, ci, cr

def main():
    print("Лабораторна робота №4: ")
    print("Задача 10: вибір авто")
    alt_names = [
        "A1: престижна іномарка",
        "A2: економічна малолітражка",
        "A3: новий автомобіль підв. прохідності",
    ]
    crit_names = [
        "K1: місткість",
        "K2: потужність двигуна",
        "K3: комфорт",
        "K4: забезпеченість запчастинами",
        "K5: ціна",
        "K6: рік випуску",
        "K7: надійність",
        "K8: економічність",
        "K9: дизайн",
    ]
    choice = (
        input(
            "\nВикористати готові експертні матриці? (Enter або т - так, н - ввести вручну): "
        )
        .strip()
        .lower()
    )
    if choice in ["", "т", "так", "y", "yes"]:
        # Матриця попарних порівнянь критеріїв
        criteria_matrix = np.array([
            [1.0, 1 / 2, 1 / 2, 1 / 2, 1 / 4, 1 / 2, 1 / 4, 1 / 2, 1.0],  # K1
            [2.0, 1.0, 1 / 2, 1.0, 1 / 3, 1.0, 1 / 3, 1 / 2, 2.0],  # K2
            [2.0, 2.0, 1.0, 1.0, 1 / 2, 2.0, 1 / 2, 1.0, 2.0],  # K3
            [2.0, 1.0, 1.0, 1.0, 1 / 3, 1.0, 1 / 2, 1 / 2, 2.0],  # K4
            [4.0, 3.0, 2.0, 3.0, 1.0, 3.0, 1.0, 2.0, 4.0],  # K5
            [2.0, 1.0, 1 / 2, 1.0, 1 / 3, 1.0, 1 / 3, 1 / 2, 1.0],  # K6
            [4.0, 3.0, 2.0, 2.0, 1.0, 3.0, 1.0, 2.0, 4.0],  # K7
            [2.0, 2.0, 1.0, 2.0, 1 / 2, 2.0, 1 / 2, 1.0, 2.0],  # K8
            [1.0, 1 / 2, 1 / 2, 1 / 2, 1 / 4, 1.0, 1 / 4, 1 / 2, 1.0],  # K9
        ])

        # Матриці порівняння трьох альтернатив за кожним з 9 критеріїв (3х3)
        alts = {
            "K1": np.array(
                [[1.0, 3.0, 1 / 3], [1 / 3, 1.0, 1 / 6], [3.0, 6.0, 1.0]]
            ),
            "K2": np.array(
                [[1.0, 5.0, 2.0], [1 / 5, 1.0, 1 / 3], [1 / 2, 3.0, 1.0]]
            ),
            "K3": np.array(
                [[1.0, 5.0, 2.0], [1 / 5, 1.0, 1 / 3], [1 / 2, 3.0, 1.0]]
            ),
            "K4": np.array(
                [[1.0, 1 / 4, 1 / 2], [4.0, 1.0, 2.0], [2.0, 1 / 2, 1.0]]
            ),
            "K5": np.array(
                [[1.0, 1 / 5, 1 / 3], [5.0, 1.0, 2.0], [3.0, 1 / 2, 1.0]]
            ),
            "K6": np.array(
                [[1.0, 1 / 3, 1 / 5], [3.0, 1.0, 1 / 2], [5.0, 2.0, 1.0]]
            ),
            "K7": np.array(
                [[1.0, 3.0, 1 / 2], [1 / 3, 1.0, 1 / 4], [2.0, 4.0, 1.0]]
            ),
            "K8": np.array(
                [[1.0, 1 / 6, 1 / 3], [6.0, 1.0, 3.0], [3.0, 1 / 3, 1.0]]
            ),
            "K9": np.array(
                [[1.0, 4.0, 2.0], [1 / 4, 1.0, 1 / 3], [1 / 2, 3.0, 1.0]]
            ),
        }
    else:
        # Ввід в консоль
        k_num = int(input("Введіть кількість критеріїв: "))
        crit_names = [
            input(f"Назва критерію {i+1}: ").strip() for i in range(k_num)
        ]
        print(
            f"\nВведіть матрицю попарних порівнянь критеріїв {k_num}x{k_num} (елементи рядка через пробіл):"
        )
        c_list = []
        for i in range(k_num):
            row = list(map(float, input(f"Рядок {i+1}: ").split()))
            c_list.append(row)
        criteria_matrix = np.array(c_list)
        a_num = int(input("\nВведіть кількість альтернатив: "))
        alt_names = [
            input(f"Назва альтернативи {i+1}: ").strip() for i in range(a_num)
        ]
        alts = {}
        for c_name in crit_names:
            print(
                f"\nВведіть матрицю попарних порівнянь альтернатив {a_num}x{a_num} для критерію '{c_name}':"
            )
            a_list = []
            for i in range(a_num):
                row = list(map(float, input(f"Рядок {i+1}: ").split()))
                a_list.append(row)
            alts[c_name] = np.array(a_list)

    # Розрахунок ваг критеріїв
    crit_weights, lambda_c, ci_c, cr_c = calculate_ahp(criteria_matrix)
    print("\nВаги і узгодженість критеріїв ")
    df_crit = pd.DataFrame({
        "Критерій": crit_names,
        "Вага (Wнорм)": np.round(crit_weights, 4),
        "Частка (%)": np.round(crit_weights * 100, 2),
    })
    print(df_crit.to_string(index=False))
    print(f"\nλmax = {lambda_c:.4f}, CI = {ci_c:.4f}, CR = {cr_c:.4f}")
    print(
        "Узгоджено (CR < 0.10)"
        if cr_c < 0.10
        else "Неузгоджено (CR >= 0.10)"
    )

    # Розрахунок локальних пріоритетів альтернатив
    local_weights = {}
    print("\nУзгодженість матриць за критеріями")
    for key, matrix in alts.items():
        w, l_max, ci, cr = calculate_ahp(matrix)
        local_weights[key] = w
        status = "Узгоджено" if cr < 0.10 else "Неузгоджено"
        print(
            f"Критерій {key:<4}: λmax = {l_max:.4f}, CI = {ci:.4f}, CR = {cr:.4f} -> {status}"
        )
    df_local = pd.DataFrame(local_weights, index=alt_names)
    print("\nТаблиця локальних пріоритетів альтернатив:")
    print(df_local.round(4))

    # Розрахунок глобальних пріоритетів
    global_scores = df_local.values.dot(crit_weights)
    df_global = pd.DataFrame({
        "Альтернатива": alt_names,
        "Глобальний пріоритет": np.round(global_scores, 4),
        "Частка (%)": np.round(global_scores * 100, 2),
    }).sort_values("Глобальний пріоритет", ascending=False)
    df_global["Ранг"] = range(1, len(df_global) + 1)
    print("\nПідсумкові глобальні пріоритети альтернатив ")
    print(df_global.to_string(index=False))
    best_alt = df_global.iloc[0]["Альтернатива"]
    best_weight = df_global.iloc[0]["Глобальний пріоритет"]
    best_pct = df_global.iloc[0]["Частка (%)"]
    print("\nВисновок ")
    print(
        f"Найкраща альтернатива: {best_alt}\n"
        f"Глобальна вага: {best_weight:.4f} ({best_pct}% загального пріоритету)."
    )
if __name__ == "__main__":
    main()