from .Steps.step import StepException


class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, inputs, utils):
        data = {}
        for step in self.steps:
            try:
                data = step.process(data, inputs, utils)
            except StepException as e:
                print("Exception occurred: ", e)
                break
        return data
