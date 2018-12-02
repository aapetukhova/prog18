from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run











##from flask import Flask
##from flask import url_for, render_template, request, redirect
##
##app = Flask(__name__)
##
##app.route('/langs')
##def langs():
##    with open('langs.txt', 'r', encoding='utf-8') as f:
##        content = f.read().split('\n')
##    return render_template('index.html', content=content)
##
##if __name__ == '__main__':
##    app.run(debug=True)
##    
