import flet
from functools import partial
from email_validator import validate_email, EmailNotValidError
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
        func4,
        ):
        self.title = title
        self._sub_title = sub_title
        self.btn_name = btn_name
        self.erro = erro
        self.type_collaborator_ref = type_collaboraty
        self.func = func
        self.func2 = func2
        self.func3 = func3
        self.func4 = func4
        super().__init__()
    
    def InputTextField(self, text:str, hide:bool):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=275,
                # bgcolor="#f0f3f6",
                bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                content_padding=10,
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
                can_reveal_password=hide,
            ),
        )
    
    def InputTextField2(self, text:str, hide:bool):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=145,
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
    
    def InputTextField3(self, text:str, width_field:int):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=width_field,
                bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                text_size=12,
                color=COLOR_TEXT_IN_FIELD,
                border_color=COLOR_BORDER_COLOR,
                hint_text=text,
                filled=True,
                cursor_color=COLOR_TEXT,
                hint_style=flet.TextStyle(
                    size=12,
                    color=COLOR_TEXT_IN_FIELD,
                ),
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
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2)
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
        
        self._checkbox_collaborator = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Row(
                controls=[
                flet.Checkbox(on_change=partial(self.func2)),
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
            visible=False,
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
            visible=False,
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
            visible=False,
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
            visible=False,
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
                flet.Checkbox(),
                flet.Text(
                    value="Permitir agendamento?",
                    size=20,
                    weight="bold",
                    color=COLOR_TEXT_IN_FIELD),
                ],
            visible=False,
            alignment=flet.MainAxisAlignment.CENTER,
            ))
        
        self._checkbox_terms = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Column(
                controls=[
                    flet.Row(
                        controls=[
                            flet.Checkbox(),
                            flet.Text(
                                spans=[
                                    flet.TextSpan(
                                        "Ao aceitar você concorda com os ",
                                        flet.TextStyle(size=14, weight=flet.FontWeight.BOLD, color=COLOR_TEXT_IN_FIELD),
                                    ),
                                    flet.TextSpan(
                                        "Termos",
                                        flet.TextStyle(size=14, weight=flet.FontWeight.BOLD, color="blue", decoration=flet.TextDecoration.UNDERLINE),
                                        url="http://easyscheduling.com.br/termos-de-uso",
                                    ),
                                ],
                            ),
                        ],
                        alignment=flet.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    flet.Row(
                        controls=[
                            flet.Text(
                                spans=[
                                    flet.TextSpan(
                                        "de Uso",
                                        flet.TextStyle(size=14, weight=flet.FontWeight.BOLD, color="blue", decoration=flet.TextDecoration.UNDERLINE),
                                        url="http://easyscheduling.com.br/termos-de-uso",
                                    ),
                                    flet.TextSpan(
                                        " e a ",
                                        flet.TextStyle(size=14, weight=flet.FontWeight.BOLD, color=COLOR_TEXT_IN_FIELD),
                                    ),
                                    flet.TextSpan(
                                        "Política de Privacidade",
                                        flet.TextStyle(size=14, weight=flet.FontWeight.BOLD, color="blue", decoration=flet.TextDecoration.UNDERLINE),
                                        url="http://easyscheduling.com.br/politica-de-privacidade",
                                    ),
                                ],
                            ),
                        ],
                        alignment=flet.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                ],
                spacing=0,  
            ),
            visible=True,
        )

        self._weekdays_button = flet.Container(
            visible=False,
            content=flet.ElevatedButton(
                on_click=partial(self.func4),
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
            horizontal_alignment="center",
            controls=[
                self._title,
                self._sub_title,
                flet.Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("E-mail",
                                            False),
                        self.InputTextField("Senha",
                                            True),
                        self.InputTextField("Nome",
                                            False),
                    ],
                ),
                flet.Row(
                    alignment="center",
                    spacing=12,
                    visible=True,
                    controls=[
                        self.InputTextField3("DDD (Ex:11)", 97.5),
                        self.InputTextField3("Telefone", 167.5),
                        ],
                ),
                self._type_collaborator,
                self._checkbox_collaborator,
                self._text,
                self._text2,
                flet.Row(
                    alignment="center",
                    spacing=12,
                    visible=False,
                    controls=[
                        self.InputTextField2("Começa (h)",False),
                        self.InputTextField2("Termina (h)",False),
                        ],
                ),
                self._text3,
                flet.Row(
                    alignment="center",
                    spacing=12,
                    visible=False,
                    controls=[
                        self.InputTextField2("Começa (h)",False),
                        self.InputTextField2("Termina (h)",False),
                        ],
                ),
                self._text4,
                flet.Row(
                    alignment="center",
                    spacing=12,
                    visible=False,
                    controls=[
                        self.InputTextField2("Começa (h)",False),
                        self.InputTextField2("Termina (h)",False),
                        ],
                ),
                self._checkbox_schedulling,
                self._checkbox_terms,
                flet.Container(padding=5),
                self._weekdays_button,
                self._sign_in,
                self._back_button,
                
            ],
        )

