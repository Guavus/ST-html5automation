from Utils.utility import *
from MRXUtils.MRXConstants import *
from Utils.UMConstants import *


def findPropertyColor(screenInstance,h,property,parent="allinputs",child="input",index=0):
    propertycolor=str(h[parent][child][index].value_of_css_property(property))
    return screenInstance.cm.rgb_to_hex(propertycolor)


def isColorValid(screenInstance, h, property, parent="allinputs", child='input', index=0):
    h[parent][child][index].send_keys(Keys.TAB)
    bordercolor=findPropertyColor(screenInstance,h, property,parent=parent,child=child,index=index)
    if str(bordercolor)==Constants.REDCOLOR:
        logger.debug(" Invalid %s =%s",str(h[parent][child][index].get_attribute('placeholder')),str(h[parent][child][index].get_attribute('value')))
        resultlogger.debug(" Invalid Entry =%s <br>",str(h[parent][child][index].get_attribute('value')))
        return False
    else:
        return True

def dumpResultForButton(condition,request,screenInstance,setup,button_label="Create",screen=MRXConstants.MRXUMPOPUP,testcase_id=""):
    button_status=screenInstance.cm.isButtonEnabled(button_label,getHandle(setup,screen,"allbuttons"))
    checkEqualAssert(condition,button_status,message="Checking State of Button '" + button_label + "' for Fields entered : "+str(request),testcase_id=testcase_id)
    return button_status


