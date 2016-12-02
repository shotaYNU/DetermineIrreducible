import sys
import json
import pyx
from utilities import color

def alpha_to_id(alpha):
    return ord(alpha) - ord('a')

LENGTH = 10
RADIUS = 0.45

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
    vertices.append({"x": vtxJson["coord"]["x"] * LENGTH, "y": (1.0 - vtxJson["coord"]["y"]) * LENGTH})

edges = []
for edJson in edgesJson:
    (id1, id2) = edJson.split(":")
    edges.append([alpha_to_id(id1), alpha_to_id(id2)])

canvas = pyx.canvas.canvas()
for vtx in vertices:
    canvas.fill(pyx.path.circle(vtx["x"], vtx["y"], RADIUS))

for ed in edges:
    canvas.stroke(pyx.path.line(vertices[ed[0]]["x"], vertices[ed[0]]["y"], vertices[ed[1]]["x"], vertices[ed[1]]["y"]), [pyx.style.linewidth(0.12)])

canvas.writeEPSfile(write_filepath)
