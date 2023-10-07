from flask import Flask, render_template, request, Response, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/categories-grid', methods=['GET', 'POST'])
def categories_grid():
    return render_template('categories-grid.html')

@app.route("/categories-list", methods=['GET', 'POST'])
def categories_list():
    return render_template('categories-list.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/error')
def error():
    return render_template('404.html')

@app.route("/signin", methods=['POST', 'GET'])
def signin():
    return render_template('signin.html')

@app.route("/single-post", methods=['GET','POST'])
def single_post():
    return render_template('single-post.html')

@app.route("/typography", methods=['GET', 'POST'])
def typography():
    return render_template('typography.html')

if __name__ == '__main__':
    app.run(debug=True)