from uuid import uuid4
from fastapi.param_functions import Cookie
#from pydantic.errors import NoneIsAllowedError
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime,timezone
from gino import Gino
import os


db = Gino()
import hashlib

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# some_engine = create_engine('postgresql://scott:tiger@localhost/')

try:
    from main import db
except:
    import sys
    sys.path.insert(1, '../')
    from database import db
class User(db.Model) :
    __tablename__ = 'users'
    id: int = db.Column(db.Integer, primary_key=True ,autoincrement=True) 
    login: str = db.Column(db.String,default='-')
    email: str = db.Column(db.String,default='-')
    phone: str = db.Column(db.String,default='-')
    role: str = db.Column(db.String,default='-')
    name: str = db.Column(db.String,default='-')
    admission_year:str = db.Column(db.String,default='-')
    course: int = db.Column(db.Integer,default='-')
    direction: str = db.Column(db.String,default='-')
    group: str = db.Column(db.String,default='-')
    hostel: str = db.Column(db.String,default='-')
    password: str = db.Column(db.String,default='-')
    zachetkaid : str = db.Column(db.String,default='-')
    @classmethod
    async def create_user(cls,login,email,phone,role,name, admission_year, course,direction,group,hostel,password,zachetkaid) -> "User":
        hash_password = hashlib.sha256(password.encode())
        if role == 'student':
            await Zachetka.create_zachetka(zachetkaid=zachetkaid,userId=email,name=name)
            #zachetkaid = zachetkaid.zachetkaid
            user = await cls.create(login=login,email=email,phone=phone,role=role,name=name, 
            admission_year=admission_year, course=course,direction=direction,group=group
            ,hostel=hostel,password=str(hash_password.hexdigest()),zachetkaid=zachetkaid)
        else:
            user = await cls.create(login=login,email=email,phone=phone,role=role,name=name, 
            admission_year=admission_year, course=course,direction=direction,group=group
            ,hostel=hostel,password=str(hash_password.hexdigest()))
        return user
    @classmethod
    async def check_password(cls,email,password)-> "User":
        pass_user = await User.query.where(User.email==email).gino.first()
        if pass_user is not None:
            pass_user = pass_user.password 
            if pass_user == password:
                return True
            else:
                return False
        else: 
            return False
    @classmethod
    async def get_role(cls,username) -> "User": 
        user = await cls.query.where(User.email == username).gino.first()
        role = user.role
        return role
    @classmethod
    async def get_user_for_email(cls,email) -> "User":
        user = await cls.query.where(User.email == email).gino.first()
        if user is not None:

            return user
        else:
            return None 
    @classmethod 
    async def get_name(cls,email) -> "User":
        user = await cls.query.where(User.email == email).gino.first()
        name = user.name
        return name
class Messages(db.Model):
    __tablename__ = 'messages'
    id:  int = db.Column(db.Integer, primary_key=True,autoincrement=True)
    chat_id : int =  db.Column(db.Integer,default=0)
    message_id : int =  db.Column(db.Integer,default=0,autoincrement=True)
    sender:str = db.Column(db.String, default='-')
    text: str = db.Column(db.Text,default='')
    date = db.Column(db.DateTime())
    @classmethod
    async def up_message(cls,chat_id,sender,text):
        date = datetime.now()
        return await cls.create(chat_id=chat_id,sender=sender,text=text,date = date)
    @classmethod
    async def get_message(cls,id):
        return await cls.get(id)
class Dialogs(db.Model): 
    __tablename__ = 'dialogs'
    id:  int = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    sender_1: str =  db.Column(db.String,default='-')
    sender_2: str =  db.Column(db.String,default='-')
    dialog: db.Column(JSON, nullable=False, server_default="{}")
    
    @classmethod
    async def get_or_create(cls,sender_1,sender_2)-> "Dialogs":
        dialog = await Dialogs.query.where(Dialogs.sender_1 == sender_1 and Dialogs.sender_2== sender_2).gino.first()
        if dialog is None:
            dialog  = await Dialogs.query.where(Dialogs.sender_1 == sender_2 and Dialogs.sender_1== sender_2).gino.first()
            if dialog is None:
                dialog = await cls.create(sender_1 = sender_1 , sender_2 = sender_2)
        return dialog
   
    @classmethod
    async def up_message(cls,sender_1,sender_2,message)-> "Messages":
        dialog = await Dialogs.get_or_create(sender_1=sender_1,sender_2=sender_2)
        new = await Messages.up_message(dialog.id,sender_1,message)
        return new

    async def get_dialog(sender_1,sender_2)-> "Messages":
        dialog = await Dialogs.get_or_create(sender_1=sender_1,sender_2=sender_2)
        messages = await Messages.query.where(Messages.chat_id==dialog.id).gino.all()
        return messages

