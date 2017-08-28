from Utils.SetUp import *
from Utils.utility import *
from classes.Pages.ExplorePageClass import *
try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    #exploreInstance = ExplorePageClass(setup.d)
    exploreHandle = getHandle(setup, Constants.VALIDATE_HEADER)

    headerComponents = setup.cM.getNodeElements("headerComponent", "component")
    for k,headerComponent in headerComponents.iteritems():
        if headerComponent['leftLogoFlag']=='True':
            checkEqualAssert(1,len(exploreHandle['leftHeader']['img_Logo']),message="Validate Logo Present on left Side",testcase_id=headerComponent['testcaseID'])
        if headerComponent['projectTitleFlag']=='True':
            checkEqualAssert(str(headerComponent['projectTitle']).strip(), str(exploreHandle['leftHeader']['project_Name'][0].text).strip(), message="Validate Project title on left Side",testcase_id=headerComponent['testcaseID'])
        if headerComponent['screenFlag']=='True':
            checkEqualAssert(headerComponent['numberOfScreen'],str(len(exploreHandle['centerHeader']['alllinks'])),message="Validate Center Header i.e Number of available Screen", testcase_id=headerComponent['testcaseID'])
            allScreen=True
            for ele in exploreHandle['centerHeader']['alllinks']:
                if not str(ele.text) in headerComponent['listOfScreen']:
                    allScreen=False
                    break
            checkEqualAssert(True,allScreen,message="Validate Screen Name at Center of Header ::"+str(headerComponent['listOfScreen']), testcase_id=headerComponent['testcaseID'])

        if headerComponent['userNameFlag']=="True":
            userFlag=False
            for ele in exploreHandle['rightHeader']['userName']:
                if str(Constants.USERNAME).strip()==str(ele.text).strip():
                    userFlag=True
                    break
            checkEqualAssert(True,userFlag,message="Validate User Name :: "+Constants.USERNAME+" Present on Right Side ", testcase_id=headerComponent['testcaseID'])

        if headerComponent['profilePicFlag']=="True":
            pass

        if headerComponent['switcherIconFlag']=="True":
            checkEqualAssert(1, len(exploreHandle['rightHeader']['switcher']), message="Validate Switcher Present on Right Side",testcase_id=headerComponent['testcaseID'])

        if headerComponent['helpIconFlag']=="True":
            pass

    #exploreInstance.launchModule(exploreHandle, "USER DISTRIBUTION")

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s", r, str(e))
    setup.d.close()