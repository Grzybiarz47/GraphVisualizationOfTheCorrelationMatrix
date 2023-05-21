from enum import Enum
from Graphs import Graphs
from GlobalStats import GlobalStats
from LocalStats import LocalStats
import pandas as pd
import numpy as np
import math
import settings

import sys
sys.path.insert(0,'./shrinkage')
from shrinkage.rie_lp import LedoitPecheShrinkage
from shrinkage.simulation import DataMatrix

class GraphTypes(Enum):
    MST = 1
    THRESHOLD_GRAPH = 2
    MINIMAL_N_EDGES = 3

class ShrinkageTypes(Enum):
    NO_SHRINKAGE = 1,
    SIMPLE_SHRINKAGE_LP = 2,
    WINDOWED_SHRINKAGE_LP = 3

class WindowAnalyzer:
    data = pd.DataFrame()

    def __init__(self, df):
        self.data = df
        sys.path.insert(0,'./shrinkage')
    
    def getSingleWindow(self, window, graph_type=GraphTypes.MST, shrinkage_type=ShrinkageTypes.NO_SHRINKAGE):
        return self.__pickWindowResults(window, graph_type, shrinkage_type)
    
    def getAllWindows(self, df, graph_type=GraphTypes.MST, shrinkage_type=ShrinkageTypes.NO_SHRINKAGE, print_stats=False):
        return self.__createWindows(df, graph_type, shrinkage_type, print_stats)
    
    def __createConvMatrix(self, df):
        real_data = DataMatrix(
            method='load',
            Y=df.to_numpy().T
        )

        LPS = LedoitPecheShrinkage(
            Y=real_data.Y,
            T=self.__calcWindowSize()
        )

        conv = LPS.rie(x=LPS.E_eigval)
        return conv

    def __shrinkConvMatrix(self, df):
        real_data = DataMatrix(
            method='load',
            Y=df.to_numpy().T
        )

        LPS = LedoitPecheShrinkage(
            Y=real_data.Y,
            T=self.__calcWindowSize()
        )

        conv = LPS.rie(x=LPS.xi_LP)
        return conv

    def __shrinkWindowedConvMatrix(self, df):
        real_data = DataMatrix(
            method='load',
            Y=df.to_numpy().T
        )

        LPS = LedoitPecheShrinkage(
            Y=real_data.Y,
            T=self.__calcWindowSize(),
            T_out=settings.year_span
        )

        conv = LPS.rie(x=LPS.xi_oracle_mwcv_iso)
        return conv
    
    def __calcCorrelationCoef(self, conv_i, conv_j, conv_ij):
        p = (conv_ij)/math.sqrt((conv_i)*(conv_j))
        return p

    def __createCoefMatrix(self, df):
        corr = np.zeros(shape=(settings.n, settings.n))
        conv = self.__createConvMatrix(df)
        for i in range(settings.n):
            for j in range(settings.n):
                corr[i][j] = self.__calcCorrelationCoef(conv[i][i], conv[j][j], conv[i][j])

        return corr
    
    def __createImprovedCoefMatrix(self, df):
        corr = np.zeros(shape=(settings.n, settings.n))
        conv = self.__shrinkConvMatrix(df)
        for i in range(settings.n):
            for j in range(settings.n):
                corr[i][j] = self.__calcCorrelationCoef(conv[i][i], conv[j][j], conv[i][j])

        return corr
    
    def __createImprovedWindowedCoefMatrix(self, df):
        corr = np.zeros(shape=(settings.n, settings.n))
        conv = self.__shrinkWindowedConvMatrix(df)
        for i in range(settings.n):
            for j in range(settings.n):
                corr[i][j] = self.__calcCorrelationCoef(conv[i][i], conv[j][j], conv[i][j])

        return corr
    
    def __createDistanceMatrix(self, corr):
        distances = np.zeros(shape=(settings.n, settings.n))
        for i in range(settings.n):
            for j in range(settings.n):
                if i == j:
                    distances[i][j] = 0
                else:
                    p = corr[i][j]
                    distances[i][j] = math.sqrt(2.0*abs(1 - p))

        return distances
    
    def __pickWindowResults(self, window, graph_type=GraphTypes.MST, shrinkage_type=ShrinkageTypes.NO_SHRINKAGE):
        corrMatrix = np.zeros(shape=(settings.n, settings.n))
        if shrinkage_type == ShrinkageTypes.NO_SHRINKAGE:
            corrMatrix = self.__createCoefMatrix(window)
        elif shrinkage_type == ShrinkageTypes.SIMPLE_SHRINKAGE_LP:
            corrMatrix = self.__createImprovedCoefMatrix(window)
        elif shrinkage_type == ShrinkageTypes.WINDOWED_SHRINKAGE_LP:
            corrMatrix = self.__createImprovedWindowedCoefMatrix(window)

        distMatrix = self.__createDistanceMatrix(corrMatrix)
        g = Graphs()

        if graph_type == GraphTypes.MST:
            graph, edges, weights = g.createTree(distMatrix)
        elif graph_type == GraphTypes.THRESHOLD_GRAPH:
            graph, edges, weights = g.createGraphWithThreshold(distMatrix)
        elif graph_type == GraphTypes.MINIMAL_N_EDGES:
            graph, edges, weights = g.createMinimalNTree(distMatrix)

        return [corrMatrix, distMatrix, graph, edges, weights]
    
    def __createWindows(self, df, graph_type, shrinkage_type, print_stats):
        period = df.shape[0]
        start_time = 0
        global_stats = GlobalStats()

        if shrinkage_type == ShrinkageTypes.WINDOWED_SHRINKAGE_LP:
            period -= 2*settings.year_span

        prev_edges = []
        Lengths = []
        Centrals = []
        Dates = []    
        Occupation = []
        Robustness = []
        Num_edges = []

        window_size = self.__calcWindowSize()
        while start_time + window_size < period:
            end_time = start_time + window_size
            Dates.append(end_time)
            if shrinkage_type == ShrinkageTypes.WINDOWED_SHRINKAGE_LP:
                end_time += 2*settings.year_span
            window = df[start_time:end_time]

            start_time += settings.step_size
            corrMatrix, _, _, edges, weights = self.__pickWindowResults(window, graph_type, shrinkage_type)
            mean_coef, variance, skewness, kurtosis = global_stats.makeNewStats(corrMatrix)

            #norm length
            newL = LocalStats.findLength(weights, len(edges))
            Lengths.append(newL)
            
            #central node
            central_node_index = LocalStats.findCentralNode(edges, corrMatrix)
            Centrals.append(central_node_index)
            
            #mean occupation layer
            _, mean_occupation_layer = LocalStats.findMeanOccupationLayer(edges.copy(), central_node_index)
            Occupation.append(mean_occupation_layer)

            #robustness
            r = 0
            if prev_edges != []:
                r = LocalStats.findRobustness(prev_edges, edges)
                Robustness.append(r)
            prev_edges = edges

            #num edges
            Num_edges.append(len(edges))

            if print_stats == True:
                print("Length: " + str(newL))
                print("Mean coefficient: " + str(mean_coef))
                print("Central node: " + settings.column_names[central_node_index])
                print("Mean ocupation layer: " + str(mean_occupation_layer))
                print("Robustness: " + str(r))
                print("Variance: " + str(variance))
                print("Skewness: " + str(skewness))
                print("Kurtosis: " + str(kurtosis))
                print("Number of edges: " + str(len(edges)))
                print('\n')

        Means, Variances, Skewness, Kurtosis = global_stats.getAllStats()
        return [Dates, Lengths, Means, Centrals, Occupation, Robustness, Variances, Skewness, Kurtosis, Num_edges]
    
    def __calcWindowSize(self):
        T = settings.window_size
        if settings.act_single_window:
            T = settings.window_end - settings.window_start
        return T
