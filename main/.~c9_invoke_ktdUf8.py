#this is the file that starts the server and has all of the server commands in it
#!/usr/bin/env python

import psycopg2
import psycopg2.extras
import os
import csv
from flask import Flask, session, render_template, request, redirect, url_for
from werkzeug import secure_filename
from itertools import repeat
import cgi, cgitb
#unicodeData.encode('ascii', 'ignore')
#from flask.ext.mail import Mail
#mail = Mail(app)

# may need this for later
#cgitb.enable()

app = Flask(__name__)

app.secret_key = os.urandom(24).encode('hex')

loginError = False
verifiedUser = ''
userType = ''


#connectToDB--------------------------------------------------------------------------------------------
def connectToDB():
    connectionString = 'dbname=umw_training user=website password=umw16p91V2Hkl8m9 host=localhost'
    print connectionString
    try:
        print("Connected to database")
        #print(psycopg2.connect(connectionString))
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")
#end connect to DB---------------------------------------------------------------------------------------

#login---------------------------------------------------------------------------------------------------    
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'username' in session and session['username'] != '':
        return redirect(url_for('adminHome'))
        
    session['username'] = ""
    pw = ""
    if 'loginError' in session:
        loginError = session['loginError']
    else:
        loginError = False
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    
    # if user typed in a post ...
    if request.method == 'POST':
      db = connectToDB()
      cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
      session['username'] = request.form['username']
      print('you are user:', session['username'])

      pw = request.form['pw']
      query = "SELECT * FROM users WHERE user_name = '%s' AND password = crypt('****************', password)" % (session['username'],)
      #print query
      cur.execute("SELECT * FROM users WHERE user_name = %s AND password = crypt(%s, password)", (session['username'], pw))
      if cur.fetchone():
         verifiedUser = session['username']
         session['loginError'] = False
         #Admins--------------------
         cur.execute("SELECT * FROM admin WHERE user_name = %s", (verifiedUser,))
         if cur.fetchone():
            session['userType'] = 'admin'
            query = "SELECT admin_id FROM admin WHERE user_name = '%s'" % (session['username'],)
       #     print query
            cur.execute("SELECT admin_id FROM admin WHERE user_name = %s", (session['username'],))
            session['ID'] = cur.fetchall()
            session['ID'] = session['ID'][0][0]
        #    print session['ID']
         #Students--------------------
         cur.execute("SELECT * FROM students WHERE user_name = %s", (verifiedUser,))
         if cur.fetchone():
            session['userType'] = 'student'
            query = "SELECT student_id FROM students WHERE user_name = '%s'" % (session['username'],)
         #   print query
            cur.execute("SELECT student_id FROM students WHERE user_name = %s", (session['username'],))
            session['ID'] = cur.fetchall()
            session['ID'] = session['ID'][0][0]
          #  print session['ID']
         
         if session['userType'] == 'admin':
            return redirect(url_for('adminHome'))
         if session['userType'] == 'student':
            return redirect(url_for('studentHome'))
      else:
         verifiedUser = ''
         session['username'] = ''
         session['loginError'] = True
         loginError = session['loginError']
    return render_template('index.html', user = verifiedUser, loginError = loginError)
#end login----------------------------------------------------------------------------------------------------

#**********************************
#*************ADMIN****************
#**********************************

#admin home---------------------------------------------------------------------------------------------------    
@app.route('/aHome', methods=['GET', 'POST'])
def adminHome():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "SELECT * FROM users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('adminHome'))
        else:
            verifiedUser = ''
            session['username'] = ''

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        #print(names)
        
    #user and userType are being passed to the website here
    return render_template('Theme/aHome.html', user = verifiedUser, userType = userType, Name = names)
#end adminHome------------------------------------------------------------------------------------------------------------------------ 

#admin calendar page------------------------------------------------------    
@app.route('/aCalendar', methods=['GET', 'POST'])
def adminCalendarPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "SELECT * FROM users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('adminHome'))
        else:
            verifiedUser = ''
            session['username'] = ''

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here
    return render_template('Theme/aCalendar.html', user = verifiedUser, userType = userType, Name = names)
#end admin calendar page--------------------------------------------------     

#admin exercises page------------------------------------------------------    
@app.route('/aExercises', methods=['GET', 'POST'])
def adminExercisesPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # get all exercises from the database ...
    rows = []
    query = "SELECT exercise_name, muscle_group, youtube_link FROM exercises"
    print query
    cur.execute("SELECT exercise_name, muscle_group, youtube_link FROM exercises")
    #if cur.fetchone():
    rows = cur.fetchall()
    print(rows)
    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    # if user typed in a post ...
    if request.method == 'POST':
        print "made it to post"
        
        #This is where we iterate through all exercises found in the database to see which one was selected.
        action = request.form['action']
        exercise = request.form['exercise']
        print(action)
        print(exercise)
        if action == 'Edit':
            session['exercise'] = exercise
            return redirect(url_for('adminEditExercisesPage'))
        if action == 'Delete':
            confirm = request.form['confirmD']
            print(confirm)
            if confirm == 'Delete':
                cur.execute("SELECT exercise_id from exercises WHERE exercise_name = %s", (exercise,))
                ID = cur.fetchall()
                ID = ID[0][0]
                print ID
                try:
                    cur.execute("DELETE FROM workout_exercises WHERE exercise_id = %s", (ID,))
                except:
                    print("Problem deleting from workout_exercises")
                    db.rollback()
                db.commit()
                query = "DELETE FROM exercises WHERE exercise_name = '%s'" % (exercise,)
                print(query)
                try:
                    cur.execute("DELETE FROM exercises WHERE exercise_name = %s", (exercise,))
                except:
                    print("Problem deleting from exercises")
                    db.rollback()
                db.commit()
            return redirect(url_for('adminExercisesPage'))
        if action == 'View':
            session['exercise'] = exercise
            return redirect(url_for('adminViewExercisesPage'))
        
    #user and userType are being passed to the website here along with the exercise data as "results".
    return render_template('Theme/aExercises.html', user = verifiedUser, userType = userType, Name = names, results = rows)
