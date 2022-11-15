from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import ConvertImageFormatModel, ToolsModel, IMAGE_FORMAT_CHOICES, convertedImageDeleteTask
from PIL import Image
from django.conf import settings
from django.utils import timezone
import string, random, os, datetime
# Create your views here.
MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
def tools(request):
    obj = ToolsModel.objects.all() 
    return render(request, 'tools/tools.html', {"obj":obj})


def AllConvertImageFormatToAnother(request):
    IMAGE_FORMAT_LIST = [i[0] for i in IMAGE_FORMAT_CHOICES]
    print(IMAGE_FORMAT_LIST)
    obj = ConvertImageFormatModel.objects.all()
    for o in obj:
        o.title = o.title.replace(' ', '-')

    return render(request, 'tools/AllConvertImageFormatToAnother.html', {"obj":obj, "IMAGE_FORMAT_LIST":IMAGE_FORMAT_LIST})

def ConvertImageFormatToAnother(request, id):
    
    """
    if '-' in title:
        title = title.replace('-', ' ')
    """
    obj = ConvertImageFormatModel.objects.filter(id=id)[0]
    
    return render(request, 'tools/ConvertImageFormatToAnother.html', {'obj':obj})

def imageConveringProcess(request):
    if request.method == 'POST':

        convert_id = request.POST['convert_id']
        img = request.FILES['img']
        img_name = img.name.rsplit('.', 1)[0]
        
        img = Image.open(img)# type: ignore
        from_format = ConvertImageFormatModel.objects.get(id=convert_id).from_format
        to_format = ConvertImageFormatModel.objects.get(id=convert_id).to_format
        string_gen_length= 50
        
        folder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=string_gen_length))
        img_path = str(MEDIA_ROOT / 'coverted_img_format' / folder_name / img_name)  + '.' + to_format

        img_url_path = MEDIA_URL + '/coverted_img_format/' + folder_name + '/' + img_name + '.' + to_format

        if from_format.lower() == 'png' and to_format.lower() == 'jpg':
                img=img.convert('RGB')
        if to_format.lower() == 'pdf':
            img=img.convert('RGB')
            
        os.mkdir(MEDIA_ROOT / 'coverted_img_format' / folder_name)
        img.save(img_path)
        task_delete_in = timezone.now() + datetime.timedelta(hours=24)
        create_task = convertedImageDeleteTask.objects.create(path=img_path, delete_date_time=task_delete_in)
        create_task.save()
        return ToolsDownloadPage(request, img_path, img_url_path)

def ToolsDownloadPage(request, path, file_url):

    def convert_bytes(size):
        """ Convert bytes to KB, or MB or GB"""
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0

    file_size = os.path.getsize(path)
    file_size = convert_bytes(file_size)
    file_name = path.split('\\')[-1]
    print(path)

    return render(request, 'tools/ToolsDownloadPage.html', {'file_size':file_size, 'file_name':file_name, 'file_url':file_url})

def HtmlToPdf(request):
    return render(request, 'tools/HtmlTo/HtmlToPdf.html')

def taskDeleteConvertedImages(requests):
    REFERER = requests.META['HTTP_REFERER']
    taskes = convertedImageDeleteTask.objects.all()
    for task in taskes:

        if task.delete_date_time <= timezone.now():
            file_path = task.path
            file_folder = file_path.rsplit('\\', 1)[0]
            os.remove(file_path)
            os.rmdir(file_folder)
            task.delete()
    return HttpResponseRedirect(REFERER)