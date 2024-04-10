import customtkinter as ctk
from .Page_model import PageModel
from .styles.style import *
from .styles.colors import colors
from .utils.msg_boxes import error_msg, success_msg, warning_msg
from copy import deepcopy
import asyncio, aiohttp
from requests import get, post, delete, put
from datetime import datetime

async def get_dados_bancos_direcionamentos ():
    async with aiohttp.ClientSession() as session:
        tasks = [
            session.get('http://127.0.0.1:8000/bancos/', ssl=False),
            session.get('http://127.0.0.1:8000/direcionamentos/', ssl=False),
            session.get('http://127.0.0.1:8000/depositos/', ssl=False),
        ]

        responses = await asyncio.gather(*tasks)

        data = [
            await response.json() 
            for response in responses
        ]

    return data

async def get_depositos ():
        async with aiohttp.ClientSession() as session:

            response = await asyncio.gather(session.get('http://127.0.0.1:8000/depositos/', ssl=False))

            data = await response[0].json()
                
        
        return data

class Depositos_Page(PageModel):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)

        dados_direc_banco_depos = asyncio.run(get_dados_bancos_direcionamentos())

        self.lista_bancos: list = dados_direc_banco_depos[0]
        self.lista_direcionamentos: list = dados_direc_banco_depos[1]
        self.lista_depositos = dados_direc_banco_depos[2]
        self.conta_depositos = 0
        self.lista_depositos_adicionar = []

        self.bancos_por_id: dict = {
            banco['id']: banco['nome']
            for banco in self.lista_bancos
        }

        self.direcionamentos_por_id: dict = {
            direcionamento['id']: direcionamento['nome']
            for direcionamento in self.lista_direcionamentos
        }

        self.master = ctk.CTkToplevel(master=self.master)

        self.master.geometry("1280x720")
        self.master.title("Depósitos")

        self.tab_view = ctk.CTkTabview(self.master, bg_color=colors['color1'])

        self.tab_view.add('Adicionar Deposito')
        self.tab_view.add('Editar Deposito')
        self.tab_view.add('Excluir Deposito')

        self.tab_adiciona_Deposito = PageModel(self.tab_view.tab('Adicionar Deposito'))
        self.tab_editar_Deposito = PageModel(self.tab_view.tab('Editar Deposito'))
        self.tab_excluir_Deposito = PageModel(self.tab_view.tab('Excluir Deposito'))

        self.cria_widgets_tab_adiciona_Deposito()
        self.cria_widgets_tab_edita_Deposito()
        self.cria_widgets_tab_excluir_Deposito()

        self.tab_view.pack(expand=True, fill='both')

    def adiciona_lista_depositos (self, deposito: dict) -> bool:
        deposito_para_adicionar = {
            'id_banco': [
                banco['id'] 
                for banco in self.lista_bancos 
                if banco['nome'] == deposito['banco']
            ][0],
            'id_direcionamento': [
                direcionamento['id']
                for direcionamento in self.lista_direcionamentos
                if direcionamento['nome'] == deposito['direcionamento']
            ][0],
            'valor': float(deposito['valor']),
            'descricao': deposito['descricao']
        }

        self.lista_depositos_adicionar.append(deposito_para_adicionar)

    def verifica_entradas_adicionar (self) -> bool:

        if not self.verifica_entrada_banco ('add'):
            warning_msg('Erro', 'Selecione um banco!')
            return False
        
        if not self.verifica_entrada_direcionamento ('add'):
            warning_msg('Erro', 'Selecione um direcionamento!')
            return False
        
        if not self.verifica_entrada_valor ('add'):
            return False
        
        return True
    
    def verifica_entradas_editar (self) -> bool:   
        
        if not self.verifica_entrada_banco ('edit'):
            warning_msg('Erro', 'Selecione um banco!')
            return False
        
        if not self.verifica_entrada_direcionamento ('edit'):
            warning_msg('Erro', 'Selecione um direcionamento!')
            return False
        
        if not self.verifica_entrada_valor ('edit'):
            return False
        
        return True
        
    def verifica_entrada_banco (self, pag: str) -> bool:

        bancos_existentes = [
                banco['nome'] for banco in self.lista_bancos
        ]

        if pag == 'add':
            banco = self.banco_name_comboBox_add_Deposito.get()
            
            if not banco:
                return False
            
            if not banco in bancos_existentes:
                warning_msg('Erro', 'Banco inexistente!')
                return False
            
            return True
            
        if pag == 'edit':
            banco = self.banco_name_comboBox_edit_Deposito.get()
            
            if not banco:
                return False
            
            if not banco in bancos_existentes:
                warning_msg('Erro', 'Banco inexistente!')
                return False
            
            return True
        
        # Criar para página excluir
        warning_msg('Erro', 'Envie a pagina a ser verificada!')

    def verifica_entrada_direcionamento (self, pag: str) -> bool:

        if pag == 'add':
            if not self.direcionamento_name_comboBox_add_Deposito.get():
                return False
            
            return True
        
        if pag == 'edit':
            if not self.direcionamento_name_comboBox_edit_Deposito.get():
                return False
            
            return True
        
        # Criar para página excluir
        warning_msg('Erro', 'Envie a pagina a ser verificada!')

    def verifica_entrada_valor (self, pag: str) -> bool:

        if pag == 'add':
            if not self.valor_entry_add_Deposito.get():
                warning_msg('Erro', 'O valor deve ser preenchido!')
                return False
            
            try:
                
                valor_deposito = self.valor_entry_add_Deposito.get()

                float(valor_deposito)

            except Exception:
                warning_msg('Erro', 'O valor deve ser um número!')
                return False
            
            return True
        
        if pag == 'edit':
            if not self.valor_entry_edit_Deposito.get():
                warning_msg('Erro', 'O valor deve ser preenchido!')
                return False
            
            try:
                
                valor_deposito = self.valor_entry_edit_Deposito.get()

                float(valor_deposito)
                
            except Exception:
                warning_msg('Erro', 'O valor deve ser um número!')
                return False
            
            return True
        
        warning_msg('Erro', 'Envie a pagina a ser verificada!')

    def atualiza_frame_lista_depositos (self) -> None:

        if not self.verifica_entradas_adicionar():
            warning_msg('Erro', 'Campos inválidos')
            return
        
        deposito = {
            'banco': self.banco_name_comboBox_add_Deposito.get(),
            'direcionamento': self.direcionamento_name_comboBox_add_Deposito.get(),
            'valor': self.valor_entry_add_Deposito.get(),
            'descricao': self.descricao_entry_add_Deposito.get()
        }

        dep_string = (
            f"Depósito {self.conta_depositos + 1}\n" +
            f"\tBanco: {deposito['banco']}\n" +
            f"\tDirecionamento: {deposito['direcionamento']}\n" +
            f"\tValor: R$ {deposito['valor']}"
            f"\tDescrição: {deposito['descricao']}"
        )

        self.frame_lista_depositos.Label(
            {
                **lbl_style.light_rectangle_bg['large'],
                'text': dep_string,
                'justify': 'left'
            },
            {
                'row': self.conta_depositos + 1,
                'column': 0,
                'padx': 3,
                'pady': 5
            }
        )

        self.adiciona_lista_depositos(deposito)

        self.conta_depositos += 1

        self.frame_lista_depositos.build()

    def limpa_frame_lista_depositos (self):
        for widget in self.frame_lista_depositos.master.winfo_children()[1:]:
            widget.destroy()

        self.lista_depositos_adicionar = []
        self.conta_depositos = 0

        self.frame_lista_depositos.build()

    def remove_ultimo_lista_depositos (self):

        if not len(self.lista_depositos_adicionar):
            return 
        
        self.lista_depositos_adicionar.pop()
        self.frame_lista_depositos.master.winfo_children()[-1].destroy()
        self.conta_depositos -= 1

        self.frame_lista_depositos.build()

    def adiciona_Deposito (self):

        if not self.lista_depositos_adicionar:
            if not self.verifica_entrada_banco ('add'):
                warning_msg('Erro', 'Preencha os campos!')
                return
            
            self.atualiza_frame_lista_depositos()
        
        adicionou = post(
            "http://localhost:8000/depositos",
            json={'depositos': self.lista_depositos_adicionar}
        )

        if adicionou.status_code == 201:
            success_msg('Sucesso', 'Depósitos adicionado')
            self.conta_depositos = 0
            self.limpa_frame_lista_depositos()
            self.lista_depositos_adicionar = []	
            self.listar_depositos_em_frame(self.frame_lista_depositos_delete, "delete", True)
            self.listar_depositos_em_frame(self.frame_lista_depositos_edit, "edit", True)
            return
        
        error_msg('Erro', 'Erro ao adicionar depósitos')

    def cria_widgets_tab_adiciona_Deposito(self):
        main_frame = PageModel(self.tab_adiciona_Deposito.Frame(
            {
                **frame_style.fg_1
            },
            {
                'relx': 0.35,
                'rely': 0.3,
                'anchor': 'center'
            }
        ))

        self.frame_lista_depositos = PageModel(self.tab_adiciona_Deposito.ScrollableFrame(
            {
                **frame_style.fg_1,
                'width': 300,
                'height': 500
            },
            {
                'relx': 0.78,
                'rely': 0.5,
                'anchor': 'center'
            }
        ))

        self.frame_lista_depositos.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Depósitos a serem Adicionados',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 15,
                'pady': 10
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Banco:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.banco_name_comboBox_add_Deposito = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values': [""] + [banco['nome'] for banco in self.lista_bancos],
            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Direcionamento:',
            },
            {
                'row': 1,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.direcionamento_name_comboBox_add_Deposito = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values':[""] + [direcionamento['nome'] for direcionamento in self.lista_direcionamentos],
            },
            {
                'row': 1,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Valor:',
            },
            {
                'row': 0,
                'column': 2,
                'padx': 10,
                'pady': 5
            }
        )

        self.valor_entry_add_Deposito = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Valor',
            },
            {
                'row': 0,
                'column': 3,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Descrição:',
            },
            {
                'row': 1,
                'column': 2,
                'padx': 10,
                'pady': 5
            }
        )

        self.descricao_entry_add_Deposito = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Descrição',
            },
            {
                'row': 1,
                'column': 3,
                'padx': 10,
                'pady': 5
            }
        )

        self.tab_adiciona_Deposito.Button(
            {
                **btn_style.medium,
                'text': 'Adicionar outro depósito',
                'command': self.atualiza_frame_lista_depositos
            },
            {
                'relx': 0.18,
                'rely': 0.45,
                'anchor': 'center'
            }
        )

        self.tab_adiciona_Deposito.Button(
            {
                **btn_style.medium,
                'text': 'Remove último depósito',
                'command': self.remove_ultimo_lista_depositos
            },
            {
                'relx': 0.37,
                'rely': 0.45,
                'anchor': 'center'
            }
        )

        self.tab_adiciona_Deposito.Button(
            {
                **btn_style.medium,
                'text': 'Limpar depósitos',
                'command': self.limpa_frame_lista_depositos
            },
            {
                'relx': 0.54,
                'rely': 0.45,
                'anchor': 'center'
            }
        )

        self.tab_adiciona_Deposito.Button(
            {
                **btn_style.large,
                'text': 'Enviar depósitos',
                'command': self.adiciona_Deposito
            },
            {
                'relx': 0.35,
                'rely': 0.57,
                'anchor': 'center'
            }
        )

        main_frame.build()
        self.frame_lista_depositos.build()
        self.tab_adiciona_Deposito.build()
        
    def listar_depositos_em_frame (self, frame, page, updating: bool= False):

        depositos = self.lista_depositos

        if updating:
            depositos = asyncio.run(get_depositos())

        actual_month = datetime.now().month
        start_of_the_month = datetime.strptime(f'01/{actual_month}/{datetime.now().year}', '%d/%m/%Y')
        end_of_the_month = datetime.strptime(f'01/{actual_month + 1 if actual_month != 12 else 1}/{datetime.now().year}', '%d/%m/%Y')

        for wid in frame.master.winfo_children()[1:]:
            wid.destroy()

        for i, deposito in enumerate(depositos):
            if start_of_the_month <= datetime.strptime(deposito['created_at'], '%d/%m/%Y') < end_of_the_month:
            
                frame_deposito = PageModel(frame.Frame(
                    {
                        **frame_style.fg_2,
                    },
                    {
                        'row': i + 1,
                        'column': 0,
                        'padx': 5,
                        'pady': 5
                    }
                ))

                
                frame_deposito.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': deposito['id'],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 0,
                    }
                )
                frame_deposito.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': self.bancos_por_id[deposito['id_banco']],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 1,
                    }
                )
                frame_deposito.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': self.direcionamentos_por_id[deposito['id_direcionamento']],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 2,
                    }
                )
                frame_deposito.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': deposito['valor'],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 3,
                    }
                )
                frame_deposito.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': deposito['descricao'],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 4,
                    }
                )

                for lbl in frame_deposito.master.winfo_children():
                    lbl.configure(
                        fg_color='transparent'
                    )

                    lbl.bind(
                        '<Button-1>',
                        lambda event: self.get_dados_deposito(page, event.widget.master.master)
                    )

                    lbl.bind(
                        '<Enter>',
                        lambda event: (
                            event.widget.master.master.configure(fg_color=frame_style.fg_3['fg_color'])
                        )
                    )

                    lbl.bind(
                        '<Leave>',
                        lambda event: (
                            event.widget.master.master.configure(fg_color=frame_style.fg_2['fg_color'])
                        )
                    )
            
                frame_deposito.build()

        frame.build()
    def cria_headers_depositos (self, frame):
        frame.Label(
            {
                **lbl_style.dark_rectangle_bg['medium'],
                'text': 'id',
                'width': 100,
                'height': 20,
                'justify': 'center',
            },
            {
                'row': 0,
                'column': 0,
            }
        )
        frame.Label(
            {
                **lbl_style.dark_rectangle_bg['medium'],
                'text': 'Banco',
                'width': 100,
                'height': 20,
                'justify': 'center',
            },
            {
                'row': 0,
                'column': 1,
                
            }
        )

        frame.Label(
            {
                **lbl_style.dark_rectangle_bg['medium'],
                'text': 'Direcionamento',
                'width': 100,
                'height': 20,
                'justify': 'center',
            },
            {
                'row': 0,
                'column': 2,
                
            }
        )

        frame.Label(
            {
                **lbl_style.dark_rectangle_bg['medium'],
                'text': 'Valor',
                'width': 100,
                'height': 20,
                'justify': 'center',
            },
            {
                'row': 0,
                'column': 3,
                
            }
        )

        frame.Label(
            {
                **lbl_style.dark_rectangle_bg['medium'],
                'text': 'descricao',
                'width': 100,
                'height': 40,
                'justify': 'center',
            },
            {
                'row': 0,
                'column': 4,
                
            }
        )

        frame.build()

    def escreve_dados_deposito_selecionado (self, page:str, deposito: list):

        deposito = {
            'id': deposito[0],
            'banco': deposito[1],
            'direcionamento': deposito[2],
            'valor': deposito[3],
            'descricao': deposito[4],
        }


        if page == 'edit':
            self.banco_id_entry_edit_Deposito.configure(
                textvariable = ctk.StringVar(value=deposito['id'])
            )
            self.banco_name_comboBox_edit_Deposito.configure(
                variable = ctk.StringVar(value=deposito['banco'])
            )

            self.direcionamento_name_comboBox_edit_Deposito.configure(
                variable = ctk.StringVar(value=deposito['direcionamento'])
            )
            self.valor_entry_edit_Deposito.configure(
                textvariable = ctk.StringVar(value=deposito['valor'])
            )

            self.descricao_entry_edit_Deposito.configure(
                textvariable = ctk.StringVar(value=deposito['descricao'])
            )

            return

        self.banco_id_entry_delete_Deposito.configure(
            textvariable = ctk.StringVar(value=deposito['id'])
        )
        self.banco_name_comboBox_delete_Deposito.configure(
            variable = ctk.StringVar(value=deposito['banco'])
        )

        self.direcionamento_name_comboBox_delete_Deposito.configure(
            variable = ctk.StringVar(value=deposito['direcionamento'])
        )
        self.valor_entry_delete_Deposito.configure(
            textvariable = ctk.StringVar(value=deposito['valor'])
        )

        self.descricao_entry_delete_Deposito.configure(
            textvariable = ctk.StringVar(value=deposito['descricao'])
        )

    def get_dados_deposito (self, page, deposito):

        dados_deposito = [
            dado.cget('text') for dado in deposito.winfo_children()
        ]
        
        self.escreve_dados_deposito_selecionado(page, dados_deposito)
        
    def edita_deposito (self):
        id_deposito = self.banco_id_entry_edit_Deposito.get()

        novo_id_banco = [
            key
            for key, nome in self.bancos_por_id.items()
            if nome == self.banco_name_comboBox_edit_Deposito.get()
        ][0]

        novo_id_direcionamento = [
            key
            for key, nome in self.direcionamentos_por_id.items()
            if nome == self.direcionamento_name_comboBox_edit_Deposito.get()
        ][0]

        novo_deposito = {
            'novo_id_banco': novo_id_banco,
            'novo_id_direcionamento': novo_id_direcionamento,
            'novo_valor': float(self.valor_entry_edit_Deposito.get()),
            'nova_descricao': self.descricao_entry_edit_Deposito.get(),
        }

        res = put(
            f'http://localhost:8000/depositos/{id_deposito}',
            json=novo_deposito
        )

        if res.status_code == 500:
            error_msg('Erro', 'Erro ao editar depósitos')
            return
        
        if res.status_code == 404:
            error_msg('Erro', 'Depósitos inexistente!')
            return
        
        self.listar_depositos_em_frame(self.frame_lista_depositos_edit, "edit", True)
        
        success_msg('Editado', 'Depósitos editado com sucesso!')

    def deleta_deposito (self):
        id_deposito = self.banco_id_entry_delete_Deposito.get()

        res = delete(
            f'http://localhost:8000/depositos/{id_deposito}'
        )

        if res.status_code == 500:
            error_msg('Erro', 'Erro ao deletar depósitos')
            return

        if res.status_code == 404:
            error_msg('Erro', 'Depósitos inexistente!')
            return
        
        self.listar_depositos_em_frame(self.frame_lista_depositos_delete, "delete", True)

        success_msg('Deletado', 'Depósitos deletado com sucesso!')

    def cria_widgets_tab_edita_Deposito(self):
        main_frame = PageModel(self.tab_editar_Deposito.Frame(
            {
                **frame_style.fg_1
            },
            {
                'relx': 0.32,
                'rely': 0.3,
                'anchor': 'center'
            }
        ))

        self.frame_lista_depositos_edit = PageModel(
            self.tab_editar_Deposito.ScrollableFrame(
                {
                    **frame_style.fg_1,
                    'width': 550,
                    'height': 600
                },
                {
                    'relx': 0.73,
                    'rely': 0.5,
                    'anchor': 'center'
                }
            )
        )

        frame_lista_depositos_edit_headers = PageModel(
            self.frame_lista_depositos_edit.Frame(
                {
                    **frame_style.fg_1
                },
                {
                    'row': 0,
                    'column': 0,
                    'padx': 5,
                    'pady': 5
                }
            )
        )

        self.cria_headers_depositos(frame_lista_depositos_edit_headers)

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'id:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.banco_id_entry_edit_Deposito = main_frame.Entry(
            {
                **entry_style.small,

            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Banco:',
            },
            {
                'row': 1,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.banco_name_comboBox_edit_Deposito = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values': [""] + [banco['nome'] for banco in self.lista_bancos],
            },
            {
                'row': 1,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Direcionamento:',
            },
            {
                'row': 2,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.direcionamento_name_comboBox_edit_Deposito = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values':[""] + [direcionamento['nome'] for direcionamento in self.lista_direcionamentos],
            },
            {
                'row': 2,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Valor:',
            },
            {
                'row': 3,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.valor_entry_edit_Deposito = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Valor',
            },
            {
                'row': 3,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Descrição:',
            },
            {
                'row': 4,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.descricao_entry_edit_Deposito = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Descrição',
            },
            {
                'row': 4,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        self.tab_editar_Deposito.Button(
            {
                **btn_style.large,
                'text': 'Editar',
                'command': self.edita_deposito
            },
            {
                'relx': 0.23,
                'rely': 0.6,
                'anchor': 'center'
            }
        )

        self.tab_editar_Deposito.Button(
            {
                **btn_style.large,
                'text': 'Atualizar',
                'command': lambda:self.listar_depositos_em_frame(self.frame_lista_depositos_edit, 'edit', True)
            },
            {
                'relx': 0.4,
                'rely': 0.6,
                'anchor': 'center'
            }
        )

        main_frame.build()
        self.frame_lista_depositos_edit.build()
        self.listar_depositos_em_frame(self.frame_lista_depositos_edit, 'edit')
        self.tab_editar_Deposito.build()

    def cria_widgets_tab_excluir_Deposito(self):
        main_frame = PageModel(self.tab_excluir_Deposito.Frame(
            {
                **frame_style.fg_1
            },
            {
                'relx': 0.32,
                'rely': 0.3,
                'anchor': 'center'
            }
        ))

        self.frame_lista_depositos_delete = PageModel(
            self.tab_excluir_Deposito.ScrollableFrame(
                {
                    **frame_style.fg_1,
                    'width': 550,
                    'height': 600
                },
                {
                    'relx': 0.73,
                    'rely': 0.5,
                    'anchor': 'center'
                }
            )
        )

        frame_lista_depositos_delete_headers = PageModel(
            self.frame_lista_depositos_delete.Frame(
                {
                    **frame_style.fg_1
                },
                {
                    'row': 0,
                    'column': 0,
                    'padx': 5,
                    'pady': 5
                }
            )
        )

        self.cria_headers_depositos(frame_lista_depositos_delete_headers)

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'id:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.banco_id_entry_delete_Deposito = main_frame.Entry(
            {
                **entry_style.small,

            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Banco:',
            },
            {
                'row': 1,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.banco_name_comboBox_delete_Deposito = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values': [""] + [banco['nome'] for banco in self.lista_bancos],
            },
            {
                'row': 1,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Direcionamento:',
            },
            {
                'row': 2,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.direcionamento_name_comboBox_delete_Deposito = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values':[""] + [direcionamento['nome'] for direcionamento in self.lista_direcionamentos],
            },
            {
                'row': 2,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Valor:',
            },
            {
                'row': 3,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.valor_entry_delete_Deposito = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Valor',
            },
            {
                'row': 3,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Descrição:',
            },
            {
                'row': 4,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.descricao_entry_delete_Deposito = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Descrição',
            },
            {
                'row': 4,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        self.tab_excluir_Deposito.Button(
            {
                **btn_style.large,
                'text': 'delete',
                'command': self.deleta_deposito
            },
            {
                'relx': 0.23,
                'rely': 0.6,
                'anchor': 'center'
            }
        )

        self.tab_excluir_Deposito.Button(
            {
                **btn_style.large,
                'text': 'Atualizar',
                'command': lambda:self.listar_depositos_em_frame(self.frame_lista_depositos_delete, 'delete', True)
            },
            {
                'relx': 0.4,
                'rely': 0.6,
                'anchor': 'center'
            }
        )

        main_frame.build()
        self.frame_lista_depositos_delete.build()
        self.listar_depositos_em_frame(self.frame_lista_depositos_delete, 'delete')
        self.tab_excluir_Deposito.build()