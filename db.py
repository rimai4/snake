import sqlite3

con = sqlite3.connect("high_scores.db")
cur = con.cursor()
cur.execute(
    "create table if not exists high_scores (id integer primary key autoincrement, name string, score integer)"
)


# this needs to be done in a transaction
def add_high_score(name, score, remove_last=False):
    if remove_last:
        cur.execute(
            "delete from high_scores where id in (select id from high_scores order by score limit 1)"
        )
    cur.execute("insert into high_scores(name, score) values (?, ?)", [name, score])
    con.commit()


def should_delete_last_score():
    cur.execute("select count(*) from high_scores")
    count = cur.fetchone()[0]
    return count == 5


def select_high_scores():
    cur.execute("select score, name from high_scores order by score desc")
    return cur.fetchall()


def is_high_score(score):
    cur.execute("select score from high_scores order by score desc limit 1 offset 4")
    number_5_score_record = cur.fetchone()
    if number_5_score_record:
        number_5_score = number_5_score_record[0]
        return score >= number_5_score
    return True
