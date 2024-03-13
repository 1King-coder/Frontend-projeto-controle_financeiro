from .Page_model import PageModel
import customtkinter as ctk
from .styles.style import *
from .Bancos import Bancos_Page
from .Direcionamentos import Direcionamentos_Page
from .Depositos import Depositos_Page
from .Gastos import Gastos_Page
from .Transferencias import Transferencias_Page


class HomePage(PageModel):

    def __init__ (self, master: 'ctk.CTk') -> None:
        super().__init__(master)

        self.master.title('Home')
        

        self.Button(
            {
                **btn_style.large,
                'text': 'Bancos',
                'command': lambda: self.abre_tela('bancos')
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 10,
            }
        )

        self.Button(
            {
                **btn_style.large,
                'text': 'Direcionamentos',
                'command': lambda: self.abre_tela('direcionamentos')
            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 10,
            }
        )

        self.Button(
            {
                **btn_style.large,
                'text': 'Depósitos',
                'command': lambda: self.abre_tela('depositos')
            },
            {
                'row': 1,
                'column': 0,
                'padx': 10,
                'pady': 10,
            }
        )

        self.Button(
            {
                **btn_style.large,
                'text': 'Gastos',
                'command': lambda: self.abre_tela('gastos')
            },
            {
                'row': 1,
                'column': 1,
                'padx': 10,
                'pady': 10,
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
                'rely': 0.5,
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

        


        




        


        