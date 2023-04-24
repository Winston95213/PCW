import os

from .step import Step


class Preflight(Step):
    def __init__(self):
        super().__init__()

    def process(self, data, inputs, utils):
        images_folder = "static/product_images"
        if not os.path.exists(images_folder):
            print("Creating product_images folder...")
            os.makedirs(images_folder)
        # pc_images_folder = "product_images/pc_images"
        # if not os.path.exists(pc_images_folder):
        #     os.makedirs(pc_images_folder)
        # mo_images_folder = "product_images/momo_images"
        # if not os.path.exists(mo_images_folder):
        #     os.makedirs(mo_images_folder)

        print("Preflight process succeeded")
