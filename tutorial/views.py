
from django.shortcuts import render,HttpResponse,redirect
import json
import pandas
from subprocess import run,PIPE
import sys
import subprocess
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import seaborn as sns
import re
import collections
import plotly
import tweepy
from tweepy import OAuthHandler
from tweepy import API,Cursor
from tweepy import Stream
from tweepy.streaming import StreamListener
import pymysql
from matplotlib import pylab
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
import base64
from wordcloud import WordCloud
from django.contrib.auth.decorators import login_required

from tweepy_tutorial_copy import api

style = '''<style>

.mystyle {
    font-size: 11pt;
    font-family: Arial;
    border-collapse: collapse;
    border: 1px solid silver;

}

.mystyle td, th {
    padding: 5px;
}

.mystyle tr:nth-child(even) {
    background: #E0E0E0;
}

.mystyle tr:hover {
    background: silver;
    cursor: pointer;
}  

    </style>'''


@login_required()
def home(request):
    return render(request,'tutorial/home.html')

def trends(request):
    return render(request, 'tutorial/trends.html')
def timeline(request):
    return render(request,'tutorial/timeline.html')
full=[]

def tw_to_df(res):
    df = pd.DataFrame(data=[tweet.full_text for tweet in res], columns=['tweets'])
    df['id'] = np.array([tweet.id for tweet in res])
    df['source'] = np.array([tweet.source for tweet in res])
    # df['likes'] = np.array([tweet.favorite_count for tweet in res])
    l=[]
    for tweet in res:
        try:
            if tweet.retweeted_status:
                likes = tweet.retweeted_status.favorite_count
                l.append(likes)
        except:
            m=tweet.favorite_count
            l.append(m)
    df['likes'] = np.array(l)

    return df

@login_required()
def top_time(request):
    x = request.POST.get('screen')
    y = request.POST.get('num')
    res=[]
    for status in tweepy.Cursor(api.user_timeline, screen_name=x, tweet_mode="extended").items(int(y)):
        res.append(status)
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('colheader_justify', 'center')
    df = tw_to_df(res)
    return HttpResponse(style + df.to_html(classes='mystyle'))



def tweets_to_data_frame(res):
    df = pd.DataFrame(data=[i[2] for i in res], columns=['tweets'])
    df['id'] = np.array([i[0] for i in res])
    df['source'] = np.array([i[6] for i in res])
    df['likes'] = np.array([i[4] for i in res])
    return df



@login_required()
def search(request):
     a = request.POST.get('param')
     b= request.POST.get('number')
     # conn = pymysql.connect(host="localhost", user="root", passwd="", db="tweets_db")
     # mycursor = conn.cursor()
     user=[]
     id=[]
     res=[]
     for tweet in Cursor(api.search,tweet_mode="extended",q=a).items(int(b)):
         res.append(tweet)
         # full.append(tweet)
         # id.append(tweet.id)
         # text = tweet.full_text
         # retweet_count = tweet.retweet_count
         # create = tweet.created_at
         # likes = tweet.favorite_count
         # source=tweet.source
         # location = tweet.user.location
         # retweet="False"
         # try:
         #   if tweet.retweeted_status:
         #    retweet = "True"
         #    likes=tweet.retweeted_status.favorite_count
         # except:
         #    retweet="False"
         # reply="False"
         # try:
         #   if tweet.in_reply_to_screen_name:
         #    reply = "True"
         # except:
         #    reply="False"
         #
         # try:
         #   if not location:
         #     location="None"
         # except:
         #     location= tweet.user.location

         # sql = "INSERT INTO Tweets (retweet_count,tweet,created_time,likes,location,source,reply,retweeted) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
         # val = [retweet_count, text,create,likes,location,source,reply,retweet]
         # mycursor.execute(sql, val)
         # conn.commit()
         #add(retweet_count,text)
     # conn.close()
     pd.set_option('display.max_colwidth', -1)
     pd.set_option('colheader_justify', 'center')
     df = tw_to_df(res)
     return HttpResponse(style+df.to_html(classes='mystyle'))


@login_required()
def top_trends(request):

    b=request.POST.get('trw')
    trend = api.trends_available()
    # parentid country
    dict = {}
    res=[]
    for i in trend:
        if i['country'] not in dict:
            dict[i['country']] = i['parentid']
    if b in dict:
        t = api.trends_place(int(dict[b]))
        data = t[0]
        tr = data['trends']
        for i in tr:
            res.append(i['name'])
        pd.set_option('display.max_colwidth',-1)
        df=pd.DataFrame()
        df['trends']=list(i for i in res)
        pd.set_option('colheader_justify', 'center')
        return HttpResponse(style+df.to_html(classes='mystyle'))
        # return render(request, 'tutorial/trend_display.html',{'res':res})

    else:
        return HttpResponse("No Such COUNTRY EXISTS")



