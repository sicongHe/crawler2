import sqlite3


def select():
    print('Your target:')
    target = input()
    try:
        if target == 'no':
            exit()
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        if target == 'all':
            cursor.execute("select distinct * from user")
            write = True
        else:
            cursor.execute("select * from user where name='%s'" % target)
        values = cursor.fetchall()
        cursor.close()
        conn.close()
        if values == []:
            print('%s Not Found,please try again...' % target)
        else:
            if write == True:
                with open('out.txt','w') as f:
                    for i in values:
                        for n in i:
                            n = str(n)
                            f.write(n)
                            f.write(' ')
                        f.write('\n')
    except BaseException as e:
        print(e)
        select()
    finally:
        select()

if __name__ == '__main__':
    select()
