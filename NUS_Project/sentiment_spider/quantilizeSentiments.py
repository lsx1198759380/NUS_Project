import SQL
from snownlp import SnowNLP
import tushare as ts
import pandas as pd
import math
import datetime,traceback
pd.set_option('display.max_columns',None)

def quantilizeSentiments(data,date):
    pos=neg=0
    print(len(data[date]))
    for comment in data[date]:
        try:#受到snownlp中算法限制，这里可能会因为出现了snownlp中没有的词而报错，所以添加了try-except语句
            nlp = SnowNLP(comment['comment'])
            sentimentScore = nlp.sentiments
        except:
            print(traceback.format_exc())
            continue
        if(sentimentScore>0.6):
            fans=SQL.selectFansByUserId(comment['user_id'])
            pos+=1+math.log(comment['like_count']+fans[0][0]+1,2)
        if(sentimentScore<0.4):
            fans=SQL.selectFansByUserId(comment['user_id'])
            neg+=1+math.log(comment['like_count']+fans[0][0]+1,2)
    print("负："+str(neg)+"  正："+str(pos))
    return (pos/(pos+neg+0.0001)-0.5)*math.log(len(data[date])+1,2)

# def max_min_normalization(x,max,min):#将数据标准化
#     return (x-min)/(max-min+1)

def data(share_code):#整合数据，生成excel
    print(ts.__version__)
    ts.set_token('你的token')
    a = SQL.selectCommentOrderByDate(share_code,0)
    #把评论数据变成以date为key，所有在date日发表的关于share_code股票评论为value的值的dict
    preDate = a[0][4]
    commentList = []
    comments = {}
    for i in a:
        if not i[4] == preDate:
            comments[preDate] = commentList
            commentList = [{"comment": i[2], "like_count": i[3], "user_id": i[5]}]
            preDate = i[4]
        else:
            commentList.append({"comment": i[2], "like_count": i[3], "user_id": i[5]})
    comments[preDate] = commentList

    scoreList = []
    dateList=list(comments.keys())
    for i in range(len(dateList)):
        score = quantilizeSentiments(comments, dateList[i])#第i日的评论情绪得分
        print(score)
        print(str(dateList[i])+' 计算完成')
        if i==0:
            scoreList.append([datetime.datetime.strptime(str(dateList[i]),'%Y-%m-%d').date(), score])
        else:
            scoreList.append([datetime.datetime.strptime(str(dateList[i]),'%Y-%m-%d').date(),score])#第i日的市场情绪得分
    scoreFrame = pd.DataFrame(scoreList, columns=['date', 'score'])
    scoreFrame.to_excel('score.xlsx', index=False)
    # #获得股票市场信息
    pro = ts.pro_api()
    df = pro.daily(ts_code="000001.SZ",start_date='20170601', end_date='20191231')
    print(type(df))
    df=df.rename(columns={'trade_date': 'date'})
    print(type(df['date'][0]))
    for i in range(len(df)):
        date=df['date'][i]
        df['date'][i]=datetime.datetime.strptime(date[0:4]+'-'+date[4:6]+'-'+date[6:],'%Y-%m-%d').date()
    print(type(df['date'][0]))
    df.to_excel('share.xlsx')
    share = pd.read_excel('share.xlsx')
    share = share[['date', 'close']]
    score = pd.read_excel('score.xlsx')

    print(share['date'][0])
    print(type(share['date'][0]))
    print(type(score['date'][0]))
    data = pd.merge(score, share, on='date', how='inner')
    data = data.rename(columns={'close': 'price'})
    data.to_excel('data.xlsx', index=False)

if __name__ == '__main__':
    data('zssh000001')