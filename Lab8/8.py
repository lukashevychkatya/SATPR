import numpy as np
def print_table(title, matrix, row_labels, col_labels, row_totals=None, col_totals=None):
    print(f"\n{title}")
    header = f"{'':<12}" + "".join([f"{cl:>12}" for cl in col_labels])
    if row_totals is not None:
        header += f"{'Запаси':>10}"
    print(header)
    print("-" * len(header))
    for i, r_label in enumerate(row_labels):
        row_str = f"{r_label:<12}" + "".join([f"{matrix[i, j]:>12.0f}" for j in range(len(col_labels))])
        if row_totals is not None:
            row_str += f"{row_totals[i]:>10.0f}"
        print(row_str)
    if col_totals is not None:
        print("-" * len(header))
        col_str = f"{'Потреби':<12}" + "".join([f"{col_totals[j]:>12.0f}" for j in range(len(col_labels))])
        if row_totals is not None:
            col_str += f"{sum(col_totals):>10.0f}"
        print(col_str)

def solve_transportation_problem():
    print("Розв'язання транспортної задачі (методи пн-зх кута і потенціалів)")
    # ввод даних
    use_default = input("Використати дані за замовчуванням (варіант 10)? (y/n): ").strip().lower()
    if use_default in ['y', 'yes', 'так', '1', '']:
        m, n = 5, 7
        a = np.array([310, 260, 280, 360, 220], dtype=float)
        b = np.array([170, 200, 180, 210, 240, 180, 150], dtype=float)
        C_orig = np.array([
            [11, 19, 15, 12, 11, 15, 15],
            [8, 12, 7, 6, 16, 10, 6],
            [5, 16, 16, 21, 14, 20, 19],
            [19, 16, 7, 9, 11, 13, 11],
            [22, 8, 18, 22, 13, 6, 19]
        ], dtype=float)
    else:
        m = int(input("Введіть кількість заводів (m): "))
        n = int(input("Введіть кількість складів (n): "))
        print(f"Введіть потужності {m} заводів через пробіл:")
        a = np.array(list(map(float, input().split())), dtype=float)
        print(f"Введіть потреби {n} складів через пробіл:")
        b = np.array(list(map(float, input().split())), dtype=float)
        print(f"Введіть матрицю тарифів {m}x{n} (по {n} чисел через пробіл у кожному рядку):")
        C_orig_list = []
        for i in range(m):
            row = list(map(float, input(f"Завод A{i + 1}: ").split()))
            C_orig_list.append(row)
        C_orig = np.array(C_orig_list, dtype=float)

    # збалансування задачі
    sum_a, sum_b = np.sum(a), np.sum(b)
    print(f"\nЗагальні запаси: {sum_a:.0f} | Загальні потреби: {sum_b:.0f}")
    if sum_a == sum_b:
        print("Задача є закритою/збалансованою")
        C, a_ext, b_ext = C_orig.copy(), a.copy(), b.copy()
        row_labels = [f"A{i + 1}" for i in range(m)]
        col_labels = [f"B{j + 1}" for j in range(n)]
    elif sum_a > sum_b:
        diff = sum_a - sum_b
        print(f"Задача є відкритою (запаси > потреби на {diff:.0f}). Додамо фіктивний склад B{n + 1}.")
        b_ext = np.append(b, diff)
        a_ext = a.copy()
        C = np.hstack([C_orig, np.zeros((m, 1))])
        row_labels = [f"A{i + 1}" for i in range(m)]
        col_labels = [f"B{j + 1}" for j in range(n)] + [f"B{n + 1}(фікт)"]
    else:
        diff = sum_b - sum_a
        print(f"Задача є відкритою (потреби > запаси на {diff:.0f}). Додамо фіктивний завод A{m + 1}.")
        a_ext = np.append(a, diff)
        b_ext = b.copy()
        C = np.vstack([C_orig, np.zeros((1, n))])
        row_labels = [f"A{i + 1}" for i in range(m)] + [f"A{m + 1}(фікт)"]
        col_labels = [f"B{j + 1}" for j in range(n)]

    # метод північно-західного кута
    M, N = C.shape
    X_nw = np.zeros((M, N))
    a_rem, b_rem = a_ext.copy(), b_ext.copy()
    i, j = 0, 0
    basic = []
    while i < M and j < N:
        val = min(a_rem[i], b_rem[j])
        X_nw[i, j] = val
        basic.append((i, j))
        a_rem[i] -= val
        b_rem[j] -= val
        if a_rem[i] == 0 and i < M - 1:
            if b_rem[j] == 0 and j < N - 1:
                j += 1
                basic.append((i, j))
            i += 1
        elif b_rem[j] == 0 and j < N - 1:
            j += 1
        else:
            i += 1
            j += 1
    cost_nw = np.sum(X_nw * C)
    print_table("Початковий опорний план (пн-зх кут): ", X_nw, row_labels, col_labels, a_ext, b_ext)
    print(f"\nЗагальні витрати = {cost_nw:.0f} ")

    # метод потенціалів
    def get_cycle(start_cell, current_basic):
        nodes = list(current_basic) + [start_cell]
        rows, cols = {}, {}
        for r, c in nodes:
            rows.setdefault(r, []).append((r, c))
            cols.setdefault(c, []).append((r, c))
        changed = True
        while changed:
            changed = False
            for r, c in list(nodes):
                if (r, c) == start_cell:
                    continue
                if len([x for x in rows[r] if x in nodes]) < 2 or len([x for x in cols[c] if x in nodes]) < 2:
                    nodes.remove((r, c))
                    changed = True
        curr = start_cell
        cycle = [curr]
        search_row = True
        while True:
            next_nodes = [x for x in (rows[curr[0]] if search_row else cols[curr[1]]) if x in nodes and x != curr]
            if not next_nodes or next_nodes[0] == start_cell:
                break
            cycle.append(next_nodes[0])
            curr = next_nodes[0]
            search_row = not search_row
        return cycle
    X = X_nw.copy()
    current_basic = list(basic)
    iteration = 0
    while True:
        iteration += 1
        u, v = [None] * M, [None] * N
        u[0] = 0.0
        while True:
            updated = False
            for (r, c) in current_basic:
                if u[r] is not None and v[c] is None:
                    v[c] = C[r, c] - u[r]
                    updated = True
                elif u[r] is None and v[c] is not None:
                    u[r] = C[r, c] - v[c]
                    updated = True
            if not updated:
                break
        Delta = np.zeros((M, N))
        max_delta = -1e9
        enter_cell = None
        for i_idx in range(M):
            for j_idx in range(N):
                if (i_idx, j_idx) not in current_basic:
                    Delta[i_idx, j_idx] = u[i_idx] + v[j_idx] - C[i_idx, j_idx]
                    if Delta[i_idx, j_idx] > max_delta:
                        max_delta = Delta[i_idx, j_idx]
                        enter_cell = (i_idx, j_idx)
        if max_delta <= 1e-9:
            print("\nДосягнуто оптимальний план перевезень ")
            break
        cycle = get_cycle(enter_cell, current_basic)
        minus_cells = cycle[1::2]
        plus_cells = cycle[0::2]
        theta = min(X[r, c] for (r, c) in minus_cells)
        leaving_cell = [cell for cell in minus_cells if X[cell] == theta][0]
        for (r, c) in plus_cells:
            X[r, c] += theta
        for (r, c) in minus_cells:
            X[r, c] -= theta
        current_basic.remove(leaving_cell)
        current_basic.append(enter_cell)
    cost_opt = np.sum(X * C)
    print_table(" Оптимальний план перевезень:", X, row_labels, col_labels, a_ext, b_ext)
    print(f"\nМінімальні сумарні витрати = {cost_opt:.0f} ")
if __name__ == "__main__":
    solve_transportation_problem()