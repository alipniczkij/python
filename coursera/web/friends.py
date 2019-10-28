import requests
from datetime import datetime

ACCESS_TOKEN = ''
now = datetime.now()


class SplitError(Exception):
    pass


def calc_age(uid):
    info = {}
    ages = []
    r1 = requests.get('https://api.vk.com/method/users.get?v=5.71&access_token=' +
                      ACCESS_TOKEN + '&user_ids=' + uid).json()
    user_id = r1['response'][0]['id']
    r2 = requests.get('https://api.vk.com/method/friends.get?v=5.71'
                      '&access_token={}&user_id={}&fields=bdate'.format(ACCESS_TOKEN, user_id)).json()
    for i in range(r2['response']['count']):
        try:
            _, _, was_born = r2['response']['items'][i]['bdate'].split('.', 2)
            age = now.year - int(was_born)
            if age not in info:
                info[age] = 0
            info[age] += 1
        except (ValueError, KeyError):
            continue
    for key in info:
        ages.append((key, info[key]))
    return sorted(ages, key=lambda val: (-val[1], val[0]))


if __name__ == "__main__":
    res = calc_age('id')
    print(res)
