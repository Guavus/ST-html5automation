from Utils.utility import *
from UMUtils.UMConstants import *



def dumpResultForButton(condition,request,screenInstance,setup,button_label="Create",screen=UMConstants.UMPOPUP_ADDROLE,testcase_id="",parent="allbuttons",child="button"):
    button_status=screenInstance.cm.isButtonEnabled(button_label,getHandle(setup,screen,parent))
    checkEqualAssert(condition,button_status,message="Checking State of Button '" + button_label + "' for Fields entered : "+str(request),testcase_id=testcase_id)
    return button_status



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



def setRoleDetails(screenInstance, setup, k='0',screen=UMConstants.UMPOPUP_ADDROLE,roleDetail={},button1='Create',button2='Cancel',condition1=False,condition2=True):
    logger.info("Method Called : setRoleDetails")
    createBtnStatus = False
    roleNameFromUI = ""

    dumpResultForButton(condition2, " When no property is set", button_label=button2, screenInstance=screenInstance, setup=setup,screen=screen,testcase_id='Reflex-UM-12')


    #################### Enter Role Name
    handle = getHandle(setup, screen, 'allinputs')
    logger.info("Going to set Role Name =" +roleDetail['rolename'])
    roleNameToBeEntered = str(roleDetail['rolename'])
    roleNameFromUI = screenInstance.cm.sendkeys_input(roleNameToBeEntered, handle, index=0)
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
    checkBoxIndexListToBeChecked  = [int(index.strip()) for index in roleDetail['applicationprivileges'].split(",")]
    for index in checkBoxIndexListToBeChecked:
        screenInstance.click(getHandle(setup, screen,'tree')['tree']['checkboxes'][index])
        checkBoxesListToBeChecked += [applicationPrivilegesDict[str(index)]['name'].strip()]


    # Get Selection from UI
    handle = getHandle(setup, screen, "tree")
    checkedCheckBoxesListFromUI = []
    for x in range(len(handle['tree']['checkboxes'])):
        if handle['tree']['checkboxes'][x].is_selected():
            checkedCheckBoxesListFromUI += [str(handle['tree']['checkboxes'][x].find_element_by_xpath("..").text)]


    createBtnStatus = dumpResultForButton(condition2, "Application Privileges", button_label=button1, screenInstance=screenInstance, setup=setup,screen=screen,testcase_id='Reflex-UM-11')
    dumpResultForButton(condition2, "Application Privileges", button_label=button2, screenInstance=screenInstance, setup=setup, screen=screen,testcase_id='Reflex-UM-12')


    return roleNameToBeEntered, checkBoxesListToBeChecked, roleNameFromUI, checkedCheckBoxesListFromUI , createBtnStatus


def clickOnPopupIcon(setup,h,screen,parent='filterArea',child='icon'):
    logger.info("Clicking on FilterIcon")
    try:
        javaScript_str = "var evObj = document.createEvent('MouseEvents');" + "evObj.initMouseEvent(\"mouseover\",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);" + "arguments[0].dispatchEvent(evObj);"
        setup.d.execute_script(javaScript_str, h[parent][child][0])
        time.sleep(2)
        h[parent][child][0].click()
    except:
        logger.info('Not able to click on = %s',child)
        return False
    return True




def editRole(setup,tableHandle,screenInstance, columnValueInRowToBeEdited,roleDetail,parentscreen=UMConstants.UMSCREEN_MANAGEROLES,screen=UMConstants.UMPOPUP_ADDROLE,k='0', colIndex=0):
    click_status = False
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
                elem_classname = elem.find_element_by_css_selector("div.buttonContainer").find_element_by_tag_name('span').get_attribute('class')
                if "disable" not in elem_classname.lower():
                    click_status = True
                break

        if click_status and columnValueInRowToBeEdited != 'Admin' :
            try:
                expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, updateBtnStatus = setRoleDetails(screenInstance=screenInstance,setup=setup, k=k,screen=screen,roleDetail=roleDetail,button1='Update',condition1=True)
            except Exception as e:
                logger.info("Got Exception on creating a role inside editRole method when executed scenario" + str(k) + " : " + str(e))
                expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, updateBtnStatus = str(roleDetail['rolename']), [int(index.strip()) for index in roleDetail['applicationprivileges'].split(",")], "", "", False

        elif click_status and columnValueInRowToBeEdited == 'Admin':
            handle = getHandle(setup, screen, 'allbuttons')
            if len(handle['allbuttons']['button']) > 0:
                screenInstance.hoverAndClickButton(setup, "Cancel", handle)

    else:
        logger.info("Input Column value for row to be edited not found at column index " +str(colIndex) + " under manage roles table")


    return click_status, expectedRoleName, expectedCheckedCheckBoxesList, roleNameFromUI, checkedCheckBoxesListFromUI, updateBtnStatus


