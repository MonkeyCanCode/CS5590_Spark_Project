import json
import re
from textblob import TextBlob
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import gender_guesser.detector as gender
import csv
from pprint import pprint

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
def get_tweet_location(location):
    if location==None:
        return 'none'
    usa=["usa","USA","FL","CA","NC","PA","NY","WA","BC","GA"]
    for x in usa:
        if x in location:
            return 'usa'
    return 'ousa'

def get_tweet_gender(name):
    n=name.split(" ")
    d = gender.Detector()
    return (d.get_gender(clean_tweet(n[0])))

follow=None
temp=0
def get_tweet_follower(tweet):
    global follow,temp
    if follow==None:
        follow=[tweet]
        return
    if (temp<10):
        follow=follow+[tweet]
        temp=temp+1
        return
    for x in range(0,10):
        if (int(follow[x]["user"]["followers_count"])<int(tweet["user"]["followers_count"])):
            for i in range(0,10):
                if(favo[i]["user"]["id"]==tweet["user"]["id"]):
                    return
            for i in range(9,x,-1):
                follow[i]=follow[i-1]
            follow[x]=tweet
            return
friends=None
temp1=0
def get_tweet_friends(tweet):
    global friends,temp1
    if friends==None:
        friends=[tweet]
        return
    if (temp1<10):
        friends=friends+[tweet]
        temp1=temp1+1
        return
    for x in range(0,10):
        if (int(friends[x]["user"]["friends_count"])<int(tweet["user"]["friends_count"])):
            for i in range(0,10):
                if(favo[i]["user"]["id"]==tweet["user"]["id"]):
                    return
            for i in range(9,x,-1):
                friends[i]=friends[i-1]
            friends[x]=tweet
            return

retweet=None
temp3=0
def get_tweet_retweet(tweet):
    global retweet,temp3
    if retweet==None:
        retweet=[tweet]
        return
    if (temp3<10):
        try:
            if tweet["retweeted_status"]["retweet_count"]=="true":
                pass
        except:
            return
        retweet=retweet+[tweet]
        temp3=temp3+1
        return
    try:
        if tweet["retweeted_status"]["retweet_count"] == "true":
            pass
    except:
        return
    for x in range(0,10):
        if (int(retweet[x]["retweeted_status"]["retweet_count"])<int(tweet["retweeted_status"]["retweet_count"])):
            for i in range(0,10):
                if(favo[i]["user"]["id"]==tweet["user"]["id"]):
                    return
            for i in range(9,x,-1):
                retweet[i]=retweet[i-1]
            retweet[x]=tweet
            return
count=0
def get_tweet_count():
    global count
    count=+1
verified=0
def get_tweet_verified(tweet):
    global verified
    if tweet["user"]["verified"]==True:
        verified=verified+1

def get_tweet_title(tweet):
    if "trump" in tweet:
        return "trump"
    elif "senate" in tweet:
        return "senate"
    elif "house" in tweet:
        return "house"
    else:
        return "other"
favo=None
temp4=0
def get_tweet_favo(tweet):
    global favo,temp4
    if favo==None:
        favo=[tweet]
        return
    if (temp4<10):
        favo=favo+[tweet]
        temp4=temp4+1
        return
    for x in range(0,10):
        if (int(favo[x]["user"]["favourites_count"])<int(tweet["user"]["favourites_count"])):
            for i in range(0,10):
                if(favo[i]["user"]["id"]==(tweet["user"]["id"])):
                    return
            for i in range(9,x,-1):
                favo[i]=favo[i-1]
            favo[x]=tweet
            return


s=[]
max=25000
with open('data.json') as fp:
    ans = []
    for line in fp:
        if not line.strip():
            continue
        #print(line)
        data=json.loads(line)
        ans=ans+[data]
        max=max-1
        if(max==0):
            break



s1=[]
s2=[]
s3=0
s4=[]
'''
with open('test1.csv', 'w') as csvfile:
    print("x")
    filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(["_c0","text", "target"])
    print("x2")
    c = 0
    for x in ans:
        result=0
        print(c)
        s = s + [get_tweet_sentiment(x["text"])]
        if (s == "negative"):
            result = 0
        elif (s == "positive"):
            result = 1
        else:
            result = 2
        try:
            filewriter.writerow([c, x["text"], result])
        except:
            continue
        c = c + 1
'''

