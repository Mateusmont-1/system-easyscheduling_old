# Implementação que eu realizei antes para tela_logyn.py

import flet
import datetime
from functools import partial
from google.cloud.firestore_v1 import FieldFilter

from . import tela_menu_main
from . import register
from . import tela_transicao
from .firebase_config import get_firestore_client
from .config import COLOR_BORDER_COLOR_ERROR, COLOR_TEXT_IN_DROPDOWN, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        collaborator_ref,
        func1,
        func2,
        func3,
        func4,
        ):
        super().__init__()
        self.title = title
        self.collaborator_ref = collaborator_ref
        self.func = func1
        self.func2 = func2
        self.func3 = func3
        self.func4 = func4
        
        self.collaborator_dict = dict()
        
    
    def InputTextField(self, text:str, hide:bool, value_text=None, read_only=False):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                visible=False,
                height=48,
                width=275,
                read_only=read_only,
                # bgcolor="#f0f3f6",
                bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                content_padding=5,
                text_size=12,
                color=COLOR_TEXT_IN_FIELD,
                value = value_text,
                border_color=COLOR_BORDER_COLOR,
                hint_text=text,
                filled=True,
                cursor_color=COLOR_TEXT,
                hint_style=flet.TextStyle(
                    size=20,
                    color=COLOR_TEXT_IN_FIELD,
                ),
                password=hide,
            ),
        ) 
    
    def build(self):
        self._title = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Text(
                value=self.title,
                size=30,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT,
            ),
        )
        self.collaborator_choose = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha o(a) atendente", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func)
                                  )
            )
        
        for atendente in self.collaborator_ref:
            # Cada documento é um objeto com ID e dados
            atendente_dropdown = self.collaborator_choose.content
            _colaborador_id = atendente.id
            _atendente_data = atendente.to_dict()
        
            _nome = _atendente_data['nome']
            
            # adiciona no dropdown o atendente
            atendente_dropdown.options.append(flet.dropdown.Option(text= _nome, key= _colaborador_id,))
            
            self.collaborator_dict[_colaborador_id] = _atendente_data
        
        self.date_picker = flet.Container(
            alignment=flet.alignment.center,
            content=flet.DatePicker(
                first_date=datetime.datetime.now(),
                last_date=datetime.datetime.now() + datetime.timedelta(days=60),
                on_change=partial(self.func2)
            )
            )
        
        self.day_choose = flet.Container(
            visible=False,
            content=flet.ElevatedButton(
                on_click=lambda _: self.date_picker.content.pick_date(),
                icon=flet.icons.CALENDAR_MONTH,
                text="Informe o dia",
                style=flet.ButtonStyle(
                    shape={
                        "":flet.RoundedRectangleBorder
                        (radius=8),
                    },
                    color={
                        "":"white",
                    }
                ),
                bgcolor=COLOR_BACKGROUND_BUTTON,
                color=COLOR_TEXT_IN_BUTTON,
                height=48,
                width=275,
            )
        )

        self.query_type = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha o tipo de folga",
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func)
                                  )
            )
        
        for i in range(2):
            # Cada documento é um objeto com ID e dados
            query_dropdown = self.query_type.content
            if i < 1:
                texto = "Diário"
            elif i < 2:
                texto = "Semanal"
            # elif i < 3:
            #     texto = "Mensal"
            # adiciona no dropdown o atendente
            query_dropdown.options.append(flet.dropdown.Option(text= texto, key= i))

        self._sign_in = flet.Container(
            content=flet.ElevatedButton(
                on_click=partial(self.func4),
                content=flet.Text(
                    "Cadastrar",
                    size=20,
                    weight="bold",
                ),
                style=flet.ButtonStyle(
                    shape={
                        "":flet.RoundedRectangleBorder
                        (radius=8),
                    },
                    color={
                        "":"white",
                    }
                ),
                bgcolor=COLOR_BACKGROUND_BUTTON,
                color=COLOR_TEXT_IN_BUTTON,
                height=48,
                width=275,
            )
        )

        self._back_button = flet.Container(
            content=flet.ElevatedButton(
                on_click=partial(self.func3),
                content=flet.Text(
                    "Voltar",
                    size=20,
                    weight="bold",
                ),
                style=flet.ButtonStyle(
                    shape={
                        "":flet.RoundedRectangleBorder
                        (radius=8),
                    },
                    color={
                        "":"white",
                    }
                ),
                bgcolor=COLOR_BACKGROUND_BUTTON,
                color=COLOR_TEXT_IN_BUTTON,
                height=48,
                width=275,
            )
        )
        
        return flet.Column(
            scroll="hidden",
            horizontal_alignment="center",
            controls=[
                self._title,
                self.collaborator_choose,
                self.query_type,
                self.day_choose,
                flet.Container(padding=3),
                flet.Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("Data selecionada",
                                            False, None, True),
                    ],
                ),
                self._sign_in,
                self._back_button,
                self.date_picker,
            ],
        )

