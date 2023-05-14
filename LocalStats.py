import settings
import numpy as np

class LocalStats:
    @staticmethod
    def findLength(weights, num_edges):
        return sum(weights)/num_edges

    @staticmethod
    def findCentralNode(edges, corr):
        vertex_degree = np.zeros(settings.n)
        sum_weights = np.zeros(settings.n)
        for edge in edges:
            a, b = edge
            vertex_degree[a] += 1
            vertex_degree[b] += 1
            sum_weights[a] += corr[a][b]
            sum_weights[b] += corr[b][a]
        
        res_array = []
        for i in range(settings.n):
            res_array.append((vertex_degree[i], -sum_weights[i]))
        return res_array.index(max(res_array))

    @staticmethod
    def findMeanOccupationLayer(edges, center):
        result = np.full(settings.n, -1, dtype=int)
        result[center] = 0
        change_occured = True
        while edges != [] and change_occured:
            change_occured = False
            e = edges
            for edge in e:
                a, b = edge
                if result[a] != -1 and result[b] == -1:
                    result[b] = result[a] + 1
                    edges.remove(edge)
                    change_occured = True
                elif result[a] == -1 and result[b] != -1:
                    result[a] = result[b] + 1
                    edges.remove(edge)
                    change_occured = True
        
        max_val = max(result)
        for i in range(len(result)):
            if result[i] == -1:
                result[i] = max_val + 1
                    
        s = np.sum(result)
        return [result, s/settings.n]

    @staticmethod
    def findRobustness(prev_edges, new_edges):
        intersection = list(set(prev_edges).intersection(new_edges))
        return len(intersection)/len(prev_edges)