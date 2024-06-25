# Implementação que eu realizei antes para tela_logyn.py

import flet
import datetime
from functools import partial
from google.cloud.firestore_v1 import FieldFilter

from . import tela_menu_main
from .firebase_config import get_firestore_client
from .config import COLOR_TEXT_IN_DROPDOWN, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        collaborator_ref,
        func1,
        func2,
        func3,
        ):
        super().__init__()
        self.title = title
        self.collaborator_ref = collaborator_ref
        self.func = func1
        self.func2 = func2
        self.func3 = func3
        
        self.collaborator_dict = dict()
        
    
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
        self.collaborator_choose = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha o(a) atendente", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func)
                                  )
            )
        
        for atendente in self.collaborator_ref:
            # Cada documento é um objeto com ID e dados
            atendente_dropdown = self.collaborator_choose.content
            _colaborador_id = atendente.id
            _atendente_data = atendente.to_dict()
        
            _nome = _atendente_data['nome']
            
            # adiciona no dropdown o atendente
            atendente_dropdown.options.append(flet.dropdown.Option(text= _nome, key= _colaborador_id,))
            
            self.collaborator_dict[_colaborador_id] = _atendente_data
        
        self.date_picker = flet.Container(
            alignment=flet.alignment.center,
            content=flet.DatePicker(
                first_date=datetime.datetime(year=2024, month=6, day=1),
                last_date=datetime.datetime.now(),
                on_change=partial(self.func2)
            )
            )
        
        self.day_choose = flet.Container(
            visible=False,
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

        self.query_type = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha o tipo de consulta",
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func)
                                  )
            )
        
        for i in range(3):
            # Cada documento é um objeto com ID e dados
            query_dropdown = self.query_type.content
            if i < 1:
                texto = "Diário"
            elif i < 2:
                texto = "Semanal"
            elif i < 3:
                texto = "Mensal"
            # adiciona no dropdown o atendente
            query_dropdown.options.append(flet.dropdown.Option(text= texto, key= i))

        
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
                                              color=COLOR_TEXT_IN_FIELD,)),
                    flet.DataColumn(flet.Text("Nome do atendente",
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
                value="Não possui entradas",
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
                self.collaborator_choose,
                self.query_type,
                self.day_choose,
                flet.Container(padding=3),
                self.data_table,
                self.date_picker,
                self.no_scheduling,
                self._back_button,
            ],
        )

