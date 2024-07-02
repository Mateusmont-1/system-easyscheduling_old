import flet
import datetime
from functools import partial

from . import tela_menu_main
from . import register_expenses
from .firebase_config import get_firestore_client
from . import tela_transicao
from .config import COLOR_BORDER_COLOR_ERROR, COLOR_TEXT_IN_DROPDOWN, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        sub_title:str,
        btn_name:str,
        erro:str,
        category_ref,
        func,
        func2,
        func3
        ):
        self.title = title
        self._sub_title = sub_title
        self.btn_name = btn_name
        self.erro = erro
        self.category_ref = category_ref
        self.func = func
        self.func2 = func2
        self.func3 = func3
        super().__init__()
        
        self.category_dict = dict()
    
    def InputTextField(self, text:str, hide:bool, visible_text=False):
        return flet.Container(
            visible=visible_text,
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
        
        self.date_picker = flet.Container(
            alignment=flet.alignment.center,
            content=flet.DatePicker(
                first_date=datetime.datetime.now() - datetime.timedelta(days=31),
                last_date=datetime.datetime.now() + datetime.timedelta(days=31),
                on_change=partial(self.func)
            )
            )
        
        self.day_choose = flet.Container(
            visible=True,
            content=flet.ElevatedButton(
                on_click=lambda _: self.date_picker.content.pick_date(),
                icon=flet.icons.CALENDAR_MONTH,
                text="Informe o dia",
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
        
        self._category_expense = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Informe a categoria", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  )
            )
        
        for categoria in self.category_ref:
            # Cada documento é um objeto com ID e dados            
            category_dropdown = self._category_expense.content
            _categoria_id = categoria.id
            _categoria_data = categoria.to_dict()
            
            if _categoria_data['ativo']:
                _nome = _categoria_data['nome']
            
                # adiciona no dropdown as categoria de despesa
                category_dropdown.options.append(flet.dropdown.Option(text= _nome, key= _categoria_id,))

                self.category_dict[_categoria_id] = _categoria_data
        
        self._sign_in = flet.Container(
            content=flet.ElevatedButton(
                on_click=partial(self.func2),
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
                visible=False,
                bgcolor=COLOR_BACKGROUND_BUTTON,
                color=COLOR_TEXT_IN_BUTTON,
                height=48,
                width=275,
            )
        )
        
        self._back_button = flet.Container(
            content=flet.ElevatedButton(
                on_click=partial(self.func3),
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
                self.day_choose,
                self._category_expense,
                flet.Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("Valor (R$)",
                                            False),
                        self.InputTextField("Descrição",
                                            False),
                    ],
                ),
                flet.Container(padding=5),
                self._sign_in,
                self._back_button,
                flet.Container(padding=10),
                self.date_picker
            ],
        )

async def main(page: flet.page, user):
    # Configurações iniciais da página
    page.title = "Cadastro despesa"
    page.clean()

    # Obtém o cliente Firestore e as categorias
    db = get_firestore_client()
    category_ref = db.collection("categorias").stream()

    # Variáveis para armazenar a data formatada, ano e mês
    data_formatada = None
    data_ano = None
    data_mes = None

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

    # Função chamada quando a data é alterada
    def _on_date_change(e=None):
        # Torna visíveis os campos relacionados à despesa
        _sign_in_._category_expense.visible = True
        _sign_in_._category_expense.update()
        for control in _sign_in_.controls[0].controls[4].controls:
            control.visible = True
            control.update()
        _sign_in_._sign_in.content.visible = True
        _sign_in_._sign_in.content.update()

        # Formata a data selecionada
        selected_date = e.control.value
        data_objeto = datetime.datetime.strptime(str(selected_date), '%Y-%m-%d %H:%M:%S')
        nonlocal data_formatada, data_ano, data_mes
        data_formatada = data_objeto.strftime('%d-%m-%Y')
        data_ano = data_objeto.strftime('%Y')
        data_mes = data_objeto.strftime('%m')

    # Função para criar um novo produto
    async def _create_produto(e):
        if verificar_campos():
            descricao = str(_sign_in_.controls[0].controls[4].controls[1].content.value)
            preco = float(str(_sign_in_.controls[0].controls[4].controls[0].content.value).replace(',', "."))
            id_category = _sign_in_._category_expense.content.value
            name_category = _sign_in_.category_dict[id_category]['nome']

            # Cria e registra a despesa
            registra_despesa = register_expenses.CreateExpense(data_formatada, data_mes, data_ano, id_category, name_category, preco, descricao)
            if registra_despesa.registrar_despesa():
                await tela_transicao.main(page, user, "Despesa registrada!")
            else:
                print('Não foi cadastrado')

    # Verifica se os campos estão preenchidos corretamente
    def verificar_campos():
        descricao = _sign_in_.controls[0].controls[4].controls[1].content
        preco = _sign_in_.controls[0].controls[4].controls[0].content
        dropdown_category = _sign_in_._category_expense.content

        # Função auxiliar para checar cada campo
        def check_field(field, error_condition):
            if error_condition:
                field.border_color = COLOR_BORDER_COLOR_ERROR
                field.update()
                return False
            field.border_color = COLOR_BORDER_COLOR
            field.update()
            return True

        # Verifica todos os campos
        valid = True
        valid &= check_field(descricao, descricao.value == "")
        valid &= check_field(preco, preco.value == "" or not converte_float(preco.value.replace(',', ".")) or float(preco.value.replace(',', ".")) == 0.0)
        valid &= check_field(dropdown_category, dropdown_category.value is None)
        return valid

    # Converte string para float
    def converte_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    # Função para retornar ao menu principal
    async def _back_button(e):
        await tela_menu_main.main(page, user)

    # Cria o widget de adição de despesas
    _sign_in_ = UserWidget(
        "Adicionar despesa!",
        "Entre com os dados da despesa abaixo",
        "Cadastrar",
        "",
        category_ref,
        _on_date_change,
        _create_produto,
        _back_button,
    )

    # Adiciona o widget à coluna principal e à página
    _sign_in_main = _main_column_()
    _sign_in_main.content.controls.append(flet.Container(padding=0))
    _sign_in_main.content.controls.append(_sign_in_)

    add_page(_sign_in_main)
   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER) 