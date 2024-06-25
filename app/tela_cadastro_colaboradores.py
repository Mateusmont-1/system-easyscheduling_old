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
        ):
        self.title = title
        self._sub_title = sub_title
        self.btn_name = btn_name
        self.erro = erro
        self.type_collaborator_ref = type_collaboraty
        self.func = func
        self.func2 = func2
        self.func3 = func3
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
                spacing=0,  # Ajuste o espaçamento entre os elementos
            ),
            visible=True,
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
                self._sign_in,
                self._back_button,
            ],
        )

async def main(page:flet.page, user):
    page.title = "Cadastro colaborador"
    # page.bgcolor = "#f0f3f6"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.theme_mode = "dark"

    page.clean()
    
    db = get_firestore_client()
    type_collaboraty_ref = db.collection("funcoes").stream()
    
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

    async def _register_collaboraty(e):
        # Obtendo email, senha, nome, telefone, informado na interface
        email = _register_collaboraty_.controls[0].controls[2].controls[0].content.value
        senha = _register_collaboraty_.controls[0].controls[2].controls[1].content.value
        nome = _register_collaboraty_.controls[0].controls[2].controls[2].content.value
        ddd = _register_collaboraty_.controls[0].controls[3].controls[0].content.value
        telefone = _register_collaboraty_.controls[0].controls[3].controls[1].content.value
        checkbox_termos = _register_collaboraty_._checkbox_terms.content.controls[0].controls[0].value
        # Obtendo o tipo de colaborador
        type_collaboraty = _register_collaboraty_._type_collaborator.content.value
        # Verificação se é para cadastrar como atendente ou somente administrador
        checkbox_create_collaborator = _register_collaboraty_._checkbox_collaborator.content.controls[0].value
        # Verificação se é para permitir agendamento com o atendente
        checkbox_scheduling = _register_collaboraty_._checkbox_schedulling.content.controls[0].value
        # Se todos os campos foram preenchidos executa cadastro no sistema
        if verifica_campos():
            # Unificando DDD com telefone
            telefone_completo = f'({ddd}){telefone.replace("-", "")}'
            # Obtendo os valores de horário de funcionamento
            workday_start_time = _register_collaboraty_.controls[0].controls[8].controls[0].content.value
            workday_end_time = _register_collaboraty_.controls[0].controls[8].controls[1].content.value
            saturday_start_time = _register_collaboraty_.controls[0].controls[10].controls[0].content.value
            saturday_end_time = _register_collaboraty_.controls[0].controls[10].controls[1].content.value
            sunday_start_time = _register_collaboraty_.controls[0].controls[12].controls[0].content.value
            sunday_end_time = _register_collaboraty_.controls[0].controls[12].controls[1].content.value
            cadastro = register.Collaborator(email, senha, 
                                             nome, telefone_completo,
                                             checkbox_termos, 
                                             type_collaboraty, checkbox_create_collaborator,
                                             checkbox_scheduling, workday_start_time,
                                             workday_end_time, saturday_start_time,
                                             saturday_end_time, sunday_start_time,
                                             sunday_end_time)
            cadastro.criar_colaborador()
            if cadastro.uid:
                texto = "Colaborador cadastrado!"
                await tela_transicao.main(page, user, texto)
            else:
                email = _register_collaboraty_.controls[0].controls[2].controls[0].content
                email.border_color = COLOR_BORDER_COLOR_ERROR
                email.value = "E-mail informado em uso"
                email.update()
            
    def verifica_campos():

        def is_valid_email(email):
            try:
                # Valida o email e retorna as informações normalizadas
                valid = validate_email(email)
                email = valid.email
                return True
            except EmailNotValidError as ex:
                # O email não é válido, trate o erro aqui
                print(str(ex))
                return False
        
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

        # Obtendo email, senha, nome, telefone, informado na interface
        email = _register_collaboraty_.controls[0].controls[2].controls[0].content
        senha = _register_collaboraty_.controls[0].controls[2].controls[1].content
        nome = _register_collaboraty_.controls[0].controls[2].controls[2].content
        ddd = _register_collaboraty_.controls[0].controls[3].controls[0].content
        telefone = _register_collaboraty_.controls[0].controls[3].controls[1].content
        # Obtendo o tipo de colaborador
        type_collaboraty = _register_collaboraty_._type_collaborator.content
        # Verificação se é para cadastrar como atendente ou somente administrador
        checkbox_create_collaborator = _register_collaboraty_._checkbox_collaborator.content.controls[0].value
        # Verificação se é para permitir agendamento com o atendente
        checkbox_termos = _register_collaboraty_._checkbox_terms.content.controls[0].controls[0]
        # Verificação se os termos de uso foram aceitos
        verifica = 0
        if email.value == "":
            email.border_color = COLOR_BORDER_COLOR_ERROR
            email.update()
            verifica += 1
        elif is_valid_email(email.value):
            email.border_color = COLOR_BORDER_COLOR_ERROR
            email.update()
        else:
            email.border_color = COLOR_BORDER_COLOR
            email.update()
            verifica += 1
        if senha.value == "":
            senha.border_color = COLOR_BORDER_COLOR_ERROR
            senha.update()
            verifica += 1
        elif len(senha.value) < 6:
            senha.border_color = '#FF0000'
            senha.update()
            verifica += 1
        else:
            senha.border_color = COLOR_BORDER_COLOR
            senha.update()
        if nome.value == "":
            nome.border_color = COLOR_BORDER_COLOR_ERROR
            nome.update()
            verifica += 1
        else:
            nome.border_color = COLOR_BORDER_COLOR
            nome.update()
        if ddd.value == "":
            ddd.border_color = COLOR_BORDER_COLOR_ERROR
            ddd.update()
            verifica += 1
        elif len(ddd.value) != 2:
            ddd.border_color = COLOR_BORDER_COLOR_ERROR
            ddd.update()
            verifica += 1
        else:
            ddd.border_color = COLOR_BORDER_COLOR
            ddd.update()
        if telefone.value == "":
            telefone.border_color = COLOR_BORDER_COLOR_ERROR
            telefone.update()
            verifica += 1
        elif len(telefone.value.replace('-', "")) < 8 or len(telefone.value.replace('-', "")) > 9:
            telefone.border_color = COLOR_BORDER_COLOR_ERROR
            telefone.update()
            verifica += 1
        else:
            telefone.border_color = COLOR_BORDER_COLOR
            telefone.error_text = None
            telefone.update()
        if type_collaboraty.value == None:
            type_collaboraty.border_color = COLOR_BORDER_COLOR_ERROR
            type_collaboraty.update()
            verifica +=1
        else:
            type_collaboraty.border_color = COLOR_BORDER_COLOR
            type_collaboraty.update()

        if not checkbox_termos.value:
            checkbox_termos.is_error = True
            verifica += 1
            checkbox_termos.update()
        else:
            checkbox_termos.is_error = False
            checkbox_termos.update()
        # Verifica se a opção de criar atendente no sistema está ativa
        if checkbox_create_collaborator == True:
            # Se estiver ativo possui mais campos de prenchimentos obrigatorios
            # Obtendo referencia aos campos que devem ser preenchidos
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
            
            # # Verificação se os hórarios estão preenchidos
            # if workday_start_time.value == "":
            #     workday_start_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     workday_start_time.update()
            #     verifica += 1
            # # Verifica se o valor presente não é um digito
            # elif not workday_start_time.value.isdigit():
            #     workday_start_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     workday_start_time.update()
            #     verifica += 1
            # else:
            #     workday_start_time.border_color = COLOR_BORDER_COLOR
            #     workday_start_time.update()
                
            # if workday_end_time.value == "":
            #     workday_end_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     workday_end_time.update()
            #     verifica += 1
            # elif not workday_end_time.value.isdigit():
            #     workday_end_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     workday_end_time.update()
            #     verifica += 1
            # else:
            #     workday_end_time.border_color = COLOR_BORDER_COLOR
            #     workday_end_time.update()

            # if saturday_start_time.value == "":
            #     saturday_start_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     saturday_start_time.update()
            #     verifica += 1
            # elif not saturday_start_time.value.isdigit():
            #     saturday_start_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     saturday_start_time.update()
            #     verifica += 1
            # else:
            #     saturday_start_time.border_color = COLOR_BORDER_COLOR
            #     saturday_start_time.update()

            # if saturday_end_time.value == "":
            #     saturday_end_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     saturday_end_time.update()
            #     verifica += 1
            # elif not saturday_end_time.value.isdigit():
            #     saturday_end_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     saturday_end_time.update()
            #     verifica += 1
            # else:
            #     saturday_end_time.border_color = COLOR_BORDER_COLOR
            #     saturday_end_time.update()

            # if sunday_start_time.value == "":
            #     sunday_start_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     sunday_start_time.update()
            #     verifica += 1
            # elif not sunday_start_time.value.isdigit():
            #     sunday_start_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     sunday_start_time.update()
            #     verifica += 1
            # else:
            #     sunday_start_time.border_color = COLOR_BORDER_COLOR
            #     sunday_start_time.update()
            
            # if sunday_end_time.value == "":
            #     sunday_end_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     sunday_end_time.update()
            #     verifica += 1
            # elif not sunday_end_time.value.isdigit():
            #     sunday_end_time.border_color = COLOR_BORDER_COLOR_ERROR
            #     sunday_end_time.update()
            #     verifica += 1
            # else:
            #     sunday_end_time.border_color = COLOR_BORDER_COLOR
            #     sunday_end_time.update()
        
        return True if verifica == 0 else None

    def check_create_collaborator(e):
        type_collaboraty = _register_collaboraty_._type_collaborator.content
        checkbox_create_collaborator = _register_collaboraty_._checkbox_collaborator.content
        checkbox_sheduling = _register_collaboraty_._checkbox_schedulling.content
        
        text_time = _register_collaboraty_._text
        text_time2 = _register_collaboraty_._text2
        text_time3 = _register_collaboraty_._text3
        text_time4 = _register_collaboraty_._text4
        row_segunda_sexta = _register_collaboraty_.controls[0].controls[8]
        row_sabado = _register_collaboraty_.controls[0].controls[10]
        row_domingo = _register_collaboraty_.controls[0].controls[12]
        # email = _sign_in_.controls[0].controls[3].controls[0].content
        
        if type_collaboraty.value == "administrador":
            checkbox_create_collaborator.visible = True
            checkbox_create_collaborator.update()
            
        else:
            checkbox_create_collaborator.visible = False
            checkbox_create_collaborator.controls[0].value = True
            checkbox_create_collaborator.update()
            
        if checkbox_create_collaborator.controls[0].value == True:
            checkbox_sheduling.visible = True
            text_time.visible = True
            text_time2.visible = True
            text_time3.visible = True
            text_time4.visible = True
            row_segunda_sexta.visible = True
            row_sabado.visible = True
            row_domingo.visible = True
            checkbox_sheduling.update()
            text_time.update()
            text_time2.update()
            text_time3.update()
            text_time4.update()
            row_segunda_sexta.update()
            row_sabado.update()
            row_domingo.update()
            
        else:
            checkbox_sheduling.visible = False
            text_time.visible = False
            text_time2.visible = False
            text_time3.visible = False
            text_time4.visible = False
            row_segunda_sexta.visible = False
            row_sabado.visible = False
            row_domingo.visible = False
            checkbox_sheduling.update()
            text_time.update()
            text_time2.update()
            text_time3.update()
            text_time4.update()
            row_segunda_sexta.update()
            row_sabado.update()
            row_domingo.update()

        # _register_collaboraty_._type_collaborator.content
    
    async def _back_button(e):
        await tela_menu_main.main(page,user)
    
    _register_collaboraty_ = UserWidget(
        "Registrar colaborador!",
        "Entre com os dados do colaborador abaixo",
        "Registrar",
        "",
        type_collaboraty_ref,
        _register_collaboraty,
        check_create_collaborator,
        _back_button,
    )
    
    _register_collaboraty_main = _main_column_()
    _register_collaboraty_main.content.controls.append(flet.Container(padding=0))
    _register_collaboraty_main.content.controls.append(_register_collaboraty_)
    
    add_page(_register_collaboraty_main)

# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER) 