def setUserDetail(setup,screenInstance,screenName,userDetail,button='Create',checkComplusoryFieldFlag=False):
    detail=[]
    flag_fname=False
    flag_lname=False
    flag_email = False
    flag_password = False
    flag_cpassword = False

    ############################################ Setting User Role #####################################################

    logger.info("Going to select UserRole for user ="+userDetail['username'])
    userRole_text = screenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup,screenName,'allselects'), str(userDetail['userrole']), index=0)
    checkEqualAssert(str(userDetail['userrole']), userRole_text,message="Verify selected User Role")

    # if str(userRole_text)=="Application":
    #     UserRole = '1'
    # else:
    #     UserRole='0'
    ############################################ Setting UserName ######################################################
    h = getHandle(setup,screenName,'allinputs')
    logger.info("Going to Enter detail of user ="+userDetail['username'])
    logger.info("Going to set UserName =%s",userDetail['username'])

    userNameFromUI = screenInstance.cm.sendkeys_input(userDetail['username'],h,0)
    checkEqualAssert(str(userNameFromUI),str(userDetail['username']),message="Verify Entered User Name")
    if not isColorValid(screenInstance, h,property=Constants.BORDERCOLOR, index=0):
        raise
    flag_usename=True
    dumpResultForButton(flag_usename and flag_fname and flag_lname and flag_email and flag_password and flag_cpassword, "UserName", screenInstance,setup)

    ############################################ Setting First and Last Name ###########################################

    firstNameFromUI = screenInstance.cm.sendkeys_input(userDetail['firstname'], h, 1)
    checkEqualAssert(str(firstNameFromUI), str(userDetail['firstname']),message="Verify Entered First Name")
    if not isColorValid(screenInstance, h,property=Constants.BORDERCOLOR, index=1):
        raise
    flag_fname=True
    dumpResultForButton(flag_usename and flag_fname and flag_lname and flag_email and flag_password and flag_cpassword,"First Name", screenInstance, setup)

    lastNameFromUI = screenInstance.cm.sendkeys_input(userDetail['lastname'], h, 2)
    checkEqualAssert(str(lastNameFromUI), str(userDetail['lastname']),message="Verify Entered Last Name")
    if not isColorValid(screenInstance, h,property=Constants.BORDERCOLOR, index=2):
        raise
    flag_lname=True
    dumpResultForButton(flag_usename and flag_fname and flag_lname and flag_email and flag_password and flag_cpassword,"Last Name", screenInstance, setup)

    detail.append(str(firstNameFromUI)+" "+str(lastNameFromUI))

    detail.append(str(userNameFromUI))

    ############################################ Setting Email #########################################################
    logger.info("Going to set Email =%s",userDetail['email'])
    emailFromUI= screenInstance.cm.sendkeys_input(userDetail['email'],h,0,child="email")
    checkEqualAssert(str(emailFromUI), str(userDetail['email']),message="Verify Entered Email")
    if not isColorValid(screenInstance, h, property=Constants.BORDERCOLOR,child='email', index=0):
        raise
    detail.append(str(emailFromUI))
    flag_email=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Email", screenInstance,setup)


    detail.append(str(userRole_text))
    detail.append(str(Constants.LASTMODIFYTEXTFORNEWUSER))

    ############################################ Setting Enabled/Disabled Slider #######################################
    sliderHandle=getHandle(setup,screenName,'allsliders')
    logger.info('Going to set enabled slider =%s for user =%s',userDetail['enabled'],userDetail['username'])
    colorOfEnabled=findPropertyColor(screenInstance,sliderHandle,property=Constants.BACKGROUNDCOLOR,parent='allsliders',child='slider',index=0)
    status=''
    if (userDetail['enabled']=="1" and str(colorOfEnabled)!=Constants.WHITECOLOR) or (userDetail['enabled']=="0" and str(colorOfEnabled)==Constants.WHITECOLOR):
        screenInstance.cm.click(sliderHandle['allsliders']['slider'][0])
        time.sleep(2)
        if findPropertyColor(screenInstance,sliderHandle,property=Constants.BACKGROUNDCOLOR,parent='allsliders',child='slider',index=0)==Constants.WHITECOLOR:
            status=Constants.ENABLED_STATUS
        else:
            status=Constants.DISABLED_STATUS
    elif userDetail['enabled']=="1" and str(colorOfEnabled)==Constants.WHITECOLOR:
        status=Constants.ENABLED_STATUS
    elif userDetail['enabled']!="1" and str(colorOfEnabled)!=Constants.WHITECOLOR:
        status = Constants.DISABLED_STATUS
    detail.append(status)

    ############################################ Setting Password/Confirm Password #####################################
    logger.info("Going to set Password =%s",userDetail['password'])
    passwordFromUI=screenInstance.cm.sendkeys_input(userDetail['password'],h,0,child="password")
    checkEqualAssert(str(passwordFromUI), str(userDetail['password']),message="Verify Entered Password")
    if not isColorValid(screenInstance, h,property=Constants.BORDERCOLOR,child='password', index=0):
        raise
    flag_password=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Password", screenInstance,setup)


    logger.info("Going to set Confirm Password =%s",userDetail['cpassword'])
    cpasswordFromUI = screenInstance.cm.sendkeys_input(userDetail['cpassword'], h,1,child="password")
    checkEqualAssert(str(cpasswordFromUI), str(userDetail['cpassword']),message="Verify Entered Confirm Password")
    if not isColorValid(screenInstance, h,property=Constants.BORDERCOLOR,child='password', index=1):
        raise
    flag_cpassword=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Confirm Password", screenInstance,setup)

    password=screenInstance.cm.getValue_input(h,0,child="password")
    cpassword=screenInstance.cm.getValue_input(h,1,child="password")
    checkEqualAssert(str(password), str(cpassword),message="Verify Password")

    ####################################################################################################################
    # logger.info("Going to set privileges =%s",userDetail['value'])
    # privileges_list=str(userDetail['value']).split(',')
    #
    # if UserRole=='1':
    #     if screenInstance.cm.isCheckBoxSelectedWithName_UMMural(h,Constants.UM_PARENT_WORKFLOWS)==1:
    #         screenInstance.cm.clickCheckBoxWithName_UMMural(h,Constants.UM_PARENT_WORKFLOWS,UserRole=UserRole,force=True)
    #     if screenInstance.cm.isCheckBoxSelectedWithName_UMMural(h, Constants.UM_PARENT_BULKSTATS_KPI)== 1:
    #         screenInstance.cm.clickCheckBoxWithName_UMMural(h, Constants.UM_PARENT_BULKSTATS_KPI, UserRole=UserRole, force=True)
    #
    #     for value in privileges_list:
    #         screenInstance.cm.clickCheckBoxWithName_UMMural(h,value,UserRole=UserRole)
    #
    # detailofcheckbox,checklist,unchecklist=screenInstance.cm.getAllCheckBoxElement_UMMural(getHandle(setup,MuralConstants.UserPopUpScreen,'allcheckboxes'))

    ####################################################################################################################

    button_status=dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword , "All Field",screenInstance,setup)

    if checkComplusoryFieldFlag:
        checkComplusoryField(setup,screenInstance,screenName,userDetail,button='Create')
        logger.info('Going to Click on Cancel Button')
        screenInstance.cm.clickButton("Cancel", getHandle(setup,screenName,'allbuttons'))
        return []

    if not button_status:
        logger.info("*************Create Button not enable**********")
        raise

    if button_status and button=="Cancel":
        logger.info('Going to Click on Cancel Button')
        screenInstance.cm.clickButton(button, getHandle(setup,screenName,'allbuttons'))
        return []

    if button_status and button=="Cross":
        logger.info("Going to Click on 'X' Button")
        screenInstance.clickIcon(getHandle(setup, screenName,'icons'),setup.d, child='closePopupIcon')
        return []

    if button_status and button=="Create":
        logger.info('Going to Click on %s Button with User details = %s',button,str(detail))
        click_status=screenInstance.cm.clickButton(button,getHandle(setup,screenName,"allbuttons"))
        checkEqualAssert(True,click_status,message="Verify clicked status of "+button)

        erroFlag,msg=errorMsgOnPopUp(setup,screenName)

        if erroFlag:
            checkEqualAssert(MRXConstants.MRX_SAME_USER_ERROR_MSG,msg,message="Verfiy error msg in case of Same Username")
            screenInstance.clickIcon(getHandle(setup,screenName,'icons'),setup.d)
            return []
        checkEqualAssert(0,len(getHandle(setup,screenName,'allbuttons')['allbuttons']['button']),message="Verify Popscreen close after click on button ="+button)
    logger.info('User created with details= %s',str(detail))
    return detail


