import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime, timedelta
import os
import pickle

class sprzedajemy:

    def __init__(self,query,since,description_bool,ads_bool,only_new):
        self.since = since
        self.only_new = only_new
        self.description_bool = description_bool # jeśli wartość ma true, wyskoczy więcej ogłoszeń, ale szansa na to że nie będą powiązane z ogłoszeniem rośnie
        self.ads_bool = ads_bool #jeśli ma wartość True włączamy do wyniku wyszukiwania również oferty wyróźnione
        self.query = query # list of keywords
        self.base_link = 'https://sprzedajemy.pl/wszystkie-ogloszenia?inp_text%5Bv%5D={}&offset={}'
        self.base_link_description = 'https://sprzedajemy.pl/wszystkie-ogloszenia?inp_text%5Bv%5D={}&inp_text%5Bn%5D=1&offset={}'
        self.headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }


    def format_query(self):
        if self.ads_bool == "True":
            self.ads_bool = True
        else:
            self.ads_bool = False
        
        if self.description_bool == "True":
            self.description_bool = True
        else:
            self.description_bool = False
        
        if self.only_new == "True":
            self.only_new = True
        else:
            self.only_new = False
        if len(self.query) == 0:
            raise Exception('Lista nie zawiera żadnych słów. olx.py')
        if len(self.query) == 1:
            return self.query[0]
        
        format_query = ''

        for query in range(len(self.query)):

            if query == len(self.query)-1 : 
                format_query = format_query + self.query[query]
            else:            
                format_query = format_query + self.query[query]+'+'

        return format_query

    def send_request(self,query,page_num,description_bool):
        if description_bool:
            link = self.base_link_description.format(query, page_num)
        else:
            link = self.base_link.format(query,page_num)
        response = requests.get(link,headers=self.headers)
        self.date_today = date.today()

        return response

    def parse_response(self, response):

        stop_var = 0

        link_list = []

        soup = BeautifulSoup(response.text,'html.parser')

        if self.ads_bool:
            cells_m = soup.find('ul',{'class':'list highlighted'})
            try:
                cells = cells_m.find_all('article',{'class':'element'})
            except AttributeError:
                stop_var = 1   

            if stop_var == 0:
                for cell in cells:
                    href = cell.find('a',{'class','offerLink'})
                    date_time = cell.find('time',{'class':'time'})
                    link_list.append(['https://sprzedajemy.pl/'+href['href'],date_time])
            
        
        cells_m = soup.find('ul',{'class':'list normal'})
        try:
            cells = cells_m.find_all('article',{'class':'element'})
        except AttributeError:
            return 0
        for cell in cells:
            href = cell.find('a',{'class','offerLink'})
            date_time = cell.find('time',{'class':'time'})
            if href != None or date_time != None:
                link_list.append(['https://sprzedajemy.pl/'+href['href'],date_time['datetime']])
        return link_list

    def end_operations(self,new_list):
        
        file_name = 'sprzedajemy'
        for x in range(len(self.query)):
            file_name= file_name+self.query[x]

        if not os.path.exists(file_name+'.pkl'):
            with open(file_name+'.pkl', 'wb') as f:
                pickle.dump({'dict':new_list}, f)
            return new_list
        else:
            with open(file_name+'.pkl', 'rb') as f:
                loaded_dict = pickle.load(f)
            
            list_loaded = loaded_dict['dict']
            list_loaded_=[]
            
            for h in new_list:
                if h not in list_loaded:
                    list_loaded_.append(h)

            for n in new_list:
                list_loaded.append(n)
            with open(file_name+'.pkl', 'wb') as f:
                pickle.dump({'dict':list_loaded}, f)

            return list_loaded_


    def main(self):
        page_num = 0
        query = self.format_query()
        returned_request = self.send_request(query,page_num,self.description_bool)
        listt = self.parse_response(returned_request)
        if listt == 0:
            return 0 
        if self.only_new:
            list_new = []
            for el in listt:
                list_new.append(el[0])
            x = self.end_operations(list_new)
            return x
        return listt


#sprzedajemy(['czarny','kot'],'since',True,True).main()