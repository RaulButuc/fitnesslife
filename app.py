from flask import Flask, render_template, json, request,redirect,session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import speech_recognition as sr
import pprint
from textblob import TextBlob
from textblob import Word
from twilio.rest import TwilioRestClient

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mamaligos'
app.config['MYSQL_DATABASE_DB'] = 'fitnessDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

r = sr.Recognizer()
m = sr.Microphone()
exerciseType = ['shoulder', 'chest', 'muscle', 'circuit', 'back', 'leg' , 'calories', 'lose weight']

@app.route('/sendSMS')
def other():
    # Find these values at https://twilio.com/user/account
    account_sid = "AC4ed44c0b7196e2c3882456916d9f0710"
    auth_token = "78181ae564197745d7621a411458cd24"
    client = TwilioRestClient(account_sid, auth_token)
     
    message = client.messages.create(to="+447759366400", from_="+441445295014",body="Hello there!")

    return render_template('index.html')

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
                text = value.encode("utf-8")
                text = text.decode("utf-8")
                for tag in TextBlob(text).tags:
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

                #Working with the state of the user
                state = TextBlob(text).sentiment.polarity
                print(state)
                print (state)
                if -1 <= state < -0.75:
                    return "weareyoung.mp3"
                elif -0.75 <= state < -0.5:
                    return "limbaromana.mp3"
                elif -0.5 <= state < -0.25:
                    return "bobmarley.mp3"
                elif -0.25 <= state < 0:
                    return "thelumineers.mp3" 
                elif 0 <= state < 0.25:
                    return "eyeofthetiger.mp3"
                elif 0.25 <= state < 0.5:
                    return "goodnight.mp3"
                elif 0.5 <= state < 0.75:
                    return "dimitrivegas.mp3"
                elif 0.75 <= state <= 1:
                    return "herecomestheboom.mp3"

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass

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
    con = mysql.connect()
    cursor = con.cursor()

    try:
        _username = request.form['username']
        _password = request.form['inputPassword']
        
        # connect to mysql
        sql = "select * from users where username ='" + _username + "'" + " and" + " passsword='" + _password + "'"

        data = cursor.fetchall()

        
        print (data)

        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
            

    except Exception as e:
        return render_template('main.html',error = str(e))

    finally:
        cursor.close()
        con.close()


@app.route('/signUp', methods=['POST','GET'])
def signUp():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name     = request.form['name']
        _surname  = request.form ['surname']
        _username = request.form['username']
        _password = request.form['password']
        _age      = request.form['age']
        _height   = request.form['height']
        _weight   = request.form['weight']
        _gender   = request.form['gender']

        _picture = "not yet"
        points = 0
        queryData =[]
        queryData.append(_username)
        queryData.append(_password)
        queryData.append(_age)
        queryData.append(_weight)
        queryData.append(_height)
        queryData.append(_picture)
        queryData.append(points)
        queryData.append(_name)
        queryData.append(_surname)


        # validate the received values
        if _name and _username and _surname and _password and _age and _height and _weight and _gender: 
            # All Good, let's call MySQL
            _hashed_password = generate_password_hash(_password)
            print (queryData[0]) #username
            print (queryData[1]) #password
            print (queryData[2])#age
            print (queryData[3])#weght
            print (queryData[4])#height
            print (queryData[5])#picture
            print (queryData[6])#points
            print (queryData[7])#name 
            print (queryData[8])#surname

            cursor.execute('INSERT INTO users(username, \
                   passsword, age, weight, height, picture_src,points,first_name, surname) \
                   VALUES ("%s", "%s", "%d", "%d", "%s", "%s", "%d", "%s","%s" )' % \
                   (queryData[0],_hashed_password,int(queryData[2]),int(queryData[3]),str(queryData[4]),queryData[5],int(queryData[6]),queryData[7],queryData[8]))

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
