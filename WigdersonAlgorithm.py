def _get_color(neighbors, min_color):
    used = [False] * (len(neighbors) + 1)

    for c in neighbors:
        assert c - min_color >= 0
        if len(used) > c - min_color:
            used[c - min_color] = True

    for i in range(len(used)):
        if not used[i]:
            return i + min_color

    assert False


def _greed_dfs(v, graph, used, vertices, colors, min_color):
    used[v] = True

    neighbors = set()
    for u in graph[v]:
        if u in vertices and not used[u]:
            _greed_dfs(u, graph, used, vertices, colors, min_color)
        if u in vertices and colors[u]:
            neighbors.add(colors[u])

    colors[v] = _get_color(neighbors, min_color)


def _bin_dfs(v, graph, used, vertices, colors, min_color, last_color=0):
    used[v] = True
    bin_color = (last_color ^ 1)
    colors[v] = bin_color + min_color

    for u in graph[v]:
        if u in vertices and not used[u]:
            _bin_dfs(u, graph, used, vertices, colors, min_color, bin_color)


def _coloring(graph, vertices, colors, min_color, dfs_fun):
    used = [False] * len(graph)

    for v in vertices:
        if not used[v]:
            dfs_fun(v, graph, used, vertices, colors, min_color)


def _get_degree(v, graph, colors):
    d = 0
    for u in graph[v]:
        if colors[u] == 0:
            d += 1

    return d


def _get_maximal_degree(graph, colors):
    cur_v, cur_d = -1, -1

    for v in range(len(graph)):
        for u in graph[v]:
            cur_d, cur_v = max((cur_d, cur_v), (_get_degree(u, graph, colors), u))

    return cur_d, cur_v


def get_coloring(graph):
    k = max(int(len(graph) ** 0.5), 2)
    colors = [0] * len(graph)
    min_color = 1

    while True:
        max_d, v = _get_maximal_degree(graph, colors)
        if max_d < k:
            break

        vertices = set()
        colors[v] = min_color
        min_color += 1

        for u in graph[v]:
            if colors[u] == 0:
                vertices.add(u)

        _coloring(graph, vertices, colors, min_color, _bin_dfs)
        min_color = max(colors) + 1

    vertices = set()
    for v in range(len(graph)):
        if colors[v] == 0:
            vertices.add(v)

    _coloring(graph, vertices, colors, min_color, _greed_dfs)

    return colors
