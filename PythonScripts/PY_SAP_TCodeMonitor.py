# Importing the Libraries
import win32com.client
import sys
import subprocess
import time


# This function will Login to SAP from the SAP Logon window

def saplogin(sysID, clNo, usrID, pwRd, tCode):
    try:

        path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe"
        subprocess.Popen(path)
        time.sleep(10)

        SapGuiAuto = win32com.client.GetObject('SAPGUI')
        if not type(SapGuiAuto) == win32com.client.CDispatch:
            return

        application = SapGuiAuto.GetScriptingEngine
        if not type(application) == win32com.client.CDispatch:
            SapGuiAuto = None
            return
        connection = application.OpenConnection(sysID, True)

        if not type(connection) == win32com.client.CDispatch:
            application = None
            SapGuiAuto = None
            return

        session = connection.Children(0)
        if not type(session) == win32com.client.CDispatch:
            connection = None
            application = None
            SapGuiAuto = None
            return

        session.findById("wnd[0]/usr/txtRSYST-MANDT").text = clNo
        session.findById("wnd[0]/usr/txtRSYST-BNAME").text = usrID
        session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = pwRd
        session.findById("wnd[0]").sendVKey(0)

        ################## Code For Multiple Login into SAP System ####################################
        if session.ActiveWindow.Name == "wnd[1]":
            if session.findById("wnd[1]").text == "License Information for Multiple Logons":
                session.findById("wnd[1]/usr/radMULTI_LOGON_OPT2").select()
                session.findById("wnd[1]/usr/radMULTI_LOGON_OPT2").setFocus()
                print("License Information for Multiple Logons error occurred and resolved")
                session.findById("wnd[1]/tbar[0]/btn[0]").press()

        ###################### Executing Tcode #########################
        session.findById("wnd[0]/tbar[0]/okcd").text = tCode
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/tbar[0]/btn[0]").press()
        session.findById("wnd[0]/tbar[0]/btn[15]").press()

    except:
        print(sys.exc_info()[0])

    finally:
        session = None
        connection.CloseSession("ses[0]")
        time.sleep(10)
        connection = None
        application = None
        SapGuiAuto = None


if __name__ == "__main__":
    sysID = str(sys.argv[1])
    clNo = str(sys.argv[2])
    usrID = str(sys.argv[3])
    pwRd = str(sys.argv[4])
    tCode = str(sys.argv[5])
    outputMsg = saplogin(sysID, clNo, usrID, pwRd, tCode)
    print(outputMsg)