@login_required()
def show(request):
    res=[]
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="tweets_db")
    mycursor = conn.cursor()
    query = "SELECT * from tweets LIMIT 50"
    mycursor.execute(query)
    for row in mycursor.fetchall():
        res.append(row)
    df = tweets_to_data_frame(res)
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('colheader_justify', 'center')
    # return render(request,'tutorial/show.html',{'df':df.to_html(classes='mystyle')})


    return HttpResponse(style+df.to_html(classes='mystyle'))

@login_required()
def visualize(request):
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="tweets_db")
    mycursor = conn.cursor()
    query = "Select COUNT(*) from tweets"
    query1 = "Select COUNT(*) from tweets where retweeted='True' and reply='False' "
    query2 = "Select COUNT(*) from tweets where retweeted='False' and reply='True' "
    query3 = "Select COUNT(*) from tweets where retweeted='False' and reply='False' "

    mycursor.execute(query)
    data = mycursor.fetchone()

    mycursor.execute(query1)
    data1 = mycursor.fetchone()

    print("% of retweet are " + str((data1[0] / data[0]) * 100))
    mycursor.execute(query2)
    data2 = mycursor.fetchone()

    print("% of reply are " + str((data2[0] / data[0]) * 100))
    mycursor.execute(query3)
    data3 = mycursor.fetchone()
    print("% of plain tweet are " + str((data3[0] / data[0]) * 100))

    conn.close()

    len_list = [data[0], data1[0], data2[0], data3[0]]
    item_list = ['All Tweets', 'Retweets', 'Replies', 'Plain text tweets']
    plt.figure(figsize=(10, 6))
    sns.set(style="darkgrid")
    plt.title('Tweet categories', fontsize=20)
    plt.xlabel('Type of tweet')
    plt.ylabel('Number of tweets')
    sns.barplot(x=item_list, y=len_list, edgecolor='black', linewidth=1)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png= buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic= graphic.decode('utf-8')

    # graph_div = plotly.offline.plot(plt, auto_open=False, output_type="div")
    # context = {'graph_div':graph_div}
    return render(request,'tutorial/visu.html',{'graphic':graphic})

@login_required()
def hash(request):
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="tweets_db")
    mycursor = conn.cursor()

    hashtag_pattern = re.compile(r"#[a-zA-Z]+")
    query = "Select tweet from tweets"
    mycursor.execute(query)
    count = 1
    hashtag_matches = []
    for row in mycursor.fetchall():
        hashtag_matches.append(row[0])
    new_list = list(filter(hashtag_pattern.findall, hashtag_matches))
    conn.close()
    each_word = []
    for i in new_list:
        each_word.append(re.split(r'\s', i))

    hashtag_dict = {}
    for match in each_word:
        for singlematch in match:
            if re.search(r'#[a-zA-Z]', singlematch):
                if singlematch not in hashtag_dict.keys():
                    hashtag_dict[singlematch] = 1
                else:
                    hashtag_dict[singlematch] = hashtag_dict[singlematch] + 1

    hashtag_ordered_list = sorted(hashtag_dict.items(), key=lambda x: x[1])
    hashtag_ordered_list = hashtag_ordered_list[::-1]
    # Separating the hashtags and their values into two different lists
    hashtag_ordered_values = []
    hashtag_ordered_keys = []
    # Pick the 20 most used hashtags to plot
    for item in hashtag_ordered_list[0:20]:
        hashtag_ordered_keys.append(item[0])
        hashtag_ordered_values.append(item[1])

    fig, ax = plt.subplots(figsize=(12, 12))
    y_pos = np.arange(len(hashtag_ordered_keys))
    ax.barh(y_pos, list(hashtag_ordered_values)[::-1], align='center', color='green', edgecolor='black', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(hashtag_ordered_keys)[::-1])
    ax.set_xlabel("Nº of appereances")
    ax.set_title("Most used #hashtags", fontsize=20)
    plt.tight_layout(pad=3)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic1 = base64.b64encode(image_png)
    fig1 = graphic1.decode('utf-8')

    hashtag_ordered_dict = {}
    for item in hashtag_ordered_list[0:20]:
        hashtag_ordered_dict[item[0]] = item[1]
    wordcloud = WordCloud(width=1000, height=1000, random_state=21, max_font_size=200,
                          background_color='white').generate_from_frequencies(hashtag_ordered_dict)
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png1 = buffer.getvalue()
    buffer.close()
    graphic2 = base64.b64encode(image_png1)
    fig2 = graphic2.decode('utf-8')
    context={'figure1':fig1,'figure2':fig2}

    return render(request, 'tutorial/visu_hash.html', context)

