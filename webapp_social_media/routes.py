from PIL import Image
import secrets
import os
from flask import render_template, url_for, flash, redirect, request, abort
from webapp_social_media import app, db, bcrypt
from webapp_social_media.forms import RegistrationForm, RegistrationFormPremium, LoginForm, UpdateAccountForm, PostForm, UserInterestForm, SearchUserForm
from webapp_social_media.models import User, Post, InterestTopic, InterestTopicUser, requests, friends
from flask_login import login_user, current_user, logout_user, login_required
import logging
from sqlalchemy import and_
import random


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    return render_template('home.html', title='Home')


@app.route("/")
@app.route("/feed")
def feed():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=current_user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    if current_user.requests.count() > 0:
        flash('Você tem solicitações de amizade pendente. Favor entrar em sua conta para responde-las!')
    return render_template('feed.html', posts=posts)


@app.route('/interests/<string:username>', methods=['GET', 'POST'])
def interests(username):
    form = UserInterestForm()
    user = User.query.filter_by(username=username).first_or_404()     

    if request.method == 'POST':
        interests = request.form.getlist('interests')
        
        user_interest = InterestTopicUser.query.filter_by(user_id=user.id)

        for u in user_interest:
            db.session.delete(u)

        for i in interests:
            interest = InterestTopic.query.filter_by(label=i).first_or_404()
            userInterest = InterestTopicUser(topic=interest, interested=user)
            db.session.add(userInterest)

        db.session.commit()
        return redirect(url_for('home'))

    elif request.method == 'GET':        
        user_interest = InterestTopicUser.query.filter_by(interested=user)
        user_interest_list = []
        for u in user_interest:
            user_interest_list.append(u.topic_id)        
        interests = InterestTopic.query.all()
        image_file = url_for(
        'static', filename='profile_pics/' + user.image_file)
        return render_template('interest.html', interests=interests, user_interest=user_interest_list, user=user, image_file=image_file, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, data_nasc=form.data_nasc.data, start_work_date=form.start_work_date.data, work_state=form.work_state.data,
                    work_city=form.work_city.data, number_friends=0, salary=form.salary.data, instruction=form.instruction.data, company=form.company.data, card_number=0, card_name='', expiration_date='', cvv='', user_type='free')
        db.session.add(user)
        db.session.commit()
        flash('Sua conta acaba de ser criada. Você já pode acessar o sistema!', 'success')        
        return redirect(url_for('interests', username=user.username))
    return render_template('register.html', title='Registro', form=form)


