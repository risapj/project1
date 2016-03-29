#!/usr/bin/env python2.7

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import jinja2

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://trw2121:JVTTMM@w4111db.eastus.cloudapp.azure.com/trw2121"

#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def mainpage():
  return render_template("mainpage.html")

@app.route('/danishgirl')
def danishgirl():
  #dg = g.conn.execute("SELECT * FROM Movie M, Acts_in A, Directs D, Writes W, Nominated_p Np, Nominated_m Nm WHERE M.mid = 3")
  #dg = g.conn.execute("SELECT * FROM Movie M, Acts_in A WHERE M.mid = 3")

#below does no work, middle dg does. 
  dg = g.conn.execute("SELECT * FROM Person P WHERE P.pid IN (SELECT * FROM Acts_in  Movie M3))")
  dginfo = dg.fetchall()
  
  return render_template("danishgirl.html", data = dginfo)


@app.route('/movie-search')
@app.route('/movie-search<search>')
def moviesearch(search=None):
#get all info from Movie
  forTable = g.conn.execute("SELECT * FROM Movie")
  minfo = forTable.fetchall()

#get info from Movie, create array, put titles in array 
  ddmenu = g.conn.execute("SELECT * FROM Movie")
  movies = []
  for result in ddmenu:
    movies.append(result['title'].encode('utf-8'))

  results = g.conn;
  title = request.args.get('title')
  if title == "All":
    title = None
  else:
    results.execute("SELECT DISTINCT M.title, M.length, M.language, M.release_date, M.genre FROM Movie M")
  
  return render_template("movie-search.html", data = movies, data2 = minfo, title = title, resutls = results)

'''
@app.route('/movie-search/<search>')
def search(search=None):
  movies = g.conn.cursor()
  movies.execute("SELECT DISTINCT title FROM Movie;")
  movies = movies.fetchall();

  if title == "All":
    title = None

  title = request.args.get('Movie')
  movieinfo = g.conn.cursor()
  director = g.conn.cursor()
  writer = g.conn.cursor()
  actchar = g.conn.cursor()
  award = g.conn.cursor()

  if title == "All":
    title = None

  if title:
    movieinfo.execute("SELECT DISTINCT M.mid, M.title, M.length, M.language, M.release_date, M.production_co, M.genre FROM Movie M WHERE M.title =\'" + title + "\'")
    director.execute("SELECT DISTINCT P.name FROM Movie M, Directs D, Person P WHERE M.title =\'" + title + "\' AND M.mid = D.mid AND D.pid = P.pid")
    writer.execute("SELECT DISTINCT P.name FROM Movie M, Writes W, Person P WHERE M.title =\'" + title + "\' AND M.mid = W.mid AND W.pid = P.pid")
    actchar.execute("SELECT DISTINCT P.name, A.char_name FROM Person P, Acts_in A, Movie M WHERE M.title =\'" + title + "\' AND M.mid = A.mid AND A.pid = P.pid")
    award.execute("SELECT A.aid, A.year, A.type, A.category FROM Awards A, Nominated_p Np, Nominated_m Nm, Movie M WHERE M.title =\'")

  final_results = []
  for result in results:
    current_movie = {}
    #movieinfo =  
'''


#  return render_template("movie-search.html", **context)



@app.route('/person-search')
def personsearch():
#get all info from Movie
  forTable = g.conn.execute("SELECT * FROM Person")
  pinfo = forTable.fetchall()

#get info from Movie, create array, put titles in array 
  ddmenu = g.conn.execute("SELECT * FROM Person")
  people = []
  for result in ddmenu:
    people.append(result['name'].encode('utf-8'))

  return render_template("person-search.html", data = people, data2 = pinfo)


@app.route('/award-search')
def awardsearch():
  return render_template("award-search.html")

@app.route('/character-search')
def charactersearch():
  return render_template("character-search.html")

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
