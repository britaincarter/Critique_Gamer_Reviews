#!/usr/bin/env python2.7

"""

To run locally:
    python server.py

Go to http://localhost:8111 in your browser
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DATABASEURI = "postgresql://:admin@vpallone.com"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  Ran on every request to setup a global database connection g
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
  End of request, close the database connection.
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  return render_template("index.html")
  
@app.route('/another')
def another():
  return render_template("another.html")

@app.route('/dev_avg', methods=['GET'])
def dev_avg():
  form = request.args.get('developer')
  if form == "":
  	cursor = g.conn.execute("WITH avgs AS (SELECT G.url AS gurl, AVG(A.rating) AS gavg FROM game G, author Au, article A, shares S WHERE G.gid = S.gid AND A.aurl = S.aurl AND S.aid = Au.aid GROUP BY (G.gid)) SELECT C.name, AVG(gavg) FROM avgs, Company C WHERE gurl = C.url  GROUP BY (C.name)")
  else:
  	cursor = g.conn.execute("WITH avgs AS (SELECT G.url AS gurl, AVG(A.rating) AS gavg FROM game G, author Au, article A, shares S WHERE G.gid = S.gid AND A.aurl = S.aurl AND S.aid = Au.aid GROUP BY (G.gid)) SELECT C.name, AVG(gavg) FROM avgs, Company C WHERE gurl = C.url AND C.name = '%s' GROUP BY (C.name)" % form)
  header = "** NAME | AVG RATING **"
  companies = []
  companies.append(header)
  for result in cursor:
    tmp = ""
    tmp += str(result[0])
    tmp += " | "
    tmp += str(result[1])
    companies.append(tmp)
  cursor.close()
  context = dict(data = companies)
  return render_template("data.html", **context)

@app.route('/articles', methods=['GET'])
def author():
  form1 = request.args.get('author')
  form2 = request.args.get('game_article')
  if form1 == "" and form2 == "":
  	cursor = g.conn.execute("SELECT G.gname, Au.aname, A.rating, A.aurl FROM Article A, Shares S, Game G, Author Au, Critic C, Publishes P, Reviews R WHERE R.gid = G.gid AND Au.aid = R.aid AND A.aurl = S.aurl AND S.gid = G.gid AND C.url = P.url AND P.aurl = A.aurl AND Au.url = C.url") 
  elif form1 == "":
  	cursor = g.conn.execute("SELECT G.gname, Au.aname, A.rating, A.aurl FROM Article A, Shares S, Game G, Author Au, Critic C, Publishes P, Reviews R WHERE R.gid = G.gid AND Au.aid = R.aid AND A.aurl = S.aurl AND S.gid = G.gid AND C.url = P.url AND P.aurl = A.aurl AND Au.url = C.url AND G.gname = '%s'" % form2)
  elif form2 == "":
  	cursor = g.conn.execute("SELECT G.gname, Au.aname, A.rating, A.aurl FROM Article A, Shares S, Game G, Author Au, Critic C, Publishes P, Reviews R WHERE R.gid = G.gid AND Au.aid = R.aid AND A.aurl = S.aurl AND S.gid = G.gid AND C.url = P.url AND P.aurl = A.aurl AND Au.url = C.url AND Au.aname = '%s'" % form1)
  else:
    tmp = ""
    tmp += str(result[0])
    tmp += " | "
    tmp += str(result[1])
    tmp += " | "
    tmp += str(result[2])
    tmp += " | "
    tmp += str(result[3])
    articles.append(tmp)
  cursor.close()
  context = dict(data = articles)
  return render_template("data.html", **context)


@app.route('/dist_avg', methods=['GET'])
def dist_avg():
  form = request.args.get('distributor')
  if form == "":
  	cursor = g.conn.execute("WITH avgs AS (SELECT D.url AS durl, AVG(S.price) AS pavg FROM game G, Sells S, Distributor D WHERE G.gid = S.gid AND D.url = S.url GROUP BY (D.url)) SELECT C.name, AVG(pavg) FROM avgs, Company C WHERE Durl = C.url GROUP BY (C.name)")
  else:
  	cursor = g.conn.execute("WITH avgs AS (SELECT D.url AS durl, AVG(S.price) AS pavg FROM game G, Sells S, Distributor D WHERE G.gid = S.gid AND D.url = S.url GROUP BY (D.url)) SELECT C.name, AVG(pavg) FROM avgs, Company C WHERE Durl = C.url AND C.name = '%s' GROUP BY (C.name)" % form)
  header = "** NAME | AVG PRICE **"
  companies = []
  companies.append(header)
  for result in cursor:
    tmp = ""
    tmp += str(result[0])
    tmp += " | "
    tmp += str(result[1])
    companies.append(tmp)
  cursor.close()
  context = dict(data = companies)
  return render_template("data.html", **context)


@app.route('/company', methods=['GET'])
def company():
  form = request.args.get('company')
  if form == "":
  	cursor = g.conn.execute("WITH avgs AS(SELECT C.name AS cn, AVG(A.rating) AS avg FROM company C, author Au, article A, shares S WHERE Au.url = C.url AND A.aurl = S.aurl AND S.aid = Au.aid GROUP BY (C.name)) SELECT DISTINCT cn, avg FROM avgs, company C WHERE C.name = cn")
  else:
  	cursor = g.conn.execute("WITH avgs AS(SELECT C.name AS cn, AVG(A.rating) AS avg FROM company C, author Au, article A, shares S WHERE Au.url = C.url AND A.aurl = S.aurl AND S.aid = Au.aid GROUP BY (C.name)) SELECT DISTINCT cn, avg FROM avgs, company C WHERE C.name = cn AND cn = '%s'" % form)
  header = "** NAME | AVG RATING **"
  companies = []
  companies.append(header)
  for result in cursor:
    tmp = ""
    tmp += str(result[0])
    tmp += " | "
    tmp += str(result[1])
    companies.append(tmp)
  cursor.close()
  context = dict(data = companies)
  return render_template("data.html", **context)

@app.route('/gamegenre', methods=['GET'])
def gamegenre():
  genre = request.args.get('genre')
  rating = request.args.get('rating')
  games = []
  
  if genre == "" and rating == "":
	cursor = g.conn.execute("WITH avgs AS (SELECT G.gname AS gn, AVG(A.rating) AS avg FROM game G, author Au, article A, shares S WHERE G.gid = S.gid AND A.aurl = S.aurl AND S.aid = Au.aid GROUP BY (G.gid)) SELECT DISTINCT gn, G.genre, avg FROM avgs, game G WHERE gn = G.gname")
  elif genre == "":
	cursor = g.conn.execute("WITH avgs AS (SELECT G.gname AS gn, AVG(A.rating) AS avg FROM game G, author Au, article A, shares S WHERE G.gid = S.gid AND A.aurl = S.aurl AND S.aid = Au.aid GROUP BY (G.gid)) SELECT DISTINCT gn, G.genre, avg FROM avgs, game G WHERE gn = G.gname AND avg >= %s" % rating)
  elif rating == "":
	cursor = g.conn.execute("WITH avgs AS (SELECT G.gname AS gn, AVG(A.rating) AS avg FROM game G, author Au, article A, shares S WHERE G.gid = S.gid AND A.aurl = S.aurl AND S.aid = Au.aid GROUP BY (G.gid)) SELECT DISTINCT gn, G.genre, avg FROM avgs, game G WHERE gn = G.gname AND G.genre = '%s'" % genre)
  else:	  
	cursor = g.conn.execute("WITH avgs AS (SELECT G.gname AS gn, AVG(A.rating) AS avg FROM game G, author Au, article A, shares S WHERE G.gid = S.gid AND A.aurl = S.aurl AND S.aid = Au.aid GROUP BY (G.gid)) SELECT DISTINCT gn, G.genre, avg FROM avgs, game G WHERE gn = G.gname AND avg >= %s AND G.genre = '%s'" % (rating, genre))

  header = "** NAME | GENRE | RATING **"
  games.append(header)
  for result in cursor:
    tmp = ""
    tmp += str(result[0])
    tmp += " | "
    tmp += str(result[1])
    tmp += " | "
    tmp += str(result[2])
    games.append(tmp)
  cursor.close()
  context = dict(data = games)
  return render_template("data.html", **context)

@app.route('/companytype', methods=['GET'])
def companytype():
  check = 0
  form = request.args.get('companytype')

  if form == "Distributor":
  	header = "** URL | Name | Location | Type **"
  	cursor = g.conn.execute("SELECT S.url, C.name, C.location, S.type FROM %s S, Company C WHERE C.url = S.url" % form)
  elif form == "Developer":
  	header = "** URL | Name | Location | Prestige **" 
  	cursor = g.conn.execute("SELECT S.url, C.name, C.location, S.prestige FROM %s S, Company C WHERE C.url = S.url" % form)
  elif form == "Critic":
  	header = "** URL | Name | Location | Media **"
  	cursor = g.conn.execute("SELECT S.url, C.name, C.location, S.media FROM %s S, Company C WHERE C.url = S.url" % form)
  else:
  	header = "** URL | Name | Location **"
  	cursor = g.conn.execute("SELECT C.url, C.name, C.location FROM Company C")
	check = 1

  companytype = []
  companytype.append(header)
  for result in cursor:
    tmp = ""
    tmp += str(result[0])
    tmp += " | "
    tmp += str(result[1])
    tmp += " | "
    tmp += str(result[2])
    if check == 0:
    	tmp += " | "
    	tmp += str(result[3])
    companytype.append(tmp)
  cursor.close()
  context = dict(data = companytype)
  return render_template("data.html", **context)

@app.route('/see_like_author', methods=['GET'])
def see_like_author():
  user_name = request.args.get('see_user_like_author')
  Searched = request.args.get('see_like_author')

  print user_name
  print Searched

  if user_name == "":
	return render_template("another.html") 

  elif Searched == "":

	cursor = g.conn.execute(("SELECT A.aname FROM Author A, Likes_Author L, siteUser U WHERE L.aid = A.aid AND L.uid = U.uid AND U.uname='%s'")%user_name)

  else:
	cursor = g.conn.execute(("SELECT A.aname FROM Author A, Likes_Author L, siteUser U WHERE L.aid = A.aid AND L.uid = U.uid AND A.aname = '%s' AND U.uname='%s'")%(Searched, user_name))

  header = "** Author **"
  authors = []
  authors.append(header)
  for result in cursor:
    tmp = ""
    tmp += str(result[0])
    authors.append(tmp)
  cursor.close()
  context = dict(data = authors)
  return render_template("data.html", **context)


@app.route('/see_like_company', methods=['GET'])
def see_like_company():
  user_name = request.args.get('see_user_like_company')
  companySearched = request.args.get('see_like_company')

  print user_name
  print companySearched

  if user_name == "":
	return render_template("another.html") 

  elif companySearched == "":

	cursor = g.conn.execute(("SELECT C.name FROM Company C, Likes_Company L, siteUser U WHERE L.url = C.url AND L.uid = U.uid AND U.uname='%s'")%user_name)

  else:
	cursor = g.conn.execute(("SELECT C.name FROM Company C, Likes_Company L, siteUser U WHERE L.url = C.url AND L.uid = U.uid AND C.name = '%s' AND U.uname='%s'")%(companySearched, user_name))
  
  header = "** Company **"
  companies = []
  companies.append(header)
  for result in cursor:
    tmp = ""
    tmp += str(result[0])
    companies.append(tmp)
  cursor.close()
  context = dict(data = companies)
  return render_template("data.html", **context)


@app.route('/see_like_game', methods=['GET'])
def see_like_game():
  user_name = request.args.get('see_user_like_game')
  gameSearched = request.args.get('see_like_game')

  print user_name
  print gameSearched

  if user_name == "":
	return render_template("another.html") 

  elif gameSearched == "":

	cursor = g.conn.execute(("SELECT G.gname FROM Game G, Likes_Game L, siteUser U WHERE L.gid = G.gid AND L.uid = U.uid AND U.uname='%s'")%user_name)

  else:
	cursor = g.conn.execute(("SELECT G.gname FROM Game G, Likes_Game L, siteUser U WHERE L.gid = G.gid AND L.uid = U.uid AND G.gname = '%s' AND U.uname='%s'")%(gameSearched, user_name))

  header = "** Game **"
  games = []
  games.append(header)
  for result in cursor:
    tmp = ""
    tmp += str(result[0])
    games.append(tmp)
  cursor.close()
  context = dict(data = games)
  return render_template("data.html", **context)


@app.route('/like_company', methods=['POST'])
def like_company():
    form = request.form['like_company']
    user_name = request.form['user_like_company']
    if form == "":
        return redirect('/another')
    elif user_name == "":
        return redirect('/another')
    else:
        cursor = g.conn.execute("SELECT MAX(U.uid) FROM siteuser U")
        max_id = []
        for result in cursor:
                tmp = str(result[0])
                max_id.append(tmp)
        cursor.close()

        intmax_id = int(max_id[0])
        newuser_id= intmax_id+1
        cursor = g.conn.execute(("SELECT U.uid FROM siteuser U WHERE U.uname = '%s'")%user_name)

        PKnameExists = []
        for result in cursor:
                tmp = str(result[0])
                PKnameExists.append(tmp)
        cursor.close()
        if PKnameExists:
                PKname = int(PKnameExists[0])
        else:
                PKname = ""

        cursor = g.conn.execute(("SELECT C.url FROM Company C WHERE C.name = '%s'")%form)

        PKcompanyExists = []
        for result in cursor:
                tmp = str(result[0])
                PKcompanyExists.append(tmp)
        cursor.close()

        if PKcompanyExists:
                PKcompany = PKcompanyExists[0]
        else:
                PKcompany = ""
        if PKname != "" and PKcompany != "":
                cursor = g.conn.execute(("SELECT L.url FROM likes_company L WHERE L.url = '%s' AND L.uid = %d")%(PKcompany, PKname))

                check = []
                for result in cursor:
                        tmp = str(result[0])
                        check.append(tmp)
                cursor.close()

                if not check:
                        g.conn.execute(("INSERT INTO likes_company(uid, url) VALUES (%d, '%s')"%(PKname, PKcompany)))
                else:
                        return redirect('/another')

        elif PKcompany != "" and PKname == "":
                g.conn.execute("INSERT INTO siteUser(uid, uname, email, locale) VALUES (%d, '%s', '%s', NULL)"%(newuser_id, user_name, user_name))
                g.conn.execute("INSERT INTO likes_company(uid, url) VALUES (%d, '%s')"%(newuser_id, PKcompany))

        return redirect('/another')


@app.route('/like_author', methods=['POST'])
def like_author():
    form = request.form['like_author']
    user_name = request.form['user_like_author']
    if form == "":
        return redirect('/another')
    elif user_name == "":
        return redirect('/another')
    else:
        cursor = g.conn.execute("SELECT MAX(U.uid) FROM siteuser U")
        max_id = []
        for result in cursor:
                tmp = str(result[0])
                max_id.append(tmp)
        cursor.close()
        intmax_id = int(max_id[0])
        newuser_id= intmax_id+1
        cursor = g.conn.execute(("SELECT U.uid FROM siteuser U WHERE U.uname = '%s'")%user_name)

        PKnameExists = []
        for result in cursor:
                tmp = str(result[0])
                PKnameExists.append(tmp)
        cursor.close()
        if PKnameExists:
                PKname = int(PKnameExists[0])
        else:
                PKname = ""

        cursor = g.conn.execute(("SELECT A.aid FROM Author A WHERE A.aname = '%s'")%form)
        PKauthorExists = []
        for result in cursor:
                tmp = result[0]
                PKauthorExists.append(tmp)
        cursor.close()

        if PKauthorExists:
                PKauthor = PKauthorExists[0]
        else:
                PKauthor = ""
        if PKname != "" and PKauthor != "":
                cursor = g.conn.execute(("SELECT L.aid FROM likes_author L WHERE L.aid = %d AND L.uid = %d")%(PKauthor, PKname)) 

                check = []
                for result in cursor:
                        tmp = result[0]
                        check.append(tmp)
                cursor.close()

                if not check:
                        g.conn.execute(("INSERT INTO likes_author(uid, aid) VALUES (%d, %d)"%(PKname, PKauthor)))
                else:
                        return redirect('/another')
 
        elif PKauthor != "" and PKname == "":
                g.conn.execute("INSERT INTO siteUser(uid, uname, email, locale) VALUES (%d, '%s', '%s', NULL)"%(newuser_id, user_name, user_name))
                g.conn.execute("INSERT INTO likes_author(uid, aid) VALUES (%d, %d)"%(newuser_id, PKauthor))

        return redirect('/another')

@app.route('/like_game', methods=['POST'])
def like_game():
    form = request.form['like_game']
    user_name = request.form['user_like_game']    

    if form == "":      
        return redirect('/another')
    elif user_name == "":
        return redirect('/another')
    else:
        cursor = g.conn.execute("SELECT MAX(U.uid) FROM siteuser U")    
        max_id = []
        for result in cursor:
                tmp = str(result[0])
                max_id.append(tmp)
        cursor.close()
        intmax_id = int(max_id[0])
        newuser_id= intmax_id+1
        cursor = g.conn.execute(("SELECT U.uid FROM siteuser U WHERE U.uname = '%s'")%user_name)
        
        PKnameExists = []
        for result in cursor:
                tmp = result[0]
                PKnameExists.append(tmp)
        cursor.close()
        if PKnameExists:
                PKname = int(PKnameExists[0])
        else:
                PKname = ""

        cursor = g.conn.execute(("SELECT G.gid FROM Game G WHERE G.gname = '%s'")%form)
        
        PKgameExists = []
        for result in cursor:
                tmp = result[0]
                PKgameExists.append(tmp)
        cursor.close()
        
        if PKgameExists:
                PKgame = PKgameExists[0]
        else:
                PKgame = ""
        if PKname != "" and PKgame != "":
                cursor = g.conn.execute(("SELECT L.gid FROM likes_game L WHERE L.gid = %d AND L.uid = %d")%(PKgame, PKname)) 
                check = []
                for result in cursor:
                        tmp = str(result[0])
                        check.append(tmp)
                cursor.close()
        
                for result in cursor:
                        tmp = str(result[0])
                        check.append(tmp)
                cursor.close()
        
        if PKgameExists:
                PKgame = PKgameExists[0]
        else:
                PKgame = ""
        if PKname != "" and PKgame != "":
                cursor = g.conn.execute(("SELECT L.gid FROM likes_game L WHERE L.gid = %d AND L.uid = %d")%(PKgame, PKname)) 
                check = []
                for result in cursor:
                        tmp = str(result[0])
                        check.append(tmp)
                cursor.close()

                if not check:
                        g.conn.execute(("INSERT INTO likes_game(uid, gid) VALUES (%d, %d)"%(PKname, PKgame)))
                else:
                        return redirect('/another')

        elif PKgame != "" and PKname == "":
                g.conn.execute("INSERT INTO siteUser(uid, uname, email, locale) VALUES (%d, '%s', '%s', NULL)"%(newuser_id, user_name, user_name))
                g.conn.execute("INSERT INTO likes_game(uid, gid) VALUES (%d, %d)"%(newuser_id, PKgame))
        return redirect('/another')


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    Handles command line parameters.
    Run the server using:
        python server.py
    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
