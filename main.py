from sprzedajemy import sprzedajemy
from olx import olx
from lento import lento
from datetime import datetime
import json
from allegrolokalne import allegro
from gumtree import gumtree

class program:

    def __init__(self):
        pass

    def get_offers(self):

        with open('config.json') as f:
            data = json.load(f)

        only_new = data['ogolne']['only_new']
        if only_new == "True":
            only_new = True
        else:
            only_new = False

        words = data['ogolne']['query']

        self.keywords = words.split(' ')

        self.since = datetime.strptime(data['ogolne']['date'], '%Y-%m-%d %H:%M')
        #sprzedajemy
        sprzedajemy_list = sprzedajemy(self.keywords,'since',data['sprzedajemy']['description'],data['sprzedajemy']['ads'],only_new).main()

        #olx
        olx_list = olx(self.keywords,'since',data['olx']['description'],data['olx']['ads'],only_new).main()

        #lento
        lento_list = lento(self.keywords,'since',data['lento']['description'],data['lento']['ads'],only_new).main()

        #allegro
        allegro_list = allegro(self.keywords,data['allegro']['ads']).main()

        #gumtree
        gumtree_list = gumtree(self.keywords,'since',data['gumtree']['ads'],only_new).main()
        # print(lento_list[0])
        # print(sprzedajemy_list[0])
        # print(olx_list[0])

        if not only_new:
            sprzedajmy_dates = [[datetime.strptime(x[1],'%Y-%m-%d %H:%M:%S'),sprzedajemy_list.index(x)] for x in sprzedajemy_list]
            if lento_list != [] and lento_list !=0:
                lento_dates = [[datetime.strptime(x[1],'%Y-%m-%d %H:%M'),lento_list.index(x)] for x in lento_list]
            else:
                lento_dates = []
            olx_dates_1 = [[datetime.strptime(x[1],'%Y-%m-%d %H:%M'),olx_list.index(x)] for x in olx_list if len(x[1])>11]
            olx_dates_2 = [[datetime.strptime(x[1],'%Y-%m-%d'),olx_list.index(x)] for x in olx_list if len(x[1])<11]
            gumtree_dates = [x[1] for x in gumtree_list]
            gumtree_pos = [x for x in gumtree_dates if isinstance(x,int) and not x>self.since]
            olx_pos_1 = [x[1] for x in olx_dates_1 if x[0]>self.since]
            olx_pos_2 = [x[1] for x in olx_dates_2 if x[0]>self.since]
            sprzedajemy_pos = [x[1] for x in sprzedajmy_dates if x[0]>self.since]
            lento_pos = [x[1] for x in lento_dates if x[0]>self.since]
        


        # print(olx_pos_2)
        # print(olx_pos_1)
        # print(sprzedajemy_pos)
        # print(lento_pos)
        # print(len(lento_list))

        if not only_new:
            for x in olx_pos_1:
                if data['olx']['ads'] == 'False' and 'promoted' not in olx_list[x][0]:
                    print(olx_list[x][0])
            for x in olx_pos_2:
                if data['olx']['ads'] == 'False' and 'promoted' not in olx_list[x][0]:
                    print(olx_list[x][0])
            for x in sprzedajemy_pos:
                print(sprzedajemy_list[x][0])
            for x in lento_pos:
                print(lento_list[x][0])
            for x in gumtree_pos:
                print(gumtree_list[x][0])
        else:
            for x in olx_list:
                if data['olx']['ads'] == 'False':
                    if 'promoted' not in x:
                        print(x)
            if lento_list !=0:
                for x in lento_list:
                    print(x)
            if sprzedajemy_list !=0:
                for x in sprzedajemy_list:
                    print(x)
            if allegro_list !=0:
                for x in allegro_list:
                    print(x)

program().get_offers()