def errorMsgOnPopUp(setup,screenName,parent='errorMsgContainer',child='msg'):
    time.sleep(5)
    errorMessage=''
    popUpHandle=getHandle(setup,screenName,parent)
    if len(popUpHandle[parent][child])!=0:
        r = "issue_" + str(random.randint(99999, 9999999)) + ".png"
        setup.d.save_screenshot(r)
        logger.debug("ERROR :: Screenshot with name = %s is saved", r)
        logger.error("Error msg found on Popup")
        errorMessage= str(popUpHandle[parent][child][0].text).strip()

        logger.error("Error Message = %s", errorMessage)
        resultlogger.info("ERROR :: Screenshot with name = %s is saved <br>", r)
        resultlogger.info("******* Error msg found = %s *******<br>", errorMessage)
        return True,errorMessage
    else:
        return False,errorMessage


def getUserDetailFromUI(setup,screenInstance,screenName):
    detail = []
    h = getHandle(setup,screenName,'allinputs')
    userRole_text = screenInstance.dropdown.getSelectionOnVisibleDropDown(getHandle(setup,screenName,'allselects'),index=0)

    userNameFromUI = str(h['allinputs']['input'][0].get_attribute('value'))

    firstNameFromUI = screenInstance.cm.getValue_input(h, 1)
    lastNameFromUI = screenInstance.cm.getValue_input( h, 2)
    detail.append((str(firstNameFromUI) + " " + str(lastNameFromUI)).strip(' '))
    detail.append(str(userNameFromUI))
    emailFromUI = screenInstance.cm.getValue_input(h, 0, child="email")
    detail.append(str(emailFromUI))

    detail.append(str(userRole_text))
    sliderHandle = getHandle(setup, screenName, 'allsliders')

    colorOfEnabled = findPropertyColor(screenInstance,sliderHandle, property=Constants.BACKGROUNDCOLOR, parent='allsliders',child='slider', index=0)
    if (str(colorOfEnabled) != Constants.WHITECOLOR) :
        status = Constants.DISABLED_STATUS
    else:
        status = Constants.ENABLED_STATUS

    detail.append(str(Constants.LASTMODIFYTEXTFORNEWUSER))
    detail.append(status)

    # detailofcheckbox, checklist, unchecklist = screenInstance.cm.getAllCheckBoxElement_UMMural(getHandle(setup,MuralConstants.UserPopUpScreen,'allcheckboxes'))

    return detail



