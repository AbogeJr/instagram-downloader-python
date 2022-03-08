from urllib import response
from flask import Flask, render_template, url_for, flash, redirect
import requests
import re
from forms import URLForm 
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c968502a61da53471f4fd0fcb148cada'


def get_response(url):
    r = requests.get(url)
    while r.status_code != 200:
        r = response.get(url)
        print(r.text)
    return r.text

def prepare_urls(matches):
    return list({match.replace("\\u0026","&") for match in matches})   


# Registration Page
@app.route("/", methods=['GET', 'POST'])
def register():
    form = URLForm()
    url = form.url
    if form.validate_on_submit():
        url = form.url.data
        response = get_response(url)
        vid_matches = re.findall('"video_url":"([^"]+)"',response)
        pic_matches = re.findall('"display_url":"([^"]+)"', response)
        vid_urls = prepare_urls(vid_matches)
        pic_urls = prepare_urls(pic_matches)
        return render_template('results.html', form=form, vids=vid_urls, pics=pic_urls, title="Results")
    return render_template('index.html', form=form)     


if __name__ == '__main__':
    app.run(debug=True)
