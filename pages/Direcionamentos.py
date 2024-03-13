import customtkinter as ctk
from .Page_model import PageModel
from .styles.style import *
from .styles.colors import colors
from .utils.msg_boxes import error_msg, success_msg, warning_msg

from requests import get, post, delete, put


class Direcionamentos_Page(PageModel):
    def __init__ (self, master: 'ctk.CTk') -> None:
        super().__init__(master)

        self.master = ctk.CTkToplevel(self.master)

        self.master.geometry("1280x720")
        self.master.title("Bancos")

        self.tab_view = ctk.CTkTabview(self.master, width=400, height=300, bg_color=colors['color1'])

        self.tab_view.add('Adicionar Direcionamento')
        self.tab_view.add('Editar Direcionamento')
        self.tab_view.add('Excluir Direcionamento')


        self.tab_adiciona_direcionamento = PageModel(self.tab_view.tab('Adicionar Direcionamento'))
        self.tab_editar_direcionamento = PageModel(self.tab_view.tab('Editar Direcionamento'))
        self.tab_excluir_direcionamento = PageModel(self.tab_view.tab('Excluir Direcionamento'))

        self.cria_widgets_tab_adiciona_direcionamento()
        self.cria_widgets_tab_editar_direcionamento()
        self.cria_widgets_tab_excluir_direcionamento()

        self.tab_view.pack(expand=True, fill='both')

    def verifica_direcionamento_existe(self, nome_direcionamento: str):
        direc = get(f"http://localhost:8000/direcionamentos/get-id/{nome_direcionamento}").status_code

        if direc == 200:
            return True
        
        return False
    
    def adiciona_direcionamento(self):
        nome_direcionamento = self.nome_direcionamento_entry.get()

        if self.verifica_direcionamento_existe(nome_direcionamento):
            warning_msg('Alerta', "Direcionamento ja existe")
            return
        
        adicionou = post(
            "http://localhost:8000/direcionamentos",
            json={"nome_direcionamento": nome_direcionamento}
        )
        
        if adicionou.status_code == 201:
            success_msg('Sucesso', "Direcionamento adicionado")
            return
        
        error_msg('Erro', "Erro ao adicionar direcionamento")

    def get_dados_direcionamento (self, nome_direcionamento: str) -> tuple:

        response_get_id = get(f"http://localhost:8000/direcionamentos/get-id/{nome_direcionamento}")

        if response_get_id.status_code == 404:
            return None

        id_direcionamento = response_get_id.json()['id_direcionamento']
        
        res_get_saldo = get(f"http://localhost:8000/direcionamentos/{id_direcionamento}")
        
        saldo_direcionamento = res_get_saldo.json()['saldo']
        
        return (id_direcionamento, nome_direcionamento, saldo_direcionamento)
    
    def escreve_dados_direcionamento (self, entry_nome: 'ctk.CTkEntry', campo_nome: 'ctk.CTkEntry', campo_saldo: 'ctk.CTkEntry') -> None:
        
        
        def escreve ():
            dados_banco = self.get_dados_direcionamento(entry_nome.get())

            if not dados_banco:
                error_msg('Erro', 'Direcionamento inexistente!')
                return None
            
            _, nome_direcionamento, saldo_direcionamento = dados_banco
            campo_nome.configure(textvariable=ctk.StringVar(value=nome_direcionamento))
            campo_saldo.configure(textvariable=ctk.StringVar(value=saldo_direcionamento))


        return escreve
    
    def edita_direcionamento (self) -> None:
        nome_direcionamento = self.nome_direcionamento_entry_edit_comando.get()
        
        if not self.verifica_direcionamento_existe(nome_direcionamento):
            error_msg('Erro', 'Direcionamento inexistente!')
            return

        res_get_id = get(
            f"http://localhost:8000/direcionamentos/get-id/{nome_direcionamento}"
        )
        
        novo_nome = self.novo_nome_direcionamento_entry_edit_comando.get()

        if not novo_nome:
            warning_msg('Erro', 'Nenhum novo nome informado!')
            return
        
        if novo_nome == nome_direcionamento:
            warning_msg('Erro', 'Novo nome é o mesmo que o antigo!')
            return
        
        if res_get_id.status_code == 404:
            error_msg('Erro', 'Direcionamento inexistente!')
            return
        
        id_direcionamento = res_get_id.json()['id_direcionamento']

        res_edit = put(f"http://localhost:8000/direcionamentos/{id_direcionamento}", json={"novo_nome": novo_nome})
        if res_edit == 200:
            success_msg('Editado', 'Direcionamento editado com sucesso!')
            return
        
        error_msg('Erro', 'Falha ao editar o nome do Direcionamento!')

    def deleta_direcionamento (self) -> None:
        nome_direcionamento = self.nome_direcionamento_entry_delet_comando.get()

        if not self.verifica_direcionamento_existe(nome_direcionamento):
            error_msg('Erro', 'Direcionamento inexistente!')
            return
        
        id_direcionamento = get(
            f"http://localhost:8000/direcionamentos/get-id/{nome_direcionamento}"
        ).json()['id_direcionamento']

        res_deletou = delete(f"http://localhost:8000/direcionamentos/{id_direcionamento}")

        if res_deletou.status_code == 200:
            success_msg('Deletado', 'Direcionamento deletado com sucesso!')
            return
        
        error_msg('Erro', 'Falha ao deletar o direcionamento!')


    def cria_widgets_tab_adiciona_direcionamento(self):
        frame = PageModel(self.tab_adiciona_direcionamento.Frame(
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
                'text': 'Nome do Direcionamento:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 5,
                'pady': 10,
            }
        )
        self.nome_direcionamento_entry = frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Nome do Direcionamento',
            },
            {
                'row': 0,
                'column': 1,
                'padx': 20,
                'pady': 10,
            }
        )
        frame.build()

        self.tab_adiciona_direcionamento.Button(
            {
                **btn_style.medium,
                'text': 'Adicionar',
                'command': self.adiciona_direcionamento
            },
            {
                'relx': 0.44,
                'rely': 0.5,
            }
        )

        self.tab_adiciona_direcionamento.build()

    def cria_widgets_tab_editar_direcionamento(self):
        frame_dados_direcionamento = PageModel(self.tab_editar_direcionamento.Frame(
            {
                **frame_style.fg_1

            },
            {
                'relx': 0.5,
                'rely': 0.3,
                'anchor': 'center'
            }
        ))

        frame_dados_direcionamento.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Nome',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5,
            }
        )

        self.nome_direcionamento_entry_edit_dados = frame_dados_direcionamento.Entry(
            {
                **entry_style.small,
            },
            {
                'row': 1,
                'column': 0,
                'padx': 10,
                'pady': 5,
            }
        )

        frame_dados_direcionamento.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Saldo',
            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 5,
            }
        )

        self.saldo_direcionamento_entry_edit_dados = frame_dados_direcionamento.Entry(
            {
                **entry_style.small,
            },
            {
                'row': 1,
                'column': 1,
                'padx': 10,
                'pady': 5,
            }
        )

        frame_dados_direcionamento.build()

        frame_comandos = PageModel(self.tab_editar_direcionamento.Frame(
            {
                **frame_style.fg_1
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
                'text': 'Nome do direcionamento:'
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5,
            }
        )

        self.nome_direcionamento_entry_edit_comando = frame_comandos.Entry(
            {
                **entry_style.medium,
            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 5,
            }
        )

        frame_comandos.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Novo Nome:'
            },
            {
                'row': 0,
                'column': 2,
                'padx': 10,
                'pady': 5,
            }
        )

        self.novo_nome_direcionamento_entry_edit_comando = frame_comandos.Entry(
            {
                **entry_style.medium,
            },
            {
                'row': 0,
                'column': 3,
                'padx': 10,
                'pady': 5,
            }
        )

        self.tab_editar_direcionamento.Button(
            {
                **btn_style.medium,
                'text': 'Pesquisar',
                'command': self.escreve_dados_direcionamento(self.nome_direcionamento_entry_edit_comando, self.nome_direcionamento_entry_edit_dados, self.saldo_direcionamento_entry_edit_dados)
            },
            {
                'relx': 0.4,
                'rely': 0.55,
                'anchor': 'center'
            }
        )

        self.tab_editar_direcionamento.Button(
            {
                **btn_style.medium,
                'text': 'Editar',
                'command': self.edita_direcionamento
            },
            {
                'relx': 0.6,
                'rely': 0.55,
                'anchor': 'center'
            }
        )

        frame_comandos.build()

        self.tab_editar_direcionamento.build()

    def cria_widgets_tab_excluir_direcionamento(self):
        frame_dados_direcionamento = PageModel(self.tab_excluir_direcionamento.Frame(
            {
                **frame_style.fg_1,
            },
            {
                'relx': 0.5,
                'rely': 0.3,
                'anchor': 'center'
            }
        ))

        frame_dados_direcionamento.Label(
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

        frame_dados_direcionamento.Label(
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
    
        self.nome_direcionamento_entry_delet = frame_dados_direcionamento.Entry(
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

        self.saldo_direcionamento_entry_delet = frame_dados_direcionamento.Entry(
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

        frame_comandos = PageModel(self.tab_excluir_direcionamento.Frame(
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
                'text': 'Nome do Direcionamento:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 10,
                'pady': 5,
            }
        )

        self.nome_direcionamento_entry_delet_comando = frame_comandos.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Nome do Direcionamento',
            },
            {
                'row': 0,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )

        self.tab_excluir_direcionamento.Button(
            {
                **btn_style.medium,
                'text': 'Pesquisar',
                'command': self.escreve_dados_direcionamento(self.nome_direcionamento_entry_delet_comando, self.nome_direcionamento_entry_delet, self.saldo_direcionamento_entry_delet)
            },
            {
                'relx': 0.4,
                'rely': 0.55,
                'anchor': 'center',
            }
        )

        self.tab_excluir_direcionamento.Button(
            {
                **btn_style.medium,
                'text': 'Excluir',
                'command': self.deleta_direcionamento
            },
            {
                'relx': 0.6,
                'rely': 0.55,
                'anchor': 'center',
            }
        )

        frame_dados_direcionamento.build()
        frame_comandos.build()
        self.tab_excluir_direcionamento.build( )  
