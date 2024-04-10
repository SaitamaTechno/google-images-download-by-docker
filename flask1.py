from flask import Flask, request, send_from_directory, render_template,redirect
import os
import subprocess
import threading
import json
from zipfile import ZipFile 

os.chdir("/headless/google-images-download")


def convertTuple(tup):
    st = ''.join(map(str, tup))
    return st
output_list=["empty"]
thread_available=1
def bash(keyword, limit):
    cmd=f"python3 bing_scraper.py --search '{keyword}' --limit {limit} --download"
    s = subprocess.getstatusoutput(cmd)
    output=convertTuple(s)
    path=f'images/{keyword.replace(" ", "_")}'
    files=[f"{path}/{file}" for file in os.listdir(path)]
    with ZipFile(path+'/'+keyword.replace(" ", "_")+'_all_in_one.zip','w') as zip: 
        # writing each file one by one 
        for file in files: 
            zip.write(file) 
    output_list[0]=output

#current_location=os.getcwd()
#print(current_location)

app = Flask(__name__)
# Directory where images are stored

UPLOAD_FOLDER = '.'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to serve the main page with links to images
@app.route('/')
def index():
    # Get list of image files in the images directory
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    directories=[i for i in images if os.path.isdir(i)]
    images=[i for i in images if os.path.isdir(i)==0]
    directories.sort()
    images.sort()
    return render_template('index.html', images=images,dirs=directories)

# Route to handle GET requests with search and limit arguments
@app.route('/search', methods=['GET'])
def search():
    global thread_available
    search_term = request.args.get('search')
    gui = int(request.args.get('gui'))
    limit = int(request.args.get('limit', 3))  # Default limit is 3
    # Process search and limit here (you can customize this according to your needs)
    # For now, just printing search term and limit
    if search_term and thread_available:
        thread_available=0
        output_list[0]="processing"
        print(output_list)
        threading.Thread(target=bash, args=(search_term,limit,)).start()
        return json.dumps({'system':'started', 'data':'It may take 30 seconds, refresh the page.'},ensure_ascii=False)
    elif search_term and output_list[0]=='processing':
        return json.dumps({'system':'processing', 'data':'It may take 30 seconds, refresh the page.'},ensure_ascii=False)
    elif search_term and output_list[0]!='empty' and output_list[0]!='processing' and gui==0:
        thread_available=1
        files=os.listdir(f'images/{search_term.replace(" ", "_")}')
        files=[f'/images/{search_term.replace(" ", "_")}/'+file for file in files]
        return json.dumps({'system':'finished', 'data':files},ensure_ascii=False)
    elif search_term and output_list[0]!='empty' and output_list[0]!='processing' and gui==1:
        thread_available=1
        path=f'/images/{search_term.replace(" ", "_")}'
        return redirect(path)
    return json.dumps({'system':'off', 'data':'Try passing args: /search?limit=3&search=bees on flower&gui=0'},ensure_ascii=False)

# Route to serve images from the specified directory
@app.route('/<path:filename>', methods=['GET'])
def get_image(filename):
    if os.path.isdir(filename):
        return get_dir(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<mydir>', methods=['GET'])
def get_dir(mydir):
    if os.path.isdir(mydir)!=1:
        return get_image(mydir)
    images = os.listdir(mydir)
    directories=[mydir+"/"+i for i in images if os.path.isdir(mydir+"/"+i)]
    images=[mydir+"/"+i for i in images if os.path.isdir(mydir+"/"+i)==0]
    directories.sort()
    images.sort()
    return render_template('index.html', images=images,dirs=directories)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
