from Visualization import Visualization
from colour import Color
import matplotlib.pyplot as plt
import igraph as ig
import settings
import imageio

class Animation:
    data = []
    ths = []
    sectors = []

    @staticmethod
    def createAnimation(sectors):
        Animation.sectors = sectors
        time = len(Animation.data)

        #create fixed layout for all plots
        last_edges = Animation.data[len(Animation.data) - 1][1]
        g = ig.Graph(settings.n, last_edges)
        layout = g.layout_auto()

        for t in range(time):
            Animation.__createFrame(t, layout)
        
        frames = []
        for t in range(time):
            image = imageio.v2.imread(f'./img/img_{t}.png')
            frames.append(image)

        imageio.mimsave('./img/threshold_graph.gif', frames, duration=2000)

    @staticmethod
    def __createFrame(frame, layout):
        weights, edges = Animation.data[frame]
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
        ig.plot(
            g,
            target=ax,
            layout=layout,
            vertex_size=0.3,
            vertex_frame_width=1.0,
            vertex_frame_color="black",
            vertex_label=g.vs["name"],
            vertex_label_size=5.75,
            vertex_color=[Visualization.vertices_colors[Animation.sectors[name]] for name in g.vs["name"]],
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
        plt.savefig(f'./img/img_{frame}.png', transparent = False, facecolor='white')
        plt.close()

    @staticmethod
    def clean():
        Animation.data = []
        Animation.ths = []
        Animation.sectors = []