class Cookies(db.Model): 
    __tablename__ = 'cookies'
    value: str =  db.Column(db.String,primary_key=True)
    userId: str = db.Column(db.String, default='-')

    date = db.Column(db.DateTime())
    @classmethod
    async def get_or_create(cls,userId,value)-> "Cookies":
        cookie_token = await cls.get(value)
        if cookie_token is None:
            date = datetime.now()
            return await cls.create(value=value,userId=userId,date=date)
        else:
            #print(cookie_token.__dict__)
            return await cookie_token
            datetimes = cookie_token.__dict__
            datetimes = datetimes["__values__"]
            datetimes = datetimes["date"]
            print(datetimes)

            date = datetime.now()
            # date_cookies = cookie_token.date
            # period = date - date_cookies
            # if int(period.days) > 7:
            #     return "Token is no valid"
            # else:
            #     return cls.get(value)
    @classmethod
    async def get_cookie(cls,value) -> "Cookies":
        await Cookies.delete_not_valid_token()
        cookie_token = await cls.get(value)
        if cookie_token is None:
            return 504
        else:
            return cookie_token
    @classmethod
    async def delete_not_valid_token(cls) -> "Cookies":
        cookies = await cls.query.gino.all()
        print(cookies)
        date = datetime.now()
        for i in cookies:
            date_cookies = i.date
            print(date_cookies)
            period = date - date_cookies
            if int(period.days) > 7:
                await cls.delete.where(Cookies.value == i.value).gino.status()
    @classmethod 
    async def delete_cookie(cls,value) -> "Cookies":
        ##cls.delete.where(Cookies.value == value).gino.status()
        return await cls.delete.where(Cookies.value == value).gino.status()
                

class Dopusk_submissions(db.Model): 
    __tablename__ = 'dopusk_submissions'
    id:  int = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    student: str =  db.Column(db.String,default='-')
    teacher: str =  db.Column(db.String,default='-')
    subject: str =  db.Column(db.String,default='-')
    status_author: str = db.Column(db.String,default='-')
    semestr: int = db.Column(db.Integer)
    status: str =  db.Column(db.String,default='Получено')
    date = db.Column(db.DateTime())
    
 

    @classmethod
    async def get_or_create_dopusk(cls,student,subject,teacher,status_author,semestr)-> "Dopusk_submissions":
        date = datetime.now()
        dopusk = await cls.query.where(cls.student == student).gino.all()
        if dopusk is not None:
            for i in dopusk:
                dopusk_subject = i.subject
                if dopusk_subject == subject:
                    return i
            return await cls.create(student=student,subject=subject,teacher=teacher,status_author=status_author,date = date,semestr=semestr)
        if dopusk is None:
            return await cls.create(student=student,subject=subject,teacher=teacher,status_author=status_author,date = date,semestr=semestr)

    @classmethod
    async def update_spravka(cls,student,subject,teacher,new_status,status_author):
       #dopusk = await Dopusk_submissions.get_or_create_dopusk(student,subject,teacher,status_author)
        #print(dopusk)
        dopusk = await cls.query.where(Dopusk_submissions.student == student and Dopusk_submissions.subject == subject and Dopusk_submissions.teacher == teacher).gino.first()
        if dopusk is not None:
            new_dopusk_status = await dopusk.update(status=new_status).apply()
            new_status_author = await dopusk.update(status_author=status_author).apply()
            new_time = await dopusk.update(date = datetime.now()).apply()
            return dopusk
        if dopusk is None:
            return "dopusk is none"
        return 
    @classmethod
    async def get_dopusk_of_user(cls,student):
        dopusk = await cls.query.where(Dopusk_submissions.student == student).gino.all()
        return dopusk
    @classmethod
    async def get_all(cls):
        return await cls.query.gino.all()

    @classmethod
    async def update_status(cls,id,new_status):
        dopusk = await cls.get(id)
        if dopusk is not None:
            if new_status == 'got':
                new_status = 'Готово'
            elif new_status == "obrab":
                new_status = 'Обрабатывается'
            elif new_status == 'pol':
                new_status = 'Получено'
            new_dopusk_status = await dopusk.update(status = new_status).apply()
            new_time = await dopusk.update(date = datetime.now()).apply()
            return dopusk
        else:
            return "dopusk id none"
 