def editUserDetail(setup,screenInstance,screenName,userDetail,button='Create'):
    detail = []

    ############################################ Updating User Role ####################################################
    logger.info("Going to update UserRole = %s for user = %s",userDetail['userrole'],userDetail['username'])
    userRole_text = screenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup,screenName,'allselects'), str(userDetail['userrole']), index=0)
    checkEqualAssert(str(userDetail['userrole']),userRole_text,message="Verify Edited User Role")

    ############################################ Getting Username #####################################################

    h = getHandle(setup, screenName, 'allinputs')
    logger.info("Going to Update detail of user =" + userDetail['username'])
    checkEqualAssert(False,h['allinputs']['input'][0].is_enabled(),message="On Edit Window, Username should not be editable")
    userNameFromUI = str(h['allinputs']['input'][0].get_attribute('value'))

    ############################################ Updating First/Last Name ##############################################
    firstNameFromUI = screenInstance.cm.sendkeys_input(userDetail['firstname'], h, 1)
    checkEqualAssert(str(firstNameFromUI), str(userDetail['firstname']),message="Verify Entered First Name, during Edit User")
    lastNameFromUI = screenInstance.cm.sendkeys_input(userDetail['lastname'], h, 2)
    checkEqualAssert(str(lastNameFromUI), str(userDetail['lastname']),message="Verify Entered Last Name, during Edit User")
    detail.append(str(firstNameFromUI) + " " + str(lastNameFromUI))
    detail.append(str(userNameFromUI))

    ############################################ Updating Email ########################################################
    logger.info("Going to set Email =%s" + userDetail['email'])
    emailFromUI = screenInstance.cm.sendkeys_input(userDetail['email'], h, 0, child="email")
    checkEqualAssert(str(emailFromUI), str(userDetail['email']),message="Verify Entered Email,during Edit User")
    if not isColorValid(screenInstance, h, property=Constants.BORDERCOLOR, child='email', index=0):
        raise
    detail.append(str(emailFromUI))
    detail.append(str(userRole_text))

    ################################### Updating Enabled/Disabled Slider (Status) ######################################

    sliderHandle = getHandle(setup, screenName, 'allsliders')
    status=''
    logger.info('Going to set enabled slider =%s for user =%s', userDetail['enabled'], userDetail['username'])
    colorOfEnabled = findPropertyColor(screenInstance, sliderHandle, property=Constants.BACKGROUNDCOLOR, parent='allsliders',child='slider', index=0)
    if (userDetail['enabled'] == "1" and str(colorOfEnabled) != Constants.WHITECOLOR) or (userDetail['enabled'] == "0" and str(colorOfEnabled) == Constants.WHITECOLOR):
        screenInstance.cm.click(sliderHandle['allsliders']['slider'][0])
        time.sleep(2)
        if findPropertyColor(screenInstance, sliderHandle, property=Constants.BACKGROUNDCOLOR, parent='allsliders', child='slider',index=0) == Constants.WHITECOLOR:
            status = Constants.ENABLED_STATUS
        else:
            status = Constants.DISABLED_STATUS
    elif userDetail['enabled'] == "1" and str(colorOfEnabled) == Constants.WHITECOLOR:
        status = Constants.ENABLED_STATUS
    elif userDetail['enabled'] != "1" and str(colorOfEnabled) != Constants.WHITECOLOR:
        status = Constants.DISABLED_STATUS


    import datetime
    utc = datetime.datetime.utcnow()
    dateString = utc.strftime(MRXConstants.TIMEPATTERN)
    detail.append(str(dateString))

    detail.append(status)

    ############################################ Updating Password #####################################################

    checkEqualAssert(False,h['allinputs']['password'][0].is_enabled(),message="With out click on 'Update Password', Password input box should be inactive on Edit window")
    logger.debug('Going to click on update Password')
    h['allinputs']['updatePwd'][0].click()

    logger.info("Going to update Password =%s", userDetail['password'])
    passwordFromUI = screenInstance.cm.sendkeys_input(userDetail['password'], h, 0, child="password")
    checkEqualAssert(str(passwordFromUI), str(userDetail['password']),message="Verify Entered Password,during Edit User")
    if not isColorValid(screenInstance, h, property=Constants.BORDERCOLOR, child='password', index=0):
        raise

    logger.info("Going to set Confirm Password =%s", userDetail['cpassword'])
    cpasswordFromUI = screenInstance.cm.sendkeys_input(userDetail['cpassword'], h, 1, child="password")
    checkEqualAssert(str(cpasswordFromUI), str(userDetail['cpassword']),message="Verify Entered Password,during Edit User")
    if not isColorValid(screenInstance, h, property=Constants.BORDERCOLOR, child='password', index=1):
        raise

    password = screenInstance.cm.getValue_input(h, 0, child="password")
    cpassword = screenInstance.cm.getValue_input(h, 1, child="password")
    checkEqualAssert(str(password), str(cpassword),message="Verify Password,during Edit User")

    ####################################################################################################################


    # logger.info("Going to set privileges =%s", userDetail['value'])
    # privileges_list = str(userDetail['value']).split(',')
    #
    # if UserRole == '1':
    #     if screenInstance.cm.isCheckBoxSelectedWithName_UMMural(h, Constants.UM_PARENT_WORKFLOWS) == 1:
    #         screenInstance.cm.clickCheckBoxWithName_UMMural(h, Constants.UM_PARENT_WORKFLOWS, UserRole=UserRole,force=True)
    #     if screenInstance.cm.isCheckBoxSelectedWithName_UMMural(h, Constants.UM_PARENT_BULKSTATS_KPI) == 1:
    #         screenInstance.cm.clickCheckBoxWithName_UMMural(h, Constants.UM_PARENT_BULKSTATS_KPI, UserRole=UserRole,force=True)
    #
    #     for value in privileges_list:
    #         screenInstance.cm.clickCheckBoxWithName_UMMural(h, value, UserRole=UserRole)
    #
    # detailofcheckbox, checklist, unchecklist = screenInstance.cm.getAllCheckBoxElement_UMMural(getHandle(setup,MuralConstants.UserPopUpScreen,'allcheckboxes'))

    ####################################################################################################################

    if button == "Cancel":
        logger.info('Going to Click on Cancel Button')
        screenInstance.cm.clickButton(button, getHandle(setup,screenName,'allbuttons'))
        return []

    if button == "Cross":
        logger.info("Going to Click on 'X' Button")
        screenInstance.clickIcon(getHandle(setup, screenName, 'icons'), setup.d, child='closePopupIcon')
        return []

    if button == "Update":
        logger.info('Going to Click on %s Button with details %s',button,str(detail))
        click_status = screenInstance.cm.clickButton(button, getHandle(setup,screenName,'allbuttons'))
        checkEqualAssert(True, click_status,message="Verify whether " + button + " button clicked or not")
        # flag, msg = confirm(setup)
        # if flag == True:
        #     h['icons']['closePopupIcon'][0].click()
        #     return []
        checkEqualAssert(0, len(getHandle(setup,screenName, 'allbuttons')['allbuttons']['button']),message="Verify Popscreen close after click on button =" + button)

    return detail


