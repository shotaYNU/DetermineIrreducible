import json
import copy
import Queue

class BreadthFirstSearch(object):
    def __init__(self, start_edge, clockwise, size):
        self.start_edge = start_edge
        self.clockwise = clockwise
        self.order = []
        visited = [False] * size
        waiting = Queue.Queue()
        waiting.put(start_edge)
        while not waiting.empty():
            now_edge = end_edge = waiting.get()
            visited[now_edge.start] = True
            while True:
                if not visited[now_edge.end]:
                    waiting.put(now_edge.inverse)
                    visited[now_edge.end] = True
                self.order.append(now_edge)
                now_edge = now_edge.next if clockwise else now_edge.prev
                if now_edge == end_edge:
                    break
        self.now_count = 0
    def has_next(self):
        return self.now_count != len(self.order)
    def next(self):
        count = self.now_count
        self.now_count += 1
        return self.order[count]

class Autohomeomorphism(object):
    @staticmethod
    def homeomorphic(aut1, aut2):
        return Representation.compare_representation(aut1.best_rep, aut2.best_rep) == Representation.Results.AUTOMORPHISM
    def __init__(self, graph):
        self.count = 0
        self.best_rep = Representation(graph.vertices[0].first_edge, True, graph.vertices_num)
        for vtx in graph.vertices:
            start_edge = now_edge = vtx.first_edge
            while True:
                for clockwise in [True, False]:
                    rep = Representation(now_edge, clockwise, graph.vertices_num)
                    compare_result = Representation.compare_representation(self.best_rep, rep)
                    if compare_result == Representation.Results.BETTER:
                       self.best_rep = rep
                       self.count = 1
                    elif compare_result == Representation.Results.AUTOMORPHISM:
                      self.count += 1
                now_edge = now_edge.next
                if now_edge == start_edge:
                    break

class Representation(object):
    class Results:
        (
            FAIL,
            AUTOMORPHISM,
            BETTER
        ) = range(0, 3)

    @staticmethod
    def compare_representation(rep1, rep2):
        if len(rep1.representation) != len(rep2.representation):
            return Representation.Results.FAIL
        for i, _ in enumerate(rep1.representation):
            if rep1.representation[i] < rep2.representation[i]:
                return Representation.Results.FAIL
            elif rep1.representation[i] > rep2.representation[i]:
                return Representation.Results.BETTER
        return Representation.Results.AUTOMORPHISM
    def __init__(self, ed, clockwise, size):
        bfs = BreadthFirstSearch(ed, clockwise, size)
        index_mapping = [-1] * size
        now_id = -1
        self.representation = []
        self.ed = ed
        id_count = 1
        while bfs.has_next():
            ed = bfs.next()
            if now_id != ed.start:
                now_id = ed.start
                self.representation.append(0)
                if index_mapping[now_id] == -1:
                    index_mapping[now_id] = id_count
                    id_count += 1
            if index_mapping[ed.end] == -1:
                index_mapping[ed.end] = id_count
                id_count += 1
            self.representation.append(index_mapping[ed.end])
        self.representation.append(0)
    def to_string(self):
        string = ""
        for num in self.representation:
            string += (str(num) + ":")
        return string

