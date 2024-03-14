import customtkinter as ctk
from .Page_model import PageModel
from .styles.style import *
from .styles.colors import colors
from .utils.msg_boxes import error_msg, success_msg, warning_msg
from requests import get, post, delete, put
from datetime import datetime

class Transferencias_Page(PageModel):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)

        self.lista_bancos: list = get('http://127.0.0.1:8000/bancos/').json()
        self.lista_direcionamentos: list = get('http://127.0.0.1:8000/direcionamentos/').json()
 
        self.bancos_por_id: dict = {
            banco['id']: banco['nome']
            for banco in self.lista_bancos
        }

        self.id_por_banco: dict = {
            banco['nome']: banco['id']
            for banco in self.lista_bancos
        }
        

        self.direcionamentos_por_id: dict = {
            direcionamento['id']: direcionamento['nome']
            for direcionamento in self.lista_direcionamentos
        }

        self.id_por_direcionamento: dict = {
            direcionamento['nome']: direcionamento['id']
            for direcionamento in self.lista_direcionamentos
        }

        self.master = ctk.CTkToplevel(master=self.master)

        self.master.geometry("1280x720")
        self.master.title("Transferências")

        self.tab_view = ctk.CTkTabview(self.master, bg_color=colors['color1'])

        self.tab_view.add('Adicionar Transferência')
        self.tab_view.add('Editar Transferência')
        self.tab_view.add('Excluir Transferência')

        self.tab_adiciona_Transferencias = PageModel(self.tab_view.tab('Adicionar Transferência'))
        self.tab_editar_Transferencia = PageModel(self.tab_view.tab('Editar Transferência'))
        self.tab_excluir_Transferencia = PageModel(self.tab_view.tab('Excluir Transferência'))

        self.cria_widgets_tab_adiciona_Transferencias()
        self.cria_widgets_tab_edita_Transferencia()
        self.cria_widgets_tab_excluir_Transferencia()

        self.tab_view.pack(expand=True, fill='both')

    
    def verifica_entradas (self, page: str) -> bool:

        if not self.verifica_entradas_transferencia (page):
            return False
        
        if not self.verifica_entrada_valor (page):
            return False
        
        return True
            
    def verifica_entradas_transferencia (self, pag: str) -> bool:

        bancos_existentes = [
            banco['nome'] for banco in self.lista_bancos
        ]

        direcionamentos_existentes = [
            direcionamento['nome'] for direcionamento in self.lista_direcionamentos
        ]

        tipo = 'banco' if not self.tipo_tranferencia_add_switch.get() else 'direcionamento'
        local = 'banco' if self.tipo_tranferencia_add_switch.get() else 'direcionamento'

        origem = self.__getattribute__(f'origem_name_comboBox_{pag}_Transferencia').get()
        destino = self.__getattribute__(f'destino_name_comboBox_{pag}_Transferencia').get()
        local_transf = self.__getattribute__(f'local_tranf_name_comboBox_{pag}_Transferencia').get()

        if not origem:
            warning_msg('Erro', f'Selecione um {tipo} de origem!')
            return False
        
        if not destino:
            warning_msg('Erro', f'Selecione um {tipo} de destino!')
            return False
        
        if not local_transf:
            warning_msg('Erro', f'Selecione um {local} direcionamento!')
            return False
        
            
        if not (origem in bancos_existentes) and not (origem in direcionamentos_existentes):
            warning_msg('Erro', f'{tipo} de origem inexistente!')
            return False
        
        if not (destino in bancos_existentes) and not (destino in direcionamentos_existentes):
            warning_msg('Erro', f'{tipo} de destino inexistente!')
            return False
        
        if not (local_transf in direcionamentos_existentes) and not (local_transf in bancos_existentes):
            warning_msg('Erro', f'{local} inexistente!')
            return False
        
        if origem == destino:
            warning_msg('Erro', 'Origem e Destino devem ser diferentes!')
            return False
        
        return True
        
    def verifica_entrada_valor (self, pag: str) -> bool:

        valor_tranferencia = self.__getattribute__(f'valor_entry_{pag}_Transferencia').get()
                
        if not valor_tranferencia:
                warning_msg('Erro', 'O valor deve ser preenchido!')
                return False
            
        try:
            
            float(valor_tranferencia)

        except Exception:
            warning_msg('Erro', 'O valor deve ser um número!')
            return False
        
        return True

    def controla_switch (self, page: str):

        lbl_tiulo = self.__getattribute__(f'label_titulo_{page}')
        lbl_origem = self.__getattribute__(f'label_origem_{page}')
        lbl_destino = self.__getattribute__(f'label_destino_{page}')
        lbl_local_transf = self.__getattribute__(f'label_local_tranf_{page}')
        switch = self.__getattribute__(f'tipo_tranferencia_{page}_switch')
        cbox_origem = self.__getattribute__(f'origem_name_comboBox_{page}_Transferencia')
        cbox_destino = self.__getattribute__(f'destino_name_comboBox_{page}_Transferencia')
        cbox_local_transf = self.__getattribute__(f'local_tranf_name_comboBox_{page}_Transferencia')

        tipo_tranferencia = 'Transferência entre \nBancos' if not switch.get() else 'Transferência entre \nDirecionamentos'

        if page == 'edit' or page == 'delete':
            self.listar_transferencias_em_frame(page)

        lbl_tiulo.configure(text=tipo_tranferencia)

        if not switch.get():
            lbl_origem.configure(text='Banco \nde origem:')

            cbox_origem.configure(
                values= [
                    banco['nome'] for banco in self.lista_bancos
                ]
            )
            lbl_destino.configure(text='Banco \nde destino: ')
            cbox_destino.configure(
                values=[
                    banco['nome'] for banco in self.lista_bancos
                ]
            )

            lbl_local_transf.configure(text='Direcionamento: ')
            cbox_local_transf.configure(
                values=[
                    direcionamento['nome'] for direcionamento in self.lista_direcionamentos
                ]
            )

            return
        
        lbl_origem.configure(text='Direcionamento \nde origem: ')

        cbox_origem.configure(
            values=[
                direcionamento['nome'] for direcionamento in self.lista_direcionamentos
            ]
        )

        lbl_destino.configure(text='Direcionamento \nde destino: ')

        cbox_destino.configure(
            values=[
                direcionamento['nome'] for direcionamento in self.lista_direcionamentos
            ]
        )

        lbl_local_transf.configure(text='Banco: ')

        cbox_local_transf.configure(
            values=[
                banco['nome'] for banco in self.lista_bancos
            ]
        )

    def adiciona_Transferencia (self):

        if not self.verifica_entradas('add'):
            return
        
        route = 'transferencias_entre_bancos' if not self.tipo_tranferencia_add_switch.get() else 'transferencias_entre_direcionamentos'

        tipo = 'banco' if not self.tipo_tranferencia_add_switch.get() else 'direcionamento'
        local = 'banco' if self.tipo_tranferencia_add_switch.get() else 'direcionamento'

        origem = self.origem_name_comboBox_add_Transferencia.get()
        destino = self.destino_name_comboBox_add_Transferencia.get()
        local_dado = self.local_tranf_name_comboBox_add_Transferencia.get()
        
        id_origem = self.__getattribute__(f'id_por_{tipo}').get(origem)
        id_destino = self.__getattribute__(f'id_por_{tipo}').get(destino)
        id_local = self.__getattribute__(f'id_por_{local}').get(local_dado)

        transferencia = {   
            f'id_{tipo}_origem': id_origem,
            f'id_{tipo}_destino': id_destino,
            f'id_{local}': id_local,
            'descricao': self.descricao_entry_add_Transferencia.get(),
            'valor': self.valor_entry_add_Transferencia.get()
        }

        adicionou = post(
            f"http://localhost:8000/{route}",
            json=transferencia
        )

        if adicionou.status_code == 201:
            success_msg('Sucesso', 'Transferência adicionada com sucesso!')
            return
        
        error_msg('Erro', 'Erro ao adicionar Transferência!')

    def cria_widgets_tab_adiciona_Transferencias(self):
        self.tipo_tranferencia_add_switch = self.tab_adiciona_Transferencias.Switch(
            {
                **switch_style.default,
                'text': 'Tipo de transferência',
                'command': lambda: self.controla_switch('add'),
                'width': 250,
                'height': 40,
                
            },
            {
                'relx': 0.5,
                'rely': 0.1,
                'anchor': 'center'
            }
        )

        self.label_titulo_add = self.tab_adiciona_Transferencias.Label(
            {
                'font': ('Roboto', 20),
                'corner_radius': 4,
                'fg_color': colors['color1'],    
                'text_color': colors['color5'],
                'text': 'Transferência entre \nBancos',
                'width': 230,
                'height': 80
            },
            {
                'relx': 0.5,
                'rely': 0.2,
                'anchor': 'center'
            }
        )


        main_frame = PageModel(self.tab_adiciona_Transferencias.Frame(
            {
                **frame_style.fg_1,
            },
            {
                'relx': 0.5,
                'rely': 0.45,
                'anchor': 'center'
            }
        ))

        self.label_origem_add = main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Banco de origem:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.origem_name_comboBox_add_Transferencia = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values': [""] + [banco['nome'] for banco in self.lista_bancos],
            },
            {
                'row': 0,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        self.label_destino_add = main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Banco de destino:',
            },
            {
                'row': 1,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.destino_name_comboBox_add_Transferencia = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values':[""] + [banco['nome'] for banco in self.lista_bancos],
            },
            {
                'row': 1,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        self.label_local_tranf_add = main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Direcionamento:',
            },
            {
                'row': 2,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.local_tranf_name_comboBox_add_Transferencia = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values': [""] + [direcionamento['nome'] for direcionamento in self.lista_direcionamentos],
            },
            {
                'row': 2,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Valor:',
            },
            {
                'row': 4,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.valor_entry_add_Transferencia = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Valor',
            },
            {
                'row': 4,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Descrição:',
            },
            {
                'row': 3,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.descricao_entry_add_Transferencia = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Descrição: ',
            },
            {
                'row': 3,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        self.tab_adiciona_Transferencias.Button(
            {
                **btn_style.large,
                'text': 'Adicionar Transferência',
                'command': self.adiciona_Transferencia
            },
            {
                'relx': 0.5,
                'rely': 0.7,
                'anchor': 'center'
            }
        )

        main_frame.build()
        self.tab_adiciona_Transferencias.build()
        
    def listar_transferencias_em_frame (self, page):

        frame = self.__getattribute__(f'frame_lista_transferencias_{page}')

        tipo_transf = 'transferencias_entre_bancos' if not self.__getattribute__(f'tipo_tranferencia_{page}_switch').get() else 'transferencias_entre_direcionamentos'
        
        transferencias = get(
            f'http://localhost:8000/{tipo_transf}/'
        ).json()

        actual_month = datetime.now().month
        start_of_the_month = datetime.strptime(f'01/{actual_month - 1}/{datetime.now().year}', '%d/%m/%Y')
        end_of_the_month = datetime.strptime(f'01/{actual_month + 1 if actual_month != 12 else 1}/{datetime.now().year}', '%d/%m/%Y')

        tipo = 'banco' if not self.__getattribute__(f'tipo_tranferencia_{page}_switch').get() else 'direcionamento'
        local = 'banco' if self.__getattribute__(f'tipo_tranferencia_{page}_switch').get() else 'direcionamento'

        for wid in frame.master.winfo_children()[1:]:
            wid.destroy()

        for i, transferencia in enumerate(transferencias):
            if start_of_the_month <= datetime.strptime(transferencia['created_at'], '%d/%m/%Y') < end_of_the_month:
            
                frame_transferencia = PageModel(frame.Frame(
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

                
                frame_transferencia.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': transferencia['id'],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 0,
                    }
                )
                frame_transferencia.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': self.__getattribute__(f'{tipo}s_por_id')[transferencia[f'id_{tipo}_origem']],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 1,
                    }
                )
                frame_transferencia.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text':self.__getattribute__(f'{tipo}s_por_id')[transferencia[f'id_{tipo}_destino']],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 2,
                    }
                )
                frame_transferencia.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': transferencia['valor'],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 4
                    }
                )
                frame_transferencia.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': self.__getattribute__(f'{local}s_por_id')[transferencia[f'id_{local}']],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 3,
                    }
                )

                for lbl in frame_transferencia.master.winfo_children():
                    lbl.configure(
                        fg_color='transparent'
                    )

                    lbl.bind(
                        '<Button-1>',
                        lambda event: self.get_dados_transferencia(page, event.widget.master.master)
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
            
            frame_transferencia.build()

        frame.build()

    def cria_headers_transferencias (self, page):
        frame: 'PageModel' = self.__getattribute__(f'frame_lista_transferencias_{page}_headers')
        
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
                'text': 'Origem',
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
                'text': 'Destino',
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
                'text': 'Local',
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
                'text': 'Valor',
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

    def escreve_dados_trasnferencia_selecionada (self, page: str, transferencia: list):


        transferencia = {
            'id': transferencia[0],
            'origem': transferencia[1],
            'destino': transferencia[2],
            'local': transferencia[4],
            'valor': transferencia[3],
        }

        transferencia_id_entry = self.__getattribute__(f'transferencia_id_entry_{page}_Transferencia') 
        origem_name_comboBox = self.__getattribute__(f'origem_name_comboBox_{page}_Transferencia')
        destino_name_comboBox = self.__getattribute__(f'destino_name_comboBox_{page}_Transferencia')
        valor_entry = self.__getattribute__(f'valor_entry_{page}_Transferencia')
        local_comboBox = self.__getattribute__(f'local_tranf_name_comboBox_{page}_Transferencia')


        transferencia_id_entry.configure(
            textvariable = ctk.StringVar(value=transferencia['id'])
        )
        origem_name_comboBox.configure(
            variable = ctk.StringVar(value=transferencia['origem'])
        )

        destino_name_comboBox.configure(
            variable = ctk.StringVar(value=transferencia['destino'])
        )
        valor_entry.configure(
            textvariable = ctk.StringVar(value=transferencia['valor'])
        )

        local_comboBox.configure(
            variable = ctk.StringVar(value=transferencia['local'])
        )

    def get_dados_transferencia (self, page, transferencia):

        dados_transferencia = [
            dado.cget('text') for dado in transferencia.winfo_children()
        ]
        
        self.escreve_dados_trasnferencia_selecionada(page, dados_transferencia)
        
    def edita_transferencia (self):
        tipo_switch = self.tipo_tranferencia_edit_switch.get()
        id_transferencia = self.transferencia_id_entry_edit_Transferencia.get()

        local = 'banco' if tipo_switch else 'direcionamento'
        tipo = 'banco' if not tipo_switch else 'direcionamento'

        tipo_transferencia_route = 'transferencias_entre_bancos' if not tipo_switch else 'transferencias_entre_direcionamentos'

        if not self.verifica_entradas('edit'):
            warning_msg('Erro', 'Verifique as entradas')
            return

        novo_id_origem = self.__getattribute__(f'id_por_{tipo}')[self.origem_name_comboBox_edit_Transferencia.get()]
        novo_id_destino = self.__getattribute__(f'id_por_{tipo}')[self.destino_name_comboBox_edit_Transferencia.get()]
        novo_id_local = self.__getattribute__(f'id_por_{local}')[self.local_tranf_name_comboBox_edit_Transferencia.get()]

        novo_deposito = {
            f'novo_id_{tipo}_origem': novo_id_origem,
            f'novo_id_{tipo}_destino': novo_id_destino,
            f'novo_id_{local}': novo_id_local,
            'novo_valor': self.valor_entry_edit_Transferencia.get(),
        }

        res = put(
            f'http://localhost:8000/{tipo_transferencia_route}/{id_transferencia}',
            json=novo_deposito
        )

        if res.status_code == 500:
            error_msg('Erro', 'Erro ao editar transferência')
            return
        
        if res.status_code == 404:
            error_msg('Erro', 'Transferência inexistente!')
            return
        
        success_msg('Editado', 'Transferência editado com sucesso!')

    def deleta_transferencia (self):
        id_transferencia = self.transferencia_id_entry_delete_Transferencia.get()

        route = 'transferencias_entre_bancos' if not self.tipo_tranferencia_delete_switch.get() else 'transferencias_entre_direcionamentos'


        res = delete(
            f'http://localhost:8000/{route}/{id_transferencia}'
        )

        if res.status_code == 500:
            error_msg('Erro', 'Erro ao deletar gasto')
            return

        if res.status_code == 404:
            error_msg('Erro', 'Gasto inexistente!')
            return

        success_msg('Deletado', 'Gastos deletado com sucesso!')

    def cria_widgets_tab_edita_Transferencia(self):
        self.tipo_tranferencia_edit_switch = self.tab_editar_Transferencia.Switch(
            {
                **switch_style.default,
                'text': 'Tipo de transferência',
                'command': lambda: self.controla_switch('edit'),
                'width': 250,
                'height': 40,
                
            },
            {
                'relx': 0.32,
                'rely': 0.1,
                'anchor': 'center'
            }
        )

        self.label_titulo_edit = self.tab_editar_Transferencia.Label(
            {
                'font': ('Roboto', 20),
                'corner_radius': 4,
                'fg_color': colors['color1'],    
                'text_color': colors['color5'],
                'text': 'Transferência entre \nBancos',
                'width': 230,
                'height': 80
            },
            {
                'relx': 0.23,
                'rely': 0.15,
            }
        )

        main_frame = PageModel(self.tab_editar_Transferencia.Frame(
            {
                **frame_style.fg_1
            },
            {
                'relx': 0.32,
                'rely': 0.5,
                'anchor': 'center'
            }
        ))

        self.frame_lista_transferencias_edit = PageModel(
            self.tab_editar_Transferencia.ScrollableFrame(
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

        self.frame_lista_transferencias_edit_headers = PageModel(
            self.frame_lista_transferencias_edit.Frame(
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

        self.cria_headers_transferencias('edit')

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'id:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.transferencia_id_entry_edit_Transferencia = main_frame.Entry(
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

        self.label_origem_edit = main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Banco de \norigem:',
            },
            {
                'row': 1,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.origem_name_comboBox_edit_Transferencia = main_frame.ComboBox(
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

        self.label_destino_edit = main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Banco de \ndestino:',
            },
            {
                'row': 2,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.destino_name_comboBox_edit_Transferencia = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values':[""] + [banco['nome'] for banco in self.lista_bancos],
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

        self.valor_entry_edit_Transferencia = main_frame.Entry(
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

        self.label_local_tranf_edit = main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Direcionamento:',
            },
            {
                'row': 4,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.local_tranf_name_comboBox_edit_Transferencia = main_frame.ComboBox(
            {
                **entry_style.medium,
                'values': [""] + [direcionamento['nome'] for direcionamento in self.lista_direcionamentos]
            },
            {
                'row': 4,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )


        self.tab_editar_Transferencia.Button(
            {
                **btn_style.large,
                'text': 'Editar',
                'command': self.edita_transferencia
            },
            {
                'relx': 0.23,
                'rely': 0.85,
                'anchor': 'center'
            }
        )

        self.tab_editar_Transferencia.Button(
            {
                **btn_style.large,
                'text': 'Atualizar',
                'command': lambda:self.listar_transferencias_em_frame('edit')
            },
            {
                'relx': 0.4,
                'rely': 0.85,
                'anchor': 'center'
            }
        )

        main_frame.build()
        self.frame_lista_transferencias_edit.build()
        self.listar_transferencias_em_frame('edit')
        self.tab_editar_Transferencia.build()

    def cria_widgets_tab_excluir_Transferencia(self):
        self.tipo_tranferencia_delete_switch = self.tab_excluir_Transferencia.Switch(
            {
                **switch_style.default,
                'text': 'Tipo de transferência',
                'command': lambda: self.controla_switch('delete'),
                'width': 250,
                'height': 40,
                
            },
            {
                'relx': 0.32,
                'rely': 0.1,
                'anchor': 'center'
            }
        )

        self.label_titulo_delete = self.tab_excluir_Transferencia.Label(
            {
                'font': ('Roboto', 20),
                'corner_radius': 4,
                'fg_color': colors['color1'],    
                'text_color': colors['color5'],
                'text': 'Transferência entre \nBancos',
                'width': 230,
                'height': 80
            },
            {
                'relx': 0.23,
                'rely': 0.15,
            }
        )

        main_frame = PageModel(self.tab_excluir_Transferencia.Frame(
            {
                **frame_style.fg_1
            },
            {
                'relx': 0.32,
                'rely': 0.5,
                'anchor': 'center'
            }
        ))

        self.frame_lista_transferencias_delete = PageModel(
            self.tab_excluir_Transferencia.ScrollableFrame(
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

        self.frame_lista_transferencias_delete_headers = PageModel(
            self.frame_lista_transferencias_delete.Frame(
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

        self.cria_headers_transferencias('delete')

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'id:',
            },
            {
                'row': 0,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.transferencia_id_entry_delete_Transferencia = main_frame.Entry(
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

        self.label_origem_delete = main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Banco de \norigem:',
            },
            {
                'row': 1,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.origem_name_comboBox_delete_Transferencia = main_frame.ComboBox(
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

        self.label_destino_delete = main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Banco de \ndestino:',
            },
            {
                'row': 2,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.destino_name_comboBox_delete_Transferencia = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values':[""] + [banco['nome'] for banco in self.lista_bancos],
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

        self.valor_entry_delete_Transferencia = main_frame.Entry(
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

        self.label_local_tranf_delete = main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Direcionamento:',
            },
            {
                'row': 4,
                'column': 0,
                'padx': 10,
                'pady': 5
            }
        )

        self.local_tranf_name_comboBox_delete_Transferencia = main_frame.ComboBox(
            {
                **entry_style.medium,
                'values': [""] + [direcionamento['nome'] for direcionamento in self.lista_direcionamentos]
            },
            {
                'row': 4,
                'column': 1,
                'padx': 10,
                'pady': 5
            }
        )


        self.tab_excluir_Transferencia.Button(
            {
                **btn_style.large,
                'text': 'Deletar',
                'command': self.deleta_transferencia
            },
            {
                'relx': 0.23,
                'rely': 0.85,
                'anchor': 'center'
            }
        )

        self.tab_excluir_Transferencia.Button(
            {
                **btn_style.large,
                'text': 'Atualizar',
                'command': lambda:self.listar_transferencias_em_frame('edit')
            },
            {
                'relx': 0.4,
                'rely': 0.85,
                'anchor': 'center'
            }
        )

        main_frame.build()
        self.frame_lista_transferencias_delete.build()
        self.listar_transferencias_em_frame('delete')
        self.tab_excluir_Transferencia.build()
