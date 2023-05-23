from PIL import ImageTk, Image
from tkinter import filedialog
import customtkinter
import commands
import settings

#SETUP
settings.init()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
app_label_text = "Graph visualization of the correlation matrix"
root = customtkinter.CTk()
root.title(app_label_text)
root.geometry("700x500")

main_frame = customtkinter.CTkScrollableFrame(master=root)
main_frame.pack(pady=20, padx=60, fill="both", expand=True)

#READ PATH
main_label = customtkinter.CTkLabel(master=main_frame, text=app_label_text, font=("Roboto", 24))
main_label.pack(pady=12, padx=10)

dir_path = customtkinter.StringVar(value="")
def read_directory():
    filename = filedialog.askdirectory()
    dir_path.set(filename)
    directory_label.configure(text=filename)
    print(filename)

read_button = customtkinter.CTkButton(master=main_frame, 
                                      text="Read path", 
                                      command=read_directory)
read_button.pack(pady=12, padx=10)

directory_label = customtkinter.CTkLabel(master=main_frame, text="Set directory of *.csv files", font=("Roboto", 15))
directory_label.pack(pady=12, padx=10)

#DRAW TYPE
radio_button_draw_type_var = customtkinter.IntVar(value=0)
def read_radio_button_draw_type():
    print("toggled draw type, current value:", radio_button_draw_type_var.get())
    if radio_button_draw_type_var.get() == 0 or radio_button_draw_type_var.get() == 1:
        entry_window_size.configure(state="disabled")
        entry_window_step_size.configure(state="disabled")
        entry_window_start.configure(state="normal")
        entry_window_end.configure(state="normal")
        checkbox.configure(state="disabled")
    elif radio_button_draw_type_var.get() == 2:
        entry_window_size.configure(state="normal")
        entry_window_step_size.configure(state="normal")
        entry_window_start.configure(state="disabled")
        entry_window_end.configure(state="disabled")
        checkbox.configure(state="normal")

radio_button_draw_type_frame = customtkinter.CTkFrame(master=main_frame)
radio_button_draw_type_frame.pack(pady=20, padx=60, fill="both")

radio_button_draw_type_single_window = customtkinter.CTkRadioButton(master=radio_button_draw_type_frame, 
                                                                    text="Draw graph for single window",
                                                                    command=read_radio_button_draw_type, 
                                                                    variable=radio_button_draw_type_var, 
                                                                    value=0)
radio_button_draw_type_single_window.pack(pady=12, padx=10)

radio_button_draw_type_draw_matrix = customtkinter.CTkRadioButton(master=radio_button_draw_type_frame, 
                                                                    text="Draw correlation matrix for single window",
                                                                    command=read_radio_button_draw_type, 
                                                                    variable=radio_button_draw_type_var, 
                                                                    value=1)
radio_button_draw_type_draw_matrix.pack(pady=12, padx=10)

entry_window_start = customtkinter.CTkEntry(master=radio_button_draw_type_frame, 
                                            placeholder_text="Window start")
entry_window_start.pack(pady=12, padx=10)

entry_window_end = customtkinter.CTkEntry(master=radio_button_draw_type_frame, 
                                          placeholder_text="Window end")
entry_window_end.pack(pady=12, padx=10)

radio_button_draw_type_all_stats = customtkinter.CTkRadioButton(master=radio_button_draw_type_frame, 
                                                                text="Draw stats",
                                                                command=read_radio_button_draw_type, 
                                                                variable=radio_button_draw_type_var, 
                                                                value=2)
radio_button_draw_type_all_stats.pack(pady=12, padx=10)

entry_window_size = customtkinter.CTkEntry(master=radio_button_draw_type_frame, 
                                           placeholder_text="Window size")
entry_window_size.configure(state="disabled")
entry_window_size.pack(pady=12, padx=10)

entry_window_step_size = customtkinter.CTkEntry(master=radio_button_draw_type_frame,
                                                placeholder_text="Window step size")
