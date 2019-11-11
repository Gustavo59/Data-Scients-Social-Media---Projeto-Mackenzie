from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from webapp_social_media.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Escolha um nome de usuário. Você pode alterar isso mais tarde!',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Endereço de E-mail',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirme sua senha', validators=[
                                     DataRequired(), EqualTo('password')])
    data_nasc = StringField('Data de nascimento (dd/mm/aaaa)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    start_work_date = StringField('Data de início de trabalho com ciência de dados (dd/mm/aaaa)',
                                  validators=[DataRequired(), Length(min=2, max=20)])
    work_state = SelectField('Estado onde você trabalha',choices=[("Acre","Acre"),("Alagoas","Alagoas"),("Amapá","Amapá"),("Amazonas","Amazonas"),("Bahia","Bahia"),("Ceará","Ceará"),("Distrito Federal","Distrito Federal"),("Espírito Santo","Espírito Santo"),("Goiás","Goiás"),("Maranhão","Maranhão"),("Mato Grosso","Mato Grosso"),("Mato Grosso do Sul","Mato Grosso do Sul"),("Minas Gerais","Minas Gerais"),("Pará","Pará"),("Paraíba","Paraíba"),("Paraná","Paraná"),("Pernambuco","Pernambuco"),("Piauí","Piauí"),("Rio de Janeiro","Rio de Janeiro"),("Rio Grande do Norte","Rio Grande do Norte"),("Rio Grande do Sul","Rio Grande do Sul"),("Rondônia","Rondônia"),("Roraima","Roraima"),("Santa Catarina","Santa Catarina"),("São Paulo","São Paulo"),("Sergipe","Sergipe"),("Tocantins","Tocantins")],
                             validators=[DataRequired()])
    work_city = StringField('Cidade onde você trabalha',
                            validators=[DataRequired(), Length(min=2, max=40)])
    salary = FloatField('Seu salário atual',
                        validators=[DataRequired()])
    instruction = SelectField('Seu nível de instrução',choices=[("Ensino Fundamental Incompleto","Ensino Fundamental Incompleto"),("Ensino Fundamental Completo","Ensino Fundamental Completo"),("Ensino Médio Incompleto","Ensino Médio Incompleto"),("Ensino Médio Completo","Ensino Médio Completo"),("Ensino Superior Completo","Ensino Superior Completo"),("Ensino Superior Incompleto","Ensino Superior Incompleto"),("Pós-Graduação","Pós-Graduação"),("Mestrado","Mestrado"),("Doutorado","Doutorado")],
                              validators=[DataRequired()])
    company = StringField('Nome da empresa que você trabalha atualmente',
                          validators=[DataRequired()])
    submit = SubmitField('Criar conta')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class RegistrationFormPremium(FlaskForm):
    username = StringField('Escolha um nome de usuário. Você pode alterar isso mais tarde!',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Endereço de E-mail',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirme sua senha', validators=[
                                     DataRequired(), EqualTo('password')])
    data_nasc = StringField('Data de nascimento (dd/mm/aaaa)',
                            validators=[DataRequired(), Length(min=2, max=20)])
    start_work_date = StringField('Data de início de trabalho com ciência de dados (dd/mm/aaaa)',
                                  validators=[DataRequired(), Length(min=2, max=20)])
    work_state = SelectField('Estado onde você trabalha',choices=[("Acre","Acre"),("Alagoas","Alagoas"),("Amapá","Amapá"),("Amazonas","Amazonas"),("Bahia","Bahia"),("Ceará","Ceará"),("Distrito Federal","Distrito Federal"),("Espírito Santo","Espírito Santo"),("Goiás","Goiás"),("Maranhão","Maranhão"),("Mato Grosso","Mato Grosso"),("Mato Grosso do Sul","Mato Grosso do Sul"),("Minas Gerais","Minas Gerais"),("Pará","Pará"),("Paraíba","Paraíba"),("Paraná","Paraná"),("Pernambuco","Pernambuco"),("Piauí","Piauí"),("Rio de Janeiro","Rio de Janeiro"),("Rio Grande do Norte","Rio Grande do Norte"),("Rio Grande do Sul","Rio Grande do Sul"),("Rondônia","Rondônia"),("Roraima","Roraima"),("Santa Catarina","Santa Catarina"),("São Paulo","São Paulo"),("Sergipe","Sergipe"),("Tocantins","Tocantins")],
                             validators=[DataRequired()])
    work_city = StringField('Cidade onde você trabalha',
                            validators=[DataRequired(), Length(min=2, max=20)])
    salary = FloatField('Seu salário atual',
                        validators=[DataRequired()])
    instruction = SelectField('Seu nível de instrução',choices=[("Ensino Fundamental Incompleto","Ensino Fundamental Incompleto"),("Ensino Fundamental Completo","Ensino Fundamental Completo"),("Ensino Médio Incompleto","Ensino Médio Incompleto"),("Ensino Médio Completo","Ensino Médio Completo"),("Ensino Superior Completo","Ensino Superior Completo"),("Ensino Superior Incompleto","Ensino Superior Incompleto"),("Pós-Graduação","Pós-Graduação"),("Mestrado","Mestrado"),("Doutorado","Doutorado")],
                              validators=[DataRequired()])
    company = StringField('Nome da empresa que você trabalha atualmente',
                          validators=[DataRequired()])
    card_number = FloatField('Número do cartão de crédito',
                             validators=[DataRequired()])
    card_name = StringField('Nome no cartão de crédito',
                            validators=[DataRequired(), Length(min=2, max=20)])
    expiration_date = StringField('Data de validade',
                                  validators=[DataRequired(), Length(min=2, max=20)])
    cvv = StringField('Código de Verificacao - CVV',
                      validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Criar conta')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nome de usuário',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    data_nasc = StringField('Data de nascimento', validators=[
                            DataRequired(), Length(min=2, max=20)])
    start_work_date = StringField('Data de início de trabalho com ciência de dados', validators=[
                                  DataRequired(), Length(min=2, max=20)])
    work_state = SelectField('Estado onde você trabalha',choices=[("Acre","Acre"),("Alagoas","Alagoas"),("Amapá","Amapá"),("Amazonas","Amazonas"),("Bahia","Bahia"),("Ceará","Ceará"),("Distrito Federal","Distrito Federal"),("Espírito Santo","Espírito Santo"),("Goiás","Goiás"),("Maranhão","Maranhão"),("Mato Grosso","Mato Grosso"),("Mato Grosso do Sul","Mato Grosso do Sul"),("Minas Gerais","Minas Gerais"),("Pará","Pará"),("Paraíba","Paraíba"),("Paraná","Paraná"),("Pernambuco","Pernambuco"),("Piauí","Piauí"),("Rio de Janeiro","Rio de Janeiro"),("Rio Grande do Norte","Rio Grande do Norte"),("Rio Grande do Sul","Rio Grande do Sul"),("Rondônia","Rondônia"),("Roraima","Roraima"),("Santa Catarina","Santa Catarina"),("São Paulo","São Paulo"),("Sergipe","Sergipe"),("Tocantins","Tocantins")],
                             validators=[DataRequired()])
    work_city = StringField('Cidade onde você trabalha', validators=[
                            DataRequired(), Length(min=2, max=20)])
    salary = FloatField('Seu salário atual', validators=[DataRequired()])
    instruction = SelectField('Seu nível de instrução',choices=[("Ensino Fundamental Incompleto","Ensino Fundamental Incompleto"),("Ensino Fundamental Completo","Ensino Fundamental Completo"),("Ensino Médio Incompleto","Ensino Médio Incompleto"),("Ensino Médio Completo","Ensino Médio Completo"),("Ensino Superior Completo","Ensino Superior Completo"),("Ensino Superior Incompleto","Ensino Superior Incompleto"),("Pós-Graduação","Pós-Graduação"),("Mestrado","Mestrado"),("Doutorado","Doutorado")],
                              validators=[DataRequired()])
    company = StringField('Nome da empresa que você trabalha atualmente', validators=[
                          DataRequired(), Length(min=2, max=40)])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])    
    card_number = FloatField('Número do cartão de crédito')
    card_name = StringField('Nome no cartão de crédito')
    expiration_date = StringField('Data de validade')
    cvv = StringField('Código de Verificacao - CVV')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Conteúdo', validators=[DataRequired()])
    submit = SubmitField('Publicar')

class UserInterestForm(FlaskForm):    
    submit = SubmitField('Post')

class SearchUserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    submit = SubmitField('Post')

