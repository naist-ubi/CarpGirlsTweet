#coding:utf-8

from requests_oauthlib import OAuth1Session
import json
import re
import time
import datetime

consumerKey = 'quTWDwlCp6n0FZqG36dxRrjWF'
consumerSecret = 'DLZ2LGSYq5mxTOaI9TMGUHr7cvIvSqhbRE2xfRCnzxjS8S2cCA'
accessToken = '102337785-wUVeAEL68JUVkJC0lEn6m5CmtvU4fuxmq5NQBKLU'
accessSecret = 'USKxdciRz7GZwb1O6FtTKv3wur0Geq1515Md1X8IeOrC6'

usernames = []
search_words = "カープ女子"
#取得するtweetの数
tweetCount = '200'
#取得するユーザーの人数
userCount = '20'
pages = '1'

#OAuthでGET
twitter = OAuth1Session(consumerKey, consumerSecret, accessToken, accessSecret)

# タイムライン取得URL
tweetUrl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
# ユーザー取得
userUrl = "https://api.twitter.com/1.1/users/search.json"
#パラメータ
params = {}

#書き込み用ファイルを生成
fw = open("input.txt", "w")


#現在時刻をUNIX Timeで返す
def now_unix_time():
    return time.mktime(datetime.datetime.now().timetuple())


def getUser():
    pages = 1
    while(pages < 8):
        params = {'q': search_words, 'page': str(pages), 'count': userCount}
        req = twitter.get(userUrl, params=params)

        #レスポンスの確認
        if req.status_code == 200:
            #レスポンスはJSON形式
            userSearch = json.loads(req.text)
            for tweet in userSearch:
                #ユーザー名に"BOT"と入っているものは除外
                if tweet["name"].find("BOT") == -1:
                    s = tweet["id_str"]
                    usernames.append(s)
                    print(tweet["name"])
        else:
            print("Error: %d" % req.status_code)
        pages = pages + 1
        print(pages)


def getTweet(username, max_id, since_id):

    while(True):
        #ReTweetは除外
        params = {'user_id': username, 'count': tweetCount, 'include_rts': 'false'}
        #max_idの指定があれば設定する
        if max_id != -1:
            params['max_id'] = max_id
        #since_idの設定があれば設定する
        if since_id != -1:
            params['since_id'] = since_id

        req = twitter.get(tweetUrl, params=params)

        #レスポンスの確認
        if req.status_code == 200:

            limit = req.headers['x-rate-limit-remaining']
            reset = req.headers['x-rate-limit-reset']
            print(limit)

            if int(limit) == 0:
                recoverytime = int(reset) - now_unix_time()
                if recoverytime > 0:
                    print("Please wait... %d" % recoverytime)
                    time.sleep(recoverytime + 5)

            #レスポンスはJSON形式
            timeline = json.loads(req.text)
            try:
                max_id = timeline[-1]["id"] - 1
            except:
                break
            #各ツイートの本文を表示
            for tweet in timeline:
                s = tweet["text"].encode('utf-8')
                if s.find("http") == -1:
                    #リプライネーム部分消去
                    s = re.sub(r'@[A-Za-z0-9.-_]*', '', s)
                    #ハッシュタグ部分消去
                    s = re.sub(r'#[A-Za-z0-9.-_]*', '', s)
                    #ファイルへの書き込み
                    fw.write("\n%s" % s)   
        else:
            print("Error: %d" % req.status_code)


def userLoop(usernaems):
    for username in usernames:
        sinceId = -1
        maxId = -1
        print("うぇい")
        getTweet(username, max_id=maxId, since_id=sinceId)

getUser()
userLoop(usernames)
fw.close()
print("完了")
