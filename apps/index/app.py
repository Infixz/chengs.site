# coding: utf-8
from flask import Flask
from flask import request, make_response
from flask import redirect, abort

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>叼你？??</h><p><a href="http://localhost:8080/blog">BLOG</a></p>'


@app.route('/user/<name>')
def user_index(name):
    return "%s" % name


@app.route('/blog')
def blog():
    name = request.values.get("name", 'flask')
    resp = make_response(
            '<h1>blog<h1><a href="http://localhost:8080/blog/1">BLOG 1</a>'
            '<a href="http://localhost:8080/blog/2">BLOG 2</a>')
    resp.set_cookie("name", name)
    resp.set_cookie("age", "1 month")
    return resp


@app.route('/blog/<item_num>')
def blog_item(item_num):
    if int(item_num) > 10000:
        abort(404)
    return "the %sth blog" % item_num


@app.route('/friend')
def friend():
    return redirect('http://www.baidu.com')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
