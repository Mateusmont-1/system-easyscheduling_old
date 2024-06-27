import flet
from functools import partial
from email_validator import validate_email, EmailNotValidError

from . import login
from . import tela_menu_main
from . import tela_cadastro_clientes
from . import tela_redefinir_senha
from . import tela_transicao
from .config import (
    COLOR_BORDER_COLOR_ERROR, COLOR_BACKGROUND_CONTAINER, COLOR_BORDER_COLOR, COLOR_TEXT,
    COLOR_TEXT_BUTTON, COLOR_TEXT_IN_BUTTON, COLOR_BACKGROUND_BUTTON, COLOR_TEXT_IN_FIELD,
    COLOR_BACKGROUND_TEXT_FIELD
)

class UserWidget(flet.UserControl):
    def __init__(
        self,
        image,
        title: str,
        sub_title: str,
        btn_name: str,
        text: str,
        func1,
        func2,
        func3,
        stored_email: str = ""
    ):
        super().__init__()
        self.image = image
        self.title = title
        self._sub_title = sub_title
        self.btn_name = btn_name
        self.text = text
        self.func = func1
        self.func2 = func2
        self.func3 = func3
        self.stored_email = stored_email

    def InputTextField(self, text: str, hide: bool, default_value: str = ""):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=275,
                keyboard_type="email",
                value=default_value,
                bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                content_padding=10,
                on_submit=partial(self.func),
                text_size=16,
                color=COLOR_TEXT_IN_FIELD,
                border_color=COLOR_BORDER_COLOR,
                hint_text=text,
                filled=True,
                cursor_color=COLOR_TEXT,
                hint_style=flet.TextStyle(
                    size=18,
                    color=COLOR_TEXT_IN_FIELD,
                ),
                password=hide,
                can_reveal_password=hide,
            ),
        )

    def build(self):
        self._image_logo = flet.Container(
            content=flet.Image(
                src=self.image,
                width=150,  # Defina o tamanho desejado
                height=150,  # Defina o tamanho desejado
                fit=flet.ImageFit.COVER,
            ),
            width=150,
            height=150,
            border_radius=flet.border_radius.all(75),  # Torna a borda arredondada
        )

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

        self.remember_me_checkbox = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Row(
                controls=[
                flet.Checkbox(label="Lembrar-se", value=bool(self.stored_email))
                ],
            alignment=flet.MainAxisAlignment.CENTER,
            ))

        # self.remember_me_checkbox = flet.Checkbox(label="Lembrar-se", value=bool(self.stored_email))

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
                        "": flet.RoundedRectangleBorder(radius=8),
                    },
                    color={
                        "": "white",
                    }
                ),
                color=COLOR_TEXT_IN_BUTTON,
                bgcolor=COLOR_BACKGROUND_BUTTON,
                height=48,
                width=275,
            )
        )

        self.forgot_password = flet.TextButton(
            content=flet.Text(
                "Esqueceu a senha?",
                size=15,
                color=COLOR_TEXT_IN_FIELD,
            ),
            on_click=partial(self.func3),
        )

        self._footer = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Text(
                "Desenvolvido por Mateus Monteiro",
                size=12,
                weight=flet.FontWeight.W_400,
                color=COLOR_TEXT,
                text_align=flet.TextAlign.CENTER
            ),
        )

        return flet.Column(
            horizontal_alignment="center",
            controls=[
                self._image_logo,
                self._title,
                self._sub_title,
                flet.Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("E-mail", False, self.stored_email),
                        self.InputTextField("Senha", True),
                    ],
                ),
                self.remember_me_checkbox,
                flet.Container(padding=2),
                self._sign_in,
                flet.Row(
                    alignment=flet.MainAxisAlignment.CENTER,
                    controls=[
                        flet.Container(
                            content=flet.Text(
                                self.text,
                                size=15,
                                color="#C0C0C0",
                            )
                        ),
                        flet.TextButton(
                            content=flet.Text(
                                "cadastrar-se",
                                size=15,
                                color=COLOR_TEXT_IN_FIELD,
                            ),
                            on_click=partial(self.func2),
                        )
                    ],
                ),
                self.forgot_password,
                flet.Container(padding=1),
                self._footer,
            ],
        )