print("x2")
c=0
file=open("test12.txt","w")
file.write("_c0,text,target\n")
for x in ans:

    #s=s+[get_tweet_sentiment(x["text"])]
    s = get_tweet_sentiment(x["text"])
    if(s=="negative"):
        result=0
    elif(s=="positive"):
        result=1
    else:
        continue
    ss=str(c)+","+clean_tweet(x["text"]).replace(","," ").strip("\r\n")+","+str(result)+"\n"
    try:
        file.write(ss)
    except:
        continue
    c=c+1

file.close()
'''
    s1 = s1 + [get_tweet_location(x["user"]["location"])]
    #s2=s2+[get_tweet_gender(x["user"]["name"])]
    s4 = s4 + [get_tweet_title(x["text"])]
    get_tweet_count()
    get_tweet_verified(x)
    get_tweet_retweet(x)
    get_tweet_favo(x)
    get_tweet_follower(x)
    get_tweet_friends(x)
print("-----------favourites_count-----")
for x in range(0, 10):
    print(favo[x]["user"]["name"])
    print(favo[x]["user"]["favourites_count"])
'''


'''
plotly.tools.set_credentials_file(username='harshil134', api_key='ND3xwbelYwGP8dUBpRwM')
trump=(s4.count("trump")/(len(s4)+1))*100
senate=(s4.count("senate")/(len(s4)+1))*100
house=(s4.count("house")/(len(s4)+1))*100
other=(s4.count("other")/(len(s4)+1))*100
print(trump)
print(other)
labels = ['trump','senate','house','other']
values = [trump,senate,house,other]
trace = go.Pie(labels=labels, values=values)

py.iplot([trace], filename='title_distribution')

'''

''' 
print("------count-----------")
print(len(ans))
print("-----------------------")
print("---------account verified-----------")
print(verified)

print("-------tweet that are retweeted the most------------")
for x in range(0, 10):
    print(retweet[x]["user"]["name"])
    print(retweet[x]["retweeted_status"]["retweet_count"])
print("-----------------------")

print("------followers_count-------")
for x in range(0,10):
    print(follow[x]["user"]["name"])
    print(follow[x]["user"]["followers_count"])

print("-----------------------")
print("-------friends_count--------")
for x in range(0,10):
    print(friends[x]["user"]["name"])
    print(friends[x]["user"]["friends_count"])
print("-----------------------")
  
n=(s.count("negative")/(len(s)+1))*100
p=(s.count("positive")/(len(s)+1))*100
nu=(s.count("neutral")/(len(s)+1))*100

usa=(s1.count("usa")/(len(s1)+1))*100
no=(s1.count("none")/(len(s1)+1))*100
ousa=(s1.count("ousa")/(len(s1)+1))*100

male=(s2.count("male")/(len(s2)+1))*100
female=(s2.count("female")/(len(s2)+1))*100
unknown=(s2.count("unknown")/(len(s2)+1))*100
print("--------negative postive tweet-------------")
print("negative:" + str(n))
print("positive:" + str(p))
print("neutral:" + str(nu))

plotly.tools.set_credentials_file(username='harshil134', api_key='ND3xwbelYwGP8dUBpRwM')





plotly.offline.plot({
    "data": [go.Scatter(x=['negative', 'positive', 'neutral'], y=[n,p,nu])],
    "layout": go.Layout(title="polaritie")
}, auto_open=True)

plotly.offline.plot({
    "data": [go.Scatter(x=['tweet from usa', 'tweet from rest of the world', 'none'], y=[usa,ousa,no])],
    "layout": go.Layout(title="tweet location")
}, auto_open=True)

'''


'''
labels = ['male','female','unknown']
values = [male,female,unknown]
trace = go.Pie(labels=labels, values=values)

py.iplot([trace], filename='basic_pie_chart')







data1 = [go.Bar(
            x=['negative', 'positive', 'neutral'],
            y=[n, p, nu]
    )]

py.iplot(data1, filename='test-bar')
'''