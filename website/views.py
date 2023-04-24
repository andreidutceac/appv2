import datetime
import json
from datetime import timedelta

import plotly.express as px
from flask import Blueprint, render_template, request, flash, jsonify
from flask import Markup
from flask_login import login_required, current_user
from plotly.graph_objs import Scatter
from plotly.offline import plot
import plotly.graph_objs as go

from . import db
from .models import Note, Kilometers, Reading

# from .news import get_news



views = Blueprint('views', __name__)


# day_articles = get_news()
# date1 = day_articles[0]["date"]
# title1 = day_articles[0]["title"]
# link1 = day_articles[0]["link"]
# date2 = day_articles[1]["date"]
# title2 = day_articles[1]["title"]
# link2 = day_articles[1]["link"]
# date3 = day_articles[2]["date"]
# title3 = day_articles[2]["title"]
# link3 = day_articles[2]["link"]
# date4 = day_articles[3]["date"]
# title4 = day_articles[3]["title"]
# link4 = day_articles[3]["link"]
# date5 = day_articles[4]["date"]
# title5 = day_articles[4]["title"]
# link5 = day_articles[4]["link"]


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    today = datetime.date.today()

    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            if Note.query.filter_by(date=f"{today}").first() and Note.query.filter_by(user_id=f"{current_user.id}").first():
                flash('One note per day!:)', category='error')
            else:
                new_note = Note(data=note, date=f"{today}", user_id=current_user.id)  # providing the schema for the note
                db.session.add(new_note)  # adding the note to the database
                db.session.commit()
                flash('Note added!', category='success')
    return render_template("notes.html", user=current_user)


@views.route('/athletics', methods=['POST', 'GET'])
@login_required
def athletics():
    today = datetime.date.today()
    today_run = ""
    total_run = 0
    average = 0

    trainings = []
    dates = []
    runs = []


    runs = Kilometers.query.filter_by(user_id=f"{current_user.id}").all()

    for run in runs:
        trainings.append((run.km))
        dates.append((run.date))

    # sort values by dates
    n = len(dates)
    for i in range(n):
        for j in range(n - 1):
            if dates[j] > dates[j + 1]:
                val = dates[j]
                dates[j] = dates[j + 1]
                dates[j + 1] = val

                val2 = trainings[j]
                trainings[j] = trainings[j + 1]
                trainings[j + 1] = val2



    while str(today) > str(dates[n-1]):
        today = today + timedelta(days=-1)
        if str(today) == str(dates[n-1]):
            break
        dates.append(str(today))
        trainings.append(0)
        ok = 0

        if Kilometers.query.filter_by(date=f"{today}").all():
            runs = Kilometers.query.filter_by(date=f"{today}").all()
            for run in runs:
                if run.user_id == current_user.id:
                    ok = 1
            if ok == 0:
                save = Kilometers(km=0, date=f"{today}", user_id=current_user.id)
                db.session.add(save)  # adding the note to the database
                db.session.commit()



    print(trainings)

    # plot trainings
    my_plot_div = plot([Scatter(x=dates, y=trainings)], output_type='div')

    # plot week's average
    weeks = []
    total_week = []
    for i in range(int(len(trainings)/7)):
        weeks.append(i+1)
        sum= 0
        for j in range(7):
            sum = sum + trainings[(7*i) + (1*j)]
        total_week.append(sum)


    print(total_week)
    data = [go.Bar(x=weeks, y=total_week)]

    my_week_average = plot( data, output_type='div')


    # calculate the average
    length = 0
    for run in runs:
        if run.km != 0:
            total_run = total_run + run.km
            length = length + 1

    if length != 0:
        average = (total_run / length)

    # set km=0 automatically each day in case there is no running
    today = datetime.date.today()
    ok=0
    runs = Kilometers.query.filter_by(date=f"{today}").all()
    for run in runs:
        if run.user_id == current_user.id:
            ok = 1
            print("user")
    if ok == 0:
        save = Kilometers(km=0, date=f"{today}", user_id=current_user.id)
        db.session.add(save)  # adding the note to the database
        db.session.commit()




    # if press the submit button
    if request.method == 'POST':
        today = datetime.date.today()
        run_distance = request.form.get('run')
        #print(run_distance)
        id_item = current_user.id

        if len(run_distance) < 0:
            flash('Not valid!', category='error')
        else:
            if Kilometers.query.filter_by(date=f"{today}") and Kilometers.query.filter_by(user_id=f"{current_user.id}").first():


                runs = Kilometers.query.filter_by(date=f"{today}").all()
                for run in runs:
                    print(str(today))
                    if run.user_id == current_user.id:
                        print(run_distance)
                        run.km = run_distance
                        db.session.commit()
                print("exista")
            else:
                save = Kilometers(km=run_distance, date=f"{today}", user_id=id_item)
                db.session.add(save)  # adding the note to the database
                db.session.commit()
                flash('Save added!', category='success')


        today_run = run_distance




    return render_template("athletics.html", user=current_user, run=today_run, average=round(average,2),
                           total_run=round(total_run,2), div_placeholder=Markup(my_plot_div), graph_bar=Markup(my_week_average))
    # , date1=date1, title1=title1,
    #                        link1=link1, date2=date2, title2=title2, link2=link2, date3=date3, title3=title3, link3=link3,
    #                        date4=date4, title4=title4, link4=link4, date5=date5, title5=title5, link5=link5)


