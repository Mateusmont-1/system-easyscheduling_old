import flet
import asyncio

from .config import COLOR_BACKGROUND_CONTAINER, COLOR_BORDER_COLOR, COLOR_TEXT, COLOR_TEXT_BUTTON, COLOR_TEXT_IN_BUTTON, COLOR_BACKGROUND_BUTTON, COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        ):
        self.title = title
        super().__init__()

       
    
    
    def build(self):
        self._title = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Text(
                self.title,
                size=40,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT,
            ),
        )
        
        return flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            alignment=flet.MainAxisAlignment.CENTER,
            controls=[
                self._title,
            ],
        )

async def main(page: flet.Page, user=None, texto:str=None, tela_inicial:bool=None):
    page.clean()
    
    def page_resize(e=None, inicio=None):
        if e:
            if page.width > 600:     
                largura = 600
                _transicao_main.width = largura
                _transicao_main.update()
            else:
                largura = page.width - 30
                _transicao_main.width = largura
                _transicao_main.update()
            if page.height > 600:     
                altura = 600
                _transicao_main.height = altura
                _transicao_main.update()
            else:
                altura = page.height - 60
                _transicao_main.height = altura
                _transicao_main.update()

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
        
    _transicao_ = UserWidget(texto)
    _transicao_main = _main_column_()
    _transicao_main.content.controls.append(flet.Container(padding=0))
    _transicao_main.content.controls.append(_transicao_)
    
    page.add(
        flet.Row(
            alignment="center",
            spacing=25,
            controls=[
                _transicao_main,
            ]
        )
    )
    
    # Espera 2.5 segundos antes de transitar para a tela do menu principal
    await asyncio.sleep(2.5)

    # Se a variavel tela_inicial for verdadeira a tela de transição irá para tela_login
    if tela_inicial:
        from . import tela_login
        await tela_login.main(page)
    # Se não irá para tela_menu
    else:
        from . import tela_menu_main
        await tela_menu_main.main(page, user)
    
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)