def deleteRole(setup,tableHandle,screenInstance,columnValueInRowToBeDeleted,parentScreen=UMConstants.UMSCREEN_MANAGEROLES,screen=UMConstants.UMPOPUP_CONFIRM_DELETEROLE,colIndex=0):
    click_status = False
    click_status_fromDelPopup = False
    popup_disappear_status = ""
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
                elem_classname = elem.find_element_by_css_selector("div.buttonContainer").find_element_by_tag_name('span').get_attribute('class')
                if "disable"  not in elem_classname.lower():
                    click_status = True
                break

        if click_status and columnValueInRowToBeDeleted != 'Admin':
            dumpResultForButton(True, "Delete role confirmation", button_label="Cancel",screenInstance=screenInstance, setup=setup, screen=screen,testcase_id='Reflex-UM-185')
            dumpResultForButton(True, "Delete role confirmation", button_label="Ok",screenInstance=screenInstance, setup=setup, screen=screen,testcase_id='Reflex-UM-186')
            handle = getHandle(setup, screen, 'allbuttons')
            logger.debug("Going to click on 'Ok' buttton on delete role popup ")
            click_status_fromDelPopup = screenInstance.hoverAndClickButton(setup, "Ok", handle)
            handle = getHandle(setup, screen, 'allbuttons')
            popup_disappear_status = (len(handle['allbuttons']['button']) == 0)

        elif click_status and columnValueInRowToBeDeleted == 'Admin':
            handle = getHandle(setup, screen, 'allbuttons')
            if len(handle['allbuttons']['button']) > 0:
                screenInstance.hoverAndClickButton(setup, "Cancel", handle)


    else:
        logger.info("Input Column value for row to be deleted not found at column index " +str(colIndex) + " under manage roles table")
        return click_status, False, click_status_fromDelPopup, popup_disappear_status



    if click_status_fromDelPopup != True:
        click_status_fromDelPopup = False


    return click_status, True, click_status_fromDelPopup, popup_disappear_status





def findPropertyColor(screenInstance,h,property,parent="allinputs",child="input",index=0):
    propertycolor=str(h[parent][child][index].value_of_css_property(property))
    return screenInstance.cm.rgb_to_hex(propertycolor)




def isColorValid(screenInstance, h, property, parent="allinputs", child='input', index=0):
    #h[parent][child][index].send_keys(Keys.TAB)
    bordercolor=findPropertyColor(screenInstance,h, property,parent=parent,child=child,index=index)
    if str(bordercolor)==Constants.REDCOLOR:
        logger.debug(" Invalid %s =%s",str(h[parent][child][index].get_attribute('placeholder')),str(h[parent][child][index].get_attribute('value')))
        resultlogger.debug(" Invalid Entry =%s <br>",str(h[parent][child][index].get_attribute('value')))
        return False
    else:
        return True




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




