import Exporter,sys 
import csv
import time,datetime
import datetime
from time import mktime

# from dateutil.relativedelta import relativedelta

arg_list = ['--username', '@tomfeeback', '--convid', '355537360030674944','--since','start_date','--until','end_date']

with open("./data/nuanced_hate_2.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if row[3] != "-":
                arg_list[1] = row[3]
                arg_list[3] = row[1]
                # print(row)

                ts = time.strptime(row[4],'%Y-%m-%d %H:%M:%S')
                dt = datetime.datetime.fromtimestamp(mktime(ts))
                # print(dt)
                # time.strftime('%Y-%m-%d'))
                start_time = dt-datetime.timedelta(days=1)
                until_time = dt+datetime.timedelta(days=21)
                # print(until_time)
                
                start_date_str = start_time.strftime("%Y-%m-%d")
                end_date_str = until_time.strftime("%Y-%m-%d")


                arg_list[5] = start_date_str
                arg_list[7] = end_date_str 
                # print(start_date_str)
                # print(end_date_str)
                print(arg_list)
                try:
                    Exporter.main(arg_list)
                except:
                    continue

                line_count2 = 0
                with open("output_got.csv") as csv_file2:    
                    csv_reader2 = csv.reader(csv_file2, delimiter=';')  
                    for row2 in csv_reader2:
                        if line_count2 == 0:
                            line_count2 += 1
                        else:
                            reply_id = row2[-2]
                            tweet_id = arg_list[3]
                            print(reply_id,tweet_id)
                            with open('./output/nuanced_hate.txt','a+') as final:
                                final.write( str(tweet_id) + "," + str(reply_id) + '\n')
