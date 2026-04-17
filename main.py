import requests
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from datetime import datetime, timedelta
import math

# Configuração de Caminhos e Conexão
DIRETORIO_APP = os.path.dirname(os.path.abspath(__file__))
CAMINHO_LOGO = os.path.join(DIRETORIO_APP, 'logo.png')
URL_BASE = "http://192.168.1.86:5000"

# --- CLASSE PARA O FUNDO GRID ANIMADO NEON CORRIGIDO ---
class FundoGridNeon(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0
        with self.canvas.before:
            # Fundo Azul Marinho Profundo
            Color(0.01, 0.05, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            # Cor das Linhas Neon
            self.cor_linha = Color(0.8, 1, 1, 0.3)
        
        self.bind(size=self.atualizar_fundo, pos=self.atualizar_fundo)
        Clock.schedule_interval(self.animar_grid, 1 / 60)

    def atualizar_fundo(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def animar_grid(self, dt):
        self.time += dt
        self.cor_linha.a = 0.2 + 0.15 * math.sin(self.time * 2)
        
        self.canvas.before.remove_group('linhas')
        with self.canvas.before:
            Color(self.cor_linha.r, self.cor_linha.g, self.cor_linha.b, self.cor_linha.a, group='linhas')
            w, h = self.size
            esp = 60
            vel = 15
            
            offset_y = (self.time * vel) % esp
            for y in range(int(offset_y), h, esp):
                Line(points=[0, y, w, y], width=1, group='linhas')
                
            offset_x = (self.time * vel * 0.5) % esp
            for x in range(int(offset_x), w, esp):
                Line(points=[x, 0, x, h], width=1, group='linhas')

def MarcaDagua():
    return Label(text="Desenvolvido por: Rafael Drones", font_size='12sp', color=(1, 1, 1, 0.3), size_hint_y=None, height=30)

# --- TELA 1: MENU ---
class TelaMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        fundo = FundoGridNeon()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        cabecalho = BoxLayout(orientation='horizontal', size_hint_y=None, height=150, spacing=10)
        if os.path.exists(CAMINHO_LOGO):
            cabecalho.add_widget(Image(source=CAMINHO_LOGO))
            cabecalho.add_widget(Label(text="BEM VINDO", font_size='28sp', bold=True, color=(1, 0.8, 0, 1), size_hint_x=2))
            cabecalho.add_widget(Image(source=CAMINHO_LOGO))
        else:
            cabecalho.add_widget(Label(text="BEM VINDO", font_size='32sp', bold=True, color=(1, 0.8, 0, 1)))

        layout.add_widget(cabecalho)
        
        box_btn = BoxLayout(orientation='vertical', padding=[20, 50], spacing=30)
        btn_add = Button(text="[+] CADASTRAR PRODUTO", font_size='20sp', bold=True, background_color=(0, 0.6, 0.3, 1), background_normal='')
        btn_add.bind(on_press=lambda x: setattr(self.manager, 'current', 'adicionar'))
        
        btn_ver = Button(text="[🔍] VER ESTOQUE", font_size='20sp', bold=True, background_color=(0, 0.4, 0.7, 1), background_normal='')
        btn_ver.bind(on_press=self.ir_para_lista)
        
        box_btn.add_widget(btn_add); box_btn.add_widget(btn_ver)
        layout.add_widget(box_btn); layout.add_widget(MarcaDagua())
        
        fundo.add_widget(layout)
        self.add_widget(fundo)

    def ir_para_lista(self, instance):
        self.manager.get_screen('lista').atualizar_lista()
        self.manager.current = 'lista'

# --- TELA 2: ADICIONAR ---
class TelaAdicionar(Screen):
    def on_enter(self): self.nome.focus = True
    def __init__(self, **kw):
        super().__init__(**kw)
        fundo = FundoGridNeon()
        layout = BoxLayout(orientation='vertical', padding=20)
        form = BoxLayout(orientation='vertical', padding=[10, 20], spacing=15)
        
        form.add_widget(Label(text="NOVO CADASTRO", font_size='20sp', bold=True, color=(1, 0.8, 0, 1)))
        self.nome = TextInput(hint_text="Nome do Produto", multiline=False, font_size='18sp', write_tab=False)
        self.venc = TextInput(hint_text="Data: DDMM", multiline=False, font_size='18sp', write_tab=False)
        self.venc.bind(text=self.aplicar_mascara)
        self.prazo = TextInput(text="1", multiline=False, font_size='18sp', write_tab=False)

        form.add_widget(self.nome); form.add_widget(self.venc); form.add_widget(self.prazo)
        
        btn_s = Button(text="SALVAR", bold=True, height=60, size_hint_y=None, background_color=(0, 0.8, 0, 1), background_normal='')
        btn_s.bind(on_press=self.enviar)
        btn_v = Button(text="VOLTAR", height=50, size_hint_y=None, background_color=(0.7, 0, 0, 1), background_normal='')
        btn_v.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        
        form.add_widget(btn_s); form.add_widget(btn_v)
        layout.add_widget(form); layout.add_widget(MarcaDagua())
        fundo.add_widget(layout); self.add_widget(fundo)

    def aplicar_mascara(self, instance, value):
        puro = "".join(filter(str.isdigit, value))
        if len(puro) >= 4:
            novo = puro[:2] + '/' + puro[2:4]
            if instance.text != novo: instance.text = novo
        if len(instance.text) > 5: instance.text = instance.text[:5]

    def enviar(self, *args):
        try:
            dia_mes = self.venc.text
            venc_dt = datetime.strptime(f"{dia_mes}/{datetime.now().year}", "%d/%m/%Y")
            if venc_dt < datetime.now() - timedelta(days=1): venc_dt = venc_dt.replace(year=venc_dt.year + 1)
            alerta_dt = venc_dt - timedelta(days=int(self.prazo.text))
            dados = {"produto": self.nome.text.upper(), "vencimento": venc_dt.strftime('%d/%m/%Y'), "alerta": alerta_dt.strftime('%d/%m/%Y')}
            requests.post(f"{URL_BASE}/adicionar", json=dados, timeout=5)
            self.nome.text = ""; self.venc.text = ""; self.manager.current = 'menu'
        except: self.venc.text = ""; self.venc.hint_text = "ERRO"

# --- TELA 3: LISTA (COM FUNDO PARA OS ITENS) ---
class ItemLista(BoxLayout):
    def __init__(self, texto_info, id_item, callback_del, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 90
        self.padding = 10
        self.spacing = 10

        # Fundo sólido para o item não confundir com o grid neon
        with self.canvas.before:
            Color(0.1, 0.15, 0.3, 0.9) # Azul escuro sólido
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.add_widget(Label(text=texto_info, halign='left', valign='middle', font_size='13sp'))
        btn = Button(text="APAGAR", size_hint_x=None, width=90, background_color=(1, 0, 0, 1), background_normal='')
        btn.bind(on_press=lambda x: callback_del(id_item))
        self.add_widget(btn)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class TelaLista(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.fundo = FundoGridNeon()
        layout_p = BoxLayout(orientation='vertical', padding=10)
        self.container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.container.bind(minimum_height=self.container.setter('height'))
        
        scroll = ScrollView(); scroll.add_widget(self.container)
        layout_p.add_widget(Label(text="ESTOQUE CENTRAL", bold=True, size_hint_y=None, height=40))
        layout_p.add_widget(scroll)
        
        btn_v = Button(text="VOLTAR", size_hint_y=None, height=60, background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        btn_v.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        layout_p.add_widget(btn_v); layout_p.add_widget(MarcaDagua())
        
        self.fundo.add_widget(layout_p)
        self.add_widget(self.fundo)

    def atualizar_lista(self):
        self.container.clear_widgets()
        try:
            res = requests.get(f"{URL_BASE}/listar", timeout=5)
            for item in res.json():
                txt = f"📦 {item['produto']}\nVenc: {item['vencimento']} | Alerta: {item['alerta']}"
                self.container.add_widget(ItemLista(txt, item['id'], self.apagar))
        except: self.container.add_widget(Label(text="SERVIDOR OFF-LINE"))

    def apagar(self, item_id):
        try:
            requests.delete(f"{URL_BASE}/apagar_item/{item_id}", timeout=5)
            self.atualizar_lista()
        except: pass

class AppNossaConveniencia(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaMenu(name='menu'))
        sm.add_widget(TelaAdicionar(name='adicionar'))
        sm.add_widget(TelaLista(name='lista'))
        return sm

if __name__ == "__main__":
    AppNossaConveniencia().run()