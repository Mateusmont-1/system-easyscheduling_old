import flet
import datetime
from functools import partial
from google.cloud.firestore_v1 import FieldFilter
import asyncio

from . import tela_menu_main
from . import tela_editar_despesa
from .firebase_config import get_firestore_client
from .config import COLOR_BACKGROUND_PAGE, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        func1,
        func2,
        func3,
        ):
        super().__init__()
        self.title = title
        self.func = func1
        self.func2 = func2
        self.func3 = func3
        
    
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
      
        
        self.date_picker = flet.Container(
            alignment=flet.alignment.center,
            content=flet.DatePicker(
                first_date=datetime.datetime.now() - datetime.timedelta(days=31),
                last_date=datetime.datetime.now() + datetime.timedelta(days=31),
                on_change=partial(self.func2)
            )
            )
        
        self.day_choose = flet.Container(
            visible=True,
            content=flet.ElevatedButton(
                on_click=lambda _: self.date_picker.content.pick_date(),
                icon=flet.icons.CALENDAR_MONTH,
                text="Informe o mês",
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
        
        self.data_table = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Row(
                scroll=True,
                controls=[flet.DataTable(
                columns=[
                    flet.DataColumn(flet.Text("Data",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                    flet.DataColumn(flet.Text("Categoria",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                    flet.DataColumn(flet.Text("Valor",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                ],
            )
            ]
            )
        )
        
        self.no_scheduling = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Text(
                value="Não possui despesas",
                size=30,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT_IN_FIELD,
            ),
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
            scroll="hidden",
            horizontal_alignment="center",
            controls=[
                self._title,
                self.day_choose,
                flet.Container(padding=3),
                self.data_table,
                self.date_picker,
                self.no_scheduling,
                self._back_button,
            ],
        )

async def main(page:flet.page, user):
    page.title = "Verificar despesas"
    # page.bgcolor = "#f0f3f6"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.theme_mode = "dark"
    page.clean()
    
    id_despesa = ""
    mes_despesa = ""
    ano_despesa = ""
    
    db = get_firestore_client()
    
    def _visible_button(e):
        dropdown = e.control.value
        _scheduling_.day_choose.visible = True
        _scheduling_.day_choose.update()

        if _scheduling_.date_picker.content.value != None:
            _on_date_change()
    
    def show_details(row_data, id):
        nonlocal id_despesa, ano_despesa, mes_despesa
        
        dia, mes, ano = row_data['data'].split('-')
        mes_despesa = mes
        ano_despesa = ano
        
        # dialog.content.controls = [flet.Text(f"{key}: {value}") for key, value in row_data.items()]
        dialog.content.controls = [
            flet.Text(f"Data: {row_data['data']}"),
            flet.Text(f"Categoria: {row_data['categoria_nome']}"),
            flet.Text(f"Valor: {row_data['valor']}"),
            flet.Text(f"Descrição: {row_data['descricao']}"),
        ]
        dialog.open = True
        id_despesa = id
        page.update()
    
    async def _tela_editar_despesa(e):
        close_dialog()
        await asyncio.sleep(0.1)
        await tela_editar_despesa.main(page,user, ano_despesa, mes_despesa, id_despesa)
        
    id_despesa = None
    # Criar o diálogo uma vez
    dialog = flet.AlertDialog(
        scrollable=True,
        title=flet.Text("Detalhes da Despesa"),
        content=flet.Column([]),
        actions=[
            flet.TextButton("Editar despesa", on_click=_tela_editar_despesa),
            flet.TextButton("Fechar", on_click=lambda e: close_dialog()),
            
        ]
    )

    def close_dialog():
        dialog.open = False
        page.update()

    page.dialog = dialog
        
    def despesas_por_mes_ano(ano, mes):
        despesas_filtradas = dict()

        # Referência à subcoleção do mês dentro do ano especificado
        mes_ref = db.collection('despesas').document(ano).collection(mes)
    
        # Consultar todas as despesas dentro do mês
        despesas = mes_ref.stream()
    
        for despesa in despesas:
            despesas_filtradas[despesa.id] = despesa.to_dict()
    
        return despesas_filtradas

    def _on_date_change(e=None):
        # verifica se a função foi executada no date_picker
        if e:
            selected_date = e.control.value
        else:
            selected_date = _scheduling_.date_picker.content.value
        
       # Obtendo referência ao widget data_table
        data_table = _scheduling_.data_table.content
        data_table.controls[0].rows.clear()
        data_table.update()
        
        # Formatando a data de "ano-mes-dia" para "mes/ano"
        data_objeto = datetime.datetime.strptime(str(selected_date), '%Y-%m-%d %H:%M:%S')
        mes = data_objeto.strftime('%m')
        ano = data_objeto.strftime('%Y')
        
        # Consulta no banco de dados referente ao mês e ano selecionados
        despesas_filtradas = despesas_por_mes_ano(ano, mes)
        
        # Verifica se possui dados na lista
        if despesas_filtradas:
            _scheduling_.data_table.visible = True
            _scheduling_.data_table.update()
            _scheduling_.no_scheduling.visible = False
            _scheduling_.no_scheduling.update()

            # Itera sobre os resultados
            for despesa_id, despesa_dict in despesas_filtradas.items():
                data = despesa_dict.get('data', 'N/A')
                valor = despesa_dict.get('valor', 'N/A')
                categoria = despesa_dict.get('categoria_nome', 'N/A')
                data_table.controls[0].rows.append(flet.DataRow(cells=[
                    flet.DataCell(flet.Text(data, text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                    flet.DataCell(flet.Text(categoria, text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                    flet.DataCell(flet.Text(valor, text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                    ],
                    on_select_changed=lambda e, 
                    despesa_dict=despesa_dict, despesa_id=despesa_id: show_details(
                        despesa_dict, despesa_id)
                    )
                )
                data_table.update()

            if len(data_table.controls[0].rows) == 0:
                _scheduling_.data_table.visible = False
                _scheduling_.data_table.update()
                _scheduling_.no_scheduling.visible = True
                _scheduling_.no_scheduling.update()
        else:
            # Caso não possua, oculta a DataTable e aparece texto "Não possui despesas"
            _scheduling_.data_table.visible = False
            _scheduling_.data_table.update()
            _scheduling_.no_scheduling.visible = True
            _scheduling_.no_scheduling.update()   
    
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

    async def _back_button(e):
        await tela_menu_main.main(page,user)   
        
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
        "Verificar despesas!",
        _visible_button,
        _on_date_change,
        _back_button,
    )
    
    _scheduling_main = _main_column_()
    _scheduling_main.content.controls.append(flet.Container(padding=0))
    _scheduling_main.content.controls.append(_scheduling_)
    
    add_page(_scheduling_main)
   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)
