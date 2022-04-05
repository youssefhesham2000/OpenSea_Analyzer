
import json
from threading import Thread

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import logging
from . import scraber
from . import DBManager
from . import processesManager

@csrf_exempt
def recieveUrls(request):
    urls = json.loads(request.body)
    DBManager.insert_new_urls(urls)
    return HttpResponse("ok")

@csrf_exempt
def scrabeByVersion(request):
    version_to_scrabe = json.loads(request.body)
    urls = DBManager.get_url_by_version(version_to_scrabe['version'])
    logging.warning(version_to_scrabe)
    processesManager.scrape(urls)
    return HttpResponse("ok")


@csrf_exempt
def testing(request):
    instance =  scraber.scrape_by_url((448,"https://opensea.io/assets/klaytn/0x8f5aa6b6dcd2d952a22920e8fe3f798471d05901/3562"))
    DBManager.insert_new_instance_data(instance)
    return HttpResponse("ok")