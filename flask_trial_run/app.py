from flask import Flask, render_template, flash, redirect, Markup, request
from config import Config
from forms import LoginForm

app = Flask(__name__)  
app.config.from_object(Config)

name="To whom it may concern"

@app.route('/' or '/login', methods= ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        global name
        name = str("Dear " + str(form.username.data))
        return redirect('/index')
    return render_template('login.html', title='Log in', form=form)

@app.route("/index")
def firstpage():
    return render_template("index.html",title='Home')

# @app.route("/blog")
# def blogpage():
#     return render_template("blog.html", title='blog', posts=posts)

@app.route("/Letter")
def MyResume():
    global name
    return render_template("letter.html",title='Reid Taylor', name=name)

@app.route("/Resume")
def MyLetter():
    return render_template("calculator.html",title='Reid Taylor')

@app.route('/upload', methods=['GET','POST'])
def upload():
    region = request.args.get('region')
    if region =='contiguous':
        filename = 'contstate_plt.svg'
        alt='National Distribution of police killings in the contiguous United States'
        height = "385px"
    elif region=='continental':
        filename = 'state_plt.svg'
        alt='National Distribution of police killings in the continental United States'
        height='510px'
    elif region == 'northeast':
        filename= 'NEstate_plt.svg'
        alt='National Distribution of police killings in the Northeastern United States' 
        height = "775px"
    elif region == "southeast":
        filename= "SEstate_plt.svg"
        alt='National Distribution of police killings in the Southeastern United States'
        height = "600px"
    elif region == "midwest":
        filename= 'MWstate_plt.svg'
        alt='National Distribution of police killings in the Midwetern United States'
        height = "790px"
    elif region == "plains": 
        filename = "Pstate_plt.svg"
        alt='National Distribution of police killings in the Great Plains of the United States'
        height = "775px"
    elif region == "pacific":
        filename= "PWstate_plt.svg"
        alt='National Distribution of police killings in the Pacific Western United States'
        height = "750px"
    else:
        filename = 'state_plt.svg'
        alt='National Distribution of police killings in the continental United States'
        height = "510px"
    mfile = "POPcounty_plt.svg"
    markers = request.args.get('markers')
    if markers == 'marked':
        mfile = "POPMcounty_plt.svg"
    elif markers == "unmarked":
        mfile = "POPcounty_plt.svg"
    return render_template('upload.html', title='Data Science', filename=filename, height=height, alt=alt, mfile=mfile)

if __name__ == '__main__':
    app.run(debug=True)