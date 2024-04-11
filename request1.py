import requests
import time

import io
from PIL import Image

def get_image_links(main_url, search_term, limit=3, zipped=0):
    url=main_url+"/images/" +search_term.replace(" ", "_")
    r=requests.get(url)
    if r.status_code==200:
        return ["This image is already searched. Url: "+ url]
    counter=0
    while 1:
        search_term=search_term.replace(" ", "%20")
        r=requests.get(f"{main_url}/search?limit={limit}&search={search_term}&gui=0")
        #print(r.text)
        print("It may take 30 seconds please wait! Time:", counter)
        counter+=1
        response=r.json()
        if "finished" in r.text:
            break
        time.sleep(1)
    if zipped==0:
        links=[main_url+link for link in response["data"] if ".zip" not in link]
    elif zipped==1:
        links=[main_url+link for link in response["data"] if ".zip" in link]
    return links


def save_image(img_name,url):
    #url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZrz4CwbEZEC67yep0rajv4Jb9dlRiPuWNRKZlrw0ke6xCRo8vNW06-zGe9Q&s'
    data = requests.get(url).content
    imgbytes = io.BytesIO(data)
    img = Image.open(imgbytes)
    with open(img_name, "wb") as f:
        f.write(imgbytes.getbuffer())

def save_images(image_links):
    for i, img_link in enumerate(image_links):
        if ".jpg" in img_link:
            img_name=search_term.replace(" ", "_")+str(i)+".jpg"
        elif ".png" in img_link:
            img_name=search_term.replace(" ", "_")+str(i)+".png"
        elif ".jpeg" in img_link:
            img_name=search_term.replace(" ", "_")+str(i)+".jpeg"
        else:
            img_name=search_term.replace(" ", "_")+str(i)+img_link[-5:]
        save_image("images/"+img_name, img_link)
"""
# example usage

search_term="dragonball super"
main_url="http://192.168.1.236"
image_links=get_image_links(main_url, search_term)
print(image_links)

if "This image is already searched." not in image_links[0]:
    save_images(image_links)
    print("images downloaded")
else:
    print("Failed to download, because the image is already searched.")
"""