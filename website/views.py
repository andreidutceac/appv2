from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, Kilometers, Reading
from . import db
import json
import datetime
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup

views = Blueprint('views', __name__)


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
        print(run.km)

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

    my_plot_div = plot([Scatter(x=dates, y=trainings)], output_type='div')

    # calculate the average
    length = 0
    for run in runs:
        if run.km != 0:
            total_run = total_run + run.km
            length = length + 1

    if length != 0:
        average = (total_run / length)

    # set km=0 automatically each day in case there is no running
    if Kilometers.query.filter_by(date=f"{today}").first() and Kilometers.query.filter_by(
            user_id=f"{current_user.id}").first():
        pass
    else:
        save = Kilometers(km=0, date=f"{today}", user_id=current_user.id)
        db.session.add(save)  # adding the note to the database
        db.session.commit()

    # if press the submit button
    if request.method == 'POST':
        run_distance = request.form.get('run')
        print(current_user.id)
        id_item = current_user.id

        if len(run_distance) < 0:
            flash('Not valid!', category='error')
        else:
            if Kilometers.query.filter_by(date=f"{today}") and Kilometers.query.filter_by(user_id=f"{current_user.id}").first():

                runs = Kilometers.query.filter_by(date=f"{today}").all()
                for run in runs:
                    print(run.user_id)
                    if run.user_id == current_user.id:
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
                           total_run=total_run, div_placeholder=Markup(my_plot_div))


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

    my_plot_div = plot([Scatter(x=dates, y=pages)], output_type='div')

    reads = Reading.query.filter_by(user_id=f"{current_user.id}").all()

    # calculate the average
    length = 0
    for read in reads:
        if read.pages != 0:
            total_read = total_read + read.pages
            length = length + 1

    if length != 0:
        average = (total_read / length)

    # set pages = 0 automatically each day in case there is no reading
    if Reading.query.filter_by(date=f"{today}").first() and Reading.query.filter_by(
            user_id=f"{current_user.id}").first():
        pass
    else:
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
                           total_read=total_read, div_placeholder=Markup(my_plot_div))



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
