from Utils.SetUp import *
from Utils.utility import *
from classes.Pages.ExplorePageClass import *
try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)

    #exploreInstance = ExplorePageClass(setup.d)
    #exploreInstance.launchModule(exploreHandle, "USER DISTRIBUTION")

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
            availableScreenList=[]
            for ele in exploreHandle['centerHeader']['alllinks']:
                availableScreenList.append(str(ele.text).strip())
            availableScreen=','.join(availableScreenList)
            checkEqualAssert(headerComponent['listOfScreen'],availableScreen,message="Validate Screen Name at Center of Header ::"+str(headerComponent['listOfScreen']), testcase_id=headerComponent['testcaseID'])

        if headerComponent['userNameFlag']=="True":
            count=0
            for ele in exploreHandle['rightHeader']['userName']:
                if str(Constants.USERNAME).strip()==str(ele.text).strip():
                    count=count+1

            checkEqualAssert(1,count,message="Validate User Name :: "+Constants.USERNAME+" Present on Right Side ", testcase_id=headerComponent['testcaseID'])


        isProfilePicPresent=False
        isHelpIconPresent=False
        for img in exploreHandle['rightHeader']['image']:
            if 'profile' in str(img.get_attribute('src')):
                isProfilePicPresent=True
            elif 'help' in str(img.get_attribute('src')):
                isHelpIconPresent=True


        if headerComponent['profilePicFlag']=="True":
            checkEqualAssert(True,isProfilePicPresent,message="Validate User Image Present on Right Side",testcase_id=headerComponent['testcaseID'])

        if headerComponent['switcherIconFlag']=="True":
            checkEqualAssert(1, len(exploreHandle['rightHeader']['switcher']), message="Validate Switcher Present on Right Side",testcase_id=headerComponent['testcaseID'])

        if headerComponent['helpIconFlag']=="True":
            checkEqualAssert(True,isHelpIconPresent,message="Validate Help Icon Present on Right Side",testcase_id=headerComponent['testcaseID'])

    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s", r, str(e))
    setup.d.close()