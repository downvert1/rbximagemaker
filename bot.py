import json, os
import PIL
import matplotlib
from wand.image import Image


with open("config.json", "r") as file:
    config = json.load(file)

output_path1 = config.get('WorkspacePath')
os.makedirs(f"{output_path1}\\ImgLoader", exist_ok=True) 
output_path = f"{output_path1}\\ImgLoader"

fileName = input("Enter file name e.g. (test.png): ")
size = input("Enter image base / width size: ")


basewidth = int(size)
img = PIL.Image.open(os.path.join("Images", str(fileName)))
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
img.save(os.path.join("Images", str(fileName)))

image = PIL.Image.open(os.path.join("Images", str(fileName)))


width1, height1 = image.size


print(width1, height1)

pixels = []
width, height = 0, 0
blob = None

class MyPixel(object):
    red = 0
    green = 0
    blue = 0
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue
    def __repr__(self):
        return u'#{0.red:02X}{0.green:02X}{0.blue:02X}'.format(self)

class MyImage(Image):
    @property
    def pixels(self):
        pixels = []
        self.depth = 8
        blob = self.make_blob(format='RGB')
        for cursor in range(0, self.width * self.height * 3, 3):
            pixel = MyPixel(red=blob[cursor],
                            green=blob[cursor + 1],
                            blue=blob[cursor + 2])
            pixels.append(pixel)
        return pixels

with MyImage(filename=os.path.join("Images", str(fileName))) as img:
    with open(os.path.join("Data(ignore)", f"hextlist_{str(fileName).replace('.png', '')}.txt"),'w') as file:
        for hex in img.pixels:
            file.write(f"{str(hex).replace('#', '')} ")

    a_file = open(os.path.join("Data(ignore)", f"hextlist_{str(fileName).replace('.png', '')}.txt"), "r+")
    current_data = a_file.read()
    if not os.path.exists(f"{output_path}\\{fileName.replace('.png', '')}"):
        os.mkdir(f"{output_path}\\{fileName.replace('.png', '')}")
        print("created")
    else:    
        print("Directory exists")
    end_file = open(f"{output_path}\\{fileName.replace('.png', '')}\\Data.txt", "w")
    end_file.write(f"local module = {{\nWidth = {width1},\nHeight = {height1},\nData = \"{current_data.rstrip()}\"\n}}\nreturn module")

    


