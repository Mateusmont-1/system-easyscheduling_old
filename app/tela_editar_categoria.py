import flet
from functools import partial

from . import tela_menu_main
from . import register_expenses
from .firebase_config import get_firestore_client
from . import tela_transicao
from .config import COLOR_BORDER_COLOR_ERROR, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        sub_title:str,
        btn_name:str,
        erro:str,
        categoria_ref,
        func,
        func2,
        ):
        self.title = title
        self._sub_title = sub_title
        self.btn_name = btn_name
        self.erro = erro
        self.categoria_ref = categoria_ref.to_dict()
        self.func = func
        self.func2 = func2
        super().__init__()
    
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
        
        self._checkbox = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Row(
                controls=[
                flet.Checkbox(value=self.categoria_ref['ativo']),
                flet.Text(
                    value="Permitir utilização?",
                    size=20,
                    weight="bold",
                    color=COLOR_TEXT_IN_FIELD,),
                ],
            visible=True,
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
                        self.InputTextField("Nome",
                                            False, self.categoria_ref['nome']),
                    ],
                ),
                self._checkbox,
                flet.Container(padding=5),
                self._sign_in,
                self._back_button,
                flet.Container(padding=10),
            ],
        )

async def main(page:flet.page, user, id_categoria):
    page.title = "Editar categoria"
    # page.bgcolor = "#f0f3f6"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.theme_mode = "dark"

    page.clean()
    
    db = get_firestore_client()
    categoria_ref = db.collection("categorias").document(id_categoria).get()
    
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
                spacing=25,
                controls=[
                extruct,
                ]
            )
        )

    async def _update_produto(e):
        
        verifica = verificar_campos()
            
        if verifica:      
            nome = str(_sign_in_.controls[0].controls[2].controls[0].content.value) 
            checkbox_venda = _sign_in_._checkbox.content.controls[0].value
            
            cadastra_categoria = register_expenses.UpdateCategory(nome, checkbox_venda, id_categoria)
            confirma = cadastra_categoria.atualizar_categoria()
            if confirma:
                texto = "Categoria atualizada!"
                await tela_transicao.main(page, user, texto)
                ...
            else:
                nome = _sign_in_.controls[0].controls[3].controls[0].content
                nome.error_text = "Este serviço já existe!"
                nome.update()
            
    def verificar_campos():
        nome = _sign_in_.controls[0].controls[2].controls[0].content
        verificar = 0
        if nome.value == "":
            nome.border_color = COLOR_BORDER_COLOR_ERROR
            verificar += 1
        else:
            nome.border_color = COLOR_BORDER_COLOR
        
        nome.update()
        
        return True if verificar == 0 else None
    
    async def _back_button(e):
        await tela_menu_main.main(page, user)
        
    _sign_in_ = UserWidget(
        "Atualizar categoria!",
        "Entre com os dados da categoria abaixo",
        "Atualizar",
        "",
        categoria_ref,
        _update_produto,
        _back_button,
        
    )
    
    _sign_in_main = _main_column_()
    _sign_in_main.content.controls.append(flet.Container(padding=0))
    _sign_in_main.content.controls.append(_sign_in_)
    
    add_page(_sign_in_main)


# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER) 