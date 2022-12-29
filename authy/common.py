import os
from twilio.rest import Client




def send_otp(otp, mobile_number):
    account_sid = "AC0b4eb16bbc5f191168dd2b259126174c"
    auth_token = "46dd8bd32f6eca976934a792e6704637"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    body=f"Hello from Twilio {otp}",
    from_="+14258421994",
    to=f"+91{mobile_number}"
    )

    print(message.sid)