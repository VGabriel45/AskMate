from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

@database_common.connection_handler
def get_data(cursor: RealDictCursor) -> list:
    query = """
            SELECT *
            FROM question
            ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_question_tags(cursor: RealDictCursor, question_id) -> list:
    query = """
            SELECT * FROM tag JOIN question_tag ON question_tag.tag_id = tag.id JOIN question ON question_tag.question_id = question.id WHERE question_tag.question_id = %s"""
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_latest_questions(cursor: RealDictCursor) -> list:
    query = """
            SELECT *
            FROM question
            ORDER BY id DESC FETCH first 5 rows only """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_comment(cursor: RealDictCursor, id) -> list:
    query = """
            SELECT *
            FROM comment
            WHERE question_id = %s"""
    cursor.execute(query, (id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_comment(cursor: RealDictCursor, id) -> list:
    query = """
            SELECT *
            FROM comment
            WHERE answer_id = %s"""
    cursor.execute(query, (id,))
    return cursor.fetchall()


@database_common.connection_handler
def reverse_list(cursor: RealDictCursor) -> list:
    query = """
               SELECT *
               FROM question
               ORDER BY id DESC"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_question_in_csv(cursor: RealDictCursor,submission_time, view_number, vote_number, title, message, image) -> list:
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
    cursor.execute(query, (submission_time, view_number, vote_number, title, message,image,))


@database_common.connection_handler
def add_answer_in_csv(cursor: RealDictCursor,submission_time, vote_number, message, question_id, image) -> list:
    query = """
    INSERT INTO answer (submission_time, vote_number, message, question_id, image)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(query, (submission_time, vote_number, message, question_id, image,))


@database_common.connection_handler
def add_tag_in_csv(cursor: RealDictCursor, name) -> list:
    query = """
    INSERT INTO tag (name)
    VALUES (%s);
    """
    cursor.execute(query, (name,))


@database_common.connection_handler
def add_tag_in_question_tag(cursor: RealDictCursor, question_id, tag_id) -> list:
    query = """
    INSERT INTO question_tag (question_id, tag_id)
    VALUES (%s, %s);
    """
    cursor.execute(query, (question_id, tag_id,))


@database_common.connection_handler
def add_comment_for_question(cursor: RealDictCursor,question_id, message, submission_time) -> list:
    query = """
    INSERT INTO comment (question_id, message, submission_time)
    VALUES (%s, %s, %s);
    """
    cursor.execute(query, (question_id ,message, submission_time,))


@database_common.connection_handler
def add_comment_for_answer(cursor: RealDictCursor,answer_id, message, submission_time) -> list:
    query = """
    INSERT INTO comment (answer_id, message, submission_time)
    VALUES (%s, %s, %s);
    """
    cursor.execute(query, (answer_id ,message, submission_time,))


@database_common.connection_handler
def update_question_on_csv(cursor: RealDictCursor, title, message, image, id) -> list:
    query = """
        UPDATE question
        SET title = %s , message = %s , image = %s
        WHERE id = %s;
        """
    cursor.execute(query, (title, message, image, id,))


@database_common.connection_handler
def update_answer_on_csv(cursor: RealDictCursor, message, image, id) -> list:
    query = """
        UPDATE answer
        SET message = %s , image = %s
        WHERE id = %s;
        """
    cursor.execute(query, ( message, image, id,))


@database_common.connection_handler
def update_comment_on_csv(cursor: RealDictCursor, message, id) -> list:
    query = """
        UPDATE comment
        SET message = %s
        WHERE id = %s;
        """
    cursor.execute(query, ( message, id,))


@database_common.connection_handler
def view_up_answer(cursor: RealDictCursor, id) -> list:
    query = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = %s;
        """
    cursor.execute(query, (id,))



@database_common.connection_handler
def edit_comment_count(cursor: RealDictCursor, id) -> list:
    query = """
        UPDATE comment
        SET edited_count = edited_count + 1
        WHERE id = %s;
        """
    cursor.execute(query, (id,))


@database_common.connection_handler
def get_vote_number(cursor: RealDictCursor, id) -> list:
    query = """
        SELECT vote_number FROM question WHERE id = %s;
        """
    cursor.execute(query, (id,))
    return cursor.fetchall()


@database_common.connection_handler
def vote_up_question(cursor: RealDictCursor, id) -> list:
    query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %s;
        """
    cursor.execute(query, (id,))


@database_common.connection_handler
def vote_down_question(cursor: RealDictCursor, id) -> list:
    query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %s;
        """
    cursor.execute(query, (id,))


@database_common.connection_handler
def vote_up_answer(cursor: RealDictCursor, id) -> list:
    query = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %s;
        """
    cursor.execute(query, (id,))


@database_common.connection_handler
def vote_down_answer(cursor: RealDictCursor, id) -> list:
    query = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %s;
        """
    cursor.execute(query, (id,))


@database_common.connection_handler
def delete_question_on_csv(cursor: RealDictCursor, id) -> list:
    query = """
            DELETE FROM question WHERE id = %s;
            """
    cursor.execute(query, (id,))


@database_common.connection_handler
def delete_answer_on_csv(cursor: RealDictCursor, id) -> list:
    query = """
            DELETE FROM answer WHERE id = %s;
            """
    cursor.execute(query, (id,))


@database_common.connection_handler
def delete_comment_on_csv(cursor: RealDictCursor, id) -> list:
    query = """
            DELETE FROM comment WHERE id = %s;
            """
    cursor.execute(query, (id,))


@database_common.connection_handler
def delete_tag_on_csv(cursor: RealDictCursor, id) -> list:
    query = """
            DELETE FROM tag WHERE id = %s;
            """
    cursor.execute(query, (id,))


@database_common.connection_handler
def find_question(cursor: RealDictCursor, id) -> list:
    query = """
            SELECT * FROM question WHERE id = %s
            """
    cursor.execute(query, (id,))
    return cursor.fetchall()


@database_common.connection_handler
def find_answers(cursor: RealDictCursor, id) -> list:
    query = """
                SELECT * FROM answer WHERE id = %s
                """
    cursor.execute(query, (id,))
    return cursor.fetchall()


@database_common.connection_handler
def sort_csv(cursor: RealDictCursor, param, direction) -> list:
    query = """
            SELECT * FROM question ORDER BY {} {}
            """.format(param, direction)
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def find_question_answer(cursor: RealDictCursor, question_id) -> list:
    query = """
                SELECT * FROM answer WHERE question_id = %s
                """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()

@database_common.connection_handler
def find_id_question_answer(cursor: RealDictCursor, question_id) -> list:
    query = """
                SELECT id FROM answer WHERE question_id = %s
                """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_comments(cursor: RealDictCursor) -> list:
    query = """
                SELECT * FROM comment ORDER BY submission_time;
                """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor: RealDictCursor, id) -> list:
    query = """
                SELECT * FROM comment WHERE id = %s
                """
    cursor.execute(query, (id,))
    return cursor.fetchall()


@database_common.connection_handler
def get_tag_id(cursor: RealDictCursor, name) -> list:
    query = """
                SELECT id FROM tag WHERE name = %s
                """
    cursor.execute(query, (name,))
    return cursor.fetchone()


@database_common.connection_handler
def search_questions(cursor: RealDictCursor, title) -> list:
    query = """
                SELECT * FROM question WHERE title ILIKE '%{}%' OR message ILIKE '%{}%'
                """.format(title, title)
    cursor.execute(query)
    return cursor.fetchall()