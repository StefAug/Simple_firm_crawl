from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from functools import partial
from kivy.core.window import Window
from kivy.uix.image import Image

import requests
import urllib.request as req

from bs4 import BeautifulSoup

class firma:
    def __init__(self,name,simb,bid_ask,bid_vol,date,time,last_price,var,var_p,open_price,high_price,low_price,avg_price,w52_high,w52_low,market_cap,PER,EPS,Dividend,no_shares,nominal_value,share_capital):
        self.name=name
        self.simb=simb
        self.bid_ask=bid_ask
        self.bid_vol=bid_vol
        self.date=date
        self.time=time
        self.last_price=last_price
        self.var=var
        self.var_p=var_p
        self.open_price=open_price
        self.high_price=high_price
        self.low_price=low_price
        self.avg_price=avg_price
        self.w52_high=w52_high
        self.w52_low=w52_low
        self.market_cap=market_cap
        self.PER=PER
        self.EPS=EPS
        self.Dividend=Dividend
        self.no_shares=no_shares
        self.nominal_value=nominal_value
        self.share_capital=share_capital
    def return_bid(self):
        return self.bid_ask
    def set_name(self,name):
        self.name=name
 
 
def img_dwn(imgurl, img_name):
    req.urlretrieve(imgurl,img_name)

def crawl():
   
    site_simb=[]
    firm_simb=[]
    tbody=[]
    nr_date=0
    headers = {'User-Agent': 'Mozilla/5.0'}
   
    url = "http://www.bvb.ro/FinancialInstruments/Markets/Shares"
       
    r = requests.get(url, headers=headers)
    firme=list()   
    soup = BeautifulSoup(r.text, 'html.parser')
    loose_detail = [c.get_text(separator=' ') for c in soup.findAll('table')[0].findAll('tr')]
    for o in loose_detail:
       site_simb.append(o.split())
    for x in site_simb:
        firm_simb.append(x[0])
    for simb in firm_simb[1:20]:
        
        urlo="http://www.bvb.ro/FinancialInstruments/Details/FinancialInstrumentsDetails.aspx?s="+simb
        ra = requests.get(urlo, headers=headers)
        soup=BeautifulSoup(ra.text,'html.parser')
       
        urlw="https://www.tradeville.eu/actiuni/actiuni-"+simb+"#cotatii"
        rw = requests.get(urlw, headers=headers)
        soup2=BeautifulSoup(rw.text,'html.parser')
        for x in soup2.findAll("img",{"id":"graficpoza"}):
           img_dwn(str(x['src']),"img"+str(nr_date)+".jpg")
       
        table=soup.find("div",{"class":"boxed-panel"})
        o=str(table.get_text()).split()
        firme.append(firma("blank",str(simb),str(o[4])+str(o[5])+str(o[6]),str(o[11])+str(o[12])+str(o[13]),str(o[14]),str(o[15])+str(o[16]),str(o[18]),str(o[19]),str(o[21]),str(o[23]),str(o[25]),str(o[27]),str(o[29]),str(o[35]),str(o[38]),str(o[41]),str(o[42]),str(o[44]),str(o[52]),str(o[54]),str(o[56]),str(o[57])))
        nr_date=nr_date+1
    return firme

crawl()
def crawl_basic():
    html_exit=open("Dev_Ext.txt","w+")

    headers = {'User-Agent': 'Mozilla/5.0'}
    
    url = "http://www.bvb.ro/FinancialInstruments/Markets/Shares"
    
    r = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    loose = [c.get_text(separator='') for c in soup.findAll('table')[0].findAll('tr')]
    abc=[]
    for o in loose:
        abc.append(o.split()[1:3])
    return abc


Builder.load_string('''

<RecView>:
 
    viewclass: 'Button'
    width: 100
    RecycleBoxLayout:
        width: root.width
        size_hint_y: None
 
        height: self.minimum_height
 
        orientation: 'vertical'
 
''')

class BackLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(26 / 256, 140 / 256, 255 / 256, 1)
            Rectangle(pos=self.pos, size=self.size)


class RecView(RecycleView):
 
    def __init__(self, **kwargs):
 
        super(RecView, self).__init__(**kwargs)
 
        self.data = {}

    def appendData(self, txt, action):
        self.data.append({'text':txt, 'height':30, 'on_release':action})


class GUIApp(App):
    
    
    def build(self):
        Window.clearcolor = (0, 89 / 256, 179 / 256, 1)
        self.lista_firme=crawl()
        self.box = BoxLayout(orientation = 'horizontal') #container
        self.grid1 = GridLayout(cols = 2, padding = 10) #first grid
        self.auxgrid = GridLayout(cols = 1, padding = 10, size_hint_x = None)
        self.grid2 = GridLayout(cols = 1, padding = 10) #second grid
        self.grid3 = GridLayout(cols = 2) #third grid
        self.menu = RecView() #scroll menu
        self.chart = BoxLayout(orientation = 'horizontal')
        self.screen1 = BoxLayout(orientation = 'horizontal')
        self.screen2 = BoxLayout(orientation = 'horizontal')
        self.grid_screen1 = GridLayout(cols = 2)
        self.grid_screen2 = GridLayout(cols = 2)

        self.image = Image(source = '')
        self.chart.add_widget(self.image)

        label = BackLabel(text = 'Company symbol:')
        self.comp_name = BackLabel(text = 'Exemplu')
        self.grid_screen1.add_widget(label)
        self.grid_screen1.add_widget(self.comp_name)

        label = BackLabel(text = 'Open price:')
        self.shore_price = BackLabel(text = '1567.43')
        self.grid_screen1.add_widget(label)
        self.grid_screen1.add_widget(self.shore_price)

        label = BackLabel(text = 'Date of last update:')
        self.last_date = BackLabel(text = '23.05.2019')
        self.grid_screen1.add_widget(label)
        self.grid_screen1.add_widget(self.last_date)

        label = BackLabel(text = 'Last price:')
        
        self.last_price = BackLabel(text = '1')
        self.grid_screen1.add_widget(label)
        self.grid_screen1.add_widget(self.last_price)

        self.screen1.add_widget(self.grid_screen1)
        
        label = BackLabel(text = 'Risk of investment:')
        self.risk = BackLabel(text = 'Risk')
        self.grid_screen2.add_widget(label)
        self.grid_screen2.add_widget(self.risk)
        
        self.checkButton = Button(text = 'Refresh')
        self.grid_screen2.add_widget(BackLabel())
        self.grid_screen2.add_widget(self.checkButton)
        
        self.screen2.add_widget(self.grid_screen2)

        self.grid3.add_widget(self.screen1)
        self.grid3.add_widget(self.screen2)

        self.grid2.add_widget(self.chart)
        self.grid2.add_widget(self.grid3)

        self.auxgrid.add_widget(self.menu)
        self.grid1.add_widget(self.auxgrid)
        self.grid1.add_widget(self.grid2)

        self.box.add_widget(self.grid1)

        self.processInput()

        return self.box
    
    def refresh_crawl(self):
        self.lista_firme = crawl()
        
    def changeCompany(self, index):
        self.comp_name.text = self.lista_firme[index].simb
        self.image.source = "img"+str(index)+".jpg"
        self.last_date.text = self.lista_firme[index].date[9:]
        self.shore_price.text = self.lista_firme[index].open_price[5:]
        self.last_price.text = self.lista_firme[index].last_price[5:]
        self.risk.text = self.lista_firme[index].var_p
        
    def processInput(self):
        index = 0
        for i in self.lista_firme:
            self.menu.appendData(i.simb, partial(self.changeCompany, index))
            index = index + 1



GUIApp().run()