def verifySortingOnTable(setup,screenInstance,screenName,sortTableColumnTag,sortTableColumnInnerTag,parent='table',testcase_id=""):
    columns = setup.cM.getNodeElements(sortTableColumnTag, sortTableColumnInnerTag)
    column_names = []
    for k, column in columns.iteritems():
        column_names.append(column['locatorText'])

    tableHandle = getHandle(setup,screenName, parent)
    tableMap = screenInstance.table.getTableDataMap(tableHandle, driver=setup,colIndex=-1)

    if tableMap['rows'] == Constants.NODATA:
        logger.info("*********Table Data Not Present************")
        return

    for columnname in column_names:
        sortedData = sortTable(setup, screenInstance,screenName,columnName=columnname,testcase_id=testcase_id)
        resultlogger.debug('<br>*********** Logging Results for checkSortTable on Column %s ***********<br><br>',columnname)

        for k, v in sortedData.iteritems():
            if tableMap['rows'].has_key(k):
                checkEqualAssert(tableMap['rows'][k], sortedData[k],message="Verify sorted Table rows present in table with key : " + k)
            else:
                logger.info("********table not contain row with key********* : " + k)


def sortTable(setup,instance,screenName,columnName="Name",testcase_id=""):
    tableHandle = getHandle(setup,screenName, "table")
    instance.table.sortTable1(tableHandle,columnName)
    tableHandle = getHandle(setup,screenName, "table")

    data2 = instance.table.getTableData1(tableHandle)
    columnIndex = instance.table.getIndexForValueInArray(data2['header'], columnName)

    col = []
    for i in range(len(data2['rows'])):
        col.append(data2['rows'][i][columnIndex])

    checkEqualAssert(sorted(col,key=lambda s: s.lower(),reverse=True),col,message="Verify Sorting on Column: " + columnName,testcase_id=testcase_id)
    logger.info("Sorted")
    cdata2 = instance.table.convertDataToDictWithKeyAsRow(data2)
    return cdata2

# def verifyChangePasswordAndUserPrivileges(setup,screenInstance,handle,usersDetail,listOfPrivilegesFromTable,button='Change'):
#     ChangePassword(setup, screenInstance, handle, usersDetail, button=button)
#     if usersDetail['userrole']=='Admin' or (usersDetail['username']).lower=='admin':
#         listOfPrivilegesFromTable.append('User Management')
#         listOfPrivilegesFromTable.append('System Monitoring')
#
#     for Privileges in listOfPrivilegesFromTable:
#         privileges=Privileges.replace(' ','')
#         privileges =privileges.replace('/', '')
#         function="check"+privileges
#         getattr(CheckPrivileges(BasePageClass),function)(setup)


def validateMinimumPasswordRequirement(setup,screenName,parent='validatePasswordMsg',child='msg',index=0):
    logger.info("Method Called : validateMinimumPasswordRequirement")
    h=getHandle(setup,screenName,parent)
    if len(h[parent][child])>index:
        return str(h[parent][child][index].text).strip()
    else:
        return ""

def errorMsgOnChangePasswordPopup(setup,screenName,parent='errormsg',child='msg',index=0):
    logger.info("Method Called : errorMsgOnChangePasswordPopup")
    h = getHandle(setup, screenName, parent)
    if len(h[parent][child]) > index:
        return str(h[parent][child][index].text).strip(),True
    else:
        return "",False


