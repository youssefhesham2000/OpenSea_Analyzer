from multiprocessing import Process
from . import scraber
import logging

from . import DBManager


def scrape_worker(assigned_urls):
    instances = [scraber.scrape_by_url(url) for url in assigned_urls]
    logging.warning("finished looping")
    [DBManager.insert_new_instance_data(instance) for instance in instances]

    return


def scrape(urls):
    url_list = split_urls(urls)
    processes = []
    for i in range(6):
        process = Process(target=scrape_worker, args=((url_list[i],)))
        process.start()
        processes.append(process)
    logging.warning("finished")
    for p in processes:
        logging.warning("i am hanged")
        p.join()
        logging.warning("i am free now")
    logging.warning("finished joining")
    return


def split_urls(urls):
    url_lists = []
    length = len(urls)
    split_size = length//6
    for i in range(5):
        url_lists.append(urls[i*split_size:(i+1)*split_size-1])
    url_lists.append(urls[5*split_size:])
    return url_lists




