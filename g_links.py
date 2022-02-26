#import requests
#from lxml import html
from googlesearch import search
#from bs4 import BeautifulSoup

def google_link(query):
    search_result_list = list(search(query, num_results=2))
    # old:     search_result_list = list(search(query, tld="co.in", num=2, stop=2, pause=1))
    '''
    page = requests.get(search_result_list[0])
    tree = html.fromstring(page.content)
    soup = BeautifulSoup(page.content, features="lxml")
    '''
    return search_result_list[0]


