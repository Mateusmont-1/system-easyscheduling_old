# Implementação que eu realizei antes para tela_logyn.py

import flet
import datetime
from functools import partial
from google.cloud.firestore_v1 import FieldFilter

from . import tela_menu_main
from .firebase_config import get_firestore_client
from .config import COLOR_BACKGROUND_PAGE, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD


class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        func,
        func2,
        ):
        super().__init__()
        self.title = title
        self.func = func
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
        
        self.date_picker = flet.Container(
            alignment=flet.alignment.center,
            content=flet.DatePicker(
                first_date=datetime.datetime(year=2024, month=6, day=1),
                last_date=datetime.datetime.now(),
                on_change=partial(self.func)
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
                    flet.DataColumn(flet.Text("Categoria",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                    flet.DataColumn(flet.Text("Valor (R$)",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                ]
            )
            ]
            )
        )
        
        self.no_scheduling = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Text(
                value="Não possui receitas",
                size=30,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT_IN_FIELD,
            ),
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
    page.title = "Relátorio mensal"
    # page.bgcolor = "#f0f3f6"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.theme_mode = "dark"
    page.clean()
    
    db = get_firestore_client()
    
    def _on_date_change(e=None):
        # Verifica se a função foi executada no date_picker
        if e:
            selected_date = e.control.value
        else:
            selected_date = _scheduling_.date_picker.content.value

        # Obtendo referência ao widget data_table
        data_table = _scheduling_.data_table.content
        data_table.controls[0].rows.clear()
        data_table.update()

        # Formatando a data para extrair mês e ano
        data_objeto = datetime.datetime.strptime(str(selected_date), '%Y-%m-%d %H:%M:%S')
        mes = data_objeto.month
        ano = data_objeto.year

        # Query no banco de dados referente ao mês e ano
        transacoes_ref = db.collection("transacoes").document(str(ano)).collection(str(mes).zfill(2))
        despesas_ref = db.collection("despesas").document(str(ano)).collection(str(mes).zfill(2))

        transacoes = transacoes_ref.stream()
        despesas = despesas_ref.stream()

        lista_transacoes = list(transacoes)
        lista_despesas = list(despesas)

        total_ganho = 0
        total_despesas = 0

        # Itera sobre as transações para calcular o total de ganhos
        for transacao in lista_transacoes:
            transacao_data = transacao.to_dict()
            valor = transacao_data.get('total', 0)
            total_ganho += valor

        # Itera sobre as despesas para calcular o total de despesas
        for despesa in lista_despesas:
            despesa_data = despesa.to_dict()
            valor = despesa_data.get('valor', 0)
            total_despesas += valor

        saldo = total_ganho - total_despesas

        # Exibe o total de ganhos, despesas e saldo no mês selecionado
        data_table.controls[0].rows.append(flet.DataRow(cells=[
            flet.DataCell(flet.Text("Total Ganho",
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text(f'R$ {total_ganho:.2f}',
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
        ]))
        data_table.update()

        data_table.controls[0].rows.append(flet.DataRow(cells=[
            flet.DataCell(flet.Text("Total Despesas",
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text(f'R$ {total_despesas:.2f}',
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
        ]))
        data_table.update()

        data_table.controls[0].rows.append(flet.DataRow(cells=[
            flet.DataCell(flet.Text("Saldo",
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text(f'R$ {saldo:.2f}',
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
        ]))
        data_table.update()

        # Atualiza a visibilidade da data_table
        if len(data_table.controls[0].rows) == 0:
            _scheduling_.data_table.visible = False
            _scheduling_.data_table.update()
            _scheduling_.no_scheduling.visible = True
            _scheduling_.no_scheduling.update()
        else:
            _scheduling_.data_table.visible = True
            _scheduling_.data_table.update()
            _scheduling_.no_scheduling.visible = False
            _scheduling_.no_scheduling.update()

    async def _back_button(e):
        await tela_menu_main.main(page,user)
                
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
        "Receita Barbearia!",
        _on_date_change,
        _back_button,
    )
    
    _scheduling_main = _main_column_()
    _scheduling_main.content.controls.append(flet.Container(padding=0))
    _scheduling_main.content.controls.append(_scheduling_)
    
    add_page(_scheduling_main)
   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)
