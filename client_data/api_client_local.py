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
    host_IP = "127.0.0.1"
    API_port_number = 5000
    while True:
        request = requests.get("http://" + host_IP + ":" + str(API_port_number) + "/question")
        if request.status_code == 200:
            try:
                print_request_info_get_delete(request)
                answer = dat_prep.predict_probability(request.json())
                request = requests.post("http://" + host_IP + ":" + str(API_port_number) + "/answer",
                                        json=json.dumps({"question": request.json(), "answer": answer.tolist()}))
                print_request_info_post_put(request)
            except ValueError:
                request = requests.post("http://" + host_IP + ":" + str(API_port_number) + "/answer",
                                        json=json.dumps({"question": request.json(), "answer": "wrong_data"}))
        else:
            print("nothing")
        time.sleep(2)