def ChangePassword(setup,screenInstance,screenName,handle,usersDetail,button='Change'):
    if len(handle['allinputs']['password'])>0:
        flag_new_password = False
        flag_new_cpassword=False

        logger.info("Going to Enter Current Password =%s",usersDetail['currentpassword'])
        currentpasswordfromUI = screenInstance.cm.sendkeys_input(usersDetail['currentpassword'], handle,0,child='password')
        checkEqualAssert(str(currentpasswordfromUI), str(usersDetail['currentpassword']),message="Verify Current Password")

        flag_current_password = True
        dumpResultForButton(flag_current_password and flag_new_password and flag_new_cpassword , "Current Password", screenInstance, setup,button_label="Change")

        logger.info("Going to Enter New Password =%s",usersDetail['newpassword'])
        newpasswordFromUI = screenInstance.cm.sendkeys_input(usersDetail['newpassword'], handle,1, child="password")
        checkEqualAssert(str(newpasswordFromUI), str(usersDetail['newpassword']),message="Verify Entered Password")

        screenInstance.cm.sendkeys_input(Keys.TAB,handle,1,child="password",clear=False)
        msg=validateMinimumPasswordRequirement(setup,screenName)

        if msg!='':
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.info('Password = %s is not valid :: Screenshot save with name =%s',newpasswordFromUI,r)
            resultlogger.info('Password = %s is not valid :: Screenshot save with name =%s <br>',newpasswordFromUI,r)
            screenInstance.clickIcon(handle, setup.d, child='closePopupIcon')
            checkEqualAssert(True,msg!='',message="Minimum requirement for Password not satisfied :: Msg = "+str(msg))
            return msg,False

        flag_new_password = True
        dumpResultForButton(flag_current_password and flag_new_password and flag_new_cpassword, "New Password", screenInstance, setup,button_label="Change")

        logger.info("Going to set Confirm Password =%s", usersDetail['newcpassword'])
        newcpasswordFromUI = screenInstance.cm.sendkeys_input(usersDetail['newcpassword'],handle, 2, child="password")
        checkEqualAssert(str(newcpasswordFromUI), str(usersDetail['newcpassword']),message="Verify Entered Password")
        screenInstance.cm.sendkeys_input(Keys.TAB, handle, 2, child="password",clear=False)
        msg = validateMinimumPasswordRequirement(setup, screenName)
        if msg!= '':
            r = "issue_" + str(random.randint(0, 9999999)) + ".png"
            setup.d.save_screenshot(r)
            logger.info('Confirm Password = %s not match with New Password :: Screenshot save with name =%s', newcpasswordFromUI, r)
            resultlogger.info('Confirm Password = %s not match with New Password :: Screenshot save with name =%s <br>', newcpasswordFromUI, r)
            screenInstance.clickIcon(handle,setup.d,child='closePopupIcon')
            checkEqualAssert(MRXConstants.Passoword_Not_Matched,str(msg).strip(),message="Verify Password Mismatch Message")
            return msg,False

        flag_new_cpassword = True
        button_status = dumpResultForButton(flag_current_password and flag_new_password and flag_new_cpassword,"All Field on Change Password Screen", screenInstance, setup,button_label='Change')

        if button_status and button == "Change":
            click_status = screenInstance.cm.clickButton(button, handle)
            checkEqualAssert(True, click_status,message="Verify whether " + button + " button clicked or not")
            isError(setup)
            errorMsg,erroFlag=errorMsgOnChangePasswordPopup(setup,screenName)
            if erroFlag and errorMsg!='':
                r = "issue_" + str(random.randint(0, 9999999)) + ".png"
                setup.d.save_screenshot(r)
                logger.info('Error Found on Change Password Popup :: Screenshot save with name =%s',str(errorMsg),r)
                resultlogger.info('Error Found on Change Password Popup :: Screenshot save with name =%s <br>',str(errorMsg),r)
                screenInstance.cm.clickButton('Cancel',handle)
                checkEqualAssert(MRXConstants.Invalid_Current_Password,errorMsg,message="Verify invalid current password msg")
                return errorMsg,False

        if button == "Cancel":
            screenInstance.cm.clickButton(button, handle)
            return "Cancel",True

        return '',True

    else:
        logger.error("Handle for input type Password not Found")
        resultlogger.error("Handle for input (type =Password) not Found <br>")
        return '',False


def checkUMSwitchForUser(setup,exploreScreenInstance,workFlowInstance,adminFlag=True):
    try:
        moduleList=exploreScreenInstance.exploreList.getAvailableModule(getHandle(setup,Constants.VALIDATE_HEADER))
        for module in moduleList:
            exploreHandle = getHandle(setup,MRXConstants.ExploreScreen)
            if module=="WORKFLOWS":
                exploreScreenInstance.exploreList.launchModule(exploreHandle,module)
                workFlowInstance.launchScreen("Distribution", getHandle(setup, MRXConstants.WFSCREEN))
                time.sleep(5)
                exploreScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup,MRXConstants.BREADCRUMB_SCREEN))
                availableOptionOnWorkFlow=exploreScreenInstance.cm.availableOptionOnWorkFlowDrop(getHandle(setup,MRXConstants.BREADCRUMB_SCREEN))
                for screen in availableOptionOnWorkFlow:
                    exploreScreenInstance.cm.gotoScreenViaWorkFlowDrop_MRX(setup,str(screen),getHandle(setup, MRXConstants.BREADCRUMB_SCREEN))
                    time.sleep(5)
                    flag=checkUM(setup, exploreScreenInstance)
                    if ((not flag) and adminFlag) or (flag and (not adminFlag)):
                        return False,str(screen)
                    exploreScreenInstance.cm.activateWorkFlowDropDown(getHandle(setup, MRXConstants.BREADCRUMB_SCREEN))
            else:
                exploreScreenInstance.exploreList.launchModule(exploreHandle,module)
                isError(setup)
                flag = checkUM(setup, exploreScreenInstance)
                if ((not flag) and adminFlag) or (flag and (not adminFlag)):
                    return False, str(module)
        return True,''

    except Exception as e:
        logger.error("Got Exception during movement across Screen :: Exception =%s",str(e))
        return False,module

def checkUM(setup,exploreScreenInstance):
    exploreScreenInstance.exploreList.switchApp(getHandle(setup, MRXConstants.ExploreScreen, 'appHeader'))
    switchOption = exploreScreenInstance.exploreList.getAllApps(getHandle(setup, MRXConstants.ExploreScreen, 'switchApp'))
    if 'User Management' in switchOption:
        return True
    else:
        return False


