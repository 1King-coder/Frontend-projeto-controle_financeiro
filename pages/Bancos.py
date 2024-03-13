import customtkinter as ctk
from .Page_model import PageModel
from .styles.style import *
from .styles.colors import colors
from .utils.msg_boxes import error_msg, success_msg, warning_msg

from requests import get, post, delete, put

class Bancos_Page(PageModel):

    def __init__ (self, master: 'ctk.CTk') -> None:
        super().__init__(master)

        self.master = ctk.CTkToplevel(self.master)

        self.master.geometry("1280x720")
        self.master.title("Bancos")

        self.tab_view = ctk.CTkTabview(self.master, bg_color=colors['color1'])

        self.tab_view.add('Adicionar Banco')
        self.tab_view.add('Editar Banco')
        self.tab_view.add('Excluir Banco')

        self.tab_adiciona_banco = PageModel(self.tab_view.tab('Adicionar Banco'))
        self.tab_editar_banco = PageModel(self.tab_view.tab('Editar Banco'))
        self.tab_excluir_banco = PageModel(self.tab_view.tab('Excluir Banco'))

        self.cria_widgets_tab_adiciona_banco()
        self.cria_widgets_tab_edita_banco()
        self.cria_widgets_tab_excluir_banco()

        self.tab_view.pack(expand=True, fill='both')

    def verifica_banco_existe(self, nome_direcionamento: str):
        banco = get(f"http://localhost:8000/bancos/get-id/{nome_direcionamento}").status_code

        if banco == 200:
            return True
        
        return False
    
    def adiciona_banco(self):
        nome_banco = self.nome_banco_entry.get()

        if self.verifica_banco_existe(nome_banco):
            warning_msg('Alerta', "Banco já existente")
            return
        
        adicionou = post(
            "http://localhost:8000/bancos",
            json={"nome_banco": nome_banco}
        )
        
        if adicionou.status_code == 201:
            success_msg('Sucesso', "Banco adicionado")
            return
        
        error_msg('Erro', "Erro ao adicionar banco")

    def get_dados_banco (self, nome_banco: str) -> tuple:

        response_get_id = get(f"http://localhost:8000/bancos/get-id/{nome_banco}")

        if response_get_id.status_code == 404:
            return None
        
        id_banco = response_get_id.json()['id_banco']

        res_get_saldo = get(f"http://localhost:8000/bancos/{id_banco}")
        
        saldo_banco = res_get_saldo.json()['saldo']
        
        return (id_banco, nome_banco, saldo_banco)
    
    def escreve_dados_banco (self, entry_nome: 'ctk.CTkEntry', campo_nome: 'ctk.CTkEntry', campo_saldo: 'ctk.CTkEntry') -> None:
        
        
        def escreve ():
            dados_banco = self.get_dados_banco(entry_nome.get())

            if not dados_banco:
                error_msg('Erro', 'Banco inexistente!')
                return None
            
            _, nome_banco, saldo_banco = dados_banco
            campo_nome.configure(textvariable=ctk.StringVar(value=nome_banco))
            campo_saldo.configure(textvariable=ctk.StringVar(value=saldo_banco))


        return escreve
    
    def edita_banco (self) -> None:
        nome_banco = self.nome_banco_entry_edit_comando.get()
        
        if not self.verifica_banco_existe(nome_banco):
            error_msg('Erro', 'Banco inexistente!')
            return
        
        res_get_id = get(
            f"http://localhost:8000/bancos/get-id/{nome_banco}"
        )
        
        novo_nome = self.novo_nome_banco_entry_edit_comando.get()

        if not novo_nome:
            warning_msg('Erro', 'Nenhum novo nome informado!')
            return
        
        if novo_nome == nome_banco:
            warning_msg('Erro', 'Novo nome é o mesmo que o antigo!')
            return
        
        if res_get_id.status_code == 404:
            error_msg('Erro', 'Banco inexistente!')
            return
        
        id_banco = res_get_id.json()['id_banco']

        res_edit = put(f"http://localhost:8000/bancos/{id_banco}", json={"novo_nome": novo_nome})
        if res_edit.status_code == 200:
            success_msg('Editado', 'Banco editado com sucesso!')
            return
        
        error_msg('Erro', 'Falha ao editar o nome do Banco!')

    def deleta_banco (self) -> None:
        nome_banco = self.nome_banco_entry_delet_comando.get()

        if not self.verifica_banco_existe(nome_banco):
            error_msg('Erro', 'Banco inexistente!')
            return
        
        id_banco = get(
            f"http://localhost:8000/bancos/get-id/{nome_banco}"
        ).json()['id_banco']

        res_deletou = delete(f"http://localhost:8000/bancos/{id_banco}")

        if res_deletou.status_code == 200:
            success_msg('Deletado', 'Banco deletado com sucesso!')
            return
        
        error_msg('Erro', 'Falha ao deletar o banco!')

    def cria_widgets_tab_adiciona_banco (self):
        frame = PageModel(self.tab_adiciona_banco.Frame(
            {
                **frame_style.fg_1
            },
            {
                'relx': 0.5,
                'rely': 0.3,
                'anchor': 'center'
            }
        ))
        frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Nome do Banco:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 5,
                'pady': 10,
            }
        )
        self.nome_banco_entry = frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Nome do Banco',
            },
            {
                'row': 0,
                'column': 1,
                'padx': 20,
                'pady': 10,
            }
        )
        frame.build()

        self.tab_adiciona_banco.Button(
            {
                **btn_style.medium,
                'text': 'Adicionar',
                'command': self.adiciona_banco
            },
            {
                'relx': 0.44,
                'rely': 0.5,
            }
        )

        self.tab_adiciona_banco.build()
        
    def cria_widgets_tab_edita_banco (self):
        frame_dados_banco = PageModel(self.tab_editar_banco.Frame(
            {
                **frame_style.fg_1,
            },
            {
                'relx': 0.5,
                'rely': 0.3,
                'anchor': 'center'
            }
        ))

        frame_dados_banco.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Nome',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.nome_banco_entry_edit = frame_dados_banco.Entry(
            {
                **entry_style.small,
            },
            {
                'row': 1,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )
        

        frame_dados_banco.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Saldo',
            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        self.saldo_banco_entry_edit = frame_dados_banco.Entry(
            {
                **entry_style.small,
            },
            {
                'row': 1,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )


        frame_comandos = PageModel(self.tab_editar_banco.Frame(
            {
                **frame_style.fg_1,
            },
            {
                'relx': 0.5,
                'rely': 0.45,
                'anchor': 'center'
            }
        ))

        frame_comandos.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Nome Banco:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5,
            }
        )

        self.nome_banco_entry_edit_comando = frame_comandos.Entry(
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

        frame_comandos.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Novo Nome:',
            },
            {
                'row': 0,
                'column': 2,
                'padx': 10,
                'pady': 5,
            }
        )

        self.novo_nome_banco_entry_edit_comando = frame_comandos.Entry(
            {
                **entry_style.small,

            },
            {
                'row': 0,
                'column': 3,
                'padx': 10,
                'pady': 5
            }
        )

        self.tab_editar_banco.Button(
            {
                **btn_style.medium,
                'text': 'Pesquisar',
                'command': self.escreve_dados_banco(self.nome_banco_entry_edit_comando, self.nome_banco_entry_edit, self.saldo_banco_entry_edit)
            },
            {
                'relx': 0.4,
                'rely': 0.55,
                'anchor': 'center',
            }
        )

        self.tab_editar_banco.Button(
            {
                **btn_style.medium,
                'text': 'Editar',
                'command': self.edita_banco
            },
            {
                'relx': 0.6,
                'rely': 0.55,
                'anchor': 'center',
            }
        )

        



        frame_dados_banco.build()
        frame_comandos.build()

        self.tab_editar_banco.build()

    def cria_widgets_tab_excluir_banco (self):
        frame_dados_banco = PageModel(self.tab_excluir_banco.Frame(
            {
                **frame_style.fg_1,
            },
            {
                'relx': 0.5,
                'rely': 0.3,
                'anchor': 'center'
            }
        ))

        frame_dados_banco.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Nome',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        frame_dados_banco.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Saldo',
            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )
    
        self.nome_banco_entry_delet = frame_dados_banco.Entry(
            {
                **entry_style.medium,
                
            },
            {
                'row': 1,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.saldo_banco_entry_delet = frame_dados_banco.Entry(
            {
                **entry_style.medium,
            },
            {
                'row': 1,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        frame_comandos = PageModel(self.tab_excluir_banco.Frame(
            {
                **frame_style.fg_1,
                
            },
            {
                'relx': 0.5,
                'rely': 0.45,
                'anchor': 'center'
            }
        ))

        frame_comandos.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Nome do Banco:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5,
            }
        )

        self.nome_banco_entry_delet_comando = frame_comandos.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Nome do Banco',
            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        self.tab_excluir_banco.Button(
            {
                **btn_style.medium,
                'text': 'Pesquisar',
                'command': self.escreve_dados_banco(self.nome_banco_entry_delet_comando, self.nome_banco_entry_delet, self.saldo_banco_entry_delet)
            },
            {
                'relx': 0.4,
                'rely': 0.55,
                'anchor': 'center',
            }
        )

        self.tab_excluir_banco.Button(
            {
                **btn_style.medium,
                'text': 'Excluir',
                'command': self.deleta_banco
            },
            {
                'relx': 0.6,
                'rely': 0.55,
                'anchor': 'center',
            }
        )

        frame_dados_banco.build()
        frame_comandos.build()
        self.tab_excluir_banco.build()
