# Download the helper library from https://www.twilio.com/docs/python/install
#!/usr/bin/env python

import os, sys
from Webserver import Credentials as CRD
from twilio.rest import Client


client = Client(CRD.Config["TWILIO_ACCOUNT_SID"], CRD.Config["TWILIO_AUTH_TOKEN"])




call = client.calls.create(
                        url="https://9bae-2a02-a420-6b-a40e-95b8-d9e9-33cd-f4ee.ngrok.io/" ,
                        to=+31638475605,
                        from_=+13854816716
                    )

print(call.sid)




