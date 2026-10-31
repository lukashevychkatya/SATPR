import pandas as pd

def main():
  print("Прийняття рішень в умовах невизначеності ")
  try:
    n = int(input("Введіть кількість стратегій: "))
    m = int(input("Введіть кількість станів природи: "))
  except ValueError:
    print("Помилка: введіть ціле число")
    return
  print("\nТип матриці:")
  print("1 - Прибуток (максимізація)")
  print("2 - Витрати (мінімізація)")
  matrix_type = input("Оберіть тип (1 або 2, за замовчуванням 2): ").strip()
  is_cost = matrix_type != "1"
  states = [f"S{j + 1}" for j in range(m)]
  strategies = []
  data = {s: [] for s in states}
  for i in range(n):
    name = input(f"\nНазва стратегії {i + 1}: ").strip()
    strategies.append(name)
    vals_str = input(
        f"Введіть {m} значень через пробіл для '{name}' ({' '.join(states)}): "
    )
    vals = list(map(float, vals_str.split()))
    while len(vals) != m:
      print(f"Помилка: потрібно ввести {m} чисел. Спробуйте ще раз:")
      vals = list(map(float, input().split()))
    for j, s in enumerate(states):
      data[s].append(vals[j])

  alpha = float(
      input("\nВведіть коефіцієнт оптимізму α (λ) (0-1, наприклад 0.6): ")
  )
  df = pd.DataFrame({"Стратегія": strategies, **data})

  if not is_cost:
    # Задача на доходи (максимізація)
    df["Лаплас"] = df[states].mean(axis=1)
    df["Вальд"] = df[states].min(axis=1)
    df["Maximax"] = df[states].max(axis=1)
    max_states = df[states].max()
    regret = max_states - df[states]
    df["Севідж (max жаль)"] = regret.max(axis=1)
    df["Гурвіц"] = (
        alpha * df[states].max(axis=1) + (1 - alpha) * df[states].min(axis=1)
    )
    criteria = ["Лаплас", "Вальд", "Maximax", "Севідж (max жаль)", "Гурвіц"]
    best = {}
    for c in criteria:
      if "Севідж" in c:
        best[c] = df.loc[df[c].idxmin(), "Стратегія"]
      else:
        best[c] = df.loc[df[c].idxmax(), "Стратегія"]
  else:
    # Задача на витрати (мінімізація) - задача 10
    df["Лаплас"] = df[states].mean(axis=1)
    df["Вальд (max витрат)"] = df[states].max(axis=1)
    df["Оптимізм (min витрат)"] = df[states].min(axis=1)
    min_states = df[states].min()
    regret = df[states] - min_states
    df["Севідж (max жаль)"] = regret.max(axis=1)

    # Критерій Гурвіца для витрат:
    # W_i = alpha * min + (1 - alpha) * max
    df["Гурвіц"] = (
        alpha * df[states].min(axis=1) + (1 - alpha) * df[states].max(axis=1)
    )
    criteria = [
        "Лаплас",
        "Вальд (max витрат)",
        "Оптимізм (min витрат)",
        "Севідж (max жаль)",
        "Гурвіц",
    ]
    best = {}
    for c in criteria:
      best[c] = df.loc[df[c].idxmin(), "Стратегія"]

  print("\n" + "=" * 75)
  print("Розрахункова таблиця:")
  print(df.round(2).to_string(index=False))
  print("=" * 75)

  print("\nОптимальні стратегії за критеріями:")
  for k, v in best.items():
    val = df.loc[df["Стратегія"] == v, k].values[0]
    print(f"{k}: {v} (значення = {round(val, 2)})")

if __name__ == "__main__":
  main()