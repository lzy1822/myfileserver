import json
import os
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from uploadfile.serializers import FileUploadSerializer
from uploadfile.control.dealpdf  import dealpdf
from uploadfile.control.dealattach  import DealAttach

from django.shortcuts import render

from django.core.exceptions import ValidationError

def show_upload_file(request):
    '''
    显示测试上传页面
    '''
    return render(request, 'uploadfile.html')

def show_file(request):
    '''
    显示测试上传页面
    '''    
    return render(request, 'index.html')


class FileUploadView(APIView):
    """
    接收文件的接口
    """
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        """
        post 接口
        """
        print("调用 FileUploadView",request.data)
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            # 处理上传的文件
            uploaded_file = serializer.validated_data['file']
            #藏编号
            tcode = request.POST.get('tcode')
            print(tcode)
            #册、经卷 的编号。volume like 1,123。sutra like 955_1,955_30,963_1(经_卷)
            volumeorsutra = request.POST.get('volumeorsutra')
            print(volumeorsutra)

            df=dealpdf()
            #1 保存文件
            filename=df.savepdf(uploaded_file,tcode)

            #2分解pdf为图片        
            df.dealpdf(filename,tcode,volumeorsutra)

            return Response({'message': '文件上传成功'})

        return Response(serializer.errors, status=400)



class UploadWordAttachmentView(APIView):
    '''
    功能上传附件。
    调用url：http://127.0.0.1:8000/upload_attach/
    参数：在formdata中增加file对象
      const formData = new FormData(form);
      formData.append('file', file);
    逻辑：
    1.保存文件。保存前要生成一个唯一id的目录，这样可以保证文件名避免重复。而且目录根据日期分类：attach/date/uuid/file
    2.返回url实际示例：'suburl':'/files/attach/20240129/b3d9d25e-0a2b-40ad-a792-1cd38126fa67/manage.py'
    3.访问url示例：http://127.0.0.1:8000/files/attach/20240129/b3d9d25e-0a2b-40ad-a792-1cd38126fa67/manage.py
       即http://127.0.0.1:8000/是前缀
    '''
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        '''
        同上
        '''
        print("调用 UploadWordAttachmentView",request.data)
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            # 处理上传的文件
            uploaded_file = serializer.validated_data['file']
            print(uploaded_file)
            df=DealAttach()
            suburl=df.save_attach(uploaded_file)
            print('return:',suburl)
            return Response({'suburl': suburl})
        else:
            print(serializer)
        return Response(serializer.errors, status=400)
    

class UploadLocalView(APIView):
    def post(self, request, format=None):
        """
        post 接口
        """
        print("调用 FileUploadView",request.data)
        # serializer = FileUploadSerializer(data=request.data)
        # if serializer.is_valid():
        if(request.data):
           #路径
            pdfpath1=request.POST.get('pdfpath')
            #藏编号
            tcode = request.POST.get('tcode')
            print(tcode)
            #册、经卷 的编号。volume like 1,123。sutra like 955_1,955_30,963_1(经_卷)
            # volumeorsutra = request.POST.get('volumeorsutra')
            # print(volumeorsutra)
            pdfpath=os.path.join(pdfpath1,tcode)
            # 处理上传的文件
            self.loadpdf(pdfpath,tcode)
            return Response({'message': '文件上传成功'})

        return Response(serializer.errors, status=400)
    
    def loadpdf(self,pdfpath:str,tcode:str):
        df=dealpdf()
        # 获取目录下所有文件列表
        file_list = [f for f in os.listdir(pdfpath) if f.endswith('.pdf')]
        for file in file_list:
            try:
                if file.index('_')<0:
                    continue
                fpath=os.path.join(pdfpath,file)
                # 使用 split() 方法以下划线为分隔符拆分字符串
                index = file.split('_')[0]
                # print("正在处理第{}个文件".format(index))
                df.dealpdf(fpath,tcode,str(index))
            except Exception as e:
                print("处理第{}个文件失败：{}".format(index,e))

def get_sutra_dir(sutra_tcode:str):
    '''
    获取指定藏经的目录
    '''
    # 处理上传的文件
    # 判断是否存在sutra目录
    if not os.path.exists(os.path.join(os.getcwd(),'files','raw_images',sutra_tcode)):
        return None
    return os.path.join(os.getcwd(),'files','raw_images',sutra_tcode)

class UploadVolumesView(APIView):
    '''
     调用url：http://127.0.0.1:8000/all_volumes/
    '''
    def post(self, request, format=None):
        '''
        获得指定藏对应文件夹下的所有子文件夹名称，存入列表中返回给请求方
        data：{
            'sutra': 'zh'
        }
        '''
        # 解析请求数据
        data = json.loads(request.body)
        
        # 处理请求数据
        sutra = data.get('sutra', None)  # 获取 'sutra' 字段的值
        #sutra=request.data.get('sutra')
        if not sutra:
            return Response({'message': '藏经不能为空'}, status=400)
        # 处理上传的文件
        sutra_dir=get_sutra_dir(sutra)
        # 判断是否存在sutra目录
        if not os.path.exists(sutra_dir):
            return Response({'message': '藏经不存在'}, status=400)
        # 获取目录下所有子文件夹名称
       
        subdirs_with_file_count = []
        for subdir in os.listdir(sutra_dir):
            full_path = os.path.join(sutra_dir, subdir)
            if os.path.isdir(full_path):
                files = [os.path.basename(f) for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]
                subdir_info = {
                    'folder_name': subdir,
                    'file_count': len(files)
                }
                subdirs_with_file_count.append(subdir_info)
        sorted_data = sorted(subdirs_with_file_count, key=lambda x: int(x['folder_name']))
        return Response({'volumes': sorted_data})
   
    


class UploadSutrasView(APIView):
    '''
    调用url：http://127.0.0.1:8000/all_sutras/
    参数：无
    '''
    def post(self, request, format=None):
        '''
        获得指定文件夹下的藏经文件夹名称，存入列表中返回给请求方
        没有参数，返回所有藏经名称
        '''
       
        # 获取目录下所有子文件夹名称
        sutra_dir=get_sutra_dir('')
        subdirs = [os.path.basename(f) for f in os.listdir(sutra_dir) if os.path.isdir(os.path.join(sutra_dir,f))]
        return Response({'sutras': subdirs})
      
    
