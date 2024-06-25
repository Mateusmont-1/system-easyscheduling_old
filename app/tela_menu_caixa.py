import flet
from flet import *
from functools import partial

from . import tela_menu_main
from . import tela_finalizar_atendimento
from . import tela_cadastro_despesa
from . import tela_menu_despesa
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
        self._visible_create_service = False
        self._visible_create_expenses = False
        self._visible_expenses = False
        # Botão de retornar é visivel para todos os tipos de usuario
        self._visible_back_ = True
        
        # De acordo com o perfil do usuario define a visibilidade dos botões que ele possui acesso 
        # como True
        if self.user['funcaoID'] == "colaborador":
            self._visible_create_service = True
            
        elif self.user['funcaoID'] == "administrador":
            self._visible_create_service = True
            self._visible_create_expenses = True
            self._visible_expenses = True
            
        else:
            ...
    
    def Create_button(self, text, func, visible_button=False):
        return flet.Container(
            visible=visible_button,
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
        
        self._create_service = self.Create_button("Adicionar atendimento", self.func, self._visible_create_service)
        self._create_expenses = self.Create_button("Adicionar despesas", self.func2, self._visible_create_expenses)
        self._expenses = self.Create_button("Despesas", self.func3, self._visible_expenses)
        self._back_ = self.Create_button("Voltar", self.func4, self._visible_back_)
        
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
                        controls=[self._create_service]),
                    flet.Row(
                        alignment="center",
                        controls=[self._create_expenses]),
                    flet.Row(
                        alignment="center",
                        controls=[self._expenses]),
                    flet.Row(
                        alignment="center", 
                        controls=[self._back_]),
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

    async def _create_servico(e):
        await tela_finalizar_atendimento.main(page,user)
        # tela_cadastro_servico.main(page, user)
        
    async def _create_expenses(e):
        await tela_cadastro_despesa.main(page, user)
    
    async def _expenser(e):
        await tela_menu_despesa.main(page, user)
    
    async def _back_button(e):
        await tela_menu_main.main(page,user)
    
    _menu_ = UserWidget(
        "Caixa!",
        _create_servico,
        _create_expenses,
        _expenser,
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
