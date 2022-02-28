from urllib import response
from flask import Flask, render_template, url_for, flash, redirect
import requests
import re
from forms import URLForm 


def get_response(url):
    r = requests.get(url)
    while r.status_code != 200:
        r = response.get(url)
        print(r.text)
    return r.text

def prepare_urls(matches):
    return list({match.replace("\\u0026","&") for match in matches})
# url = input("Enter Instagram url : ")
# response = get_response(url)

# vid_matches = re.findall('"video_url":"([^"]+)"',response)
# pic_matches = re.findall('"display_url":"([^"]+)"', response)

# vid_urls = prepare_urls(vid_matches)
# pic_urls = prepare_urls(pic_matches)

# if vid_urls:
#     print(f"Detected Videos : \n{vid_urls}\n")

# if pic_urls:
#     print(f"Detected pictures : \n{pic_urls}\n")

# if not(vid_urls or pic_urls):
#     print("No videos or images found")



app = Flask(__name__)
app.config['SECRET_KEY'] = 'c968502a61da53471f4fd0fcb148cada'
# Registration Page
@app.route("/home", methods=['GET', 'POST'])
def register():
    form = URLForm()
    url = form.url
    response = get_response(url)
    vid_matches = re.findall('"video_url":"([^"]+)"',response)
    pic_matches = re.findall('"display_url":"([^"]+)"', response)

    vid_urls = prepare_urls(vid_matches)
    pic_urls = prepare_urls(pic_matches)


    if form.validate_on_submit():
        flash(f'URL submitted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('index.html', form=form, v_urls=vid_urls, p_urls=pic_urls)    


if __name__ == '__main__':
    app.run(debug=True)
