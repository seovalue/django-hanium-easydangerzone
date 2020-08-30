from django.shortcuts import render
import os
import subprocess
from werkzeug.utils import secure_filename
from sendfile import sendfile
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadDocumentForm


# Create your views here.
def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def fileupload(request):
    form = UploadDocumentForm()
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)  # Do not forget to add: request.FILES
        if form.is_valid():
            # Do something with our files or simply save them
            # if saved, our files would be located in media/ folder under the project's base folder
            form.save()
    return render(request,'fileupload.html',locals())


# def fileupload(request):
#     if request.method == 'POST':
#         f = request.files['file']
#         # 저장할 경로 + 파일명
#         filename = f.filename
#         print(filename)
#         path = '/tmp/'
#         f.save(path + secure_filename(filename))
#         uploadpath = " " + path + filename + " "
#         print(uploadpath)
#         # subprocess.call(["/usr/bin/dangerzone-container" " documenttopixels --document-filename" + uploadpath + "--pixel-dir /tmp/dangerzone-pixel --container-name flmcode/dangerzone"],shell=True)
#         # subprocess.call(["/usr/bin/dangerzone-container" " pixelstopdf --pixel-dir /tmp/dangerzone-pixel --safe-dir /tmp/dangerzone-safe --container-name flmcode/dangerzone --ocr 0 --ocr-lang eng"],shell=True)
#         # os.rename("/tmp/dangerzone-safe/safe-output-compressed.pdf",
#         #           "/tmp/dangerzone-safe/" + filename + "_" + "safe-output.pdf")
#         # sendfile(request, "/tmp/dangerzone-safe/" + filename + "_" + "safe-output.pdf", mimetype='application/pdf')
#         return "undone"
#     else:
#         return render(request,'fileupload.html')