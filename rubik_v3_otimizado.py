import csv

from src.solvers import a_star_solver, bfs_solver, generate_scrambled_cube, ids_solver

MAX_MOVES = 5
resultados = []

for n in range(1, MAX_MOVES + 1):
    print(f'\n=== Embaralhamento com {n} movimentos ===')
    scrambled_cube, scramble_seq = generate_scrambled_cube(n)
    print(f'Movimentos de embaralhamento: {scramble_seq}')

    for nome_alg, func in [('BFS', bfs_solver), ('IDS', ids_solver), ('A*', a_star_solver)]:
        print(f'\n[{nome_alg}]')

        result, tempo = func(scrambled_cube)

        if result.solution:
            print(f'Solução ({len(result.solution)} passos): {result.solution}')
            print(f'Tempo: {tempo:.4f}s | Memória (estrutura): {result.memoria} | Nós: {result.nos} | Ramificação média: {result.avg_branching:.2f}')
        else:
            print('Solução não encontrada.')

        resultados.append({
            'Movimentos Embaralhados': n,
            'Algoritmo': nome_alg,
            'Passos Solução': len(result.solution) if result.solution else 'N/A',
            'Tempo (s)': f'{tempo:.4f}' if tempo else 'N/A',
            'Memória Máx. (Fila/Pilha/Heap)': result.memoria,
            'Nós Expandidos': result.nos,
            'Fator Ramificação Média': f'{result.avg_branching:.2f}' if result.avg_branching else 'N/A'
        })

with open('relatorio_resultados.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=resultados[0].keys())
    writer.writeheader()
    writer.writerows(resultados)

print("\nRelatório salvo em 'relatorio_resultados.csv'")
