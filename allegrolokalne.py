import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime, timedelta
import os
import json
import pickle

class allegro:

    def __init__(self,query,ads_bool):
        self.query = query #query list to search
        self.ads_bool = ads_bool #jeśli ma wartość True włączamy do wyniku wyszukiwania również oferty wyróźnione
        self.base_link = "https://allegrolokalnie.pl/oferty/q/{}?page={}"
        self.len_query = len(self.query)
        self.headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
    def format_query(self):
        
        if self.ads_bool == "True":
            self.ads_bool = True
        else:
            self.ads_bool = False

        if self.len_query == 0:
            raise Exception('Lista nie zawiera żadnych słów. olx.py')
        if self.len_query == 1:
            return self.query[0]
        
        format_query = ''

        for query in range(len(self.query)):

            if query == self.len_query-1 : 
                format_query = format_query + self.query[query]
            else:            
                format_query = format_query + self.query[query]+'%20'

        return format_query
    
    def send_request(self,query,page_num): #query:formated query page_num:number page


        link = self.base_link.format(query,page_num)
        response = requests.get(link,headers=self.headers)
        self.date_today = date.today()

        return response
    
    def parse_response(self,response):
        
        link_list = []
        link_list2 = []
        soup = BeautifulSoup(response.text,'html.parser')

        offers = soup.find('div',{'class':'listing__items'})

        var_1 = 0
        for offer in offers:
            if "Ogłoszenia" in offer:
                pos = offers.index(offer)

                var_1 = 1
            if var_1 == 1:
                link = [ t for t in str(offer).split() if t.startswith('href') ]
                if link != []:
                    if 'images' not  in link:
                        link_list.append(link[0])
            elif var_1 == 0:
                link = [ t for t in str(offer).split() if t.startswith('href') ]
                if link != []:
                    if 'images' not  in link:
                        link_list.append(link[0])
            for link in link_list:
                g = link.split('"')
                link_list2.append('https://allegrolokalnie.pl/'+g[1])
                
        
        return link_list2    
    
    def end_operations(self,new_list):
        
        file_name = 'allegro'
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
        list_main = []
        for x in range(3):
            page_num =x
            query = self.format_query()
            returned_request = self.send_request(query,page_num)
            listt = self.parse_response(returned_request)
            for y in listt:
                list_main.append(y)
        b = self.end_operations(list_main)
        if b == []:
            return list_main[:5]
        return b




#allegro(['samsung','s10'],'since',True,True).main()