def checkComplusoryField(setup,screenInstance,screenName,userDetail,button='Create'):
    ############################################ Checking UserName ######################################################
    h = getHandle(setup,screenName,'allinputs')
    logger.info("Going to Enter detail of user ="+userDetail['username'])
    logger.info("Going to set UserName =%s",userDetail['username'])

    screenInstance.cm.sendkeys_input('',h,0)
    dumpResultForButton(False,"Blank Username (Verifing complusory Field)",screenInstance, setup,testcase_id="MKR-3481")
    userNameFromUI = screenInstance.cm.sendkeys_input(userDetail['username'],h,0)

    ############################################ Checking First and Last Name ###########################################

    screenInstance.cm.sendkeys_input('', h, 1)
    dumpResultForButton(False, "Blank FirstName (Verifing complusory Field)", screenInstance, setup,testcase_id="MKR-3481")
    firstNameFromUI = screenInstance.cm.sendkeys_input(userDetail['firstname'], h, 1)

    screenInstance.cm.sendkeys_input('', h, 2)
    dumpResultForButton(False, "Blank LastName (Verifing complusory Field)", screenInstance, setup,testcase_id="MKR-3481")
    lastNameFromUI = screenInstance.cm.sendkeys_input(userDetail['lastname'], h, 2)

    ############################################ Checking Email #########################################################
    screenInstance.cm.sendkeys_input('', h, 0,child="email")
    dumpResultForButton(False, "Blank Email (Verifing complusory Field)", screenInstance, setup,testcase_id="MKR-3481")
    emailFromUI= screenInstance.cm.sendkeys_input(userDetail['email'],h,0,child="email")

    ############################################ Checking Password/Confirm Password #####################################
    screenInstance.cm.sendkeys_input('', h, 0,child='password')
    dumpResultForButton(False, "Blank Password (Verifing complusory Field)", screenInstance, setup,testcase_id="MKR-3481")
    passwordFromUI=screenInstance.cm.sendkeys_input(userDetail['password'],h,0,child="password")

    screenInstance.cm.sendkeys_input('', h, 1,child='password')
    dumpResultForButton(False, "Blank Confirm Password (Verifing complusory Field)", screenInstance, setup,testcase_id="MKR-3481")
    cpasswordFromUI = screenInstance.cm.sendkeys_input(userDetail['cpassword'], h,1,child="password")
    return




def setRoleDetails(screenInstance, setup, k='0',screen=UMConstants.UMPOPUP_ADDROLE,values={},button1='Create',button2='Cancel',condition1=False,condition2=True):
    logger.info("Method Called : setRoleDetails")
    createBtnStatus = False
    dumpResultForButton(condition2, " When no property is set", button_label=button2, screenInstance=screenInstance, setup=setup,screen=screen,testcase_id='Reflex-UM-12')


    #################### Enter Role Name
    handle = getHandle(setup, screen, 'allinputs')
    logger.info("Going to set Role Name =" +values['rolename'])
    roleNameToBeEntered = str(values['rolename'])
    screenInstance.cm.sendkeys_input(roleNameToBeEntered, handle, index=0)
    createBtnStatus = dumpResultForButton(condition1,"Role Name", button_label=button1,screenInstance=screenInstance, setup=setup,screen=screen,testcase_id='Reflex-UM-11')
    dumpResultForButton(condition2, "Role Name", button_label=button2, screenInstance=screenInstance, setup=setup, screen=screen,testcase_id='Reflex-UM-12')


    #################### Set Privileges
    # Expand tree if collapsed
    handle = getHandle(setup, screen, "tree")
    if len(handle['tree']['treeCollapser']) > 0:
        logger.debug("Tree Toggle buttons are in collapsed state under privileges section on add role popup")
        for x in range(len(handle['tree']['treeCollapser'])):
            screenInstance.click(handle['tree']['treeCollapser'][x])

    else:
        logger.debug("Tree Toggle buttons are already in expanded state under privileges section on add role popup")


    ## Clear selection if any
    handle = getHandle(setup, screen, "tree")
    for x in range(len(handle['tree']['checkboxes'])):
        if handle['tree']['checkboxes'][x].is_selected():
            screenInstance.click(handle['tree']['checkboxes'][x])

    # Set selection
    checkBoxesListToBeChecked =[]
    applicationPrivilegesDict = setup.cM.getNodeElements("applicationPrivileges", "privilege")
    checkBoxIndexListToBeChecked  = [int(index.strip()) for index in values['applicationprivileges'].split(",")]
    for index in checkBoxIndexListToBeChecked:
        screenInstance.click(getHandle(setup, screen,'tree')['tree']['checkboxes'][index])
        checkBoxesListToBeChecked += [applicationPrivilegesDict[str(index)]['name'].strip()]

    createBtnStatus = dumpResultForButton(condition2, "Application Privileges", button_label=button1, screenInstance=screenInstance, setup=setup,screen=screen,testcase_id='Reflex-UM-11')
    dumpResultForButton(condition2, "Application Privileges", button_label=button2, screenInstance=screenInstance, setup=setup, screen=screen,testcase_id='Reflex-UM-12')

    return roleNameToBeEntered, checkBoxesListToBeChecked , createBtnStatus


