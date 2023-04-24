

from .step import Step


class Postflight(Step):
    def __init__(self):
        super().__init__()

    def process(self, data, inputs, utils):
        print("END OF THE CODE")
        return data