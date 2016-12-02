import sys
import json
import numpy
from utilities import color

def alpha_to_id(alpha):
    return ord(alpha) - ord('a')
def spring_layout(width, height, vertices, edges):
    velocity = []
    delta = numpy.array([0, 0])
    rate = 0.9
    for id1 in range(len(vertices)):
        force = numpy.array([0, 0])
        for ed in edges:
            if id1 in ed:
                id2 = ed[(ed.index(id1) + 1) % 2]
                x1 = vertices[id1]["x"]
                y1 = vertices[id1]["y"]
                x2 = vertices[id2]["x"]
                y2 = vertices[id2]["y"]
                delta = numpy.array([x2 - x1, y2 - y1])
                force = force + 0.06 * delta
        velocity.append(numpy.array([force[0] * 0.85, force[1] * 0.85]))
    for index, vtx in enumerate(vertices):
        if not vtx["fix"]:
            delta = numpy.array([vtx["x"], vtx["y"]])
            delta = delta + velocity[index]
            delta[0] = min(width * rate, max(width * (1 - rate), delta[0]))
            delta[1] = min(height * rate, max(height * (1 - rate), delta[1]))
            vtx["x"] = delta[0]
            vtx["y"] = delta[1]

args = sys.argv
if len(args) < 3:
    print color.color.NG + "error" + color.color.END_CODE + ": too few arguments to run"
    exit(1)

read_filepath = args[1]
write_filepath = args[2]
read_file = open(read_filepath)
json_file = json.load(read_file)
read_file.close()
verticesJson = json_file["graphic"]["vertices"]
edgesJson = json_file["graphic"]["edges"]

vertices = []
for vtxJson in verticesJson:
    vertices.append({"x": vtxJson["coord"]["x"], "y": vtxJson["coord"]["y"], "fix": vtxJson["fix"]})

edges = []
for edJson in edgesJson:
    (id1, id2) = edJson.split(":")
    edges.append([alpha_to_id(id1), alpha_to_id(id2)])

for _ in range(50):
    spring_layout(1.0, 1.0, vertices, edges)

for index, vtxJson in enumerate(json_file["graphic"]["vertices"]):
    vtxJson["coord"]["x"] = vertices[index]["x"]
    vtxJson["coord"]["y"] = vertices[index]["y"]
write_file = open(write_filepath, 'w')
json.dump(json_file, write_file)
write_file.close()
