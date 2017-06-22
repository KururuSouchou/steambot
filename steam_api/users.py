# _*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup as bs
from xml.dom import minidom
import json


class UserDoesNotExistError(Exception):
    pass


class User(object):

    def __init__(self, steamID64, api_key):
        self.steamID64 = steamID64
        self.api_key = api_key

    def check_account(self):
        url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}".format(
            self.api_key,
            self.steamID64
        )
        d = json.loads(requests.get(url).content)
        if not d["response"]["players"]:
            raise UserDoesNotExistError
        else:
            return d["response"]["players"][0]["personaname"]

    def get_whishlist(self):
        url = "http://steamcommunity.com/profiles/{}/wishlist".format(
            self.steamID64
        )
        r = requests.get(url)
        soup = bs(r.content, "html.parser")
        wish_games = soup.findAll("div", "wishlistRow")
        game_ids = [i["id"].split("_")[-1] for i in wish_games]
        return game_ids

    @staticmethod
    def get_id_from_customURL(customURL):
        url = "http://steamcommunity.com/id/{}/?xml=1".format(
            customURL
        )
        dom = minidom.parseString(
            requests.get(url).content
        )
        steamID64 = dom.getElementsByTagName("steamID64")[0].firstChild.data
        return steamID64
