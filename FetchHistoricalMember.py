# Code obtained from 
# https://github.com/msitt/blpapi-python/tree/master/examples
# Revised by Liansai Dong
# Last Edit: 2018-03-26
# CPython version: 3.4.4

# RefDataTableOverrideExample.py
from __future__ import print_function
from __future__ import absolute_import

import blpapi
from optparse import OptionParser

import os
import re

dir = "FetchedHistoricalMember/"
if not os.path.exists(dir):
    os.makedirs(dir)

SECURITY_DATA = blpapi.Name("securityData")
SECURITY = blpapi.Name("security")
FIELD_DATA = blpapi.Name("fieldData")
FIELD_EXCEPTIONS = blpapi.Name("fieldExceptions")
FIELD_ID = blpapi.Name("fieldId")
ERROR_INFO = blpapi.Name("errorInfo")


def parseCmdLine():
    parser = OptionParser(description="Retrieve reference data.")
    parser.add_option("-a",
                      "--ip",
                      dest="host",
                      help="server name or IP (default: %default)",
                      metavar="ipAddress",
                      default="localhost")
    parser.add_option("-p",
                      dest="port",
                      type="int",
                      help="server port (default: %default)",
                      metavar="tcpPort",
                      default=8194)

    (options, args) = parser.parse_args()

    return options


def processMessage(tkList, date, msg):
    filename = dir + "MemberList" + date + ".txt"
    with open(filename, "w") as file: # change to 'a' for append

        securityDataArray = msg.getElement(SECURITY_DATA)
        for securityData in securityDataArray.values():
            print(securityData.getElementAsString(SECURITY))
            fieldData = securityData.getElement(FIELD_DATA)
            for field in fieldData.elements():
                if not field.isValid():
                    print(field.name(), "is NULL.")
                elif field.isArray():
                    # The following illustrates how to iterate over complex
                    # data returns.
                    for i, row in enumerate(field.values()):
                        # print("Row %d: %s" % (i, row))
                        file.write("Row" + str(i) + ": " + str(row))
                        # print(str(row))
                        m = re.search('Code = \"([\s\w/]+)\"', str(row))
                        if m:
                            ticker = m.group(1)
                        # print("parsed ticker is .. " + ticker)

                        if ticker not in tkList:
                            tkList.add(ticker)
                else:
                    pass # <- added due to the other statement is commented off
                    # print("%s = %s" % (field.name(), field.getValueAsString()))
                    # file.write(field.name() + " = " + field.getValueAsString())

            fieldExceptionArray = securityData.getElement(FIELD_EXCEPTIONS)
            for fieldException in fieldExceptionArray.values():
                errorInfo = fieldException.getElement(ERROR_INFO)
                print("%s: %s" % (errorInfo.getElementAsString("category"),
                                  fieldException.getElementAsString(FIELD_ID)))


def getMemberAtDate(tickerList, date):
    global options
    options = parseCmdLine()

    # Fill SessionOptions
    sessionOptions = blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print("Connecting to %s:%d" % (options.host, options.port))

    # Create a Session
    session = blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print("Failed to start session.")
        return

    if not session.openService("//blp/refdata"):
        print("Failed to open //blp/refdata")
        return

    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest("ReferenceDataRequest")

    # Add securities to request.
    request.append("securities", "SPX Index")
    # Add fields to request. Cash flow is a table (data set) field.
    request.append("fields", "INDX_MWEIGHT")

    # Add scalar overrides to request.
    overrides = request.getElement("overrides")
    override1 = overrides.appendElement()
    override1.setElement("fieldId", "END_DATE_OVERRIDE")
    override1.setElement("value", date)
    

    print("Sending Request:", request)
    cid = session.sendRequest(request)  

    try:
        # Process received events
        while(True):
            # We provide timeout to give the chance to Ctrl+C handling:
            ev = session.nextEvent(500)
            for msg in ev:
                if cid in msg.correlationIds():
                    # Process the response generically.
                    processMessage(tickerList, date, msg)
            # Response completly received, so we could exit
            if ev.eventType() == blpapi.Event.RESPONSE:
                break
    finally:
        # Stop the session
        session.stop()

if __name__ == "__main__":
    print("RefDataTableOverrideExample")
    tL = set([])
    try:
        getMemberAtDate(tL, "20101101")
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping...")

    with open("tikersList1.txt", "w") as f:
        f.write("\n".join(tL))




__copyright__ = """
Copyright 2012. Bloomberg Finance L.P.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  The above
copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""