def setUserDetail(setup,screenInstance,screenName,userDetail,button='Create',checkComplusoryFieldFlag=False,check_TimezoneDropdownList_Flag=False):
    detail={}
    flag_fname=False
    flag_lname=False
    flag_email = False
    flag_password = False
    flag_cpassword = False

    ############################################ Setting User Role #####################################################

    logger.info("Going to select UserRole for user ="+userDetail['username'])
    userRole_text = screenInstance.dropdown.doSelectionOnVisibleDropDown(getHandle(setup,screenName,'allselects'), str(userDetail['userrole']), index=0)
    checkEqualAssert(str(userDetail['userrole']), userRole_text,message="Verify selected User Role")

    detail['userrole'] = str(userRole_text)

    ############################################ Setting UserName ######################################################
    h = getHandle(setup,screenName,'allinputs')
    logger.info("Going to Enter detail of user ="+userDetail['username'])
    logger.info("Going to set UserName =%s",userDetail['username'])

    userNameFromUI = screenInstance.cm.sendkeys_input(userDetail['username'],h,0)
    checkEqualAssert(str(userNameFromUI),str(userDetail['username']),message="Verify Entered User Name")
    if not isColorValid(screenInstance, h,property=Constants.BORDERTOPCOLOR, index=0):
        raise Exception
    flag_usename=True
    dumpResultForButton(flag_usename and flag_fname and flag_lname and flag_email and flag_password and flag_cpassword, "UserName", screenInstance,setup)

    detail['username'] = str(userNameFromUI)

    ############################################ Setting First and Last Name ###########################################

    firstNameFromUI = screenInstance.cm.sendkeys_input(userDetail['firstname'], h, 1)
    checkEqualAssert(str(firstNameFromUI), str(userDetail['firstname']),message="Verify Entered First Name")
    if not isColorValid(screenInstance, h,property=Constants.BORDERTOPCOLOR, index=1):
        raise Exception
    flag_fname=True
    dumpResultForButton(flag_usename and flag_fname and flag_lname and flag_email and flag_password and flag_cpassword,"First Name", screenInstance, setup)

    lastNameFromUI = screenInstance.cm.sendkeys_input(userDetail['lastname'], h, 2)
    checkEqualAssert(str(lastNameFromUI), str(userDetail['lastname']),message="Verify Entered Last Name")
    if not isColorValid(screenInstance, h,property=Constants.BORDERTOPCOLOR, index=2):
        raise Exception
    flag_lname=True
    dumpResultForButton(flag_usename and flag_fname and flag_lname and flag_email and flag_password and flag_cpassword,"Last Name", screenInstance, setup)


    detail['name'] = str(firstNameFromUI)+" "+str(lastNameFromUI)

    ############################################ Setting Email #########################################################
    logger.info("Going to set Email =%s",userDetail['email'])
    emailFromUI= screenInstance.cm.sendkeys_input(userDetail['email'],h,0,child="email")
    checkEqualAssert(str(emailFromUI), str(userDetail['email']),message="Verify Entered Email")
    if not isColorValid(screenInstance, h, property=Constants.BORDERTOPCOLOR,child='email', index=0):
        raise Exception

    detail['email'] = str(emailFromUI)
    flag_email=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Email", screenInstance,setup)


    detail['lastmodified'] = str(Constants.LASTMODIFYTEXTFORNEWUSER)


    ########################################### Setting Timezone #######################################################
    logger.info("Going to set timezone =%s", userDetail['timezone'])
    timezone_handle =  getHandle(setup, screenName, 'allselects')

    selectedTimezoneFromUI = screenInstance.dropdown.doSelectionOnVisibleDropDown(timezone_handle,str(userDetail['timezone']), index=1)
    checkEqualAssert(str(userDetail['timezone']), str(selectedTimezoneFromUI), message="Verify Selected Timezone")

    if check_TimezoneDropdownList_Flag:
        timezoneDropdownListFromUI = []
        timezoneDropdownListFromUI += [str(timezone) for timezone in timezone_handle['allselects']['select'][1].text.split("\n")]
        checkEqualAssert(str(UMConstants.EXPECTED_TIMEZONE_LIST), str(timezoneDropdownListFromUI), message="Verify available timezone options in dropdown",testcase_id='Reflex-UM-266')


    detail['timezone'] = str(selectedTimezoneFromUI)
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Timezone", screenInstance,setup)

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

    detail['sliderstatus'] = status

    ############################################ Setting Password/Confirm Password #####################################
    logger.info("Going to set Password =%s",userDetail['password'])
    passwordFromUI=screenInstance.cm.sendkeys_input(userDetail['password'],h,0,child="password")
    checkEqualAssert(str(passwordFromUI), str(userDetail['password']),message="Verify Entered Password")
    if not isColorValid(screenInstance, h,property=Constants.BORDERTOPCOLOR,child='password', index=0):
        raise Exception
    flag_password=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Password", screenInstance,setup)


    logger.info("Going to set Confirm Password =%s",userDetail['cpassword'])
    cpasswordFromUI = screenInstance.cm.sendkeys_input(userDetail['cpassword'], h,1,child="password")
    checkEqualAssert(str(cpasswordFromUI), str(userDetail['cpassword']),message="Verify Entered Confirm Password")
    if not isColorValid(screenInstance, h,property=Constants.BORDERTOPCOLOR,child='password', index=1):
        raise Exception
    flag_cpassword=True
    dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword, "Confirm Password", screenInstance,setup)

    password=screenInstance.cm.getValue_input(h,0,child="password")
    cpassword=screenInstance.cm.getValue_input(h,1,child="password")
    checkEqualAssert(str(password), str(cpassword),message="Verify Password")
    detail['password'] = str(password)
    detail['cpassword'] = str(cpassword)

    button_status=dumpResultForButton(flag_usename and flag_email and flag_password and flag_cpassword , "All Field",screenInstance,setup)

    if checkComplusoryFieldFlag:
        checkComplusoryField(setup,screenInstance,screenName,userDetail,button='Create')
        logger.info('Going to Click on Cancel Button')
        screenInstance.cm.clickButton("Cancel", getHandle(setup,screenName,'allbuttons'))
        return []

    if not button_status:
        logger.info("*************Create Button not enable**********")
        raise Exception

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
            checkEqualAssert(UMConstants.SAME_USER_ERROR_MSG,msg,message="Verfiy error msg in case of Same Username")
            screenInstance.clickIcon(getHandle(setup,screenName,'icons'),setup.d)
            return detail, not erroFlag
        checkEqualAssert(0,len(getHandle(setup,screenName,'allbuttons')['allbuttons']['button']),message="Verify Popscreen close after click on button ="+button)
    logger.info('User created with details= %s',str(detail))
    return detail, not erroFlag





