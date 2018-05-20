import sys
import datetime
import time
import re
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import csv
import pymysql
from datetime import timedelta
import numpy

# global variables
host_name = '10.64.12.11'
username = 'scripterIn'
password = 'scripter'
server_version_file = 'ServerVersion.csv'
KPI_5_dir_path = 'KPI_5'
ServerNameList = []
processed_data = {}

# method to process db query data
def process_query_response(query, csv_handle, cur, start_timestamp_str, end_timestamp_str, server):
    row_count = cur.execute(query)

    if row_count > 0 :
        result = cur.fetchall()
        for row in result:
            csv_handle.writerow(row)
    elif row_count == 0:
        csv_handle.writerow(['', '', server])

# process token from checkin_checkout_data line
def process_token_checkin_checkout(checkout, checkin, server_name):

    # store time in 4 hours slots for 24 Hours
    time_split_four_hours = [0, 0, 0, 0, 0, 0]

    # converting the checkin, checkout string to datetime object
    checkin_obj = datetime.datetime.strptime(checkin, '%m/%d/%Y %H:%M')
    checkout_obj = datetime.datetime.strptime(checkout, '%m/%d/%Y %H:%M')

    # fetching only time
    checkin_time = checkin_obj.time()
    checkout_time = checkout_obj.time()

    # calculating total time in minutes
    difference = checkin_obj - checkout_obj
    total_minutes = (difference.days * 24 * 60) + (difference.seconds / 60)
    if total_minutes < 0:
        raise Exception("Time difference is negative for checkin:"+ str(checkin) + " and checkout:"+ str(checkout) + " time for server: "+ str(server_name))

    # fetching starting time slots
    hour_value = int(re.findall(r'\d+/\d+/\d+\s(\d+):\d+', checkout)[0])
    start_time_slot = hour_value//4

    # finding total slots to which time needs to be added
    total_slots_to_add_time, remaining_time_minutes = total_minutes//240, total_minutes%240

    # loop to process total minutes to all corresponding slots
    start = start_time_slot
    count = total_slots_to_add_time
    # flag for first slot time
    flag = 0
    while (total_minutes > 0):

        # find the endtime for the slot which is the starting slot for checkout time
        slot_endtime = datetime.time(((start+1)*4)%24, 0, 0)

        # time difference in minutes bw slot end time and checkout time
        time_diff = (datetime.datetime.combine(datetime.date.today(),slot_endtime) - datetime.datetime.combine(datetime.date.today(),checkout_time)).seconds//60

        if total_minutes <= time_diff and flag == 0:
            flag = 1
            time_split_four_hours[start] += total_minutes
            start += 1
            total_minutes = 0

        elif total_minutes > time_diff and flag == 0:
            flag = 1
            time_split_four_hours[start] += time_diff
            total_minutes -= time_diff
            start += 1
            if count == 0:
                remaining_time_minutes -= time_diff
            elif count > 0:
                if time_diff <= remaining_time_minutes:
                    remaining_time_minutes -= time_diff
                else:
                    count -= 1

        elif remaining_time_minutes <= 240 and count == 0:
            time_split_four_hours[start] += total_minutes
            total_minutes = 0
            remaining_time_minutes = 0

        elif count >= 0:
            time_split_four_hours[start] += 240
            total_minutes -= 240
            start += 1
            count -= 1
        # looping back the slot number starting
        if start == 6:
            start = 0

    # updating the processed data to the dictionary
    if server_name not in processed_data:
        processed_data.update({
            server_name: {
                "hr0-4"   : time_split_four_hours[0],
                "hr4-8"   : time_split_four_hours[1],
                "hr8-12"  : time_split_four_hours[2],
                "hr12-16" : time_split_four_hours[3],
                "hr16-20" : time_split_four_hours[4],
                "hr20-24" : time_split_four_hours[5]
            }
        })
    else:
        processed_data[server_name]["hr0-4"] += time_split_four_hours[0]
        processed_data[server_name]["hr4-8"] += time_split_four_hours[1]
        processed_data[server_name]["hr8-12"] += time_split_four_hours[2]
        processed_data[server_name]["hr12-16"] += time_split_four_hours[3]
        processed_data[server_name]["hr16-20"] += time_split_four_hours[4]
        processed_data[server_name]["hr20-24"] += time_split_four_hours[5]

