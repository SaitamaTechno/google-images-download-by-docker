import requests
import time

def get_image_links(main_url, search_term, limit=3, zipped=0):
    url=main_url+"/images/" +search_term.replace(" ", "_")
    r=requests.get(url)
    if r.status_code==200:
        return "This image is already searched. Url: "+ url
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

main_url="http://192.168.1.236"
image_links=get_image_links(main_url, "son goku")
print(image_links)
