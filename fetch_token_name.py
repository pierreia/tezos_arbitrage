import requests


def get_token_name(address, token_id):
    payload = {'contract': address, 'tokenId': token_id}
    r = requests.get(
        'https://api.tzkt.io/v1/tokens/', params=payload)
    res = r.json()
    return (res[0]['metadata']['symbol'])
