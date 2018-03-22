
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User,Manhua,Chapter
from ..email import send_email
from .forms import LoginForm, RegistrationForm, Addmhname
import os
import re


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/redirect', methods=['GET', 'POST'])
def leo_redirect():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

@auth.route('/manhuaname', methods=['GET', 'POST'])
def get_manhuaname():
    form = Addmhname()
    if form.validate_on_submit():
        manhua  = Manhua(mhname=form.mhname.data)
        db.session.add(manhua)
        db.session.commit()
    return render_template('auth/addnewmh.html', form=form)
    #return redirect(url_for('auth.leo_redirect'))


@auth.route('/leomahua')
def leomahua():
    list = Manhua.query.order_by(Manhua.mhname)
    # print list
    # print list[0].mhname
    # print type(list[0])
    return render_template('auth/showmh.html', data_list=list)

@auth.route('/leopic')
def leopic():
    #list = Manhua.query.order_by(Manhua.mhname)
    # print list
    # print list[0].mhname
    # print type(list[0])

    url_list = getDate()
    return render_template('auth/showpic.html', url_list=url_list)


@auth.route('/addpic')
def addpic():
    url_list = getDate()


    #Chapter
    #list = Manhua.query.order_by(Manhua.mhname)
    # print list
    # print list[0].mhname
    # print type(list[0])
    #return render_template('auth/showpic.html')



def getDate():
    loadfile = [u'./app/static']
    mydict = {}
    mylist = []
    while(loadfile):
        try:
            path = loadfile.pop()
            #
            #print path
            for x in os.listdir(path):
                if os.path.isfile(os.path.join(path,x)):
                    if os.path.splitext(x)[1]=='.jpg' or os.path.splitext(x)[1]=='.png':
                        try:
                            pass
                        except Exception,e:
                            pass
                        templist = test3(path.split('\\')[-1],x,path.split('\\')[-2])
                        mydict[templist[0]] = templist
                else:
                    loadfile.append(os.path.join(path,x))

        except Exception,e:
            print str(e) + path


    #InsertData('mhpic',mydict)
    url_list = []
    for key in mydict:
        mylist.append(mydict[key])
        url_list.append(mydict[key][5].replace('./app/static/',""))

    return url_list

def test3(chaptername,check_str,mhname):
    str_type = check_str.split('.')[-1]
    str_name = chaptername

    pattern = re.compile(u'(.+)\.+(.+)')
    match = pattern.match(check_str)
    str_id =  match.group(1)

    str_nums = str_id.replace(chaptername,'')
    if str_nums.find('num')!=-1:
        str_nums = check_str.split('.')[0].replace('num','')

    return [str_id,str_type,mhname,str_name,str_nums,mhname + '/' + str_name + '/' + check_str]