import requests as r
import xlsxwriter
from bs4 import BeautifulSoup
import random
import time
import json
from MySig import printMySignature


def getProxy():
    website = r.get('https://www.us-proxy.org/')
    html = website.text

    soup = BeautifulSoup(html,'html.parser')

    new_soup = soup.tbody

    var = []

    index = 0
    for i in new_soup.find_all('td'):
        var.append(i.text)
#create local lsit
    l = []
    whileIndex = 0
    while(True):
        if (whileIndex < len(var)) and (var[whileIndex+4] == 'elite proxy' or 'anonymous' or 'transparent') :
            l.append(str(var[whileIndex])+":"+str(var[whileIndex+1]))
        else:
            break
        whileIndex += 8
    rand = random.choice(l).split(':')
    return "http://" + str(rand[0]) + ":" + str(rand[1])

def geturl(url):
    m = r.get(url , proxies={'http':getProxy()})
    m_text = m.text
    
    ## dd/mm/yyyy format
    date,month,year = time.strftime("%d/%m/%Y").split('/')

    #List of strings to hold post url to be scraped
    post_url = []

    soup = BeautifulSoup(m_text,'html.parser')
    for links in soup.find_all('a'):

        temp = links['href']
        temp = str(temp)
        #remove duplicates having comments and selecting only posts in same month
        if not temp.__contains__('comments') :
            list = temp.split('/')
            if len(list) > 5 and list[3] == year and list[4] == month:
                get_link = ''
                for x in list:
                    get_link += str(x)+'/'
                get_link = get_link.rstrip('/')
                post_url.append(get_link)

        else :
            continue

    return post_url

def get_individual_posts(urls):
    complete_post = {}
    for each_url in urls:
        html = r.get(each_url, proxies={'http':getProxy()})
        html = html.text
        soup_object = BeautifulSoup(html,'html.parser')
        
        # Get headline
        headline = soup_object.find('h1', class_ = 'headline')
        print("Post \n"+headline.get_text())

        #subsequent paragraph
        paragraphs = ""
        for para in soup_object.find_all('p', class_ = 'story-body-text story-content'):
            #'|' is seperator for paragraphs
            paragraphs +='|'+para.get_text()
        para_list = paragraphs.split('|')
        for x in para_list:
            #if isSpam(x) == False:
            print(x+'\n')
        d = createDict(headline.get_text(), para_list)
        complete_post.update(d)
        #generate_excel_and_json_file(headline.get_text(), para_list)
        print('\n\n\n')


def createDict(headline, para_list):
    d = {headline : x for x in para_list}
    return d

def generate_excel_and_json_file(headline,paragraphs):
    #Creates Json File
    with open(time.strftime("%d/%m/%Y") +'.json', 'w') as fp:
        json.dump(headline, fp)
        json.dump(paragraphs,fp)
    #creates Excel File
    workbook = xlsxwriter.Workbook(time.strftime("%d/%m/%Y")+'.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0


    workbook.close()

#printMySignature();
urls = geturl("http://www.nytimes.com")
get_individual_posts(urls)
