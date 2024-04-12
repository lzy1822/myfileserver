"""附件处理模块
"""
import os
from datetime import datetime
import uuid

from django.core.files.storage import FileSystemStorage
from django.conf import settings




#类dealattach，保存附件的类
class DealAttach:
    """附件处理类，主要是为了保存docx、pdf等附件。
    """

    def __init__(self):
        pass

    def __getfolder(self):
        str_folder =settings.MEDIA_ROOT+"/attach"

        # 获取当前日期
        now = datetime.now()
        # 拼接年、月、日
        year = str(now.year)
        month = str(now.month).zfill(2)
        day = str(now.day).zfill(2)
        # 拼接字符串
        date_str = year + month + day
        str_folder =str_folder +'/'+date_str

        # 生成唯一标识字符串
        unique_id = str(uuid.uuid4())
        str_folder =str_folder +'/'+unique_id

        if not os.path.exists( str_folder  ):
            os.makedirs(str_folder )

        return str_folder




    def save_attach(self,uploaded_file):
        '''
        保存附件，要限制文件大小，避免恶意攻击
        路径：word/date/uuid/file

        '''
        # 1 使用FileSystemStorage保存文件

        str_folder=self.__getfolder()
        print(str_folder)

        file_storage = FileSystemStorage(location=str_folder)

        saved_file = file_storage.save(uploaded_file.name, uploaded_file)

        # 获取保存的文件名，原始文件名uploaded_file.name
        #保存后的文件名file_name
        file_path = file_storage.path(saved_file)
        # file_name = file_path.split("/")[-1]  # 从完整路径中提取文件名
        returl= file_path[len(settings.MEDIA_ROOT):]
        returl="/files"+returl
        print("保存",returl)
        return returl

