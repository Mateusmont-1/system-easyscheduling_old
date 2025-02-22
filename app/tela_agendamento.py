# Implementação que eu realizei antes para tela_logyn.py

import flet
import datetime
from functools import partial
from google.cloud.firestore_v1 import FieldFilter
import asyncio

from . import tela_menu_main
from .firebase_config import get_firestore_client
from . import scheduling_db
from . import tela_transicao
from . import whatsapp
from .whatsapp import TELEFONE_CONTACT, CONTACT_NAME
from .config import COLOR_BACKGROUND_PAGE, COLOR_TEXT_IN_DROPDOWN, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        name:str,
        phone:str,
        service_ref,
        func1,
        func2,
        func3,
        func4,
        func5
        ):
        self.title = title
        self.name = name
        self.phone = phone
        self.service_ref = service_ref
        self.func = func1
        self.func2 = func2
        self.func3 = func3
        self.func4 = func4
        self.func5 = func5
        self.service_dict = {}
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
                text_size=12,
                color=COLOR_TEXT_IN_FIELD,
                value = value_text,
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

    def InputTextField2(self, text:str, hide:bool, value_text=None):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=275,
                keyboard_type="phone",
                bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                content_padding=10,
                text_size=12,
                color=COLOR_TEXT_IN_FIELD,
                value = value_text,
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
        self.service_choose = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha o Serviço",
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func5)
                                  )
            )
        
        for _service in self.service_ref:
            # Cada documento é um objeto com ID e dados
            service = self.service_choose.content
            _service_id = _service.id
            _service_data = _service.to_dict()
            
            if _service_data['permitir_agendamento']:
        
                _nome = f'{_service_data["nome"]} - R${_service_data["preco"]}'
                #adiciona no dropdown o Servico
                service.options.append(flet.dropdown.Option(text= _nome, key= _service_id,))
                self.service_dict[_service_id] = _service_data
            
        
        self.date_picker = flet.Container(
            alignment=flet.alignment.center,
            content=flet.DatePicker(
                first_date=datetime.datetime.now(),
                last_date=datetime.datetime.now() + datetime.timedelta(days=15),
                on_change=partial(self.func),
            )
            )
        
        self.day_choose = flet.Container(
            visible=False,
            content=flet.ElevatedButton(
                on_click=lambda _: self.date_picker.content.pick_date(),
                icon=flet.icons.CALENDAR_MONTH,
                text="Escolha o dia",
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
        
        self.hour_choose = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha o Horário",
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2)
                                  )
            )
        
        self.collaborator_choose = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha o(a) atendente",
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  )
            )
        
        self._register = flet.Container(
            content=flet.ElevatedButton(
                on_click=partial(self.func3),
                content=flet.Text(
                    "Realizar agendamento",
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
                on_click=partial(self.func4),
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
                flet.Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("Informe seu nome!",
                                            False, self.name),
                        self.InputTextField2("Informe seu telefone!",
                                            False, self.phone),
                    ],
                ),
                self.service_choose,
                self.day_choose,
                self.hour_choose,
                self.collaborator_choose,
                flet.Container(padding=3),
                self._register,
                self._back_button,
                self.date_picker,
            ],
        )

