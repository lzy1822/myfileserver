import os

from uploadfile.control.dealpdf import dealpdf
#from 'uploadfile\\control\\dealpdf' import dealpdf
# from  control.dealpdf import dealpdf
# import dealpdf
def loadpdf(pdfpath:str,tcode:str,volumeorsutra:str):
    df=dealpdf()
    # 获取目录下所有文件列表
    file_list = [os.path.join(pdfpath, f) for f in os.listdir(pdfpath) if f.endswith('.pdf')]
    for file,index in zip(file_list,range(len(file_list))):
        print("正在处理第{}个文件".format(index+1))
        
        # dealpdf(file,tcode,str(index+1))

        
    pass


# p=r'G:\01【隋朝】房山石经\01 房山石经（北京华夏出版社 2000年）【30册】PDF'
# loadpdf(p,'FS','01')