def getRoleDetails(screenInstance, setup,screen=UMConstants.UMPOPUP_ADDROLE):
    handle = getHandle(setup, screen, 'allinputs')
    roleNameFromUI = str(screenInstance.cm.getValue_input(handle, 0))

    handle = getHandle(setup, screen, "tree")
    checkedCheckBoxesListFromUI = []
    for x in range(len(handle['tree']['checkboxes'])):
        if handle['tree']['checkboxes'][x].is_selected():
            checkedCheckBoxesListFromUI += [str(handle['tree']['checkboxes'][x].find_element_by_xpath("..").text)]


    return roleNameFromUI , checkedCheckBoxesListFromUI


def clickOnPopupIcon(setup,h,screen,parent='filterArea',child='icon'):
    logger.info("Clicking on FilterIcon")
    try:
        javaScript_str = "var evObj = document.createEvent('MouseEvents');" + "evObj.initMouseEvent(\"mouseover\",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);" + "arguments[0].dispatchEvent(evObj);"
        setup.d.execute_script(javaScript_str, h[parent][child][0])
        time.sleep(2)
        h[parent][child][0].click()
    except:
        logger.info('Not able to click on = %s',child)
        resultlogger.info('Not able to click on = %s', child)
        return False
    return True




def editRole(setup,tableHandle,screenInstance,screen,columnValueInRowToBeEdited,roleDetail,k='0', colIndex=0):
    expectedRoleName, expectedCheckedCheckBoxesList, createBtnStatus = "","",""

    column_ValuesFromTable = screenInstance.table.getColumnValueFromTable(colIndex, tableHandle)
    if columnValueInRowToBeEdited in column_ValuesFromTable:
        for header in tableHandle['table']['HEADERROW']:
            if str(header.text) == "Edit":
                indexForColumnEdit = tableHandle['table']['HEADERROW'].index(header)
                break
        for value in column_ValuesFromTable:
            if value == columnValueInRowToBeEdited:
                indexColumnValueForRowToBeEdited = screenInstance.table.getIndexForValueInArray1(column_ValuesFromTable,value)
                elem = tableHandle['table']['ROWS'][indexColumnValueForRowToBeEdited * len(tableHandle['table']['HEADERROW']) + indexForColumnEdit]
                screenInstance.click(elem)
                break
        expectedRoleName, expectedCheckedCheckBoxesList, createBtnStatus = setRoleDetails(screenInstance=screenInstance,setup=setup, k=k,screen=UMConstants.UMPOPUP_ADDROLE,values=roleDetail,button1='Update',condition1=True)
    else:
        logger.info("Input Column value for row to be edited not found at column index " +str(colIndex) + " under manage roles table")


    return expectedRoleName, expectedCheckedCheckBoxesList, createBtnStatus


def deleteRole(setup,tableHandle,screenInstance,columnValueInRowToBeDeleted,parentScreen=UMConstants.UMSCREEN_MANAGEROLES,screen=UMConstants.UMPOPUP_DELETEROLE,colIndex=0):
    column_ValuesFromTable = screenInstance.table.getColumnValueFromTable(colIndex, tableHandle)
    if columnValueInRowToBeDeleted in column_ValuesFromTable:
        for header in tableHandle['table']['HEADERROW']:
            if str(header.text) == "Delete":
                indexForColumnEdit = tableHandle['table']['HEADERROW'].index(header)
                break
        for value in column_ValuesFromTable:
            if value == columnValueInRowToBeDeleted:
                indexColumnValueForRowToBeDeleted = screenInstance.table.getIndexForValueInArray1(column_ValuesFromTable,value)
                elem = tableHandle['table']['ROWS'][indexColumnValueForRowToBeDeleted * len(tableHandle['table']['HEADERROW']) + indexForColumnEdit]
                screenInstance.click(elem)
                dumpResultForButton(True, "Delete role", button_label="Cancel",screenInstance=screenInstance, setup=setup, screen=screen,testcase_id='Reflex-UM-185')
                dumpResultForButton(True, "Delete role", button_label="Ok",screenInstance=screenInstance, setup=setup, screen=screen,testcase_id='Reflex-UM-186')
                handle = getHandle(setup, screen, 'allbuttons')
                logger.debug("Going to click on 'Ok' buttton on delete role popup ")
                screenInstance.hoverAndClickButton(setup, "Ok", handle)
                break
    else:
        logger.info("Input Column value for row to be deleted not found at column index " +str(colIndex) + " under manage roles table")