#end admin exercises page--------------------------------------------------  

#admin view exercise page------------------------------------------------------    
@app.route('/aViewExercises', methods=['GET', 'POST'])
def adminViewExercisesPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'exercise' in session:
        exercise = session['exercise']
    else:
        return redirect(url_for('adminExercisesPage'))
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # get all data for the exercise ...
    rows = []
    query = "SELECT exercise_name, muscle_group, description, youtube_link FROM exercises WHERE exercise_name = '%s'" % (exercise,)
    print query
    cur.execute("SELECT exercise_name, muscle_group, description, youtube_link FROM exercises WHERE exercise_name = %s",(exercise,))
    rows = cur.fetchall()
    print(rows)
    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    #user, userType, names, and all data for the exercise are being passed to the website here. 
    return render_template('Theme/aViewExercises.html', user = verifiedUser, userType = userType, Name = names, results = rows, exercise = exercise)
#end admin view exercises page-------------------------------------------------- 

#admin edit exercise page------------------------------------------------------    
@app.route('/aEditExercises', methods=['GET', 'POST'])
def adminEditExercisesPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'exercise' in session:
        exercise = session['exercise']
    else:
        return redirect(url_for('adminExercisesPage'))
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    badName = False
    exerciseEdited = False
    
    # get all data for the exercise ...
    rows = []
    query = "SELECT exercise_name, muscle_group, description, youtube_link FROM exercises WHERE exercise_name = '%s'" % (exercise,)
    print query
    cur.execute("SELECT exercise_name, muscle_group, description, youtube_link FROM exercises WHERE exercise_name = %s",(exercise,))
    rows = cur.fetchall()
    print(rows)
    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    if request.method == 'POST':
        print "HI"
        
        exerciseName = request.form['ename']
        print(exerciseName)
        muscleGroup = request.form['emusclegroup']
        print(muscleGroup)
        description = request.form['edesc']
        print(description)
        youTube = request.form['eyoutube']
        print(youTube)
        
        query = "SELECT exercise_name FROM exercises WHERE exercise_name = '%s'" % (exerciseName,)
        print query
        cur.execute("SELECT exercise_name FROM exercises WHERE exercise_name = %s", (exerciseName,))
        if cur.fetchone() and exerciseName != exercise:
            badName = True
        elif exerciseName == '':
            badName = True
        else:
            badName = False
            exerciseEdited = True
            query = "UPDATE exercises SET (admin_id, exercise_name, description, muscle_group, youtube_link) = ('%s', '%s', '%s', '%s', '%s') WHERE exercise_name = '%s'" % (session['ID'],exerciseName,description,muscleGroup,youTube,exercise)
            print query
            try:
                cur.execute("UPDATE exercises SET (admin_id, exercise_name, description, muscle_group, youtube_link) = (%s, %s, %s, %s, %s) WHERE exercise_name = %s", (session['ID'],exerciseName,description,muscleGroup,youTube,exercise))
            except:
                print("Problem updating exercises")
                db.rollback()
            db.commit()
            session['exercise'] = exerciseName
            exercise = exerciseName
            # get the newly updated exercies ready for display
            cur.execute("SELECT exercise_name, muscle_group, description, youtube_link FROM exercises WHERE exercise_name = %s",(exercise,))
            rows = cur.fetchall()
            print("done!")
    #user, userType, names, and all data for the exercise are being passed to the website here. badName and exerciseEdited are for error and success notification.
    return render_template('Theme/aEditExercises.html', user = verifiedUser, userType = userType, Name = names, results = rows, exercise = exercise, badName = badName, exerciseEdited = exerciseEdited)
#end admin edit exercises page--------------------------------------------------

#admin create exercises page------------------------------------------------------    
@app.route('/aCreateExercise', methods=['GET', 'POST'])
def adminCreateExercisePage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    badName = False
    exerciseCreated = False

    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        
        exerciseName = request.form['ename']
        print(exerciseName)
        muscleGroup = request.form['emusclegroup']
        print(muscleGroup)
        description = request.form['edesc']
        print(description)
        youTube = request.form['eyoutube']
        print(youTube)
        
        query = "SELECT exercise_name FROM exercises WHERE exercise_name = '%s'" % (exerciseName,)
        print query
        cur.execute("SELECT exercise_name FROM exercises WHERE exercise_name = %s", (exerciseName,))
        if cur.fetchone():
            badName = True
            #return redirect(url_for('adminCreateExercisePage'))
        elif exerciseName == '':
            badName = True
        else:
            badName = False
            exerciseCreated = True
            query = "INSERT INTO exercises (admin_id, exercise_name, description, muscle_group, youtube_link) VALUES ('%s', '%s', '%s', '%s', '%s')" % (session['ID'],exerciseName,description,muscleGroup,youTube)
            print query
            try:
                cur.execute("INSERT INTO exercises (admin_id, exercise_name, description, muscle_group, youtube_link) VALUES (%s, %s, %s, %s, %s)", (session['ID'],exerciseName,description,muscleGroup,youTube))
            except:
                print("Problem inserting into exercises")
                db.rollback()
            db.commit()
            
            print("done!")

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here. badName and exerciseCreated are for error and success notification.
    return render_template('Theme/aCreateExercise.html', user = verifiedUser, userType = userType, Name = names, badName = badName, exerciseCreated = exerciseCreated)
