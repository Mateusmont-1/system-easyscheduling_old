import flet
from functools import partial
import re

from . import tela_menu_main
from . import register
from .firebase_config import get_firestore_client
from . import tela_transicao
from .config import COLOR_BORDER_COLOR_ERROR, COLOR_TEXT_IN_DROPDOWN, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD


class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        sub_title:str,
        btn_name:str,
        erro:str,
        type_collaboraty,
        func,
        func2,
        func3,
        collaborator_ref,
        user_ref
        ):
        self.title = title
        self._sub_title = sub_title
        self.btn_name = btn_name
        self.erro = erro
        self.type_collaborator_ref = type_collaboraty
        self.func = func
        self.func2 = func2
        self.func3 = func3
        self.collaborator_ref = collaborator_ref.to_dict()
        self.user_ref = user_ref.to_dict()
        self.collaborator_id = collaborator_ref.id
        super().__init__()
    
    def InputTextField(self, text:str, hide:bool, value_text=None):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=275,
                # bgcolor="#f0f3f6",
                bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                content_padding=10,
                value=value_text,
                text_size=12,
                color=COLOR_TEXT_IN_FIELD,
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
    
    def InputTextField2(self, text:str, hide:bool, value_text=None):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=145,
                value=value_text,
                bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                text_size=12,
                color=COLOR_TEXT_IN_FIELD,
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
        
    def SignInOption(self):
        return flet.Container(
            content=flet.ElevatedButton
        )
    
    def build(self):
        self._title = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Text(
                self.title,
                size=30,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT,
            ),
        )
        
        self._sub_title = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Text(
                self._sub_title,
                text_align="center",
                color=COLOR_TEXT,
                size=25
            ),
        )
        
        self._type_collaborator = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha o nivel de acesso", 
                                  value=self.user_ref['funcaoID'],
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  )
            )
        
        for type in self.type_collaborator_ref:
            # Cada documento é um objeto com ID e dados     
            if type.id != "cliente":
                
                type_dropdown = self._type_collaborator.content
                _type_id = type.id
                _type_data = type.to_dict()
        
                _nome = type.id
            
                # adiciona no dropdown o atendente
                type_dropdown.options.append(flet.dropdown.Option(text= _nome, key= _type_id,))
        
        self._checkbox_barber = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Row(
                controls=[
                flet.Checkbox(value=True),
                flet.Text(
                    value="Cadastrar como atendente?",
                    size=20,
                    weight="bold",
                    color=COLOR_TEXT_IN_FIELD,),
                ],
            visible=False,
            alignment=flet.MainAxisAlignment.CENTER,
            ))
        
        self._text = flet.Container(
            alignment=flet.alignment.center,
            visible=True,
            content=flet.Text(
                "Informe o horário de atendimento",
                size=20,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT,
            ),
        )
        self._text2 = flet.Container(
            alignment=flet.alignment.center,
            visible=True,
            content=flet.Text(
                "Segunda a Sexta-feira:",
                size=20,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT,
            ),
        )
        self._text3 = flet.Container(
            alignment=flet.alignment.center,
            visible=True,
            content=flet.Text(
                "Sábado:",
                size=20,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT,
            ),
        )
        self._text4 = flet.Container(
            alignment=flet.alignment.center,
            visible=True,
            content=flet.Text(
                "Domingo:",
                size=20,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT,
            ),
        )
        
        self._checkbox_schedulling = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Row(
                controls=[
                flet.Checkbox(value=self.collaborator_ref['permitir_agendamento']),
                flet.Text(
                    value="Permitir agendamento?",
                    size=20,
                    weight="bold",
                    color=COLOR_TEXT_IN_FIELD,),
                ],
            visible=True,
            alignment=flet.MainAxisAlignment.CENTER,
            ))
        
        self._weekdays_button = flet.Container(
            content=flet.ElevatedButton(
                on_click=partial(self.func3),
                content=flet.Text(
                    "Dias de Trabalho",
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

        self._sign_in = flet.Container(
            content=flet.ElevatedButton(
                on_click=partial(self.func),
                content=flet.Text(
                    self.btn_name,
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
                on_click=partial(self.func2),
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
            horizontal_alignment="center",
            controls=[
                self._title,
                self._sub_title,
                flet.Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("Nome",
                                            False, self.user_ref['nome']),
                        self.InputTextField("Telefone",
                                            False, self.user_ref['telefone']),
                    ],
                ),
                self._type_collaborator,
                self._checkbox_barber,
                self._text,
                self._text2,
                flet.Row(
                    alignment="center",
                    spacing=12,
                    visible=True,
                    controls=[
                        self.InputTextField2("Começa (h)",False, str(self.collaborator_ref['semana_inicio'])),
                        self.InputTextField2("Termina (h)",False, str(self.collaborator_ref['semana_fim'])),
                        ],
                ),
                self._text3,
                flet.Row(
                    alignment="center",
                    spacing=12,
                    visible=True,
                    controls=[
                        self.InputTextField2("Começa (h)",False, str(self.collaborator_ref['sabado_inicio'])),
                        self.InputTextField2("Termina (h)",False, str(self.collaborator_ref['sabado_fim'])),
                        ],
                ),
                self._text4,
                flet.Row(
                    alignment="center",
                    spacing=12,
                    visible=True,
                    controls=[
                        self.InputTextField2("Começa (h)",False, str(self.collaborator_ref['domingo_inicio'])),
                        self.InputTextField2("Termina (h)",False, str(self.collaborator_ref['domingo_fim'])),
                        ],
                ),
                self._checkbox_schedulling,
                flet.Container(padding=5),
                self._weekdays_button,
                self._sign_in,
                self._back_button,
            ],
        )

async def main(page:flet.page, user, id_colaborador):
    page.title = "Editar colaborador"

    page.clean()
    
    db = get_firestore_client()
    type_collaboraty_ref = db.collection("funcoes").stream()
    
    colaborar_ref = db.collection("colaborador").document(id_colaborador).get()
    user_ref = db.collection("usuarios").document(id_colaborador).get()
    
    def page_resize(e=None, inicio=None):
        if e:
            if page.width > 600:     
                largura = 600
                _register_collaboraty_main.width = largura
                _register_collaboraty_main.update()
            else:
                largura = page.width - 30
                _register_collaboraty_main.width = largura
                _register_collaboraty_main.update()
            if page.height > 600:     
                altura = 600
                _register_collaboraty_main.height = altura
                _register_collaboraty_main.update()
            else:
                altura = page.height - 60
                _register_collaboraty_main.height = altura
                _register_collaboraty_main.update()

        # Inicio True retorna largura para _main_column
        if inicio:
            if page.width > 600:     
                largura = 600
                return largura
            else:
                largura = page.width - 30
                return largura

        # Inicio False retorna altura para _main_column    
        elif inicio is False:
            if page.height > 600:     
                altura = 600
                return altura
            else:
                altura = page.width - 60
                return altura    
    
    page.window.on_resized = page_resize
                
    def open_weekday_dialog(e):
        dias_trabalhados = _register_collaboraty_.collaborator_ref.get('dias_trabalhados', [0, 1, 2, 3, 4, 5, 6])
        dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
        
        checkboxes = []
        for i, dia in enumerate(dias_semana):
            checkboxes.append(
                flet.Checkbox(label=dia, value=(i in dias_trabalhados), data=i)
            )
        
        weekdays_dialog = flet.AlertDialog(
            title=flet.Text("Selecione os Dias da Semana"),
            scrollable=True,
            content=flet.Column(controls=checkboxes),
            actions=[flet.TextButton("OK", on_click=close_weekday_dialog)]
        )
        
        page.dialog = weekdays_dialog
        weekdays_dialog.open = True
        page.update()

    def close_weekday_dialog(e):
        checkboxes = page.dialog.content.controls
        work_days_selected = [cb.data for cb in checkboxes if cb.value]
        _register_collaboraty_.collaborator_ref['dias_trabalhados'] = work_days_selected
        
        page.dialog.open = False
        page.update()

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
    
    async def back_button(e):
        await tela_menu_main.main(page, user)
                
        
    def add_page(extruct):
        page.add(
            flet.Row(
                alignment="center",
                spacing=25,
                controls=[
                extruct,
                ]
            )
        )

    async def _update_collaboraty(e):
        # Obtendo email, senha, nome, telefone, informado na interface
        nome = _register_collaboraty_.controls[0].controls[2].controls[0].content.value
        telefone = _register_collaboraty_.controls[0].controls[2].controls[1].content.value
        # Obtendo o tipo de colaborador
        type_collaboraty = _register_collaboraty_._type_collaborator.content.value
        # Verificação se é para permitir agendamento com o barbeiro
        checkbox_scheduling = _register_collaboraty_._checkbox_schedulling.content.controls[0].value
        # Se todos os campos foram preenchidos executa cadastro no sistema
        if verifica_campos():
            # Verifica se o campo 'dias_trabalhados' está presente, caso contrário assume todos os dias da semana
            dias_trabalhados = _register_collaboraty_.collaborator_ref.get('dias_trabalhados', [0, 1, 2, 3, 4, 5, 6])
    
            # Obtendo os valores de horário de funcionamento
            workday_start_time = _register_collaboraty_.controls[0].controls[7].controls[0].content.value
            workday_end_time = _register_collaboraty_.controls[0].controls[7].controls[1].content.value
            saturday_start_time = _register_collaboraty_.controls[0].controls[9].controls[0].content.value
            saturday_end_time = _register_collaboraty_.controls[0].controls[9].controls[1].content.value
            sunday_start_time = _register_collaboraty_.controls[0].controls[11].controls[0].content.value
            sunday_end_time = _register_collaboraty_.controls[0].controls[11].controls[1].content.value
            # Cria a instância da classe UpdateCollaborator com os parâmetros necessários
            cadastro = register.UpdateCollaborator(
                nome, telefone, type_collaboraty, checkbox_scheduling, 
                workday_start_time, workday_end_time, 
                saturday_start_time, saturday_end_time, 
                sunday_start_time, sunday_end_time, 
                id_colaborador, dias_trabalhados
            )
            cadastro.atualizar_colaborador()
            
            texto = "Colaborador atualizado!"
            await tela_transicao.main(page, user, texto)     
                
    def verifica_campos():

        # Expressão regular para validar o formato "HH:MM"
        time_format_regex = re.compile(r'^\d{2}:\d{2}$')

        # Função para validar um campo de horário
        def validate_time_field(time_field):
            if time_field.value == "":
                time_field.border_color = COLOR_BORDER_COLOR_ERROR
                time_field.update()
                return 1
            elif not time_format_regex.match(time_field.value):
                time_field.border_color = COLOR_BORDER_COLOR_ERROR
                time_field.update()
                return 1
            else:
                time_field.border_color = COLOR_BORDER_COLOR
                time_field.update()
                return 0
            
        # Obtendo nome, telefone, informado na interface
        nome = _register_collaboraty_.controls[0].controls[2].controls[0].content
        telefone = _register_collaboraty_.controls[0].controls[2].controls[1].content
        # Obtendo o tipo de colaborador
        type_collaboraty = _register_collaboraty_._type_collaborator.content
        # Verificação se é para cadastrar como atendente ou somente administrador
        checkbox_create_barber = _register_collaboraty_._checkbox_barber.content.controls[0].value
        # Verificação se é para permitir agendamento com o atendente
        
        verifica = 0
        if nome.value == "":
            nome.border_color = COLOR_BORDER_COLOR_ERROR
            nome.update()
            verifica += 1
        else:
            nome.border_color = COLOR_BORDER_COLOR
            nome.update()
        if telefone.value == "":
            telefone.border_color = COLOR_BORDER_COLOR_ERROR
            telefone.update()
            verifica += 1
        else:
            telefone.border_color = COLOR_BORDER_COLOR
            telefone.update()
        if type_collaboraty.value == None:
            type_collaboraty.border_color = COLOR_BORDER_COLOR_ERROR
            verifica +=1
        # Verifica se a opção de criar atendente no sistema está ativa
        if checkbox_create_barber == True:
            # Se estiver ativo possui mais campos de prenchimentos obrigatorios
            # Obtendo referencia aos campos que devem ser preenchidos
            workday_start_time = _register_collaboraty_.controls[0].controls[7].controls[0].content
            workday_end_time = _register_collaboraty_.controls[0].controls[7].controls[1].content
            saturday_start_time = _register_collaboraty_.controls[0].controls[9].controls[0].content
            saturday_end_time = _register_collaboraty_.controls[0].controls[9].controls[1].content
            sunday_start_time = _register_collaboraty_.controls[0].controls[11].controls[0].content
            sunday_end_time = _register_collaboraty_.controls[0].controls[11].controls[1].content

            
            verifica += validate_time_field(workday_start_time)
            verifica += validate_time_field(workday_end_time)
            verifica += validate_time_field(saturday_start_time)
            verifica += validate_time_field(saturday_end_time)
            verifica += validate_time_field(sunday_start_time)
            verifica += validate_time_field(sunday_end_time)
        
        return True if verifica == 0 else None
    
    _register_collaboraty_ = UserWidget(
        "Editar colaborador!",
        "Entre com os dados do colaborador abaixo",
        "Atualizar",
        "",
        type_collaboraty_ref,
        _update_collaboraty,
        back_button,
        open_weekday_dialog,
        colaborar_ref,
        user_ref
    )
    
    _register_collaboraty_main = _main_column_()
    _register_collaboraty_main.content.controls.append(flet.Container(padding=0))
    _register_collaboraty_main.content.controls.append(_register_collaboraty_)
    
    add_page(_register_collaboraty_main)

# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)
