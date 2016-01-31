from flask import Flask, request, redirect
import pygal
from pygal.style import DefaultStyle

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Go to /home.html to submit date, it will automatically redirect to /graph.html'

@app.route('/home.html', methods = ['POST'])
def signup():
    date = request.form['date']
    print("The date is '" + date + "'")
    return redirect('/graph.html')

@app.route('/graph.html')
def graphe():
    
    #exemple de graphe en attendant les data
    graph = pygal.StackedLine(fill=True, interpolate='cubic', style=NeonStyle)
    graph.title = '% Change Coolness of programming languages over time.'
    graph.x_labels = ['2011','2012','2013','2014','2015','2016']
    graph.add('Python',  [15, 31, 89, 200, 356, 900])
    graph.add('Java',    [15, 45, 76, 80,  91,  95])
    graph.add('C++',     [5,  51, 54, 102, 150, 201])
    graph.add('All others combined!',  [5, 15, 21, 55, 92, 105])
    graph_data = graph.render_data_uri()
    
    return render_template("graph.html", graph_data = graph_data)

if __name__ == '__main__':
    app.run()