#end admin create exercise page--------------------------------------------------

#admin workouts page------------------------------------------------------    
@app.route('/aWorkouts', methods=['GET', 'POST'])
def adminWorkoutsPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    session['exerciseCount'] = 2
    session['previousInput'] = [['','','','','','','']]
    #session['previousInput'].append(['cat','','','','',''])
    print("exerciseCount= ",session['exerciseCount'])
    # get all workouts from the database ...
    rows = []
    query = "SELECT workout_name FROM workouts"
    print query
    cur.execute("SELECT workout_name FROM workouts")
    #if cur.fetchone():
    rows = cur.fetchall()
    print(rows)
    
    workoutInfo = []
    query = "SELECT workout_id, workout_name FROM workouts"
    print query
    cur.execute("SELECT workout_id, workout_name FROM workouts")
    #if cur.fetchone():
    workoutInfo = cur.fetchall()
    print(workoutInfo)
    
    workoutInfoRows = []
    
    for row in workoutInfo:
        query = "SELECT count(workout_id) FROM workout_exercises WHERE workout_id = '%s';" % (row[0],)
        print query
        cur.execute("SELECT count(workout_id) FROM workout_exercises WHERE workout_id = %s",(row[0],))
        workoutInfoRows.append([cur.fetchone()[0]])
    print('workoutInfoRows= ', workoutInfoRows)

    ## For dubugging ##
    #print(rows[0][0])
    
    
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        print "made it to post"
        
        #This is where we iterate through all workouts found in the database to see which one was selected.
        action = request.form['action']
        workout = request.form['workout']
        print(action)
        print(workout)
        if action == 'Edit':
            session['workout'] = workout
            return redirect(url_for('adminEditWorkoutsPage'))
        if action == 'Delete':
            confirm = request.form['confirmD']
            print(confirm)
            if confirm == 'Delete':
                
                query = "SELECT workout_id FROM workouts WHERE workout_name = '%s'" % (workout,)
                print(query)
                cur.execute("SELECT workout_id FROM workouts WHERE workout_name = %s", (workout,))
                deleteID = cur.fetchall()[0][0]
                print deleteID
                
                try:
                    cur.execute("DELETE FROM workout_exercises WHERE workout_id = %s", (deleteID,))
                except:
                    print("Problem deleting from workout_exercises")
                    db.rollback()
                db.commit()
                
                query = "DELETE FROM workouts WHERE workout_id = %s" % (deleteID,)
                print(query)
                try:
                    cur.execute("DELETE FROM workouts WHERE workout_id = %s", (deleteID,))
                except:
                    print("Problem deleting from workouts")
                    db.rollback()
                db.commit()
                
            return redirect(url_for('adminWorkoutsPage'))
        if action == 'View':
            print("action= ", action)
            session['workout'] = workout
            print(session['workout'])
            return redirect(url_for('adminViewWorkoutsPage'))
        
    #user and userType are being passed to the website here along with the workout data as "results".
    return render_template('Theme/aWorkouts.html', user = verifiedUser, userType = userType, Name = names, results = rows, workoutInfoRows = workoutInfoRows)
#end admin workout page--------------------------------------------------  

