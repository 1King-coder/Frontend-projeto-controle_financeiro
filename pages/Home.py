from .Page_model import PageModel
import customtkinter as ctk
from .styles.style import *
from .Bancos import Bancos_Page
from .Direcionamentos import Direcionamentos_Page
from .Depositos import Depositos_Page
from .Gastos import Gastos_Page
from .Transferencias import Transferencias_Page
import pyautogui as pg
from pathlib import Path
from time import sleep
from requests import patch
from .utils.config import HOST_URL


DASHBOARD_NAME = 'Dashboard Controle Financeiro.pbix'


class HomePage(PageModel):

    def __init__ (self, master: 'ctk.CTk') -> None:
        super().__init__(master)

        # Atualiza controle de parcelas pagas
        try:
            sleep(2)
            patch(f"{HOST_URL}/gastos_periodizados")

        except Exception as e:
            print(e)
            return

        self.master.title('Home')

        self.Button(
            {
                **btn_style.large,
                'text': 'Dashboard',
                'command': self.abre_dashboard
            },
            {
                'relx': 0.5,
                'rely': 0.15,
                'anchor': 'center'
            }
        )
        

        self.Button(
            {
                **btn_style.large,
                'text': 'Bancos',
                'command': lambda: self.abre_tela('bancos')
            },
            {
                'relx': 0.25,
                'rely': 0.35,
                'anchor': 'center'
            }
        )

        self.Button(
            {
                **btn_style.large,
                'text': 'Direcionamentos',
                'command': lambda: self.abre_tela('direcionamentos')
            },
            {
                'relx': 0.75,
                'rely': 0.35,
                'anchor': 'center'
            }
        )

        self.Button(
            {
                **btn_style.large,
                'text': 'Depósitos',
                'command': lambda: self.abre_tela('depositos')
            },
            {
                'relx': 0.25,
                'rely': 0.55,
                'anchor': 'center'
            }
        )

        self.Button(
            {
                **btn_style.large,
                'text': 'Gastos',
                'command': lambda: self.abre_tela('gastos')
            },
            {
                'relx': 0.75,
                'rely': 0.55,
                'anchor': 'center'
            }
        )

        self.Button(
            {
                **btn_style.large,
                'text': 'Transferências',
                'command': lambda: self.abre_tela('transferencias')
            },
            {
                'relx': 0.5,
                'rely': 0.75,
                'anchor': 'center'
            }
        )

    def abre_tela (self, nome_tela: str):


        telas = {
            'bancos': Bancos_Page,
            'direcionamentos': Direcionamentos_Page,
            'depositos': Depositos_Page,
            'gastos': Gastos_Page,
            'transferencias': Transferencias_Page
        }

        telas[nome_tela](self.master)

    def abre_dashboard (self):
        local_path = Path(__file__).parent.parent.parent

        pg.keyDown('win')
        pg.press('r')
        pg.keyUp('win')
        pg.write('explorer')
        pg.press('enter')
        for _ in range(6):
            sleep(0.2)
            pg.press('tab')
        
        pg.write(str(local_path))
        pg.press('enter')
        pg.press('down')
        pg.press('down')
        pg.press('enter')



        


        




        


        