def editUser(setup,tableHandle,screenInstance,userDetail,k,targetUser_Username,actionUser,targetUser,parentscreen=UMConstants.UMSCREEN_MANAGEUSERS,screen=UMConstants.UMPOPUP_ADDUSER, colIndex=0):
    click_status_edit, updateBtn_status = False, False
    column_ValuesFromTable = screenInstance.table.getColumnValueFromTable(colIndex, tableHandle)
    if targetUser_Username in column_ValuesFromTable:
        for header in tableHandle['table']['HEADERROW']:
            if str(header.text) == "Edit":
                indexForColumnEdit = tableHandle['table']['HEADERROW'].index(header)
                break
        for value in column_ValuesFromTable:
            if value == targetUser_Username:
                indexColumnValueForRowToBeEdited = screenInstance.table.getIndexForValueInArray1(column_ValuesFromTable,value)
                elem = tableHandle['table']['ROWS'][indexColumnValueForRowToBeEdited * len(tableHandle['table']['HEADERROW']) + indexForColumnEdit]
                screenInstance.click(elem)
                elem_classname = elem.find_element_by_css_selector("div.buttonContainer").find_element_by_tag_name('span').get_attribute('class')
                if "disable" not in elem_classname.lower():
                    click_status_edit = True
                break


        modifiableFieldsDictFromUI = {"username": "disabled", "fname": "disabled", "lname": "disabled", "email": "disabled", "updatePasswordLink":"disabled",
                            "password": "disabled", "cpassword": "disabled", "userrole": "disabled",
                            "timezone": "disabled", "slider": "disabled"}



        condition = (actionUser != "superadmin" and targetUser != 'superadmin')  or ("adminuser" not in actionUser and targetUser != "superadmin")

        if click_status_edit  and condition:

            handle = getHandle(setup,screen,'allinputs')

            ## Check if input field for username is enabled
            if handle['allinputs']['input'][0].is_enabled():
                modifiableFieldsDictFromUI['username'] = 'enabled'
                screenInstance.cm.sendkeys_input(userDetail['username'], handle, 0)


            ## Check if input field for firstname is enabled
            if handle['allinputs']['input'][1].is_enabled():
                modifiableFieldsDictFromUI['fname'] = 'enabled'
                screenInstance.cm.sendkeys_input(userDetail['firstname'], handle, 1)

            ## Check if input field for lastname is enabled
            if handle['allinputs']['input'][2].is_enabled():
                modifiableFieldsDictFromUI['lname'] = 'enabled'
                screenInstance.cm.sendkeys_input(userDetail['lastname'], handle, 2)

            ## Check if input field for email is enabled
            if handle['allinputs']['email'][0].is_enabled():
                modifiableFieldsDictFromUI['email'] = 'enabled'
                screenInstance.cm.sendkeys_input(userDetail['email'], handle, 0,child='email')

            ## Check if input field for Update password Link is enabled
            click_status = screenInstance.click(getHandle(setup, screen, 'allinputs')['allinputs']['updatePwd'][0])
            if click_status == True:
                modifiableFieldsDictFromUI['updatePasswordLink'] = 'enabled'

            ## Check if input field for Password is enabled
            if handle['allinputs']['password'][0].is_enabled():
                modifiableFieldsDictFromUI['password'] = 'enabled'
                newPassword = str(screenInstance.cm.sendkeys_input(userDetail['newpassword'], handle, 0, child='password'))
                currentPassword = userDetail['currentpassword']

                if newPassword == currentPassword:
                    bgColor_status = isColorValid(screenInstance, h=handle, property=Constants.BORDERTOPCOLOR, child='password', index=0)
                    checkEqualAssert(str([currentPassword,False]), str([newPassword,bgColor_status]),message="Verify that on updating one's password, current password cannot be set as new password . Password  update policy is to followed.", testcase_id="Reflex-UM-238")

            ## Check if input field for Confirm password is enabled
            if handle['allinputs']['password'][1].is_enabled():
                modifiableFieldsDictFromUI['cpassword'] = 'enabled'
                screenInstance.cm.sendkeys_input(userDetail['newcpassword'], handle, 1, child='password')


            ## Check if input field for Role is enabled
            handle = getHandle(setup, screen, 'allselects')
            if handle['allselects']['select'][0].is_enabled():
                modifiableFieldsDictFromUI['userrole'] = 'enabled'
                screenInstance.dropdown.doSelectionOnVisibleDropDown(handle,str(userDetail['userrole']), index=0)

            ## Check if input field for timezone is enabled
            if handle['allselects']['select'][1].is_enabled():
                modifiableFieldsDictFromUI['timezone'] = 'enabled'
                screenInstance.dropdown.doSelectionOnVisibleDropDown(handle,str(userDetail['timezone']),index=1)


            ## Check if input slider  is enabled
            label_classname = setup.d.find_element_by_css_selector("div.switchContainer").find_element_by_tag_name("label").get_attribute("class")
            if "disable" in label_classname.lower():
                modifiableFieldsDictFromUI['slider'] = Constants.DISABLED_STATUS
            else:
                modifiableFieldsDictFromUI['slider'] = Constants.ENABLED_STATUS



            updateBtn_status = dumpResultForButton(True, "Edit user", button_label="Update", screenInstance=screenInstance, setup=setup,screen=screen, testcase_id='')
            screenInstance.hoverAndClickButton(setup, "Cancel",getHandle(setup, screen, 'allbuttons'))

        elif click_status_edit and not condition:
            handle = getHandle(setup, screen, 'allbuttons')
            if len(handle['allbuttons']['button']) > 0:
                screenInstance.hoverAndClickButton(setup, "Cancel", handle)

    else:
        logger.info("Input Column value for row to be edited not found at column index " + str(colIndex) + " under manage users table")

    return click_status_edit, sorted(modifiableFieldsDictFromUI.iteritems()),updateBtn_status









