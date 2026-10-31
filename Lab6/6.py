import numpy as np
def plurality(voters, preferences, candidates):
    first_votes = {c: 0 for c in candidates}
    for count, pref in zip(voters, preferences):
        first_votes[pref[0]] += count
    sorted_cand = sorted(
        candidates, key=lambda c: first_votes[c], reverse=True
    )
    return sorted_cand, first_votes

def absolute_majority(voters, preferences, candidates):
    total_voters = sum(voters)
    sorted_cand, first_votes = plurality(voters, preferences, candidates)

    # Якщо хтось набрав понад 50% у 1-му турі
    if first_votes[sorted_cand[0]] > total_voters / 2:
        return sorted_cand, first_votes
    # 2й тур між двома лідерами 1го туру
    top1, top2 = sorted_cand[0], sorted_cand[1]
    round2_votes = {top1: 0, top2: 0}
    for count, pref in zip(voters, preferences):
        if pref.index(top1) < pref.index(top2):
            round2_votes[top1] += count
        else:
            round2_votes[top2] += count
    winner = top1 if round2_votes[top1] >= round2_votes[top2] else top2
    loser = top2 if winner == top1 else top1
    full_order = [winner, loser] + [
        c for c in sorted_cand if c not in [winner, loser]
    ]
    return full_order, round2_votes

def borda(voters, preferences, candidates):
    m = len(candidates)
    scores = {c: 0 for c in candidates}
    for count, pref in zip(voters, preferences):
        for rank, c in enumerate(pref):
            scores[c] += count * (m - 1 - rank)
    sorted_cand = sorted(candidates, key=lambda c: scores[c], reverse=True)
    return sorted_cand, scores

def pairwise(voters, preferences, candidates):
    n = len(candidates)
    matrix = {c1: {c2: 0 for c2 in candidates} for c1 in candidates}
    for count, pref in zip(voters, preferences):
        for i in range(len(pref)):
            for j in range(i + 1, len(pref)):
                c1, c2 = pref[i], pref[j]
                matrix[c1][c2] += count
    return matrix

def condorcet(voters, preferences, candidates):
    matrix = pairwise(voters, preferences, candidates)
    pairwise_wins = {
        c1: sum(
            1
            for c2 in candidates
            if c1 != c2 and matrix[c1][c2] > matrix[c2][c1]
        )
        for c1 in candidates
    }
    sorted_cand = sorted(
        candidates, key=lambda c: pairwise_wins[c], reverse=True
    )
    return sorted_cand, matrix

def copeland(voters, preferences, candidates):
    matrix = pairwise(voters, preferences, candidates)
    copeland_scores = {c: 0 for c in candidates}
    for c1 in candidates:
        for c2 in candidates:
            if c1 != c2:
                if matrix[c1][c2] > matrix[c2][c1]:
                    copeland_scores[c1] += 1
                elif matrix[c1][c2] < matrix[c2][c1]:
                    copeland_scores[c1] -= 1
    sorted_cand = sorted(
        candidates, key=lambda c: copeland_scores[c], reverse=True
    )
    return sorted_cand, copeland_scores

def simpson(voters, preferences, candidates):
    matrix = pairwise(voters, preferences, candidates)
    simpson_scores = {}
    for c1 in candidates:
        min_support = min(matrix[c1][c2] for c2 in candidates if c1 != c2)
        simpson_scores[c1] = min_support
    sorted_cand = sorted(
        candidates, key=lambda c: simpson_scores[c], reverse=True
    )
    return sorted_cand, simpson_scores

def main():
    print('Лабораторна робота №6. Методи голосування \n')
    try:
        raw_voters = input(
            'Введіть кількість голосів для кожної групи (через пробіл): '
        )
        voters = list(map(int, raw_voters.strip().split()))
    except ValueError:
        print('Помилка - введіть цілі числа')
        return
    num_groups = len(voters)
    print(
        '\nВведіть уподобання для кожної групи виборців (кандидати через пробіл):'
    )
    preferences = []
    candidates = set()
    for i in range(num_groups):
        pref_str = input(f'Група {i + 1}: ').strip().split()
        preferences.append(pref_str)
        for c in pref_str:
            candidates.add(c)

    candidates = sorted(list(candidates))
    # Обчислення
    plurality_order, _ = plurality(voters, preferences, candidates)
    abs_order, _ = absolute_majority(voters, preferences, candidates)
    borda_order, _ = borda(voters, preferences, candidates)
    condorcet_order, _ = condorcet(voters, preferences, candidates)
    copeland_order, _ = copeland(voters, preferences, candidates)
    simpson_order, _ = simpson(voters, preferences, candidates)
    print('\nРезультати голосування:')
    print('+' + '-' * 26 + '+' + '-' * 31 + '+')
    print(
        f'| {"Правило голосування":<24} | {"Кандидат переможець / Ранг":<29} |'
    )
    print('=' * 60)
    print(
        f'| {"Відносної більшості":<24} | {" = ".join(plurality_order[0:1]) + " > " + " > ".join(plurality_order[1:]):<29} |'
    )
    print('+' + '-' * 26 + '+' + '-' * 31 + '+')
    print(
        f'| {"Абсолютної більшості":<24} | {" > ".join(abs_order):<29} |'
    )
    print('+' + '-' * 26 + '+' + '-' * 31 + '+')
    print(f'| {"Правило Борда":<24} | {" > ".join(borda_order):<29} |')
    print('+' + '-' * 26 + '+' + '-' * 31 + '+')
    print(f'| {"Правило Кондорсе":<24} | {" > ".join(condorcet_order):<29} |')
    print('+' + '-' * 26 + '+' + '-' * 31 + '+')
    print(f'| {"Правило Копленда":<24} | {" > ".join(copeland_order):<29} |')
    print('+' + '-' * 26 + '+' + '-' * 31 + '+')
    print(f'| {"Правило Сімпсона":<24} | {" > ".join(simpson_order):<29} |')
    print('+' + '-' * 26 + '+' + '-' * 31 + '+')
if __name__ == '__main__':
    main()