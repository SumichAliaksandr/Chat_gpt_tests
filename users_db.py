import os
import random
import sqlite3
from time import sleep

from generator import generate_test, generate_long_answer, generate_parts

column_names = ['id', 'asked', 'number_of_right_answers', 'last_mes_id', 'theme', 'question']

def connection():

    return sqlite3.connect(f"users.db")


def create_users_base():
    if os.path.exists(f"users.db"):
        return
    db = connection()
    cur = db.cursor()
    sql = 'create table users( '+ ', '.join(column_names) + ' )'
    cur.execute(sql)
    db.close()


def user_in_db(user_id):
    db = connection()
    cur = db.cursor()
    cur.execute(f'select id from users where id={user_id}')
    res = cur.fetchone()
    if res:
        return True
    else:
        return False


def new_user(user_id):
    if user_in_db(user_id):
        return

    db = connection()
    cur = db.cursor()
    ques = '?'
    val = [user_id, ]
    for i in range(0, len(column_names) - 1):
        ques += ', ?'
        val.append(0)
    sql = f"INSERT INTO users({', '.join(column_names)}) values ({ques})"
    print(sql, val)
    cur.execute(sql, val)
    db.commit()
    db.close()
    set_question_theme(user_id)


def get_number_of_right_answers(user_id):
    db = connection()
    cur = db.cursor()
    cur.execute(f"select number_of_right_answers from users where id={user_id}")
    res = cur.fetchone()
    db.close()
    try:
        res = res[0]
    except:
        print('No such user')
        res = 0
    return res


def get_question_theme(user_id):
    db = connection()
    cur = db.cursor()
    cur.execute(f"select theme from users where id={user_id}")
    res = cur.fetchone()
    db.close()
    try:
        res = res[0]
    except:
        print('No such user')
        res = 0
    return res

def insert_mes_id(user_id, mes_id):
    db = connection()
    cur = db.cursor()
    cur.execute(f"UPDATE users SET last_mes_id={mes_id} WHERE id={user_id}")
    db.commit()
    db.close()


def get_mes_id(user_id):
    db = connection()
    cur = db.cursor()
    cur.execute(f"select last_mes_id from users where id={user_id}")
    res = cur.fetchone()
    db.close()
    try:
        res = res[0]
    except:
        print('No message yet')
        res = 0
    return res


def increase_number_right_answers(user_id):
    number_right_answers = get_number_of_right_answers(user_id)
    db = connection()
    cur = db.cursor()
    cur.execute(f"UPDATE users SET number_of_right_answers={number_right_answers + 1} WHERE id={user_id}")
    db.commit()
    db.close()

def get_number_of_asked(user_id):
    db = connection()
    cur = db.cursor()
    cur.execute(f"select asked from users where id={user_id}")
    res = cur.fetchone()
    db.close()
    try:
        res = res[0]
    except:
        print('No such user')
        res = 0
    return res


def increase_number_asked(user_id):
    number_right_asked = get_number_of_asked(user_id)
    db = connection()
    cur = db.cursor()
    cur.execute(f"UPDATE users SET asked={number_right_asked + 1} WHERE id={user_id}")
    db.commit()
    db.close()


def set_question_theme(user_id, theme=None):
    print(theme)
    db = connection()
    cur = db.cursor()
    if theme:
        cur.execute(f"UPDATE users SET theme ='{theme}' WHERE id={user_id}")
    else:
        cur.execute(f"UPDATE users SET theme ='Cats' WHERE id={user_id}")
    db.commit()
    db.close()


def get_stat_user(user_id):

    db = connection()
    cur = db.cursor()
    cur.execute(f"select * from users where id={user_id}")
    res = cur.fetchone()
    db.close()
    dct_user = {}
    for i, field in enumerate(column_names):
        dct_user[field] = res[i]
    return dct_user


def set_question(user_id, answer_long):
    print(user_id, answer_long)
    answer_long = answer_long.replace('"', '')
    answer_long = answer_long.replace("'", '`')
    db = connection()
    cur = db.cursor()
    cur.execute(f"UPDATE users SET question='{answer_long}' WHERE id={user_id}")
    db.commit()
    db.close()

def get_question_for(user_id):
    q = get_question_theme(user_id)
    parts = generate_parts(q)

    while True:
        concret_question = q + ' ' + random.choice(parts)
        test = generate_test(concret_question)
        answer = generate_long_answer(test['question'])
        if check_the_same(test['answer'].lower(), answer.lower()) and not \
                check_the_same(test['var1'].lower(), answer.lower()) and not\
                check_the_same(test['var2'].lower(), answer.lower()):
            break
        sleep(2)
    set_question(user_id, answer)
    return test

def check_the_same(answer: str, description: str):
    print(answer, description)
    answer_parts = answer.split()
    count = 0
    for part in answer_parts:
        if part in description:
            count += 1
    if 100 * count/len(answer_parts) > 49:
        return True
    else:
        return False







