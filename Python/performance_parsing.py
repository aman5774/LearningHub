import datetime
import json


class Performance:
    time_stamp = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    file1=open("performance"+time_stamp+".txt","a+")

def performance_metrics(data):
    print data
    Performance.file1.write(data)

def performance_parsing():
    results = {}
    with open('../performance.txt') as fp:
        for line in fp:
            tokens = line.split("::")
            if(len(tokens)==7):
                testcase,slot,API,response_time,elapsed_time,status_code,result = tokens[0],tokens[1],tokens[2],float(tokens[3]),float(tokens[4]),tokens[5],tokens[6].strip()
                
                if testcase not in results:
                    results.update({
                        testcase:{
                            "Overall_data":{
                                "total_requests":1,
                                slot+"_total_requests":1,
                                API:{
                                    "total_requests":1,
                                    "passed_requests":0,
                                    "failed_requests":0,
                                    "min_response_time":response_time,
                                    "maximum_response_time":response_time,
                                    "sum_response_time":response_time,
                                    "min_elapsed_time":elapsed_time,
                                    "maximum_elapsed_time":elapsed_time,
                                    "sum_elapsed_time":elapsed_time,
                                    "status_codes":{
                                        status_code:1
                                        }
                                    }
                                },
                            slot:{
                                "total_requests":1,
                                API:{
                                    "total_requests":1,
                                    "passed_requests":0,
                                    "failed_requests":0,
                                    "min_response_time":response_time,
                                    "maximum_response_time":response_time,
                                    "sum_response_time":response_time,
                                    "min_elapsed_time":elapsed_time,
                                    "maximum_elapsed_time":elapsed_time,
                                    "sum_elapsed_time":elapsed_time,
                                    "status_codes":{
                                        status_code:1
                                        }
                                    }
                                }
                            }
                        })
                    #checking if result is True or False, updating the result in results dictionary
                    if(result == "True"):
                        t = results[testcase]["Overall_data"][API]
                        t["passed_requests"]+=1
                        t = results[testcase][slot][API]
                        t["passed_requests"]+=1
                        
                    elif(result == "False"):
                        t = results[testcase]["Overall_data"][API]
                        t["failed_requests"]+=1
                        t = results[testcase][slot][API]
                        t["failed_requests"]+=1
                else:
                    testcase = results[testcase]

                    # checking slot is present or not in testcase
                    if slot not in testcase:
                        testcase.update({
                            slot:{
                                "total_requests":1,
                                API:{
                                    "total_requests":1,
                                    "passed_requests":0,
                                    "failed_requests":0,
                                    "min_response_time":response_time,
                                    "maximum_response_time":response_time,
                                    "sum_response_time":response_time,
                                    "min_elapsed_time":elapsed_time,
                                    "maximum_elapsed_time":elapsed_time,
                                    "sum_elapsed_time":elapsed_time,
                                    "status_codes":{
                                        status_code:1
                                        }
                                    }
                                }
                            })
                        if(result == "True"):
                            t = testcase[slot][API]
                            t["passed_requests"]+=1
                        
                        elif(result == "False"):
                            t = testcase[slot][API]
                            t["failed_requests"]+=1
                        
                        
                                
                    else:
                        testcase_slot = testcase[slot]
                        testcase_slot["total_requests"] += 1

                        #checking API in slot key
                        if API not in testcase_slot:
                            testcase_slot.update({
                                API:{
                                    "total_requests":1,
                                    "passed_requests":0,
                                    "failed_requests":0,
                                    "min_response_time":response_time,
                                    "maximum_response_time":response_time,
                                    "sum_response_time":response_time,
                                    "min_elapsed_time":elapsed_time,
                                    "maximum_elapsed_time":elapsed_time,
                                    "sum_elapsed_time":elapsed_time,
                                    "status_codes":{
                                        status_code:1
                                        }
                                    }
                                })
                            if(result == "True"):
                                t = testcase_slot[API]
                                t["passed_requests"]+=1
                        
                            elif(result == "False"):
                                t = testcase_slot[API]
                                t["failed_requests"]+=1
                        
                        else:
                            testcase_slot_api = testcase_slot[API]
                            testcase_slot_api["total_requests"] += 1
                            
                            #checking result and updating
                            if(result == "True"):
                                testcase_slot_api["passed_requests"] += 1
                            elif(result == "False"):
                                testcase_slot_api["failed_requests"] += 1

                            #checking response and elapsed time and updating
                            if(response_time <= testcase_slot_api["min_response_time"]):
                                testcase_slot_api["min_response_time"] = response_time
                            if(response_time >= testcase_slot_api["maximum_response_time"]):
                                testcase_slot_api["maximum_response_time"] = response_time

                            if(elapsed_time <= testcase_slot_api["min_elapsed_time"]):
                                testcase_slot_api["min_elapsed_time"] = elapsed_time
                            if(elapsed_time >= testcase_slot_api["maximum_elapsed_time"]):
                                testcase_slot_api["maximum_elapsed_time"] = elapsed_time

                            testcase_slot_api["sum_response_time"] += response_time
                            testcase_slot_api["sum_elapsed_time"] += elapsed_time

                            # checking status code and updating
                            testcase_slot_api_statuscode = testcase_slot_api["status_codes"]
                            if status_code not in testcase_slot_api_statuscode:
                                testcase_slot_api_statuscode.update({
                                        status_code:1
                                    })
                            else:
                                testcase_slot_api_statuscode[status_code] += 1

                    #updating test case overall data
                    testcase_overall = testcase["Overall_data"]
                    testcase_overall["total_requests"]+=1
                    if slot+"_total_requests" not in testcase_overall:
                        testcase_overall[slot+"_total_requests"]= 0
                    testcase_overall[slot+"_total_requests"] += 1

                    #checking if API in testcase Overall key
                    if API not in testcase_overall:
                        testcase_overall.update({
                            API:{
                                "total_requests":1,
                                "passed_requests":0,
                                "failed_requests":0,
                                "min_response_time":response_time,
                                "maximum_response_time":response_time,
                                "sum_response_time":response_time,
                                "min_elapsed_time":elapsed_time,
                                "maximum_elapsed_time":elapsed_time,
                                "sum_elapsed_time":elapsed_time,
                                "status_codes":{
                                    status_code:1
                                    }
                                }
                            })
                        if(result == "True"):
                            t = testcase["Overall_data"][API]
                            t["passed_requests"]+=1
                        
                        
                        elif(result == "False"):
                            t = testcase["Overall_data"][API]
                            t["failed_requests"]+=1
                  
                    else:
                        testcase_overall_api = testcase_overall[API]
                        testcase_overall_api["total_requests"] += 1

                        #checking result and updating
                        if(result == "True"):
                            testcase_overall_api["passed_requests"] += 1
                        elif(result == "False"):
                            testcase_overall_api["failed_requests"] += 1

                        #checking response and elapsed time and updating
                        if(response_time <= testcase_overall_api["min_response_time"]):
                            testcase_overall_api["min_response_time"] = response_time
                        if(response_time >= testcase_overall_api["maximum_response_time"]):
                            testcase_overall_api["maximum_response_time"] = response_time

                        if(elapsed_time <= testcase_overall_api["min_elapsed_time"]):
                            testcase_overall_api["min_elapsed_time"] = elapsed_time
                        if(elapsed_time >= testcase_overall_api["maximum_elapsed_time"]):
                            testcase_overall_api["maximum_elapsed_time"] = elapsed_time

                        testcase_overall_api["sum_response_time"] += response_time
                        testcase_overall_api["sum_elapsed_time"] += elapsed_time

                        # checking status code and updating
                        testcase_overall_api_statuscode = testcase_overall_api["status_codes"]
                        if status_code not in testcase_overall_api_statuscode:
                            testcase_overall_api_statuscode.update({
                                    status_code:1
                                })
                        else:
                            testcase_overall_api_statuscode[status_code] += 1

                        
            else:
                print("Invalid number of tokens.. Tokens:"+str(len(tokens)))
    print(json.dumps(results, indent=4))

performance_parsing()
