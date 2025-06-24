# Comparação de algoritmos para resolução do cubo de Rubik

O objetivo desse projeto é realizar uma análise comparativa de algoritmos de resolução do Cubo de Rubik, serão analisados os algortimos de busca em largura(BFS), Busca em profundidade(IDS) e Busca A* com heurística.

## Instalando as dependências

Garanta ter o poetry instalado:

````bash
    pip install poetry
````

Instale as dependências do projeto

````bash
    poetry install --no-root
````

## Executando

Com o objetivo de estudar as particularidades do desafio de resolver o Cubo de Rubik, temos alguns arquivos que servem como ponto de entrada para diferentes perspectivas.

</br>Execute essa linha de comando para obter um cubo se resolvendo de forma visual e com possibilidade de interação.
````bash
    poetry run python run_solver_interface.py
````

</br>Execute essa linha de comando para executar um script que roda um teste variando de 0 a N o número de embaralhamento e retornando métricas para os 3 algoritmos utilizados.
````bash
    poetry run python rubik_v3_otimizado.py
````

</br>Execute `plot.ipynb` para obter gráficos de tempo, memória... para a N execuções de cada algoritmo comparadas.