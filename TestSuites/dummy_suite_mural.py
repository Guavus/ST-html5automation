import glob

from selenium import webdriver

from Utils.logger import *
from Utils.resultlogger import *
import os
import platform
from Utils.send_mail_1 import *

if platform.system() == "Windows":
    delimiter = "\\"
else:
    delimiter = "/"

test_file_strings = glob.glob('../*dummy_package*/test_*.py')

# module_strings = [str.split('/')[1] + "." + str.split('/')[2].split('.')[0] for str in test_file_strings]
module_strings = [str2.split(delimiter)[1] + "." + str2.split(delimiter)[2].split('.')[0] for str2 in test_file_strings]
# [__import__(str) for str in module_strings]

import __builtin__
__builtin__.testcases = []
testsuite = {}

global result_chart_file_path
result_chart_file_path = '../logs/result_chart_'+time.strftime("%d_%m_%y_%H_%M_%S")+'.html'
logger.info("Chart File Path ========= %s",str(result_chart_file_path))

with open('../logs/result_chart_'+time.strftime("%d_%m_%y_%H_%M_%S")+'.html',"w") as f:
    f.write("")
result_chart_file_path = os.path.abspath(result_chart_file_path)
for str1 in module_strings:
    try:
        logger.debug('*********** TestCase Start ***********')

        # testcases = []
        import __builtin__
        __builtin__.testcases = []

        resultlogger.debug('<br>*********** Logging Results for %str ***********<br>',str1)
        logger.debug('Executing TestCase %s', str1)
        __import__(str1)
        pass_count = 0
        fail_count = 0
        for tc in testcases:
            if tc['status'] == "FAIL":
                fail_count=fail_count+1
            elif tc['status'] == "PASS":
                pass_count=pass_count+1

        testcases.append(pass_count)
        testcases.append(fail_count)
        testsuite[str1] = testcases
        logger.debug('*********** TestCase End (%s) ***********', str1)

        try:
            logger.debug('Executing  "taskkill /im chromedriver.exe /f"')
            print os.system("taskkill /im chromedriver.exe /f")
            logger.debug('ChromeDriver killed by taskkill /im chromedriver.exe /f')
            print os.system("taskkill /im chrome.exe /f")
            logger.debug('ChromeBrowser killed by taskkill /im chrome.exe /f')


            #add chart here

        except Exception as e:
            logger.error('Got Exception %s while executing "taskkill /im chromedriver.exe /f"', e)
            try:
                logger.debug('Executing  "taskkill /im chrome.exe /f"')
                print os.system("taskkill /im chrome.exe /f")
            except:
                logger.error('Got Exception %s while executing "taskkill /im chrome.exe /f"', e)



    except Exception as e:
        # driver.save_screenshot('screenshots/screenie.png')
        logger.error('Exception found while executing %s ::: %s',str1,e)
        logger.debug('*********** TestCase (%s) End with Exceptions ***********', str1)
        try:
            logger.debug('Executing  "taskkill /im chromedriver.exe /f"')
            print os.system("taskkill /im chromedriver.exe /f")
            logger.debug('ChromeDriver killed by taskkill /im chromedriver.exe /f')
        except Exception as e:
            logger.error('Got Exception %s while executing "taskkill /im chromedriver.exe /f"',e)



