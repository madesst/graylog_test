import time
import sys
import psycopg2
import math

def main():

  start = time.time()
  secondsPause = 2

  con = None

  try:

    con = psycopg2.connect(database='vagrant', user='vagrant')
    cur = con.cursor()

    cur.execute("TRUNCATE TABLE test_1")
    cur.execute("TRUNCATE TABLE test_2")

    while (con):

      time.sleep(secondsPause)
      totalTime = int(math.floor(time.time() - start));

      if totalTime % 20 == 0:
        cur.execute("insert into test_1 (name) values ('vagrant')");
      elif totalTime % 10 == 0:
        cur.execute("insert into test_2 (name) values ('vagrant')");
      elif totalTime % 2 == 0:
        cur.execute("update test_1 set name = 'test_1' where id is null");

      cur.execute("""-- multiline query
        select * from test_1
          inner join test_2 on test_1.id = test_2.id
        where test_1.id is null-- no data required
        order by test_1.id desc
        """);

      if totalTime > 200:
        start = time.time()

      con.commit()

  except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)

  finally:

    if con:
      con.close();

main()