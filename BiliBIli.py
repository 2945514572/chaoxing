import pprint

url='https://www.bilibili.com/video/BV1r84y1Q7Ns/?vd_source=ca054da076aeea2eb6a2283f37c05fa7'


# bilibili:
# url='https://xy117x141x153x232xy.mcdn.bilivideo.cn:4483/upgcxcode/73/85/232138573/232138573_nb2-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1693576764&gen=playurlv2&os=mcdn&oi=1864802050&trid=00004da1b85bea88484fbdc754b5276f0151u&mid=1601375910&platform=pc&upsig=f2af60b259f618235eff3cda32e8e5cc&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=1003124&bvc=vod&nettype=0&orderid=0,3&buvid=B1E08BC2-1C7F-3518-8AB5-B0F29B40AFFC43038infoc&build=0&f=u_0_0&agrr=0&bw=40090&logo=A0000001'


import re
import json
import requests
import subprocess
head={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62','referer':'https://www.bilibili.com/'}
res=requests.get(url,headers=head)
res.encoding=res.apparent_encoding
# print(res.text)
# open('B站.mp4','wb').write(res.content)
play_info=re.findall('<script>window.__playinfo__=(.*?)</script>',res.text)[0]
# print(play_info)
json_data=json.loads(play_info)
# print(json_data)
# pprint.pprint(json_data)
video_url=json_data['data']['dash']['video'][0]['baseUrl']
audio_url=json_data['data']['dash']['audio'][0]['baseUrl']
print(video_url)
v=requests.get(video_url,headers=head).content
a=requests.get(audio_url,headers=head).content
title='B站'
open(title+'.mp4','wb').write(v)
open(title+'.mp3','wb').write(a)
COMMAND = f'ffmpeg -i {title}.mp4 -i {title}.mp3 -c:v copy -c:a aac -strict experimental {title}output.mp4'

subprocess.run(COMMAND,shell=True)