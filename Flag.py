# variables
T = 'tasmania'
V = 'victoria'
Q = 'queensland'
NSW = 'new south wales'
WA = 'western australia'
SA = 'southern australia'
NT = 'northwest territories'

# map
australia = {T: {V},
             V: {SA, NSW, T},
             Q: {NT, SA, NSW},
             NSW: {Q, SA, V},
             WA: {NT, SA},
             SA: {WA, NT, Q, NSW, V},
             NT: {WA, Q, SA}}
# values
colors = {'blue', 'red', 'yellow', 'green'}


def check_valid(map):
    for node, nexts in map.items():
        assert (node not in nexts)  # # no node linked to itself
        for next in nexts:
            assert (next in map and node in map[next])  # A linked to B implies B linked to A


def check_solution(map, solution):
    if solution is not None:
        for node, nexts in map.items():
            assert (node in solution)
            color = solution[node]
            for next in nexts:
                assert (next in solution and solution[next] != color)


def find_best_candidate(map, possible_candidate):
    if True:
        for value in map:
            if value not in possible_candidate:
                print("P1-> ", -len(
                    {possible_candidate[neighboors] for neighboors in map[value] if neighboors in possible_candidate}))
                print("P2-> ", -len({neighboors for neighboors in map[value] if neighboors not in possible_candidate}))
                print("P3-> ",
                      {possible_candidate[neighboors] for neighboors in map[value] if neighboors in possible_candidate})
                print("P4-> ", {neighboors for neighboors in map[value] if neighboors not in possible_candidate})
                print("N-> ", value)

        candidates_with_add_info = [
            (
                -len({possible_candidate[neighboors] for neighboors in map[value] if neighboors in possible_candidate}),
                -len({neighboors for neighboors in map[value] if neighboors not in possible_candidate}),
                value
            ) for value in map if value not in possible_candidate]
        print("candidates_with_add_info: ", candidates_with_add_info)
        candidates_with_add_info.sort()  # order
        candidates = [value for _, _, value in candidates_with_add_info]
    else:
        candidates = [n for n in map if n not in possible_candidate]
        candidates.sort()  # just to have some consistent performances
    if candidates:
        candidate = candidates[0]
        assert (candidate not in possible_candidate)
        print("Candidate: ", candidate)
        return candidate
    assert (set(map.keys()) == set(possible_candidate.keys()))
    return None


# possible_candidate - supostos candidatos(dicionario com nome da cidade e com a cor atribuida

def solve(map, colors, possible_candidate, depth):
    candidate = find_best_candidate(map, possible_candidate)
    if candidate is None:
        return possible_candidate  # Solution is found
    for cor in colors - {possible_candidate[neighboors] for neighboors in map[candidate] if
                         neighboors in possible_candidate}:
        assert (candidate not in possible_candidate)
        assert (all((neighboors not in possible_candidate or possible_candidate[neighboors] != cor) for neighboors in
                    map[candidate]))
        possible_candidate[candidate] = cor
        if solve(map, colors, possible_candidate, depth + 1):
            return possible_candidate
        else:
            del possible_candidate[candidate]
    return None


def solve_problem(map, colors):
    check_valid(map)  # validate nodes
    solution = solve(map, colors, dict(), 0)  # find solution
    print(solution)
    check_solution(map, solution)  # test solution


solve_problem(australia, colors)
# map = grafo