async def main(page: flet.Page):
    page.clean()
    
    # Adicione uma função para carregar o email armazenado
    async def load_stored_email():
        stored_email = await page.client_storage.get_async("email")
        return stored_email

    image_logo = "icon.png"

    def page_resize(e=None, inicio=None):
        if e:
            if page.width > 600:
                largura = 600
                _sign_in_main.width = largura
                _sign_in_main.update()
            else:
                largura = page.width - 30
                _sign_in_main.width = largura
                _sign_in_main.update()
            if page.height > 600:
                altura = 600
                _sign_in_main.height = altura
                _sign_in_main.update()
            else:
                altura = page.height - 60
                _sign_in_main.height = altura
                _sign_in_main.update()

        if inicio:
            if page.width > 600:
                largura = 600
                return largura
            else:
                largura = page.width - 30
                return largura

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
                spacing=0,
                controls=[
                    extruct,
                ]
            )
        )

    async def _login_user(e):
        email = _sign_in_.controls[0].controls[3].controls[0].content
        senha = _sign_in_.controls[0].controls[3].controls[1].content
        remember_me = _sign_in_.remember_me_checkbox.content.controls[0].value
        if remember_me:
            # Armazenar o e-mail no armazenamento local
            await page.client_storage.set_async("email", email.value)
        else:
            # Remover o e-mail armazenado se o checkbox não estiver marcado
            await page.client_storage.remove_async("email")
        
        page.update()

        if verifica_campos():
            conta = login.User(email.value, senha.value)
            acesso = conta.login_firebase()
            if acesso == "email_not_found":
                email.border_color = COLOR_BORDER_COLOR_ERROR
                email.update()
            elif acesso == "incorrect_password":
                senha.border_color = COLOR_BORDER_COLOR_ERROR
                senha.update()
            elif acesso == "email_not_verified":
                texto = "E-mail de verificação enviado, verifique seu e-mail!"
                await tela_transicao.main(page, None, texto, True)
            elif acesso:
                await tela_menu_main.main(page, acesso)

    def verifica_campos():
        def is_valid_email(email):
            try:
                valid = validate_email(email)
                email = valid.email
                return True
            except EmailNotValidError as ex:
                print(str(ex))
                return False

        email = _sign_in_.controls[0].controls[3].controls[0].content
        senha = _sign_in_.controls[0].controls[3].controls[1].content
        verifica = 0
        if email.value == "":
            email.border_color = COLOR_BORDER_COLOR_ERROR
            email.update()
            verifica += 1
        elif is_valid_email(email.value):
            email.border_color = COLOR_BORDER_COLOR
            email.update()
        else:
            email.border_color = COLOR_BORDER_COLOR_ERROR
            email.update()
            verifica += 1
        if senha.value == "":
            senha.border_color = COLOR_BORDER_COLOR_ERROR
            senha.update()
            verifica += 1
        elif len(senha.value) < 6:
            senha.border_color = COLOR_BORDER_COLOR_ERROR
            senha.update()
            verifica += 1
        else:
            senha.border_color = COLOR_BORDER_COLOR
            senha.update()

        return True if verifica == 0 else False
    
    async def _register_user(e):
        await tela_cadastro_clientes.main(page)

    async def _forgot_password(e):
        await tela_redefinir_senha.main(page)

    # Carregar o email armazenado e criar a instância de UserWidget
    stored_email = await load_stored_email()

    _sign_in_ = UserWidget(
        image_logo,
        "Bem vindo!",
        "Entre com os dados da sua conta abaixo",
        "Entrar",
        "Não tem uma conta?",
        _login_user,
        _register_user,
        _forgot_password,
        stored_email,
    )

    _sign_in_main = _main_column_()
    _sign_in_main.content.controls.append(flet.Container(padding=0))
    _sign_in_main.content.controls.append(_sign_in_)

    add_page(_sign_in_main)
