from Utils.SetUp import *
from Utils.utility import *
from classes.Pages.ExplorePageClass import *
try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)



    exploreHandle = getHandle(setup, Constants.VALIDATE_FOOTER)

    footerComponents = setup.cM.getNodeElements("footerComponent", "component")
    for k,footerComponent in footerComponents.iteritems():
        if footerComponent['timezoneLabel']=='True':
            checkEqualAssert(footerComponent['timezoneText'].strip(),str(exploreHandle['leftFooter']['timeZoneText'][0].text).strip(),message="Validate timezone label on footer",testcase_id=footerComponent['testcaseID'])
        if footerComponent['orgLabel']=='True':
            checkEqualAssert(footerComponent['orgText'].strip(), exploreHandle['rightFooter']['orgText'][0].text.encode('ascii','replace'), message="Validate organisation label on footer",testcase_id=footerComponent['testcaseID'])





    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved and Exception = %s", r, str(e))
    setup.d.close()