#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, redirect, render_template
import pygal
from datetime import date
from pygal.style import DefaultStyle
import wikipedia
import subprocess
import pandas as pd
from urllib2 import unquote

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

    day = int(date_split[0]) - 1
    month = int(date_split[1])

    if month == 2:
        day += 31
    elif month == 3:
        day = day + 31 + 28

    date_from = 0
    # type = 1 => periode 30 jours
    if period == 1:
        date_from = day - 30

    filePath = '/home/ubuntu/projetnosql/day_'+str(day)+'_24htrending.csv'

    df = pd.read_csv(filePath, sep=",", engine="python")
    


    wikipedia.set_lang("en")
    
    name1=df.ix[0,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name1)
    name1=unq.decode('utf-8')
    
    if wikipedia.search(name1) :
        sumup1 = wikipedia.summary(name1, sentences= 2)
    else:
        sumup1 = "no sum up"
    view1=df.ix[0,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name1, (df.ix[0,:][4:28]).values)
    trend1 = line_chart.render_data_uri()
    
    name2=df.ix[1,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name2)
    name2=unq.decode('utf-8')
    if wikipedia.search(name2) :
        sumup2 = wikipedia.summary(name2, sentences= 2)
    else:
        sumup2 = "no sum up"
    view2=df.ix[1,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name2, (df.ix[1,:][4:28]).values)
    trend2 = line_chart.render_data_uri()
    
    name3=df.ix[2,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name3)
    name3=unq.decode('utf-8')

    if wikipedia.search(name3) :
        sumup3 = wikipedia.summary(name3, sentences= 2)
    else:
        sumup3 = "no sum up"
    view3=df.ix[2,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name3, (df.ix[2,:][4:28]).values)
    trend3 = graph_data = line_chart.render_data_uri()
    
    name4=df.ix[3,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name4)
    name4=unq.decode('utf-8')

    if wikipedia.search(name4) :
        sumup4 = wikipedia.summary(name4, sentences= 2)
    else:
        sumup4 = "no sum up"
    view4=df.ix[3,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name4, (df.ix[3,:][4:28]).values)
    trend4 = line_chart.render_data_uri()
    
    name5=df.ix[4,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name5)
    name5=unq.decode('utf-8')

    if wikipedia.search(name5) :
        sumup5 = wikipedia.summary(name5, sentences= 2)
    else:
        sumup5 = "no sum up"
    view5=df.ix[4,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name5, (df.ix[4,:][4:28]).values)
    trend5 = line_chart.render_data_uri()
    
    name6=df.ix[5,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name6)
    name6=unq.decode('utf-8')

    if wikipedia.search(name6) :
        sumup6 = wikipedia.summary(name6, sentences= 2)
    else:
        sumup6 = "no sum up"
    view6=df.ix[5,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name6, (df.ix[5,:][4:28]).values)
    trend6 = line_chart.render_data_uri()
    
    name7=df.ix[6,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name7)
    name7=unq.decode('utf-8')

    if wikipedia.search(name7) :
        sumup7 = wikipedia.summary(name7, sentences= 2)
    else:
        sumup7 = "no sum up"
    view7=df.ix[6,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name7, (df.ix[6,:][4:28]).values)
    trend7 = line_chart.render_data_uri()

    
    name8=df.ix[7,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name8)
    name8=unq.decode('utf-8')

    if wikipedia.search(name8) :
        sumup8 = wikipedia.summary(name8, sentences= 2)
    else:
        sumup8 = "no sum up"
    view8=df.ix[7,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name8, (df.ix[7,:][4:28]).values)
    trend8 = line_chart.render_data_uri()
    
    name9=df.ix[8,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name9)
    name9=unq.decode('utf-8')

    if wikipedia.search(name9) :
        sumup9 = wikipedia.summary(name9, sentences= 2)
    else:
        sumup9 = "no sum up"
    view9=df.ix[8,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name9, (df.ix[8,:][4:28]).values)
    trend9 = line_chart.render_data_uri()
    
    name10=df.ix[9,:][1].replace('_',' ').encode('latin1')
    unq = unquote(name10)
    name10=unq.decode('utf-8')

    if wikipedia.search(name10) :
        sumup10 = wikipedia.summary(name10, sentences= 2)
    else:
        sumup10 = "no sum up"
    view10=df.ix[9,:][2]
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name10, (df.ix[9,:][4:28]).values)
    trend10 = line_chart.render_data_uri()
    
    name1=name1+' ('+df.ix[0,:][0]+')'
    name2=name2+' ('+df.ix[1,:][0]+')'
    name3=name3+' ('+df.ix[2,:][0]+')'
    name4=name4+' ('+df.ix[3,:][0]+')'
    name5=name5+' ('+df.ix[4,:][0]+')'
    name6=name6+' ('+df.ix[5,:][0]+')'
    name7=name7+' ('+df.ix[6,:][0]+')'
    name8=name8+' ('+df.ix[7,:][0]+')'
    name9=name9+' ('+df.ix[8,:][0]+')'
    name10=name10+' ('+df.ix[9,:][0]+')'    
#    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=NeonStyle)
#    line_chart.title = 'Browser usage evolution (in %)'
#    line_chart.x_labels = map(str, range(2002, 2013))
#    line_chart.add(df['page'], [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
#    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
#    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
#    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
#    graph_data = line_chart.render_data_uri()
    
    
#    sumup = wikipedia.summary("Facebook", sentences=2)
    return render_template("form_action_day.html",name1=name1,sumup1=sumup1,view1=view1,trend1=trend1,name2=name2,sumup2=sumup2,view2=view2,trend2=trend2,name3=name3,sumup3=sumup3,view3=view3,trend3=trend3,name4=name4,sumup4=sumup4,view4=view4,trend4=trend4,name5=name5,sumup5=sumup5,view5=view5,trend5=trend5,name6=name6,sumup6=sumup6,view6=view6,trend6=trend6,name7=name7,sumup7=sumup7,view7=view7,trend7=trend7,name8=name8,sumup8=sumup8,view8=view8,trend8=trend8,name9=name9,sumup9=sumup9,view9=view9,trend9=trend9,name10=name10,sumup10=sumup10,view10=view10,trend10=trend10)


    #out =df.shape 
    #err = filePath
   
    #return render_template("form_action_day.html", out=out,err=err)

    

    # return render_template('form_action_day.html', name1=name1,sumup1=sumup1,view1=view1,rank1=rank1,trend1=trend1,
    #     out=day,err=date_from)


if __name__ == '__main__':
    app.run(debug=True)
