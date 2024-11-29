import networkx as nx
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import Counter
from itertools import combinations, groupby, product


colors = list(mcolors.get_named_colors_mapping().keys())
def randgraph(n,G):
  edges = combinations(range(n), 2)
  p = random.random()
  G.add_nodes_from(range(n), color='')
  if(p <= 0):
    return G
  if(p >= 1):
    return nx.complete_graph(n,create_using=G)
  for _, edges2 in groupby(edges, key=lambda x: x[0]):
    edges2 = list(edges2)
    randEdge = random.choice(edges2)
    G.add_edge(*randEdge)
    for e in edges2:
      if random.random() < p:
        G.add_edge(*e)
  return G

def isDomaticPartition(G,colorMap): 
  colors = []
  for i in G.nodes:
    G.nodes[i]['color'] = colorMap[i]
  for x in G.nodes:
    if G.nodes[x]['color'] not in colors:
      colors.append(G.nodes[x]['color'])
  for i in G.nodes:
    colorChecker = colors.copy()
    colorChecker.remove(G.nodes[i]['color'])
    for j in G.adj[i]:
      if G.nodes[j]['color'] in colorChecker:
        colorChecker.remove(G.nodes[j]['color'])
    if len(colorChecker) != 0:
      return False
  return True

def randTreeGraph(vertices,minLeafs,maxRuns):
  isValidGraph = False
  breaker = 0
  global bestLeafCount
  while breaker < maxRuns:
    breaker += 1
    if isValidGraph == True:
      break
    Tree = nx.random_tree(vertices)
    for i in Tree.nodes:
      leafCount = maxLeafCount = 0
      for j in Tree.adj[i]:
        if len(Tree.adj[j]) == 1:
          leafCount += 1
      if leafCount > maxLeafCount:
        maxLeafCount = leafCount
      if maxLeafCount > bestLeafCount:
        bestLeafCount = maxLeafCount
        bestTree = Tree
    if maxLeafCount >= minLeafs:
      isValidGraph = True
  return bestTree

def findDomaticPartitions(graph,isEqualPartition):
  minDegree = len(graph.nodes)
  global dAllPart
  for i in graph.nodes:
    if minDegree > len(graph.adj[i]):
      minDegree = len(graph.adj[i])
  coloringProducts = product(range(1,minDegree+2),repeat=len(graph.nodes))
  totalColorings = list(coloringProducts)
  allColors = list(range(1,minDegree+2))
  dPart = {}
  dPartTemp = {}
  dPartEqual = {}
  for color in allColors:
    dPartTemp[color] = []
    dPart[color] = []
    dPartEqual[color] = []
  for possibleColoring in totalColorings:
    for color in allColors:
      if color not in possibleColoring:
        if max(possibleColoring) == color - 1:
          dPartTemp[color - 1].append(possibleColoring)
        break
      if color == minDegree + 1:
        dPartTemp[minDegree+1].append(possibleColoring)
  for domaticSet, domaticColorings in dPartTemp.items():
    for validColoring in domaticColorings:
      if isDomaticPartition(graph,validColoring):
        dPart[domaticSet].append(validColoring)
  dAllPart = dPart
  if isEqualPartition:
    for domaticSet, domaticColorings in dPart.items():
      for validColoring in domaticColorings:
        if isEquitable(validColoring):
          dPartEqual[domaticSet].append(validColoring)
    return dPartEqual
  else:
    return dPart
    
def isEquitable(coloring):
  count = list(Counter(coloring).values())
  max = count[0]
  min = count[-1]
  if abs(min - max) > 1:
    return False
  return True

def colorConvert(partition):
  colorMap = []
  for i in partition:
    colorMap.append(colors[i])
  return colorMap
  
def dicPrint(dictionary):
  print()
  for keys,values in dictionary.items():
    print(keys,":")
    print(values)
  print()
  
def Remove(tuples):
    tuples = [t for t in tuples if t]
    return tuples
    
def Main():
  i = 0
  runs = 100
  while i < runs:
    G = nx.Graph()
  
    vertices = 6
  
    randgraph(vertices,G)

    dPartEqual = findDomaticPartitions(G,True)
    dPartEqualasList = Remove(list(dPartEqual.values()))
  
    dPart = dAllPart
    dPartasList = Remove(list(dPart.values()))

    domaticNumber = max(dPartasList[-1][-1])
    equitableDomaticNumber = max(dPartEqualasList[-1][-1])
    color_map = colorConvert(dPartasList[-1][-1])
    print("---------------------------------------------")
    i += 1
    print(i)
    print("Partition shown in the image: ",dPartasList[-1][-1])
    print("domatic number: ",domaticNumber)
    print("equitable domatic number: ",equitableDomaticNumber)
    nx.draw(G, node_color=color_map ,with_labels=True)
    plt.savefig("Graph.png")
  
    if not domaticNumber == equitableDomaticNumber:
      DN = str(domaticNumber)
      EDN = str(equitableDomaticNumber)
      breaker = str(i)
      file_name = "{}--{}--DN-{}&EDN-{}-EquDomNum.png"
      plt.savefig(file_name.format(vertices,breaker,DN,EDN))
      plt.close()
      color_map = colorConvert(dPartasList[-1][-1])
      nx.draw(G, node_color=color_map ,with_labels=True)
      file_name = "{}--{}--DN-{}&EDN-{}-DomNum.png"
      plt.savefig(file_name.format(vertices,breaker,DN,EDN))
    plt.close()
    
def tester():
  G = nx.Graph()
  
  vertices = 6
  
  randgraph(vertices,G)

  dPartEqual = findDomaticPartitions(G,True)
  dPartEqualasList = Remove(list(dPartEqual.values()))

  dPart = dAllPart
  dPartasList = Remove(list(dPart.values()))

  domaticNumber = max(dPartasList[-1][-1])
  equitableDomaticNumber = max(dPartEqualasList[-1][-1])
  color_map = colorConvert(dPartEqualasList[-1][-1])
  print("---------------------------------------------")
  print("Partition shown in the image: ",dPartEqualasList[-1][-1])
  print("domatic number: ",domaticNumber)
  print("equitable domatic number: ",equitableDomaticNumber)
  nx.draw(G, node_color=color_map ,with_labels=True)
  plt.savefig("Graph.png")

bestLeafCount = 0
dAllPart = {}
Main()
