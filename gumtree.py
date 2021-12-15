import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime, timedelta
import os
import pickle

class gumtree:

    def __init__(self,query,since,ads_bool,only_new):
        self.since = since
        self.only_new = only_new
        self.ads_bool = ads_bool #jeśli ma wartość True włączamy do wyniku wyszukiwania również oferty wyróźnione
        self.query = query # list of keywords
        self.base_link = 'https://www.gumtree.pl/s-wszystkie-the-reklamy/v1b0p1?q={}'
        self.headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
    def format_query(self):

        if self.ads_bool == "True":
            self.ads_bool = True
        else:
            self.ads_bool = False

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
    
    def send_request(self,query):

        link = self.base_link.format(query)
        response = requests.get(link,headers=self.headers)
        self.date_today = datetime.now()
        return response
    
    def parse_response(self, response):

        link_list = []
        soup = BeautifulSoup(response.text,'html.parser')
        if self.ads_bool:
            cells_u = soup.find('div',{'class','topAdsContainer'})
            cells = cells_u.find_all('div',{'class':'tileV1'})
            for cell in cells:
                href = cell.find('a',{'class':'href-link tile-title-text'})
                link_list.append([href['href']])
        
        cells_u = soup.find('div',{'class','view'})
        cells = cells_u.find_all('div',{'class':'tileV1'})
        for cell in cells:
            href = cell.find('a',{'class':'href-link tile-title-text'})
            date_time = cell.find('div',{'class':'creation-date'})
            date_time = self.parse_date(date_time)
            if isinstance(date_time,int):
                continue
            link_list.append([href['href'],date_time])
        return link_list

    def parse_date(self,date):
        
        time_offer = 0


        if 'godzin temu' in date.text:
            time_offer = self.date_today - timedelta(hours=float(date.text[:-12]))
        elif 'dzień' in date.text:
            time_offer = self.date_today - timedelta(days=1)
        elif 'dni' in date.text:
            time_offer = self.date_today - timedelta(days=float(date.text[:-9]))
        

        return time_offer

    def end_operations(self,new_list):
        
        file_name = 'gumtree'
        for x in range(len(self.query)):
            file_name= file_name+self.query[x]

        if not os.path.exists(file_name+'.pkl'):
            with open(file_name+'.pkl', 'wb') as f:
                pickle.dump({'dict':new_list}, f)
            return new_list[:10]
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
        returned_request = self.send_request(query)
        list = self.parse_response(returned_request)
        if self.only_new:
            list_new = []
            for el in list:
                list_new.append(el[0])
            x = self.end_operations(list_new)
            return x
        return list

#gumtree(['koty'],'since',True,True).main()