from redis import Redis
import json
import requests
from bs4 import BeautifulSoup as bs
import urllib.parse as urlparse


db = Redis()


def set_legion(user_id, v):
    db.set("{}_legion".format(user_id), v)
    

def get_legion(user_id):
    v = db.get("{}_legion".format(user_id))
    if v:
        return v.decode('utf-8')
    else:
        return 'cn'
    

def db_get_list(k):
    v = db.get(k)
    if v:
        v = v.decode('utf-8')
        v = json.loads(v)
        return v
    else:
        return []
        

def db_set_list(k, l):
    v = db_get_list(k)
    for i in l:
        if i not in v:
            v.append(i)
    db.set(k, json.dumps(v))


def db_remove(k, v):
    l = db_get_list(k)
    if v in l:
        l.remove(v)
        db.set(k, json.dumps(l))


def get_price(s, legion):
    base_url = 'https://www.steamprices.com/{}/'.format(legion)
    if s.startswith("bundle"):
        url = urlparse.urljoin(base_url, s)
    else:
        url = urlparse.urljoin(base_url, "app/%s" % s)
    check_url = 'https://store.steampowered.com/'
    if s.startswith("bundle"):
        check_url = urlparse.urljoin(check_url, s)
    else:
        check_url = urlparse.urljoin(check_url, "app/%s" % s)
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    try:
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
        title_line = "*%s* " % title
        current_line = "现价: `%s`" % current
        lowest_line = "最低: `%s`" % lowest
        check_line = "[去睇下](%s)" % check_url
        msg = "\r\n".join([title_line, current_line, lowest_line, check_line])
    except IndexError:
        msg = "你讲乜柒"
    return msg