def dump_to_html(testsuite):
    with open(result_chart_file_path,"a") as f:
        f.write("<table>")
        f.write("<tr>")
        f.write("<td>"+str("Testcase")+"</td>")
        f.write("<td>"+str("Status")+"</td>")
        f.write("<td>"+str("Expected Result")+"</td>")
        f.write("<td>"+str("Actual Result")+"</td>")
        f.write("</tr>")
        for suite,testcases in testsuite.iteritems():
            f.write(str(suite))
            f.write("<table>")
            f.write("<tr>")
            f.write("<td>"+str("Testcase")+"</td>")
            f.write("<td>"+str("Status")+"</td>")
            f.write("<td>"+str("Expected Result")+"</td>")
            f.write("<td>"+str("Actual Result")+"</td>")
            f.write("</tr>")
            for i in range(len(testcases)-2):
                # if testcases[i]['status'] == "FAIL":
                f.write("<tr>")
                f.write("<td>"+str(testcases[i]['title'])+"</td>")
                f.write("<td><font color='red'>"+str(testcases[i]['status'])+"</font></td>")
                f.write("<td>"+str(testcases[i]['expected'])+"</td>")
                f.write("<td>"+str(testcases[i]['actual'])+"</td>")
                # for k,v in testcases[i].iteritems():
                #     f.write("<td>"+str(v)+"</td>")
                f.write("</tr>")
            f.write("</table>")
            f.write("<br><br>")


    suites = testsuite.keys()
    failCounts = []
    passCounts = []
    for i in range(len(suites)):
        failCounts.append(testsuite[suites[i]][len(testsuite[suites[i]])-1])
        passCounts.append(testsuite[suites[i]][len(testsuite[suites[i]])-2])

    text_to_dump = "Highcharts.chart('container', {chart: {type: 'bar'},title: {text: 'Test Results'},xAxis: {categories: " \
                   +str(suites)+ \
                   "},yAxis: {min: 0,title: {text: 'TestCase Numbers'}},legend: {reversed: true},plotOptions: {series: {stacking: 'normal'}}," \
                   "series: [{name: 'Fail',data: " \
                   +str(failCounts)+ \
                   "}," \
                   "{name: 'Pass',data: " \
                   +str(passCounts)+ \
                   "}]});"
    return text_to_dump

    # with open("/Users/mayank.mahajan/Downloads/Archive-3/js_1.js","w") as f:
    #     global js_file_path
    #     # js_file_path = os.path.abspath("../logs/js_1.js")
    #     js_file_path = "js_1.js"
    #     f.write(text_to_dump)

    # return text_to_dump




# suites = testsuite.keys()
# for i in range(len(suites)):
#     failCounts = testsuite[suites[i]][len(testsuite[suites[i]])-1]
#     passCounts = testsuite[suites[i]][len(testsuite[suites[i]])-2]
#
# text_to_dump = "Highcharts.chart('container', {chart: {type: 'bar'},title: {text: 'Test Results'},xAxis: {categories: " \
#                +str(suites)+ \
#                "},yAxis: {min: 0,title: {text: 'TestCase Numbers'}},legend: {reversed: true},plotOptions: {series: {stacking: 'normal'}}," \
#                "series: [{name: 'Fail',data: " \
#                +str(failCounts)+ \
#                "}," \
#                "{name: 'Pass',data: " \
#                +str(passCounts)+ \
#                "}]});"
#
#
# with open("../logs/js_1.js","w") as f:
#     f.write(text_to_dump)

text_to_dump  = dump_to_html(testsuite)
with open(result_chart_file_path) as f:
    data = f.readlines()
    # sendmail_selenium(additional_script_path=js_file_path,additional_text=data[0])
    sendmail_selenium(additional_script_path=text_to_dump,additional_text=data[0])

    # from selenium.webdriver import *
    # webdriver.Chrome()
    # webdriver.Ac

    # Highcharts.chart('container', {chart: {type: 'bar'},title: {text: 'Test Results'},xAxis: {categories: arguments[0]},yAxis: {min: 0,title: {text: 'TestCase Numbers'}},legend: {reversed: true},plotOptions: {series: {stacking: 'normal'}},series: [{name: 'Fail',data: arguments[1]}, {name: 'Pass',data: arguments[2]}]});




# import unittest
# testSuite = unittest.TestSuite()
# suites = [unittest.TestLoader().loadTestsFromName(str) for str in module_strings]
# [testSuite.addTest(suite) for suite in suites]
# print testSuite
#
# result = unittest.TestResult()
# testSuite.run(result)
# print result
#
# Ok, at this point, I have a result, how do I display it as the normal unit test
# command line output?
# if __name__ == "__main__":
#     unittest.main()