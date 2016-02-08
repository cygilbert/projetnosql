#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, redirect, render_template
import pygal
from datetime import date
from pygal.style import DefaultStyle
import wikipedia
import subprocess
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('accueil.html')

@app.route('/home')
def home():
	return render_template('accueil.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/request_period')
def form_submit_period():
	return render_template('form_submit_period.html')

@app.route('/request_day')
def form_submit_day():
    return render_template('form_submit_day.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/graph_period/', methods=['POST'])
def form_action_period():
    date_from=request.form['date_from']
    date_to=request.form['date_from']

    graph = pygal.StackedLine(fill=True)
    graph.title = '% Change Coolness of programming languages over time.'
    graph.x_labels = ['2011','2012','2013','2014','2015','2016']
    graph.add('Python',  [15, 31, 89, 200, 356, 900])
    graph.add('Java',    [15, 45, 76, 80,  91,  95])
    graph.add('C++',     [5,  51, 54, 102, 150, 201])
    graph.add('All others combined!',  [5, 15, 21, 55, 92, 105])
    graph_data = graph.render_data_uri()


    return render_template('form_action_period.html', graph_data = graph_data)

@app.route('/graph_day/', methods=['POST'])
def form_action_day():

    date = request.form['day']
    period = int(request.form['period'])

    date_split = date.split('/')

    day = int(date_split[0] - 1 )
    month = int(date_split[1])

    if month == 2:
        day += 31
    elif month == 3:
        day = day + 31 + 28

    date_from = 0
    # type = 1 => periode 30 jours
    if period == 1:
        date_from = day - 30
        cmd = ["dse", "spark-submit", "/home/ubuntu/batch_test.py", "0", "0"]
    elif period == 0:
        cmd = ["dse", "spark-submit", "/home/ubuntu/batch_test.py", "0"]

    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')

    # filePath = '/ubuntu/home/projetnosql/'
    # fileName = 'day_' + str(day) + '_24htrending.csv'
    
    # df = pd.read_csv(filePath+fileName, sep=", ", engine="python", header=None)
    # element 0 => row=df.ix[0,:]
    out_split = out.split("parent))")
    rows = out_split[1]

    row = rows.split()
    lolo = row[8]

    rows = len(row)


    # Graph code
    wikipedia.set_lang("en")
    tic=2002
    tac=2013

    name='Firefox'    
    name1=row[1]
    sumup1=wikipedia.summary(name, sentences=2)
    view1=row[2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name1, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend1 = line_chart.render_data_uri()
    
    name2=row[4]
    sumup2=wikipedia.summary(name, sentences=2)
    view2=row[5]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name2, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend2 = line_chart.render_data_uri()
    
    name3=row[7]
    sumup3=wikipedia.summary(name, sentences=2)
    view3=row[8]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name3, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend3 = graph_data = line_chart.render_data_uri()
    
    name4=row[10]
    sumup4=wikipedia.summary(name, sentences=2)
    view4=row[11]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name4, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend4 = line_chart.render_data_uri()
    
    name5=row[13]
    sumup5=wikipedia.summary(name, sentences=2)
    view5=row[14]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name5, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend5 = line_chart.render_data_uri()
    
    name6=row[16]
    sumup6=wikipedia.summary(name, sentences=2)
    view6=row[17]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name6, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend6 = line_chart.render_data_uri()
    
    name7=row[19]
    sumup7=wikipedia.summary(name, sentences=2)
    view7=row[20]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name7, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend7 = line_chart.render_data_uri()
    
    name8=row[22]
    sumup8=wikipedia.summary(name, sentences=2)
    view8=row[23]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name8, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend8 = line_chart.render_data_uri()
    
    name9=row[25]
    sumup9=wikipedia.summary(name, sentences=2)
    view9=row[26]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name9, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend9 = line_chart.render_data_uri()
    
    name10=row[28]
    sumup10=wikipedia.summary(name, sentences=2)
    view10=row[29]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name10, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend10 = line_chart.render_data_uri()
    
    return render_template("form_action_day.html",name1=name1,sumup1=sumup1,view1=view1,trend1=trend1,
        name2=name2,sumup2=sumup2,view2=view2,trend2=trend2,
        name3=name3,sumup3=sumup3,view3=view3,trend3=trend3,
        name4=name4,sumup4=sumup4,view4=view4,trend4=trend4,
        name5=name5,sumup5=sumup5,view5=view5,trend5=trend5,
        name6=name6,sumup6=sumup6,view6=view6,trend6=trend6,
        name7=name7,sumup7=sumup7,view7=view7,trend7=trend7,
        name8=name8,sumup8=sumup8,view8=view8,trend8=trend8,
        name9=name9,sumup9=sumup9,view9=view9,trend9=trend9,
        name10=name10,sumup10=sumup10,view10=view10,trend10=trend10,
        out=rows, err=lolo)


if __name__ == '__main__':
    app.run(debug=True)
