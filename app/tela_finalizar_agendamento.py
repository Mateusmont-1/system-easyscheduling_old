import flet
from functools import partial
from google.cloud.firestore_v1 import FieldFilter

from . import tela_verificar_agendamentos
from .firebase_config import get_firestore_client
from . import scheduling_db
from . import tela_transicao
from .config import COLOR_BORDER_COLOR_ERROR, COLOR_TEXT_IN_DROPDOWN, COLOR_BACKGROUND_CONTAINER,COLOR_BACKGROUND_BUTTON,COLOR_BACKGROUND_TEXT_FIELD,COLOR_TEXT_BUTTON,COLOR_TEXT,COLOR_TEXT_IN_BUTTON,COLOR_BORDER_COLOR,COLOR_TEXT_IN_FIELD

class UserWidget(flet.UserControl):
    def __init__(
        self,
        title:str,
        scheduling_id,   
        dict_scheduling,
        product_ref,
        service_ref,
        collaborator_ref,
        func1,
        func2,
        func3,
        ):
        self.title = title
        self.scheduling_id = scheduling_id
        self.dict_scheduling = dict_scheduling
        self.product_ref = product_ref
        self.service_ref = service_ref
        self.collaborator_ref = collaborator_ref
        self.func = func1
        self.func2 = func2
        self.func3 = func3
        
        self.name = dict_scheduling['nome']
        self.phone = dict_scheduling['telefone']
        self.data = f"{dict_scheduling['data']}"
        self.time = dict_scheduling['horario']
        self.price_service = dict_scheduling['preco_servico']
        self.service = dict_scheduling['servico_id']
        self.collaborator_id = dict_scheduling['colaborador_id']
        self.data_time = f'{self.data} as {self.time}'
        self.service_dict = {}
        self.product_dict = {}
        self.price_products = 0.0

        super().__init__()
    
    def InputTextField(self, text:str, hide:bool, value_text=None, read_only=False):
        return flet.Container(
            alignment=flet.alignment.center,
            content=flet.TextField(
                height=48,
                width=275,
                # bgcolor="#f0f3f6",
                bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                content_padding=10,
                text_size=12,
                read_only= read_only,
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
                                  on_change=partial(self.func2),
                                  )
            )
        
        self.service_choose2 = flet.Container(
            visible=True,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha outro serviço", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2),
                                  )
            )
        
        self.service_choose3 = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha outro serviço", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2),
                                  )
            )
        
        self.service_choose4 = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha outro serviço", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2),
                                  )
            )
        
        self.service_choose5 = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha outro serviço", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2),
                                  )
            )
        
        # Adicionando no dropdown a opção de nenhum serviço
        self.service_choose.content.options.append(flet.dropdown.Option(text= "Nenhum serviço", key= "Nenhum", ))
        self.service_choose2.content.options.append(flet.dropdown.Option(text= "Nenhum serviço", key= "Nenhum", ))
        self.service_choose3.content.options.append(flet.dropdown.Option(text= "Nenhum serviço", key= "Nenhum", ))
        self.service_choose4.content.options.append(flet.dropdown.Option(text= "Nenhum serviço", key= "Nenhum", ))
        self.service_choose5.content.options.append(flet.dropdown.Option(text= "Nenhum serviço", key= "Nenhum", ))

        self.service_dict["Nenhum"] = {'nome': 'Nenhum', 'preco': 0.0}

        for _service in self.service_ref:
            # Cada documento é um objeto com ID e dados
            service = self.service_choose.content
            service2 = self.service_choose2.content
            service3 = self.service_choose3.content
            service4 = self.service_choose4.content
            service5 = self.service_choose5.content
            _service_id = _service.id
            _service_data = _service.to_dict()
            
            if _service_data['permitir_agendamento']:
                _nome = f'{_service_data["nome"]} R${_service_data["preco"]}'
                #adiciona no dropdown o Servico
                service.options.append(flet.dropdown.Option(text= _nome, key= _service_id, ))
                service2.options.append(flet.dropdown.Option(text= _nome, key= _service_id, ))
                service3.options.append(flet.dropdown.Option(text= _nome, key= _service_id, ))
                service4.options.append(flet.dropdown.Option(text= _nome, key= _service_id, ))
                service5.options.append(flet.dropdown.Option(text= _nome, key= _service_id, ))

                self.service_dict[_service_id] = _service_data
        
        self.service_choose.content.value = self.service
        
        self.collaborator_choose = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha o(a) atendente",
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  )
            )
        
        for _collaborator in self.collaborator_ref:
            collaborator = self.collaborator_choose.content
            _collaborator_id = _collaborator.id
            _collaborator_date = _collaborator.to_dict()
            if _collaborator_date['permitir_agendamento']:
                _nome = f'{_collaborator_date["nome"]}'
                collaborator.options.append(flet.dropdown.Option(text= _nome, key=_collaborator_id))
            
        self.collaborator_choose.content.value = self.collaborator_id
        
        self.product_choose = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha outro produto", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_BUTTON),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_BUTTON,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2),
                                  )
            )
        
        self.product_choose2 = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha outro produto", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2),
                                  )
            )
        
        self.product_choose3 = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha outro produto", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2),
                                  )
            )
        
        self.product_choose4 = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha outro produto", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2),
                                  )
            )
        
        self.product_choose5 = flet.Container(
            visible=False,
            alignment=flet.alignment.center,
            content=flet.Dropdown(label="Escolha outro produto", 
                                  label_style=flet.TextStyle(color=COLOR_TEXT_IN_DROPDOWN),
                                  width=275,
                                  border_color=COLOR_BORDER_COLOR,
                                  color=COLOR_TEXT_IN_DROPDOWN,
                                  bgcolor=COLOR_BACKGROUND_TEXT_FIELD,
                                  on_change=partial(self.func2),
                                  )
            )
        
        # Adicionando opção para remover produto
        self.product_choose.content.options.append(flet.dropdown.Option(text= "Nenhum produto", key= "Nenhum", ))
        self.product_choose2.content.options.append(flet.dropdown.Option(text= "Nenhum produto", key= "Nenhum", ))
        self.product_choose3.content.options.append(flet.dropdown.Option(text= "Nenhum produto", key= "Nenhum", ))
        self.product_choose4.content.options.append(flet.dropdown.Option(text= "Nenhum produto", key= "Nenhum", ))
        self.product_choose5.content.options.append(flet.dropdown.Option(text= "Nenhum produto", key= "Nenhum", ))
        
        self.product_dict["Nenhum"] = {'nome': 'Nenhum', 'preco': 0.0}
        
        # Preenchendo os Dropdown de produto
        for _product in self.product_ref:
            product = self.product_choose.content
            product2 = self.product_choose2.content
            product3 = self.product_choose3.content
            product4 = self.product_choose4.content
            product5 = self.product_choose5.content
            
            _product_id = _product.id
            _product_date = _product.to_dict()
            
            if _product_date['permitir_venda']:
                _nome = f'{_product_date["nome"]} R${_product_date["preco"]}'
                product.options.append(flet.dropdown.Option(text= _nome, key=_product_id))
                product2.options.append(flet.dropdown.Option(text= _nome, key=_product_id))
                product3.options.append(flet.dropdown.Option(text= _nome, key=_product_id))
                product4.options.append(flet.dropdown.Option(text= _nome, key=_product_id))
                product5.options.append(flet.dropdown.Option(text= _nome, key=_product_id))
            
                self.product_dict[_product_id] = _product_date
            
        self._price = flet.Container(
            alignment=flet.alignment.center,
            content=flet.Text(
                value="Preço total",
                size=20,
                text_align="center",
                weight="bold",
                color=COLOR_TEXT,
            ),
        )
        
        self._finish = flet.Container(
            content=flet.ElevatedButton(
                on_click=partial(self.func),
                content=flet.Text(
                    "Finalizar agendamento",
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
                flet.Column(
                    spacing=12,
                    controls=[
                        self.InputTextField("Nome no agendamento!",
                                            False, self.name, True),
                        self.InputTextField("Telefone no agendamento!",
                                            False, self.phone, True),
                        self.InputTextField("Data e hora!",
                                            False, self.data_time, True),
                    ],
                ),
                self.collaborator_choose,
                self.service_choose,
                self.service_choose2,
                self.service_choose3,
                self.service_choose4,
                self.service_choose5,
                self.product_choose,
                self.product_choose2,
                self.product_choose3,
                self.product_choose4,
                self.product_choose5,
                self._price,
                flet.Column(
                    spacing=0,
                    controls=[
                        self.InputTextField("Preço total!",
                                            False, self.price_service),
                    ],
                ),
                flet.Container(padding=3),
                self._finish,
                self._back_button,
            ],
        )

async def main(page:flet.page, user, id_scheduling):
    page.title = "Finalizar agendamento"
    page.clean()
    
    db = get_firestore_client()
    service_ref = db.collection("servico").stream()

    scheduling_ref = db.collection("agendamentos").document(id_scheduling).get().to_dict()

    product_ref = db.collection("produto").stream()
    collaborator_ref = db.collection("colaborador").stream()

    list_services_select = list()
    list_products_select = list()
  
    def adicionar_dicionario(key, dicionario, lista):
        if key in dicionario and key != "Nenhum":
            produto = dicionario[key]
            lista.append({'nome': produto['nome'], 'preco': produto['preco']})

    def atualizar_visibilidade_widgets(widgets, dicionario, lista):
        total = 0
        for i in range(len(widgets) - 1):
            if widgets[i].content.value:
                key = widgets[i].content.value
                widgets[i + 1].visible = True
                widgets[i + 1].update()
                total += dicionario[key]['preco']
                adicionar_dicionario(key, dicionario, lista)
        return total

    async def widget_visible(e=None):
        # Obtendo referência dos widgets de serviço e produto
        service_selects = [
            _scheduling_.service_choose,
            _scheduling_.service_choose2,
            _scheduling_.service_choose3,
            _scheduling_.service_choose4,
            _scheduling_.service_choose5
        ]
        
        product_selects = [
            _scheduling_.product_choose,
            _scheduling_.product_choose2,
            _scheduling_.product_choose3,
            _scheduling_.product_choose4,
            _scheduling_.product_choose5,
        ]

        # Obtendo referência aos dicionários de produto e serviço
        product_dict = _scheduling_.product_dict
        service_dict = _scheduling_.service_dict

        # Limpando as listas antes do loop
        list_services_select.clear()
        list_products_select.clear()

        # Atualizando a visibilidade dos widgets e somando preços
        _scheduling_.soma_servico = atualizar_visibilidade_widgets(service_selects, service_dict, list_services_select)
        _scheduling_.soma_produto = atualizar_visibilidade_widgets(product_selects, product_dict, list_products_select)

        # Atualizando o preço total e a UI
        update_price()
        await _scheduling_.update_async()

    async def finish_scheduling(e):

        if not hasattr(_scheduling_, 'soma_servico') or _scheduling_.soma_servico is None:
            await widget_visible()

        if verifica_campos():
            # Obtendo referencia dos widget
            collaborator_id = _scheduling_.collaborator_choose.content.value
            service_id = _scheduling_.service_choose.content.value
            name_service = _scheduling_.service_dict[service_id]["nome"]
            price_services = float(_scheduling_.soma_servico)
            price_products = float(_scheduling_.soma_produto)
            price_total = float(
                str(
                    _scheduling_.controls[0].controls[14].controls[0].content.value
                    ).replace(',', "."))
        
            discount = (price_services + price_products) - price_total
        
            finish = scheduling_db.FinishScheduling(
                id_scheduling,
                collaborator_id,
                name_service,
                service_id,
                list_services_select,
                list_products_select,
                price_services,
                price_products,
                discount,
                price_total)
        
            finish.finish_scheduling()
            texto = "Agendamento finalizado!"
            await tela_transicao.main(page, user, texto)

    def update_price():    
    # def update_price(e):
         # Campo preço na tela
        price_page = _scheduling_.controls[0].controls[14].controls[0].content

        # Atualizar o valor total
        total_price = _scheduling_.soma_servico + _scheduling_.soma_produto
        price_page.value = total_price
        price_page.update()

    def verifica_campos():
        verifica = 0
        price_page = _scheduling_.controls[0].controls[14].controls[0].content
        
        if price_page.value == "":
            price_page.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        elif not converte_float(str(price_page.value).replace(',', ".")):
            price_page.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        elif float(str(price_page.value).replace(',', ".")) == 0.0:
            price_page.border_color = COLOR_BORDER_COLOR_ERROR
            verifica += 1
        
        else:
            price_page.error_text = None
            
        price_page.update()
        return True if verifica == 0 else None

    def converte_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    async def _back_button_(e):
        await tela_verificar_agendamentos.main(page,user)           
       
    def page_resize(e=None, inicio=None):
        if e:
            if page.width > 600:     
                largura = 600
                _scheduling_main.width = largura
                _scheduling_main.update()
            else:
                largura = page.width - 30
                _scheduling_main.width = largura
                _scheduling_main.update()
            if page.height > 600:     
                altura = 600
                _scheduling_main.height = altura
                _scheduling_main.update()
            else:
                altura = page.height - 60
                _scheduling_main.height = altura
                _scheduling_main.update()

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
        "Finalizar agendamento!",
        id_scheduling,
        scheduling_ref,
        product_ref,
        service_ref,
        collaborator_ref,
        finish_scheduling,
        widget_visible,
        _back_button_,
    )
    

    
    _scheduling_main = _main_column_()
    _scheduling_main.content.controls.append(flet.Container(padding=0))
    _scheduling_main.content.controls.append(_scheduling_)
    
    add_page(_scheduling_main)
   
# flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER, port=8080) 