class Spravka_submissions(db.Model): 
    __tablename__ = 'spravka_submissions'
    id:  int = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    student: str =  db.Column(db.String,default='-')
    way_point: str =  db.Column(db.String,default='-')
    status_author: str = db.Column(db.String,default='-')
    quantity: int = db.Column(db.Integer,default=0)
    status: str =  db.Column(db.String,default='Получено')
    date = db.Column(db.DateTime())
    @classmethod
    async def get_or_create_spravka(cls,student,way_point,quantity,status_author)-> "Spravka_submissions":
        date = datetime.now()
        spravka = await cls.query.where(cls.student == student).gino.all()
        if spravka is not None:
            for i in spravka:
                spravka_way_piont = i.way_point
                if spravka_way_piont == way_point:
                    return i
            return await cls.create(student=student,way_point=way_point,quantity=quantity,status_author=status_author,date = date)
        if spravka is None:
            return await cls.create(student=student,way_point=way_point,quantity=quantity,status_author=status_author,date=date)

    @classmethod
    async def update_spravka(cls,student,way_point,quantity,new_status,status_author):
        spravka = await Spravka_submissions.get_or_create_spravka(student,way_point,quantity,status_author)
        print(spravka)
        new_spravka_status = await spravka.update(status=new_status).apply()
        new_status_author = await spravka.update(status_author=status_author).apply()
        return 

    @classmethod
    async def get_all(cls):
        return await cls.query.gino.all()    
    @classmethod
    async def get_spravka_of_user(cls,student):
        spravka = await cls.query.where(Spravka_submissions.student == student).gino.all()
        return spravka
    @classmethod
    async def update_status(cls,id,new_status):
        spravka = await cls.get(id)
        if spravka is not None:
            if new_status == 'got':
                new_status = 'Готово'
            elif new_status == "obrab":
                new_status = 'Обрабатывается'
            elif new_status == 'pol':
                new_status = 'Получено'
            new_spravka_status = await spravka.update(status = new_status).apply()
            new_time = await spravka.update(date = datetime.now()).apply()
            return spravka
        else:
            return "spravka id none"



class Zachetka(db.Model):
    __tablename__ = 'zachetka'
    id : str = db.Column(db.String, primary_key=True)
    userId: str = db.Column(db.String)
    name: str = db.Column(db.String)
    @classmethod
    async def create_zachetka(cls,zachetkaid,userId,name):
        return await cls.create(id=zachetkaid,userId=userId,name=name)
    @classmethod
    async def get_zachetka_name(cls,name):
        return cls.query.where(Zachetka.name==name).gino.first()
    @classmethod 
    async def get_zachetka_userId(cls,userId):
        return cls.query.where(Zachetka.userId == userId).gino.first()
    
class Notes(db.Model):
    __tablename__ = 'notes'
    id : int =  db.Column(db.Integer, primary_key=True ,autoincrement=True)
    zachetkaid: int = db.Column(db.Integer)
    teacher: str =  db.Column(db.String,default='-')
    subject: str =  db.Column(db.String,default='-')
    semestr: str =  db.Column(db.String,default='-')
    note: str =  db.Column(db.String,default='-')

    @classmethod
    async def create_note(cls,zachetkaid,teacher,subject,semestr,note):
        return await cls.create(zachetkaid=int(zachetkaid),teacher=teacher,subject=subject,semestr=semestr,note=note)
    @classmethod
    async def create_note_name(cls,name,teacher,subject,semestr,note):
        student = await User.query.where(User.name == name).gino.first()
        zachetkaid = student.zachetkaid 
        return await cls.create(zachetkaid=int(zachetkaid),teacher=teacher,subject=subject,semestr=semestr,note=note)
    @classmethod
    async def get_notes_of_zachetka(cls,zachetkaid)-> "Notes":
        notes = await cls.query.where(Notes.zachetkaid == int(zachetkaid)).gino.all()
        return notes

class Subject(db.Model):
    __tablename__ = 'subject'
    id : int =  db.Column(db.Integer, primary_key=True ,autoincrement=True)
    teacher: str =  db.Column(db.String,default='-')
    group: str =  db.Column(db.String,default='-')
    subjects: str =  db.Column(db.String,default='-')
    @classmethod
    async def create_s(cls,teacher,group,subjects) -> "Subject":
        return await Subject.create(teacher=teacher,group=group,subjects=subjects)
    @classmethod
    async def get_students(cls,id) -> "Subject":
        group = await cls.get(int(id))
        
        group = group.group
        students = await User.query.where(User.role == 'student'and User.group == group).gino.all()
        return students
    @classmethod
    async def get_subjects(cls,teacher): 
        return await cls.query.where(Subject.teacher == teacher).gino.all()