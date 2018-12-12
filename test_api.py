#! usr/bin/env/python3
# -*- coding : utf8 -*-


import requests


class Api_communicant(object):
    """ This object has the job of communicating with the DB
    """

    def __init__(self):
        """

        """
        self.response = requests.get('https://python.org/')

    def api_answer_checking(self):
        """

        """
        if self.response.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        for line in self.response.json():
            print(line)

if __name__ == '__main__':
    test = Api_communicant()
    test.api_answer_checking()
