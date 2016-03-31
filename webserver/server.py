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
  else:
    results = g.conn.execute("SELECT * FROM Movie M")

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

  return render_template('movie-search.html', data = movies, data2 = minfo, chosen_title = title, title = title, results = final_results)


@app.route('/person-search')
@app.route('/person-search<search>')
def personsearch(search=None):
#get all info from Person
  forTable = g.conn.execute("SELECT * FROM Person")
  pinfo = forTable.fetchall()

#get info from Movie, create array, put titles in array 
  ddmenu = g.conn.execute("SELECT * FROM Person")
  people = []
  for result in ddmenu:
    people.append(result['name'].encode('utf-8'))

  name = request.args.get('name')

  if name == "All":
    name = None
  if name:
    results = g.conn.execute("SELECT * FROM Person P WHERE P.name = \'"+name+"\'")
  else:
    results = g.conn.execute("SELECT * FROM Person P")

  moviechar = g.conn.execute("SELECT A.pid, A.char_name, M.title, M.release_date, M.mid FROM Acts_in A, Movie M WHERE A.mid=M.mid")
  director = g.conn.execute("SELECT D.pid, M.title, M.release_date, M.mid FROM Directs D, Movie M WHERE D.mid=M.mid")
  writer = g.conn.execute("SELECT W.pid, M.title, M.release_date, M.mid FROM Writes W, Movie M WHERE W.mid=M.mid")
  awards = g.conn.execute("SELECT N.pid, A.year, A.type, A.category, N.won, M.title FROM Nominated_p N, Awards A, Movie M WHERE A.aid=N.aid AND N.mid=M.mid")

  final_results = []
  for result in results:
    current_person = {}
    current_person["info"] = [result[1], str(result[2]), result[3], result[4]]
    person_id = str(result[0])
    moviechar_array = []
    for mc in  moviechar:
      if person_id == str(mc[0]):
        moviechar_array.append([mc[1].encode('utf-8'), mc[2].encode('utf-8'), mc[3]])
    current_person["moviechar"] = moviechar_array
    director_array = []
    for d in director:
      if person_id == str(d[0]):
        director_array.append([d[1].encode('utf-8'), d[2]])
    current_person["director"] = director_array
    writer_array = []
    for w in writer:
      if person_id == str(w[0]):
        writer_array.append([w[1].encode('utf-8'), w[2]])
    current_person["writer"] = writer_array
    award_array = []
    for a in awards:
      if person_id == str(a[0]):
        won = str(a[4])
        won2 = "t"
        if won == won2:
          win = 'Won'
        else:
          win = 'Nominated'
        award_array.append([a[5].encode('utf-8'), a[1], a[2].encode('utf-8'), a[3].encode('utf-8'), win])
    current_person["award"] = award_array
    final_results.append(current_person)

  return render_template("person-search.html", name = name, chosen_name = name, data = people, data2 = pinfo, results= final_results)


@app.route('/award-search')
@app.route('/award-search<search>')
def index(search=None):

  ay = []
  awardYear = g.conn.execute("SELECT DISTINCT A.year FROM Awards A")
  for year in awardYear:
    ay.append(str(year[0]).encode('utf-8'))

  awardType = g.conn.execute("SELECT DISTINCT A.type FROM Awards A")
  at = []
  for ty in awardType:
    at.append(ty[0].encode('utf-8'))

  awardCat = g.conn.execute("SELECT DISTINCT A.category FROM Awards A")
  ac = []
  for result in awardCat:
    ac.append(result[0].encode('utf-8'))

  year =  request.args.get('year')
  atype =  request.args.get('atype')
  category = request.args.get('category')

  if year == "All":
    year = None
  if atype == "All":
    atype = None
  if category == "All":
    category = None


  if atype and category and year:
    results= g.conn.execute("SELECT * FROM Awards A WHERE A.type=\'" + atype + " \' AND A.category = \'" + category + "\' AND A.year =\'"+year+"\'")
  elif atype:
    results=g.conn.execute("SELECT * FROM Awards A WHERE A.type = \'" + atype + "\'")
  elif category:
    results=g.conn.execute("SELECT * FROM Awards A WHERE A.category=\'" + category + "\'")
  elif atype and category:
    results= g.conn.execute("SELECT * FROM Awards A WHERE A.type=\'" + atype + " \' AND A.category = \'" + category + "\'")
  elif atype and year:
    results= g.conn.execute("SELECT * FROM Awards A WHERE A.type=\'" + atype + " \' AND A.year =\'"+year+"\'")
  elif category and year:
    results= g.conn.execute("SELECT * FROM Awards A WHERE A.category = \'" + category + "\' AND A.year =\'"+year+"\'")
  else:
    results=g.conn.execute("SELECT * FROM Awards A")

  moviesp = g.conn.execute("SELECT M.mid, M.title, P.name, N.aid, N.won FROM Movie M, Person P, Nominated_p N, Awards A WHERE N.mid=M.mid AND N.aid = A.aid AND N.pid=P.pid")
  moviesm = g.conn.execute("SELECT M.mid, M.title, N.aid, N.won FROM Movie M, Nominated_m N, Awards A WHERE N.mid=M.mid AND N.aid = A.aid")

  final_results = []
  for result in results:
    current_award = {}
    current_award["info"] = [result[1], result[2], result[3]]
    aid = str(result[0])
    mp_array = []
    for mp in moviesp:
      if aid == str(mp[3]):
        won = str(mp[4])
        won2 = "t"
        if won ==won2:
          win = 'Won'
        else:
          win = 'Nominated'
        mp_array.append([mp[1].encode('utf-8'), mp[2].encode('utf-8'), win])
    current_award["moviep"] = mp_array
    m_array = []
    for m in moviesm:
      if aid == str(m[2]):
        won = str(m[3])
        won2 = "t"
        if won==won2:
          win = 'Won'
        else:
          win = 'Nominated'
        m_array.append([m[1].encode('utf-8'), win])
    current_award["moviem"] = m_array
    final_results.append(current_award) 

  return render_template('award-search.html', awardYear = ay, awardType=at, awardCat=ac, chosen_year = ay, chosen_type = at, chosen_cat = ac, results=final_results)