async def main(page: flet.page, user):
    # Configurações iniciais da página
    page.title = "Cadastrar folga"
    page.clean()
    
    # Obtém o cliente Firestore e a referência aos colaboradores
    db = get_firestore_client()
    collaborator_ref = db.collection("colaborador").stream()
    
    datas_folga = None

    # Função chamada quando a data é alterada
    def _on_date_change(e=None):
        selected_date = obter_data_selecionada(e)
        collaborator_choose, query_type, data_select = obter_referencias_widgets()
        mes, ano, data_formatada = extrair_mes_ano(selected_date)
        
        # Define as datas de folga conforme o tipo de consulta
        nonlocal datas_folga
        if query_type.value == "0":
            datas_folga = [data_formatada]
            data_select.value = data_formatada
        elif query_type.value == "1":
            datas_folga = obter_dias_da_semana(selected_date)
            data_select.value = ", ".join(datas_folga)
        
        data_select.visible = True
        data_select.update()
        return collaborator_choose, datas_folga

    # Função para cadastrar as folgas
    async def _cadastrar(e):
        if verifica_campos():
            collaborator_choose, query_type, data_select = obter_referencias_widgets()
            nonlocal datas_folga
            colaborador_id = collaborator_choose.value
            
            # Adiciona as datas de folga para o colaborador
            leave_manager = register.CollaboratorLeaveManager(colaborador_id)
            confirma = leave_manager.adicionar_datas_folga(datas_folga)
            if confirma:
                texto = "Folga cadastrada!"
                await tela_transicao.main(page, user, texto)
            else:
                data_select.border_color = COLOR_BORDER_COLOR_ERROR
                data_select.update()

    # Obtém a data selecionada no date_picker ou no evento
    def obter_data_selecionada(e):
        if e:
            return e.control.value
        return _scheduling_.date_picker.content.value

    # Obtém referências aos widgets necessários
    def obter_referencias_widgets():
        collaborator_choose = _scheduling_.collaborator_choose.content
        query_type = _scheduling_.query_type.content
        data_select = _scheduling_.controls[0].controls[5].controls[0].content
        return collaborator_choose, query_type, data_select

    # Extrai o mês, ano e data formatada de uma data fornecida
    def extrair_mes_ano(selected_date):
        data_objeto = datetime.datetime.strptime(str(selected_date), '%Y-%m-%d %H:%M:%S')
        data_formatada = data_objeto.strftime('%d-%m-%Y')
        return data_objeto.month, data_objeto.year, data_formatada

    # Obtém os dias da semana a partir de uma data fornecida
    def obter_dias_da_semana(selected_date):
        data_objeto = datetime.datetime.strptime(str(selected_date), '%Y-%m-%d %H:%M:%S')
        inicio_semana = data_objeto - datetime.timedelta(days=data_objeto.weekday())
        dias_semana = [(inicio_semana + datetime.timedelta(days=i)).strftime('%d-%m-%Y') for i in range(7)]
        return dias_semana

    # Função para atualizar a visibilidade dos widgets
    async def _visible_button(e):
        query_type = _scheduling_.query_type
        day_choose = _scheduling_.day_choose
        
        if not query_type.visible:
            query_type.visible = True
            query_type.update()
        else:
            day_choose.content.text = "Informe o dia" if query_type.content.value == "0" else "Informe a semana"
            day_choose.visible = True
            day_choose.update()

        if _scheduling_.date_picker.content.value is not None:
            _on_date_change()

    # Verifica se os campos estão preenchidos corretamente
    def verifica_campos():
        collaborator_choose, query_type, data_select = obter_referencias_widgets()
        campos = [
            (collaborator_choose, collaborator_choose.value),
            (query_type, query_type.value),
            (data_select, data_select.value),
        ]
        
        campos_invalidos = False
        for campo, valor in campos:
            if not valor:  # Verifica se o valor está vazio ou None
                campo.border_color = COLOR_BORDER_COLOR_ERROR
                campo.update()
                campos_invalidos = True
            else:
                campo.border_color = COLOR_BORDER_COLOR
                campo.update()
        
        return not campos_invalidos

    # Função para retornar à página principal
    async def return_page(e):
        await tela_menu_main.main(page, user)
             
    # Função para redimensionar a página
    def page_resize(e=None, inicio=None):
        largura = min(page.width - 30, 600)
        altura = min(page.height - 60, 600)
        if e:
            _scheduling_.width = largura
            _scheduling_.height = altura
            _scheduling_.update()
        if inicio is not None:
            return largura if inicio else altura
    
    # Define o manipulador para redimensionamento da janela
    page.window.on_resized = page_resize
                
    # Cria a coluna principal da interface
    def _main_column_():
        return flet.Container(
            width=page_resize(e=None, inicio=True),
            height=page_resize(e=None, inicio=False),
            bgcolor=COLOR_BACKGROUND_CONTAINER,
            padding=12,
            border_radius=35,
            content=flet.Column(
                scroll="hidden",
                spacing=0,
                horizontal_alignment="center",
            )
        ) 
        
    # Adiciona um componente à página
    def add_page(extruct):
        page.add(flet.Row(alignment="center", spacing=25, controls=[extruct]))
        
    # Cria o widget de agendamento de folgas
    _scheduling_ = UserWidget(
        "Cadastrar folga!",
        collaborator_ref,
        _visible_button,
        _on_date_change,
        return_page,
        _cadastrar,
    )
    
    _scheduling_main = _main_column_()
    _scheduling_main.content.controls.append(flet.Container(padding=0))
    _scheduling_main.content.controls.append(_scheduling_)
    
    add_page(_scheduling_main)

   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER, port=8090)
