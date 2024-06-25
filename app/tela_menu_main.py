import flet
from functools import partial
import webbrowser

from . import tela_menu_relatorio
from . import tela_menu_agendamento
from . import tela_menu_service
from . import tela_menu_product
from . import tela_menu_colaborador
from . import tela_menu_caixa
from . import tela_login
from .config import URL_MAPS ,COLOR_BACKGROUND_CONTAINER, COLOR_BORDER_COLOR, COLOR_TEXT, COLOR_TEXT_BUTTON, COLOR_TEXT_IN_BUTTON, COLOR_BACKGROUND_BUTTON, COLOR_TEXT_IN_FIELD


class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        func,
        func2,
        func3,
        func4,
        func5,
        func6,
        func7,
        user,
        ):
        self.title = title
        self.func = func
        self.func2 = func2
        self.func3 = func3
        self.func4 = func4
        self.func5 = func5
        self.func6 = func6
        self.func7 = func7
        self.user = user
        super().__init__()

        # Criando as variaveis para aparecer ou não o botão na interface
        self._visible_scheduling_ = False
        self._visible_service_ = False
        self._visible_product_ = False
        self._visible_barber_ = False
        self._visible_report_ = False
        self._visible_caixa_ = False
        # Botão de logout e endereço é visivel para todos os tipos de usuario
        self._visible_address_ = True
        self._visible_log_out_ = True
        
        # De acordo com o perfil do usuario define a visibilidade dos botões que ele possui acesso 
        # como True
        if self.user['funcaoID'] == "colaborador":
            self._visible_scheduling_ = True
            self._visible_report_ = True
            self._visible_caixa_ = True
            
        elif self.user['funcaoID'] == "administrador":
            self._visible_scheduling_ = True
            self._visible_service_ = True
            self._visible_product_ = True
            self._visible_barber_ = True
            self._visible_report_ = True
            self._visible_caixa_ = True
        else:
            self._visible_scheduling_ = True
        
        
    def SignInOption(self):
        return flet.Container(
            content=flet.ElevatedButton
        )
    
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

    def Create_button_url(self, text, visible=False, url_text=None):
        return flet.Container(
            visible=visible,
            content=flet.ElevatedButton(
                url=url_text,
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

        self._scheduling_ = self.Create_button("Agendamento", self.func, self._visible_scheduling_)
        self._service_ = self.Create_button("Serviço", self.func2, self._visible_service_)
        self._product_ = self.Create_button("Produto", self.func3, self._visible_product_)
        self._barber_ = self.Create_button("Colaborador", self.func4, self._visible_barber_)
        self._report_ = self.Create_button("Relátorio", self.func5, self._visible_report_)
        self._caixa_ = self.Create_button("Caixa", self.func6, self._visible_caixa_)
        self._address_ = self.Create_button_url("Endereço", self._visible_address_, URL_MAPS)
        self._log_out_ = self.Create_button("Deslogar", self.func7, self._visible_log_out_)
        
        if self.user['funcaoID'] == "cliente":
            return flet.Column(
                horizontal_alignment="center",
                controls=[
                    self._title,
                    flet.Container(padding=5),
                    flet.Column(
                        alignment=flet.MainAxisAlignment.CENTER,
                        controls=[
                            flet.Row(alignment="center",controls=[self._scheduling_]),
                            flet.Row(alignment="center", controls=[self._address_]),
                            flet.Row(alignment="center", controls=[self._log_out_]),
                        ]),
                    flet.Container(padding=5),
                ],
            )
        
        elif self.user['funcaoID'] == "colaborador":
            return flet.Column(
                horizontal_alignment="center",
                controls=[
                    self._title,
                    flet.Container(padding=5),
                    flet.Column(
                        alignment=flet.MainAxisAlignment.CENTER,
                        controls=[
                            flet.Row(alignment="center",controls=[self._scheduling_]),
                            flet.Row(alignment="center", controls=[self._report_]),
                            flet.Row(alignment="center", controls=[self._caixa_]),
                            flet.Row(alignment="center", controls=[self._address_]),
                            flet.Row(alignment="center", controls=[self._log_out_]),
                        ]),
                    flet.Container(padding=5),
                ],
            )
        
        return flet.Column(
            horizontal_alignment="center",
            controls=[
                self._title,
                flet.Container(padding=5),
                flet.Column(
                    alignment=flet.MainAxisAlignment.CENTER,
                    controls=[
                    flet.Row(alignment="center",controls=[self._scheduling_]),
                    flet.Row(alignment="center",controls=[self._service_]),
                    flet.Row(alignment="center",controls=[self._product_]),
                    flet.Row(alignment="center", controls=[self._barber_]),
                    flet.Row(alignment="center", controls=[self._report_]),
                    flet.Row(alignment="center", controls=[self._caixa_]),
                    flet.Row(alignment="center", controls=[self._address_]),
                    flet.Row(alignment="center", controls=[self._log_out_]),
                    ]),
                flet.Container(padding=5),
            ],
        )

async def main(page: flet.Page, user: dict):
    page.title = "Menus"
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

    async def _button_scheduling(e):
        await tela_menu_agendamento.main(page, user)

    async def _button_service(e):
        await tela_menu_service.main(page, user)

    async def _button_product(e):
        await tela_menu_product.main(page, user)

    async def _button_barber(e):
        await tela_menu_colaborador.main(page, user)

    async def _button_report(e):
        await tela_menu_relatorio.main(page, user)

    async def _button_caixa(e):
        await tela_menu_caixa.main(page, user)

    async def _button_address(e):
        ...

    #     # e.page.launch_url("https://maps.app.goo.gl/S6ee1U8CFyjqrS2U9")
    #     if page.can_launch_url("https://maps.app.goo.gl/S6ee1U8CFyjqrS2U9"):
    #         e.page.launch_url("https://maps.app.goo.gl/S6ee1U8CFyjqrS2U9")
    #     # e.page.launch_url("https://www.google.com/maps/search/?api=1&query=37.7749,-122.4194")
    #     # page.launch_url("https://maps.app.goo.gl/S6ee1U8CFyjqrS2U9",)

    async def _button_log_out(e):
        await tela_login.main(page)

   
    _menu_ = UserWidget(
        "Menus!",
        _button_scheduling,
        _button_service,
        _button_product,
        _button_barber,
        _button_report,
        _button_caixa,
        _button_log_out,
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
