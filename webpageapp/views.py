from django.shortcuts import render
import os
import subprocess
from werkzeug.utils import secure_filename
from sendfile import sendfile
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadDocumentForm
from django.core.files.storage import FileSystemStorage
import datetime
from django import get_version
from django.http import FileResponse

g_number_of_visitor = 0
g_number_of_file = 0
is_same = False
# Create your views here.
def index(request):
    print(get_version())
    global g_number_of_visitor, g_number_of_file
    g_number_of_visitor += 1

    folder = 'media/my_folder/'
    if request.method=='POST' and request.FILES['inputFile']:
        g_number_of_file += 1
        myfile = request.FILES['inputFile']
        fs = FileSystemStorage(location=folder)
        fs.save(myfile.name, myfile)
        filename = myfile.name
        print(filename)
        # os.remove(media\my_folder\+filename, option)
        file_url = fs.url(filename)
        # uploadpath = " " + path + filename + " "
        # subprocess.call(["/usr/bin/dangerzone-container" " documenttopixels --document-filename" + uploadpath + "--pixel-dir /tmp/dangerzone-pixel --container-name flmcode/dangerzone"],shell=True)
        # subprocess.call(["/usr/bin/dangerzone-container" " pixelstopdf --pixel-dir /tmp/dangerzone-pixel --safe-dir /tmp/dangerzone-safe --container-name flmcode/dangerzone --ocr 0 --ocr-lang eng"],shell=True)
        # os.rename("/tmp/dangerzone-safe/safe-output-compressed.pdf",
        #           "/tmp/dangerzone-safe/" + filename + "_" + "safe-output.pdf")
        return render(request, 'fileupload.html',{'file_url':file_url})
    else:
        return render(request, 'index.html')
    #
    # form = UploadDocumentForm()
    # if request.method == 'POST':
    #     file = request.FILES
    #     file_name = default_storage.save(file['inputFile'], file)
    #     form = request.FILES  # Do not forget to add: request.FILES
    #     print(form)
    #     # if form.is_valid():
    #     #     # Do something with our files or simply save them
    #     #     # if saved, our files would be located in media/ folder under the project's base folder
    #     #     file = form.save(commit=False)
    #     #     return HttpResponseRedirect('/fileupload')
    # return render(request, 'index.html',{'form':form})

def contact(request):
    return render(request, 'contact.html')

def dashboard(request):
    return render(request, 'dashboard.html',{'cnt':g_number_of_visitor, 'file_cnt': g_number_of_file})

def fileupload(request):
    return render(request,'fileupload.html')

def sendmail(request):
    return render(request,'sendmail.html')


# def fileupload(request):
#     if request.method == 'POST':
#         f = request.files['file']
#         # 저장할 경로 + 파일명
#         filename = f.filename
#         print(filename)
#         path = '/tmp/'
#         f.save(path + secure_filename(filename))
#         uploadpath = " " + path + filename + " "
#         subprocess.call(["/usr/bin/dangerzone-container" " documenttopixels --document-filename" + uploadpath + "--pixel-dir /tmp/dangerzone-pixel --container-name flmcode/dangerzone"],shell=True)
#         subprocess.call(["/usr/bin/dangerzone-container" " pixelstopdf --pixel-dir /tmp/dangerzone-pixel --safe-dir /tmp/dangerzone-safe --container-name flmcode/dangerzone --ocr 0 --ocr-lang eng"],shell=True)
#         os.rename("/tmp/dangerzone-safe/safe-output-compressed.pdf",
#                   "/tmp/dangerzone-safe/" + filename + "_" + "safe-output.pdf")
#         sendfile(request, "/tmp/dangerzone-safe/" + filename + "_" + "safe-output.pdf", mimetype='application/pdf')
#         return "undone"
#     else:
#         return render(request,'fileupload.html')


