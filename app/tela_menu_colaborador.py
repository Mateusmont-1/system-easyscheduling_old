import flet
from flet import *
from functools import partial

from . import tela_menu_main
from . import tela_cadastro_colaboradores
from . import tela_verificar_colaboradores
from . import tela_menu_folga
from .config import COLOR_BACKGROUND_CONTAINER, COLOR_BORDER_COLOR, COLOR_TEXT, COLOR_TEXT_BUTTON, COLOR_TEXT_IN_BUTTON, COLOR_BACKGROUND_BUTTON, COLOR_TEXT_IN_FIELD


class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        func,
        func2,
        func3,
        func4,
        user,
        ):
        self.title = title
        self.func = func
        self.func2 = func2
        self.func3 = func3
        self.func4 = func4
        self.user = user
        super().__init__()

        # Criando as variaveis para aparecer ou não o botão na interface
        self._visible_create_collaborator = False
        self._visible_edit_collaborator = False
        # Botão de retornar é visivel para todos os tipos de usuario
        self._visible_back_ = True
        
        # De acordo com o perfil do usuario define a visibilidade dos botões que ele possui acesso 
        # como True
        if self.user['funcaoID'] == "colaborador":
            ...
            
        elif self.user['funcaoID'] == "administrador":
            self._visible_create_collaborator = True
            self._visible_edit_collaborator = True
            
        else:
            ...
    
    def Create_button(self, text, func, visible=False):
        return flet.Container(
            visible=visible,
            content=flet.ElevatedButton(
                on_click=partial(func),  # Aqui você pode adicionar a função que será chamada quando o botão for clicado
                content=flet.Text(
                    text,
                    size=20,
                    weight="bold",
                ),
                style=flet.ButtonStyle(
                    shape={
                        "":flet.RoundedRectangleBorder(radius=8),
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
        
        self._create_collaborator = self.Create_button("Criar colaborador", self.func, self._visible_create_collaborator)
        self._edit_collaborator = self.Create_button("Editar colaborador", self.func2, self._visible_edit_collaborator)
        self._folga = self.Create_button("Folga", self.func3, self._visible_edit_collaborator)
        self._back = self.Create_button("Voltar", self.func4, self._visible_back_)

        return flet.Column(
            horizontal_alignment="center",
            controls=[
                self._title,
                flet.Container(padding=5),
                flet.Column(
                    alignment=flet.MainAxisAlignment.CENTER,
                    controls=[
                    flet.Row(
                        alignment="center",
                        controls=[self._create_collaborator]),
                    flet.Row(
                        alignment="center",
                        controls=[self._edit_collaborator]),
                    flet.Row(
                        alignment="center",
                        controls=[self._folga]),
                    flet.Row(
                        alignment="center",
                        controls=[self._back]),
                    ]),
                    
                flet.Container(padding=5),
            ],
        )

async def main(page:flet.page, user):
    # page.bgcolor = "#f0f3f6"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.theme_mode = "dark"
    page.clean()

    def page_resize(e=None, inicio=None):
        if e:
            if page.width > 600:     
                largura = 600
                _menu_main.width = largura
                _menu_main.update()
            else:
                largura = page.width - 30
                _menu_main.width = largura
                _menu_main.update()
            if page.height > 600:     
                altura = 600
                _menu_main.height = altura
                _menu_main.update()
            else:
                altura = page.height - 60
                _menu_main.height = altura
                _menu_main.update()

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

    async def _tela_create_collaborator(e):
        await tela_cadastro_colaboradores.main(page, user)
    
    async def _tela_verificar_colaboradores(e):
        await tela_verificar_colaboradores.main(page, user)

    async def _tela_menu_folga_button(e):
        await tela_menu_folga.main(page, user)
        
    async def _back_button(e):
        await tela_menu_main.main(page, user)
    
    _menu_ = UserWidget(
        "Colaborador!",
        _tela_create_collaborator,
        _tela_verificar_colaboradores,
        _tela_menu_folga_button,
        _back_button,
        user,
    )
    _menu_main = _main_column_()
    _menu_main.content.controls.append(flet.Container(padding=0))
    _menu_main.content.controls.append(_menu_)
    
    page.add(
        flet.Row(
            alignment="center",
            spacing=25,
            controls=[
                _menu_main,
            ]
        )
    )
    
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)
