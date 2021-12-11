import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime, timedelta

class olx:

    def __init__(self,query,since,description_bool,ads_bool):
        self.query = query #query list to search
        self.description_bool = description_bool # jeśli wartość ma true, wyskoczy więcej ogłoszeń, ale szansa na to że nie będą powiązane z ogłoszeniem rośnie
        self.ads_bool = ads_bool #jeśli ma wartość True włączamy do wyniku wyszukiwania również oferty wyróźnione
        self.since = since #ogłoszenia od daty w formacie %d-%m-%Y %H:%M:%S
        self.base_link_description = "https://www.olx.pl/oferty/q-{}/?search%5Bdescription%5D={}"
        self.base_link = "https://www.olx.pl/oferty/q-{}/?page={}"
        self.len_query = len(self.query)
        self.headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }

    def format_query(self):
        
        if self.len_query == 0:
            raise Exception('Lista nie zawiera żadnych słów. olx.py')
        if self.len_query == 1:
            return self.query[0]
        
        format_query = ''

        for query in range(len(self.query)):

            if query == self.len_query-1 : 
                format_query = format_query + self.query[query]
            else:            
                format_query = format_query + self.query[query]+'-'

        return format_query
    
    def send_request(self,query,page_num,description_bool): #query:formated query page_num:number page

        if description_bool:
            link = self.base_link_description.format(query, page_num)
        else:
            link = self.base_link.format(query,page_num)

        response = requests.get(link,headers=self.headers)

        self.date_today = date.today()

        return response

    def parse_response(self,response):
        
        link_list = []

        soup = BeautifulSoup(response.text,'html.parser')
        

        if self.ads_bool:
            cells  = soup.find_all('td',{'class':'offer promoted'})
            for offer in cells:
                href = offer.find('a',{'data-cy':'listing-ad-title'})
                date = offer.find('i',{'data-icon':'clock'}).parent
                date = self.parse_date(date,self.date_today)
                link_list.append([href['href'], date])
        
        cells_2 = soup.find_all('td',{'class':'offer'})
        for offer in cells_2:
            href = offer.find('a',{'data-cy':'listing-ad-title'})
            date = offer.find('i',{'data-icon':'clock'}).parent
            date = self.parse_date(date,self.date_today)
            link_list.append([href['href'],date])

        print(link_list)
        return link_list
    
    def parse_date(self, date, time_date): #date: data wystawienia ogłoszenie time_date:dzisiejsza dara
        
        date_offer = 0

        if 'dzisiaj' in date.text:
            date_offer = str(time_date)+' '+date.text[-5:]

        elif 'wczoraj' in date.text:
            yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
            date_offer = str(yesterday_date) + ' '+date.text[-5:]
        
        else:
            month = date.text[-3:]
            month_num = self.convert_date(month)
            date_offer_early = datetime(int(str(time_date)[:4]),month_num,int(date.text[:-5]))
            date_offer = date_offer_early.strftime("%Y-%m-%d")

        return date_offer
    
    def convert_date(self,date):

        month_list = ['sty','lut','mar','kwi','maj','cze','lip','sie','wrz','paz','lis','gru']

        pos = month_list.index(date)

        return pos+1


    def main(self):

        page_num =1 
        query = self.format_query
        returned_request = self.send_request(query,page_num,self.description_bool)
        list = self.parse_response(returned_request)

        return list


#pierwszy argument to lista słów kluczowych
#drugi to data od której mamy brać ogłoszenia
#trzeci to wartość bool, która określa czy w wyszukiwaniu ma brać słowa z ogłoszeń
#czwarty to wartość boool, która określa czy ma brać pod uwagę oferty promowane


#olx(['rower'],'kupa',True,True).main()

            