entry_window_step_size.configure(state="disabled")
entry_window_step_size.pack(pady=12, padx=10)

#DRAW ALL STATS
check_box_draw_all_stats_var = customtkinter.StringVar(value="off")
def read_checkbox_all_stats():
    print("checkbox toggled, current value:", check_box_draw_all_stats_var.get())

checkbox = customtkinter.CTkCheckBox(master=radio_button_draw_type_frame,
                                     text="Draw all stats together",
                                     command=read_checkbox_all_stats,
                                     variable=check_box_draw_all_stats_var,
                                     onvalue="on",
                                     offvalue="off")
checkbox.configure(state="disabled")
checkbox.pack(padx=12, pady=10)

#SHRINKAGE TYPES
radio_button_shrinkage_type_var = customtkinter.IntVar(value=0)
def read_radio_button_shrinkage_type():
    print("toggled shrink type, current value:", radio_button_shrinkage_type_var.get())

radio_button_shrinkage_type_frame = customtkinter.CTkFrame(master=main_frame)
radio_button_shrinkage_type_frame.pack(pady=20, padx=60, fill="both")

radio_button_shrinkage_type_mst = customtkinter.CTkRadioButton(master=radio_button_shrinkage_type_frame, 
                                                           text="No shrinkage",
                                                           command=read_radio_button_shrinkage_type, 
                                                           variable=radio_button_shrinkage_type_var, 
                                                           value=0)
radio_button_shrinkage_type_mst.pack(pady=12, padx=10)
radio_button_shrinkage_type_minnedges = customtkinter.CTkRadioButton(master=radio_button_shrinkage_type_frame, 
                                                                 text="LP shrinkage on static window", 
                                                                 command=read_radio_button_shrinkage_type, 
                                                                 variable=radio_button_shrinkage_type_var, 
                                                                 value=1)
radio_button_shrinkage_type_minnedges.pack(pady=12, padx=10)
radio_button_shrinkage_type_threshold = customtkinter.CTkRadioButton(master=radio_button_shrinkage_type_frame, 
                                                                 text="Bartz shrinkage on moving window",
                                                                 command=read_radio_button_shrinkage_type,
                                                                 variable=radio_button_shrinkage_type_var, 
                                                                 value=2)
radio_button_shrinkage_type_threshold.pack(pady=12, padx=10)

#GRAPH TYPES
radio_button_graph_type_var = customtkinter.IntVar(value=0)
def read_radio_button_graph_type():
    print("toggled graph type, current value:", radio_button_graph_type_var.get())
    if radio_button_graph_type_var.get() == 0:
        entry_n_edges.configure(state="disabled")
        entry_threshold.configure(state="disabled")
    elif radio_button_graph_type_var.get() == 1:
        entry_n_edges.configure(state="normal")
        entry_threshold.configure(state="disabled")
    elif radio_button_graph_type_var.get() == 2:
        entry_n_edges.configure(state="disabled")
        entry_threshold.configure(state="normal")

radio_button_graph_type_frame = customtkinter.CTkFrame(master=main_frame)
radio_button_graph_type_frame.pack(pady=20, padx=60, fill="both")

radio_button_graph_type_mst = customtkinter.CTkRadioButton(master=radio_button_graph_type_frame, 
                                                           text="Minnimal Spanning Tree",
                                                           command=read_radio_button_graph_type, 
                                                           variable=radio_button_graph_type_var, 
                                                           value=0)
radio_button_graph_type_mst.pack(pady=12, padx=10)
radio_button_graph_type_minnedges = customtkinter.CTkRadioButton(master=radio_button_graph_type_frame, 
                                                                 text="Minnimal N Edges graph", 
                                                                 command=read_radio_button_graph_type, 
                                                                 variable=radio_button_graph_type_var, 
                                                                 value=1)
radio_button_graph_type_minnedges.pack(pady=12, padx=10)

