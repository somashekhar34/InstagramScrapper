from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import os
from datetime import date
import random

# Instagram URL
instagram_url = "https://www.instagram.com"

# Enter the Instagram handle username
profile_url = ""

response = requests.get(f"{instagram_url}/{profile_url}")
today = date.today()
current_date = today.strftime("%d/%m/%Y")

print(response.status_code)

if response.ok:
    print("HTTP request successful")
    html = response.text
    bs_html = BeautifulSoup(html, features="lxml")
    body = bs_html.find('body')
    script_tag = body.find('script')
    script_content = script_tag.contents[0].strip()
    data_json = json.loads(script_content)

    profile_data = data_json['entry_data']['ProfilePage'][0]
    media_data = profile_data['graphql']['user']['edge_owner_to_timeline_media']['edges']

    for i in range(3):
        media = media_data[i]['node']
        is_video = media['is_video']
        shortcode = media['shortcode']
        caption = media['edge_media_to_caption']['edges'][0]['node']['text']
        hindu_newspaper = caption.find("Hindu newspaper")
        instagram_api_url = f"https://www.instagram.com/p/{shortcode}/?__a=1"
        api_data = json.load(urllib.request.urlopen(instagram_api_url))

        if hindu_newspaper != -1 and not is_video:
            folder_name = caption[16:36].strip()
            folder_path = f'D:/Upsc/{folder_name}'
            folder_name_parts = folder_name.split()
            first_part = folder_name_parts[0]
            date_parts = current_date.split('/')
            year = str(int(date_parts[0]))

            if first_part.find(year) != -1:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                    try:
                        for j in range(len(api_data['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'])):
                            resource = api_data['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][j]['node']['display_resources'][0]
                            image_url = resource['src']

                            while True:
                                filename = f'pic{j+1}.jpg'
                                file_path = os.path.join(folder_path, filename)
                                file_exists = os.path.isfile(file_path)

                                if not file_exists:
                                    with open(file_path, 'wb+') as handle:
                                        response = requests.get(image_url, stream=True)

                                        if not response.ok:
                                            print(response)

                                        for block in response.iter_content(1024):
                                            if not block:
                                                break
                                            handle.write(block)
                                else:
                                    continue
                                break

                            print("\nDownloading completed - Image:", j+1)
                    except:
                        print("Only one page of images available")

                else:
                    print("Folder already exists")
        else:
            break
