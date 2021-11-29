from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

def display_text(disp, text, *args):
    if len(args) < 2:
        FONT_SIZE = 12
    elif len(args) == 2:
        FONT_SIZE = 8
    else:
        FONT_SIZE = 6

    width = disp.width
    height = disp.height

    # 1 bit pixel
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("./static/ARIALUNI.TTF", FONT_SIZE)

    draw.rectangle((0, 0, width-1, height-1), outline=0, fill=0)

    draw.text((0, 0), text, font=font, fill=255)

    if len(args) > 0:
        for i, item in enumerate(args):
            draw.text((0, (i + 1) * FONT_SIZE-1), item, font=font, fill=255)

    disp.image(image)
    disp.show()
    #time.sleep(0.2)