# method to plot the chart/graph for kpi-5 using matplotlib and dump the data to csv file
def plot_kpi_5(processed_data, output_filepath= "KPI_5", title= "KPI_5"):

    server_name = []
    hr0_4 = []
    hr4_8 = []
    hr8_12 = []
    hr12_16 = []
    hr16_20 = []
    hr20_24 = []

    # processing the data from dictionary
    for server in processed_data:
        server_data = processed_data[server]
        server_name.append(server)
        hr0_4.append(server_data['hr0-4']/60.0)
        hr4_8.append(server_data['hr4-8']/60.0)
        hr8_12.append(server_data['hr8-12']/60.0)
        hr12_16.append(server_data['hr12-16']/60.0)
        hr16_20.append(server_data['hr16-20']/60.0)
        hr20_24.append(server_data['hr20-24']/60.0)

    # storing data in csv file
    with open(output_filepath + "/kpi5.csv", "wb") as file_handle:
        c = csv.writer(file_handle)
        c.writerow(['server', 'hr0-4', 'hr4-8', 'hr8-12', 'hr12-16', 'hr16-20', 'hr20-24'])
        for i in range(0,len(server_name)):
            c.writerow([server_name[i], hr0_4[i], hr4_8[i], hr8_12[i], hr12_16[i], hr16_20[i], hr20_24[i]])

    x = numpy.arange(len(server_name))
    # plot
    rcParams.update({'figure.autolayout': True})
    plt.bar(x, hr0_4, width= 0.5, color= 'blue')
    plt.bar(x, hr4_8, width= 0.5, color= 'orange', bottom= hr0_4)
    plt.bar(x, hr8_12, width= 0.5, color= 'green', bottom= [ a+b for a, b in zip(hr0_4, hr4_8)])
    plt.bar(x, hr12_16, width= 0.5, color= 'red', bottom= [ a+b+c for a, b, c in zip(hr0_4, hr4_8, hr8_12)])
    plt.bar(x, hr16_20, width= 0.5, color= 'yellow', bottom= [ a+b+c+d for a,b,c,d in zip(hr0_4, hr4_8, hr8_12, hr12_16)])
    plt.bar(x, hr20_24, width= 0.5, color= 'black', bottom= [ a+b+c+d+e for a,b,c,d,e in zip(hr0_4, hr4_8, hr8_12, hr12_16, hr16_20)])

    # labels
    plt.xticks(x, server_name, fontsize= 5, rotation= 90)
    total_hours_in_week = 7*24 + 3
    plt.yticks(numpy.arange(0, total_hours_in_week , 10), fontsize= 5)
    plt.title(title)
    plt.xlabel('Server Name')
    plt.ylabel('Hours Used')

    #legend
    blue_patch = mpatches.Patch(color='blue', label= 'hr0-4')
    orange_patch = mpatches.Patch(color='orange', label= 'hr4-8')
    green_patch = mpatches.Patch(color='green', label= 'hr8-12')
    red_patch = mpatches.Patch(color='red', label= 'hr12-16')
    yellow_patch = mpatches.Patch(color='yellow', label= 'hr16-20')
    black_patch = mpatches.Patch(color='black', label= 'hr20-24')
    plt.legend(handles= [blue_patch, orange_patch, green_patch, red_patch, yellow_patch, black_patch], loc= 'upper right', prop={'size': 5})

    # display
    plt.savefig(output_filepath + "/kpi5.png", dpi= 400)

