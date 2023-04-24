import pprint
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

from .step import Step


class Organizer(Step):
    def __init__(self):
        super().__init__()

    def cheap_data(self, com_data, inputs):

        # cheap_data = sorted(list(map(int, cheap_data)))
        cheap_data = com_data.sort_values(by=["Price"], ignore_index=True).iloc[0:5]
        # pprint.pprint(cheap_data.iloc[0:5].to_dict())
        
        return cheap_data

    def filter(self, com_data):
        ComData = com_data
        avg = int(com_data["Price"].mean())
        min = com_data["Price"].min().astype(int)
        filter_price = (avg - min)/2
        print("filter price:", filter_price)
        ComData = ComData[ComData['Price'] > filter_price].sort_values(by=["Price"], ignore_index=True)
        return ComData

    def zip(self, zip_data):
        pn = zip_data["ProductName"]
        p = zip_data["Price"]
        l = zip_data["Link"]
        i = zip_data["Image"]
        zip_data = zip(pn, p, l, i)
        # zip_data = dict((pn, {p, l, i}) for pn, p, l, i in zip_data)

        return zip_data

    def process(self, data, inputs, utils):
        columns = ["ProductName", "Price", "Link", "Image"]
        pchome_df = pd.DataFrame(data["pchome_data"], columns=columns)
        momo_df = pd.DataFrame(data["momo_data"], columns=columns)
        com_data = pd.concat([pchome_df, momo_df]).iloc[0:39]
        com_data = com_data.sort_values(by=["Price"], ignore_index=True)
        all_data = com_data
        com_data = self.filter(com_data)
        cheap_data = self.cheap_data(com_data, inputs)
        zip_data = self.zip(cheap_data)

        precision_data = list(self.zip(com_data))

        data = {"PchomeData": pchome_df, "MomoData": momo_df, "ComData": com_data,
                "CheapData": cheap_data, "ZipData": zip_data, "AllData": all_data, "PrecisionData": precision_data}
        return data