entry_n_edges = customtkinter.CTkEntry(master=radio_button_graph_type_frame, 
                                       placeholder_text="Number of edges")
entry_n_edges.configure(state="disabled")
entry_n_edges.pack(pady=12, padx=10)

radio_button_graph_type_threshold = customtkinter.CTkRadioButton(master=radio_button_graph_type_frame, 
                                                                 text="Threshold graph",
                                                                 command=read_radio_button_graph_type,
                                                                 variable=radio_button_graph_type_var, 
                                                                 value=2)
radio_button_graph_type_threshold.pack(pady=12, padx=10)

entry_threshold = customtkinter.CTkEntry(master=radio_button_graph_type_frame,
                                         placeholder_text="Threshold value")
entry_threshold.configure(state="disabled")
entry_threshold.pack(pady=12, padx=10)

#GRAPH REPRESENTATION
radio_button_draw_graph_circular_var = customtkinter.IntVar(value=0)
def read_graph_representation():
    print("toggled graph representation type, current value:", radio_button_draw_graph_circular_var.get())
    if radio_button_draw_graph_circular_var.get() == 0:
        settings.circular = False
    elif radio_button_draw_graph_circular_var.get() == 1:
        settings.circular = True

radio_button_draw_graph_frame = customtkinter.CTkFrame(master=main_frame)
radio_button_draw_graph_frame.pack(pady=20, padx=60, fill="both")

radio_button_draw_graph_auto = customtkinter.CTkRadioButton(master=radio_button_draw_graph_frame, 
                                                            text="Automatic graph representation",
                                                            command=read_graph_representation, 
                                                            variable=radio_button_draw_graph_circular_var, 
                                                            value=0)
radio_button_draw_graph_auto.pack(pady=12, padx=10)

radio_button_draw_graph_circular = customtkinter.CTkRadioButton(master=radio_button_draw_graph_frame, 
                                                                text="Circular graph representation",
                                                                command=read_graph_representation, 
                                                                variable=radio_button_draw_graph_circular_var, 
                                                                value=1)
radio_button_draw_graph_circular.pack(pady=12, padx=10)

#PICK COLUMN
option_type_var = customtkinter.StringVar(value="Close")
def read_option_menu(choice):
    print("option menu dropdown clicked:", choice)

option_menu = customtkinter.CTkOptionMenu(master=radio_button_draw_graph_frame,
                                          values=["Close", "Open", "High", "Low"],
                                          command=read_option_menu,
                                          variable=option_type_var)
option_menu.pack(pady=12, padx=10)
option_menu.set("Close")

#CREATE DRAWING
def create_plot():
    if check_box_draw_all_stats_var.get() == "on":
        settings.all_stats_together = True
    else:
        settings.all_stats_together = False

    if radio_button_draw_type_var.get() == 0 or radio_button_draw_type_var.get() == 1:
        settings.window_start = int(entry_window_start.get())
        settings.window_end = int(entry_window_end.get())
        settings.act_single_window = True
        settings.all_stats_together = False
    elif radio_button_draw_type_var.get() == 2:
        settings.window_size = int(entry_window_size.get())
        settings.step_size = int(entry_window_step_size.get())
        settings.act_single_window = False
        
    if radio_button_graph_type_var.get() == 1:
        settings.minimal_edges = int(entry_n_edges.get())
    elif radio_button_graph_type_var.get() == 2:
        settings.threshold = float(entry_threshold.get())

    commands.draw(draw_type=radio_button_draw_type_var.get(),
                  graph_type=radio_button_graph_type_var.get(),
                  shrinkage_type=radio_button_shrinkage_type_var.get(),
                  colummn_picked=option_type_var.get(),
                  path=dir_path.get())

create_button = customtkinter.CTkButton(master=main_frame, 
                                        text="Create plot", 
                                        command=create_plot)
create_button.pack(pady=12, padx=10)

root.mainloop()