from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import numpy as np

poem =  \
"""
             绝句
             杜甫
    两个黄鹂鸣翠柳，一行白鹭上青天。
    窗含西岭千秋雪，门泊东吴万里船。
"""
 
 
def draw_png(name, font_size = 24):
    font=ImageFont.truetype(file_path, font_size)
    text_width, text_height = font.getsize(poem)
    #image = Image.new(mode='RGB', size=(text_width, text_height))
    image = Image('bg.jpg')
    draw_table = ImageDraw.Draw(im=image)
    draw_table.text(xy=(0, 0), text=poem, fill='#000000', font=font)
    return image
    # image.show()  # 直接显示图片
    
def draw(font_fath, img_path):
    #考虑到会有很多关键词，所以多关键词，放列表里，如['甘孜','内蒙古']
    #i = ["重生杀手的主角爱人"]
        img = cv2.imdecode(np.fromfile('bg.jpg',dtype=np.uint8),-1) # 图片名称不能有汉字
        cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # cv2和PIL中颜色的hex码的储存顺序不同
        pilimg = Image.fromarray(cv2img)

        # PIL图片上打印汉字
        draw = ImageDraw.Draw(pilimg) # 图片上打印
        font = ImageFont.truetype(font_fath, 60, encoding="utf-8") # 参数1：字体文件路径，参数2：字体大小

        draw.text((0,0), poem, (30, 29, 29), font=font) # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
        cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
        cv2.imshow("photo", cv2charimg)
        cv2.imencode('.jpg',cv2charimg)[1].tofile(img_path)
        cv2.waitKey (0)
        cv2.destroyAllWindows()


def run():
    print('开始运行:')
    dir = '500+字体'
    img_dir = 'previews'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    extensions = ['.ttf', '.otf', '.ttc']
    for p in os.listdir(dir):
        file_path = os.path.join(dir, p)
        if os.path.isfile(file_path):
            if any(os.path.splitext(p)[-1].lower() == i for i in extensions):
                try:
                    image = draw_png(file_path)
                    image.save(os.path.join(img_dir,os.path.splitext(p)[0])+'.png', 'PNG')  # 保存在当前路径下，格式为PNG
                    image.close()
                except Exception as e:
                    print(file_path, ' ERR: ', e)


if __name__ == "__main__":
    draw('DroidSansChinese.ttf','1.jpg')