def deleteUser(setup, tableHandle, screenInstance, k,targetUser_Username,actionUser,targetUser, parentscreen=UMConstants.UMSCREEN_MANAGEUSERS,screen=UMConstants.UMPOPUP_CONFIRM_DELETEROLE, colIndex = 0):
    click_status = False
    click_status_fromDelPopup = False
    popup_disappear_status = False
    column_ValuesFromTable = screenInstance.table.getColumnValueFromTable(colIndex, tableHandle)
    if targetUser_Username in column_ValuesFromTable:
        for header in tableHandle['table']['HEADERROW']:
            if str(header.text) == "Delete":
                indexForColumnEdit = tableHandle['table']['HEADERROW'].index(header)
                break
        for value in column_ValuesFromTable:
            if value == targetUser_Username:
                indexColumnValueForRowToBeEdited = screenInstance.table.getIndexForValueInArray1(column_ValuesFromTable,value)
                elem = tableHandle['table']['ROWS'][indexColumnValueForRowToBeEdited * len(tableHandle['table']['HEADERROW']) + indexForColumnEdit]
                screenInstance.click(elem)
                elem_classname = elem.find_element_by_css_selector("div.buttonContainer").find_element_by_tag_name('span').get_attribute('class')
                if "disable" not in elem_classname.lower():
                    click_status = True
                break


        condition =  (actionUser != "superadmin" and targetUser != 'superadmin') or ("adminuser" not in actionUser and targetUser != "superadmin")  or ("adminuser" not in actionUser and "adminuser" not in targetUser and actionUser != targetUser)
        if click_status and condition:

            dumpResultForButton(True, "Delete user confirmation", button_label="Cancel", screenInstance=screenInstance, setup=setup,screen=screen, testcase_id='')
            dumpResultForButton(True, "Delete user confirmation", button_label="Ok", screenInstance=screenInstance, setup=setup,screen=screen, testcase_id='')
            handle = getHandle(setup, screen, 'allbuttons')
            logger.debug("Going to click on 'Ok' buttton on delete user popup ")
            click_status_fromDelPopup = screenInstance.hoverAndClickButton(setup, "Ok", handle)
            handle = getHandle(setup, screen, 'allbuttons')
            popup_disappear_status = (len(handle['allbuttons']['button']) == 0)

        elif click_status and not condition:
            handle = getHandle(setup, screen, 'allbuttons')
            if len(handle['allbuttons']['button']) > 0:
                screenInstance.hoverAndClickButton(setup, "Cancel", handle)

    else:
        logger.info("Input Column value for row to be deleted not found at column index " +str(colIndex) + " under manage users table")
        return click_status, False, click_status_fromDelPopup, popup_disappear_status


    if click_status_fromDelPopup != True:
        click_status_fromDelPopup = False

    return  click_status,True,click_status_fromDelPopup,popup_disappear_status



