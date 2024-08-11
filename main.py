import customtkinter as ctk
from pages.styles.colors import colors
from pages.Home import HomePage
import pyautogui as pg
from time import sleep



app = ctk.CTk(fg_color=colors['color1'])

app.geometry("450x500")

page_test = HomePage(app)   

page_test.build()

app.mainloop()


