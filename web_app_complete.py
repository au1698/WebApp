from flask import Flask, render_template,request,redirect,flash
import socket
import sqlite3 as sql
import webbrowser

""" The script implements a web app updated to 6/09 
"""

PORT = 65438        # The port used by the server at Neurolab

HOST = "130.251.2.215" # Public IP NEUROLAB FOR UDP CONNECTION

# Private Ip network HUAWEI P30
#HOST = "192.168.43.28"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

user_input = int(0)  # declare the function

#print(input_angle)

app = Flask(__name__)

# connect to qa_database.sq (database will be created, if not exist)
con = sql.connect('qa_database.db')

con.execute('CREATE TABLE IF NOT EXISTS Experiment_table (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'question TEXT)')

#con.row_factory = sql.Row      TO OBTAIN RAW

#con.execute('CREATE TABLE IF NOT EXISTS Experiment_table (ID INTEGER PRIMARY KEY,'
            #+ 'testo TEXT)')

con.close

# homepage
@app.route('/')
def start():
  return (render_template("ola.html")) # i put the name of the HTML fileù

# Page to Control Arduino with Buttons
@app.route('/',methods = ['POST','GET'])
def angle():
    if request.method == 'POST':

        if request.form.get('action1') == 'LEFT':
            print("left")
            user_input = 180
            user_input = str(user_input)
            s.sendto(user_input.encode(), (HOST, PORT))
            pass

        elif request.form.get('action2') == 'RIGHT':
            print("right")
            user_input = 0
            user_input = str(user_input)
            s.sendto(user_input.encode(), (HOST, PORT))
            pass

        elif request.form.get('action3') == 'CENTER':
            print("center")
            print("back")
            user_input = 90
            user_input = str(user_input)  # CONVERTIRE SEMPRE IN STRING E POI FARE L'ENCODE
            s.sendto(user_input.encode(), (HOST, PORT))
            pass
        elif request.form.get('action4') == 'BACK':
            user_input = 0
            user_input = str(user_input)
            s.sendto(user_input.encode(), (HOST, PORT))
            pass
        elif request.form.get('action5') == 'NEXT':
            print("back")
            return (render_template("sentence.html"))
            pass
        if request.form.get('action6') == 'ZOOM':
            webbrowser.open("https://us05web.zoom.us/j/82231219904?pwd=VUkySGxKSnFaNGNPenZpbzREcnhzZz09")

    return (render_template("ola.html"))

# Form Page
@app.route('/sentence',methods = ['POST','GET'])
def sentence():
   if request.method == 'POST':
       question = request.form['txt']   # the Server takes the input
       int = 00

       # Splits at space

       # store in database
       con = sql.connect('qa_database.db')
       c = con.cursor()  # cursor
       # insert data
       #c.execute("INSERT INTO Experiment_table (ID,testo) VALUES (?,?)",(int,question))
       c.execute("INSERT INTO Experiment_table (question) VALUES (?)",
                 (question,))  # QUA CI VUOLE LA VIRGOLA SENNò NON FUNZIONA (perchè una tuple)


       con.commit()  # apply changes

       # send values to arduino
   return (render_template("sentence.html", value=sentence))

if __name__ == "__main__":
    
   app.run(debug=True)  # questo runna tutto quello sopra
#app.run()
#serve(app, host='0.0.0.0', port=5000)


# debug = True allows possible Python errors to appear on the web page.

s.close()