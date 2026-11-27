import heapq


# 1. Поиск цикла в графе (неориентированный, список смежности)
def has_cycle(graph):
    # DFS с запоминанием "откуда пришли" (parent).
    # Повторное посещение обнаруживается так: если сосед u уже посещен
    # и u - не родитель текущей вершины v, значит мы пришли в u другим
    # путем, то есть между v и u есть второе ребро-путь -> цикл.
    # Родителя исключаем, потому что ребро "назад к отцу" есть всегда
    # и циклом не является.
    # Перебираем все компоненты связности: цикл может быть в любой.
    visited = set()

    def dfs(v, parent):
        visited.add(v)
        for u in graph.get(v, []):
            if u not in visited:
                if dfs(u, v):
                    return True
            elif u != parent:
                return True          # visited + не родитель => цикл
        return False

    for v in graph:
        if v not in visited:
            if dfs(v, None):
                return True
    return False


# 2. Является ли граф деревом
def is_tree(graph):
    # Дерево = связный граф без циклов. Проверяем два условия:
    #   1) связность - обходом из одной вершины посещаем все V вершин;
    #   2) E = V - 1, где E - число ребер (для неориентированного графа
    #      сумма степеней делится на 2).
    #
    # Почему условий достаточно: в связном графе всегда есть остовное
    # дерево на V - 1 ребрах, значит E >= V - 1. Равенство E = V - 1
    # означает, что лишних ребер (замыкающих цикл) нет. Обратно: дерево
    # по определению связно и имеет ровно V - 1 ребро. То есть
    # "связность + E = V - 1" равносильно "связность + ацикличность".
    V = len(graph)
    if V == 0:
        return True

    start = next(iter(graph))
    seen = set([start])
    stack = [start]
    while stack:
        v = stack.pop()
        for u in graph.get(v, []):
            if u not in seen:
                seen.add(u)
                stack.append(u)

    edges = sum(len(adj) for adj in graph.values()) // 2
    return len(seen) == V and edges == V - 1


# 3. Алгоритм Дейкстры
def dijkstra(graph, start):
    # Приоритетная очередь (min-heap) всегда отдает вершину с наименьшим
    # текущим расстоянием, поэтому вершины "закрываются" в правильном
    # порядке: когда вершину извлекли, найденное расстояние до нее уже
    # минимально (все пути через еще не обработанные вершины длиннее,
    # так как веса неотрицательны).
    #
    # Сложность O((V + E) log V): каждое ребро может вызвать одну
    # операцию push в кучу (O(log V)), плюс до V извлечений минимума
    # (O(log V)) -> (V + E) log V.
    #
    # graph: {вершина: [(сосед, вес), ...]}
    dist = {v: float('inf') for v in graph}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]:
            continue                 # устаревшая запись в куче
        for u, w in graph.get(v, []):
            nd = d + w
            if nd < dist[u]:
                dist[u] = nd
                heapq.heappush(pq, (nd, u))
    return dist


# 4. Проверка на двудольность
def is_bipartite(graph):
    # Красим вершины в два цвета: стартовой даем 0, всем ее соседям - 1,
    # их соседям - снова 0 и т.д. Если встретили соседа того же цвета,
    # что и текущая вершина, - раскраска невозможна, значит есть цикл
    # нечетной длины, и граф не двудольный.
    #
    # Корректность: цвет каждой вершины однозначно определяется цветом
    # стартовой (расстояние по четности), поэтому "выбора" у алгоритма
    # нет - если конфликт не найден, полученная раскраска и есть
    # разбиение на две доли. Обходим все компоненты, т.к. граф может
    # быть несвязным.
    # Время O(V + E).
    color = {}

    for start in graph:
        if start in color:
            continue
        color[start] = 0
        stack = [start]
        while stack:
            v = stack.pop()
            for u in graph.get(v, []):
                if u not in color:
                    color[u] = 1 - color[v]
                    stack.append(u)
                elif color[u] == color[v]:
                    return False
    return True
