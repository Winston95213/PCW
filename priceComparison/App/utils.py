import os


class Utils:
    def __init__(self):
        self.image_path = {"pchome": "product_images/pc_images", "momo": "product_images/momo_images",}

    def count_items(self, website):
        count = 0
        if os.path.isfile(website):
            dir_path = self.image_path[website]
            for path in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, path)):
                    count += 1
        return count

    def remove_items(self, dir_path):
        count = 0
        for path in os.listdir(dir_path):
            count += 1
            os.remove(os.path.join(dir_path, path))
        print(f"Removed count items from {dir_path}")

    def Merge(self, dict1, dict2):
        res = {**dict1, **dict2}
        return res