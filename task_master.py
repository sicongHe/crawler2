# Encoding:UTF-8
import queue
from multiprocessing.managers import BaseManager
import crawler_master
import sqlite3

task_queue = queue.Queue()

result_queue = queue.Queue()

cookie_queue = queue.Queue()

user_queue = queue.Queue()

pic_queue = queue.Queue()

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
try:
    create = 'create table user(name varchar(40) primary key, '
    create2 = 'agree int, thanks int, favorite int, share int)'
    cursor.execute(create+create2)
    print('Create a new table')
except BaseException:
    print('Find a table')
finally:
    pass

class QueueManager(BaseManager):
    pass

QueueManager.register('get_user_queue', callable=lambda: user_queue)
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
QueueManager.register('get_cookie_queue', callable=lambda: cookie_queue)
QueueManager.register('get_pic_queue', callable=lambda: pic_queue)

manager = QueueManager(address=('', 6000), authkey=b'abc')

manager.start()

task = manager.get_task_queue()
result = manager.get_result_queue()
cookie = manager.get_cookie_queue()
user = manager.get_user_queue()
pic = manager.get_pic_queue()
cookies = crawler_master.login()
cookie.put(cookies)


def getresult():
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        tmp = result.get(timeout=100)
        print(tmp)
        insert = "insert into user values (?, ?, ?, ?, ?) "
        cursor.execute(insert, (tmp[0], tmp[1], tmp[2], tmp[3], tmp[4]))
        print(tmp)
        print('Insert one data...')
    except BaseException as e:
        print(e)
    finally:
        n = result.qsize()
        print('%d datas are waiting' % n) 
        cursor.close()
        conn.commit()
        conn.close()
print('Put cookies in the queue...')
task.put('https://www.zhihu.com/people/he-ti-cong/followees')
print('Put the first url')
print('Try get results...')

while True:
    getresult()


manager.shutdown()
print('master exit.')
