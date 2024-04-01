import customtkinter as ctk
from pages.styles.colors import colors
from pages.Home import HomePage
import pyautogui as pg
from time import sleep

def init_api ():
    pg.keyDown('win')
    pg.press('r')
    pg.keyUp('win')

    pg.write('cmd')
    pg.press('enter')
    sleep(0.5)
    pg.write('g:')
    pg.press('enter')
    pg.write('cd Meu Drive\\Controle Financeiro\\backend')
    pg.press('enter')
    pg.write('backendEnv\\Scripts\\activate')
    pg.press('enter')
    pg.write('uvicorn main:app')
    pg.press('enter')


# init_api()

app = ctk.CTk(fg_color=colors['color1'])

app.geometry("450x500")

page_test = HomePage(app)   

page_test.build()

app.mainloop()


