from django.shortcuts import render
import os, shutil
import subprocess
from werkzeug.utils import secure_filename
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadDocumentForm
from django.core.files.storage import FileSystemStorage
import datetime
from django import get_version
from django.http import FileResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt


g_number_of_visitor = {'8-30':30}
g_number_of_file = {'8-30':5}
date = str(datetime.date.today().month) + '-' + str(datetime.date.today().day)
# Create your views here.

def index(request):
    global g_number_of_visitor, g_number_of_file,date
    if g_number_of_visitor.get(date): #해당 날짜의 기록이 존재하면
        g_number_of_visitor[date] += 1
    else:
        g_number_of_visitor[date] = 1

    if not g_number_of_file.get(date):
        tmp = list(g_number_of_file.values())
        g_number_of_file[date] = tmp[len(tmp)-1]

    folder = 'media/my_folder/'
    if request.method=='POST' and request.FILES['inputFile']:
        if g_number_of_file.get(date):  # 해당 날짜의 기록이 존재하면
            g_number_of_file[date] += 1
        else:
            if len(g_number_of_file) == 0:
                g_number_of_file[date] = 1
            else:
                temp = list(g_number_of_file.values())
                g_number_of_file[date] = temp[len(temp) - 1] + 1  # 누적

        myfile = request.FILES['inputFile']

        fs = FileSystemStorage(location=folder)
        fs.save(myfile.name, myfile)
        filename = myfile.name
        print("파일명", filename)
        file_url = fs.url(filename)
        print('file_url: ',file_url)
        path = '/home/ubuntu/hanium-dangerzone-opensource/media/my_folder/'
        uploadpath = " " + path + filename + " "
        subprocess.call(["/usr/bin/dangerzone-container" " documenttopixels --document-filename" + uploadpath + "--pixel-dir /tmp/dangerzone-pixel --container-name flmcode/dangerzone"],shell=True)
        subprocess.call(["/usr/bin/dangerzone-container" " pixelstopdf --pixel-dir /tmp/dangerzone-pixel --safe-dir /tmp/dangerzone-safe --container-name flmcode/dangerzone --ocr 0 --ocr-lang eng"],shell=True)
        os.rename("/tmp/dangerzone-safe/safe-output-compressed.pdf",
                  "/tmp/dangerzone-safe/" + filename + "_" + "safe-output.pdf")
        file_url = '/tmp/dangerzone-safe/safe-output-compressed.pdf'
        dest_url = path + 'safe-output-compressed.pdf'
        shutil.move(file_url, dest_url)
        rm_file = 'media/my_folder/'+filename
        if os.path.isfile(rm_file):
            os.remove(rm_file)
            print(rm_file,"is deleted")
        # return render(request, 'fileupload.html', {'file_url': file_url})
        fn = 'safe-output-compressed.pdf'
        return pdf_view(request,fn)
    else:
        return render(request, 'index.html')

def pdf_view(request, fn):
    fs = FileSystemStorage()
    filename = 'my_folder/' + fn
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="safe.pdf"'
            return response
    else:
        return HttpResponseNotFound('Not Found!!!')

@csrf_exempt
def contact(request):
    return render(request, 'contact.html')

def dashboard(request):
    total_num_of_visitor_label = list(g_number_of_visitor.keys())
    total_num_of_file_label = list(g_number_of_file.keys())
    total_num_of_visitor = list(g_number_of_visitor.values())
    total_num_of_file = list(g_number_of_file.values())
    print(total_num_of_file,total_num_of_visitor)
    return render(request, 'dashboard.html',{'cnt':g_number_of_visitor[date],
                                             'file_cnt': g_number_of_file[date],
                                             'visitor_data':total_num_of_visitor,
                                             'file_data':total_num_of_file,
                                             'visitor_label': total_num_of_visitor_label,
                                             'file_label': total_num_of_file_label
                                             } )

def fileupload(request):
    return render(request,'fileupload.html')

@csrf_exempt
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


