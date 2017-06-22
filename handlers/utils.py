from redis import Redis
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse as urlparse


db = Redis()


def set_user(user_id, v):
    db.set("{}_steam_id".format(user_id), v)
    

def get_user(user_id):
    v = db.get("{}_steam_id".format(user_id))
    if v:
        return v.decode('utf-8')
    else:
        return 'cn'


def get_price(s):
    base_url = 'https://www.steamprices.com/cn/'

    url = urlparse.urljoin(base_url, "app/%s" % s)
    check_url = 'https://store.steampowered.com/'
    
    check_url = urlparse.urljoin(check_url, "app/%s" % s)
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')

    a = soup.find_all("div", {"class": "col-sm-8"})[0]
    try:
        current = a.find_all("td")[2].string
    except IndexError:
        current = ""
    title = soup.find("h1", {"class": "title"})
    title = [
        i.string for i in title.contents if i.string.split()
    ][0]
    try:
        lowest = soup.find_all(
            "span", {"class": "price value"}
        )[1].string
    except IndexError:
        lowest = ""
    if current and lowest and current == lowest:
        head_line = u"*閣下關注的遊戲：*"
        title_line = u"*%s*" % title
        foot_line = u"*現已達史上新低！*"
        check_line = "[買佢老味](%s)" % check_url
        msg = "\r\n".join([head_line, title_line, foot_line, check_line])
        return msg
    return None