class Edge(object):
    @staticmethod
    def make_edges(id1, id2, dist_id, flip):
        ed1 = Edge(); ed2 = Edge()
        ed1_op = Edge(); ed2_op = Edge()

        ed1.opposite = ed1_op; ed2.opposite = ed2_op
        ed1_op.opposite = ed1; ed2_op.opposite = ed2

        ed1.start = id1; ed1.end = id2; ed1.dist = dist_id
        ed2.start = id2; ed2.end = id1; ed2.dist = dist_id

        ed1.inverse = (ed2, flip); ed2.inverse = (ed1, flip)

        return ed1
    @staticmethod
    def equal(ed1, ed2):
        if ed1.start == ed2.start and ed1.end == ed2.end and ed1.dist == ed2.dist:
            return True
        else:
            return False
    def __init__(self):
        self._start = -1
        self._end = -1
        self._dist = -1
        self._real_start = -1
        self._real_end = -1
    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, start):
        self._start = start
        self.opposite._start = start
    @property
    def end(self):
        return self._end
    @end.setter
    def end(self, end):
        self._end = end
        self.opposite._end = end
    @property
    def dist(self):
        return self._dist
    @dist.setter
    def dist(self, dist):
        self._dist = dist
        self.opposite._dist = dist
    @property
    def inverse(self):
        return self._inverse
    @inverse.setter
    def inverse(self, inverse):
        (ed, flip) = inverse
        self._inverse = ed if not flip else ed.opposite
        self.opposite._inverse = ed.opposite if not flip else ed
    @property
    def next(self):
        return self._next
    @next.setter
    def next(self, next):
        self._next = next
        self.opposite._prev = next.opposite
    @property
    def prev(self):
        return self._prev
    @prev.setter
    def prev(self, prev):
        self._prev = prev
        self.opposite._next = prev.opposite
    @property
    def real_start(self):
        return self._real_start
    @real_start.setter
    def real_start(self, real_start):
        self._real_start = real_start
        self.opposite._real_start = real_start
    @property
    def real_end(self):
        return self._real_end
    @real_end.setter
    def real_end(self, real_end):
        self._real_end = real_end
        self.opposite._real_end = real_end
    def print_edge(self):
        print str(self.start) + "-" + str(self.end) + "(" + str(self.dist) + ")"

class Vertex(object):
    @staticmethod
    def alpha_to_id(alpha):
        if alpha.isdigit():
            return (int(alpha) * -1, False)
        flip = not ('a' <= alpha and alpha <= 'z')
        first_alpha = 'a' if not flip else 'A'
        id = ord(alpha) - ord(first_alpha)
        return (id, flip)
    @staticmethod
    def id_to_alpha(id, flip):
        first_alpha = 'a' if not flip else 'A'
        alpha = chr(ord(first_alpha) + id)
        return alpha
    def __init__(self):
        self.id = -1
        self.adjacency = []

