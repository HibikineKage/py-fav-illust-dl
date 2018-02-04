import json
import sqlite3
import twitter

db_name = 'tweets.db'

# データベースの作成と確認
def db_check(c):
    c.execute("select count(*) from sqlite_master where type='table' and name='tweets';")
    if not c.fetchone():
        c.execute("create table tweets(id integer primary key, user_id integer, url1 text, url2 text, url3 text, url4 text, downloaded integer);")
        c.execute("create index userindex on tweets(user_id);")
    c.execute("select count(*) from sqlite_master where type='table' and name='users';")
    if not c.fetchone():
        c.execute("create table users(id integer, name text, screen_name text);")
    c.commit()

# データベースにツイートとユーザーを保存
def save_tweets(tweets, users):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        db_check(c)
        c.executemany("insert into users values(?,?,?)",users)
        c.executemany("insert into tweets values(?,?,?,?,?,?,?)",tweets)
        c.commit()
        
# ツイッターにoauth接続
def open_twitter():
    with open('oauth_info.json', 'r') as f:
        oauth_info = json.load(f)
        access_token = oauth_info['access_token']
        access_token_secret = oauth_info['access_token_secret']
        consumer_key = oauth_info['consumer_key']
        consumer_secret = oauth_info['consumer_secret']

    return twitter.Twitter(
            auth=twitter.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
    )
    
# ふぁぼを取得
def get_favs(t):
    favs = []
    count = 200
    max_id = None
    for i in range(int(3200 / count)):
        if max_id is None:
            fav = t.favorites.list(count=count)
        else:
            fav = t.favorites.list(count=count, max_id=max_id)
        favs.extend(fav)
        max_id = fav[-1]['id']

# 画像の含まれるふぁぼのみを抽出
def extract_image_tweets(favs):
    return [x for x in favs if not 'media' in x['entities']]
    
def favs_to_db_format(favs)
    users = {}
    for fav in favs:
        if not 'media' in fav['entities']:
            continue
        
        # URLの抽出
        urls = []
        medias = fav['entities']['media']
        for (media, i) in zip(medias, range(len(medias))):
            if not media['type'] == 'photo':
                break
            urls.append(media['media_url_https'])
        if 0 < len(urls):
            # 4つになるよう空文字列で埋める
            urls.extend(['' for _ in range(4-len(urls))])
            # 画像の登録
            illusts.append(
                (fav['id'], fav['user']['id'], 
                urls[0], urls[1], urls[2], urls[3], '0'))
            user = fav['user']
            users[user['id']] = (user['name'], user['screen_name'])
    
    users = [(x, users[x]['name'], users[x]['screen_name']) for x in users.keys()]
    
    return (illusts, users)
    
# 特定のユーザーのツイートを抽出する
def user_tweets(user_name):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute("select id from users where name = '" + user_name + "';")
        c.
        
# ユーザー名を入力させる
def input_user_name(user_list):
    for user in user_list:
        print(user['screen_name'] + ' : ' + user['name'])
    
    print()
    print('Please input id')
    print('ex) Hibikine_Kage Hibikine_Kage_Code pokemon_onedraw')
    print('>>>', end='')

    download_users = input().split()
    
    
if __name__ == '__main__':
    t = open_twitter()
    favs = get_favs(t)
    media_favs = extract_image_tweets(favs)
    illusts, users = favs_to_db_format(media_favs)
    
    