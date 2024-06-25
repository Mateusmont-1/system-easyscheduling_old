import flet
from functools import partial
from google.cloud.firestore_v1 import FieldFilter
import asyncio

from . import tela_menu_main
from . import tela_editar_produto
from .firebase_config import get_firestore_client
from .config import COLOR_BACKGROUND_PAGE, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        produto_ref,
        func1,
        func2,
        ):
        super().__init__()
        self.title = title
        self.produto_ref = produto_ref
        self.func = func1
        self.func2 = func2
    
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
        
    def SignInOption(self):
        return flet.Container(
            content=flet.ElevatedButton
        )
    
    def build(self):
        self._title = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Text(
                value=self.title,
                size=30,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT,
            ),
        )
        
        self.data_table = flet.Container(
            visible=True,
            alignment=flet.alignment.center,
            content=flet.Row(
                scroll=True,
                controls=[flet.DataTable(
                    columns=[
                        flet.DataColumn(flet.Text("Nome produto",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                        flet.DataColumn(flet.Text("Preço",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                        flet.DataColumn(flet.Text("Permitir venda",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                ],
            )
            ]
            )
        )
        

        # Itere sobre os resultados
        for produto_ in self.produto_ref:
            produto_id = produto_.id
            produto = produto_.to_dict()
            if produto['permitir_venda']:
                texto = "Sim"
            else:
                texto = "Não"
            self.data_table.content.controls[0].rows.append(flet.DataRow(cells=[
                    flet.DataCell(flet.Text(produto['nome'],
                                            text_align="center",
                                            weight="bold",
                                            color=COLOR_TEXT_IN_FIELD,
                                            )),
                    flet.DataCell(flet.Text(produto['preco'],
                                            text_align="center",
                                            weight="bold",
                                            color=COLOR_TEXT_IN_FIELD)),
                    flet.DataCell(flet.Text(texto,
                                            text_align="center",
                                            weight="bold",
                                            color=COLOR_TEXT_IN_FIELD)),
                ],
                    on_select_changed=lambda e, _produto=produto, _produto_id =produto_id: self.func(_produto, _produto_id)
            ))

        self.no_scheduling = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Text(
                value="Não possui produtos",
                size=30,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT_IN_FIELD,
            ),
        )

        if len(self.data_table.content.controls[0].rows) == 0:
            self.no_scheduling.visible = True
            self.data_table.visible = False
        
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
            scroll="hidden",
            horizontal_alignment="center",
            controls=[
                self._title,
                flet.Container(padding=3),
                self.data_table,
                self.no_scheduling,
                self._back_button,
            ],
        )

async def main(page:flet.page, user):
    page.title = "Verificar produtos"
    # page.bgcolor = "#f0f3f6"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.theme_mode = "dark"
    page.clean()
    
    db = get_firestore_client()
    produtos_ref = db.collection("produto").stream()
    
    def show_details(row_data, id):
        nonlocal id_produto
        
        if row_data['permitir_venda']:
            texto = "Sim"
        else:
            texto = "Não"
        
        dialog.content.controls = [
            flet.Text(f"Nome Produto: {row_data['nome']}"),
            flet.Text(f"Preço: {row_data['preco']}"),
            flet.Text(f"Permitir venda: {texto}"),
        ]
        dialog.open = True
        id_produto = id
        page.update()
    
    async def button_editar_produto(e):
        close_dialog()
        await asyncio.sleep(0.1)
        await tela_editar_produto.main(page, user, id_produto)  
        
    id_produto = None
    # Criar o diálogo uma vez
    dialog = flet.AlertDialog(
        scrollable=True,
        title=flet.Text("Detalhes do Produto"),
        content=flet.Column([]),
        actions=[
            flet.TextButton("Editar produto", on_click=button_editar_produto),
            flet.TextButton("Fechar", on_click=lambda e: close_dialog()),
            
        ]
    )

    def close_dialog():
        dialog.open = False
        page.update()

    page.dialog = dialog
    
    async def _back_button(e):
        await tela_menu_main.main(page, user)
    
    def page_resize(e=None, inicio=None):
        if e:
            if page.width > 600:     
                largura = 600
                _scheduling_.width = largura
                _scheduling_.update()
            else:
                largura = page.width - 30
                _scheduling_.width = largura
                _scheduling_.update()
            if page.height > 600:     
                altura = 600
                _scheduling_.height = altura
                _scheduling_.update()
            else:
                altura = page.height - 60
                _scheduling_.height = altura
                _scheduling_.update()

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
        
    _scheduling_ = UserWidget(
        "Produtos!",
        produtos_ref,
        show_details,
        _back_button,
    )
    
    _scheduling_main = _main_column_()
    _scheduling_main.content.controls.append(flet.Container(padding=0))
    _scheduling_main.content.controls.append(_scheduling_)
    
    add_page(_scheduling_main)
   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)