class Graph:
    def view_adjacency_matrix(self):
        print_str = "   | " + " ".join(["{0:^2}".format(str(s.id)) for s in self.vertices]) + "\n"
        print_str += "------" + "---" * self.vertices_num + "\n"
        for vtx in self.vertices:
            print_str += "{0:^2}".format(str(vtx.id)) + " | "
            print_str += " ".join(["{0:^2}".format(str(e)) for e in vtx.adjacency]) + " |" + "\n"
        print print_str
    def view_rotation_clockwise(self):
        print_str = ""
        for vtx in self.vertices:
            start_edge = vtx.first_edge
            print_str += "{0:^2}".format(str(start_edge.start)) + ". " + "{0:^2}".format(str(start_edge.end)) + "(" + str(start_edge.dist) + ") "
            now_edge = start_edge.next
            while now_edge != start_edge:
                print_str += " " + "{0:^2}".format(str(now_edge.end)) + "(" + str(now_edge.dist) + ") "
                now_edge = now_edge.next
            print_str += "\n"
        print print_str
    def view_rotation_unticlockwise(self):
        print_str = ""
        for vtx in self.vertices:
            start_edge = vtx.first_edge
            print_str += "{0:^2}".format(str(start_edge.start)) + ". " + "{0:^2}".format(str(start_edge.end)) + "(" + str(start_edge.dist) + ") "
            now_edge = start_edge.prev
            while now_edge != start_edge:
                print_str += " " + "{0:^2}".format(str(now_edge.end)) + "(" + str(now_edge.dist) + ") "
                now_edge = now_edge.prev
            print_str += "\n"
        print print_str
    def __init__(self):
        self.vertices = []
        self.bounds = []
    def edges(self):
        edges = []
        for vtx in self.vertices:
            start_edge = now_edge = vtx.first_edge
            while True:
                edges.append(now_edge)
                now_edge = now_edge.next
                if now_edge == start_edge:
                    break
        return edges
    def insert_edge(self, to_ed, insert_ed):
        insert_ed.start = to_ed.start
        insert_ed.inverse.end = to_ed.inverse.end
        insert_ed.next = to_ed.next
        insert_ed.prev = to_ed
        to_ed.next.prev = insert_ed
        to_ed.next = insert_ed
    def add_subgraph(self, bounds_index, to_ed2, graph):
        to_ed1 = self.bounds[bounds_index]["edges"][0]["edge"]
        clockwise = self.bounds[bounds_index]["clockwise"]

        # relabeling
        for ed in graph.edges():
            if ed.end >= 0:
                ed.end = ed.end + self.vertices_num
                ed.inverse.start = ed.inverse.start + self.vertices_num
            ed.dist = -1
            ed.inverse.dist = -1

        # add vertex
        prev_real_num = len(self.json["graphic"]["vertices"])
        new_id_reals = {}
        for vtx in graph.vertices:
            if vtx.id < 0:
                continue
            new_vertex = Vertex()
            new_vertex.id = vtx.id + self.vertices_num
            new_vertex.first_edge = vtx.first_edge
            self.vertices.append(new_vertex)
            self.json["graphic"]["vertices"].append({ "id": Vertex.id_to_alpha(new_vertex.id, False), "coord": {"x": 0.0, "y": 0.0}, "real_id": prev_real_num + vtx.id, "fix": False })
            new_id_reals[str(new_vertex.id)] = prev_real_num + vtx.id
        self.vertices_num = len(self.vertices)
        for vtx in self.vertices:
            for i in range(self.vertices_num - len(vtx.adjacency)):
                vtx.adjacency.append(0)

        # add edge
        start_edge = now_edge = to_ed2
        to_edge = to_ed1
        count = 0
        while True:
            end_edge = now_edge.prev
            now_edge = now_edge.next
            insert_to_edge = to_edge
            while now_edge != end_edge:
                next_edge = now_edge.next
                self.insert_edge(insert_to_edge, now_edge)
                now_edge.real_start = self.bounds[bounds_index]["edges"][count]["real_start"]
                now_edge.inverse.real_end = self.bounds[bounds_index]["edges"][count]["real_start"]
                insert_to_edge = now_edge
                now_edge = next_edge
            now_edge = now_edge.next.inverse.next
            to_edge = to_edge.inverse.prev if clockwise else to_edge.inverse.next
            count += 1
            if now_edge == start_edge:
                break

        # add real edge
        for ed in self.edges():
            if ed.dist == -1:
                if ed.real_start < 0:
                    ed.real_start = new_id_reals[str(ed.start)]
                    ed.inverse.real_end = new_id_reals[str(ed.inverse.end)]
                if ed.real_end < 0:
                    ed.real_end = new_id_reals[str(ed.end)]
                    ed.inverse.real_start = new_id_reals[str(ed.inverse.start)]
                self.json["graphic"]["edges"].append(Vertex.id_to_alpha(ed.real_start, False) + ":" + Vertex.id_to_alpha(ed.real_end, False))

        # set adjacency
        for ed in self.edges():
            if ed.dist == -1:
                self.vertices[ed.start].adjacency[ed.end] += 1
                self.vertices[ed.end].adjacency[ed.start] += 1
                ed.dist = self.vertices[ed.start].adjacency[ed.end]
                ed.inverse.dist = self.vertices[ed.start].adjacency[ed.end]
    def reverse_orientation(self):
        for ed in self.edges():
            next = ed.next
            prev = ed.prev
            ed.next = prev
            ed.prev = next
    def open_graph(self, filepath):
        if type(filepath) is str:
            file = open(filepath)
            json_file = json.load(file)
            file.close()
        elif type(filepath) is dict:
            json_file = filepath
        self._open_graph_with_json(json_file)
    def _open_graph_with_json(self, graph_json):
        self.json = copy.deepcopy(graph_json)
        rotations = graph_json["base"]["rotations"]
        edges = {}
        adjacents = rotations.split(',')
        self.vertices_num = len(adjacents)
        ids = graph_json["base"]["ids"].split(',') if graph_json["base"].has_key("ids") else range(self.vertices_num)
        for id in ids:
            new_vertex = Vertex()
            new_vertex.id = int(id)
            self.vertices.append(new_vertex)
        for index1, adj in enumerate(adjacents):
            adjacency = [0 for i in range(self.vertices_num)]
            id1 = self.vertices[index1].id
            for ids in adj.split(":"):
                id2_ch = ids[0]
                dist_id = int(ids[1]) if len(ids) > 1 else 1
                (id2, flip) = Vertex.alpha_to_id(id2_ch)
                ad_index = [g.id for g in self.vertices].index(id2)
                adjacency[ad_index] += 1
                if (str(id1) + ':' + str(id2) + "_" + str(dist_id)) in edges:
                    new_ed = edges[str(id1) + ':' + str(id2) + "_" + str(dist_id)]
                else:
                    new_ed = Edge.make_edges(id1, id2, dist_id, flip)
                    edges[str(id1) + ':' + str(id2) + "_" + str(dist_id)] = new_ed
                    edges[str(id2) + ':' + str(id1) + "_" + str(dist_id)] = new_ed.inverse if not flip else new_ed.opposite.inverse
                if not hasattr(self.vertices[index1], "first_edge"):
                    self.vertices[index1].first_edge = new_ed
                    first_edge = new_ed
                else:
                    prev_edge.next = new_ed
                    new_ed.prev = prev_edge
                prev_edge = new_ed
            prev_edge.next = first_edge
            first_edge.prev = prev_edge
            self.vertices[index1].adjacency = adjacency

        if graph_json["base"].has_key("bounds"):
            bounds_str = graph_json["base"]["bounds"]
            real_bounds_str = graph_json["graphic"]["real_bounds"] if graph_json.has_key("graphic") else " ".join(["00" for i in range(len(bounds_str.split(' ')))])
            bounds_edges = []
            bounds = bounds_str.split(',')
            real_bounds = real_bounds_str.split(',')
            for b_index, b in enumerate(bounds):
                one_bound = []
                for i, edge in enumerate(b.split(' ')):
                    id1, _ = Vertex.alpha_to_id(edge[0])
                    real_id1, _ = Vertex.alpha_to_id(real_bounds[b_index].split(' ')[i][0])
                    id2, _ = Vertex.alpha_to_id(edge[1])
                    real_id2, _ = Vertex.alpha_to_id(real_bounds[b_index].split(' ')[i][1])
                    dist_id = int(edge[2]) if len(edge) > 2 else 1
                    add_edge = edges[str(id1) + ':' + str(id2) + "_" + str(dist_id)]
                    add_edge.real_start = real_id1
                    add_edge.real_end = real_id2
                    one_bound.append({ "real_start": real_id1, "real_end": real_id2, "edge": add_edge })
                if Edge.equal(one_bound[0]["edge"].inverse.prev, one_bound[1]["edge"]):
                    clockwise = True
                elif Edge.equal(one_bound[0]["edge"].inverse.next, one_bound[1]["edge"]):
                    clockwise = False
                else:
                    print "error"
                    exit(1)
                self.bounds.append({ "edges": one_bound, "clockwise": clockwise })
    def save_graph(self, save_path):
        rotations = ""
        for ed in self.edges():
            ed.mark = True
            ed.opposite.mark = False
        for vtx in self.vertices:
            start_edge = now_edge = vtx.first_edge
            while True:
                flip = (now_edge.mark != now_edge.inverse.mark)
                alpha = Vertex.id_to_alpha(now_edge.end, flip)
                dist_id = now_edge.dist
                rotations += (alpha + str(dist_id) + ":")
                now_edge = now_edge.next
                if now_edge == start_edge:
                    break
            rotations = rotations[0:-1]
            rotations += ","
        rotations = rotations[0:-1]
        self.json["base"]["rotations"] = rotations
        write_file = open(save_path, 'w')
        json.dump(self.json, write_file)
        write_file.close()
    def has_loop(self):
        for i, vtx in enumerate(self.vertices):
            if vtx.adjacency[i] > 0:
                return True
        return False
    def is_even(self):
        for vtx in self.vertices:
            if sum(vtx.adjacency) % 2 != 0:
                return False
        return True
    def is_irreducible(self):
        for vtx in self.vertices:
            if sum(vtx.adjacency) != 4:
                continue
            for first_edge in [vtx.first_edge, vtx.first_edge.next]:
                id1 = first_edge.end
                id2 = first_edge.next.next.end
                if id1 != id2 and self.vertices[id1].adjacency[id2] == 0:
                    return False
        return True
