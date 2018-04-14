import sqlite3 ,os
from flask import Flask, flash, redirect, render_template, request, session, abort , g , url_for , jsonify
from passlib.hash import sha256_crypt as sha
from functools import wraps
import csv
import distance
import json

app = Flask(__name__, static_folder="static")

Database = 'octahacks.db'

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(Database)
    return db

def query_db(query, args=(), one=False): #used to retrive values from the table
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query , args=()): #executes a sql command like alter table and insert
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query , args)
    conn.commit()
    cur.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/' ,methods=['POST','GET'])
def login():
    if request.method == "GET":
        return render_template("new_index.html")
    else:
        error = None
        username=request.form["username"]
        password=request.form["password"]
        phash = query_db("select password from users where usrname = ?", (username, ))
        if phash==[]:
            return "Username doesnt exist"

        if sha.verify(password, phash[0][0]):
            session["username"] = username
            return redirect(url_for('addpkg'))
        else:
            return "Password Incorrect"


@app.route('/#signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        submission = {}
        submission["username"] = request.form["username"]
        submission["pass"] = request.form["password"]
        submission["conf_pass"] = request.form["conf_pass"]


        if submission["pass"]!=submission["conf_pass"]:
            return "Wrong password"

        if query_db("select username from users where username = ?", (submission["username"],))!=[]:
            error = "Username already taken" 

        password = sha.encrypt(submission["pass"])
        execute_db("insert into users values(?,?)", (
            submission["username"],
            password,
        ))

        return redirect(url_for("login"))

@app.route("/#logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "GET":
        render_template("change.html")
    else:
        password = request.form["old_password"]
        old_password = query_db("select password from users where username = ?", (session["username"],))
        if sha.verify(password, old_password[0][0]):
            submission = {}
            submission["pass"] = request.form["password"]
            submission["conf_pass"] = request.form["conf_pass"]
            
            if submission["pass"]!=submission["conf_pass"]:
                flash("Password doesnt match")
                return redirect(url_for("change"))
            
            password = sha.encrypt(submission["pass"])
            
            execute_db("update users set password = ? where username = ?", (
            password,
            session["username"],))
            return redirect(url_for("login"))
        else:
            flash("Wrong Password")
            return redirect(url_for("change"))

@app.route('/#addpkg', methods=['GET', 'POST'])
def addpkg():
    if request.method == "POST":
        submission = {}
        submission["srcpin"] = form.request["srcpin"]
        submission["dstpin"] = form.request["dstpin"]
        submission["name"] = form.request["name"]
        submission["srcadd"] = form.request["srcadd"]
        submission["dstadd"] = form.request["dstadd"]

        execute_db("insert into users values(?, ?, ?, ?, ?)", (
            submission["srcpin"],
            submission["dstpin"],
            submission["name"],
            submission["srcadd"],
            submission["dstadd"],
        ))

    return render_template("addpkg.html")

@app.route('/populate')
def populate():
    f = open("postoffices.csv", 'r')
    reader = csv.reader(f)
    csv_list = list(reader)
    for po in csv_list:
        password = sha.encrypt(po[2])
        if query_db("select usrname from users where usrname = ?", (po[2], ))==[]:
            execute_db("insert into users values(?, ?)", (
                po[2],
                password,
            ))
    return "Success"

@app.route('/cal')
def cal_distime():
    res = {}
    query = query_db("select usrname from users")
    le = len(query)
    k = open('res.json', 'a')
    for i in range(16):
        temp = {}
        for j in range(16):
            dst, time = distance.parse_url(query[i][0], query[j][0])
            temp_1 = {}
            temp_1["distance"] = dst
            temp_1["time"] = time
            temp[str(query[j][0])] = temp_1
        res[str(query[i][0])] = temp
    json.dump(res, k)
    k.close()
    return "Success"

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host = "0.0.0.0",debug=True, port=8080)

















    import sys

def process(graph,dest):
    l=len(dest)
    arr=[]
    for i in range(l):
        li= []
        for j in range(l):
            li.append(0)
        arr.append(li)

    for i in range(0,l):
        for j in range(i,l):
            arr[i][j] = graph[dist[i]][dist[j]]
            arr[j][i]=arr[i][j]
    dist=[sys.maxint]*l
    visited=[false]*l
    parent=[0]*l
    dist[0]=0;
    while l is not 0:
        u=minimum(dist,visited)
        visited[u]=true
        for i in range(0,l):
            if !visited[j] and dist[j]>arr[u][j]:
                dist[j]=arr[u][j]
                parent[j]=u

    mst=[]
    for i in range(l):
        li = []
        for j in range(l):
            li.append(0)
        mst.append(li)

        
    for i in range(0,len(parent)):
        mst[parent[i]][i]=1
        mst[i][parent[i]]=1
return mst


def minimum(dist,visited):
    min=sys.maxint
    node=0;
    for x in len(dist):
        if !visited[x]&& min>dist[x]:
            min=dist[x]
            node=x
    return node


def process2(mst,x):
    for i in mst:
        if i==0
            ;
        else:
            li.append(i)
            li.append(process2(mst,i))
            return li


def fina_path():
    json_file
    truck_cap=40000
    for a in json_file:
        li.append(s['destpin'],s['id'])
        ms.append(li)
    # sort
    trucks=[]
    left=[]
    p=0
    for i in range(len(ms)):
        if ms[i]['destpin']==ms[i]['destpin']:
            trucks[p++]=ms[i:i+truck_cap]
            i+=truck+cap
        else:
            left.append(ms[i])
    set.add(source) 
    for x in left:
        set.add(x['destpin'])

    mst=process(json_file,set)
    for x in mst:
        if x is not 0:
            li.append(process2(mst,x['']))

    set2.add(li)
    truckcap=truck_cap
    for x in set2:
        for a in left:
            if set2.contains(a):
                trucks[p].append(a)
                truckcap--;
                if truckcap==0:
                    p++;
                    truckcap=truck_cap

        p++;
        truckcap=truck_cap



