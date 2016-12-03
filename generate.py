import os
import glob
import json
import graphs
from utilities import progress

components_file_b4 = open("./components/components_b4.json")
components_b4 = json.load(components_file_b4)["components"]
components_file_b4.close()

components_file_b5 = open("./components/components_b5.json")
components_b5 = json.load(components_file_b5)["components"]
components_file_b5.close()

components_file_b6 = open("./components/components_b6.json")
components_b6 = json.load(components_file_b6)["components"]
components_file_b6.close()

def next_indexies(indexies, indexies_max):
    current_index = len(indexies) - 1
    while current_index >= 0:
        indexies[current_index] += 1
        if indexies[current_index] == indexies_max[current_index]:
            indexies[current_index] = 0
            current_index -= 1
        else:
            break
    return indexies
def get_components(deg, components_index, bounds_index):
    if deg == 4:
        components = components_b4
    elif deg == 5:
        components = components_b5
    elif deg == 6:
        components = components_b6
    else:
        print "error"
        exit(1)
    components_garph = graphs.Graph()
    components_garph.open_graph(components[components_index])
    bounds = []
    for ed in components_garph.bounds[0]["edges"]:
        bounds.append(ed["edge"])
        bounds.append(ed["edge"].inverse)
    if bounds_index % 2 != 0:
        components_garph.reverse_orientation()
    return (components_garph, bounds[bounds_index])
def components_max(deg):
    if deg == 4:
        return len(components_b4)
    elif deg == 5:
        return len(components_b5)
    elif deg == 6:
        return len(components_b6)
    else:
        print "error"
        exit(1)

graph_datas = []
graph_files = glob.glob("./frames/datas/frame*.json")
for file in graph_files:
    graph = open(file)
    graph_json = json.load(graph)
    graph.close()
    graph_datas.append(graph_json)

result_list_num = {}
result_list_index = {}
result_list = []
for index, graph in enumerate(graph_datas):
    if graph["base"]["bounds"] == "":
        continue
    print graph_files[index]
    bounds = graph["base"]["bounds"]
    bounds_sizes = [len(x.split(' ')) for x in bounds.split(',')]
    indexies = [0] * len(bounds_sizes) * 2
    indexies_max = []
    max_num = 1.0
    for size in bounds_sizes:
        indexies_max.append(components_max(size))
        max_num *= components_max(size)
        indexies_max.append(size * 2)
        max_num *= size * 2
    count = 0.0
    prog = progress.progress()
    while True:
        g = graphs.Graph()
        g.open_graph(graph)
        for i in range(len(indexies) / 2):
            (components_graph, ed) = get_components(bounds_sizes[i], indexies[2 * i], indexies[2 * i + 1])
            g.add_subgraph(i, ed, components_graph)
        if not g.has_loop() and g.is_even() and g.is_irreducible():
            aut = graphs.Autohomeomorphism(g)
            if not result_list_num.has_key(aut.best_rep.to_string()):
                result_list_num[aut.best_rep.to_string()] = 0
                result_list_index[aut.best_rep.to_string()] = len(result_list_num) - 1
            result_list_num[aut.best_rep.to_string()] += 1
            result_list.append({ "index": result_list_index[aut.best_rep.to_string()], "num": result_list_num[aut.best_rep.to_string()] , "graph": g })
        indexies = next_indexies(indexies, indexies_max)
        count += 1.0
        prog.flush_progress(count / max_num)
        if indexies == [0] * len(bounds_sizes) * 2:
            break
    prog.end_flush()

only_one_save = True
if not os.path.isdir("./results/datas"):
    os.makedirs("./results/datas")
for g in result_list:
    if (only_one_save and g["num"] == 1) or not only_one_save:
        g["graph"].save_graph("./results/datas/graph" + str(g["index"]) + "_" + str(g["num"]) + ".json")

print "\nresults num:", len(result_list_num)
