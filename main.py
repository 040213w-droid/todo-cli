
import logging
from db import init_db
import crud

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("data.log", mode='w', encoding='utf-8'),
    ]
)

# 初始化数据库
init_db()

menu = """
***************** 待办事项 *******************
    1. 添加事项
    2. 查看所有任务
    3. 完成任务
    4. 删除任务
    5. 修改任务内容
    6. 退出
    7.取消完成任务
**********************************************
"""

print(menu)

while True:
    choice = input("请输入你想要的操作：")
    if choice == '1':
        title = input("请输入新的待办事项：")
        if crud.add_todo(title):    #返回True 或者 False
            print("✅ 添加成功！")
        else:
            print("❌ 添加失败，请查看日志。")

    elif choice == '2':
        todos = crud.list_todos()
        if not todos:
            print("📭 暂无待办事项。")
        else:
            for row in todos:
                status = "✓ 已完成" if row['completed'] else "✗ 未完成"   #Python 里0等于False，1等于True所以if row['completed']
                print(f"ID:{row['id']} | {row['title']} | {status} | 创建时间:{row['created_at']}")
    
    elif choice == '3':
        todo_id = input("请输入要完成的任务ID：")
        if not todo_id.isdigit():
            print("⚠️ 请输入数字ID。")
            continue
        if crud.complete_todo(int(todo_id)):
            print("✅ 标记完成！")
        else:
            print("❌ 未找到该任务或操作失败。")
    
    elif choice == '4':
        todo_id = input("请输入要删除的任务ID：")
        if not todo_id.isdigit():
            print("⚠️ 请输入数字ID。")
            continue
        # 先查一下任务内容
        todos = crud.list_todos()   #从数据库查出所有待办事项返回一个列表，每个元素都是像字典一样的 Row 对象
        target = None
        for t in todos:
            if t['id'] == int(todo_id):
                target = t
                break
        if target is None:
            print("❌ 未找到该任务。")
            continue
        confirm = input(f"是否删除任务：{target['title']} (y/n)：")
        if confirm.lower() == 'y':
            if crud.delete_todo(int(todo_id)):    #调用完会返回True或者False
                print("✅ 删除成功！")
            else:
                print("❌ 删除失败。")
        else:
            print("已取消删除。")
    
    elif choice == '5':
        todo_id = input("请输入要修改的任务ID：")
        if not todo_id.isdigit():
            print("⚠️ 请输入数字ID。")
            continue
        # 先查一下原内容
        todos = crud.list_todos()
        target = None  #是“标记变量”，表示“还没找到匹配的任务”
        for t in todos:
            if t['id'] == int(todo_id):
                target = t
                break
        if target is None:
            print("❌ 未找到该任务。")
            continue
        print(f"当前内容：{target['title']}")
        new_title = input("请输入新内容：")
        if crud.update_todo(int(todo_id), new_title):
            print("✅ 修改成功！")
        else:
            print("❌ 修改失败。")
    
    elif choice == '6':
        print("感谢使用，再见！")
        break
    
    elif choice == '7':
        todo_id = input("请输入要取消完成任务的id:")
        if not todo_id.isdigit():
            print("请输入有效数字")
            continue
        if crud.uncomplete_todo(int(todo_id)):
            print(f"取消完成成功{todo_id}")
        else:
            print("取消失败")



    else:
        print("⚠️ 输入错误,请输入1-7之间的数字。")