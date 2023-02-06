import Config.General.General_Config as Config

from twilio.rest import Client


client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)



call = client.calls.create(
                            record = True,
                            recording_status_callback  = Config.BASE_URL + "/" + Config.RECORDING_URL,
                            recording_status_callback_event="completed",
                            url= Config.BASE_URL+"/"+Config.STARTING_URL_VOICE_CALLBACK ,
                            to=Config.TO,
                            from_=Config.FROM
                        )
print(call.sid)