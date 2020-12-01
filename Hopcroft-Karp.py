
def bipartiteMatch(graph):

    # initialize greedy matching 
    matching = {}
    for u in range(len(graph)):
        for v in range(len(graph[u])):
            if graph[u][v] != 0 and v not in matching:
                matching[v] = u
                break
    
    while 1:
        preds = {}
        unmatched = []
        pred = dict([(u,unmatched) for u in range(len(graph))])
        for v in matching:
            del pred[matching[v]]
        layer = list(pred)
        
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

if __name__ == '__main__':
    import timeit
    import numpy as np
    content = np.loadtxt('file1.txt').tolist()
     
    start = timeit.default_timer()
    bipartiteMatch(content)

    stop = timeit.default_timer()

    print('Time: ', stop - start)  