def enable_DisabledIcons(setup, tableHandle,screenInstance,valueUnderAction,tableHeader_text="Edit", colIndex=0):
    elem = ""
    column_ValuesFromTable = screenInstance.table.getColumnValueFromTable(colIndex, tableHandle)

    if valueUnderAction in column_ValuesFromTable:
        for header in tableHandle['table']['HEADERROW']:
            if str(header.text) == str(tableHeader_text):
                indexForColumnEdit = tableHandle['table']['HEADERROW'].index(header)
                break
        for value in column_ValuesFromTable:
            if value == valueUnderAction:
                indexColumnValueForRowToBeEdited = screenInstance.table.getIndexForValueInArray1(column_ValuesFromTable, value)
                tableElem_cell = tableHandle['table']['ROWS'][indexColumnValueForRowToBeEdited * len(tableHandle['table']['HEADERROW']) + indexForColumnEdit]
                elem = tableElem_cell.find_element_by_css_selector("div.buttonContainer").find_element_by_tag_name('span')
                if "disable" in elem.get_attribute('class').lower():
                    setup.d.execute_script("arguments[0].classList.remove('iconStyleDisable');", elem)
                    break


    return elem




def check_element_enabled(setup,element, expected_ele_state,request, attribute_to_find='class',testcase_id=""):
    ele_state = ""
    try:
        attribute_name = str(element.get_attribute(attribute_to_find))
        if attribute_name != "":
            logger.info("Successfully got attribute "+str(attribute_to_find) + "for the element")
            if "disable" in attribute_name.lower():
                ele_state = Constants.DISABLED_STATUS
            else:
                ele_state = Constants.ENABLED_STATUS
        else:
            logger.info("Could not get attribute " + str(attribute_to_find) + "for the element")
    except :
        logger.info(" Could not get attribute " + str(attribute_to_find) + " for the element" )

    finally:
        checkEqualAssert(expected_ele_state, ele_state, message="Checking State of Element for Fields entered : " + str(request),testcase_id=testcase_id)
        return ele_state