@views.route('/reading', methods=['POST', 'GET'])
@login_required
def reading():
    today = datetime.date.today()
    today_read = ""
    total_read = 0
    average = 0

    pages = []
    dates = []

    reads = Reading.query.filter_by(user_id=f"{current_user.id}").all()

    for read in reads:
        pages.append(int(read.pages))
        dates.append((read.date))

    # sort values by dates
    n = len(pages)
    for i in range(n):
        for j in range(n-1):
            if dates[j] > dates[j+1]:
                val = dates[j]
                dates[j] = dates[j+1]
                dates[j+1] = val

                val2 = pages[j]
                pages[j] = pages[j + 1]
                pages[j + 1] = val2

    print(dates)
    print(pages)

    while str(today) > str(dates[n-1]):
        today = today + timedelta(days=-1)
        if str(today) == str(dates[n-1]):
            break
        dates.append(str(today))
        pages.append(0)
        ok = 0

        if Reading.query.filter_by(date=f"{today}").all():
            reads = Reading.query.filter_by(date=f"{today}").all()
            for read in reads:
                if read.user_id == current_user.id:
                    ok = 1
            if ok == 0:
                save = Reading(pages=0, date=f"{today}", user_id=current_user.id)
                db.session.add(save)  # adding the note to the database
                db.session.commit()

    my_plot_div = plot([Scatter(x=dates, y=pages)], output_type='div')

    reads = Reading.query.filter_by(user_id=f"{current_user.id}").all()

    weeks = []
    total_week = []
    for i in range(int(len(pages) / 7)):
        weeks.append(i + 1)
        sum = 0
        for j in range(7):
            sum = sum + pages[(7 * i) + (1 * j)]
        total_week.append(sum)

    print(total_week)
    data = [go.Bar(x=weeks, y=total_week)]

    my_week_average = plot(data, output_type='div')

    # calculate the average
    length = 0
    for read in reads:
        if read.pages != 0:
            total_read = total_read + read.pages
            length = length + 1

    if length != 0:
        average = (total_read / length)

    # set pages = 0 automatically each day in case there is no reading
    today = datetime.date.today()
    ok = 0
    reads = Reading.query.filter_by(date=f"{today}").all()
    for read in reads:
        if read.user_id == current_user.id:
            ok = 1
            print("user")
    if ok == 0:
        save = Reading(pages=0, date=f"{today}", user_id=current_user.id)
        db.session.add(save)  # adding the note to the database
        db.session.commit()

    # if press the submit button
    if request.method == 'POST':
        read_pages = request.form.get('read')
        print(current_user.id)
        id_item = current_user.id
        today = datetime.date.today()


        if len(read_pages) < 0:
            flash('Not valid!', category='error')
        else:
            if Reading.query.filter_by(date=f"{today}") and Reading.query.filter_by(user_id=f"{current_user.id}").first():
                reads = Reading.query.filter_by(date=f"{today}").all()
                for read in reads:
                    print(read.user_id)
                    if read.user_id == current_user.id:
                        read.pages = read_pages
                        db.session.commit()
                print("exista")


            else:
                save = Reading(pages=read_pages, date=f"{today}", user_id=id_item)
                db.session.add(save)  # adding the note to the database
                db.session.commit()
                flash('Save added!', category='success')


        today_read = read_pages

    return render_template("reading.html", user=current_user, today_read=today_read, average=round(average, 1),
                           total_read=total_read, div_placeholder=Markup(my_plot_div), graph_bar=Markup(my_week_average))



@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