@login_required()
def mentions(request):
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="tweets_db")
    mycursor = conn.cursor()

    hashtag_pattern = re.compile(r"@[a-zA-Z]+")
    query = "Select tweet from tweets"
    mycursor.execute(query)
    count = 1
    hashtag_matches = []
    for row in mycursor.fetchall():
        hashtag_matches.append(row[0])
    new_list = list(filter(hashtag_pattern.findall, hashtag_matches))
    conn.close()
    each_word = []
    for i in new_list:
        each_word.append(re.split(r'\s', i))

    hashtag_dict = {}
    for match in each_word:
        for singlematch in match:
            if re.search(r'@[a-zA-Z]', singlematch):
                if singlematch not in hashtag_dict.keys():
                    hashtag_dict[singlematch] = 1
                else:
                    hashtag_dict[singlematch] = hashtag_dict[singlematch] + 1

    hashtag_ordered_list = sorted(hashtag_dict.items(), key=lambda x: x[1])
    hashtag_ordered_list = hashtag_ordered_list[::-1]
    # Separating the hashtags and their values into two different lists
    hashtag_ordered_values = []
    hashtag_ordered_keys = []
    # Pick the 20 most used hashtags to plot
    for item in hashtag_ordered_list[0:20]:
        hashtag_ordered_keys.append(item[0])
        hashtag_ordered_values.append(item[1])

    fig, ax = plt.subplots(figsize=(12, 12))
    y_pos = np.arange(len(hashtag_ordered_keys))
    ax.barh(y_pos, list(hashtag_ordered_values)[::-1], align='center', color='green', edgecolor='black', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(hashtag_ordered_keys)[::-1])
    ax.set_xlabel("Nº of appereances")
    ax.set_title("Most Mentions", fontsize=20)
    plt.tight_layout(pad=3)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic1 = base64.b64encode(image_png)
    fig1 = graphic1.decode('utf-8')

    hashtag_ordered_dict = {}
    for item in hashtag_ordered_list[0:20]:
        hashtag_ordered_dict[item[0]] = item[1]
    wordcloud = WordCloud(width=1000, height=1000, random_state=21, max_font_size=200,
                          background_color='white').generate_from_frequencies(hashtag_ordered_dict)
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png1 = buffer.getvalue()
    buffer.close()
    graphic2 = base64.b64encode(image_png1)
    fig2 = graphic2.decode('utf-8')
    context = {'figure1': fig1, 'figure2': fig2}

    return render(request, 'tutorial/visu_hash.html', context)

@login_required()
def locat(request):
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="tweets_db")
    mycursor = conn.cursor()

    dict = {}
    query = "SELECT location from tweets"
    mycursor.execute(query)
    for row in mycursor.fetchall():
        if row[0] != "None":
            if row[0] not in dict.keys():
                dict[row[0]] = 1
            else:
                dict[row[0]] = dict[row[0]] + 1
    conn.close()
    hashtag_ordered_list = sorted(dict.items(), key=lambda x: x[1])
    hashtag_ordered_list = hashtag_ordered_list[::-1]
    # Separating the hashtags and their values into two different lists
    hashtag_ordered_values = []
    hashtag_ordered_keys = []
    # Pick the 20 most used hashtags to plot
    for item in hashtag_ordered_list[0:10]:
        hashtag_ordered_keys.append(item[0])
        hashtag_ordered_values.append(item[1])

    fig, ax = plt.subplots(figsize=(12, 12))
    y_pos = np.arange(len(hashtag_ordered_keys))
    ax.barh(y_pos, list(hashtag_ordered_values)[::-1], align='center', color='green', edgecolor='black', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list(hashtag_ordered_keys)[::-1])
    ax.set_xlabel("Nº of appereances")
    ax.set_title("Top locations", fontsize=20)
    plt.tight_layout(pad=3)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic1 = base64.b64encode(image_png)
    fig1 = graphic1.decode('utf-8')

    return render(request,'tutorial/location.html',{'graphic':fig1})

