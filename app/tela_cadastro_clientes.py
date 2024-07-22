import flet
from email_validator import validate_email, EmailNotValidError
from functools import partial

from . import login
from . import tela_menu_main
from . import register
from . import tela_login
from . import tela_transicao
from .config import COLOR_BORDER_COLOR_ERROR, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        sub_title:str,
        btn_name:str,
        erro:str,
        func,
        func2,
        ):
        self.title = title
        self._sub_title = sub_title
        self.btn_name = btn_name
        self.erro = erro
        self.func = func
        self.func2 = func2
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
                    size=12,
                    color=COLOR_TEXT_IN_FIELD,
                ),
                password=hide,
                can_reveal_password=hide,
            ),
        )
    
    def InputTextField2(self, text:str, width_field:int):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=width_field,
                keyboard_type="phone",
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
    
    def InputTextField3(self, text:str, width_field:int):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=275,
                keyboard_type="email",
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
            ),  # Alinha ao centro
            # padding=(padding.only(0)),
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
                        self.InputTextField3("E-mail",
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
                        self.InputTextField2("DDD (Ex:11)", 97.5),
                        self.InputTextField2("Telefone", 167.5),
                        ],
                ),
                self._checkbox_terms,
                flet.Container(padding=5),
                self._sign_in,
                self._back_button,
                flet.Container(padding=10),
                flet.Column(
                    horizontal_alignment="center",
                    controls=[
                        flet.Container(
                            content=flet.Text(
                                self.erro,
                                size=30,
                                color="black",
                            )
                        )
                    ],
                ),
            ],
        )

async def main(page: flet.Page):
    # Define o título da página
    page.title = "Cadastro"
    page.clean()

    # Função para redimensionar a página
    def page_resize(e=None, inicio=None):
        largura = min(page.width - 30, 600) if page.width <= 600 else 600
        altura = min(page.height - 60, 600) if page.height <= 600 else 600

        if e:
            _sign_in_main.width = largura
            _sign_in_main.height = altura
            _sign_in_main.update()

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
        page.add(flet.Row(alignment="center", spacing=0, controls=[extruct]))

    # Função assíncrona para voltar à página de login
    async def _back_button(e):
        await tela_login.main(page)

    # Função assíncrona para registrar o usuário
    async def _login_user(e):
        email = _sign_in_.controls[0].controls[2].controls[0].content
        senha = _sign_in_.controls[0].controls[2].controls[1].content
        nome = _sign_in_.controls[0].controls[2].controls[2].content
        ddd = _sign_in_.controls[0].controls[3].controls[0].content
        telefone = _sign_in_.controls[0].controls[3].controls[1].content
        checkbox_termos = _sign_in_._checkbox_terms.content.controls[0].controls[0].value

        if verifica_campos():
            telefone_completo = f'({ddd.value}){telefone.value.replace("-", "")}'
            cadastro = register.User(email.value, senha.value, nome.value, telefone_completo, checkbox_termos)
            cadastro.criar_usuario()

            if cadastro.uid:
                conta = login.User(email.value, senha.value)
                acesso = conta.login_firebase()

                if acesso == "email_not_verified":
                    texto = "E-mail de verificação enviado, verifique seu e-mail!"
                    await tela_transicao.main(page, None, texto, True)
                elif acesso:
                    await tela_menu_main.main(page, acesso)
            else:
                email.border_color = COLOR_BORDER_COLOR_ERROR
                email.value = "E-mail informado em uso"
                email.update()

    # Função para verificar os campos do formulário
    def verifica_campos():
        def is_valid_email(email):
            try:
                validate_email(email)  # Valida o email
                return True
            except EmailNotValidError as ex:
                print(str(ex))
                return False

        email = _sign_in_.controls[0].controls[2].controls[0].content
        senha = _sign_in_.controls[0].controls[2].controls[1].content
        nome = _sign_in_.controls[0].controls[2].controls[2].content
        ddd = _sign_in_.controls[0].controls[3].controls[0].content
        telefone = _sign_in_.controls[0].controls[3].controls[1].content
        checkbox_termos = _sign_in_._checkbox_terms.content.controls[0].controls[0]
        verifica = 0

        # Validação do campo de email
        if email.value == "":
            email.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        elif is_valid_email(email.value):
            email.border_color = COLOR_BORDER_COLOR
        else:
            email.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
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
            telefone.error_text = None
        telefone.update()

        # Validação do checkbox de termos
        if not checkbox_termos.value:
            checkbox_termos.is_error = True
            verifica += 1
        else:
            checkbox_termos.is_error = False
        checkbox_termos.update()

        return verifica == 0

    # Criação do widget de registro de usuário
    _sign_in_ = UserWidget(
        "Registrar-se!",
        "Entre com os dados da sua conta abaixo",
        "Registrar",
        "",
        _login_user,
        _back_button,
    )

    # Configuração do contêiner principal e adição do widget de registro
    _sign_in_main = _main_column_()
    _sign_in_main.content.controls.append(flet.Container(padding=0))
    _sign_in_main.content.controls.append(_sign_in_)

    add_page(_sign_in_main)

# Se necessário, adicione a chamada para a função principal conforme o seu framework/ambiente
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)
