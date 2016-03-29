#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import jinja2


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
DATABASEURI = "postgresql://trw2121:JVTTMM@w4111db.eastus.cloudapp.azure.com/trw2121"

#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
# END SQLITE SETUP CODE
#



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


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def mainpage():
  ddmenu = g.conn.execute("SELECT * FROM Movie")
  movies = []
  for result in ddmenu:
    movies.append(result['title'].encode('utf-8'))
  
#  context = dict(data = titles)
 
  return render_template("mainpage.html", data = movies)
#def index():
#  """
#  request is a special object that Flask provides to access web request information:

#  request.method:   "GET" or "POST"
#  request.form:     if the browser submitted a form, this contains the data in the form
#  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

#  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
#  """

  # DEBUG: this is debugging code to see what request looks like
#  print request.args


  #
  # example of a database query
  #

  

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
#  context = dict(data = titles)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
#  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#

@app.route('/danishgirl')
def danishgirl():
  #dg = g.conn.execute("SELECT * FROM Movie M, Acts_in A, Directs D, Writes W, Nominated_p Np, Nominated_m Nm WHERE M.mid = 3")
  #dg = g.conn.execute("SELECT * FROM Movie M, Acts_in A WHERE M.mid = 3")

#below does no work, middle dg does. 
  dg = g.conn.execute("SELECT * FROM Person P WHERE P.pid IN (SELECT * FROM Acts_in  Movie M3))")
  dginfo = dg.fetchall()
  
  return render_template("danishgirl.html", data = dginfo)




@app.route('/movie-search')
def moviesearch():
  
#get everything from Movie table
  movies = g.conn.execute("SELECT * FROM Movie;")
  titles = movies.fetchall()

  context = dict(data = titles)

  return render_template("movie-search.html", data = titles)

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
  return render_template("person-search.html")


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