@app.route("/register_premium", methods=['GET', 'POST'])
def register_premium():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = RegistrationFormPremium()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, data_nasc=form.data_nasc.data, start_work_date=form.start_work_date.data, work_state=form.work_state.data, work_city=form.work_city.data,
                    salary=form.salary.data, number_friends=0, instruction=form.instruction.data, company=form.company.data, card_number=form.card_number.data, card_name=form.card_name.data, expiration_date=form.expiration_date.data, cvv=form.cvv.data, user_type='premium')
        db.session.add(user)
        db.session.commit()
        flash('Sua conta acaba de ser criada. Você já pode acessar o sistema!', 'success')
        return redirect(url_for('interests', username=user.username))
    return render_template('register_premium.html', title='Conta Premium', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Falha no Login. Por favor cheque seu email e senha!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.data_nasc = form.data_nasc.data
        current_user.start_work_date = form.start_work_date.data
        current_user.work_state = form.work_state.data
        current_user.work_city = form.work_city.data
        current_user.salary = form.salary.data
        current_user.instruction = form.instruction.data
        current_user.company = form.company.data
        current_user.card_number = form.card_number.data
        current_user.card_name = form.card_name.data
        current_user.expiration_date = form.expiration_date.data
        current_user.cvv = form.cvv.data
        db.session.commit()
        flash('Sua conta foi atualizada com sucesso!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.data_nasc.data = current_user.data_nasc
        form.start_work_date.data = current_user.start_work_date
        form.work_state.data = current_user.work_state
        form.work_city.data = current_user.work_city
        form.salary.data = current_user.salary
        form.instruction.data = current_user.instruction
        form.company.data = current_user.company
        form.card_number.data = current_user.card_number
        form.card_name.data = current_user.card_name 
        form.expiration_date.data = current_user.expiration_date 
        form.cvv.data = current_user.cvv
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Sua publicação foi criada!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Sua publicação foi atualizada!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend="Update Post")


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Sua publicação foi deletada!', 'success')
    return redirect(url_for('home'))


@app.route("/user_posts/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    if user.is_requesting(current_user):
        flash("Este usúario solicitiou amizade com você! Responda sua solicitação")
    return render_template('user_posts.html', posts=posts, user=user, image_file=image_file)

@app.route("/user_interests/<string:username>")
def user_interests(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    interests = InterestTopicUser.query.filter_by(interested=user).paginate(page=page, per_page=5) 
    return render_template('user_interests.html', user=user, interests=interests ,image_file=image_file)

@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    form = SearchUserForm()
    user = User.query.filter_by(username=form.username.data).first()
    if user is None:        
        flash('Usuario não existe', category="message")
        return redirect(url_for('feed'))
    return redirect(url_for('user_posts', username=user.username))

@app.route('/recommend/<nickname>')
@login_required
def recommend(nickname):
    user = User.query.filter_by(username=nickname).first_or_404()
    if user is None:
        flash('Usúario %s não foi encontrado.' % nickname)
        return redirect(url_for('feed'))
    current_user.recommend(user)
    db.session.commit()
    flash('Você recomendou ' + nickname + '!')
    return redirect(url_for('user_posts', username=nickname))

@app.route('/unrecommend/<nickname>')
@login_required
def unrecommend(nickname):
    user = User.query.filter_by(username=nickname).first_or_404()
    if user is None:
        flash('Usúario %s não foi encontrado.' % nickname)
        return redirect(url_for('feed'))
    if user == current_user:
        flash('Você não pode desrecomendar você mesmo!')
        return redirect(url_for('feed'))
    current_user.unrecommend(user)
    db.session.commit()
    flash('Você não está recomendando {} mais'.format(nickname))
    return redirect(url_for('user_posts', username=nickname))

@app.route('/make_request/<nickname>')
@login_required
def make_request(nickname):
    user = User.query.filter_by(username=nickname).first_or_404()
    if user is None:
        flash('Usúario %s não foi encontrado.' % nickname)
        return redirect(url_for('feed'))
    current_user.request(user)
    db.session.commit()
    flash('Você solicitou amizado com ' + nickname + '!')
    return redirect(url_for('user_posts', username=nickname))

@app.route('/unrequest/<nickname>')
@login_required
def unrequest(nickname):
    user = User.query.filter_by(username=nickname).first_or_404()
    if user is None:
        flash('Usúario %s não foi encontrado.' % nickname)
        return redirect(url_for('feed'))
    if user == current_user:
        flash('Você não pode remover uma solicitação de amizade com você mesmo!')
        return redirect(url_for('feed'))
    current_user.unrequest(user)
    db.session.commit()
    flash('Você não está mais solicitando amizade com {} mais'.format(nickname))
    return redirect(url_for('user_posts', username=nickname))

@app.route('/accept_friendship/<nickname>')
@login_required
def accept_friendship(nickname):
    user = User.query.filter_by(username=nickname).first_or_404()
    if user is None:
        flash('Usúario %s não foi encontrado.' % nickname)
        return redirect(url_for('feed'))
    current_user.become_friend(user)
    db.session.commit()
    user.become_friend(current_user)
    db.session.commit()
    current_user.unrequest(user)
    db.session.commit()
    user.unrequest(current_user)
    db.session.commit()
    user.number_friends += 1
    current_user.number_friends += 1
    db.session.commit()
    flash('Você virou amigo de ' + nickname + '!')
    return redirect(url_for('friend_requests', username=current_user.username))   

@app.route('/deny_friendship/<nickname>')
@login_required
def deny_friendship(nickname):
    user = User.query.filter_by(username=nickname).first_or_404()
    if user is None:
        flash('Usúario %s não foi encontrado.' % nickname)
        return redirect(url_for('feed'))
    user.unrequest(current_user)
    current_user.unrequest(user)
    db.session.commit()
    flash('Você negou a solicitação de amizade de {}'.format(nickname))
    return redirect(url_for('friend_requests', username=current_user.username))

@app.route('/unfriend/<nickname>')
@login_required
def unfriend(nickname):
    user = User.query.filter_by(username=nickname).first_or_404()
    if user is None:
        flash('Usúario %s não foi encontrado.' % nickname)
        return redirect(url_for('feed'))
    if user == current_user:
        flash('Você não pode desfazer a amizade com você mesmo!')
        return redirect(url_for('feed'))
    current_user.unfriend(user)
    user.unfriend(current_user)
    user.number_friends -= 1
    current_user.number_friends -= 1
    db.session.commit()
    flash('Você não é mais amigo de {}'.format(nickname))
    return redirect(url_for('user_posts', username=nickname))

@app.route("/friend_requests/<string:username>")
def friend_requests(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename='profile_pics/' + user.image_file)  
    user_requests = user.requests    
    requester_list = []     
    for ur in user_requests:    
        requester_list.append(ur.id)
    all_requests = User.query.filter(User.id.in_(requester_list)).paginate(page=page, per_page=5)
    return render_template('friend_requests.html', requests=all_requests, user=user, image_file=image_file)

@app.route("/user_friends/<string:username>")
def user_friends(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    user_friends = user.friends    
    friends_list = []     
    for fl in user_friends:    
        friends_list.append(fl.id)
    all_friends = User.query.filter(User.id.in_(friends_list)).paginate(page=page, per_page=5)  
    return render_template('user_friends.html', friends=all_friends, user=user, image_file=image_file)

@app.route("/charts")
def chart():
    if current_user.username != 'admin':
        return redirect(url_for('feed'))
    legend_1 = 'Porcentagem de membros'
    labels_1 = ['','','','']
    values_1 = [0,0,0,0]
    colors_1 = []

    for c in range(len(values_1)):        
        colors_1.append("rgba(" + str(random.randint(0,250)) + "," + str(random.randint(0,250)) + "," + str(random.randint(0,250)) + ")")

    number_friends = 0
    number_users = 0    

    users = User.query.all()
    for user in users:
        number_friends += user.number_friends
        number_users += 1   

    if number_users != 0:
        media = number_friends/number_users
        values_1[0] = int(media/2)
        labels_1[0] = 'Menos de ' + str(values_1[0]) + ' amigos'
        values_1[1] = int(media)
        labels_1[1] = 'Entre ' + str(values_1[0]) + ' e ' + str(values_1[1]) +' amigos'
        values_1[2] = int(media + (media/2))
        labels_1[2] = 'Entre ' + str(values_1[1]) + ' e ' + str(values_1[2]) +' amigos'
        values_1[3] = int(media + media)
        labels_1[3] = 'Mais de ' + str(values_1[3]) + ' amigos'
        
    for i in range(len(values_1)):
        users = User.query.all()
        if i == 0:
            users = User.query.filter(User.number_friends<int((int(media)/2))) 
        elif i == 1:            
            users = User.query.filter(and_(User.number_friends>=int((int(media)/2)), User.number_friends<int(media)))
        elif i == 2:
            users = User.query.filter(and_(User.number_friends>=int(media), User.number_friends<int((int(media) + int(int(media)/2)))))
        elif i == 3:
            users = User.query.filter(and_(User.number_friends>=int((int(media) + (int(media)/2))), User.number_friends<(int(media) + int(media))))
        
        app.logger.info(users.count())
        values_1[i] = 0     
        for user in users:            
            values_1[i] += 1

        values_1[i] = int((values_1[i]*100)/number_users)
    
    app.logger.info(media)
    app.logger.info(values_1)
    
    legend_2 = 'Quantidade de membros conectados'
    labels_2 = []
    values_2 = []
    colors_2 = []
    
    users = User.query.filter_by().order_by(User.number_friends.desc())    
    cont = 0
    for user in users:
        if cont == 10:
            break
        labels_2.append(user.username)
        values_2.append(user.friends.count())
        cont += 1
    
    for c in range(len(values_2)):        
        colors_2.append("rgba(" + str(random.randint(0,250)) + "," + str(random.randint(0,250)) + "," + str(random.randint(0,250)) + ")")


    legend_3 = 'Quantidade de amigos por usúario no estado'
    labels_3 = ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal", "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"]
    values_3 = []
    colors_3 = []

    for c in range(len(labels_3)):        
        colors_3.append("rgba(" + str(random.randint(0,250)) + "," + str(random.randint(0,250)) + "," + str(random.randint(0,250)) + ")")

    for state in labels_3:
        users = User.query.filter_by(work_state=state)
        number_friends = 0
        number_users = 0
        for user in users:
            number_friends += user.number_friends
            number_users += 1

        if number_users != 0:
            values_3.append(number_friends/number_users)    

    return render_template('chart.html',
    values_1=values_1, labels_1=labels_1, legend_1=legend_1, colors_1=colors_1,
    values_2=values_2, labels_2=labels_2, legend_2=legend_2, colors_2=colors_2,
    values_3=values_3, labels_3=labels_3, legend_3=legend_3, colors_3=colors_3
    )
 