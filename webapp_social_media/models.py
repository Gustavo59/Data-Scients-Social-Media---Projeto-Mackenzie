from datetime import datetime
from flask import current_app
from webapp_social_media import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


recomendations = db.Table('recomendations',
                          db.Column('recommender_id', db.Integer,
                                    db.ForeignKey('user.id')),
                          db.Column('recommended_id', db.Integer,
                                    db.ForeignKey('user.id'))
                          )

requests = db.Table('requests',
                    db.Column('requester_id', db.Integer,
                              db.ForeignKey('user.id')),
                    db.Column('requested_id', db.Integer,
                              db.ForeignKey('user.id'))
                    )

friends = db.Table('friends',
                   db.Column('friend_id', db.Integer,
                             db.ForeignKey('user.id')),
                   db.Column('your_id', db.Integer,
                             db.ForeignKey('user.id'))
                   )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    data_nasc = db.Column(db.String(120), nullable=False)
    start_work_date = db.Column(db.String(120), nullable=False)
    work_state = db.Column(db.String(120), nullable=False)
    work_city = db.Column(db.String(120), nullable=False)
    salary = db.Column(db.Float(120), nullable=False)
    instruction = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    card_number = db.Column(db.Float(120), nullable=True)
    card_name = db.Column(db.String(120), nullable=True)
    expiration_date = db.Column(db.String(120), nullable=True)
    cvv = db.Column(db.String(120), nullable=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(120), nullable=False)
    number_friends = db.Column(db.Integer, nullable=False)
    interests = db.relationship(
        'InterestTopicUser', backref='interested', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    recommended = db.relationship('User',
                                  secondary=recomendations,
                                  primaryjoin=(
                                      recomendations.c.recommender_id == id),
                                  secondaryjoin=(
                                      recomendations.c.recommended_id == id),
                                  backref=db.backref(
                                      'recomendations', lazy='dynamic'),
                                  lazy='dynamic')
    requested = db.relationship('User',
                                secondary=requests,
                                primaryjoin=(
                                    requests.c.requester_id == id),
                                secondaryjoin=(
                                    requests.c.requested_id == id),
                                backref=db.backref(
                                    'requests', lazy='dynamic'),
                                lazy='dynamic')
    friended = db.relationship('User',
                               secondary=friends,
                               primaryjoin=(
                                   friends.c.friend_id == id),
                               secondaryjoin=(
                                   friends.c.your_id == id),
                               backref=db.backref(
                                   'friends', lazy='dynamic'),
                               lazy='dynamic')

    def recommend(self, user):
        if not self.is_recommending(user):
            self.recommended.append(user)
            return self

    def unrecommend(self, user):
        if self.is_recommending(user):
            self.recommended.remove(user)
            return self

    def is_recommending(self, user):
        return self.recommended.filter(recomendations.c.recommended_id == user.id).count() > 0

    def recommended_posts(self):
        return Post.query.join(recomendations, (recomendations.c.recommended_id == Post.user_id)).filter(recomendations.c.recommender_id == self.id).order_by(Post.date_posted.desc())

    def request(self, user):
        if not self.is_requesting(user):
            self.requested.append(user)
            return self

    def unrequest(self, user):
        if self.is_requesting(user):
            self.requested.remove(user)
            return self

    def is_requesting(self, user):
        return self.requested.filter(requests.c.requested_id == user.id).count() > 0

    def become_friend(self, user):
        if not self.is_friend(user):
            self.friended.append(user)
            return self

    def unfriend(self, user):
        if self.is_friend(user):
            self.friended.remove(user)
            return self

    def is_friend(self, user):
        return self.friended.filter(friends.c.your_id == user.id).count() > 0

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}', '{self.image_file}', '{self.user_type}')"


class InterestTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    users_topics_id = db.relationship('InterestTopicUser',
                                      backref='topic', lazy=True)

    def __repr__(self):
        return f"InterestTopic('{self.label}')"


class InterestTopicUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.String(100), db.ForeignKey(
        'interest_topic.label'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"InterestTopicUser('{self.topic_id}', '{self.user_id}')"
