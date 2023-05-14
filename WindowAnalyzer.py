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
    windowed_xi_LP_iso = []

    def __init__(self, df):
        self.data = df
        self.__calcWindowedXiLpOracleIso()
        sys.path.insert(0,'./shrinkage')
    
    def getSingleWindow(self, window, graph_type=GraphTypes.MST, shrinkage_type=ShrinkageTypes.NO_SHRINKAGE):
        return self.__pickWindowResults(window, graph_type, shrinkage_type)
    
    def getAllWindows(self, df, graph_type=GraphTypes.MST, shrinkage_type=ShrinkageTypes.NO_SHRINKAGE, print_stats=False):
        return self.__createWindows(df, graph_type, shrinkage_type, print_stats)

    def __shrinkConvMatrix(self, df):
        real_data = DataMatrix(
            method='load',
            Y=df.to_numpy().T
        )

        LPS = LedoitPecheShrinkage(
            Y=real_data.Y,
            T=settings.window_size
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
            T=settings.window_size
        )

        conv = LPS.rie(x=self.windowed_xi_LP_iso)
        return conv
    
    def __calcCorrelationCoef(self, a, b):
        a_avg = np.average(a)
        b_avg = np.average(b)
        ab_product = a[:]*b[:]
        ab_product_avg = np.average(ab_product)
        numerator = ab_product_avg - a_avg*b_avg
        a_squered = a[:]*a[:]
        b_squered = b[:]*b[:]
        a_squered_avg = np.average(a_squered)
        b_squered_avg = np.average(b_squered)
        
        p = (numerator)/math.sqrt((a_squered_avg - a_avg*a_avg)*(b_squered_avg - b_avg*b_avg))
        return p
    
    def __calcCorrelationCoefAfterShrinkage(self, a, b, conv_element):
        a_avg = np.average(a)
        b_avg = np.average(b)
        numerator = conv_element - a_avg*b_avg
        a_squered = a[:]*a[:]
        b_squered = b[:]*b[:]
        a_squered_avg = np.average(a_squered)
        b_squered_avg = np.average(b_squered)
        
        p = (numerator)/math.sqrt((a_squered_avg - a_avg*a_avg)*(b_squered_avg - b_avg*b_avg))
        return p

    def __createCoefMatrix(self, df):
        corr = np.zeros(shape=(settings.n, settings.n))
        for i in range(settings.n):
            for j in range(settings.n):
                corr[i][j] = self.__calcCorrelationCoef(df[settings.column_names[i]][:], df[settings.column_names[j]][:])

        return corr
    
    def __createImprovedCoefMatrix(self, df):
        corr = np.zeros(shape=(settings.n, settings.n))
        conv = self.__shrinkConvMatrix(df)
        for i in range(settings.n):
            for j in range(settings.n):
                corr[i][j] = self.__calcCorrelationCoefAfterShrinkage(df[settings.column_names[i]][:], df[settings.column_names[j]][:], conv[i][j])

        return corr
    
    def __createImprovedWindowedCoefMatrix(self, df):
        corr = np.zeros(shape=(settings.n, settings.n))
        conv = self.__shrinkWindowedConvMatrix(df)
        for i in range(settings.n):
            for j in range(settings.n):
                corr[i][j] = self.__calcCorrelationCoefAfterShrinkage(df[settings.column_names[i]][:], df[settings.column_names[j]][:], conv[i][j])

        return corr
    
    def __createDistanceMatrix(self, corr):
        distances = np.zeros(shape=(settings.n, settings.n))
        for i in range(settings.n):
            for j in range(settings.n):
                if i == j:
                    distances[i][j] = 0
                else:
                    p = corr[i][j]
                    if p > 1:
                        p = 1
                    distances[i][j] = math.sqrt(2.0*(1 - p))

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

        prev_edges = []
        Lengths = []
        Centrals = []
        Dates = []    
        Occupation = []
        Robustness = []
        Num_edges = []
        while start_time + settings.window_size < period:
            end_time = start_time + settings.window_size
            window = df[start_time:end_time]
            Dates.append(end_time)
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
            levels, mean_occupation_layer = LocalStats.findMeanOccupationLayer(edges.copy(), central_node_index)
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
            
    def __calcWindowedXiLpOracleIso(self):
        real_data = DataMatrix(
            method='load',
            Y=self.data.to_numpy().T
        )

        LPS = LedoitPecheShrinkage(
            Y=real_data.Y,
            T=settings.window_size,
            T_out=settings.step_size
        )

        self.windowed_xi_LP_iso = LPS.xi_oracle_mwcv_iso