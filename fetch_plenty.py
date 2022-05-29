from pytezos import pytezos
import requests

"""
contract_address_list = [
    'KT1XXAavg3tTj12W1ADvd3EEnm1pu6XTmiEF', #PLENTY-wBUSD
    'KT1PuPNtDFLR6U7e7vDuxunDoKasVT6kMSkz',
    'KT19Dskaofi6ZTkrw3Tq4pK7fUqHqCz4pTZ3',
    'KT1VeNQa4mucRj36qAJ9rTzm4DTJKfemVaZT',
    'KT1XVrXmWY9AdVri6KpxKo4CWxizKajmgzMt',
    'KT1D36ZG99YuhoCRZXLL86tQYAbv36bCq9XM',
    'KT1XutoFJ9dXvWxT7ttG86N2tSTUEpatFVTm',
    'KT1AbuUaPQmYLsB8n8FdSzBrxvrsm8ctwW1V',
    'KT1HUnqM6xFJa51PM2xHfLs7s6ARvXungtyq',
    'KT1UNBvCJXiwJY6tmHM7CJUVwNPew53XkSfh',
    'KT1NtsnKQ1c3rYB12ZToP77XaJs8WDBvF221']
"""

def fetch():
    print("\nFetching Plenty data...", end="\r")
    print("\nFetching Pools ...", end="\r")
    payload = {'sender': 'tz1NbDzUQCcV2kp3wxdVHVSZEDeq2h97mweW', 'limit': 10000}
    r = requests.get(
        'https://api.tzkt.io/v1/operations/originations', params=payload)
    res = r.json()

    #swaps_addresses = []
    contract_addresses = []
    for contract_info in res:
        contract = contract_info['originatedContract']
        if 'alias' in contract:
            if 'Swap' in contract['alias']:
                contract_addresses.append(contract['address'])
    tokens_info = {}

    for contract_address in contract_addresses:
        try:
            contract = pytezos.using('mainnet').contract(contract_address)
            storage = contract.storage()
            if storage['token1Address'] != 'KT1GRSvLoikDsXujKgZPsGLX8k8VvR2Tq95b':
                continue
            token_address = storage['token2Address']
            print(token_address)
            token_id = storage['token2Id']
            token_amount = storage['token2_pool']
            plenty_amount = storage['token1_pool']
            tokens_info[(str(token_address), token_id)] = {
                'token_amount': token_amount, 'plenty_amount': plenty_amount}
        except:
            print("Error while fetching data for contract", contract_address)
    return tokens_info