@app.route('/user-search')
@app.route('/user-search<search>')
def usersearch(search=None):
#get all info from User
  forTable = g.conn.execute("SELECT * FROM Users")
  uinfo = forTable.fetchall()

#get info from User, create array, put usernames in array
  ddmenu = g.conn.execute("SELECT * FROM Users")
  user = []
  for result in ddmenu:
    user.append(result['username'].encode('utf-8'))

  username = request.args.get('username')

  if username == "All":
    name = None
  if username:
    results = g.conn.execute("SELECT * FROM Users U WHERE U.username = \'"+username+"\'")
  else:
    results = g.conn.execute("SELECT * FROM Users U")

  review = g.conn.execute("SELECT R.username, M.title, R.rev_text, R.post_date FROM Movie M, Review_posted R WHERE R.mid = M.mid")
  rating = g.conn.execute("SELECT R.username, M.title, R.rating, R.post_date FROM Movie M, Rating_rated R WHERE R.mid = M.mid")

  final_results = []
  for result in results:
    current_user = {}
    current_user["info"] = [result[0], result[1], result[2], result[3]]
    uname = result[0]
    review_array = []
    for rev in review:
      if uname == str(rev[0]):
        review_array.append([rev[1].encode('utf-8'), rev[2].encode('utf-8'), rev[3]])
    current_user["review"] = review_array
    rating_array = []
    for rat in rating:
      if uname == str(rat[0]):
        rating_array.append([rat[1].encode('utf-8'), rat[2], rat[3]])
    current_user["rating"] = rating_array
    final_results.append(current_user)
  
  return render_template("user-search.html", username = username, chosen_username = username, data = user, data2 = uinfo, results=final_results)


@app.route('/character-search')
@app.route('/character-search<search>')
def characterearch(search=None):
#get all info from Character
  forTable = g.conn.execute("SELECT * FROM Character")
  cinfo = forTable.fetchall()

  ddmenu = g.conn.execute("SELECT * FROM Character")
  charac = []
  for result in ddmenu:
    charac.append(result['char_name'].encode('utf-8'))

  char_name = request.args.get('char_name')

  if char_name == "All":
    char_name = None

  if char_name:
    results = g.conn.execute("SELECT * FROM Character C WHERE C.char_name = \'"+char_name+"\'")
  else:
    results = g.conn.execute("SELECT * FROM Character C")

  moviechar = g.conn.execute("SELECT A.pid, A.char_name, M.mid, M.title, M.length, M.language, M.release_date, M.production_co, M.genre FROM Acts_in A, Movie M WHERE A.mid=M.mid")
  actors = g.conn.execute("SELECT P.pid, P.name, A.char_name, A.mid FROM Person P, Acts_in A WHERE A.pid=P.pid") 

  final_results = []
  for result in results:
    current_char = {}
    current_char["info"] = [result[0]]
    current_movie = []
    current_actor = []
    for actor in actors:
      if str(actor[2]) == str(result[0]):
        current_actor.append(actor[1])
    current_char["person_info"] = current_actor
    for mc in moviechar:
      if str(mc[1]) == str(result[0]):
        current_movie.append([mc[3]])
    current_char["movie_info"] = current_movie
    final_results.append(current_char)

  return render_template("/character-search.html", chosen_char = char_name, char_name = char_name, cinfo = cinfo, results = final_results)


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
