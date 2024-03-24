"""download data from the web and save it to the data folder"""

from bs4 import BeautifulSoup

def csda_doc_downloader():
    pass

def get_links_from_xml_dump(txt_file):
    """get links from a web page dump
    """
    with open(txt_file, 'r') as f:
        txt = f.read()
    soup = BeautifulSoup(txt, 'html.parser')
    links = soup.find_all('a')
    links = [link.get('href') for link in links if "http"]
    return links
    

if __name__ == '__main__':
    print(get_links_from_xml_dump('texts.txt'))
