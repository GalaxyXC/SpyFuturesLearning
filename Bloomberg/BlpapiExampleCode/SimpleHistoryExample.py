# Code obtained from 
# https://github.com/msitt/blpapi-python/tree/master/examples
# Revised by Liansai Dong
# Last Edit: 2018-01-25
# CPython version: 3.4.4

# Environment installed with Bloomberg Python API 3.9.0, available at
# https://www.bloomberg.com/professional/support/api-library/



from __future__ import print_function
from __future__ import absolute_import

import blpapi
from optparse import OptionParser


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


def main():
    options = parseCmdLine()
    security = "SPY US Equity"          # <<<<<<<<<<<<<<<<<<<<<<< EQUITY NAMES HERE
    # Fill SessionOptions
    sessionOptions = blpapi.SessionOptions()
    sessionOptions.setServerHost(options.host)
    sessionOptions.setServerPort(options.port)

    print("Connecting to %s:%s" % (options.host, options.port))
    # Create a Session
    session = blpapi.Session(sessionOptions)

    # Start a Session
    if not session.start():
        print("Failed to start session.")
        return

    try:
        # Open service to get historical data from
        if not session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata")
            return

        # Obtain previously opened service
        refDataService = session.getService("//blp/refdata")

        # Create and fill the request for the historical data
        request = refDataService.createRequest("HistoricalDataRequest")
        request.getElement("securities").appendValue(security)
        request.getElement("fields").appendValue("OPEN")
        request.getElement("fields").appendValue("PX_LAST")
        # request.getElement("fields").appendValue("CLOSE")
        request.getElement("fields").appendValue("HIGH")
        request.getElement("fields").appendValue("LOW")
        request.getElement("fields").appendValue("VOLUME")

        #request.getElement("fields").appendValue("INDX_MEMBERS")
        

        request.set("periodicityAdjustment", "ACTUAL")
        request.set("periodicitySelection", "DAILY")
        request.set("startDate", "20060101")
        request.set("endDate", "20171231")
        request.set("maxDataPoints", 5000)

        print("Sending Request:", request)
        # Send the request
        session.sendRequest(request)


        # Process received events
        filename = security + "_2006_2017.txt"
        file = open(filename, "w") # change to 'a' for append
        while(True):
            # We provide timeout to give the chance for Ctrl+C handling:
            ev = session.nextEvent(500)
            for msg in ev:
                file.write(str(msg))
                # print(msg)

            if ev.eventType() == blpapi.Event.RESPONSE:
                file.close()
                # Response completly received, so we could exit
                break
    finally:
        # Stop the session
        session.stop()

if __name__ == "__main__":
    print("SimpleHistoryExample")
    try:
        main()
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping...")