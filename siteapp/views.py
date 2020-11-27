from django.shortcuts import render
from siteapp.models import File, Counts
import os, shutil, subprocess, requests, datetime, json
from werkzeug.utils import secure_filename
from django.http import HttpResponseRedirect,FileResponse, HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import FileSystemStorage
from django import get_version
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
API_KEY = getattr(settings, 'API_KEY')
WEBHOOK_KEY = getattr(settings,'WEBHOOK_KEY')
BASE_DIR = os.getcwd()
# Create your views here.

### DB ###
def InsertFile(request,filetype,md5):
    File(filetype=filetype,md5=md5).save()
    return render(request, 'siteapp/mypage.html',{'text':'Insert: '+filetype + ' ' + md5})

def GetFile(md5):
    file = ''
    try:
        file = File.objects.filter(md5 = md5)[0]
    except:
        file = ''

    if file:
        print("id:{0}, md5:{1} is detected".format(file.id, file.md5))
        return "detected"
    else:
        return "undetected"


def InsertCounts(date, visitors, conversions):
    Counts(date=date, visitors=visitors, conversions=conversions).save()
    return

def GetCountsById(id):
    counts = Counts.objects.filter(id=id)[0] #아이디
    date = counts.date
    visitor = counts.visitors
    conversion = counts.conversions
    return date, visitor, conversion

def GetCountsByDate(date, v, f):
    try:
        counts = Counts.objects.filter(date=date)[0] #현재 일자
    except: #현재 일자로 된 데이터가 없으면
        InsertCounts(date, 0, 0)
        counts = Counts.objects.filter(date=date)[0]

    id = int(counts.id)
    min_date = 1
    if id > 15:
        min_date = id-14
    for i in range(min_date, id+1):
        date, visitor, conversion = GetCountsById(i)
        v[date] = visitor
        f[date] = conversion
    return v, f


def UpdateCounts(date, visitor, conversion):
    counts = Counts.objects.filter(date = date)[0]
    counts.visitors = visitor
    counts.conversions = conversion
    counts.save()
    return


### INDEX ####
def index(request):
    date = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-' + str(datetime.date.today().day)
    v_dic, f_dic = dict(), dict()
    v_dic, f_dic = GetCountsByDate(date, v_dic, f_dic)
    v_dic[date] += 1

    if request.method == 'POST' and request.FILES['inputFile']:
        uploaded_file = request.FILES['inputFile']
        fullname = uploaded_file.name
        ### 파일 확장자 확인
        idx = fullname.index('.')
        extensions = fullname[idx:]
        filename = fullname[:idx]
        new_filename = 'inputFile' + extensions
        media_dir = 'media/siteapp/files/'
        fs = FileSystemStorage(location=media_dir)
        fs.save(uploaded_file.name, uploaded_file)

        f_dic[date] += 1
        UpdateCounts(date, v_dic[date], f_dic[date])

        os.rename(media_dir + fullname, media_dir + new_filename)
        
        execute_dangerzone(new_filename);

        upload_path = BASE_DIR + '/'+media_dir
        virustotal_resource_id = virustotal_upload(upload_path + new_filename)
        print("resource id: ", virustotal_resource_id)
        jn = 'output.json'
        virustotal_download(virustotal_resource_id, upload_path + jn)

        rm_file = media_dir + new_filename
        if os.path.isfile(rm_file):
            os.remove(rm_file)
            print(rm_file, "is deleted")

        return viruschart(request, jn)
    else:

        UpdateCounts(date, v_dic[date], f_dic[date])
        return render(request, 'siteapp/index.html')

def execute_dangerzone(filename):
    fn_rm = 'media/siteapp/files/safe-output-compressed.pdf'
    if os.path.isfile(fn_rm):
        os.remove(fn_rm)

    filelist = list()
    mydir = '/tmp/dangerzone-pixel'
    for f in os.listdir(mydir):
        if f.endswith(".height") or f.endswith(".rgb") or f.endswith(".width"):
            filelist.append(f)
    for f in filelist:
        os.remove(os.path.join(mydir, f))
    
    uploadpath = os.getcwd() + '/media/siteapp/files/' + filename
    subprocess.call(["/usr/bin/dangerzone-container" " documenttopixels --document-filename " + uploadpath + " --pixel-dir /tmp/dangerzone-pixel --container-name flmcode/dangerzone"],shell=True)
    subprocess.call(["/usr/bin/dangerzone-container" " pixelstopdf --pixel-dir /tmp/dangerzone-pixel --safe-dir /tmp/dangerzone-safe --container-name flmcode/dangerzone --ocr 0 --ocr-lang eng"],shell=True)

    path = '/home/ubuntu/udev/media/siteapp/files/'
    file_url = '/tmp/dangerzone-safe/safe-output-compressed.pdf'
    dest_url = path + 'safe-output-compressed.pdf'
    try:
        shutil.move(file_url, dest_url)
    except:
        print("The file to be moved does not exist\n")

### VirusTotal ###
def virustotal_upload(orgfile):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': API_KEY}

    filename = "'" + orgfile + "'"
    files = {'file': (filename, open(orgfile, 'rb'))}
    response = requests.post(url, files=files, params=params)
    return response.json()['resource']


def virustotal_download(resource_id, filename):
    fs = FileSystemStorage()
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': API_KEY, 'resource': resource_id}
    response = requests.get(url, params=params)

    with fs.open(filename, 'w+') as json_file:
        json.dump(response.json(), json_file, indent=4, sort_keys=True)


def viruschart(request, jn):
    # jn = 'test.json' ##테스트
    filename = 'media/siteapp/files/' + jn
    json_data = ''
    md5 = ''
    with open(filename, 'r') as f:
        json_data = json.load(f)
        if 'scans' in json_data.keys():
            md5 = json_data['md5']
            json_data = json_data['scans']
        else:
            return pdf_view(request)

        hash = GetFile(md5)

        data = list()
        for key, val in json_data.items():
            data.append([key, val['detected']])

    if json_data == '':
        HttpResponseNotFound('NOT FOUND')
    return render(request, 'siteapp/detection.html', context={'data': data, 'hash':hash})

### file 작업 ###
def pdf_view(request):
    fs = FileSystemStorage()
    filename = 'siteapp/files/safe-output-compressed.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="safe.pdf"'

            fn = 'media/siteapp/files/safe-output-compressed.pdf'
            if os.path.isfile(fn):
                os.remove(fn)

            return response
    else:
        print("None")
        return HttpResponseRedirect(reverse('index'))


### VIEW ###
@csrf_exempt
def contact(request):
    return render(request, 'siteapp/contact.html',{'key':WEBHOOK_KEY})

def dashboard(request):
    date = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-' + str(datetime.date.today().day)

    v, f = {}, {}
    v, f = GetCountsByDate(date, v, f)

    total_v_label = list(v.keys())
    total_f_label = list(f.keys())
    total_v = list(v.values())
    total_f = list(f.values())

    #label : 날짜 모음
    #data : 해당 기간 동안의 데이터
    #cnt: 오늘의 방문자 수

    return render(request, 'siteapp/dashboard.html',{'cnt':v[date],
                                             'visitor_data':total_v,
                                             'file_data':total_f,
                                             'visitor_label': total_v_label,
                                             'file_label': total_f_label})

def fileupload(request):
    return render(request,'siteapp/fileupload.html')

def detection(request):
    return render(request, 'siteapp/detection.html')

@csrf_exempt
def sendmail(request):
    return render(request,'siteapp/sendmail.html')

