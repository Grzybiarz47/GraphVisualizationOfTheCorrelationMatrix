import customtkinter
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


root = customtkinter.CTk()
root.title("Graph visualization of the correlation matrix")
root.geometry("500x300")

def graph():
    house_prices = np.random.normal(200000, 25000, 5000)
    plt.hist(house_prices, 50)
    plt.show()

my_button = customtkinter.CTkButton(root, text="Try", command=graph)
my_button.pack()

root.mainloop()