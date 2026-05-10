from db import get_connection
import logging


def add_todo(title):
    """添加一条待办事项，返回 True 表示成功"""
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO todos(title) VALUES(?)", (title,))
        logging.info(f"添加任务成功: {title}")
        return True
    except Exception as e:
        logging.error(f"添加任务时出错: {e}")
        return False


def list_todos():
    """返回所有待办事项的列表，每条是 sqlite3.Row 对象"""
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM todos ORDER BY id"  #查找全部按id排序
            ).fetchall()
        return rows
    except Exception as e:
        logging.error(f"查找任务时出错: {e}")
        return []


def complete_todo(todo_id):
    """将指定 id 的任务标记为已完成，返回 True 表示成功,False 表示找不到或出错"""
    try:
        with get_connection() as conn:
            # 先检查任务是否存在
            row = conn.execute(
                "SELECT * FROM todos WHERE id = ?", (todo_id,)
            ).fetchone()
            if row is None:
                return  False  # 不存在就返回

            # 更新完成状态
            conn.execute(
                "UPDATE todos SET completed = 1 WHERE id = ?", (todo_id,)
            )
        logging.info(f"完成任务成功: id={todo_id}")
        return True         # 成功返回
    except Exception as e:
        logging.error(f"完成任务时出错: {e}")
        return False          # 异常时返


def delete_todo(todo_id):
    """删除指定 id 的任务，返回 True 表示成功,False 表示找不到或出错"""
    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM todos WHERE id = ?", (todo_id,)
            ).fetchone()
            if row is None:
                return False

            conn.execute(
                "DELETE FROM todos WHERE id = ?", (todo_id,)
            )
        logging.info(f"删除任务成功: id={todo_id}")
        return True
    except Exception as e:
        logging.error(f"删除任务时出错: {e}")
        return False


def update_todo(todo_id, new_title):
    """修改指定 id 的任务内容，返回 True 表示成功,False 表示找不到或出错"""
    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM todos WHERE id = ?", (todo_id,)
            ).fetchone()
            if row is None:
                return False

            conn.execute(
                "UPDATE todos SET title = ? WHERE id = ?",
                (new_title,todo_id)   
            )
        logging.info(f"修改任务成功: id={todo_id}, 新内容={new_title}")
        return True
    except Exception as e:
        logging.error(f"修改任务时出错: {e}")
        return False
    
def uncomplete_todo(todo_id):
    try:
        with get_connection() as conn:
            # 先检查任务是否存在
            row = conn.execute(
                "SELECT * FROM todos WHERE id = ?", (todo_id,)
            ).fetchone()
            if row is None:
                return  False  # 不存在就返回

            # 更新完成状态
            conn.execute(
                "UPDATE todos SET completed = 0 WHERE id = ?", (todo_id,)
            )
        logging.info(f"取消完成任务成功: id={todo_id}")
        return True         # 成功返回
    except Exception as e:
        logging.error(f"取消完成任务时出错: {e}")
        return False          # 异常时返