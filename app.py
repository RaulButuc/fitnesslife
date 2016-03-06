from flask import Flask, render_template, json, request,redirect,session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import speech_recognition as sr
import pprint
from textblob import TextBlob
from textblob import Word
mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'barlad'
app.config['MYSQL_DATABASE_DB'] = 'fitnessDB'
app.config['MYSQL_DATABASE_HOST'] = 'manchesterprofessionals.io'

mysql.init_app(app)

r = sr.Recognizer()
m = sr.Microphone()
exerciseType = ['shoulder', 'chest', 'muscle', 'circuit', 'back', 'leg' , 'calories', 'lose weight']

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/main')
def triggerSpeech():
    return render_template('main.html')

@app.route('/listen')
def speak():
    try:
        print("A moment of silence, please...")
        with m as source: r.adjust_for_ambient_noise(source)
        print("Set random energy threshold to {}".format(r.energy_threshold))
        #while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")

        #response array with links
        response = []
        data = []
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes: # this version of Python uses bytes for strings (Python 2)
                # print(u"You said {}".format(value).encode("utf-8"))
                text = value.encode("utf-8")
                text = text.decode("utf-8")
                # cuvant = Word(text)
                print (text + " this is the sentence")
                for tag in TextBlob(text).tags:
                    print (tag[1] + tag[0])
                    if tag[1] == 'NN' or tag[1] == 'NNP' or tag[1] == "NNS":
                        for key in exerciseType :
                            auxVar = Word(tag[0].lower()).singularize()
                            if(key == auxVar):
                                print (key + " this is it ")
                                # cursor = mysql.connect().cursor()
                                # query  = "SELECT videos.link FROM videos, workouts WHERE videos.workoutID = workouts.ID AND workouts.type='" + auxVar + "'"
                                # cursor.execute(query)
                                data.append(auxVar);
                                break

                # print (cuvant.definitions)
                how = TextBlob(text).sentiment.polarity
                print (how)
                if how > 0:
                    print ("you are happy")
                elif how < 0:
                    print ("you are sad")
                else:
                    print ("neutral mood")
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass

    return json.dumps(data)

@app.route('/main')
def runSpeech():
    return render_template('mainInterface.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('sign-up.html')

@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('index.html')
    else:
        return render_template('log-in.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/getUserRanks')
def getUserRanks():
    cursor = mysql.connect().cursor()
    query = "SELECT user_id, first_name, surname FROM `users` ORDER BY points DESC LIMIT 4;";
    
    cursor.execute(query)
    data =  cursor.fetchall()
    user = []
    for x in data:
        user.append({x[0] : x[1] + " " + x[2]})

    return json.dumps(user)

@app.route('/getBestVideos')
def getBestVideos():
   cursor = mysql.connect().cursor()
   query = "SELECT link FROM `videos` ORDER BY counter DESC LIMIT 4;"; 

   cursor.execute(query)
   data =  cursor.fetchall()
   user = []
   
   for x in data:
      user.append(x[0])

   return json.dumps(user)

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        

        
        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        


        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
            

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/signUp', methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required asdsafields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run(port=5003, debug=True)
