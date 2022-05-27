from pytezos import pytezos
import requests

contract_address_list = [
    'KT1NoozaPXHKZHobxcheTWa1XLSTChUTgBg1', #DOGA-XTZ
    'KT1Wjadao8AXkwNQmjstbPGtLd1ZrUyQEDX7', #kUSD-XTZ
    'KT1VFUkjYDh6QG8iLx5uKHPU3BWFMeYoVPTL', #ANTI-XTZ
    'KT1ND1bkLahTzVUt93zbDtGugpWcL23gyqgQ', #uUSD-XTZ
    'KT1VSjJxNq98AkPfVktpCv82hacrvgkb6hEu', #PLENTY-XTZ
    'KT19GHKwP5EMUj2LNV23i9JjAAjS74sF9pcZ', #wLINK-XTZ
    'KT1MRMsyWYCwf2ex2wN4yuihJbNykCDHdRTT', #CTez-XTZ
    'KT1QqNYN9SLz8wNn1G4McVomcCKJzdRZcsbW', #YOU-XTZ
    'KT19HdcBJw8XJkDYKLr6ez9KkhhuS8MYUdcs', #USDTz-XTZ
    'KT1LzyPS8rN375tC31WPAVHaQ4HyBvTSLwBu', #SMAK-XTZ
    'KT1VsejAEdNgz1s98MjyuLC3mcnbjUZAaNu9', #wBUSD-XTZ
    'KT1DDWpBTgqMtkdnB5W17n47MDGrKyWBbQEB', #BTCtz-XTZ
]


vortex_factory_fa12 = 'KT1UnRsTyHVGADQWDgvENL3e9i6RMnTVfmia'
vortex_factory_fa2 = 'KT1JW8AeCbvshGkyrsyu1cWa5Vt7GSpNKrUz'
vortex_manager_1 = 'KT1PwnTa2f1Uac958RFTk6i6EecPNgJrtHKv'

vortex_factories = [vortex_factory_fa12, vortex_factory_fa2, vortex_manager_1]


def fetch():
    print("\nFetching Vortex data...", end="\r")
    contract_addresses = []
    for factory in vortex_factories:
        payload = {'sender': factory, 'limit': 10000}
        r = requests.get(
            'https://api.tzkt.io/v1/operations/originations', params=payload)
        res = r.json()

        #swaps_addresses = []

        for contract_info in res:
            contract = contract_info['originatedContract']
            if 'alias' in contract:
                if 'DEX' in contract['alias']:
                    contract_addresses.append(contract['address'])
    tokens_info = {}
    for contract_address in contract_addresses:
        try:
            contract = pytezos.using('mainnet').contract(contract_address)
            storage = contract.storage()
            token_address = storage['tokenAddress']
            print(token_address)
            if 'tokenId' in storage:
                token_id = storage['tokenId']
            else:
                token_id = 0
            token_amount = storage['tokenPool']
            xtz_amount = storage['xtzPool']
            tokens_info[(str(token_address), token_id)] = {
                'token_amount': token_amount, 'xtz_amount': xtz_amount}
        except:
            print("Error while fetching data for contract", contract_address)
    return tokens_info
