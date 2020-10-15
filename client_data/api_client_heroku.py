import requests
from client_data.data_loading import data_preparing
import time
import json


def print_request_info_post_put(info):
    print("---------------------------------------------------------------")
    print("request.url: ", info.url)
    print("request.status_code: ", info.status_code)
    print("request.headers: ", info.headers)
    print("request.text: ", info.text)
    print("request.request.body: ", info.request.body)
    print("request.request.headers: ", info.request.headers)
    print("---------------------------------------------------------------")


def print_request_info_get_delete(info):
    print("---------------------------------------------------------------")
    print("request.url: ", info.url)
    print("request.status_code: ", info.status_code)
    print("request.headers: ", info.headers)
    print("request.text: ", info.text)
    print("request.request.headers: ", info.request.headers)
    print("---------------------------------------------------------------")


if __name__ == "__main__":
    dat_prep = data_preparing()
    host_IP = "https://cov-test-app.herokuapp.com"
    while True:
        request = requests.get(host_IP + "/question")
        if request.status_code == 200:
            try:
                print_request_info_get_delete(request)
                answer = dat_prep.predict_probability(request.json())
                request = requests.post(host_IP + "/answer",
                                        json=json.dumps({"question": request.json(), "answer": answer.tolist()}))
                print_request_info_post_put(request)
            except ValueError:
                request = requests.post(host_IP + "/answer",
                                        json=json.dumps(answer.tolist()))
        else:
            print("nothing")
        time.sleep(2)
