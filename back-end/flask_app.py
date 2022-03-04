import flask
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from flask_mysqldb import MySQL
import ibm

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './uploads'

app.config['MYSQL_HOST'] = 'elmo4679.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'elmo4679'
app.config['MYSQL_PASSWORD'] = 'REZa4679'
app.config['MYSQL_DB'] = 'elmo4679$movies'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

CORS(app)

mysql = MySQL(app)


@app.route('/hello')
def hello():
    return {'name': 'elmo', 'msg': 'welcome'}


@app.route('/add_comment', methods=['POST'])
def add_comment():

    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('./', filename))
        text = ibm.speech_to_text_request(f'./{filename}')
        should_save = ibm.natural_language_understanding_request(text)

        if should_save:
            movie_name = request.args.get('movie_name')
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM comments")
            comments = cur.fetchall()

            cur.execute('insert into comments (id, user_name, movie_name, comment) values (%s, %s, %s, %s)',
                        (str(len(comments)), request.args.get('user_name'), movie_name, text))
            mysql.connection.commit()
            return flask.make_response({
                'movie_name': movie_name,
                'user_name': request.args.get('user_name'),
                'comment': text
            }, 200)
        else:
            return flask.make_response(flask.jsonify('comment was not proper'), 400)
    else:
        return flask.make_response(flask.jsonify({'error': 'No file'}), 400)


@app.route('/get_comments', methods=['GET'])
def get_comments():
    movie_name = request.args.get('movie_name')
    language = request.args.get('language')
    cur = mysql.connection.cursor()
    cur.execute("select * from comments where movie_name = %s", (movie_name,))
    result = cur.fetchall()
    response = {}
    for movie in result:
        id = movie['id']
        user_name = movie['user_name']
        movie_name = movie['movie_name']
        comment = movie['comment']
        if language != 'en':
            comment = ibm.language_translator_request(comment, language)
        response[id] = {'user_name': user_name, 'comment': comment, 'movie_name': movie_name}
    return flask.make_response({'comments': response}, 200)



@app.route('/get_movies', methods=['GET'])
def get_movies():
    cur = mysql.connection.cursor()
    cur.execute("select * from movies")
    result = cur.fetchall()
    response = {}
    for movie in result:
        name = movie['name']
        director = movie['director']
        poster = movie['poster']
        response[name] = {'director': director, 'poster': poster}
    return flask.make_response({'movies': response}, 200)