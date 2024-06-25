import flet
import datetime
from functools import partial
from google.cloud.firestore_v1 import FieldFilter
import asyncio

from . import tela_menu_main
from . import tela_finalizar_agendamento
from . import scheduling_db
from . import register
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
        ):
        super().__init__()
        self.title = title
        self.collaborator_ref = collaborator_ref
        self.func = func1
        self.func2 = func2

        
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
        
        self.day_off = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Row(
                scroll=True,
                controls=[flet.DataTable(
                    columns=[
                        flet.DataColumn(flet.Text("Dias de folga",
                                              text_align="center",
                                              weight="bold",
                                              color=COLOR_TEXT_IN_FIELD,)),
                    ]
                )
                ]
            ) 
        )
        
        self.no_day_off = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Text(
                value="Não possui folgas",
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
                self.collaborator_choose,
                flet.Container(padding=3),
                self.day_off,
                self.no_day_off,
                self._back_button,
            ],
        )

async def main(page:flet.page, user):
    page.title = "Verificar folgas"
    # page.bgcolor = "#f0f3f6"
    # page.horizontal_alignment = "center"
    # page.vertical_alignment = "center"
    # page.theme_mode = "dark"
    page.clean()
    
    colaborador = None
    dia = None
    
    db = get_firestore_client()
    collaborator_ref = db.collection("colaborador").stream()
    
    async def _check_day_off(e=None):
        if e:
            collaborator_choose = e.control.value
        else:
            collaborator_choose = _scheduling_.collaborator_choose.content.value
            collaborator_update = db.collection("colaborador").stream()
            documents = _scheduling_.collaborator_documents
            documents.clear()
            for colaborador in collaborator_update:
                # Cada documento é um objeto com ID e dados
                _colaborador_id = colaborador.id
                _colaborador_data = colaborador.to_dict()

                documents[_colaborador_id] = _colaborador_data
        

        day_off_table = _scheduling_.day_off
        no_day_off = _scheduling_.no_day_off
        collaborator_ref = _scheduling_.collaborator_documents[collaborator_choose]
        day_off_collaborator = collaborator_ref.get('dias_folga', False)
        if day_off_collaborator:
            no_day_off.visible = False
            day_off_collaborator.sort()
            day_off_table.content.controls[0].rows.clear()
            current_date = datetime.datetime.now().date()
            for day in day_off_collaborator:
                day_date = datetime.datetime.strptime(day, "%d-%m-%Y").date()
                if day_date >= current_date:
                    day_off_table.visible = True
                    day_off_table.content.controls[0].rows.append(flet.DataRow(cells=[
                            flet.DataCell(flet.Text(day, text_align="center", weight="bold", color=COLOR_TEXT_IN_FIELD)),
                        ], on_select_changed=lambda e,collaborator_choose=collaborator_choose ,collaborator_ref=collaborator_ref, day=day: show_details(collaborator_choose, collaborator_ref, day)))
            if len(day_off_table.content.controls[0].rows) == 0:
                no_day_off.visible = True
                day_off_table.visible = False
        else:
            no_day_off.visible = True
            day_off_table.visible = False
        no_day_off.update()
        day_off_table.update()
    
    def show_details(collaborator_choose, collaborator, day):
        nonlocal colaborador, dia
        dia = day
        colaborador = collaborator_choose
        cancel_dialog = flet.CupertinoAlertDialog(
            title=flet.Text("Atenção"),
            content=flet.Text(f"Você tem certeza que deseja cancelar a folga do dia {day} do colaborador {collaborator['nome']}?"),
            actions=[
                flet.CupertinoDialogAction("OK", is_destructive_action=True, on_click=cancelar_folga),
                flet.CupertinoDialogAction(text="Cancel", on_click=dismiss_cancel_dialog),
            ],
        )
        page.dialog = cancel_dialog
        page.dialog.open = True
        page.update()

    # Função para abrir o CupertinoAlertDialog para confirmar cancelamento
    async def dismiss_cancel_dialog(e=None):
        page.dialog.open = False
        page.update()
        await asyncio.sleep(0.1)
    
    async def cancelar_folga(e):
        cancel = register.CollaboratorLeaveCancellationManager(colaborador)
        confirma = cancel.cancelar_dia_folga(dia)
        await dismiss_cancel_dialog()
        await _check_day_off()

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
        "Verificar folgas!",
        collaborator_ref,
        _check_day_off,
        _back_button,
    )

    _scheduling_main = _main_column_()
    _scheduling_main.content.controls.append(flet.Container(padding=0))
    _scheduling_main.content.controls.append(_scheduling_)
    
    add_page(_scheduling_main)

# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)