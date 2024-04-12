from django.core.files.storage import FileSystemStorage
from django.conf import settings
import threading
from uploadfile.control.pdftoimage  import pdf_to_images,getfilefirstname, pdf_to_images_autosize,renamefilepath
import os

"""
线程全局记录、控制
"""
g_num_threads=0

lock = threading.Lock()  # 创建互斥锁

'''
获得配置参数
'''
def getZoomConfig(tcode):
    # 查找 'GL' 并获取对应的 x 和 y 值
    x_value=1
    y_value=1
    for item in settings.ZOOM:   
        if item['TCODE'].lower()  == tcode.lower() :
            x_value = item['x']
            y_value = item['y']
            break
    print('x:',x_value,'y:',y_value)
    return x_value,y_value


'''
分解pdf线程函数  只有这一个 
'''
def splitpdf(filename,tcode,volumeorsutra):
    global g_num_threads
    #线程开始
    with lock:
        thread_id = threading.get_ident()
        # 定义线程要执行的任务
        print("线程 begin:",thread_id,".  args:",filename)    
        g_num_threads+=1
        print("线程数量：",g_num_threads)        
    
    try:
        strsubdir=getfilefirstname(volumeorsutra).split('_')[0]
        # 指定输入的 PDF 文件路径和输出目录路径    
        output_dir = settings.MEDIA_ROOT+"/raw_images/"+tcode+"/"+strsubdir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        zoom_x,zoom_y = getZoomConfig(tcode)
        # 分解 PDF 为图片
        #pdf_to_images(filename, output_dir,tcode+"_"+volumeorsutra,zoom_x,zoom_y)
        pdf_to_images_autosize(filename, output_dir,tcode+"_"+volumeorsutra)

    except Exception as e:
        # 线程异常退出时的处理代码
        print("线程中有异常 exception:", e)
   
    with lock:
        g_num_threads -= 1
        print("线程 end:",thread_id)        
        print("线程数量：",g_num_threads)

class dealpdf:
    '''
    保存pdf
    '''
    def savepdf(self,uploaded_file,tcode):
        # 1 使用FileSystemStorage保存文件
        strFolder=settings.MEDIA_ROOT+"/pdf/"+tcode+"/"

        if os.path.exists(strFolder+uploaded_file.name):
            print("文件已经存在：",strFolder+uploaded_file.name)
            renamefilepath(strFolder+uploaded_file.name)

        file_storage = FileSystemStorage(location=strFolder)

        saved_file = file_storage.save(uploaded_file.name, uploaded_file)

        # 获取保存的文件名，原始文件名uploaded_file.name
        #保存后的文件名file_name
        file_path = file_storage.path(saved_file)
        # file_name = file_path.split("/")[-1]  # 从完整路径中提取文件名
        print("保存",file_path)
        return file_path

    '''
    处理pdf,启动线程
    '''
    def dealpdf(self,filename,tcode,volumeorsutra):              
        my_thread = threading.Thread(target=splitpdf, kwargs={"filename":filename,"tcode":tcode,"volumeorsutra":volumeorsutra})
        my_thread.start()
        #splitpdf(filename,tcode,volumeorsutra)


# 判断线程是否还在运行
#if thread.is_alive():

def loadpdf(pdfpath:str,tcode:str,volumeorsutra:str):
    df=dealpdf()
    # 获取目录下所有文件列表
    file_list = [os.path.join(pdfpath, f) for f in os.listdir(pdfpath) if f.endswith('.pdf')]
    for file,index in zip(file_list,range(len(file_list))):
        print("正在处理第{}个文件".format(index+1))
        df.dealpdf(file,tcode,str(index+1))

        
    pass


# p=r'G:\01【隋朝】房山石经\01 房山石经（北京华夏出版社 2000年）【30册】PDF'
# loadpdf(p,'FS','01')