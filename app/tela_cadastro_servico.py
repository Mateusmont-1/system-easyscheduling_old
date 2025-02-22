import flet
from functools import partial

from . import tela_menu_main
from . import register_service
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
                    size=20,
                    color=COLOR_TEXT_IN_FIELD,
                ),
                password=hide,
            ),
        )
    
    def InputTextField2(self, text:str, hide:bool):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=275,
                keyboard_type="number",
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
        
        self._checkbox = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Row(
                controls=[
                flet.Checkbox(),
                flet.Text(
                    value="Permitir agendamento?",
                    size=20,
                    weight="bold",
                    color=COLOR_TEXT_IN_FIELD,),
                ],
            alignment=flet.MainAxisAlignment.CENTER,
            ))
        
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
                        self.InputTextField("Preço (R$)",
                                            False),
                        self.InputTextField2("Duração (Min)",
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

async def main(page: flet.page, user):
    # Configurações iniciais da página
    page.title = "Cadastro serviço"
    page.clean()
    
    # Função para redimensionar a página
    def page_resize(e=None, inicio=None):
        largura = min(page.width - 30, 600)
        altura = min(page.height - 60, 600)
        if e:
            _sign_in_main.width = largura
            _sign_in_main.height = altura
            _sign_in_main.update()
        if inicio is not None:
            return largura if inicio else altura

    # Define o manipulador para redimensionamento da janela
    page.window.on_resized = page_resize

    # Cria a coluna principal da interface
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
        
    # Adiciona um componente à página
    def add_page(extruct):
        page.add(flet.Row(alignment="center", spacing=25, controls=[extruct]))
        
    # Função para retornar ao menu principal
    async def _back_button(e):
        await tela_menu_main.main(page, user)
                
    # Função para cadastrar o serviço
    async def _login_user(e): 
        if verificar_campos():
            nome = str(_sign_in_.controls[0].controls[2].controls[0].content.value)
            preco = float(str(_sign_in_.controls[0].controls[2].controls[1].content.value).replace(',', "."))
            duracao = int(_sign_in_.controls[0].controls[2].controls[2].content.value)
            checkbox_scheduling = _sign_in_._checkbox.content.controls[0].value
            
            # Cria e cadastra o serviço
            cadastra_servico = register_service.Service(nome, preco, duracao, checkbox_scheduling)
            confirma = cadastra_servico.criar_servico()
            if confirma:
                texto = "Serviço cadastrado!"
                await tela_transicao.main(page, user, texto)
            else:
                nome = _sign_in_.controls[0].controls[2].controls[0].content
                nome.error_text = "Este serviço já existe!"
                nome.update()

    # Verifica se os campos estão preenchidos corretamente
    def verificar_campos():
        nome = _sign_in_.controls[0].controls[2].controls[0].content
        preco = _sign_in_.controls[0].controls[2].controls[1].content
        duracao = _sign_in_.controls[0].controls[2].controls[2].content
        verificar = 0
        if nome.value == "":
            nome.border_color = COLOR_BORDER_COLOR_ERROR
            verificar += 1
        else:
            nome.border_color = COLOR_BORDER_COLOR
        if preco.value == "":
            preco.border_color = COLOR_BORDER_COLOR_ERROR
            verificar += 1
        elif not converte_float(preco.value.replace(',', ".")):
            preco.border_color = COLOR_BORDER_COLOR_ERROR
            verificar += 1
        else:
            preco.border_color = COLOR_BORDER_COLOR
        if duracao.value == "":
            duracao.border_color = COLOR_BORDER_COLOR_ERROR
            verificar += 1
        elif not duracao.value.isdigit():
            verificar += 1
            duracao.border_color = COLOR_BORDER_COLOR_ERROR
        else:
            duracao.border_color = COLOR_BORDER_COLOR
        
        nome.update()
        preco.update()
        duracao.update()
        return True if verificar == 0 else None
        
    # Converte string para float
    def converte_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    # Cria o widget de adição de serviço
    _sign_in_ = UserWidget(
        "Adicionar serviço!",
        "Entre com os dados do serviço abaixo",
        "Cadastrar",
        "",
        _login_user,
        _back_button,
    )
    
    _sign_in_main = _main_column_()
    _sign_in_main.content.controls.append(flet.Container(padding=0))
    _sign_in_main.content.controls.append(_sign_in_)
    
    add_page(_sign_in_main)
   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER) 