def validateMinimumPasswordRequirement(setup,screenName,parent='validatePasswordMsg',child='msg',index=0):
    logger.info("Method Called : validateMinimumPasswordRequirement")
    h=getHandle(setup,screenName,parent)
    if len(h[parent][child])>index:
        return str(h[parent][child][index].text).strip()
    else:
        return ""



def errorMsgOnChangePasswordPopup(setup,screenName,parent='ErrorMsg',child='msg',index=0):
    logger.info("Method Called : errorMsgOnChangePasswordPopup")
    h = getHandle(setup, screenName, parent)
    if len(h[parent][child]) > index:
        return str(h[parent][child][index].text).strip(),True
    else:
        return "",False





def ChangePassword(setup,screenInstance,screenName,handle,usersDetail,parentLoggedInUser_Name,button='Change'):
    if len(handle['allinputs']['password'])>0:

        logger.info("Going to Enter Current Password =%s",usersDetail['currentpassword'])
        currentpasswordfromUI = screenInstance.cm.sendkeys_input(usersDetail['currentpassword'], handle,0,child='password')
        checkEqualAssert(str(currentpasswordfromUI), str(usersDetail['currentpassword']),message="Verify Current Password")

        check_element_enabled(setup, element=handle['alllinks']['a'][1], attribute_to_find='class',expected_ele_state=Constants.DISABLED_STATUS, request="Current Password")


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


        check_element_enabled(setup, element=handle['alllinks']['a'][1], attribute_to_find='class',expected_ele_state=Constants.DISABLED_STATUS, request="New Password")


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
            return msg,False

        button_status = check_element_enabled(setup, element=handle['alllinks']['a'][1], attribute_to_find='class',expected_ele_state=Constants.ENABLED_STATUS, request="Confirm New Password")

        if button_status == Constants.ENABLED_STATUS and button == "Change":
            click_status = screenInstance.cm.clickButton(button, handle,parent='alllinks', child='a')
            checkEqualAssert(True, click_status,message="Verify whether " + button + " button clicked or not")
            isError(setup)
            errorMsg,erroFlag=errorMsgOnChangePasswordPopup(setup,screenName)
            if erroFlag:
                r = "issue_" + str(random.randint(0, 9999999)) + ".png"
                setup.d.save_screenshot(r)
                logger.info('Error Found on Change Password Popup :: Screenshot save with name =%s',str(errorMsg),r)
                resultlogger.info('Error Found on Change Password Popup :: Screenshot save with name =%s <br>',str(errorMsg),r)
                password_changed_status = False
                handle = getHandle(setup, UMConstants.UMPOPUP_ERROR, "allbuttons")
                screenInstance.hoverAndClickButton(setup, "Ok", handle)
                time.sleep(5)
            else:
                logger.info("Password Changed successfully")
                password_changed_status = True
                #### Code to be added once password change functionaly is working successfully, for the expected popup on password change

            checkEqualAssert(True, password_changed_status, message="Verify that user '" + str(parentLoggedInUser_Name) + "' can successfully update his own password ",testcase_id='Reflex-UM-242,Reflex-UM-243')
            return errorMsg, password_changed_status



        if button == "Cancel":
            screenInstance.cm.clickButton(button, handle, parent='alllinks', child='a')
            return "Cancel",True

        return '',True

    else:
        logger.error("Handle for input type Password not Found")
        resultlogger.error("Handle for input (type =Password) not Found <br>")
        return '',False





