import argparse
import os
import tempfile
import json

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')


def get_data():
    if os.path.exists(storage_path):
        with open(storage_path, 'r') as f:
            in_data = f.read()
            if in_data:
                return json.loads(in_data)
    else:
        return {}


def find(key):
    data_find = get_data()
    return data_find.get(key)


def add(key, value):
    data_add = get_data()
    if key in data_add:
        data_add[key] = [value]
    else:
        data_add.append({key: value})
    with open(storage_path, 'w') as f:
        f.write(json.dumps(data_add))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--key")
    parser.add_argument("--val")
    args = parser.parse_args()

    if args.key and args.val:
        add(args.key, args.val)
        print("add to storage {} with key {}".format(args.val, args.key))
    elif args.key:
        print(find(args.key))
        print("find in storage with key {}".format(args.key))
    else:
        print('Wrong command')