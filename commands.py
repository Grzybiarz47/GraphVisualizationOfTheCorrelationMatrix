from DataFrameHandler import DataFrameHandler
from WindowAnalyzer import ShrinkageTypes, GraphTypes, WindowAnalyzer
from Visualization import Visualization
import numpy as np
import matplotlib.pyplot as plt
import settings

def draw(draw_type, graph_type, shrinkage_type, path):
    g = GraphTypes.MST
    if graph_type == 1:
        g = GraphTypes.MINIMAL_N_EDGES
    elif graph_type == 2:
        g = GraphTypes.THRESHOLD_GRAPH

    s = ShrinkageTypes.NO_SHRINKAGE
    if shrinkage_type == 1:
        s = ShrinkageTypes.SIMPLE_SHRINKAGE_LP
    elif shrinkage_type == 2:
        s = ShrinkageTypes.WINDOWED_SHRINKAGE_LP
    
    if draw_type == 0:
        draw_single_graph(g, s, path)
    elif draw_type == 1:
        draw_all_stats(g, s, path)

def draw_single_graph(graph_type, shrinkage_type, path):
    df, dates, sectors = read(path)
    analyzer = WindowAnalyzer(df)

    corr_matrix, dist_matrix, _, edges, weights = analyzer.getSingleWindow(
        df[settings.window_start:settings.window_end], graph_type, shrinkage_type)
    print(str(dates[settings.window_start]) + " - " + str(dates[settings.window_end]))

    Visualization.drawGraph(weights, edges, sectors, circular=False)
    # Visualization.drawMatrix(corr_matrix, sectors)
    # Visualization.drawMatrix(dist_matrix, sectors)

def draw_all_stats(graph_type, shrinkage_type, path):
    df, dates, _ = read(path)
    analyzer = WindowAnalyzer(df)

    window_dates, lengths, means, centrals, occupation_layer, robust, variance, skewness, kurtosis, num_edges = analyzer.getAllWindows(df, 
                                                                                                                                       graph_type, 
                                                                                                                                       shrinkage_type, 
                                                                                                                                       print_stats=True)
    window_dates = dates.iloc[window_dates]

    Visualization.drawStats(window_dates, [lengths, means, centrals, occupation_layer, robust, variance, skewness, kurtosis, num_edges])

def read(path):
    df_handler = DataFrameHandler()
    df = df_handler.read(path)
    dates = df_handler.getDates()
    sectors = df_handler.getSectors()
    return [df, dates, sectors]
