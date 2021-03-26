from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import os
from datetime import date
import random
import image_scraper
# instagram URL
insta_url="https://www.instagram.com"
# Enter the instagram handle username
profile_url=""
response=requests.get(f"{insta_url}/{profile_url}")
today = date.today()
d1 = today.strftime("%d/%m/%Y")
print(response.status_code)
#try:
if response.ok:
    print("hi")
    html = response.text
    bs_html = BeautifulSoup(html, features="lxml")
    a = bs_html.find('body')
    b = a.find('script')
    e = b.contents[0]
    q = e[20:-1].strip()
    print(q)
    et = json.loads(q)
    #print(et)
    #print(type(et))
    ty = et['entry_data']['ProfilePage']
    put = ty[0]
    yes = put['graphql']['user']['edge_owner_to_timeline_media']['edges']
    #print(yes)
    #print(len(yes))
    for ip in range(3):
        etg = yes[ip]['node']
        flag = etg['is_video']
        hey=etg['shortcode']
        test = etg['edge_media_to_caption']['edges'][0]['node']['text']
        yat = test.find("Hindu newspaper")
        temp="https://www.instagram.com/p/"+hey+"/?__a=1"
        data = json.load(urllib.request.urlopen(temp))
        se=(data['graphql']['shortcode_media'])
        if yat!=-1 and flag==False:
            fold=test[16:36].strip()
            folder='D:/Upsc/'+fold
            dawn=fold.split()
            putin=dawn[0]
            d2=d1.split('/')
            cmp=str(int(d2[0]))
            if putin.find(cmp)!=-1 :
                if not os.path.exists(folder) :
                    os.makedirs(folder)
                    #print("Yes")
                    try:
                        for i in range(len(se['edge_sidecar_to_children']['edges'])):
                            r = se['edge_sidecar_to_children']['edges'][i]
                            what = r['node']['display_resources'][0]
                            when = what['src']
                            while True:
                                filename = 'pic' + str(i+1) + '.jpg'
                                folder_in=folder+'/'+filename
                                file_exists = os.path.isfile(folder_in)
                                if not file_exists:
                                    with open(folder_in, 'wb+') as handle:
                                        response = requests.get(when, stream=True)
                                        if not response.ok:
                                            print(response)
                                        for block in response.iter_content(1024):
                                            if not block:
                                                break
                                            handle.write(block)
                                else:
                                    continue
                                break
                            print("\ndownloading completed-","image:",i+1)
                            #break
                    except:
                        print("Only One Page....Man")

                else:
                    print("Already Exists..")

        else:
            break





