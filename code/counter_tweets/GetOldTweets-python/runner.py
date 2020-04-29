import Exporter,sys
import csv
import time,datetime
import datetime
from time import mktime
import multiprocessing
from joblib import Parallel, delayed

num_cores = multiprocessing.cpu_count()

# from dateutil.relativedelta import relativedelta


list_of_args = []

with open("./data/abusive_tweets_compile2.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    for row in csv_reader:
        arg_list = ['--username', '@tomfeeback', '--convid', '355537360030674944','--since','start_date','--until','end_date']

        # print(line_count)
        # if(line_count > 10000)
        #     break
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
                # print(arg_list)
                # print(arg_list)

                list_of_args.append(arg_list)

                # print(arg_list)


results = Parallel(n_jobs=8)(delayed(Exporter.main)(args) for args in list_of_args)


# for i in range(0,len(list_of_args)):
#     for each_result in results[i]:
#         with open('./output/abusive_hate.txt','a+') as final:
#             final.write( str(list_of_args[i][3]) +  "," + str(each_result.id)  + '\n')

