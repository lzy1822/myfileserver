import fitz


import os
vipshome = r'E:\\server-d\\vips-dev-8.14\\bin'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']

import pyvips



'''
获得文件名
'''
def getfilefirstname(filename):
    #"/home/xian/myfileserver/files/pdf/gl/007.pdf"
    path = filename
    filename = os.path.basename(path)
    result = filename.split(".")[0]
    print("getfilefirstname:",result)
    return result   

'''
处理文件重命名
'''
def renamefilepath(strFileName):
    bok=True
    strbb=""
    while bok :
        if not os.path.exists(strFileName+strbb):
            os.rename(strFileName,strFileName+strbb)
            bok=False
        else:
            strbb=strbb+"b"



def pdf_to_images(file_relative_path, output_dir,volumeorsutra,zoom_x,zoom_y):
    """
    file_relative_path : 文件相对路径
    """
    suboutput_dir=output_dir.replace("raw_images","images")
    if not os.path.exists(suboutput_dir):
        os.makedirs(suboutput_dir)
    page_num = 1
    pdf = fitz.open(file_relative_path)
    for page in pdf:
        rotate = int(0)
        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高4的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        #高丽再雕质量很好，修改为1,2023-11-04
        # zoom_x = 1.5 # (2-->1584x1224)
        # zoom_y = 1.5
        #修改为在settings.py中配置。
        mat = fitz.Matrix(zoom_x, zoom_y)
        pixmap = page.get_pixmap(matrix=mat, alpha=False)
        pixmap.pil_save(f"{output_dir}/{volumeorsutra}_{page_num}.jpg")
        print(f"第{page_num}保存图片完成")
        
        #图片拆分
        pdf_to_images2(f"{output_dir}/{volumeorsutra}_{page_num}.jpg",suboutput_dir+"/")

        page_num = page_num + 1       


def pdf_to_images2(file_relative_path, suboutput_dir):
    print("pdf_to_images2:",file_relative_path)
    filename=getfilefirstname(file_relative_path)

    # 打开原始图像
    image = pyvips.Image.new_from_file(file_relative_path)
    # 提取原始文件名
    output_dir=suboutput_dir+filename
    print(output_dir)
    #判断是否存在
    if os.path.exists(output_dir+"_files"):
        print("文件夹已经存在：",output_dir+"_files")
        renamefilepath(output_dir+"_files")

    # 生成瓦片图像
    image.dzsave(output_dir, suffix=".jpg", background=(0, 0, 0), tile_size=256, overlap=1, depth=11)       

def pdf_to_images_autosize(file_relative_path, output_dir, volumeorsutra):
    """
    file_relative_path : 文件相对路径
    """
    minWidth = 2000
    zoom_x = 1
    zoom_y = 1
    suboutput_dir = output_dir.replace("raw_images", "images")
    if not os.path.exists(suboutput_dir):
        os.makedirs(suboutput_dir)
    page_num = 1
    pdf = fitz.open(file_relative_path)
    for page in pdf:
        rotate = int(0)
        mat = fitz.Matrix(zoom_x, zoom_y)
        pixmap = page.get_pixmap(matrix=mat, alpha=False)

        # 如果图像宽度小于1000像素，则调整缩放系数
        if pixmap.width < minWidth:
            zoom_x = minWidth / pixmap.width
            zoom_y = minWidth / pixmap.width
            mat = fitz.Matrix(zoom_x, zoom_y)
            pixmap = page.get_pixmap(matrix=mat, alpha=False)

        output_path = f"{output_dir}/{volumeorsutra}_{page_num}.jpg"
        pixmap.pil_save(output_path)
        print(f"第{page_num}保存图片完成")

        # 图片拆分
        #pdf_to_images2(output_path, suboutput_dir + "/")
        page_num += 1