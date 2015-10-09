#coding:utf-8

from requests_oauthlib import OAuth1Session
import json
import re

consumerKey = 'quTWDwlCp6n0FZqG36dxRrjWF'
consumerSecret = 'DLZ2LGSYq5mxTOaI9TMGUHr7cvIvSqhbRE2xfRCnzxjS8S2cCA'
accessToken = '102337785-wUVeAEL68JUVkJC0lEn6m5CmtvU4fuxmq5NQBKLU'
accessSecret = 'USKxdciRz7GZwb1O6FtTKv3wur0Geq1515Md1X8IeOrC6'

usernames = []
search_words = "カープ女子"
tweetCount = '200'
userCount = '5'

# タイムライン取得URL
tweetUrl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
# ユーザー取得
userUrl = "https://api.twitter.com/1.1/users/search.json"
#パラメータ
params = {}


def getUser():

    params = {'q': search_words, 'count': userCount}

    #OAuthでGET
    twitter = OAuth1Session(consumerKey, consumerSecret, accessToken, accessSecret)
    req = twitter.get(userUrl, params=params)

    #レスポンスの確認
    if req.status_code == 200:
        #レスポンスはJSON形式
        userSearch = json.loads(req.text)
        for tweet in userSearch:
            if tweet["name"].find("BOT") == -1:
                s = tweet["id_str"]
                usernames.append(s)
                print(tweet["name"])

    else:
        print("Error: %d" % req.status_code)


def getTweet(usernames):
    #書き込み用ファイルを生成
    fw = open("input.txt", "w")

    for username in usernames:
        params = {'user_id': username, 'count': tweetCount, 'include_rts': 'false'}

        #OAuthでGET
        twitter = OAuth1Session(consumerKey, consumerSecret, accessToken, accessSecret)
        req = twitter.get(tweetUrl, params=params)

        #レスポンスの確認
        if req.status_code == 200:
            #レスポンスはJSON形式
            timeline = json.loads(req.text)
            #各ツイートの本文を表示
            for tweet in timeline:
                s = tweet["text"].encode('utf-8')
                if s.find("http") == -1:
                    s = re.sub(r'@[A-Za-z0-9.-_]*', '', s)
                    s = re.sub(r'#[A-Za-z0-9.-_]*', '', s)
                    fw.write("\n%s" % s)
                    print(req["x-rate-limit-remaing"])

        else:
            print("Error: %d" % req.status_code)

    fw.close()
    print("完了")

getUser()
getTweet(usernames)