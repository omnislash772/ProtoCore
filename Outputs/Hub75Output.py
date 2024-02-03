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
        return "Hub75Output"
    
    def Input(self, frame):
        if self.flip == 1:
           frame = frame.transpose(Image.FLIP_TOP_BOTTOM)
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
                self.matrix.SetImage(frame.convert('RGB'))
            else:
                self.matrix.SetImage(frame.copy().resize((self.cols*2, self.rows)).convert('RGB'))
    
    def getArgs(self):
        #The below default ARGS should not be changed here, these should be defined in the configuration Json when this module is being defined
        return {
            #Rows on the Hub75 panel, should equal the size of one panel in most cases
            "rows": {
                "types": [int]
            },
            #Collums on the Hub75 panel, should equal the size of one panel in most cases
            "cols": {
                "types": [int]
            },
            #how many Hub75 panels are connected in the chain
            "chain_length": {
                "types": [int],
                "default": 2
            },
            #How many Paralel chains are in your configuration,
            "parallel": {
                "types": [int],
                "default": 1
            },
            #used to tune the panels to reduce glitchy effects, adjust as needed
            "gpio_slowdown": {
                "types": [int],
                "default": 2
            },
            #Used to define what hat is used, in most cases the default is correct, other configurations are untested.
            "hardware_mapping": {
                "types": [str],
                "default": "adafruit-hat"
            },
            #Define if the panels need to be flipped. good to change if your face is showing upside down
            "flip": {
                "types": [int],
                "default": 0
            },
            #Changes the mirroring for the faces, Some panels seem to display images pre mirrored and this fixes that if set to 1
            "mirrorType": {
                "types": [int],
                "default": 0
            }
        }
