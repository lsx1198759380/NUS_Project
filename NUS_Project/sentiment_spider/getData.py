import requests
from bs4 import BeautifulSoup
import multiprocessing
import SQL
import time

def getHtml(url):#下载网页源代码
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; LCTE; rv:11.0) like Gecko'}
    r=requests.get(url,headers=header)
    r.encoding='utf-8'
    #print(r.status_code)
    r.raise_for_status()
    #print(r.text)
    return r.text


def getDate(commentHtml):#在网页源码中获得评论发表日期，格式：'YY-mm-dd'
    soup = BeautifulSoup(commentHtml, "html.parser")
    if soup.find("div", {"class": "zwfbtime"})==None:
        return None
    date = soup.find("div", {"class": "zwfbtime"}).text
    return date[4:14]

def getLikeCount(commentHtml):#在网页源码中获得特定评论的点赞人数
    soup = BeautifulSoup(commentHtml, "html.parser")
    if soup.find("div", {"data-like_count": True})==None:
        return None
    likeCount=soup.find("div", {"data-like_count": True})
    return int(likeCount['data-like_count'])

def getUserFans(userHtml):#在网页源码中获得用户粉丝数
            soup = BeautifulSoup(userHtml, "html.parser")
            #print(soup)
            if soup.find("a", {"id": "tafansa"}) == None:
                return None
            if soup.find("a", {"id": "tafansa"}).find("span") == None:
                return None
            fans=soup.find("a", {"id": "tafansa"}).find("span").text
            return int(fans)


def getAndStoreInf(html,share_code):
    soup = BeautifulSoup(html, "html.parser")
    #print(soup)
    contain = soup.find_all("div", {"class": "articleh"})#获取每条评论节点
    for i in contain:
        try:
            if i.find("em", {"class": "hinfo"}) == None and i.find("em", {"class": "settop"}) == None and "id" not in i.attrs.keys():#排除公告、新闻等内容
                content = i.find("span", {"class": "l3 a3"}).find("a")
                contentUrl="http://guba.eastmoney.com"+content["href"]#内容详情页面
                commentId=content["href"][-14:-5]
                userUrl = i.find("span", {"class": "l4 a4"}).find("a").attrs["href"]#用户主页链接
                if contentUrl.__contains__("qa") or contentUrl.__contains__("cfhpl"):#排除问答等内容，只保留用户评论
                    continue
                if userUrl=="http://guba.eastmoney.com/list,jjdt.html":#排除基金动态资讯
                    continue
                text=content.attrs["title"]#获取评论标题。因东方财富网股吧中大部分用户只发表简短的评论，其标题和内容一致，为简化，只爬取标题。
                commentHtml=getHtml(contentUrl)
                date=getDate(commentHtml)#获取评论发表时间
                if date==None:
                    continue
                likeCount=getLikeCount(commentHtml)#获取评论点赞数量
                if likeCount==None:
                    continue
                userId=userUrl[23:]#获取用户ID
                userFans=getUserFans(getHtml(userUrl))#用户粉丝数
                if userFans==None:
                    continue
                comment={"comment_id":commentId,"content":text,"like_count":likeCount,"date":date,"user_id":userId,"share_code":share_code}
                user={"id":userId,"fans":userFans}
                #存储到数据库中
                print(user)
                print(comment)
                SQL.storeUserInf(user)
                SQL.storeCommentInf(comment)
        except:
            continue

def run(data):
        html = getHtml("http://guba.eastmoney.com/list,"+data['share_code']+",f_" + str(data['page']) + ".html")
        getAndStoreInf(html,data['share_code'])
        print('-------------page-------------'+str(data['page']))


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=6)#多进程并行爬取，提高爬取速率。但进程不可设置过多，否则会被ban.
    for i in range(0,10):
        print(i)
        share_code=[]
        for page in range(i*5+1, (i+1)*5):
            share_code.append({'share_code':'600519','page':page})
        try:
            pool.map(run, share_code)
        except:
            pool.map(run, share_code)
        print('-------sleeping-------')
        time.sleep(30)#每爬取5个评论列表（约400个评论详情页面和400个用户页面），停止爬取30s，降低被ban的概率

