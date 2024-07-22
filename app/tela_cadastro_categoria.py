import flet
from functools import partial

from . import tela_menu_main
from . import register_expenses
from . import tela_transicao
from .config import COLOR_BORDER_COLOR_ERROR, COLOR_TEXT_IN_DROPDOWN, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD


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
                flet.Checkbox(),
                flet.Text(
                    value="Permitir utilização?",
                    size=20,
                    weight="bold",
                    color=COLOR_TEXT,),
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
                                            False),
                    ],
                ),
                self._checkbox,
                flet.Container(padding=5),
                self._sign_in,
                self._back_button,
                flet.Container(padding=10),
            ],
        )

async def main(page: flet.Page, user):
    # Definindo o título da página
    page.title = "Cadastro categoria"
    page.clean()
    
    # Função para ajustar o tamanho da página conforme a redimensionamento da janela
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
        page.add(
            flet.Row(
                alignment="center",
                spacing=25,
                controls=[extruct]
            )
        )

    # Função assíncrona para criar uma nova categoria
    async def _create_produto(e):
        if verificar_campos():
            nome = str(_sign_in_.controls[0].controls[2].controls[0].content.value)
            checkbox_venda = _sign_in_._checkbox.content.controls[0].value
            cadastra_categoria = register_expenses.CreateCategory(nome, checkbox_venda)
            confirma = cadastra_categoria.criar_categoria()
            
            # Verifica se a categoria foi criada com sucesso
            if confirma:
                texto = "Categoria cadastrada!"
                await tela_transicao.main(page, user, texto)
            else:
                nome_input = _sign_in_.controls[0].controls[3].controls[0].content
                nome_input.error_text = "Esta categoria já existe!"
                nome_input.update()
    
    # Função para verificar se os campos obrigatórios estão preenchidos
    def verificar_campos():
        nome = _sign_in_.controls[0].controls[2].controls[0].content
        verificar = 0
        
        # Verifica se o campo nome está vazio
        if nome.value == "":
            nome.border_color = COLOR_BORDER_COLOR_ERROR
            verificar += 1
        else:
            nome.border_color = COLOR_BORDER_COLOR
        
        nome.update()
        
        return verificar == 0
    
    # Função assíncrona para voltar à página principal
    async def _back_button(e):
        await tela_menu_main.main(page, user)
    
    # Cria o widget de cadastro de categoria
    _sign_in_ = UserWidget(
        "Adicionar categoria!",
        "Entre com os dados da categoria abaixo",
        "Cadastrar",
        "",
        _create_produto,
        _back_button,
    )
    
    # Cria o contêiner principal e adiciona o widget de cadastro
    _sign_in_main = _main_column_()
    _sign_in_main.content.controls.append(flet.Container(padding=0))
    _sign_in_main.content.controls.append(_sign_in_)
    
    add_page(_sign_in_main)

# Se necessário, adicione a chamada para a função principal conforme o seu framework/ambiente
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER) 