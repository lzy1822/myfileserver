import fitz
import pyvips
import os

'''
获得文件名
'''
def getfilefirstname(filename):
    #"/home/xian/myfileserver/files/pdf/gl/007.pdf"
    path = filename
    filename = os.path.basename(path)
    result = filename.split(".")[0]
    print(result)
    return result   


'''
获得文件列表
'''
def get_files_in_directory(directory):
    files = []
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                files.append(filepath)
    return files
#


def image_to_dzi(file_relative_path, suboutput_dir):
    print("image_to_dzi:",file_relative_path)

    # 打开原始图像
    image = pyvips.Image.new_from_file(file_relative_path)
    # 提取原始文件名
    #判断是否存在
    if os.path.exists(suboutput_dir+"_files"):
        print("文件夹已经存在：",suboutput_dir+"_files")
    else:
        # 生成瓦片图像
        image.dzsave(suboutput_dir, suffix=".jpg", background=(0, 0, 0), tile_size=256, overlap=1, depth=4)        


#######################################################
#######################################################
#下面的代码，是半自动的,实现将raw_images中的图片，生成到images中的瓦片图片。
#启动此文件的路径必须是myfilesever
#源jpg的路径需要修改下面第3行代码
#文件夹范围也需要设定，就是第4行代码的for循环的1,2
current_path = os.getcwd()#1
print("当前程序所在路径：", current_path)#2
aim_path=current_path+"/files/raw_images/ql/"#3

for i in range(1, 2):#4
    mydir=aim_path+str(i)+"/"#5
    files_list = get_files_in_directory(mydir)#6
    #print(files_list)
    for file in files_list:#7
        print(file)
        output=file.replace("raw_","").replace(".jpg","")#8
        print(output)
        image_to_dzi(file,output)#9
    