#admin create workout page------------------------------------------------------    
@app.route('/aCreateWorkout', methods=['GET', 'POST'])
def adminCreateWorkoutPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    badName = False
    workoutCreated = False
    badInput = False
    workoutName = ''
    
    if 'exerciseCount' not in session:
        session['exerciseCount'] = 2
        print("exerciseCount= ",session['exerciseCount'])
    
    query = "SELECT exercise_name FROM exercises"
    print query
    cur.execute("SELECT exercise_name FROM exercises")
    
    
    exercises = cur.fetchall()
    print("exerciseCount= ",session['exerciseCount'])

    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        inc = request.form['inc']
        if inc == 'add':
            badName = False
            workoutName = request.form['name']
            print("exerciseCount#= ",session['exerciseCount'])
            for i in range(1,session['exerciseCount']):
                print(str(i))
                exercise = str(request.form['exercise'+str(i)])
                row1 = str(request.form['row1-'+str(i)])
                print(row1)
                row2 = str(request.form['row2-'+str(i)])
                print(row2)
                row3 = str(request.form['row3-'+str(i)])
                print(row3)
                row4 = str(request.form['row4-'+str(i)])
                print(row4)
                row5 = str(request.form['row5-'+str(i)])
                print(row5)
                comments = str(request.form['comments'+str(i)])
                print(comments)
                if i == 1:
                    print("made it to if")
                    session['previousInput'] = [[str(exercise), str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)]]
                else:
                    print("made it to else")
                    session['previousInput'].append([str(exercise), str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)])
            session['previousInput'].append(['', '', '', '', '', ''])
            session['exerciseCount'] = session['exerciseCount']+1
            print("previousInput= ",session['previousInput'])
            print("exerciseCount!= ",session['exerciseCount'])
        
        elif inc == 'cancel':
            badName = False
            workoutName = request.form['name']
            print("exerciseCount#= ",session['exerciseCount'])
            for i in range(1,session['exerciseCount']):
                print(str(i))
                exercise = str(request.form['exercise'+str(i)])
                row1 = str(request.form['row1-'+str(i)])
                print(row1)
                row2 = str(request.form['row2-'+str(i)])
                print(row2)
                row3 = str(request.form['row3-'+str(i)])
                print(row3)
                row4 = str(request.form['row4-'+str(i)])
                print(row4)
                row5 = str(request.form['row5-'+str(i)])
                print(row5)
                comments = str(request.form['comments'+str(i)])
                print(comments)
                if i == 1:
                    print("made it to if")
                    session['previousInput'] = [[str(exercise), str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)]]
                else:
                    print("made it to else")
                    session['previousInput'].append([str(exercise),str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)])
            print("previousInput= ",session['previousInput'])
            print("exerciseCount!= ",session['exerciseCount'])
            
        else:
            workoutName = request.form['name']
            print(workoutName)
        
            query = "SELECT workout_name FROM workouts WHERE workout_name = '%s'" % (workoutName,)
            print query
            cur.execute("SELECT workout_name FROM workouts WHERE workout_name = %s", (workoutName,))
            if cur.fetchone():
                badName = True
                #workoutName = request.form['name']
                print("exerciseCount#= ",session['exerciseCount'])
                for i in range(1,session['exerciseCount']):
                    print(str(i))
                    exercise = str(request.form['exercise'+str(i)])
                    row1 = str(request.form['row1-'+str(i)])
                    print(row1)
                    row2 = str(request.form['row2-'+str(i)])
                    print(row2)
                    row3 = str(request.form['row3-'+str(i)])
                    print(row3)
                    row4 = str(request.form['row4-'+str(i)])
                    print(row4)
                    row5 = str(request.form['row5-'+str(i)])
                    print(row5)
                    comments = str(request.form['comments'+str(i)])
                    print(comments)
                    if i == 1:
                        print("made it to if")
                        session['previousInput'] = [[str(exercise), str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)]]
                    else:
                        print("made it to else")
                        session['previousInput'].append([str(exercise),str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)])
                print("previousInput= ",session['previousInput'])
                print("exerciseCount!= ",session['exerciseCount'])
            elif workoutName == '':
                badName = True
                #workoutName = request.form['name']
                print("exerciseCount#= ",session['exerciseCount'])
                for i in range(1,session['exerciseCount']):
                    print(str(i))
                    exercise = str(request.form['exercise'+str(i)])
                    row1 = str(request.form['row1-'+str(i)])
                    print(row1)
                    row2 = str(request.form['row2-'+str(i)])
                    print(row2)
                    row3 = str(request.form['row3-'+str(i)])
                    print(row3)
                    row4 = str(request.form['row4-'+str(i)])
                    print(row4)
                    row5 = str(request.form['row5-'+str(i)])
                    print(row5)
                    comments = str(request.form['comments'+str(i)])
                    print(comments)
                    if i == 1:
                        print("made it to if")
                        session['previousInput'] = [[str(exercise), str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)]]
                    else:
                        print("made it to else")
                        session['previousInput'].append([str(exercise),str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)])
                print("previousInput= ",session['previousInput'])
                print("exerciseCount!= ",session['exerciseCount'])
            else:
                badName = False
                workoutCreated = True

                print("exerciseCount= ",session['exerciseCount'])
                for i in range(1,session['exerciseCount']):
                    print(str(i))
                    exercise = str(request.form['exercise'+str(i)])
                    row1 = str(request.form['row1-'+str(i)])
                    if any(c.isalpha() for c in row1):
                        for c in row1:
                            if c.isalpha() and c != 'x':
                                badInput = True
                                workoutCreated = False
                        if 'x' in row1:
                            if row1.count('x') > 1:
                                badInput = True
                                workoutCreated = False
                            if row1[0] is not None and len(row1) > 0:
                                if row1[0] == 'x':
                                    badInput = True
                                    workoutCreated = False
                                if row1[len(row1)-1] == 'x':
                                    badInput = True
                                    workoutCreated = False
                        if '/' in row1:
                            if row1.count('/') > 1:
                                badInput = True
                                workoutCreated = False
                            if row1[0] is not None and len(row1) > 0:
                                if row1[0] == '/':
                                    badInput = True
                                    workoutCreated = False
                                if row1[len(row1)-1] == '/':
                                    badInput = True
                                    workoutCreated = False
                    elif '/' in row1:
                        if row1.count('/') > 1:
                            badInput = True
                            workoutCreated = False
                        if row1[0] is not None and len(row1) > 0:
                            if row1[0] == '/':
                                badInput = True
                                workoutCreated = False
                            if row1[len(row1)-1] == '/':
                                badInput = True
                                workoutCreated = False
                    elif row1 != '':
                        badInput = True
                        workoutCreated = False
                    print(row1)
                    row2 = str(request.form['row2-'+str(i)])
                    if any(c.isalpha() for c in row2):
                        for c in row2:
                            if c.isalpha() and c != 'x':
                                badInput = True
                                workoutCreated = False
                        if 'x' in row2:
                            if row2.count('x') > 1:
                                badInput = True
                                workoutCreated = False
                            if row2[0] is not None and len(row2) > 0:
                                if row2[0] == 'x':
                                    badInput = True
                                    workoutCreated = False
                                if row2[len(row2)-1] == 'x':
                                    badInput = True
                                    workoutCreated = False
                        if '/' in row2:
                            if row2.count('/') > 1:
                                badInput = True
                                workoutCreated = False
                            if row2[0] is not None and len(row2) > 0:
                                if row2[0] == '/':
                                    badInput = True
                                    workoutCreated = False
                                if row2[len(row2)-1] == '/':
                                    badInput = True
                                    workoutCreated = False
                    elif '/' in row2:
                        if row2.count('/') > 1:
                            badInput = True
                            workoutCreated = False
                        if row2[0] is not None and len(row2) > 0:
                            if row2[0] == '/':
                                badInput = True
                                workoutCreated = False
                            if row2[len(row2)-1] == '/':
                                badInput = True
                                workoutCreated = False
                    elif row2 != '':
                        badInput = True
                        workoutCreated = False
                    row3 = str(request.form['row3-'+str(i)])
                    if any(c.isalpha() for c in row3):
                        for c in row3:
                            if c.isalpha() and c != 'x':
                                badInput = True
                                workoutCreated = False
                        if 'x' in row3:
                            if row3.count('x') > 1:
                                badInput = True
                                workoutCreated = False
                            if row3[0] is not None and len(row3) > 0:
                                if row3[0] == 'x':
                                    badInput = True
                                    workoutCreated = False
                                if row3[len(row3)-1] == 'x':
                                    badInput = True
                                    workoutCreated = False
                        if '/' in row3:
                            if row3.count('/') > 1:
                                badInput = True
                                workoutCreated = False
                            if row3[0] is not None and len(row3) > 0:
                                if row3[0] == '/':
                                    badInput = True
                                    workoutCreated = False
                                if row3[len(row3)-1] == '/':
                                    badInput = True
                                    workoutCreated = False
                    elif '/' in row3:
                        if row3.count('/') > 1:
                            badInput = True
                            workoutCreated = False
                        if row3[0] is not None and len(row3) > 0:
                            if row3[0] == '/':
                                badInput = True
                                workoutCreated = False
                            if row3[len(row3)-1] == '/':
                                badInput = True
                                workoutCreated = False
                    elif row3 != '':
                        badInput = True
                        workoutCreated = False
                    row4 = str(request.form['row4-'+str(i)])
                    if any(c.isalpha() for c in row4):
                        for c in row4:
                            if c.isalpha() and c != 'x':
                                badInput = True
                                workoutCreated = False
                        if 'x' in row4:
                            if row4.count('x') > 1:
                                badInput = True
                                workoutCreated = False
                            if row4[0] is not None and len(row4) > 0:
                                if row4[0] == 'x':
                                    badInput = True
                                    workoutCreated = False
                                if row4[len(row4)-1] == 'x':
                                    badInput = True
                                    workoutCreated = False
                        if '/' in row4:
                            if row4.count('/') > 1:
                                badInput = True
                                workoutCreated = False
                            if row4[0] is not None and len(row4) > 0:
                                if row4[0] == '/':
                                    badInput = True
                                    workoutCreated = False
                                if row4[len(row4)-1] == '/':
                                    badInput = True
                                    workoutCreated = False
                    elif '/' in row4:
                        if row4.count('/') > 1:
                            badInput = True
                            workoutCreated = False
                        if row4[0] is not None and len(row4) > 0:
                            if row4[0] == '/':
                                badInput = True
                                workoutCreated = False
                            if row4[len(row4)-1] == '/':
                                badInput = True
                                workoutCreated = False
                    elif row4 != '':
                        badInput = True
                        workoutCreated = False
                    row5 = str(request.form['row5-'+str(i)])
                    if any(c.isalpha() for c in row5):
                        for c in row5:
                            if c.isalpha() and c != 'x':
                                badInput = True
                                workoutCreated = False
                        if 'x' in row5:
                            if row5.count('x') > 1:
                                badInput = True
                                workoutCreated = False
                            if row5[0] is not None and len(row5) > 0:
                                if row5[0] == 'x':
                                    badInput = True
                                    workoutCreated = False
                                if row5[len(row5)-1] == 'x':
                                    badInput = True
                                    workoutCreated = False
                        if '/' in row5:
                            if row5.count('/') > 1:
                                badInput = True
                                workoutCreated = False
                            if row5[0] is not None and len(row5) > 0:
                                if row5[0] == '/':
                                    badInput = True
                                    workoutCreated = False
                                if row5[len(row5)-1] == '/':
                                    badInput = True
                                    workoutCreated = False
                    elif '/' in row5:
                        if row5.count('/') > 1:
                            badInput = True
                            workoutCreated = False
                        if row5[0] is not None and len(row5) > 0:
                            if row5[0] == '/':
                                badInput = True
                                workoutCreated = False
                            if row5[len(row5)-1] == '/':
                                badInput = True
                                workoutCreated = False
                    elif row5 != '':
                        badInput = True
                        workoutCreated = False
                    print(row5)
                    comments = str(request.form['comments'+str(i)])
                    print(comments)
                    if i == 1:
                        print("made it to if")
                        session['previousInput'] = [[str(exercise), str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)]]
                    else:
                        print("made it to else")
                        session['previousInput'].append([str(exercise),str(row1), str(row2), str(row3), str(row4), str(row5), str(comments)])
                print("previousInput= ",session['previousInput'])
                print("exerciseCount!= ",session['exerciseCount'])
                if workoutCreated == True:
                    query = "INSERT INTO workouts (admin_id, workout_name) VALUES (%s, '%s')" % (session['ID'],workoutName)
                    print query
                    try:
                        cur.execute("INSERT INTO workouts (admin_id, workout_name) VALUES (%s, %s)", (session['ID'],workoutName))
                    except:
                        print("Problem inserting into workouts")
                        db.rollback()
                    db.commit()  
                
                    for i in range(1,session['exerciseCount']):
                        print(str(i))
                        exercise = request.form['exercise'+str(i)]
                        print(exercise)
                        row1 = request.form['row1-'+str(i)]
                        print(row1)
                        row2 = request.form['row2-'+str(i)]
                        print(row2)
                        row3 = request.form['row3-'+str(i)]
                        print(row3)
                        row4 = request.form['row4-'+str(i)]
                        print(row4)
                        row5 = request.form['row5-'+str(i)]
                        print(row5)
                        comments = request.form['comments'+str(i)]
                        print(comments)
                
                        query = "SELECT exercise_id FROM exercises WHERE exercise_name = '%s'" % (exercise,)
                        print query
                        cur.execute("SELECT exercise_id FROM exercises WHERE exercise_name = %s", (exercise,))
                        exerciseID = cur.fetchall()
                        query = "SELECT workout_id FROM workouts WHERE workout_name = '%s'" % (workoutName,)
                        print query
                        cur.execute("SELECT workout_id FROM workouts WHERE workout_name = %s", (workoutName,))
                        workoutID = cur.fetchall()
                    
                        print("exerciseID=", exerciseID)
                        print("workoutID=", workoutID)
                    
                        query = "INSERT INTO workout_exercises (exercise_id, workout_id, row_1, row_2, row_3, row_4, row_5, comments) VALUES (%s, %s, '%s', '%s', '%s', '%s', '%s', '%s')" % (exerciseID[0][0],workoutID[0][0],row1,row2,row3,row4,row5,comments)
                        print query
                
                        try:
                            cur.execute("INSERT INTO workout_exercises (exercise_id, workout_id, row_1, row_2, row_3, row_4, row_5, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (exerciseID[0][0],workoutID[0][0],row1,row2,row3,row4,row5,comments))
                        except:
                            print("Problem inserting into workouts")
                            db.rollback()
                        db.commit()
                
                print("done!")

    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
    #user and userType are being passed to the website here. badName and workoutCreated are for error and success notification.
    return render_template('Theme/aCreateWorkout.html', user = verifiedUser, userType = userType, Name = names, badName = badName, badInput = badInput, exercises = exercises, workoutCreated = workoutCreated, workoutName = workoutName, exerciseCount = session['exerciseCount'], previousInput = session['previousInput'])
#end admin create workout page--------------------------------------------------

#admin view workouts page------------------------------------------------------    
@app.route('/aViewWorkouts', methods=['GET', 'POST'])
def adminViewWorkoutsPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'workout' in session:
        workout = session['workout']
    else:
        return redirect(url_for('adminWorkoutsPage'))
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # get all data for the exercise ...
    workoutsTable = []
    exercises = []
    rows = []
    query = "SELECT workout_name, workout_id FROM workouts WHERE workout_name = '%s'" % (workout,)
    print query
    cur.execute("SELECT workout_name, workout_id FROM workouts WHERE workout_name = %s",(workout,))
    workoutsTable = cur.fetchall()
    print(workoutsTable)

    query = "SELECT exercise_id, row_1, row_2, row_3, row_4, row_5, comments FROM workout_exercises WHERE workout_id = '%s'" % (workoutsTable[0][1],)
    print query
    cur.execute("SELECT exercise_id, row_1, row_2, row_3, row_4, row_5, comments FROM workout_exercises WHERE workout_id = %s",(workoutsTable[0][1],))
    rows = cur.fetchall()
    print(rows)
    
    for row in rows:
        query = "SELECT exercise_name FROM exercises WHERE exercise_id = '%s'" % (row[0],)
        print query
        cur.execute("SELECT exercise_name FROM exercises WHERE exercise_id = %s",(row[0],))
        exercises.append(cur.fetchall())
        print(exercises)
    
    
    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    #user, userType, names, and all data for the exercise are being passed to the website here. 
    return render_template('Theme/aViewWorkouts.html', user = verifiedUser, userType = userType, Name = names, results = rows, workout = workout, workoutsTable = workoutsTable, exercises = exercises)
#end admin view workouts page--------------------------------------------------
@app.route('/aEditWorkouts', methods = ['GET', 'POST'])
def adminEditWorkoutsPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

#admin training programs page------------------------------------------------------    
@app.route('/aTrainingPrograms', methods=['GET', 'POST'])
def adminTrainingProgramsPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #session['exerciseCount'] = 2
    #session['previousInput'] = [['','','','','','','']]
    #session['previousInput'].append(['cat','','','','',''])
    #print("exerciseCount= ",session['exerciseCount'])
    # get all training programs from the database ...
    rows = []
    query = "SELECT training_program_name, sport FROM training_programs"
    print query
    cur.execute("SELECT training_program_name, sport FROM training_programs")
    #if cur.fetchone():
    rows = cur.fetchall()
    print('rows= ', rows)
    
    trainingProgramInfo = []
    query = "SELECT training_program_id, training_program_name FROM training_programs"
    print query
    cur.execute("SELECT training_program_id, training_program_name FROM training_programs")
    #if cur.fetchone():
    trainingProgramInfo = cur.fetchall()
    print('trainingProgramInfo= ', trainingProgramInfo)
    
    trainingProgramInfoRows = []
    for row in trainingProgramInfo:
        query = "SELECT count(training_program_id) FROM training_program_workouts WHERE training_program_id = '%s';" % (row[0],)
        print('query= ', query)
        cur.execute("SELECT count(training_program_id) FROM training_program_workouts WHERE training_program_id = %s",(row[0],))
        trainingProgramInfoRows.append([cur.fetchone()[0]])
    print('trainingProgramInfoRows= ', trainingProgramInfoRows)

    ## For dubugging ##
    #print(rows[0][0])
    
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        print "made it to post"
        
        #This is where we iterate through all workouts found in the database to see which one was selected.
        action = request.form['action']
        trainingProgram = request.form['trainingProgram']
        print(action)
        print(trainingProgram)
        if action == 'Edit':
            session['trainingProgram'] = trainingProgram
            return redirect(url_for('adminEditTrainingProgramPage'))
        if action == 'Delete':
            confirm = request.form['confirmD']
            print(confirm)
            if confirm == 'Delete':
                
                query = "SELECT training_program_id FROM training_programs WHERE training_program_name = '%s'" % (trainingProgram,)
                print(query)
                cur.execute("SELECT training_program_id FROM training_programs WHERE training_program_name = %s", (trainingProgram,))
                deleteID = cur.fetchall()[0][0]
                print deleteID
                
                try:
                    cur.execute("DELETE FROM training_program_workouts WHERE training_program_id = %s", (deleteID,))
                except:
                    print("Problem deleting from training_program_workouts")
                    db.rollback()
                db.commit()
                
                query = "DELETE FROM training_programs WHERE training_program_id = %s" % (deleteID,)
                print(query)
                try:
                    cur.execute("DELETE FROM training_programs WHERE training_program_id = %s", (deleteID,))
                except:
                    print("Problem deleting from training_programs")
                    db.rollback()
                db.commit()
                
            return redirect(url_for('adminTrainingProgramsPage'))
        if action == 'View':
            print("action= ", action)
            session['trainingProgram'] = trainingProgram
            print(session['trainingProgram'])
            return redirect(url_for('adminViewTrainingProgramPage'))
        
    #user and userType are being passed to the website here along with the workout data as "results".
    return render_template('Theme/aTrainingPrograms.html', user = verifiedUser, userType = userType, Name = names, results = rows, trainingProgramInfoRows=trainingProgramInfoRows)
#end admin Training Program page--------------------------------------------------

#admin view Training Program page------------------------------------------------------    
@app.route('/aViewTrainingProgram', methods=['GET', 'POST'])
def adminViewTrainingProgramPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'workout' in session:
        workout = session['workout']
    else:
        return redirect(url_for('adminTrainingProgramsPage'))
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # get all data for the exercise ...
    workoutsTable = []
    exercises = []
    rows = []
    query = "SELECT workout_name, workout_id FROM workouts WHERE workout_name = '%s'" % (workout,)
    print query
    cur.execute("SELECT workout_name, workout_id FROM workouts WHERE workout_name = %s",(workout,))
    workoutsTable = cur.fetchall()
    print(workoutsTable)

    query = "SELECT exercise_id, row_1, row_2, row_3, row_4, row_5, comments FROM workout_exercises WHERE workout_id = '%s'" % (workoutsTable[0][1],)
    print query
    if (user_exists)
    rows = cur.fetchall()
    print(rows)
    
    for row in rows:
        query = "SELECT exercise_name FROM exercises WHERE exercise_id = '%s'" % (row[0],)
        print query
        cur.execute("SELECT exercise_name FROM exercises WHERE exercise_id = %s",(row[0],))
        exercises.append(cur.fetchall())
        print(exercises)
    
    
    ## For dubugging ##
    #print(rows[0][0])
    names = None
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    #user, userType, names, and all data for the exercise are being passed to the website here. 
    return render_template('Theme/aViewTrainingProgram.html', user = verifiedUser, userType = userType, Name = names, results = rows, workout = workout, workoutsTable = workoutsTable, exercises = exercises)
#end admin view workouts page--------------------------------------------------


@app.route('/add_students_from_file', methods=['POST'])
def add_students_from_file():
    pass

@app.route("/add_single_student", methods=["POST"])
def add_single_student():
    
    username = request.form['student_username']
    first_name = request.form['student_first_name']
    last_name = request.form['student_last_name']
    email = request.form['student_email']
    sport = request.form['student_sport']
    year = request.form['student_year']
    one_rep_max = 0 # add this to the form later
    
    add_student(username, first_name, last_name, sport, year, email, one_rep_max)
    
    return redirect(url_for('adminAddUserPage'))

@app.route("/add_single_admin", methods=["POST"])
def add_single_admin():
    
    username = request.form['admin_username']
    first_name = request.form['admin_first_name']
    last_name = request.form['admin_last_name']
    email = request.form['admin_email']
    
    add_admin(username, first_name, last_name, email)
    
    return redirect(url_for('adminAddUserPage'))

def add_student(username, first_name, last_name, sport, year, email, one_rep_max, cur = None, db = None):
    
    if cur == None or db == None: # load the database only when it has not been provided by the caller / prevents loading & closing the database multiple times when adding users from a CSV
        db = connectToDB()
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    user_added = add_user(username) # using default password of 'password'
    
    if not user_added:
        return False
        
    query = "INSERT INTO students (user_name, first_name, last_name, sport, year, email, one_rep_max) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (username, first_name, last_name, sport, year, email, one_rep_max)
    
    try:
        cur.execute(query, values)
        db.commit()
        d
    except Exception as e:
        print("Error: ")
        print(e)
        print("Problem inserting into students")
        db.rollback()
    
    return True

def add_user(username, password='password', cur = None, db = None):
    
    if cur == None or db == None: # load the database only when it has not been provided by the caller / prevents loading & closing the database multiple times when adding users from a CSV
        db = connectToDB()
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    user_exists_query = "SELECT user_name FROM users WHERE user_name = %s"
    cur.execute(user_exists_query, (username,))
    user_exists = cur.fetchone()
    if not user_exists:
        return redirect(url_for('adminAddUserPage'))
    
    new_user_query = "INSERT INTO users VALUES (%s, crypt(%s, gen_salt('bf')))"
    try:
        cur.execute(new_user_query, (username, password))
        db.commit()
    except Exception as e: # catch the exception so we can show better error information to the console
        print("Error: ")
        print(e)
        return False
        db.rollback()
        
    
        
    return True
    
    
def add_admin(username, first_name, last_name, email, cur = None, db = None):
    
    if cur == None or db == None:
        db = connectToDB()
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    query = "INSERT INTO admin (user_name, first_name, last_name, email) VALUES (%s, %s, %s, %s)"
    values = (username, first_name, last_name, email)
    
    try:
        cur.execute(query, values)
    except:
        print("Problem inserting into admin")
        db.rollback()
        
    db.commit()


#admin add user page------------------------------------------------------    
@app.route('/aAddUser', methods=['GET', 'POST'])
def adminAddUserPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        return redirect(url_for('login'))
    
    if 'userType' in session:
        userType = session['userType']
    else:
        return redirect(url_for('login'))
    
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # get all exercises from the database ...
    rows = []
    types = []
    
    query = "SELECT user_name, first_name, last_name, email FROM admin"
    #print query
    cur.execute("SELECT user_name, first_name, last_name, email FROM admin")
    rows = cur.fetchall()
    thisType = ['Admin']
    thisType = [x for item in thisType for x in repeat(item, cur.rowcount)]
    types = types + thisType
    #print(rows)
    #print(types)
    #print("rowcount= ",cur.rowcount)
    
    query = "SELECT user_name, first_name, last_name, email FROM students"
    #print query
    cur.execute("SELECT user_name, first_name, last_name, email FROM students")
    rows = rows + cur.fetchall()
    thisType = ['Student']
    thisType = [x for item in thisType for x in repeat(item, cur.rowcount)]
    types = types + thisType
    #print(rows)
    #print(types)
    #print("rowcount= ",cur.rowcount)
    
    ## For dubugging ##
    #print(rows[0][0])
    
    # if user typed in a post ...
    if request.method == 'POST':
        
        #csv stuff starts here---------------------------------------
        if 'browse_file' in request.files:
            print('in browse')
            if request.files['browse_file']:
                file = request.files['browse_file']
                filename = secure_filename(str(file.filename))
                fileContents = str(file.stream.read()) 
                #trying to get it to load the data into a python dictionary
                if os.path.isfile(filename):
                    reader = csv.DictReader(open(filename, 'rU'), dialect=csv.excel_tab)

                    result = {}
                    for row in reader:
                        for column, value in row.iteritems():
                            result.setdefault(column, []).append(value)
                    print("HEYYYYYYY____________", result)
                    #we need to put it into the database here once the results are checked for errors
                    user_name = ""
                    last_name = ""
                    first_name = ""
                    sport = ""
                    year = ""
                    email = ""
                    one_rep_max = ""
                    
                    query = "INSERT INTO students (user_name, first_name, last_name, sport, year, email, one_rep_max) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    values = (user_name, first_name, last_name, sport, year, email, one_rep_max)
                    print query
                    try:
                        cur.execute(query, values)
                    except:
                        print("Problem inserting into students")
                        db.rollback()
                    db.commit()
                    
                    # We may just want to go with strictly '.csv' files. The below prints crazyness when csvTest.xlsx is uploaded, but it handles '.csv' files nicely -michael
                    print ("This is what is read from the file: ", fileContents)
                else:
                    print("This file could not be parsed. Please try another file or a differnt format.")
            else:
                #print out to user there was an error
                print("This file could not be parsed. Please try another file or a differnt format.")
        else:
            print('browse_file wasnt in request.files')
        
        #when user hits submit button
        if 'submit_file' in request.form: 
            print("You hit the file submit button!")
        else:
            print('something else happened')
            
    ####################################################################################
    ##This (below) can also be turned into a function. I think it's on like every page. 
    ####################################################################################
    names = None
    if userType == 'admin':
        # getting the user's first and last name(only admins)
        cur.execute("SELECT first_name, last_name FROM admin WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
        
        
    #user and userType are being passed to the website here
    return render_template('Theme/aAddUser.html', user = verifiedUser, userType = userType, Name = names, results = rows, types = types)
#end admin add user page--------------------------------------------------  


#Account Created Email----------------------------------------------------

#read in from csv has been priority bumped, and the email being sent out will happen after that has been imported correctly 


#End Account Created Email------------------------------------------------




#**********************************
#*************STUDENT**************
#**********************************

#student home---------------------------------------------------------------------------------------------------
@app.route('/shome', methods=['GET', 'POST'])
def studentHome():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "SELECT * FROM users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('studentHome'))
        else:
            verifiedUser = ''
            session['username'] = ''
            
    names = None
    if userType == 'student':
        # getting the user's first and last name(only students)
        cur.execute("SELECT first_name, last_name FROM students WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason
        names=cur.fetchall()
        print(names)
    
    #user and userType are being passed to the website here
    return render_template('Theme/shome.html', user = verifiedUser, userType = userType, Name = names)
#end studentHome------------------------------------------------------------------------------------------------------------------------    
    
#student calendar page---------------------------------------------------------------------------------------------------
@app.route('/scalendar', methods=['GET', 'POST'])
def studentCalendarPage():
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    if 'userType' in session:
        userType = session['userType']
    else:
        userType = ''
    if verifiedUser == '':
        return redirect(url_for('login'))
    if userType == '':
        return redirect(url_for('login'))
    if 'username' in session:
        verifiedUser = session['username']
    else:
        verifiedUser = ''
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    if request.method == 'POST':
        print "HI"
        session['username'] = request.form['username']
        print(session['username'])

        pw = request.form['pw']
        query = "SELECT * FROM users WHERE username = '%s' AND password = crypt('%s', password)" % (session['username'], pw)
        print query
        cur.execute("SELECT * FROM users WHERE username = %s AND password = crypt(%s, password)", (session['username'], pw))
        if cur.fetchone():
            verifiedUser = session['username']
            return redirect(url_for('studentHome'))
        else:
            verifiedUser = ''
            session['username'] = ''
            
    names = None
    if userType == 'student':
        # getting the user's first and last name(only students)
        cur.execute("SELECT first_name, last_name FROM students WHERE user_name = %s", (verifiedUser,)) #<- make sure if there is only one variable, it still needs a comma for some reason (I think it's because it's a tuple?)
        names=cur.fetchall()
        print(names)
    
    #user and userType are being passed to the website here
    return render_template('Theme/scalendar.html', user = verifiedUser, userType = userType, Name = names)
#end studentCalendarPage------------------------------------------------------------    
    
    
    
    
    
    
    
    
    
#keep this at the bottom. We think it starts the server    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug = True)