import requests


def get_token_name(address, id):
    r = requests.get(
        'https://api.better-call.dev/v1/contract/mainnet/{}/tokens'.format(address))
    res = r.json()
    return (res[int(id)]['symbol'])
