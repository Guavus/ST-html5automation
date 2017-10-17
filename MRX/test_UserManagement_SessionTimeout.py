from MuralUtils.ContentHelper import *
from classes.Pages.MuralScreens.UserMangementScreen import *
from classes.Pages.ExplorePageClass import *
from MRXUtils.MRXConstants import *
try:
    setup = SetUp()
    login(setup,Constants.USERNAME,Constants.PASSWORD)
    wfstart = WorkflowStartComponentClass()
    exploreScreenInstance = ExplorePageClass(setup.d)
    userScreenInstance=UserManagementScreenClass(setup.d)

    setup.d.execute_script('window.open("'+Constants.URL+'","_blank");')
    time.sleep(5)
    setup.d.switch_to.window(setup.d.window_handles[1])
    exploreScreenInstance.exploreList.clickOnIcon(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'),icon='profile')
    clickFlag = exploreScreenInstance.exploreList.clickOnLinkByValue(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'), MuralConstants.Logout)

    setup.d.switch_to.window(setup.d.window_handles[0])

    exploreHandle = getHandle(setup, MRXConstants.ExploreScreen)
    exploreScreenInstance.exploreList.launchModule(exploreHandle, "SEGMENTS")
    errFlag, errMsg = isError(setup)

    checkEqualAssert(True,errFlag,message="Validate the session of the UI.",testcase_id="MKR-3499")
    setup.d.switch_to.window(setup.d.window_handles[1])
    setup.d.close()
    setup.d.switch_to.window(setup.d.window_handles[0])
    setup.d.close()

except Exception as e:
    isError(setup)
    r = "issue_" + str(random.randint(0, 9999999)) + ".png"
    setup.d.save_screenshot(r)
    logger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved", r)
    resultlogger.debug("Got Exception from Script Level try catch :: Screenshot with name = %s is saved <br>", r)
    setup.d.close()