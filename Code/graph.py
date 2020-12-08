
class Edge(object):
  def __init__(self, u, v, w):
    self.source = u
    self.target = v
    self.capacity = w

  def __repr__(self):
    return "%s->%s:%s" % (self.source, self.target, self.capacity)


class FlowNetwork(object):
  def  __init__(self):
    self.adj = {}
    self.flow = {}

  def AddVertex(self, vertex):
    self.adj[vertex] = []

  def GetEdges(self, v):
    return self.adj[v]

  def AddEdge(self, u, v, w = 0):
    if u == v:
      raise ValueError("u == v")
    if u not in self.adj.keys():
        self.adj[u] = []
    if v not in self.adj.keys():
        self.adj[v] = []
    edge = Edge(u, v, w)
    redge = Edge(v, u, 0)
    edge.redge = redge
    redge.redge = edge
    self.adj[u].append(edge)
    self.adj[v].append(redge)
    # Intialize all flows to zero
    self.flow[edge] = 0
    self.flow[redge] = 0

  def FindPath(self, source, target, path):
    if source == target:
      return path
    for edge in self.GetEdges(source):
      residual = edge.capacity - self.flow[edge]
      if residual > 0 and not (edge, residual) in path:
        result = self.FindPath(edge.target, target, path + [(edge, residual)])
        if result != None:
          return result

  def MaxFlow(self, source, target):
    path = self.FindPath(source, target, [])
    # print('path after enter MaxFlow: %s' % path)
    # for key in self.flow:
    #   print('%s:%s' % (key,self.flow[key]))
    # print('-' * 20)
    while path != None:
      flow = min(res for edge, res in path)
      for edge, res in path:
        self.flow[edge] += flow
        self.flow[edge.redge] -= flow
    #   for key in self.flow:
    #     print('%s:%s' % (key,self.flow[key]))
      path = self.FindPath(source, target, [])
    #   print('path inside of while loop: %s' % path)
    # for key in self.flow:
    #   print('%s:%s' % (key,self.flow[key]))
    return sum(self.flow[edge] for edge in self.GetEdges(source))
  
def bipartiteMatch(graph):
    '''Find maximum cardinality matching of a bipartite graph (U,V,E).
    The input format is a dictionary mapping members of U to a list
    of their neighbors in V.  The output is a triple (M,A,B) where M is a
    dictionary mapping members of V to their matches in U, A is the part
    of the maximum independent set in U, and B is the part of the MIS in V.
    The same object may occur in both U and V, and is treated as two
    distinct vertices if this happens.'''
    
    # initialize greedy matching (redundant, but faster than full search)
    matching = {}
    for u in range(len(graph)):
        for v in range(len(graph[u])):
            if graph[u][v] != 0 and v not in matching:
                matching[v] = u
                break
    
    while 1:
        # structure residual graph into layers
        # pred[u] gives the neighbor in the previous layer for u in U
        # preds[v] gives a list of neighbors in the previous layer for v in V
        # unmatched gives a list of unmatched vertices in final layer of V,
        # and is also used as a flag value for pred[u] when u is in the first layer
        preds = {}
        unmatched = []
        pred = dict([(u,unmatched) for u in range(len(graph))])
        for v in matching:
            del pred[matching[v]]
        layer = list(pred)
        
        # repeatedly extend layering structure by another pair of layers
        while layer and not unmatched:
            newLayer = {}
            for u in layer:
                for v in range(len(graph[u])):
                    if graph[u][v] != 0 and v not in preds:
                        newLayer.setdefault(v,[]).append(u)
            layer = []
            for v in newLayer:
                preds[v] = newLayer[v]
                if v in matching:
                    layer.append(matching[v])
                    pred[matching[v]] = v
                else:
                    unmatched.append(v)
        
        # did we finish layering without finding any alternating paths?
        if not unmatched:
            unlayered = {}
            for u in range(len(graph)):
                for v in range(len(graph[u])):
                    if graph[u][v] != 0 and v not in preds:
                        unlayered[v] = None
            return (matching,list(pred),list(unlayered))

        # recursively search backward through layers to find alternating paths
        # recursion returns true if found path, false otherwise
        def recurse(v):
            if v in preds:
                L = preds[v]
                del preds[v]
                for u in L:
                    if u in pred:
                        pu = pred[u]
                        del pred[u]
                        if pu is unmatched or recurse(pu):
                            matching[v] = u
                            return 1
            return 0

        for v in unmatched: recurse(v)

import sys

if __name__ == '__main__':
    import timeit
    import numpy as np
    from operator import itemgetter
    from  networkx.algorithms import bipartite as nx
    import networkx.convert as nc
    from hungarian_algorithm import algorithm 
    from networkx.algorithms import flow as fl
    lst  = []
    for k in range(500,10000,500):
        a = int(np.random.uniform(1,k))
        lst.append((a,k-a))
    for i,j in lst:
        G = nx.random_graph(i,j, 1) 
        partition_l =   set(map(itemgetter(0),G.edges()))
        content = nx.biadjacency_matrix(G,partition_l).toarray().tolist() 
        # print(len(content))

        start = timeit.default_timer()
        bipartiteMatch(content)
        stop = timeit.default_timer()

        print('Hopcroft-Karp Time: n: ',i+j, stop - start)  

        G = nx.random_graph((i+j)//2,(i+j)//2,1)
        start = timeit.default_timer()
        algorithm.find_matching(G,matching_type = 'max', return_type = 'list')

        stop = timeit.default_timer()

        print('Hungarian Time: n: ',i+j, stop - start)  