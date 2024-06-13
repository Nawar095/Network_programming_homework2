from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact.html')
@app.route('/n_git')
def nawar_github():
    return render_template('nawar_git.html')
@app.route('/b_git')
def bashar_github():
    return render_template('bashar_git.html')
@app.route('/ref')
def references():
    return render_template('references.html')
@app.route('/learn_more')
def learnMore():
    return render_template('learn_more.html')

if __name__ == '__main__':
    app.run(debug=True)