async def main(page: flet.Page, user):
    page.title = "Agendamento"
    page.clean()

    colaboradores_disponivel = {}
    horario_disponivel = []

    db = get_firestore_client()
    user_id = user['localId']
    user_ref = db.collection("usuarios").document(user_id)
    doc_user = user_ref.get().to_dict()

    name_user = doc_user['nome']
    phone_user = doc_user['telefone']

    async def _on_date_change(e=None):
        _scheduling_.hour_choose.visible = True
        _scheduling_.collaborator_choose.visible = True
        _scheduling_.update()
        hour_choose = _scheduling_.hour_choose.content
        collaborator_choose = _scheduling_.collaborator_choose.content
        hour_choose.value = None
        collaborator_choose.value = None
        hour_choose.update()
        collaborator_choose.update()
        selected_date = e.control.value if e else _scheduling_.date_picker.content.value
        data_formatada = datetime.datetime.strptime(str(selected_date), '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
        await verifica_horario(data_formatada)

    def _service_change(e):
        _scheduling_.day_choose.visible = True
        _scheduling_.update()
        if _scheduling_.date_picker.content.value:
            asyncio.create_task(_on_date_change())

    def string_to_time(time_str):
        return datetime.datetime.strptime(time_str, '%H:%M')

    def get_agendamentos(data_desejada):
        agendamentos_ref = db.collection('agendamentos')
        query = agendamentos_ref.where(
                    filter=FieldFilter('data', "==", data_desejada)
                ).where(
                    filter=FieldFilter('status_agendamento', 'in', ['Concluido', 'Em andamento'])
                ).stream()
        
        agendamentos = {}
        for agendamento in query:
            agendamento_data = agendamento.to_dict()
            colaborador_id = agendamento_data['colaborador_id']
            if colaborador_id not in agendamentos:
                agendamentos[colaborador_id] = []
            agendamentos[colaborador_id].append(agendamento_data)
        
        return agendamentos

    def periodo_disponivel(inicio, fim, agendamentos):
        for agendamento_data in agendamentos:
            horario_agendado_str = agendamento_data.get('horario')
            if horario_agendado_str:
                horario_agendado = string_to_time(horario_agendado_str)
                duracao_agendada = datetime.timedelta(minutes=int(agendamento_data['duracao_servico']))
                fim_agendado = horario_agendado + duracao_agendada
                if inicio < fim_agendado and fim > horario_agendado:
                    return False
        return True

    async def processa_colaborador(colaborador, data_formatada, dia_atual, mes_atual, hora_atual, duracao_servico, agendamentos):
        dados = colaborador.to_dict()
        dias_folga = dados.get('dias_folga', [])  
        dias_trabalhados = dados.get('dias_trabalhados', [0, 1, 2, 3, 4, 5, 6])
        if dados['permitir_agendamento'] and data_formatada not in dias_folga:
            id = colaborador.id
            dia, mes, ano = map(int, data_formatada.split("-"))
            data = datetime.date(year=ano, month=mes, day=dia)
            dia_semana = data.weekday()
            if dia_semana not in dias_trabalhados:
                return

            horarios_disponiveis = dados['dias_uteis'] if dia_semana < 5 else dados['sabado'] if dia_semana == 5 else dados['domingo']
            for hora in horarios_disponiveis:
                if len(horarios_disponiveis) <= 1 or (dia == dia_atual and mes == mes_atual and hora < hora_atual):
                    continue

                inicio_servico = string_to_time(hora)
                fim_servico = inicio_servico + duracao_servico
                if periodo_disponivel(inicio_servico, fim_servico, agendamentos.get(id, [])):
                    if id not in colaboradores_disponivel:
                        colaboradores_disponivel[id] = {"nome": dados["nome"], "horarios_disponivel": []}
                    colaboradores_disponivel[id]["horarios_disponivel"].append(hora)
                    if hora not in horario_disponivel:
                        horario_disponivel.append(hora)
                        horario_disponivel.sort()

    async def verifica_horario(data_formatada):
        colaborador_documents = db.collection("colaborador").stream()
        service_choose = _scheduling_.service_choose.content
        service_dict = _scheduling_.service_dict[service_choose.value]

        hour_choose = _scheduling_.hour_choose.content
        hour_choose.options.clear()
        collaborator_choose = _scheduling_.collaborator_choose.content
        collaborator_choose.options.clear()

        duracao_servico = datetime.timedelta(minutes=service_dict['duracao'])
        
        data_atual = datetime.datetime.now()
        dia_atual = data_atual.day
        mes_atual = data_atual.month
        hora_atual = data_atual.strftime('%H:%M')
        
        colaboradores_disponivel.clear()
        horario_disponivel.clear()

        agendamentos = get_agendamentos(data_formatada)
        
        tasks = [processa_colaborador(colaborador, data_formatada, dia_atual, mes_atual, hora_atual, duracao_servico, agendamentos) for colaborador in colaborador_documents]
        await asyncio.gather(*tasks)
        
        hour_choose.options = [flet.dropdown.Option(hora) for hora in horario_disponivel] if colaboradores_disponivel else [flet.dropdown.Option("Não possui horário disponivel")]
        hour_choose.update()

    def verifica_colaborador(e):
        horario_escolhido = e.control.value
        collaborator_choose = _scheduling_.collaborator_choose.content
        collaborator_choose.options = [flet.dropdown.Option(text=dados['nome'], key=id) for id, dados in colaboradores_disponivel.items() if horario_escolhido in dados["horarios_disponivel"]]
        collaborator_choose.update()

    async def agendar_corte(e):
        name_user = _scheduling_.controls[0].controls[1].controls[0].content
        phone_user = _scheduling_.controls[0].controls[1].controls[1].content
        service_choose = _scheduling_.service_choose.content
        day_choose = _scheduling_.date_picker.content.value
        hour_choose = _scheduling_.hour_choose.content
        collaborator_choose = _scheduling_.collaborator_choose.content
        verifica = verifica_campos(name_user, phone_user, service_choose, hour_choose, collaborator_choose)

        if verifica:
            service_dict = _scheduling_.service_dict[service_choose.value]
            day_choose = datetime.datetime.strptime(str(day_choose), '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')

            scheduling = scheduling_db.Scheduling(user, name_user.value, phone_user.value, service_choose.value, day_choose, hour_choose.value, collaborator_choose.value, service_dict)
            _scheduling = scheduling.create_scheduling()

            texto = "Agendamento realizado!"
            name_collaborator = colaboradores_disponivel[collaborator_choose.value]['nome']
            type_message = "novo_agendamento"

            mensagem = whatsapp.MessageSender()
            mensagem.send_message(phone_user.value, name_user.value, day_choose, hour_choose.value, name_collaborator, type_message)
            mensagem.send_contact(phone_user.value, TELEFONE_CONTACT)

            await tela_transicao.main(page, user, texto)

    def verifica_campos(name, phone, service_choose, hour_choose, collaborator_choose):
        phone_correto = phone.value.replace('-', "").replace("(", "").replace(")", "")
        name.border_color = '#FF0000' if not name.value else "#f0f3f6"
        phone.border_color = '#FF0000' if not phone.value or not (10 <= len(phone_correto) <= 11) else "#f0f3f6"
        service_choose.border_color = '#FF0000' if not service_choose.value else "#f0f3f6"
        collaborator_choose.border_color = '#FF0000' if not collaborator_choose.value else "#f0f3f6"
        hour_choose.border_color = '#FF0000' if not hour_choose.value else "#f0f3f6"
        
        name.update()
        phone.update()
        service_choose.update()
        collaborator_choose.update()
        hour_choose.update()
        
        return all([name.value, phone.value, 10 <= len(phone_correto) <= 11, service_choose.value, collaborator_choose.value, hour_choose.value])

    async def return_page(e):
        await tela_menu_main.main(page, user)
        
    def page_resize(e=None, inicio=None):
        largura = min(page.width - 30, 600) if page.width > 600 else page.width - 30
        altura = min(page.height - 60, 600) if page.height > 600 else page.height - 60
        if e:
            _scheduling_.width, _scheduling_.height = largura, altura
            _scheduling_.update()
        if inicio is not None:
            return largura if inicio else altura

    page.window.on_resized = page_resize

    def _main_column():
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
        
    def add_page(extruct):
        page.add(flet.Row(alignment="center", spacing=25, controls=[extruct]))

    _scheduling_ = UserWidget(
        "Agendamento!",
        name_user,
        phone_user,
        db.collection("servico").stream(),
        _on_date_change,
        verifica_colaborador,
        agendar_corte,
        return_page,
        _service_change,
    )
    
    _scheduling_main = _main_column()
    _scheduling_main.content.controls.append(flet.Container(padding=0))
    _scheduling_main.content.controls.append(_scheduling_)
    
    add_page(_scheduling_main)
   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER) 