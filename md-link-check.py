
import markdown
import csv
import os
from bs4 import BeautifulSoup,SoupStrainer
import urllib.request
import colorama,re,queue,threading
from colorama import Fore
import validators
from urllib.parse import *
import httplib2

def check_link(address):      
    try:
        h = httplib2.Http(timeout=5)
        resp = h.request(address, 'HEAD')
        rcode=int(resp[0]['status'])
        if  rcode > 403:   
            return rcode
    except httplib2.ServerNotFoundError:
           print("ERROR: " + "Not Found");
    except Exception as e:
            print("error");


    

def getlinks(string):
    """return a list with markdown links"""
    html = markdown.markdown(string, output_format='html')
    links = list(set(re.findall(r'href=[\'"]?([^\'" >]+)', html)))
    links = list(filter(lambda l: l[0] != "{", links))
    return links



        
with open('brokenlinks.csv', 'w', newline='', errors='ignore') as csvfile:
        linkwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        directory = r'C:\Users\ROG\LinkFixer'
        for entry in os.scandir(directory):
            if (entry.path.endswith(".md")):
                    print(entry.path)
                    links =[]
                    path=entry.path
                    string = open(path,errors='ignore').read()
                    links += getlinks(string)
                    rccode = []
                    for link in links:
                        if validators.url(link):
                            address=link
                            status=""
                            status=check_link(address)
                            if status:
                                print("Broken-Link: "+link+"  Returncode: "+str(status))
                                linkwriter.writerow([entry.path,link,str(status)])
