#makes a graph of interconnected tuples in a grid of rows and cols
def makeGraph(rows, cols):
    result = dict()
    for row in range(rows):
        for col in range(cols):
            coords = (row, col)
            result[coords] = []
            for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                tempRow = row + dy
                tempCol = col + dx
                if 0<=tempRow<rows and 0<=tempCol<cols:
                    result[coords].append((tempRow, tempCol))
    return result

#from pseudocode in TA pathfinding guide
#returns list of nodes to visit from start to end
def BFS(start, end, graph):
    queue = [start]
    visited = [start]
    mapping = {start:[]} #(currentNode, prevNode)
    while queue != []:
        node = queue.pop(0)
        if node not in mapping:
            mapping[node] = []
        if node == end:
            map = extractMap(start, end, graph, mapping, resultMap = [end])
            return map
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                mapping[node].append(neighbor)
    return None

#helper function, extracts simple map from complicated mapping
def extractMap(start, end, graph, mapping, resultMap):
    if start in resultMap and end in resultMap:
        return resultMap
    else:
        currNode = resultMap[0]
        for key in mapping:
            if currNode in mapping[key]:
                resultMap.insert(0, key)
                solution = extractMap(start, end, graph, mapping, resultMap)
                if solution != None:
                    return solution
    return None

#removes node and any connection from a graph
def createHole(graph, holeNode):
    resultGraph = graph
    del resultGraph[holeNode]
    for key in resultGraph:
        if holeNode in resultGraph[key]:
            resultGraph[key].remove(holeNode)
    return resultGraph

#breaks connection between 2 nodes
def createWall(graph, node1, node2):
    resultGraph = graph
    resultGraph[node1].remove(node2)
    resultGraph[node2].remove(node1)
    return resultGraph


import random
#ta maze guide, https://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm
def kruskals(templateGraph):
    maze = dict()
    for key in templateGraph:
        maze[key] = [] #every cell in individual and unconnected
    allEdges = []
    for node1 in maze:
        for node2 in maze:
            if node1 != node2:
                if node2 in templateGraph[node1]:
                    if (node2, node1) not in allEdges:
                        allEdges.append((node1, node2))
    random.shuffle(allEdges)
    for node1, node2 in allEdges:
        if BFS(node1, node2, maze) == None:
            maze[node1].append(node2)
            maze[node2].append(node1)
    return maze

