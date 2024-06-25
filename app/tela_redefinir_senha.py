# Implementação que eu realizei antes para tela_logyn.py

import flet
from functools import partial
from email_validator import validate_email, EmailNotValidError


from . import login
from . import tela_login
from . import tela_transicao
from .config import COLOR_BORDER_COLOR_ERROR, COLOR_BACKGROUND_CONTAINER, COLOR_BORDER_COLOR, COLOR_TEXT, COLOR_TEXT_BUTTON, COLOR_TEXT_IN_BUTTON, COLOR_BACKGROUND_BUTTON, COLOR_TEXT_IN_FIELD, COLOR_BACKGROUND_TEXT_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        image,
        title:str,
        sub_title:str,
        btn_name:str,
        func1,
        func2,
        ):
        self.image = image
        self.title = title
        self._sub_title = sub_title
        self.btn_name = btn_name
        self.func = func1
        self.func2 = func2

        super().__init__()
    
    def InputTextField(self, text:str, hide:bool):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=275,
                # bgcolor="#f0f3f6",
                # bgcolor="#F7F7F7",
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
            ),
        )
        
    def SignInOption(self):
        return flet.Container(
            content=flet.ElevatedButton
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
            # clip_behavior=flet.ClipBehavior.ANTI_ALIAS,
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
                # weight="bold",
                color=COLOR_TEXT,
                size=25
            ),
        )
        
        self._forgot_password = flet.Container(
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
                color=COLOR_TEXT_IN_BUTTON,
                bgcolor=COLOR_BACKGROUND_BUTTON,
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

        # Rodapé "Desenvolvido por Mateus Monteiro"
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
                        self.InputTextField("E-mail",
                                            False),
                    ],
                ),
                flet.Container(padding=5),
                self._forgot_password,
                self._back_button,
                flet.Container(padding=35),
                self._footer,
            ],
        )

async def main(page:flet.page):
    page.clean()

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
                spacing=0,
                controls=[
                extruct,
                ]
            )
        )

    async def _redefinir_senha(e):
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
    
        email = _sign_in_.controls[0].controls[3].controls[0].content
        
        verifica = 0
        if email.value == "":
            email.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        elif is_valid_email(email.value):
            email.border_color = COLOR_BORDER_COLOR
        else:
            email.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1 

        email.update()

        if verifica == 0:
            conta = login.ForgetPassword(email.value)
            redefinir = conta.redefine_password()
            if redefinir:
                texto = "E-mail para redefinir senha enviado"
                await tela_transicao.main(page, None, texto, True)
            else:
                email.border_color = COLOR_BORDER_COLOR_ERROR
                email.update()
                # Muda a cor do campo de e-mail indicando erro

    async def _back_button(e):
        await tela_login.main(page)

    _sign_in_ = UserWidget(
        image_logo,
        "Redefinir senha",
        "Entre com os dados da sua conta abaixo",
        "Redefinir",
        _redefinir_senha,
        _back_button,
    )
    
    _sign_in_main = _main_column_()
    _sign_in_main.content.controls.append(flet.Container(padding=0))
    _sign_in_main.content.controls.append(_sign_in_)
    
    add_page(_sign_in_main)
   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)
