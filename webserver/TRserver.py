#/usr/bin/env python2.7

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


#@app.route('/movie-search', methods=['GET', 'POST'])
#@app.route('/movie-search<search>', methods=['GET', 'POST'])
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

  title = request.args.get('title')

  if title == "All":
    title = None
    

  if title:  
    results = g.conn.execute("SELECT * FROM Movie M WHERE M.title = \'"+title +"\'")
#    people = g.conn.execute("SELECT P.name, A.char_name FROM Movie M, Person P, Acts_in A WHERE M.title = \'"+title+"\' AND M.mid = A.mid AND A.pid=P.pid")
#    director = g.conn.execute("SELECT P.name FROM Movie M, Person P, Directs D WHERE M.title = \'"+title+"\' AND M.mid = D.mid AND D.pid = P.pid")
#    writer = g.conn.execute("SELECT P.name FROM Movie M, Person P, Writes W WHERE M.title = \'"+title+"\' AND M.mid = W.mid AND W.pid = P.pid")
#    awards = g.conn.execute("SELECT A.year, A.type, A.category, P.name, N.won FROM Awards A, Nominated_p N, Person P, Movie M WHERE M.title = \'"+title+"\' AND M.mid=N.mid AND N.pid=P.pid AND N.aid=A.aid")
#    awardm = g.conn.execute("SELECT A.year, A.type, A.category, N.won FROM Awards A, Nominated_m N, Movie M WHERE M.title = \'"+title+"\' AND M.mid=N.mid AND N.aid=A.aid")
#    review = g.conn.execute("SELECT R.username, R.text, R.post_time FROM Review_posted R, Movie M WHERE M.title = \'"+title+"\' AND R.mid = M.mid")
#    user = g.conn.execute("SELECT * FROM Users")
#    rating = g.conn.execute("SELECT R.username, R.rating, R.post_time FROM Rating_rated R, Movie M WHERE M.title = \'"+title+"\' AND M.mid = R.mid")
  else:
    results = g.conn.execute("SELECT * FROM Movie M")
#    people = g.conn.execute("SELECT P.name FROM Person P WHERE P.pid = 100")
#    director = g.conn.execute("SELECT P.name FROM Person P WHERE P.pid = 100")
#    writer = g.conn.execute("SELECT P.name FROM Person P WHERE P.pid = 100")
#    awards = g.conn.execute("SELECT P.name FROM Person P WHERE P.pid = 100")
#    awardm = g.conn.execute("SELECT P.name FROM Person P WHERE P.pid = 100")
#    review = g.conn.execute("SELECT P.name FROM Person P WHERE P.pid = 100")
#    user = g.conn.execute("SELECT P.name FROM Person P WHERE P.pid = 100")
#    rating = g.conn.execute("SELECT P.name FROM Person P WHERE P.pid = 100")

  people = g.conn.execute("SELECT P.pid, P.name, A.char_name, A.mid FROM Person P, Acts_in A WHERE A.pid=P.pid")
  director = g.conn.execute("SELECT P.name, D.pid, D.mid FROM Person P, Directs D WHERE D.pid = P.pid")
  writer = g.conn.execute("SELECT P.name, W.pid, W.mid FROM Person P, Writes W WHERE W.pid = P.pid")
  awards = g.conn.execute("SELECT A.year, A.type, A.category, N.won, P.name, N.mid FROM Awards A, Nominated_p N, Person p WHERE N.pid=P.pid AND N.aid=A.aid")
  awardm = g.conn.execute("SELECT A.year, A.type, A.category, N.won, N.mid FROM Awards A, Nominated_m N WHERE N.aid=A.aid")
  review = g.conn.execute("SELECT R.username, R.rev_text, R.post_date, R.mid FROM Review_posted R")
  rating = g.conn.execute("SELECT R.username, R.rating, R.post_date, R.mid FROM Rating_rated R")
  user = g.conn.execute("SELECT U.username FROM Users U") 

 # rinfo = results.fetchall()
  final_results = []
  for result in results:
    current_movie = {}
    current_movie["info"] = [result[1], result[2], result[3], result[4], result[5], result[6]]
    movie_id = str(result[0])
    people_array = []
    for p in people:
      if movie_id == str(p[3]):
        people_array.append([p[1].encode('utf-8'), p[2].encode('utf-8')])
    current_movie["actors"] = people_array
    director_array = []
    for d in director:
      if movie_id == str(d[2]):
        director_array.append([d[0].encode('utf-8')])
    current_movie["director"] = director_array
    writer_array = [] 
    for w in writer:
      if movie_id == str(w[2]):
        writer_array.append([w[0].encode('utf-8')])
    current_movie["writer"] = writer_array
    awardp_array = []
    for ap in awards:
      if movie_id == str(ap[5]):
        won = str(ap[3])
        won2 = "t"
        if won == won2:
          win = 'Won'
        else:
          win = 'Nominated'
        awardp_array.append([ap[0], ap[1].encode('utf-8'), ap[2].encode('utf-8'), ap[4].encode('utf-8'), win])
    current_movie["awardp"] = awardp_array
    awardm_array = []
    for am in awardm:
      if movie_id == str(am[4]):
        won = str(ap[3])
        won2 = "t"
        if won == won2:
          win = 'Won'
        else:
          win = 'Nominated'
        awardm_array.append([am[0], am[1].encode('utf-8'), am[2].encode('utf-8'), win])
    current_movie["awardm"] = awardm_array
    review_array = []
    for rev in review:
      if movie_id == str(rev[3]):
        for u in user: 
          if str(u[0]) == str(rev[0]):
            review_array.append([u[0].encode('utf-8'), rev[1].encode('utf-8'), rev[2]])
    current_movie["reviews"] = review_array
    rating_array = []
    for rat in rating:
      if movie_id == str(rat[3]):
        for u in user:
          if str(u[0]) == str(rat[0]):
            rating_array.append([u[0].encode('utf-8'), rat[1], rat[2]])
    current_movie["ratings"] = rating_array
    final_results.append(current_movie)

  return render_template('movie-search.html', data = movies, data2 = minfo, title = title, results = final_results)
  #return render_template("movie-search.html", data = movies, data2 = minfo, title = title)

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
