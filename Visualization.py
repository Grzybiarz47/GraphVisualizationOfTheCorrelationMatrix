from colour import Color
import matplotlib.pyplot as plt
import numpy as np
import igraph as ig
import seaborn as sns
import settings

class Visualization:
    @staticmethod
    def drawGraph(weights, edges, sectors):
        vertices_colors = dict({
            "OTH" : "#FFFFFF",
            "ENG" : "#626567",
            "MAT" : "#3498DB",
            "IND" : "#9B59B6",
            "CONSD" : "#F9E79F",
            "CONSS" : "#CA6F1E",
            "HC" : "#E74C3C",
            "FIN" : "#48C9B0",
            "IT" : "#25F62B",
            "COMMS" : "#25EDF6",
            "UTIL" : "#F28F1C",
            "RE" : "#C5B4E3"
        })
        edge_colors = list(Color("red").range_to(Color("cornsilk"), 10))
        min_weight = 0
        max_weight = 0
        if weights != []:
            min_weight = min(weights)
            max_weight = max(weights)
        diff = (max_weight - min_weight) / 9
        weight_index = []

        for w in weights:
            weight_index.append(int((w - min_weight) / diff))

        g = ig.Graph(settings.n, edges)
        g["title"] = "Correlation matrix MST"
        g.vs["name"] = settings.column_names
        g.es["weight"] = weight_index

        _, ax = plt.subplots(figsize=(20, 20))
        layout = g.layout_auto()
        if settings.circular:
            layout = g.layout_reingold_tilford_circular()
        ig.plot(
            g,
            target=ax,
            layout=layout,
            vertex_size=0.325,
            vertex_frame_width=1.0,
            vertex_frame_color="black",
            vertex_label=g.vs["name"],
            vertex_label_size=6.0,
            vertex_color=[vertices_colors[sectors[name]] for name in g.vs["name"]],
            edge_color = [edge_colors[index].hex for index in g.es["weight"]],
            edge_length = 2.0
        )
        plt.show()

    @staticmethod
    def drawStats(dates, stats):
        lengths, means, centrals, occupation_layer, robust, variance, skewness, kurtosis, num_edges = stats
        labels = list()
        for elem in centrals:
            labels.append(settings.column_names[elem])

        _, axs = plt.subplots(3, 3, figsize=(15, 12))
        axs[0, 0].plot(dates, lengths)
        axs[0, 0].set_title("Mean length")
        axs[0, 1].plot(dates, means)
        axs[0, 1].set_title("Mean coefficient")
        axs[0, 2].plot(dates, labels, 'ro')
        axs[0, 2].set_title("Central nodes")
        axs[1, 0].plot(dates, occupation_layer)
        axs[1, 0].set_title("Mean occupation layer")
        axs[1, 1].plot(dates[1:], robust)
        axs[1, 1].set_title("Robustness")
        axs[1, 2].plot(dates, variance)
        axs[1, 2].set_title("Variance")
        axs[2, 0].plot(dates, skewness)
        axs[2, 0].set_title("Skewness")
        axs[2, 1].plot(dates, kurtosis)
        axs[2, 1].set_title("Kurtosis")
        axs[2, 2].plot(dates, num_edges)
        axs[2, 2].set_title("Number of edges")
        plt.show()

    @staticmethod
    def drawMatrix(matrix, sectors):
        plt.figure(figsize=(15, 12))
        printed_matrix = np.zeros(shape=(settings.n, settings.n))
        names = sorted(sectors.items(), key=lambda x:(x[1], x[0]))
        names = [val[0] for val in names]
        old_indices = []
        for i in range(settings.n):
            old_indices.append(settings.column_names.index(names[i]))

        for i in range(settings.n):
            for j in range(settings.n):
                old_i = old_indices[i]
                old_j = old_indices[j]
                printed_matrix[i][j] = matrix[old_i][old_j]

        sns.set(font_scale=0.75)
        plot = sns.heatmap(printed_matrix, xticklabels=names, yticklabels=names)
        plt.show()
        