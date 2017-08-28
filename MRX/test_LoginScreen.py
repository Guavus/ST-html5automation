from Utils.SetUp import *
from Utils.utility import *
try:
    setup = SetUp()
    sleep(10)
    handle=getHandle(setup,Constants.LOGINSCREEN)
    loginFlag=True
    for k in handle:
        if len(handle[k][k])==0 and k!='msg':
            loginFlag=False
            break
    checkEqualAssert(True,loginFlag,message='login page gets loaded when the url is entered on a browser',testcase_id='MKR-1641')

    loginScenario = ConfigManager().getNodeElements("loginScreen_Scenario", "scenario")
    for k, scenario in loginScenario.iteritems():
        if scenario['isInCorrect']=="True":
            login(setup, scenario['username'], scenario['password'])
            if str(scenario['username']).strip() == "" or str(scenario['password']).strip() == "":
                errorMessageFromScreen=''
                h=getHandle(setup,Constants.LOGINSCREEN)
                if h['msg']['msg'] > 0:
                    errorMessageFromScreen=str(h['msg']['msg'][0].text)

                if str(scenario['username']).strip() == "" and str(scenario['password']).strip() == "":
                    checkEqualAssert(Constants.INVALIDCREDENTIAL_MESSAGE,errorMessageFromScreen,message="Validate Invalid Password Error Message")
                elif str(scenario['username']).strip() == "":
                    checkEqualAssert(Constants.INVALIDUSERNAME_MESSAGE,errorMessageFromScreen, message="Validate Invalid UserName Error Message")
                else:
                    checkEqualAssert(Constants.INVALIDPASSWORD_MESSAGE,errorMessageFromScreen, message="Validate Invalid Password Error Message")

            else:
                errorFlag, errorMsg = isError(setup)
                checkEqualAssert(scenario['isInCorrect'],str(errorFlag),message='Verify that a user is prompted with an appropriate message if invalid credentials are entered',testcase_id=scenario['testcaseID'])
                checkEqualAssert(Constants.INVALIDCREDENTIAL_POPUP_MESSAGE,errorMsg,message="Validate Error Message")

    for k,scenario in loginScenario.iteritems():
        if scenario['isInCorrect']=="False":
            login(setup, scenario['username'], scenario['password'])
            errorFlag, errorMsg = isError(setup)
            checkEqualAssert(scenario['isInCorrect'], str(errorFlag),message='Verify that user able to enter username and password in the text boxes provided, and gets successfully logged in with valid credentials.',testcase_id=scenario['testcaseID'])

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    setup.d.close()
