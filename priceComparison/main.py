import sys
sys.path.append('/')
from priceComparison.App.utils import Utils
from priceComparison.App.pipeline import Pipeline
# Steps:
from priceComparison.App.Steps.preflight import Preflight
from priceComparison.App.Steps.crawler import Crawler
from priceComparison.App.Steps.organizer import Organizer
from priceComparison.App.Steps.postflight import Postflight
from priceComparison.App.Steps.download_images import Download_Images
from priceComparison.App.Steps.mysql import MySQL

websites = ["PchomeData", "MomoData"]
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"}
product = ""


def activate(search_word):
    inputs = {"websites": websites,
              "headers": headers,
              "product": search_word,
              "limit": 20}
    utils = Utils()
    return process_request(inputs, utils)


def process_request(inputs, utils):
    steps = [
        Preflight(),
        Crawler(),
        Organizer(),
        # Download_Images(),
        # MySQL(),
        Postflight()
    ]

    p = Pipeline(steps)
    data = p.run(inputs, utils)
    return data


