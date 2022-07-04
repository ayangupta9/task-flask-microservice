import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="d3dvhdesc9dcrk",
        user="teojdhrltulgou",
        password="7ff81677ef5a62c77222feb563cf33d42214dbe1abfe9419a12fe13931d4b146",
        host="ec2-54-159-22-90.compute-1.amazonaws.com",
        port=5432,
        options="-c search_path=tech-analogy-db,public",
    )
    return conn


TABLE_NAME = "task"


def create_new_task(title, user_id, description=None, task_type=0, link=None):
    print(title, description, task_type, link)
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = """INSERT INTO task (title,description,link,task_type,user_id) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (title, description, link, task_type, user_id)

        cur.execute(insert_query, record_to_insert)
        conn.commit()
        count = cur.rowcount

        cur.close()
        conn.close()

        return f"{count} rows added in task table"
    except (Exception, psycopg2.Error) as error:
        cur.close()
        conn.close()

        return f"Failed to insert record into mobile table {error}"


def get_task_by_id(task_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        get_task_query = """SELECT * FROM task WHERE id = %s """
        cur.execute(get_task_query, [task_id])
        task_row = cur.fetchone()

        cur.close()
        conn.close()
        return task_row

    except (Exception, psycopg2.Error) as error:
        cur.close()
        conn.close()
        return f"Failed to get record from task table\r{error}"


def delete_task_by_id(task_id):
    try:

        conn = get_db_connection()
        cur = conn.cursor()

        delete_query = """DELETE FROM task WHERE id = %s RETURNING *"""
        cur.execute(delete_query, [task_id])
        delete_query_res = cur.fetchone()
        conn.commit()

        count = cur.rowcount

        cur.close()
        conn.close()

        return delete_query_res

    except (Exception, psycopg2.Error) as error:
        cur.close()
        conn.close()

        return f"Failed to insert record into mobile table {error}"


def get_all_tasks_of_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        get_all_tasks_query = """SELECT * FROM task WHERE user_id = %s"""

        cur.execute(get_all_tasks_query, [user_id])
        user_tasks = cur.fetchall()

        print(user_tasks)

        task_data = {
            "todo": [],
            "doing": [],
            "done": [],
        }

        for task in user_tasks:
            if task[-2] == 0:
                task_data["todo"].append(task)
            elif task[-2] == 1:
                task_data["doing"].append(task)
            else:
                task_data["done"].append(task)

        cur.close()
        conn.close()

        return task_data
    except (Exception, psycopg2.Error) as error:
        cur.close()
        conn.close()
        return f"Failed to insert record into mobile table {error}"


def update_task_status(task_id, new_status):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        update_query = """UPDATE task SET task_type = %s WHERE id = %s RETURNING *"""
        cur.execute(update_query, [new_status, task_id])
        update_result = cur.fetchone()

        conn.commit()

        cur.close()
        conn.close()

        return update_result

    except (Exception, psycopg2.Error) as error:
        cur.close()
        conn.close()
        return f"Failed to insert record into mobile table {error}"
