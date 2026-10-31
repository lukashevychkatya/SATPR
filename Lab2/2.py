# Лабораторна робота №2
# Прийняття рішення в умовах ризиків (дерево прийняття рішень)
# Виконала студентка групи ПП-31/1 Лукашевич К.І.

def main():
    num_alternatives = int(input("Введіть кількість альтернатив: "))
    num_scenarios = int(input("Введіть кількість сценаріїв: "))
    probabilities = list(map(float, input(f"Введіть {num_scenarios} ймовірностей через пробіл: ").split()))

    alternatives = {}
    for i in range(num_alternatives):
        profits = list(map(float, input(f"Введіть прибутки альтернативи {i+1} через пробіл: ").split()))
        alternatives[f"Альтернатива {i+1}"] = profits

    expected_profits = {}
    for alt, profits in alternatives.items():
        expected_profit = sum(p * prob for p, prob in zip(profits, probabilities))
        expected_profits[alt] = expected_profit
        print(f"{alt}: очікуваний прибуток = {round(expected_profit, 2)}")

    best_alt = max(expected_profits, key=expected_profits.get)
    print(f"\nНайкраща альтернатива: {best_alt} з очікуваним прибутком {round(expected_profits[best_alt], 2)}")

if __name__ == "__main__":
    main()

