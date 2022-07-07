import requests
import json
import os

path = os.path.dirname(os.path.abspath(__file__))


def get_token():
    try:
        secret_file = path + "\secrets.json"
        with open(secret_file) as f:
            secrets = json.loads(f.read())
        myToken = secrets["Token"]
        return myToken
    except:
        return False


# 채널명, 내용을 입력받고, 토큰을 파일로부터 획득하여 해당 채널에 내용을 post
def to_slack(text, channel="#일반"):
    myToken = get_token()
    if not myToken:
        return "No secret key! Message Failed."
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        data={"token": myToken, "channel": channel, "text": text},
    )
    if response.status_code == 200:
        return "Sucessfully Sent!"
    else:
        return "Message Failed while Posting.."


# 내 채널 목록을 "채널명": "채널id" 형태의 dictionary로 리턴
def get_channel_list(myToken):
    channel_list = requests.post(
        "https://slack.com/api/conversations.list", data={"token": myToken}
    ).json()
    if channel_list["ok"] == "false":
        return []
    channel_dict = {}
    for channel in channel_list["channels"]:
        if channel["is_member"] == "false":
            continue
        name = "#" + channel["name"]
        id = channel["id"]
        channel_dict[name] = id
    return channel_dict


# 채널id에 해당하는 채널의 대화 목록을 리스트로 리턴
def get_history_data(id, myToken, max_num):
    history_list = requests.post(
        "https://slack.com/api/conversations.history",
        data={"token": myToken, "channel": id, "limit": max_num},
    ).json()
    if history_list["ok"] == "false":
        print("Data Get Failed")
    result = []
    for message in history_list["messages"]:
        result.append([message["user"], message["text"]])
    return result


# 채널명에 해당하는 채널 내용을 리스트로 리턴
def get_channel_history(channel="#일반", max_num=10):
    myToken = get_token()
    if not myToken:
        print("No secret key!")
        return
    id_dict = get_channel_list(myToken)
    for key in id_dict.keys():
        if channel == key:
            result = get_history_data(id_dict[key], myToken, max_num)
    return result


def main():
    res = get_channel_history("#weather")
    for line in res:
        print(line)


if __name__ == "__main__":
    main()
