from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse.csgraph import breadth_first_order
from scipy.sparse import csr_matrix
import settings

class Graphs:
    def createTree(self, distMatrix):
        tree = minimum_spanning_tree(distMatrix)
        treeArr = tree.toarray()
        edges, weights = self.__extractEdges(treeArr)
        edges = self.__sortEdges(edges)
        return [tree, edges, weights]
    
    def createGraphWithThreshold(self, distMatrix):
        tmp = distMatrix.copy()
        for i in range(settings.n):
            for j in range(i):
                if tmp[i][j] > settings.threshold:
                    tmp[i][j] = 0
                tmp[j][i] = 0
                    
        graph = csr_matrix(tmp)
        graphArr = graph.toarray()
        edges, weights = self.__extractEdges(graphArr, symmetrical=True)
        edges = self.__sortEdges(edges)
        return [graph, edges, weights]
    
    def createMinimalNTree(self, distMatrix):
        tmp = distMatrix.copy()
        for i in range(settings.n):
            row = tmp[i].copy()
            row.sort()
            weights = row[1:settings.minimal_edges + 1]
            for j in range(settings.n):
                if tmp[i][j] not in weights:
                    tmp[i][j] = 0
            
        graph = csr_matrix(tmp)
        graphArr = graph.toarray()
        edges, weights = self.__extractEdges(graphArr)
        edges = self.__sortEdges(edges)
        return [graph, edges, weights]

    def __sortEdges(self, edges):
        res = []
        for edge in edges:
            a, b = edge
            if a < b:
                res.append((a, b))
            else:
                res.append((b, a))
        return res

    def __extractEdges(self, graph, symmetrical=False):
        edges = []
        weights = []
        for i in range(settings.n):
            if symmetrical:
                for j in range(i):
                    if graph[i][j] != 0:
                        edges.append((i, j))
                        weights.append(graph[i][j])
            else:
                for j in range(settings.n):
                    if graph[i][j] != 0 and (j, i) not in edges:
                        edges.append((i, j))
                        weights.append(graph[i][j])

        return [edges, weights]