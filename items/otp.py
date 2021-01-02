def send_sms(account_sid, auth_token,body,from_,to_):
    from twilio.rest import Client
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_=from_,
                        to=to_
                    )


def gen_otp():
    import math ,random
    digits = "0123456789"
    otp  = ''
    for i in range(6):
        otp += digits[math.floor(random.random()*10)]

    return otp