async def main(page:flet.page, user):
    page.title = "Relátorio atendente"
    page.clean()
    
    id_finish = ""
    
    db = get_firestore_client()
    collaborator_ref = db.collection("colaborador").stream()
    
    def _visible_button(e):
        dropdown = e.control.value
        query_type = _scheduling_.query_type
        day_choose = _scheduling_.day_choose
        if query_type.visible == False:
            query_type.visible = True
            query_type.update()
        else:
            if query_type.content.value == "0":
                day_choose.content.text = "Informe o dia"
            elif query_type.content.value == "1":
                day_choose.content.text = "Informe a semana"
            if query_type.content.value == "2":
                day_choose.content.text = "Informe o mês"
            day_choose.visible = True
            day_choose.update()

        if _scheduling_.date_picker.content.value != None:
            _on_date_change()
    
    def show_details(row_data, id):
        nonlocal id_finish
        agendamento_id = row_data['agendamento_id']
        agendamento_ref = db.collection('agendamentos').document(agendamento_id).get()
        agendamento_data = agendamento_ref.to_dict()
       # Criação da lista de controles padrão
        controls = [
            flet.Text(f"Nome cliente: {agendamento_data.get('nome', 'N/A')}"),
            flet.Text(f"Data: {row_data['data']}"),
            flet.Text(f"Hórario: {agendamento_data.get('horario', 'N/A')}"),
            flet.Text(f"Preço serviços: R$ {row_data['preco_servico']}"),
            flet.Text(f"Preço produtos: R${row_data['preco_produtos']}"),
            flet.Text(f"Valor Total: R$ {row_data['total']}")
        ]
        # Se tiver desconto aparece no dialog
        if agendamento_data['desconto'] != 0.0:
            controls.append(flet.Text(f"Desconto: R$ {row_data['desconto']}"))
        
        # Adicionando uma linha vazia
        controls.append(flet.Text(""))
        # Verifica se há produtos e adiciona mais controles se necessário
        if 'servicos' in agendamento_data and len(agendamento_data['servicos']) > 0:
            controls.append(flet.Text("Serviços:"))
            for servico in agendamento_data['servicos']:
                controls.append(flet.Text(f" - {servico['nome']}: R$ {servico['preco']}"))

        # Adicionando uma linha vazia
        controls.append(flet.Text(""))
        # Verifica se há produtos e adiciona mais controles se necessário
        if 'produtos' in agendamento_data and len(agendamento_data['produtos']) > 0:
            controls.append(flet.Text("Produtos:"))
            for produto in agendamento_data['produtos']:
                controls.append(flet.Text(f" - {produto['nome']}: R$ {produto['preco']}"))

        dialog.content.controls = controls
        dialog.open = True
        id_finish = id
        page.update()

    id_finish = None
    # Criar o diálogo uma vez
    dialog = flet.AlertDialog(
        title=flet.Text("Detalhes da Receita"),
        content=flet.Column([]),
        actions=[
            flet.TextButton("Fechar", on_click=lambda e: close_dialog()),
        ]
    )

    def close_dialog():
        dialog.open = False
        page.update()

    page.dialog = dialog

    # Função principal que é chamada na alteração da data ou do atendente
    def _on_date_change(e=None):
        selected_date = obter_data_selecionada(e)
        collaborator_choose, query_type, data_table = obter_referencias_widgets()
        limpar_tabela(data_table)
        mes, ano, data_formatada= extrair_mes_ano(selected_date)
        lista_transacoes = consultar_transacoes(ano, mes, collaborator_choose.value, query_type.value, data_formatada)
        lista_transacoes.sort(key=lambda x: datetime.datetime.strptime(x.to_dict().get('data', '01-01-1970'), '%d-%m-%Y'))
        atualizar_interface(lista_transacoes, data_table)

    # Obtém a data selecionada no date_picker ou no evento
    def obter_data_selecionada(e):
        if e:
            return e.control.value
        return _scheduling_.date_picker.content.value

    # Obtém referências aos widgets barber_choose e data_table
    def obter_referencias_widgets():
        collaborator_choose = _scheduling_.collaborator_choose.content
        query_type = _scheduling_.query_type.content
        data_table = _scheduling_.data_table.content
        return collaborator_choose, query_type, data_table

    # Limpa as linhas da tabela de dados
    def limpar_tabela(data_table):
        data_table.controls[0].rows.clear()
        data_table.update()

    # Extrai o mês e ano de uma data fornecida
    def extrair_mes_ano(selected_date):
        data_objeto = datetime.datetime.strptime(str(selected_date), '%Y-%m-%d %H:%M:%S')
        data_formatada = data_objeto.strftime('%d-%m-%Y')
        return data_objeto.month, data_objeto.year, data_formatada

    # Consulta as transações no Firestore para o mês, ano e atendente selecionado
    def consultar_transacoes(ano, mes, colaborador_id, query_type, data_formatada):
        transacoes_ref = db.collection("transacoes").document(str(ano)).collection(str(mes).zfill(2))
        if query_type == "0":
            # Consulta para ganhos diários
            query = transacoes_ref.where(filter=FieldFilter("colaborador_id", "==", colaborador_id)).where(filter=FieldFilter("data", "==", data_formatada))
        elif query_type == "1":
            # Consulta para ganhos semanais
            data = datetime.datetime.strptime(data_formatada, "%d-%m-%Y")
            start_of_week = data - datetime.timedelta(days=data.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
            
            query = transacoes_ref.where(filter=FieldFilter("colaborador_id", "==", colaborador_id)).where(filter=FieldFilter("data", ">=", start_of_week.strftime("%d-%m-%Y"))).where(filter=FieldFilter("data", "<=", end_of_week.strftime("%d-%m-%Y")))
        elif query_type == "2":
            query = transacoes_ref.where(filter=FieldFilter("colaborador_id", "==", colaborador_id))

        transacoes = query.stream()
        return list(transacoes)

    # Atualiza a interface com os dados das transações e o total ganho
    def atualizar_interface(lista_transacoes, data_table):
        if len(lista_transacoes) != 0:
            exibir_tabela()
            total_ganho_servico = 0
            total_ganho_produto = 0
            for transacao in lista_transacoes:
                ganho_servico, ganho_produto = adicionar_transacao_na_tabela(transacao, data_table)
                total_ganho_servico += ganho_servico
                total_ganho_produto += ganho_produto
            total_ganho = total_ganho_servico + total_ganho_produto
            if total_ganho > 0:
                exibir_total_ganho(total_ganho_servico, total_ganho_produto, total_ganho, data_table)
            verificar_tabela_vazia(data_table)
        else:
            ocultar_tabela()

    # Exibe a tabela e oculta o texto "Não possui transações"
    def exibir_tabela():
        _scheduling_.data_table.visible = True
        _scheduling_.data_table.update()
        _scheduling_.no_scheduling.visible = False
        _scheduling_.no_scheduling.update()

    # Adiciona uma transação à tabela de dados
    def adicionar_transacao_na_tabela(transacao, data_table):
        transacao_id = transacao.id
        transacao_data = transacao.to_dict()

        # Valor total cobrado ao cliente
        valor_total = transacao_data.get('total', 0)

        # Valores do serviço
        preco_servico = transacao_data.get('preco_servico', 0)
        desconto = transacao_data.get('desconto', 0)
        ganho_servico = preco_servico - desconto if desconto else preco_servico

        # Valores do produto
        preco_produto = transacao_data.get('preco_produtos', 0)
        ganho_produto = preco_produto

        collaborator = transacao_data.get('colaborador_id', 'N/A')
        name_collaborator = _scheduling_.collaborator_dict[collaborator]['nome']

        data_table.controls[0].rows.append(flet.DataRow(cells=[
            flet.DataCell(flet.Text(transacao_data.get('data', 'N/A'),
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text(name_collaborator,
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text(f'R$ {valor_total:.2f}',
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
        ],
            on_select_changed=lambda e, transacao=transacao_data, transacao_id=transacao_id: show_details(transacao, transacao_id)
        ))

        return ganho_servico, ganho_produto

    # Exibe o total ganho pelo atendente no mês selecionado
    def exibir_total_ganho(total_ganho_servico, total_ganho_produto, total_ganho, data_table):
        data_table.controls[0].rows.append(flet.DataRow(cells=[
            flet.DataCell(flet.Text("")),
            flet.DataCell(flet.Text("")),
            flet.DataCell(flet.Text("")),
        ]))

        data_table.controls[0].rows.append(flet.DataRow(cells=[
            flet.DataCell(flet.Text("Total Serviços",
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text("",
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text(f'R$ {total_ganho_servico:.2f}',
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
        ]))

        data_table.controls[0].rows.append(flet.DataRow(cells=[
            flet.DataCell(flet.Text("Total Produtos",
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text("",
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text(f'R$ {total_ganho_produto:.2f}',
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
        ]))

        data_table.controls[0].rows.append(flet.DataRow(cells=[
            flet.DataCell(flet.Text("Total",
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text("",
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
            flet.DataCell(flet.Text(f'R$ {total_ganho:.2f}',
                                    text_align="center",
                                    weight="bold",
                                    color=COLOR_TEXT_IN_FIELD)),
        ]))

        data_table.update()

    # Verifica se a tabela está vazia e atualiza a visibilidade dos componentes
    def verificar_tabela_vazia(data_table):
        if len(data_table.controls[0].rows) == 0:
            ocultar_tabela()

    # Oculta a tabela e exibe o texto "Não possui transações"
    def ocultar_tabela():
        _scheduling_.data_table.visible = False
        _scheduling_.data_table.update()
        _scheduling_.no_scheduling.visible = True
        _scheduling_.no_scheduling.update()

    async def return_page(e):
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
        "Receitas Atendente!",
        collaborator_ref,
        _visible_button,
        _on_date_change,
        return_page,
    )
    
    _scheduling_main = _main_column_()
    _scheduling_main.content.controls.append(flet.Container(padding=0))
    _scheduling_main.content.controls.append(_scheduling_)
    
    add_page(_scheduling_main)
   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER, port=8090)
