from DataFrameHandler import DataFrameHandler
from WindowAnalyzer import ShrinkageTypes, GraphTypes, WindowAnalyzer
from Visualization import Visualization
import numpy as np
import matplotlib.pyplot as plt
import settings

def draw(draw_type, graph_type, shrinkage_type, colummn_picked, path):
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
        draw_single_graph(g, s, colummn_picked, path)
    elif draw_type == 1:
        draw_matrix(g, s, colummn_picked, path)
    elif draw_type == 2:
        draw_all_stats(g, s, colummn_picked, path)

def draw_single_graph(graph_type, shrinkage_type, colummn_picked, path):
    df, dates, sectors = read(path, colummn_picked)
    analyzer = WindowAnalyzer(df)
    window_start = settings.window_start
    window_end = settings.window_end
    if shrinkage_type == ShrinkageTypes.WINDOWED_SHRINKAGE_LP:
        window_end += 2*settings.year_span

    _, _, _, edges, weights = analyzer.getSingleWindow(
        df[window_start:window_end], graph_type, shrinkage_type)
    print(str(dates[window_start]) + " - " + str(dates[window_end]))

    Visualization.drawGraph(weights, edges, sectors)

def draw_all_stats(graph_type, shrinkage_type, colummn_picked, path):
    df, dates, _ = read(path, colummn_picked)
    analyzer = WindowAnalyzer(df)

    window_dates, lengths, means, centrals, occupation_layer, robust, variance, skewness, kurtosis, num_edges = analyzer.getAllWindows(df, 
                                                                                                                                       graph_type, 
                                                                                                                                       shrinkage_type, 
                                                                                                                                       print_stats=True)
    window_dates = dates.iloc[window_dates]

    Visualization.drawStats(window_dates, [lengths, means, centrals, occupation_layer, robust, variance, skewness, kurtosis, num_edges])

def draw_matrix(graph_type, shrinkage_type, colummn_picked, path):
    df, dates, sectors = read(path, colummn_picked)
    analyzer = WindowAnalyzer(df)
    window_start = settings.window_start
    window_end = settings.window_end
    if shrinkage_type == ShrinkageTypes.WINDOWED_SHRINKAGE_LP:
        window_end += 2*settings.year_span

    corr_matrix, _, _, _, _ = analyzer.getSingleWindow(
        df[window_start:window_end], graph_type, shrinkage_type)
    print(str(dates[window_start]) + " - " + str(dates[window_end]))

    Visualization.drawMatrix(corr_matrix, sectors)

def read(path, colummn_picked):
    df_handler = DataFrameHandler()
    df = df_handler.read(path, colummn_picked)
    dates = df_handler.getDates()
    sectors = df_handler.getSectors()
    return [df, dates, sectors]
