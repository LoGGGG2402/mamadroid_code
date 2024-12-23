#!/usr/bin/python
# The purpose of this script is to turn a MAMADROID model into a cool visual figure
import matplotlib

matplotlib.use("Agg")
import networkx as nx
import ast
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

# Begin the magic
G = nx.Graph()
# Change the filepath to whatever you want
filepath = "graphs/ReturnParameterTest.txt"
with open(filepath, "r") as f:
    x = f.readlines()
# Now let's do some stuff with x
graph = {}
for line in x:
    (fr, to) = line.split(" ==> ")
    to = ast.literal_eval(to[:-1])
    to = [b[:-1] for b in to]
    if fr in graph:
        for d in to:
            graph[fr].append(d)
    else:
        graph[fr] = to
# Now turn the graph into a network
# Thanks to this homie: https://stackoverflow.com/a/44540691/1586231
G.add_nodes_from(graph.keys())
for fr, to in graph.items():
    G.add_edges_from(([(fr, d) for d in to]))
# Draw
plt.figure(figsize=(40, 40))
nx.draw(
    G,
    pos=graphviz_layout(G),
    node_size=1200,
    node_color="lightblue",
    linewidths=0.25,
    font_size=10,
    font_weight="bold",
    with_labels=True,
    dpi=1000,
)
plt.savefig("Graph.png", format="PNG")
