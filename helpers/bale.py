import requests


class Bale:

    @staticmethod
    def to_me(*args):
        url = "https://tapi.bale.ai/bot6585755eb40e4ab91d3545b2e05dd742a197d34f/sendMessage"

        message = ""
        for arg in args:
            message = "{}\n{}".format(message, str(arg))

        body = {
            'chat_id': '1213037233',
            'text': message,
        }

        response = requests.post(url, body)
        return response


if __name__ == '__main__':
    Bale().to_me('Hi again')
