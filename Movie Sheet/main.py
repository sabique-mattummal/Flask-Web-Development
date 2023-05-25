from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECURITY KEY"
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    class Movies(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False, unique=True)
        year = db.Column(db.Integer, nullable=False)
        description = db.Column(db.String(1000), nullable=False)
        rating = db.Column(db.Float, nullable=False)
        ranking = db.Column(db.String(250), nullable=False)
        review = db.Column(db.String(1000), nullable=False)
        img_url = db.Column(db.String(100), nullable=False)

        def __repr__(self):
            return '<Movies %r> %self.title'

    db.create_all()

class RateMovieForm(FlaskForm):
    rating = StringField('Update Rating', validators=[DataRequired()])
    review = StringField('Update Review', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddMovieForm(FlaskForm):
    title = StringField('Movie Name', validators=[DataRequired()])
    submit = SubmitField('Find')


@app.route('/')
def home():
    all_movies = Movies.query.order_by(Movies.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template('index.html', movies=all_movies)

@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie = Movies.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['POST', 'GET'])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        URL = "https://api.themoviedb.org/3/search/movie?" \
              "api_key=API KEY"
        response = requests.get(f"{URL}&query={movie_title}").json()
        data = response['results']
        return render_template('select.html',options=data)
    return render_template('add.html', form=form)

@app.route('/find_movie', methods=['GET', 'POST'])
def find_movie():
    movie_api_id = request.args.get('id')
    if movie_api_id:
        URL = f"https://api.themoviedb.org/3/movie/{movie_api_id}?" \
            f"api_key=API KEY"
        response = requests.get(URL)
        data = response.json()
        new_movie = Movies(
            title=data['original_title'],
            year = data['release_date'].split('-')[0],
            description = data['overview'],
            rating=0,
            ranking='None',
            review =data['tagline'],
            img_url=f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit', id=new_movie.id))


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    editform = RateMovieForm()
    movie_id = request.args.get('id')
    movie = Movies.query.get(movie_id)
    if editform.validate_on_submit():
        movie.rating = float(editform.rating.data)
        movie.review = editform.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=editform, movie=movie)


if __name__ == "__main__":
    app.run(debug=True)
