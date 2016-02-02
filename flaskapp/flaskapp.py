#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, redirect, render_template
import pygal
from datetime import date
from pygal.style import DefaultStyle
import wikipedia
import subprocess

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

    wikipedia.set_lang("fr")
    tic=2002
    tac=2013
    
    name1='Firefox'
    sumup1=wikipedia.summary(name1, sentences=2)
    rank1='1'
    view1='10001'
    line_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=DefaultStyle)
    line_chart.add(name1, [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    trend1 = graph_data = line_chart.render_data_uri()

    # cmd = ["ls","-l"]
    # p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
    #                         stderr=subprocess.PIPE,
    #                         stdin=subprocess.PIPE)
    # out,err = p.communicate()
    # out = out.decode('utf-8')

    return render_template('form_action_day.html', name1=name1,sumup1=sumup1,view1=view1,rank1=rank1,trend1=trend1)


if __name__ == '__main__':
    app.run(debug=True)
