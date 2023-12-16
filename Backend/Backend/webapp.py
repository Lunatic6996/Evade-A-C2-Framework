from flask import *
from os import close

app=Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

#@app.route("/ll",methods=['POST','GET'])
#def website():
 #   name=request.args.get("username")
  #  return render_template('index.html',name=name)


@app.route("/results", methods=['POST','GET'])
def result():
    name=request.form['username_input']
    return render_template('index.html',name=name)
    #return render_template('index.html',name=name)
'''
    if request.method == 'POST':
        # Use square brackets to access form data
        name = request.form['username_input']
        return f"<h1>{name} is your name</h1>"
    else:
        # If it's a GET request, render the template without the form result
        return render_template('index.html')
'''



#@app.route("/username/<name>")
#def welcome_user(name):
    #return f'<h1>Welcome {name}</h1>'

if __name__=='__main__':
    app.run(debug=True)