try:
    # # get the endtime from the user
    # input_end_time_str = sys.argv[1]
    #
    # # converting the input time to datetime object and generating endtime and starttime
    # reference_timestamp = datetime.datetime.strptime(input_end_time_str, '%Y-%m-%d')
    # end_timestamp = reference_timestamp + timedelta(hours=23, minutes=59, seconds=59)
    # start_timestamp = reference_timestamp + timedelta(days= -6)
    #
    # # timestamps in string format
    # end_timestamp_str = end_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    # start_timestamp_str = start_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    #
    # # timestamps in format to be used by select query
    # token_end_timestamp_str = end_timestamp.strftime('%m/%d/%Y %H:%M')
    # token_start_timestamp_str = start_timestamp.strftime('%m/%d/%Y %H:%M')
    #
    # # connecting to the database
    # # db = pymysql.connect(host = host_name, user = username, passwd = password)
    # # cursor_handle = db.cursor()
    #
    # # creating directory for KPI_5 ouput data
    # # if not os.path.exists(KPI_5_dir_path):
    # #     os.makedirs(KPI_5_dir_path)
    #
    # # fetching data from db and dumping it in csv file
    # timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%d_%m_%Y_%H_%M_%S')
    #
    # # timestamp_csv_file = "checkin_checkout_data_" + timestamp + ".csv"
    # # fp = open(timestamp_csv_file, "ab")
    # # c = csv.writer(fp)
    # # c.writerow(['checkin', 'checkout', 'server'])
    #
    # # fetching server name from server version file
    # with open(server_version_file, "rb") as sv_file:
    #     reader = csv.DictReader(sv_file, delimiter=',')
    #     ServerNameList = [line['ServerName'] for line in reader]
    #
    # # executing queries for each server name
    # for server in ServerNameList:
    #     query_1 = "SELECT CheckIn, CheckOut, ServerName FROM asterixtestnetwork.testspaceregistry tsr inner join asterixtestnetwork.obelixtestspace ots on tsr.TestSpaceID=ots.ServerTestSpaceID inner join asterixtestnetwork.obelixservertable ost on ots.ServerID=ost.ServerID WHERE checkout between '{0}' and '{1}' and checkin between '{0}' and '{1}' AND ServerName= '{2}'".format(start_timestamp_str, end_timestamp_str, server)
    #     query_2 = "SELECT CheckIn, '{3}', ServerName FROM asterixtestnetwork.testspaceregistry tsr inner join asterixtestnetwork.obelixtestspace ots on tsr.TestSpaceID=ots.ServerTestSpaceID inner join asterixtestnetwork.obelixservertable ost on ots.ServerID=ost.ServerID WHERE checkout < '{0}' and checkin between '{0}' and '{1}' AND ServerName= '{2}'".format(start_timestamp_str, end_timestamp_str, server, token_start_timestamp_str)
    #     query_3 = "SELECT '{3}', CheckOut, ServerName FROM asterixtestnetwork.testspaceregistry tsr inner join asterixtestnetwork.obelixtestspace ots on tsr.TestSpaceID=ots.ServerTestSpaceID inner join asterixtestnetwork.obelixservertable ost on ots.ServerID=ost.ServerID WHERE checkout between '{0}' and '{1}' and (checkin is NULL or checkin > '{1}') AND ServerName= '{2}'".format(start_timestamp_str, end_timestamp_str, server, token_end_timestamp_str)
    #     query_4 = "SELECT '{4}', '{3}', ServerName FROM asterixtestnetwork.testspaceregistry tsr inner join asterixtestnetwork.obelixtestspace ots on tsr.TestSpaceID=ots.ServerTestSpaceID inner join asterixtestnetwork.obelixservertable ost on ots.ServerID=ost.ServerID WHERE checkout < '{0}' and (checkin is NULL or checkin > '{1}') AND ServerName= '{2}'".format(start_timestamp_str, end_timestamp_str, server, token_start_timestamp_str, token_end_timestamp_str)
    #
    #     # process_query_response(query_1, c, cursor_handle, start_timestamp_str, end_timestamp_str, server)
    #     # process_query_response(query_2, c, cursor_handle, start_timestamp_str, end_timestamp_str, server)
    #     # process_query_response(query_3, c, cursor_handle, start_timestamp_str, end_timestamp_str, server)
    #     # process_query_response(query_4, c, cursor_handle, start_timestamp_str, end_timestamp_str, server)
    #
    # fp.close()
    #
    # print("Data successfully fetched from database..")
    #
    # # processing checkin_checkout_data
    # with open(timestamp_csv_file, "rb") as timestamp_file:
    #     reader = csv.DictReader(timestamp_file, delimiter=',')
    #     for line in reader:
    #         checkin = line['checkin']
    #         checkout = line['checkout']
    #         server_name = line['server']
    #         if process_token_checkin_checkout(checkout, checkin, server_name) == False:
    #             raise
    # kpi_title = start_timestamp_str.split()[0] + " to " + end_timestamp_str.split()[0]
    # plot_kpi_5(processed_data, output_filepath= KPI_5_dir_path, title= kpi_title)


    if process_token_checkin_checkout( checkout= '5/31/2018 23:55',checkin= '6/01/2018 23:54',server_name= 'Server_A') == False:
        raise
    if process_token_checkin_checkout( checkout= '5/10/2018 0:00',checkin= '5/10/2018 0:01',server_name= 'Server_B') == False:
        raise
    print("end")
    print(processed_data)
    processed_data = {
    'ECX-A05-SERVER_BA1': {'hr20-24': 3000, 'hr4-8': 1800, 'hr16-20': 2400, 'hr8-12': 1200, 'hr12-16': 1200, 'hr0-4': 360},
     'Server_2': {'hr20-24': 360, 'hr4-8': 3000, 'hr16-20': 1800, 'hr8-12': 2400, 'hr12-16': 600, 'hr0-4': 600},
     'Server_3': {'hr20-24': 3000, 'hr4-8': 1800, 'hr16-20': 2400, 'hr8-12': 1200, 'hr12-16': 1200, 'hr0-4': 360},
     'Server_4': {'hr20-24': 360, 'hr4-8': 3000, 'hr16-20': 0, 'hr8-12': 2400, 'hr12-16': 600, 'hr0-4': 600},
     'Server_5': {'hr20-24': 3000, 'hr4-8': 1800, 'hr16-20': 2400, 'hr8-12': 1200, 'hr12-16': 1200, 'hr0-4': 360},
     'Server_6': {'hr20-24': 360, 'hr4-8': 3000, 'hr16-20': 1800, 'hr8-12': 2400, 'hr12-16': 600, 'hr0-4': 600},
     'Server_7': {'hr20-24': 3000, 'hr4-8': 1800, 'hr16-20': 2400, 'hr8-12': 1200, 'hr12-16': 1200, 'hr0-4': 360},
      'Server_8': {'hr20-24': 360, 'hr4-8': 3000, 'hr16-20': 1800, 'hr8-12': 2400, 'hr12-16': 600, 'hr0-4': 600},
      'Server_9': {'hr20-24': 3000, 'hr4-8': 1800, 'hr16-20': 2400, 'hr8-12': 1200, 'hr12-16': 1200, 'hr0-4': 360},
      'Server_10': {'hr20-24': 360, 'hr4-8': 3000, 'hr16-20': 0, 'hr8-12': 2400, 'hr12-16': 600, 'hr0-4': 600},
      'Server_11': {'hr20-24': 3000, 'hr4-8': 1800, 'hr16-20': 2400, 'hr8-12': 1200, 'hr12-16': 1200, 'hr0-4': 360},
      'Server_12': {'hr20-24': 360, 'hr4-8': 3000, 'hr16-20': 1800, 'hr8-12': 2400, 'hr12-16': 600, 'hr0-4': 600},
      'Server_13': {'hr20-24': 360, 'hr4-8': 3000, 'hr16-20': 1800, 'hr8-12': 2400, 'hr12-16': 600, 'hr0-4': 600}
     }
    kpi_title = "2018-05-10 to 2018-05-17"
    plot_kpi_5(processed_data, output_filepath= KPI_5_dir_path, title= kpi_title)
except Exception as e:
    print("Exception occured:")
    print(e)
