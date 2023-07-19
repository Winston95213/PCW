import requests, pprint, os, time
from bs4 import BeautifulSoup
from multiprocessing import Process, Pool
import concurrent.futures
from threading import Thread, Timer
from .step import Step


import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


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
            # self.Rakuten(data, inputs, utils),
        ]

        start_time = time.time()

        for _ in website:
            _
            # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            #     executor.map(crawler)

        end_time = time.time()
        print(end_time - start_time)

        # 9.5367431640625e-07
        return self.data



    def Pchome(self, data, inputs, utils):
        lname = []
        lprice = []
        llink = []
        lpic = []
        online_shop = []
        ldescribe = []
        url = f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={inputs["product"]}'
        print(url)

        r = requests.get(url, headers=inputs["headers"], verify=False)
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
            online_shop.append("pchome")

        lprice = list(map(int, lprice))
        if len(lname) > self.limit:
            lname = lname[0:self.limit]
            lprice = lprice[0:self.limit]
            llink = llink[0:self.limit]
            lpic = lpic[0:self.limit]
            online_shop = online_shop[0:self.limit]

        pchome_data = {"ProductName": lname, "Price": lprice, "Link": llink, "Image": lpic, "Online_Shop": online_shop}
        self.data["pchome_data"] = pchome_data

        return pchome_data


    def MoMo(self, data, inputs, utils):
        momo_data = {}

        momo_dict = Parser(self.limit).Momo_parser(inputs, inputs["product"], utils)
        momo_data = utils.Merge(momo_data, momo_dict)
        self.data["momo_data"] = momo_data
        # print("ProductName", len(momo_data["ProductName"]))
        # print("Price", len(momo_data["Price"]))
        # print("Link",len(momo_data["Link"]))
        # print("Picture",len(momo_data["Image"]))

        return momo_data
    # TODO: BUG: The data list would been initialized while crawling new page -> make requests to MoMo Parser
    # TODO: More Commercial Website Resources

    def Rakuten(self, data, inputs, utils):
        lname = []
        lprice = []
        llink = []
        lpic = []
        online_shop = []
        url = f"https://www.rakuten.com.tw/search/{ input['product'] }"
        print(url)
        r = requests.get(url, headers=input["headers"], verify=False)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            print(soup)

class Parser(Crawler):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit

    def Momo_parser(self, inputs, product, utils):
        lname = []
        lprice = []
        llink = []
        lpic = []
        online_shop = []
        for page in range(1, 2):
            url = 'https://m.momoshop.com.tw/search.momo?_advFirst=N&curPage={' \
                  '}&_advCp=N&searchType=1&cateLevel=2&ent=k&searchKeyword={' \
                  '}&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType'.format(
                page, inputs["product"])
            print(url)
            r = requests.get(url, headers=inputs["headers"], verify=False)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
            lis = soup.find_all(class_="goodsItemLiSeo")
            for li in lis:
                pname = li.find(class_="prdName").text.strip()
                pprice = int(li.find(class_="price").text)
                ppic = li.find(class_="goodsImg")
                plink = li.find('a', href=True)
                ppic = ppic["src"].split("?t=")
                lname.append(pname)
                lprice.append(pprice)
                lpic.append(ppic)
                if product not in str(plink) or product not in plink['href']:
                    continue
                else:
                    llink.append("https://m.momoshop.com.tw/" + plink['href'])
                online_shop.append("momo")
        if len(lname) > self.limit:
            lname = lname[0:self.limit]
            lprice = lprice[0:self.limit]
            llink = llink[0:self.limit]
            lpic = lpic[0:self.limit]
            online_shop = lpic[0:self.limit]

        momo_data = {"ProductName": lname, "Price": lprice, "Link": llink, "Image": lpic, "Online_Shop": online_shop}
        return momo_data


