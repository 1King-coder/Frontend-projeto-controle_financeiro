import customtkinter as ctk
from .Page_model import PageModel
from .styles.style import *
from .styles.colors import colors
from .utils.msg_boxes import error_msg, success_msg, warning_msg
from requests import get, post, delete, put
from datetime import datetime

class Gastos_Page(PageModel):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)

        self.lista_bancos: list = get('http://127.0.0.1:8000/bancos/').json()
        self.lista_direcionamentos: list = get('http://127.0.0.1:8000/direcionamentos/').json()
        self.conta_gastos = 0
        self.lista_gastos_para_adicionar: dict[str, list[dict]] = {
            'gastos_gerais': [],
            'gastos_periodizados': [],
        }

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
        self.master.title("Gastos")

        self.tab_view = ctk.CTkTabview(self.master, bg_color=colors['color1'])

        self.tab_view.add('Adicionar Gasto')
        self.tab_view.add('Editar Gasto')
        self.tab_view.add('Excluir Gasto')

        self.tab_adiciona_Gastos = PageModel(self.tab_view.tab('Adicionar Gasto'))
        self.tab_editar_Gasto = PageModel(self.tab_view.tab('Editar Gasto'))
        self.tab_excluir_Gasto = PageModel(self.tab_view.tab('Excluir Gasto'))

        self.cria_widgets_tab_adiciona_Gastos()
        self.cria_widgets_tab_edita_Gasto()
        self.cria_widgets_tab_excluir_Gasto()

        self.tab_view.pack(expand=True, fill='both')

    def adiciona_lista_gastos (self, gasto: dict) -> bool:
        gasto_para_adicionar = {
            'id_banco': self.id_por_banco[gasto['banco']],
            'id_direcionamento': self.id_por_direcionamento[gasto['direcionamento']],
            'tipo_gasto': gasto['tipo'],
            'valor' if gasto['tipo'] == 'imediato' else 'valor_parcela': gasto['valor'],
            'descricao': gasto['descricao'],
        }

        if gasto['tipo'] == 'periodizado':
            if len(self.lista_gastos_para_adicionar['gastos_periodizados']) == 1:
                warning_msg('Aviso', 'Não pode adicionar mais de um gasto periodizado!')
                return
            
            gasto_para_adicionar.pop('tipo_gasto')
            
            gasto_para_adicionar['dia_abate'] = gasto['dia_abate']
            gasto_para_adicionar['total_parcelas'] = gasto['total_parcelas']
            gasto_para_adicionar['controle_parcelas'] = gasto['controle_parcelas']

            self.lista_gastos_para_adicionar['gastos_periodizados'].append(
                gasto_para_adicionar
            )
            return        

        self.lista_gastos_para_adicionar['gastos_gerais'].append(gasto_para_adicionar)

    def verifica_entradas_adicionar (self) -> bool:

        if not self.verifica_entrada_banco ('add'):
            warning_msg('Erro', 'Selecione um banco!')
            return False
        
        if not self.verifica_entrada_direcionamento ('add'):
            warning_msg('Erro', 'Selecione um direcionamento!')
            return False
        
        if not self.verifica_entrada_valor ('add'):
            return False
        
        if self.tipo_gasto_comboBox_add_Gasto.get() not in ['imediato', 'periodizado']:
            return False
        
        if self.tipo_gasto_comboBox_add_Gasto.get() == 'periodizado':
            if not self.verifica_entradas_periodizado ('add'):
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
        
        if self.tipo_gasto_comboBox_edit_Gasto.get() not in ['imediato', 'periodizado']:
            return False
        
        if self.tipo_gasto_comboBox_edit_Gasto.get() == 'periodizado':
            if not self.verifica_entradas_periodizado ('edit'):
                return False
            
        
        return True
    
    def verifica_entradas_periodizado (self, pag: str) -> bool:
        if pag == 'add':
            total_parcelas = self.total_parcelas_entry_add_Gasto.get()
            ctrl_parcelas = self.controle_parcelas_entry_add_Gasto.get()
            valor_parcelas = self.valor_entry_add_Gasto.get()
            dia_abate = self.dia_abate_entry_add_Gasto.get()
            
        if pag == 'edit':
            total_parcelas = self.total_parcelas_entry_edit_Gasto.get()
            ctrl_parcelas = self.controle_parcelas_entry_edit_Gasto.get()
            valor_parcelas = self.valor_entry_edit_Gasto.get()
            dia_abate = self.dia_abate_entry_edit_Gasto.get()

        try:

            int(total_parcelas)
            int(ctrl_parcelas)
            float(valor_parcelas)
            datetime.strptime(dia_abate, '%d-%m-%Y %H:%M:%S')

        except Exception:
            warning_msg('Erro', 'Entradas inválidas!')
            return False
        
        return True           
            
    def verifica_entrada_banco (self, pag: str) -> bool:

        bancos_existentes = [
                banco['nome'] for banco in self.lista_bancos
        ]

        if pag == 'add':
            banco = self.banco_name_comboBox_add_Gasto.get()
            
            
            
        if pag == 'edit':
            banco = self.banco_name_comboBox_edit_Gasto.get()
            
        if not banco:
            warning_msg('Erro', 'Selecione um banco!')
            return False
            
        if not banco in bancos_existentes:
            warning_msg('Erro', 'Banco inexistente!')
            return False
        
        return True

    def verifica_entrada_direcionamento (self, pag: str) -> bool:

        direcionamentos_existentes = [
            direcionamento['nome'] for direcionamento in self.lista_direcionamentos
        ]

        if pag == 'add':
            direcionamento = self.direcionamento_name_comboBox_add_Gasto.get()
        
        if pag == 'edit':
            direcionamento = self.direcionamento_name_comboBox_edit_Gasto.get()
            
        if not direcionamento:
            warning_msg('Erro', 'Selecione um direcionamento!')
            return False
            
        if not direcionamento in direcionamentos_existentes:
            warning_msg('Erro', 'Direcionamento inexistente!')
            return False
        
        return True
        
    def verifica_entrada_valor (self, pag: str) -> bool:

        if pag == 'add':
            valor_gasto = self.valor_entry_add_Gasto.get()
            
        
        if pag == 'edit':
            valor_gasto = self.valor_entry_edit_Gasto.get()
                
        if not valor_gasto:
                warning_msg('Erro', 'O valor deve ser preenchido!')
                return False
            
        try:
            
            float(valor_gasto)

        except Exception:
            warning_msg('Erro', 'O valor deve ser um número!')
            return False
        
        return True
        
    def atualiza_frame_lista_gastos_adicionar (self) -> None:

        if not self.verifica_entradas_adicionar():
            warning_msg('Erro', 'Campos inválidos')
            return
        
        gasto = {
            'banco': self.banco_name_comboBox_add_Gasto.get(),
            'direcionamento': self.direcionamento_name_comboBox_add_Gasto.get(),
            'tipo': self.tipo_gasto_comboBox_add_Gasto.get(),
            'valor': self.valor_entry_add_Gasto.get(),
            'descricao': self.descricao_entry_add_Gasto.get()
        }

        gasto_string = (
            f"Gasto {self.conta_gastos + 1}\n" +
            f"\tBanco: {gasto['banco']}\n" +
            f"\tDirecionamento: {gasto['direcionamento']}\n" +
            f"\tTipo: {gasto['tipo']}\n" 
        )

        if gasto['tipo'] == 'periodizado':
            gasto['dia_abate'] = self.dia_abate_entry_add_Gasto.get()
            gasto['total_parcelas'] = self.total_parcelas_entry_add_Gasto.get()
            gasto['controle_parcelas'] = self.controle_parcelas_entry_add_Gasto.get()
            gasto_string += (
                f"\tDia de abate: {gasto['dia_abate']}\n" +
                f"\tTotal de parcelas: {gasto['total_parcelas']}\n" +
                f"\tControle de parcelas: {gasto['controle_parcelas']}\n"
            )
        
        self.frame_lista_gastos_adicionar.Label(
            {
                **lbl_style.light_rectangle_bg['large'],
                'text': gasto_string,
                'justify': 'left'
            },
            {
                'row': self.conta_gastos + 1,
                'column': 0,
                'padx': 3,
                'pady': 5
            }
        )

        self.adiciona_lista_gastos(gasto)

        self.conta_gastos += 1

        self.frame_lista_gastos_adicionar.build()

    def limpa_frame_lista_gastos_adicionar (self):
        for widget in self.frame_lista_gastos_adicionar.master.winfo_children()[1:]:
            widget.destroy()

        self.lista_gastos_para_adicionar['gastos_gerais'] = []
        self.lista_gastos_para_adicionar['gastos_periodizados'] = []
        self.conta_gastos = 0

        self.frame_lista_gastos_adicionar.build()

    def remove_ultimo_lista_gastos_adicionar(self):

        ultima_label = self.frame_lista_gastos_adicionar.master.winfo_children()[-1]


        tipo_ultimo_gasto = 'imediato' if 'imediato' in ultima_label.cget('text') else 'periodizado'

        if tipo_ultimo_gasto == 'periodizado':
            lista_analisada = self.lista_gastos_para_adicionar['gastos_periodizados']
        else:
            lista_analisada = self.lista_gastos_para_adicionar['gastos_gerais']

        if not len(lista_analisada):
            return
        
        lista_analisada.pop()
        ultima_label.destroy()
        self.conta_gastos -= 1

        self.frame_lista_gastos_adicionar.build()       

    def adiciona_Gastos (self):

        if not self.lista_gastos_para_adicionar:
            warning_msg('Erro', 'Nenhum gasto adicionado')
            return
        
        adicionou_geral = post(
            "http://localhost:8000/gastos_gerais",
            json={'gastos': self.lista_gastos_para_adicionar['gastos_gerais']}
        )


        adicionou_periodizado = post(
            "http://localhost:8000/gastos_periodizados",
            json=self.lista_gastos_para_adicionar['gastos_periodizados'][0]
        )

        if adicionou_geral.status_code == 201 and adicionou_periodizado.status_code == 201:
            success_msg('Sucesso', 'Gastos adicionados com sucesso')
            self.conta_gastos = 0
            self.limpa_frame_lista_gastos_adicionar()
            self.lista_gastos_para_adicionar['gastos_gerais'] = []
            self.lista_gastos_para_adicionar['gastos_periodizados'] = []	
            return
        
        error_msg('Erro', 'Erro ao adicionar depósitos')

    def cria_widgets_tab_adiciona_Gastos(self):
        main_frame = PageModel(self.tab_adiciona_Gastos.Frame(
            {
                **frame_style.fg_1
            },
            {
                'relx': 0.3,
                'rely': 0.3,
                'anchor': 'center'
            }
        ))

        self.frame_lista_gastos_adicionar = PageModel(self.tab_adiciona_Gastos.ScrollableFrame(
            {
                **frame_style.fg_1,
                'width': 500,
                'height': 550
            },
            {
                'relx': 0.8,
                'rely': 0.5,
                'anchor': 'center'
            }
        ))

        self.frame_lista_gastos_adicionar.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Gastos a serem Adicionados',
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
                'padx': 5,
                'pady': 2
            }
        )

        self.banco_name_comboBox_add_Gasto = main_frame.ComboBox(
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

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Direcionamento:',
            },
            {
                'row': 1,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.direcionamento_name_comboBox_add_Gasto = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values':[""] + [direcionamento['nome'] for direcionamento in self.lista_direcionamentos],
            },
            {
                'row': 1,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Tipo:',
            },
            {
                'row': 2,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.tipo_gasto_comboBox_add_Gasto = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values': ["", "imediato", "periodizado"],
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
                'text': 'Dia abate:',
            },
            {
                'row': 2,
                'column': 2,
                'padx': 5,
                'pady': 2
            }
        )

        self.dia_abate_entry_add_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Dia abate',
                

            },
            {
                'row': 2,
                'column': 3,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Total de Parcelas:',
            },
            {
                'row': 3,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.total_parcelas_entry_add_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Total de Parcelas',
                

            },
            {
                'row': 3,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Parcelas já pagas:',
            },
            {
                'row': 3,
                'column': 2,
                'padx': 5,
                'pady': 2
            }
        )

        self.controle_parcelas_entry_add_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Parcelas ja pagas',
                
            },
            {
                'row': 3,
                'column': 3,
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
                'row': 0,
                'column': 2,
                'padx': 5,
                'pady': 2
            }
        )

        self.valor_entry_add_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Valor',
            },
            {
                'row': 0,
                'column': 3,
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
                'row': 1,
                'column': 2,
                'padx': 5,
                'pady': 2
            }
        )

        self.descricao_entry_add_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Descrição',
            },
            {
                'row': 1,
                'column': 3,
                'padx': 5,
                'pady': 2
            }
        )



        self.tab_adiciona_Gastos.Button(
            {
                **btn_style.medium,
                'text': 'Adicionar outro gasto',
                'command': self.atualiza_frame_lista_gastos_adicionar
            },
            {
                'relx': 0.14,
                'rely': 0.55,
                'anchor': 'center'
            }
        )

        self.tab_adiciona_Gastos.Button(
            {
                **btn_style.medium,
                'text': 'Remove último gasto',
                'command': self.remove_ultimo_lista_gastos_adicionar
            },
            {
                'relx': 0.33,
                'rely': 0.55,
                'anchor': 'center'
            }
        )

        self.tab_adiciona_Gastos.Button(
            {
                **btn_style.medium,
                'text': 'Limpar gastos',
                'command': self.limpa_frame_lista_gastos_adicionar
            },
            {
                'relx': 0.5,
                'rely': 0.55,
                'anchor': 'center'
            }
        )

        self.tab_adiciona_Gastos.Button(
            {
                **btn_style.large,
                'text': 'Enviar gastos',
                'command': self.adiciona_Gastos
            },
            {
                'relx': 0.31,
                'rely': 0.67,
                'anchor': 'center'
            }
        )

        main_frame.build()
        self.frame_lista_gastos_adicionar.build()
        self.tab_adiciona_Gastos.build()
        
    def listar_gastos_em_frame (self, frame, page):


        gastos_gerais = get(
            'http://127.0.0.1:8000/gastos_gerais/'
        ).json()

        actual_month = datetime.now().month
        start_of_the_month = datetime.strptime(f'01/{actual_month/1}/{datetime.now().year}', '%d/%m/%Y')
        end_of_the_month = datetime.strptime(f'01/{actual_month + 1 if actual_month != 12 else 1}/{datetime.now().year}', '%d/%m/%Y')

        for wid in frame.master.winfo_children()[1:]:
            wid.destroy()

        for i, gasto in enumerate(gastos_gerais):
            if start_of_the_month <= datetime.strptime(gasto['created_at'], '%d/%m/%Y') < end_of_the_month:
            
                frame_gasto = PageModel(frame.Frame(
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

                
                frame_gasto.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': gasto['id'],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 0,
                    }
                )
                frame_gasto.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': self.bancos_por_id[gasto['id_banco']],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 1,
                    }
                )
                frame_gasto.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': self.direcionamentos_por_id[gasto['id_direcionamento']],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 2,
                    }
                )
                frame_gasto.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': gasto['valor'],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 3,
                    }
                )
                frame_gasto.Label(
                    {
                        **lbl_style.light_rectangle_bg['medium'],
                        'text': gasto['tipo_gasto'],
                        'width': 100,
                        'height': 40,
                        'justify': 'center',
                    },
                    {
                        'row': 0,
                        'column': 4,
                    }
                )

                for lbl in frame_gasto.master.winfo_children():
                    lbl.configure(
                        fg_color='transparent'
                    )

                    lbl.bind(
                        '<Button-1>',
                        lambda event: self.get_dados_gasto(page, event.widget.master.master)
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
            
                frame_gasto.build()

        frame.build()

    def cria_headers_gastos (self, frame):
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
                'text': 'Tipo',
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

    def escreve_dados_gasto_selecionado (self, page:str, gasto: list):

        if gasto[4] == 'periodizado':
            dia_abate = gasto[5]
            total_parcelas = gasto[6]
            controle_parcelas = gasto[7]

        gasto = {
            'id': gasto[0],
            'banco': gasto[1],
            'direcionamento': gasto[2],
            'valor': gasto[3],
            'tipo': gasto[4],
        }

        gasto_id_entry = self.gasto_id_entry_delete_Gasto
        banco_name_comboBox = self.banco_name_comboBox_delete_Gasto
        direcionamento_name_comboBox = self.direcionamento_name_comboBox_delete_Gasto
        valor_entry = self.valor_entry_delete_Gasto
        tipo_entry = self.tipo_gasto_delete_Gasto
        dia_abate_entry = self.dia_abate_entry_delete_Gasto
        total_parcelas_entry = self.total_parcelas_entry_delete_Gasto
        controle_parcelas_entry = self.controle_parcelas_entry_delete_Gasto

        if page == 'edit':
            gasto_id_entry = self.id_gasto_entry_edit_Gasto
            banco_name_comboBox = self.banco_name_comboBox_edit_Gasto
            direcionamento_name_comboBox = self.direcionamento_name_comboBox_edit_Gasto
            valor_entry = self.valor_entry_edit_Gasto
            tipo_entry = self.tipo_gasto_edit_Gasto
            dia_abate_entry = self.dia_abate_entry_edit_Gasto
            total_parcelas_entry = self.total_parcelas_entry_edit_Gasto
            controle_parcelas_entry = self.controle_parcelas_entry_edit_Gasto

        

        

        gasto_id_entry.configure(
            textvariable = ctk.StringVar(value=gasto['id'])
        )
        banco_name_comboBox.configure(
            variable = ctk.StringVar(value=gasto['banco'])
        )

        direcionamento_name_comboBox.configure(
            variable = ctk.StringVar(value=gasto['direcionamento'])
        )
        valor_entry.configure(
            textvariable = ctk.StringVar(value=gasto['valor'])
        )

        tipo_entry.configure(
            variable = ctk.StringVar(value=gasto['tipo'])
        )

        if gasto['tipo'] == 'periodizado':


            dia_abate_entry.configure(
                textvariable = ctk.StringVar(value=dia_abate)
            )

            total_parcelas_entry.configure(
                textvariable = ctk.StringVar(value=total_parcelas)
            )

            controle_parcelas_entry.configure(
                textvariable = ctk.StringVar(value=controle_parcelas)
            )
            

    def get_dados_gasto (self, page, gasto):

        dados_gasto = [
            dado.cget('text') for dado in gasto.winfo_children()
        ]

        if 'periodizado' in dados_gasto:
            gasto_periodizado = get(
                f'http://127.0.0.1:8000/gastos_periodizados/{dados_gasto[0]}'
            ).json()

            dados_gasto.append(gasto_periodizado['dia_abate'])
            dados_gasto.append(gasto_periodizado['total_parcelas'])
            dados_gasto.append(gasto_periodizado['controle_parcelas'])
        
        self.escreve_dados_gasto_selecionado(page, dados_gasto)
        
    def edita_gasto (self):
        tipo_gasto = self.tipo_gasto_comboBox_add_Gasto.get()
        id_gasto = self.gasto_id_entry_edit_Gasto.get()

        tipo_gasto_route = 'gastos_gerais'

        if not self.verifica_entradas_editar():
            warning_msg('Erro', 'Verifique as entradas')
            return

        novo_id_banco = self.id_por_banco[self.banco_name_comboBox_edit_Gasto.get()]

        novo_id_direcionamento = self.id_por_direcionamento[self.direcionamento_name_comboBox_edit_Gasto.get()]

        novo_deposito = {
            'novo_id_banco': novo_id_banco,
            'novo_id_direcionamento': novo_id_direcionamento,
            'novo_valor': self.valor_entry_edit_Gasto.get(),
            'nova_descricao': self.descricao_entry_edit_Gasto.get(),
        }

        if tipo_gasto == 'periodizado':
            
            novo_deposito['novo_dia_abate'] = self.dia_abate_entry_edit_Gasto.get()
            novo_deposito['novo_total_parcelas'] = self.total_parcelas_entry_edit_Gasto.get()
            novo_deposito['novo_controle_parcelas'] = self.controle_parcelas_entry_edit_Gasto.get()
            tipo_gasto_route = 'gastos_periodizados'


        res = put(
            f'http://localhost:8000/{tipo_gasto_route}/{id_gasto}',
            json=novo_deposito
        )

        if res.status_code == 500:
            error_msg('Erro', 'Erro ao editar gasto')
            return
        
        if res.status_code == 404:
            error_msg('Erro', 'Gasto inexistente!')
            return
        
        success_msg('Editado', 'Gasto editado com sucesso!')

    def deleta_gasto (self):
        id_gasto = self.gasto_id_entry_delete_Gasto.get()

        route = 'gastos_gerais'

        tipo_gasto = self.tipo_gasto_comboBox_add_Gasto.get()

        if tipo_gasto == 'periodizado':
            route = 'gastos_periodizados'

        res = delete(
            f'http://localhost:8000/{route}/{id_gasto}'
        )

        if res.status_code == 500:
            error_msg('Erro', 'Erro ao deletar gasto')
            return

        if res.status_code == 404:
            error_msg('Erro', 'Gasto inexistente!')
            return

        success_msg('Deletado', 'Gastos deletado com sucesso!')

    def cria_widgets_tab_edita_Gasto(self):
        main_frame = PageModel(self.tab_editar_Gasto.Frame(
            {
                **frame_style.fg_1
            },
            {
                'relx': 0.32,
                'rely': 0.4,
                'anchor': 'center'
            }
        ))

        self.frame_lista_gastos_edit = PageModel(
            self.tab_editar_Gasto.ScrollableFrame(
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

        frame_lista_gastos_edit_headers = PageModel(
            self.frame_lista_gastos_edit.Frame(
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

        self.cria_headers_gastos(frame_lista_gastos_edit_headers)

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

        self.id_gasto_entry_edit_Gasto = main_frame.Entry(
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

        self.banco_name_comboBox_edit_Gasto = main_frame.ComboBox(
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

        self.direcionamento_name_comboBox_edit_Gasto = main_frame.ComboBox(
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

        self.valor_entry_edit_Gasto = main_frame.Entry(
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

        self.descricao_entry_edit_Gasto = main_frame.Entry(
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

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Dia abate:',
            },
            {
                'row': 5,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.dia_abate_entry_edit_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Dia abate',
                

            },
            {
                'row': 5,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Total de Parcelas:',
            },
            {
                'row': 6,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.total_parcelas_entry_edit_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Total de Parcelas',
                

            },
            {
                'row': 6,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Parcelas já pagas:',
            },
            {
                'row': 7,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.controle_parcelas_entry_edit_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Parcelas ja pagas',
                
            },
            {
                'row': 7,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Tipo'
            },
            {
                'row': 8,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.tipo_gasto_edit_Gasto = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values': [
                    '',
                    'imediato',
                    'periodizado'
                ]
            },
            {
                'row': 8,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )


        self.tab_editar_Gasto.Button(
            {
                **btn_style.large,
                'text': 'Editar',
                'command': self.edita_gasto
            },
            {
                'relx': 0.23,
                'rely': 0.85,
                'anchor': 'center'
            }
        )

        self.tab_editar_Gasto.Button(
            {
                **btn_style.large,
                'text': 'Atualizar',
                'command': lambda:self.listar_gastos_em_frame(self.frame_lista_gastos_edit, 'edit')
            },
            {
                'relx': 0.4,
                'rely': 0.85,
                'anchor': 'center'
            }
        )

        main_frame.build()
        self.frame_lista_gastos_edit.build()
        self.listar_gastos_em_frame(self.frame_lista_gastos_edit, 'edit')
        self.tab_editar_Gasto.build()

    def cria_widgets_tab_excluir_Gasto(self):
        main_frame = PageModel(self.tab_excluir_Gasto.Frame(
            {
                **frame_style.fg_1
            },
            {
                'relx': 0.32,
                'rely': 0.45,
                'anchor': 'center'
            }
        ))

        self.frame_lista_gastos_delete = PageModel(
            self.tab_excluir_Gasto.ScrollableFrame(
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

        frame_lista_gastos_delete_headers = PageModel(
            self.frame_lista_gastos_delete.Frame(
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

        self.cria_headers_gastos(frame_lista_gastos_delete_headers)

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

        self.gasto_id_entry_delete_Gasto = main_frame.Entry(
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

        self.banco_name_comboBox_delete_Gasto = main_frame.ComboBox(
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

        self.direcionamento_name_comboBox_delete_Gasto = main_frame.ComboBox(
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

        self.valor_entry_delete_Gasto = main_frame.Entry(
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

        self.descricao_entry_delete_Gasto = main_frame.Entry(
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

        self.descricao_entry_delete_Gasto = main_frame.Entry(
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

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Dia abate:',
            },
            {
                'row': 5,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.dia_abate_entry_delete_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Dia abate',
                

            },
            {
                'row': 5,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Total de Parcelas:',
            },
            {
                'row': 6,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.total_parcelas_entry_delete_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Total de Parcelas',
                

            },
            {
                'row': 6,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Parcelas já pagas:',
            },
            {
                'row': 7,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.controle_parcelas_entry_delete_Gasto = main_frame.Entry(
            {
                **entry_style.medium,
                'placeholder_text': 'Parcelas ja pagas',
                
            },
            {
                'row': 7,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )

        main_frame.Label(
            {
                **lbl_style.dark_rectangle_bg['large'],
                'text': 'Tipo'
            },
            {
                'row': 8,
                'column': 0,
                'padx': 5,
                'pady': 2
            }
        )

        self.tipo_gasto_delete_Gasto = main_frame.ComboBox(
            {
                **combobox_style.default,
                'values': [
                    '',
                    'imediato',
                    'periodizado'
                ]
            },
            {
                'row': 8,
                'column': 1,
                'padx': 5,
                'pady': 2
            }
        )


        self.tab_excluir_Gasto.Button(
            {
                **btn_style.large,
                'text': 'delete',
                'command': self.deleta_gasto
            },
            {
                'relx': 0.23,
                'rely': 0.88,
                'anchor': 'center'
            }
        )

        self.tab_excluir_Gasto.Button(
            {
                **btn_style.large,
                'text': 'Atualizar',
                'command': lambda:self.listar_gastos_em_frame(self.frame_lista_gastos_delete, 'delete')
            },
            {
                'relx': 0.4,
                'rely': 0.88,
                'anchor': 'center'
            }
        )

        main_frame.build()
        self.frame_lista_gastos_delete.build()
        self.listar_gastos_em_frame(self.frame_lista_gastos_delete, 'delete')
        self.tab_excluir_Gasto.build()


