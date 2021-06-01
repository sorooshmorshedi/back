import requests

from server import settings
from server.settings import APP_SHORT_LINK


class Sms:
    api_key = "6d848f715eb5887a757a8f71"
    secret_key = "#3Smj5rBnU8ckVN"

    @staticmethod
    def get_token():

        if settings.TESTING:
            return "It's OK"

        url = 'https://restfulsms.com/api/Token'
        data = {
            "UserApiKey": Sms.api_key,
            "SecretKey": Sms.secret_key
        }
        response = requests.post(
            url=url,
            data=data
        )
        return response.json()['TokenKey']

    @staticmethod
    def send(phone, message):

        body = {
            "Messages": [message],
            "MobileNumbers": [phone],
            "LineNumber": "3000255113",
            "SendDateTime": "",
            "CanContinueInCaseOfError": False,
        }

        token = Sms.get_token()
        url = 'https://RestfulSms.com/api/MessageSend'

        headers = {
            'Content-Type': 'application/json',
            'x-sms-ir-secure-token': token
        }

        if settings.TESTING:
            return "It's OK"

        response = requests.post(
            url=url,
            headers=headers,
            json=body,
        )

        return response.json()


if __name__ == '__main__':
    text = ""
    print(
        Sms.send('09307468674', text)
    )
