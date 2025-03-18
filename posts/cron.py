import urllib.request as libreq
import xml.etree.ElementTree as ET
from datetime import date, timedelta

from posts.models import Week, Paper


HEADER_END = 7
TITLE_LOCATION = 3
ABSTRACT_LOCATION = 4

def get_data():
    #get current date and dates for the start and end of last week, where papers will be taken from
    current_date = date.today() - timedelta(1)
    period_start = current_date - timedelta(7)
    period_end = current_date - timedelta(1)
    today = current_date.strftime("%d-%m-%Y")

    #build url for api call
    start_url = "".join([period_start.strftime("%Y"), 
                         period_start.strftime("%m"), 
                         period_start.strftime("%d")])
    end_url = "".join([period_end.strftime("%Y"), 
                       period_end.strftime("%m"), 
                       period_end.strftime("%d")])
    api_url = f'http://export.arxiv.org/api/query?search_query=all:%22machine+learning%22+AND+submittedDate:[{start_url}0600+TO+{end_url}0600]'

    # the name space from the top of the xml doc returned from the api
    ns = {"link": "http://www.w3.org/2005/Atom"}

    # get data from arxiv api and put it into tree format
    with libreq.urlopen(api_url) as url:
        r = url.read()

    r = r.decode("utf-8")
    with open("data.xml", "w") as f:
        f.write(r)

    tree = ET.parse('data.xml')
    root = tree.getroot()

    # create a list of links to the pdfs
    links = []
    # the argument to findall here is dependant on the namespace being correct
    for link in root.findall('link:entry/link:link', ns):
        if 'title' in link.attrib:
            links.append(link.attrib['href'])

    # create a list of dicts, each dict containing the title, abstract and link for a paper
    papers = []
    j = 0       # j used to iterate over the links list separately
    # iterate in this range to get around header of api call
    for i in range(HEADER_END, len(root)):
        paper = {}

        paper['title'] = root[i][TITLE_LOCATION].text
        paper['abstract'] = root[i][ABSTRACT_LOCATION].text.strip()
        paper['link'] = links[j]

        papers.append(paper)
        j += 1

    # create new Week object
    New_Week = Week(date=today)
    New_Week.save()

    #create new Paper objects for the new week
    for paper in papers:
        New_Paper = Paper(
            title = paper['title'], 
            summary = paper['abstract'], 
            link = paper['link'],
            week = New_Week
        )
        New_Paper.save()
    
    print("New Data Addded")
