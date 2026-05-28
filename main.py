import kivy
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

# BASE DE DADOS
POSTOS_COLETA = [
    {"nome": "COOP Belford Roxo", "materiais": "eletrônicos, plásticos, cabos, papéis, recicláveis",
     "endereco": "Rua Ptolomeu, 48 - Jardim Gláucia",
     "link_mapa": "https://www.google.com/maps/search/?api=1&query=Rua+Ptolomeu+48+Jardim+Gláucia+Belford+Roxo"},
    {"nome": "Trexfer", "materiais": "metais, sucatas, eletrônicos",
     "endereco": "Rua 28 de Setembro, 15 - Rocha Sobrinho",
     "link_mapa": "https://www.google.com/maps/search/?api=1&query=Rua+Vinte+e+Oito+de+Setembro+15+Rocha+Sobrinho+Belford+Roxo"},
    {"nome": "Ecobel Reciclagem", "materiais": "recicláveis, eletrônicos, celular, baterias, plástico",
     "endereco": "Av. José Mariano Passos, 1290 - Prata",
     "link_mapa": "https://www.google.com/maps/search/?api=1&query=Av+José+Mariano+Passos+1290+Prata+Belford+Roxo"}
]

# PARTE EDUCACIONAL (Fundamentação INEA)
TEXTO_EDUCATIVO = (
    "=== GUIA AMBIENTAL INEA ===\n\n"
    "O descarte irregular de eletrônicos contamina o solo e lençóis freáticos de Belford Roxo.\n\n"
    "• CHUMBO: Danos ao sistema nervoso e rins.\n"
    "• MERCÚRIO: Bioacumulativo, causa distúrbios neurológicos graves.\n"
    "• CÁDMIO: Substância cancerígena que se acumula no organismo.\n\n"
    "Ao reciclar, você impede a lixiviação destes metais no ecossistema local."
)


class InterfaceApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        self.link_atual_mapa = None

        self.add_widget(Label(text="Descarte Correto - Belford Roxo", size_hint_y=0.08, bold=True))

        self.entrada = TextInput(hint_text="Digite o material (ex: eletrônicos)...", size_hint_y=0.08, multiline=False)
        self.add_widget(self.entrada)

        # Botões de Ação
        layout_botoes = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=10)
        btn_buscar = Button(text="Buscar Posto", background_color=(0.2, 0.6, 0.2, 1))
        btn_buscar.bind(on_press=self.executar_busca)

        btn_educativo = Button(text="Guia Ambiental", background_color=(0.1, 0.4, 0.7, 1))
        btn_educativo.bind(on_press=self.exibir_educacao)

        layout_botoes.add_widget(btn_buscar)
        layout_botoes.add_widget(btn_educativo)
        self.add_widget(layout_botoes)

        self.btn_rota = Button(text="Ver Rota no Mapa", size_hint_y=0.08, background_color=(0.5, 0.5, 0.5, 1),
                               disabled=True)
        self.btn_rota.bind(on_press=self.abrir_rota)
        self.add_widget(self.btn_rota)

        self.scroll = ScrollView(size_hint_y=0.5)
        self.lbl_resultado = Label(text="Bem-vindo! Busque um posto ou leia o Guia Ambiental.", size_hint_y=None,
                                   halign='left', valign='top')
        self.lbl_resultado.bind(texture_size=self.lbl_resultado.setter('size'))
        self.lbl_resultado.text_size = (400, None)
        self.scroll.add_widget(self.lbl_resultado)
        self.add_widget(self.scroll)

    def executar_busca(self, instance):
        termo = self.entrada.text.strip().lower()
        res = next((p for p in POSTOS_COLETA if termo in p["materiais"].lower()), None)
        if res:
            self.lbl_resultado.text = f"PONTO: {res['nome']}\nENDEREÇO: {res['endereco']}\nMATERIAIS: {res['materiais']}"
            self.link_atual_mapa = res["link_mapa"]
            self.btn_rota.disabled = False
        else:
            self.lbl_resultado.text = "Nenhum ponto encontrado para este material."

    def exibir_educacao(self, instance):
        self.lbl_resultado.text = TEXTO_EDUCATIVO
        self.btn_rota.disabled = True

    def abrir_rota(self, instance):
        if self.link_atual_mapa: webbrowser.open(self.link_atual_mapa)


class MainApp(App):
    def build(self): return InterfaceApp()


if __name__ == "__main__": MainApp().run()