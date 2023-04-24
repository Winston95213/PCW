import requests, pprint, os, time
from bs4 import BeautifulSoup
from multiprocessing import Process, Pool
from threading import Thread, Timer
from .step import Step


class Crawler(Step):

    def __init__(self):
        super().__init__()
        self.data = {}
        self.limit = 0

    def process(self, data, inputs, utils):

        self.limit = inputs["limit"]
        website = [
            self.Pchome(data, inputs, utils),
            self.MoMo(data, inputs, utils),
        ]

        for _ in website:
            _

        return self.data

    def Pchome(self, data, inputs, utils):
        lname = []
        lprice = []
        llink = []
        lpic = []
        ldescribe = []
        url = f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={inputs["product"]}'
        print(url)

        r = requests.get(url, headers=inputs["headers"])
        data = r.json()
        for product in data['prods']:
            # pprint.pprint(product)
            pname = product["name"]
            pprice = int(product["price"])
            ppic = "https://cs-a.ecimg.tw" + product["picS"]
            plink = "https://24h.pchome.com.tw/prod/" + product["Id"]
            lname.append(pname)
            lprice.append(pprice)
            llink.append(plink)
            lpic.append(ppic)

        lprice = list(map(int, lprice))
        if len(lname) > self.limit:
            lname = lname[0:self.limit]
            lprice = lprice[0:self.limit]
            llink = llink[0:self.limit]
            lpic = lpic[0:self.limit]

        pchome_data = {"ProductName": lname, "Price": lprice, "Link": llink, "Image": lpic}
        self.data["pchome_data"] = pchome_data

        return pchome_data


    def MoMo(self, data, inputs, utils):
        momo_data = {}

        momo_dict = Parser(self.limit).Momo_parser(inputs, inputs["product"], utils)
        momo_data = utils.Merge(momo_data, momo_dict)
        self.data["momo_data"] = momo_data
        print("ProductName", len(momo_data["ProductName"]))
        print("Price", len(momo_data["Price"]))
        print("Link",len(momo_data["Link"]))
        print("Picture",len(momo_data["Image"]))

        return momo_data
    # TODO: BUG: The data list would been initialized while crawling new page -> make requests to MoMo Parser
    # TODO: More Commercial Website Resources

class Parser(Crawler):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit

    def Momo_parser(self, inputs, product, utils):
        lname = []
        lprice = []
        llink = []
        lpic = []
        for page in range(1, 2):
            url = 'https://m.momoshop.com.tw/search.momo?_advFirst=N&curPage={' \
                  '}&_advCp=N&searchType=1&cateLevel=2&ent=k&searchKeyword={' \
                  '}&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType'.format(
                page, inputs["product"])
            print(url)
            r = requests.get(url, headers=inputs["headers"])
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
            lis = soup.find_all(class_="goodsItemLiSeo")
            for li in lis:
                pname = li.find(class_="prdName").text.strip()
                pprice = int(li.find(class_="price").text)
                ppic = li.find(class_="goodsImg")
                plink = li.find('a', href=True)
                ppic, _ = ppic["src"].split("?t=")
                lname.append(pname)
                lprice.append(pprice)
                lpic.append(ppic)
                if product not in str(plink) or product not in plink['href']:
                    continue
                else:
                    llink.append("https://m.momoshop.com.tw/" + plink['href'])
        if len(lname) > self.limit:
            lname = lname[0:self.limit]
            lprice = lprice[0:self.limit]
            llink = llink[0:self.limit]
            lpic = lpic[0:self.limit]

        momo_data = {"ProductName": lname, "Price": lprice, "Link": llink, "Image": lpic}
        return momo_data
