from colour import Color
import matplotlib.pyplot as plt
import numpy as np
import igraph as ig
import seaborn as sns
import settings

class Visualization:
    vertices_colors = dict({
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
        "RE" : "#C5B4E3",
        "OTH" : "#FFFFFF"
    })

    @staticmethod
    def drawGraph(weights, edges, sectors):
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

        fig, ax = plt.subplots(figsize=(20, 20))
        layout = g.layout_auto()
        if settings.circular:
            layout = g.layout_reingold_tilford_circular()
        ig.plot(
            g,
            target=ax,
            layout=layout,
            vertex_size=0.3,
            vertex_frame_width=1.0,
            vertex_frame_color="black",
            vertex_label=g.vs["name"],
            vertex_label_size=5.75,
            vertex_color=[Visualization.vertices_colors[sectors[name]] for name in g.vs["name"]],
            edge_color = [edge_colors[index].hex for index in g.es["weight"]],
            edge_length = 5.0
        )
        keys = list(Visualization.vertices_colors.keys())
        keys.sort()
        vals = []
        for key in keys:
            vals.append(Visualization.vertices_colors[key])
        leg = plt.legend(keys, fontsize=10)
        for i, j in enumerate(leg.legendHandles):
            j.set_color(vals[i])
        fig.tight_layout()
        plt.get_current_fig_manager().window.state('zoomed')
        plt.show()

    @staticmethod
    def drawStats(dates, stats):
        lengths, means, centrals, occupation_layer, robust, variance, skewness, kurtosis, num_edges = stats
        labels = list()
        for elem in centrals:
            labels.append(settings.column_names[elem])

        fig, axs = plt.subplots(3, 3, figsize=(15, 12))
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
        fig.tight_layout()
        plt.get_current_fig_manager().window.state('zoomed')
        plt.show()

    @staticmethod
    def drawAllStatsTogether(dates, no_shrinkage_stats, simple_lp_shrinkage):
        labels_no_shrinkage = list()
        labels_lp_shrinkage = list()
        for elem in no_shrinkage_stats[2]:
            labels_no_shrinkage.append(settings.column_names[elem])
        for elem in simple_lp_shrinkage[2]:
            labels_lp_shrinkage.append(settings.column_names[elem])

        fig, axs = plt.subplots(4, 3, figsize=(20, 16))
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)
        for i in range(3):
            for j in range(3):
                x = dates
                if i == 0 and j == 2:
                    continue
                elif i == 1 and j == 1:
                    x = dates[1:]
                axs[i, j].plot(x, no_shrinkage_stats[i*3 + j], label="No shrinkage")
                axs[i, j].plot(x, simple_lp_shrinkage[i*3 + j], label="LP shrinkage on static window")

        axs[3, 0].plot(x, labels_no_shrinkage, 'ro')
        axs[3, 1].plot(x, labels_lp_shrinkage, 'ro')
        
        axs[0, 0].set_title("Mean length", fontsize=7, x=.5, y=.9)
        axs[0, 1].set_title("Mean coefficient", fontsize=7, x=.5, y=.9)
        axs[1, 0].set_title("Mean occupation layer", fontsize=7, x=.5, y=.9)
        axs[1, 1].set_title("Robustness", fontsize=7, x=.5, y=.9)
        axs[1, 2].set_title("Variance", fontsize=7, x=.5, y=.9)
        axs[2, 0].set_title("Skewness", fontsize=7, x=.5, y=.9)
        axs[2, 1].set_title("Kurtosis", fontsize=7, x=.5, y=.9)
        axs[2, 2].set_title("Number of edges", fontsize=7, x=.5, y=.9)
        axs[3, 0].set_title("Central nodes", fontsize=7, x=.5, y=.9)
        axs[3, 1].set_title("Central nodes - LP", fontsize=7, x=.5, y=.9)
        handles, labels = axs[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, fontsize=15, loc="upper right")
        for a in axs.flatten():
            a.tick_params(axis='both', which='major', labelsize=7)
            a.tick_params(axis='both', which='minor', labelsize=7)
        fig.delaxes(axs[0][2])
        fig.delaxes(axs[3][2])
        fig.tight_layout()
        plt.get_current_fig_manager().window.state('zoomed')
        plt.show()

    @staticmethod
    def drawMatrix(matrix, raw_sectors):
        plt.figure(figsize=(15, 12))
        printed_matrix = np.zeros(shape=(settings.n, settings.n))
        names_and_sectors = sorted(raw_sectors.items(), key=lambda x:(x[1], x[0]))
        names = [val[0] for val in names_and_sectors]
        sectors = [val[1] for val in names_and_sectors]
        old_indices = []
        for i in range(settings.n):
            old_indices.append(settings.column_names.index(names[i]))

        for i in range(settings.n):
            for j in range(settings.n):
                old_i = old_indices[i]
                old_j = old_indices[j]
                printed_matrix[i][j] = matrix[old_i][old_j]

        sns.set(font_scale=0.6)
        ax = sns.heatmap(printed_matrix, xticklabels=names, yticklabels=names)
        for i, tick_label in enumerate(ax.axes.get_xticklabels()):
            if sectors[i] != 'OTH':
                tick_label.set_color(Visualization.vertices_colors[sectors[i]])
        for i, tick_label in enumerate(ax.axes.get_yticklabels()):
            if sectors[i] != 'OTH':
                tick_label.set_color(Visualization.vertices_colors[sectors[i]])
        plt.show()