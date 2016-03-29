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

@app.route('/')
@app.route('/<search>')
def index(search=None):
  movies = g.conn.execute("SELECT DISTINCT title FROM Movie")
  movies.fetchall()
    
  people = g.conn.execute("SELECT DISTINCT name FROM Person")
  people.fetchall()

  characters = g.conn.execute("SELECT DISTINCT char_name FROM Character")
  characters.fetchall()


  title = request.args.get('title')
  person = request.args.get('person')
  charact = request.args.get('charact')
#is this allowed/ syntax???
  results = g.conn.cursor()	

  if title == "All":
    title = None
  if person == "All":
    person = None
  if charact == "All":
    charact = None

	if zipcode and cuisine:
		results.execute("SELECT DISTINCT R.r_id, R.name, A.building_number, A.street_name, A.city, A.zip, R.cuisine, R.website_url FROM Addresses A, Restaurants R WHERE A.a_id = R.a_id AND R.cuisine=\'" + cuisine + " \' AND A.zip = \'" + zipcode + "\'")
	elif cuisine:
		results.execute("SELECT DISTINCT R.r_id, R.name, A.building_number, A.street_name, A.city, A.zip, R.cuisine, R.website_url FROM Addresses A, Restaurants R WHERE A.a_id = R.a_id AND R.cuisine = \'" + cuisine + "\'")
	elif zipcode:
		results.execute("SELECT DISTINCT R.r_id, R.name, A.building_number, A.street_name, A.city, A.zip, R.cuisine, R.website_url FROM Addresses A, Restaurants R WHERE A.a_id = R.a_id AND A.zip = \'" + zipcode + "\'")
	else:
		results.execute("SELECT DISTINCT R.r_id, R.name, A.building_number, A.street_name, A.city, A.zip, R.cuisine, R.website_url FROM Addresses A, Restaurants R WHERE A.a_id = R.a_id")

	reviews = mysql.connect.cursor()
	reviews.execute("SELECT R.u_id, R.date_reviewed, R.comment, R.rating, R.r_id FROM Reviews R")
	reviews = reviews.fetchall()

	violations = mysql.connect.cursor()
	violations.execute("SELECT date_inspected, violation_count, grade, r_id, v_id FROM ViolationSummaries")	
	violations = violations.fetchall()
	
	reviewers = mysql.connect.cursor()
	reviewers.execute("SELECT name, review_count, average_rating, u_id FROM Reviewers")
	reviewers = reviewers.fetchall()
	
	violation_details = mysql.connect.cursor()
	violation_details.execute("SELECT violation_detail, critical, v_id FROM Violations")
	violation_details = violation_details.fetchall()

	final_results = []
	for result in results:
		current_restaurant = {}
		address = (str(result[2])+" "+result[3]+" "+result[4]+" "+str(result[5])).replace("None","")
		restaurant_id = str(result[0])
		review_array = []
		rating_array = []
		for review in reviews:
			if restaurant_id == str(review[4]):
				rating_array.append(review[3])
				current_review = []
				user_id = str(review[0])
				date = review[1].strftime("%Y/%m/%d")
				for reviewer in reviewers:
					if user_id == str(reviewer[3]):
						review_array.append([reviewer[0],date,review[3],review[2],reviewer[1],reviewer[2]])
		average_rating = sum(rating_array)/len(rating_array)
		if rating:
			if float(average_rating) < float(rating):
				continue
		current_restaurant["basic_info"] = [result[1], address, result[6], result[7], str(average_rating)]
		current_restaurant["reviews"] = review_array
		violation_array = []
		for violation in violations:
			if restaurant_id == str(violation[3]):
				date = violation[0].strftime("%Y/%m/%d")
				violation_detail_array = []
				for violation_detail in violation_details:
					if str(violation[4]) == str(violation_detail[2]):
						if violation_detail[1] == 1:
							critical = "True"
						else:
							critical = "False"
						violation_detail_array.append([violation_detail[0],critical])
				violation_array.append([date,violation[1],violation[2],violation_detail_array])
		current_restaurant["violations"] = violation_array
		final_results.append(current_restaurant)

	#format for each result is
	#["basic_info"] = [r_name, address, cuisine, web_url, avg_rating for restaurant]
	#["reviews"] = [[u_name,r_date,rating,comment,user_rating_count,user_rating_avg].[]] Array of arrays each array being one review
	#["violations"] = [[date,violation_count,grade],[]] Array of arrays each array being one summary

	if rating == None:
		rating == "All"
	else:
		rating = float(rating)
	if zipcode == None:
		zipcode == "All"
	else:
		zipcode = long(zipcode)

	return render_template('index.html', cuisines=cuisines, zip_codes=zip_codes, ratings=ratings, results=final_results,
			chosen_cuisine=cuisine, chosen_zip=zipcode, chosen_rating=rating)

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
