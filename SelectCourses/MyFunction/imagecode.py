import random

from PIL import Image, ImageDraw


# 生成随机的图形验证码
def create_imgcode():
    def get_randcolor():
        rgb_tuple = tuple((random.randint(0, 255) for _ in range(3)))
        # print(rgb_tuple)
        return rgb_tuple

    def get_randchar():
        super_str = chr(random.randint(65, 90))
        lower_str = chr(random.randint(97, 122))
        num_str = str(random.randint(0, 9))
        char_list = [super_str, lower_str, num_str]
        rand_char = random.choice(char_list)
        return rand_char

    img = Image.new(mode='RGB', size=(100, 30), color=(225, 225, 225))
    draw = ImageDraw.Draw(img, mode='RGB')
    code = []
    for i in range(5):
        text = get_randchar()
        rgb = get_randcolor()
        draw.text(xy=(5 + i * 20, 10), text=text, fill=rgb)
        code.append(text)
    img_code = ''.join(code)
    return img, img_code
