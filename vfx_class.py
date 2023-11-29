import PIL.Image
from PIL import ImageTk

class VfxSystemDefinitionData():
    def __init__(self, vfx, emitter, type, no_line):
        self.vfx = vfx
        self.emitter = emitter
        self.type = type
        self.no_line = no_line

class SkinCharacterDataProperties():
    def __init__(self, base, type, no_line):
        self.base = base
        self.type = type
        self.no_line = no_line

class Combine_Image():
    def __init__(self, node):
        self.image = None
        self.node = node
    
    def combine(self, im2):
        if self.image is None:
            self.image = im2
        else:
            im1 = self.image
            dst = PIL.Image.new('RGBA', (im1.width + im2.width + 10, 20))
            empty = PIL.Image.new('RGBA', (10, 20))
            dst.paste(im1, (0, 0))
            dst.paste(empty, (im1.width, 0))
            dst.paste(im2, (im1.width + 10, 0))
            
            self.image = dst
        
        return ImageTk.PhotoImage(self.image)