async def main(page: flet.Page, user):
    # Define o título da página
    page.title = "Cadastro colaborador"
    page.clean()
    
    # Estado inicial dos dias da semana
    work_monday = True
    work_tuesday = True
    work_wednesday = True
    work_thursday= True
    work_friday = True
    work_saturday = True
    work_sunday = True

    # Obtém referência ao Firestore
    db = get_firestore_client()
    type_collaboraty_ref = db.collection("funcoes").stream()
    
    # Função para redimensionar a página
    def page_resize(e=None, inicio=None):
        largura = min(page.width - 30, 600) if page.width <= 600 else 600
        altura = min(page.height - 60, 600) if page.height <= 600 else 600

        if e:
            _register_collaboraty_main.width = largura
            _register_collaboraty_main.height = altura
            _register_collaboraty_main.update()

        if inicio is not None:
            return largura if inicio else altura

    # Associa a função de redimensionamento à janela
    page.window.on_resized = page_resize

    # Cria o contêiner principal da interface
    def _main_column_():
        return flet.Container(
            width=page_resize(inicio=True),
            height=page_resize(inicio=False),
            bgcolor=COLOR_BACKGROUND_CONTAINER,
            padding=12,
            border_radius=35,
            content=flet.Column(
                scroll="hidden",
                spacing=0,
                horizontal_alignment="center",
            )
        )

    # Função para adicionar um elemento à página
    def add_page(extruct):
        page.add(flet.Row(alignment="center", spacing=25, controls=[extruct]))

    # Função para abrir o diálogo de seleção dos dias da semana
    def open_weekday_dialog(e):
        weekdays_dialog = flet.AlertDialog(
            title=flet.Text("Selecione os Dias da Semana"),
            scrollable=True,
            content=flet.Column(
                controls=[
                    flet.Checkbox(label="Segunda-feira", value=work_monday, data="monday"),
                    flet.Checkbox(label="Terça-feira", value=work_tuesday, data="tuesday"),
                    flet.Checkbox(label="Quarta-feira", value=work_wednesday, data="wednesday"),
                    flet.Checkbox(label="Quinta-feira", value=work_thursday, data="thursday"),
                    flet.Checkbox(label="Sexta-feira", value=work_friday, data="friday"),
                    flet.Checkbox(label="Sábado", value=work_saturday, data="saturday"),
                    flet.Checkbox(label="Domingo", value=work_sunday, data="sunday"),
                ]
            ),
            actions=[flet.TextButton("OK", on_click=close_weekday_dialog)],
        )
        page.dialog = weekdays_dialog
        weekdays_dialog.open = True
        page.update()
    
    # Função para fechar o diálogo e atualizar o estado dos dias da semana
    def close_weekday_dialog(e):
        nonlocal work_monday, work_tuesday, work_wednesday, work_thursday, work_friday, work_saturday, work_sunday
        checkboxes = page.dialog.content.controls
        work_monday = checkboxes[0].value
        work_tuesday = checkboxes[1].value
        work_wednesday = checkboxes[2].value
        work_thursday = checkboxes[3].value
        work_friday = checkboxes[4].value
        work_saturday = checkboxes[5].value
        work_sunday = checkboxes[6].value
        page.dialog.open = False
        page.update()

    # Função assíncrona para registrar o colaborador
    async def _register_collaboraty(e):
        email, senha, nome, ddd, telefone, checkbox_termos, type_collaboraty, checkbox_create_collaborator, checkbox_scheduling, workday_start_time, workday_end_time, saturday_start_time, saturday_end_time, sunday_start_time, sunday_end_time = get_form_values()

        if verifica_campos():
            telefone_completo = f'({ddd}){telefone.replace("-", "")}'
            list_work_days = get_work_days()

            cadastro = create_collaborator(email, senha, nome, telefone_completo, checkbox_termos, type_collaboraty, checkbox_create_collaborator, list_work_days, checkbox_scheduling, workday_start_time, workday_end_time, saturday_start_time, saturday_end_time, sunday_start_time, sunday_end_time)
            
            if cadastro.uid:
                texto = "Colaborador cadastrado!"
                await tela_transicao.main(page, user, texto)
                print(f"Dias de trabalho selecionados: {list_work_days}")
            else:
                show_email_error(email)
        
    # Função para obter os valores do formulário
    def get_form_values():
        email = _register_collaboraty_.controls[0].controls[2].controls[0].content.value
        senha = _register_collaboraty_.controls[0].controls[2].controls[1].content.value
        nome = _register_collaboraty_.controls[0].controls[2].controls[2].content.value
        ddd = _register_collaboraty_.controls[0].controls[3].controls[0].content.value
        telefone = _register_collaboraty_.controls[0].controls[3].controls[1].content.value
        checkbox_termos = _register_collaboraty_._checkbox_terms.content.controls[0].controls[0].value
        type_collaboraty = _register_collaboraty_._type_collaborator.content.value
        checkbox_create_collaborator = _register_collaboraty_._checkbox_collaborator.content.controls[0].value
        checkbox_scheduling = _register_collaboraty_._checkbox_schedulling.content.controls[0].value
        workday_start_time = _register_collaboraty_.controls[0].controls[8].controls[0].content.value
        workday_end_time = _register_collaboraty_.controls[0].controls[8].controls[1].content.value
        saturday_start_time = _register_collaboraty_.controls[0].controls[10].controls[0].content.value
        saturday_end_time = _register_collaboraty_.controls[0].controls[10].controls[1].content.value
        sunday_start_time = _register_collaboraty_.controls[0].controls[12].controls[0].content.value
        sunday_end_time = _register_collaboraty_.controls[0].controls[12].controls[1].content.value
        
        return email, senha, nome, ddd, telefone, checkbox_termos, type_collaboraty, checkbox_create_collaborator, checkbox_scheduling, workday_start_time, workday_end_time, saturday_start_time, saturday_end_time, sunday_start_time, sunday_end_time

    # Função para criar o colaborador
    def create_collaborator(email, senha, nome, telefone_completo, checkbox_termos, type_collaboraty, checkbox_create_collaborator, list_work_days, checkbox_scheduling, workday_start_time, workday_end_time, saturday_start_time, saturday_end_time, sunday_start_time, sunday_end_time):
        cadastro = register.Collaborator(
            email, senha, nome, telefone_completo,
            checkbox_termos, type_collaboraty, checkbox_create_collaborator,
            list_work_days, checkbox_scheduling, workday_start_time, workday_end_time,
            saturday_start_time, saturday_end_time, sunday_start_time, sunday_end_time
        )
        cadastro.criar_colaborador()
        return cadastro

    # Função para obter os dias de trabalho
    def get_work_days():
        work_days = []
        if work_monday:
            work_days.append(0)
        if work_tuesday:
            work_days.append(1)
        if work_wednesday:
            work_days.append(2)
        if work_thursday:
            work_days.append(3)
        if work_friday:
            work_days.append(4)
        if work_saturday:
            work_days.append(5)
        if work_sunday:
            work_days.append(6)
        return work_days

    # Função para mostrar erro no campo de email
    def show_email_error(email):
        email_input = _register_collaboraty_.controls[0].controls[2].controls[0].content
        email_input.border_color = COLOR_BORDER_COLOR_ERROR
        email_input.value = "E-mail informado em uso"
        email_input.update()
            
    # Função para verificar os campos do formulário
    def verifica_campos():
        def is_valid_email(email):
            try:
                validate_email(email)  # Valida o email
                return True
            except EmailNotValidError as ex:
                print(str(ex))
                return False
        
        # Expressão regular para validar o formato "HH:MM"
        time_format_regex = re.compile(r'^\d{2}:\d{2}$')

        # Função para validar um campo de horário
        def validate_time_field(time_field):
            if time_field.value == "" or not time_format_regex.match(time_field.value):
                time_field.border_color = COLOR_BORDER_COLOR_ERROR
                time_field.update()
                return 1
            time_field.border_color = COLOR_BORDER_COLOR
            time_field.update()
            return 0

        # Obtém os valores dos campos do formulário
        email = _register_collaboraty_.controls[0].controls[2].controls[0].content
        senha = _register_collaboraty_.controls[0].controls[2].controls[1].content
        nome = _register_collaboraty_.controls[0].controls[2].controls[2].content
        ddd = _register_collaboraty_.controls[0].controls[3].controls[0].content
        telefone = _register_collaboraty_.controls[0].controls[3].controls[1].content
        type_collaboraty = _register_collaboraty_._type_collaborator.content
        checkbox_create_collaborator = _register_collaboraty_._checkbox_collaborator.content.controls[0].value
        checkbox_termos = _register_collaboraty_._checkbox_terms.content.controls[0].controls[0]

        verifica = 0
        # Validação do campo de email
        if email.value == "" or not is_valid_email(email.value):
            email.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        else:
            email.border_color = COLOR_BORDER_COLOR
        email.update()

        # Validação do campo de senha
        if senha.value == "" or len(senha.value) < 6:
            senha.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        else:
            senha.border_color = COLOR_BORDER_COLOR
        senha.update()

        # Validação do campo de nome
        if nome.value == "":
            nome.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        else:
            nome.border_color = COLOR_BORDER_COLOR
        nome.update()

        # Validação do campo de DDD
        if ddd.value == "" or len(ddd.value) != 2:
            ddd.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        else:
            ddd.border_color = COLOR_BORDER_COLOR
        ddd.update()

        # Validação do campo de telefone
        telefone_value = telefone.value.replace('-', "")
        if telefone.value == "" or len(telefone_value) < 8 or len(telefone_value) > 9:
            telefone.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        else:
            telefone.border_color = COLOR_BORDER_COLOR
        telefone.update()

        # Validação do tipo de colaborador
        if type_collaboraty.value is None:
            type_collaboraty.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        else:
            type_collaboraty.border_color = COLOR_BORDER_COLOR
        type_collaboraty.update()

        # Validação do checkbox de termos
        if not checkbox_termos.value:
            checkbox_termos.is_error = True
            verifica += 1
        else:
            checkbox_termos.is_error = False
        checkbox_termos.update()

        # Verifica se a opção de criar atendente no sistema está ativa
        if checkbox_create_collaborator:
            # Obtém referências aos campos de horário
            workday_start_time = _register_collaboraty_.controls[0].controls[8].controls[0].content
            workday_end_time = _register_collaboraty_.controls[0].controls[8].controls[1].content
            saturday_start_time = _register_collaboraty_.controls[0].controls[10].controls[0].content
            saturday_end_time = _register_collaboraty_.controls[0].controls[10].controls[1].content
            sunday_start_time = _register_collaboraty_.controls[0].controls[12].controls[0].content
            sunday_end_time = _register_collaboraty_.controls[0].controls[12].controls[1].content

            verifica += validate_time_field(workday_start_time)
            verifica += validate_time_field(workday_end_time)
            verifica += validate_time_field(saturday_start_time)
            verifica += validate_time_field(saturday_end_time)
            verifica += validate_time_field(sunday_start_time)
            verifica += validate_time_field(sunday_end_time)
        
        return verifica == 0

    # Função para checar se o colaborador pode ser criado
    def check_create_collaborator(e):
        type_collaboraty = _register_collaboraty_._type_collaborator.content
        checkbox_create_collaborator = _register_collaboraty_._checkbox_collaborator.content
        checkbox_scheduling = _register_collaboraty_._checkbox_schedulling.content
        
        text_time = _register_collaboraty_._text
        text_time2 = _register_collaboraty_._text2
        text_time3 = _register_collaboraty_._text3
        text_time4 = _register_collaboraty_._text4
        row_segunda_sexta = _register_collaboraty_.controls[0].controls[8]
        row_sabado = _register_collaboraty_.controls[0].controls[10]
        row_domingo = _register_collaboraty_.controls[0].controls[12]
        work_day = _register_collaboraty_.controls[0].controls[16]
        
        if type_collaboraty.value == "administrador":
            checkbox_create_collaborator.visible = True
            checkbox_create_collaborator.update()
        else:
            checkbox_create_collaborator.visible = False
            checkbox_create_collaborator.controls[0].value = True
            checkbox_create_collaborator.update()
        
        elements = [
            checkbox_scheduling, text_time, text_time2, text_time3, text_time4,
            row_segunda_sexta, row_sabado, row_domingo, work_day
        ]
        visible = checkbox_create_collaborator.controls[0].value
        
        for element in elements:
            element.visible = visible
            element.update()

        
    # Função assíncrona para voltar à página principal
    async def _back_button(e):
        await tela_menu_main.main(page, user)
    
    # Cria o widget de registro de colaborador
    _register_collaboraty_ = UserWidget(
        "Registrar colaborador!",
        "Entre com os dados do colaborador abaixo",
        "Registrar",
        "",
        type_collaboraty_ref,
        _register_collaboraty,
        check_create_collaborator,
        _back_button,
        open_weekday_dialog,
    )

    # Configura o contêiner principal e adiciona o widget de registro
    _register_collaboraty_main = _main_column_()
    _register_collaboraty_main.content.controls.append(flet.Container(padding=0))
    _register_collaboraty_main.content.controls.append(_register_collaboraty_)

    add_page(_register_collaboraty_main)

# Se necessário, adicione a chamada para a função principal conforme o seu framework/ambiente
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER) 