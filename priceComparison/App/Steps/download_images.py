import requests, os

from .step import Step


class Download_Images(Step):
    def process(self, data, inputs, utils):
        path = "static/product_images"
        utils.remove_items(path)
        images_list = data["CheapData"]['Image'].values.tolist()
        for ppic in images_list:
            print(f"Loading Image {ppic}...")
            picture = requests.get(ppic)
            picture.raise_for_status()
            images_folder = open(os.path.join(path, os.path.basename(ppic)), 'wb')
            for diskStorage in picture.iter_content(20240):
                images_folder.write(diskStorage)
            images_folder.close()
        return data



