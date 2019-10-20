import sqlite3


def make_json_using_db():
    output_file = open("co2_paramter.json","w")
    output_file.write('[["co2",[')

    import pymysql
    import pymysql.cursors


    connection = pymysql.connect(host='35.244.98.157',
                                user='root',
                                password='',
                                db='weatherstore')
    with connection.cursor() as cursor:
        try:
            cursor.execute("select * from co_parameter")
            count = 0
            new_entry = 0
            for row in cursor.fetchall():
                if new_entry == 0 :
                    if row[2] == "ppm":
                        count += 1
                        output_file.write("{},{},{}".format(row[3],row[4],row[1]))
                        new_entry = 1
                else:
                    if row[2] == "ppm":
                        count += 1
                        output_file.write(",{},{},{}".format(row[3],row[4],row[1]))
                if count == 1000:
                    break
        except:
            print("opps")
        finally:
            output_file.write("]]]")
            connection.close()
            output_file.close()

def make_json(heights,points,filename):
    output_file = open(filename+".json","w")
    output_file.write('[["co2",[')
    try :
        new_entry = 0
        count = 0
        for height,point in zip(heights,points):
            if new_entry == 0:
                count += 1
                output_file.write("{},{},{}".format(point[0],point[1],height))
                new_entry = 1
            else :
                count += 1
                output_file.write(",{},{},{}".format(point[0],point[1],height))
    except:
        print("oops")
        return -1
    finally:
        output_file.write("]]]")
        output_file.close()
        return 1