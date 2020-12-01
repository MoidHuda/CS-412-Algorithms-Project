from  networkx.algorithms import bipartite as nx 
from operator import itemgetter
import numpy as np

G = nx.random_graph(5000,5000,0.4)
partition_l =   set(map(itemgetter(0),G.edges()))

np.savetxt("file1.txt", nx.biadjacency_matrix(G,partition_l).toarray()) 
