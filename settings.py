
def init():
    global n
    global column_names
    global window_size
    global step_size
    global threshold
    global minimal_edges
    global window_start
    global window_end
    global act_single_window
    global circular
    global all_stats_together
    global animate

    n = 0
    column_names = []
    window_size = 500
    step_size = 21
    threshold = 1
    minimal_edges = 2
    window_start = 0
    window_end = 500
    act_single_window = False
    circular = False
    all_stats_together = False
    animate = False