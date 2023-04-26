from Outputs import Output
from PIL import Image, ImageOps

class Hub75Output(Output.Output):
    
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        from rgbmatrix import RGBMatrix, RGBMatrixOptions # type: ignore

        options = RGBMatrixOptions()
        options.rows = self.rows
        options.cols = self.cols
        options.chain_length = self.chain_length
        options.parallel = self.parallel
        options.gpio_slowdown = self.gpio_slowdown
        options.hardware_mapping = self.hardware_mapping
        options.drop_privileges = False
        self.matrix = RGBMatrix(options=options)

    def getName(self):
        return "Tk output"
    
    def Input(self, frame):
        if frame.width != self.cols*2 and frame.width == self.cols:
            if self.mirrorType == 0:
                img_out = Image.new('RGB', (frame.width*2, frame.height))
                img_out.paste(ImageOps.mirror(frame), (frame.width,0))
                img_out.paste(frame, (0, 0))
                self.matrix.SetImage(img_out)
            else:
                img_out = Image.new('RGB', (frame.width*2, frame.height))
                img_out.paste(ImageOps.mirror(frame), (0,0))
                img_out.paste(frame, (frame.width, 0))
                self.matrix.SetImage(img_out)
        else:
            if frame.width == self.cols*2:
                self.matrix.SetImage(frame)
            else:
                self.matrix.SetImage(frame.copy().resize(self.cols*2, self.rows))
    
    def getArgs(self):
        return {
            "rows": {
                "types": [int]
            },
            "cols": {
                "types": [int]
            },
            "chain_length": {
                "types": [int],
                "default": 2
            },
            "parallel": {
                "types": [int],
                "default": 1
            },
            "gpio_slowdown": {
                "types": [int],
                "default": 2
            },
            "hardware_mapping": {
                "types": [str],
                "default": "adafruit-hat"
            },
            "mirrorType": {
                "types": [int],
                "default": 0
            }
        }