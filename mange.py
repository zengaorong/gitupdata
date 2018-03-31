import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask.ext.script import Manager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:7Monthdleo@localhost/leodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)


# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<User %r>' % self.username

class Manhua(db.Model):
    __tablename__ = 'mhname'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    mhname = db.Column(db.String(64), unique=True)
    #users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Manhua %r>' % self.mhname

class Chapter(db.Model):
    __tablename__ = 'mhchapter'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    mhname_id = db.Column(db.VARCHAR(36), db.ForeignKey('mhname.id'))
    data = db.Column(db.Text())
    chapter_nums = db.Column(db.Integer)
    pics_nums = db.Column(db.Integer)
    chapter_name = db.Column(db.String(64))
    #users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<mhchapter %r>' % self.chapter_name

# class NameForm(FlaskForm):
#     name = StringField('What is your name?', validators=[DataRequired()])
#     submit = SubmitField('Submit')
#
#
# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Role=Role)
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             db.session.commit()
#             session['known'] = False
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         return redirect(url_for('index'))
#     return render_template('index.html', form=form, name=session.get('name'),
#                            known=session.get('known', False))


db.create_all()
db.session.commit()
if __name__ == "__main__":
    manager.run()