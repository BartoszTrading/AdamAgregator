import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime, timedelta
from olx import olx

class lento:

    def __init__(self,query,since,ads_bool):
        self.since = since
        self.ads_bool = ads_bool #jeśli ma wartość True włączamy do wyniku wyszukiwania również oferty wyróźnione
        self.query = query # list of keywords
        self.base_link = 'https://www.lento.pl/ogloszenia.html?co={}'
        self.headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }

    def format_query(self):
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

    def send_request(self,query,page_num):

        link = self.base_link.format(query,page_num)
        response = requests.get(link,headers=self.headers)
        print(link)
        self.date_today = date.today()

        return response

    def parse_response(self, response):

        link_list = []

        soup = BeautifulSoup(response.text,'html.parser')
        if self.ads_bool:
            cells = soup.find_all('div',{'class','tablelist-tr tablelist-tr-promo hash'})
            for cell in cells:
                href = cell.find('a',{'class':'title-list-item'})
                date_time = cell.find('div',{'class':'data-list-item hidden-xs'})
                date_time = self.parse_date(date_time,self.date_today)
                link_list.append([href['href'],date_time])
        

        cells_no = soup.find_all('div',{'class','tablelist-tr hash'})
        cells_gray = soup.find_all('div',{'class','tablelist-tr gray hash'})
        cells = cells_no+cells_gray
        for cell in cells:
            href = cell.find('a',{'class':'title-list-item'})
            date_time = cell.find('div',{'class':'data-list-item hidden-xs'})
            date_time = self.parse_date(date_time,self.date_today)
            link_list.append([href['href'],date_time])

        return 'yes'

    def parse_date(self, date, time_date): #date: data wystawienia ogłoszenie time_date:dzisiejsza dara
        
        date_offer = 0

        if 'dzisiaj' in date.text:
            date_offer = str(time_date)+' '+date.text[-5:]

        elif 'wczoraj' in date.text:
            yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
            date_offer = str(yesterday_date) + ' '+date.text[-5:]
        
        else:
            month = date.text[3:6]
            month_num = self.convert_date(month)
            date_offer_early = datetime(int(str(time_date)[:4]),month_num,int(date.text[:-11]),int(date.text[8:10]),int(date.text[11:13]),)
            date_offer = date_offer_early.strftime("%Y-%m-%d %H:%M")

        return date_offer
    
    def convert_date(self,date):

        month_list = ['sty','lut','mar','kwi','maj','cze','lip','sie','wrz','paz','lis','gru']

        pos = month_list.index(date)

        return pos+1

    
    def main(self):
        page_num = 0
        query = self.format_query()
        returned_request = self.send_request(query,page_num)
        list = self.parse_response(returned_request)

        return list

lento(['kot'],'since',True).main()