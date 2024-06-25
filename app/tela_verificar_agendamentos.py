import flet
import datetime
from functools import partial
from google.cloud.firestore_v1 import FieldFilter
import asyncio

from . import tela_menu_main
from . import tela_finalizar_agendamento
from . import scheduling_db
from . import whatsapp
from .whatsapp import TELEFONE_CONTACT, CONTACT_NAME
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
        
        self.collaborator_documents = dict()
    
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
        
        for colaborador in self.collaborator_ref:
            # Cada documento é um objeto com ID e dados
            colaborador_dropdown = self.collaborator_choose.content
            _colaborador_id = colaborador.id
            _colaborador_data = colaborador.to_dict()
        
            _nome = _colaborador_data['nome']
            
            # adiciona no dropdown o atendente
            colaborador_dropdown.options.append(flet.dropdown.Option(text= _nome, key= _colaborador_id,))

            self.collaborator_documents[_colaborador_id] = _colaborador_data
            
        
        self.date_picker = flet.Container(
            alignment=flet.alignment.center,
            content=flet.DatePicker(
                first_date=datetime.datetime(year=2024, month=6, day=1),
                last_date=datetime.datetime.now() + datetime.timedelta(days=15),
                on_change=partial(self.func2)
            )
            )
        
        self.day_choose = flet.Container(
            visible=False,
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
        
        self.data_table = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Row(
                scroll=True,
                controls=[flet.DataTable(
                    columns=[
                        flet.DataColumn(flet.Text("Data/Hora",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD,)),
                        flet.DataColumn(flet.Text("Status",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                        flet.DataColumn(flet.Text("Nome do cliente",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD)),
                        flet.DataColumn(flet.Text("Serviço agendado",
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
                value="Não possui agendamentos",
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
                self.day_choose,
                flet.Container(padding=3),
                self.data_table,
                self.date_picker,
                self.no_scheduling,
                self._back_button,
            ],
        )

async def main(page:flet.page, user):
    page.title = "Verificar agendamentos"
    # page.bgcolor = "#f0f3f6"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.theme_mode = "dark"
    page.clean()
    
    id_finish = ""
    dict_agendamento = dict()
    
    db = get_firestore_client()
    collaborator_ref = db.collection("colaborador").stream()
    
    async def _visible_button(e):
        dropdown = e.control.value
        _scheduling_.day_choose.visible = True
        _scheduling_.day_choose.update()

        if _scheduling_.date_picker.content.value != None:
            await _on_date_change()
    
    def show_details(row_data, id):
        nonlocal id_finish
        # dialog.content.controls = [flet.Text(f"{key}: {value}") for key, value in row_data.items()]
        dialog.content.controls = [
            flet.Text(f"Data: {row_data['data']}"),
            flet.Text(f"Hórario: {row_data['horario']}"),
            flet.Text(f"Nome: {row_data['nome']}"),
            flet.Text(f"Telefone: {row_data['telefone']}"),
            flet.Text(f"Serviço: {row_data['nome_servico']}"),
            flet.Text(f"Preço: R${row_data['preco_servico']}"),
            flet.Text(f"Duração: {row_data['duracao_servico']} min"),
            flet.Text(f"Status: {row_data['status_agendamento']}"),
        ]
        dialog.open = True
        id_finish = id
        page.update()

    id_finish = None
    def close_dialog():
        dialog.open = False
        page.update()

    # Função para finalizar o agendamento
    async def tela_finalizar(e):
        close_dialog()
        await asyncio.sleep(0.1)
        await tela_finalizar_agendamento.main(page, user, id_finish)

    # Função para abrir o CupertinoAlertDialog para confirmar cancelamento
    async def dismiss_cancel_dialog(e):
        cancel_dialog.open = False
        page.update()
        await asyncio.sleep(0.1)
        page.dialog = dialog  # Redefine o dialog original
        page.update()
        close_dialog()
    
    async def cancelar_agendamento(e):

        _dict_agendamento = dict_agendamento[id_finish]
        # Obtendo valores para enviar a mensagem no whatsapp
        _phone = _dict_agendamento['telefone']
        _name = _dict_agendamento['nome']
        _day_choose = _dict_agendamento['data']
        _hour_choose = _dict_agendamento['horario']
        _collaborator_choose = _dict_agendamento['colaborador_id']
        _collaborator_name = _scheduling_.collaborator_documents[_collaborator_choose]['nome']
        
        texto = "Agendamento cancelado!"

        mensagem_texto = f"""*Mensagem automática*

Olá {_name},
    
O seu agendamento foi cancelado para o dia *{_day_choose} as {_hour_choose}* com o(a) {_collaborator_name},
            
Para qualquer informação, ou alteração entrar em contato com contato abaixo,

Atenciosamente,
*Sistema EasyScheduling*"""

        mensagem = whatsapp.MessageSender()
        mensagem_enviada = mensagem.send_message(_phone, mensagem_texto)
        mensagem_contato = mensagem.send_contact(_phone, TELEFONE_CONTACT)

        cancelar = scheduling_db.CancelScheduling(id_finish)
        _cancelar = cancelar.cancel_scheduling()
        cancel_dialog.open = False
        page.update()
        await asyncio.sleep(0.1)
        page.dialog = dialog  # Redefine o dialog original
        page.update()
        close_dialog()

        await _on_date_change()

    def open_cancel_dialog(e):
        global cancel_dialog
        cancel_dialog = flet.CupertinoAlertDialog(
            title=flet.Text("Atenção"),
            content=flet.Text("Você tem certeza que deseja cancelar o agendamento?"),
            actions=[
                flet.CupertinoDialogAction("OK", is_destructive_action=True, on_click=cancelar_agendamento),
                flet.CupertinoDialogAction(text="Cancel", on_click=dismiss_cancel_dialog),
            ],
        )
        e.control.page.dialog = cancel_dialog
        cancel_dialog.open = True
        e.control.page.update()

    # Configuração do dialog principal
    dialog = flet.AlertDialog(
        scrollable=True,
        title=flet.Text("Detalhes do Agendamento"),
        content=flet.Column([
            # Adicione aqui os detalhes do agendamento que você deseja exibir
        ]),
        actions=[
            flet.TextButton("Finalizar Agendamento", on_click=tela_finalizar),
            flet.TextButton("Cancelar Agendamento", on_click=open_cancel_dialog),
            flet.TextButton("Fechar", on_click=lambda _: close_dialog()),
        ],
    )

    page.dialog = dialog

    async def _on_date_change(e=None):
        if e:
            selected_date = e.control.value
        else:
            selected_date = _scheduling_.date_picker.content.value
        
        collaborator_choose = _scheduling_.collaborator_choose.content
        data_table = _scheduling_.data_table.content
        data_table.controls[0].rows.clear()
        await data_table.update_async()

        data_objeto = datetime.datetime.strptime(str(selected_date), '%Y-%m-%d %H:%M:%S')
        data_formatada = data_objeto.strftime('%d-%m-%Y')
        
        agendamentos_ref = db.collection("agendamentos")
        query = agendamentos_ref.where(filter=FieldFilter('data', '==', data_formatada)
                                    ).where(filter=FieldFilter("colaborador_id", "==", collaborator_choose.value))
        agendamentos = query.stream()
        
        lista_agendamentos = list(agendamentos)

        def sort_key(agendamento):
            agenda = agendamento.to_dict()
            status = agenda.get('status_agendamento', 'N/A')
            horario = agenda.get('horario', '23:59')
            
             # Prioriza agendamentos com horário e status "Em andamento"
            if 'horario' in agenda and status == "Em andamento":
                return (0, horario)
            # Agendamentos com horário e status "Concluido" vêm depois
            elif 'horario' in agenda and status == "Concluido":
                return (1, horario)
            # Agendamentos sem horário e com status "Concluido" vêm antes dos cancelados
            elif 'horario' not in agenda and status == "Concluido":
                return (2, horario)
            # Agendamentos cancelados vêm por último
            elif status == "Cancelado":
                return (3, horario)
            # Agendamentos sem horário e sem status "Em andamento" ou "Concluido" vêm por último
            else:
                return (4, horario)


        lista_agendamentos.sort(key=sort_key)

        if len(lista_agendamentos) != 0:
            _scheduling_.data_table.visible = True
            await _scheduling_.data_table.update_async()
            _scheduling_.no_scheduling.visible = False
            await _scheduling_.no_scheduling.update_async()
            for agendamento in lista_agendamentos:
                agenda_id = agendamento.id
                agenda = agendamento.to_dict()
                if agenda['status_agendamento'] == "Em andamento":
                    data = agenda.get('data', 'N/A')
                    hora = agenda.get('horario', 'N/A')
                    data_hora = data + " as " + hora
                    data_table.controls[0].rows.append(flet.DataRow(cells=[
                        flet.DataCell(flet.Text(data_hora, text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                        flet.DataCell(flet.Text(agenda['status_agendamento'], text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                        flet.DataCell(flet.Text(agenda['nome'], text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                        flet.DataCell(flet.Text(agenda['nome_servico'], text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                    ], on_select_changed=lambda e, agenda=agenda, agenda_id=agenda_id: show_details(agenda, agenda_id)))
                    dict_agendamento[agenda_id] = agenda
                    await data_table.update_async()
                elif agenda['status_agendamento'] == "Concluido" or agenda['status_agendamento'] == "Cancelado":
                    data = agenda.get('data', 'N/A')
                    hora = agenda.get('horario', 'N/A')
                    data_hora = data + " as " + hora
                    data_table.controls[0].rows.append(flet.DataRow(cells=[
                        flet.DataCell(flet.Text(data_hora, text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                        flet.DataCell(flet.Text(agenda['status_agendamento'], text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                        flet.DataCell(flet.Text(agenda.get('nome', 'N/A'), text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                        flet.DataCell(flet.Text(agenda['nome_servico'], text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                    ]))
                    await data_table.update_async()
            if len(data_table.controls[0].rows) == 0:
                _scheduling_.data_table.visible = False
                await _scheduling_.data_table.update_async()
                _scheduling_.no_scheduling.visible = True
                await _scheduling_.no_scheduling.update_async()
        else:
            _scheduling_.data_table.visible = False
            await _scheduling_.data_table.update_async()
            _scheduling_.no_scheduling.visible = True
            await _scheduling_.no_scheduling.update_async()
    
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
        "Verificar agendamentos!",
        collaborator_ref,
        _visible_button,
        _on_date_change,
        _back_button,
    )
    

    
    _scheduling_main = _main_column_()
    _scheduling_main.content.controls.append(flet.Container(padding=0))
    _scheduling_main.content.controls.append(_scheduling_)
    
    add_page(_scheduling_main)

# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)
