def send_sms(account_sid, auth_token,body,from_,to_):
    from twilio.rest import Client
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=body,
                        from_=from_,
                        to=to_
                    )

def sms_sender(number,message):
        
    import  requests
    url = "https://http-api.d7networks.com/send"
    querystring = {
    "username":"lvqd5462",
    "password":"1jwUcuxe",
    "from":"Test%20SMS",
    "content":f"{message}",
    "dlr-method":"POST",
    "dlr-url":"https://4ba60af1.ngrok.io/receive",
    "dlr":"yes",
    "dlr-level":"3",
    "to":f"{number}"
    }
    headers = {
    'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)




def gen_otp():
    import math ,random
    digits = "0123456789"
    otp  = ''
    for i in range(6):
        otp += digits[math.floor(random.random()*10)]

    return otp



