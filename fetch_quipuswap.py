from pytezos import pytezos

contract_address_list = [
    'KT1W3VGRUjvS869r4ror8kdaxqJAZUbPyjMT',
    'KT1K4EwTpbvYN9agJdjpyJm4ZZdhpUNKB3F6',
    'KT1BMEEPX7MWzwwadW3NCSZe9XGmFJ7rs7Dr',
    'KT1WBLrLE2vG8SedBqiSJFm4VVAZZBytJYHc',
    'KT1Evsp2yA19Whm24khvFPcwimK6UaAJu8Zo',
    'KT1WxgZ1ZSfMgmsSDDcUn8Xn577HwnQ7e1Lb',
    'KT1FG63hhFtMEEEtmBSX2vuFmP87t9E7Ab4t',
    'KT1T4pfr6NL8dUiz8ibesjEvH2Ne3k6AuXgn',
    'KT1UMAE2PBskeQayP5f2ZbGiVYF7h8bZ2gyp',
    'KT1DuYujxrmgepwSDHtADthhKBje9BosUs1w',
    'KT1PQ8TMzGMfViRq4tCMFKD2QF5zwJnY67Xn',
    'KT1Ti3nJT85vNn81Dy5VyNzgufkAorUoZ96q',
    'KT1U2hs5eNdeCpHouAvQXGMzGFGJowbhjqmo',
    'KT1DksKXvCBJN7Mw6frGj6y6F3CbABWZVpj1',
    'KT1Ca5FGSeFLH3ugstc5p56gJDMPeraBcDqE',
    'KT1RsfuBee5o7GtYrdB7bzQ1M6oVgyBnxY4S',
    'KT1Lpysr4nzcFegC9ci9kjoqVidwoanEmJWt',
    'KT1Lvtxpg4MiT2Bs38XGxwh3LGi5MkCENp4v',
    'KT1Lotcahh85kp878JCEc1TjetZ2EgqB24vA',
    'KT1MaefGJRtu57DiVhQNEjYgTYok3X71iEDj',
    'KT1DA8NH6UqCiSZhEg5KboxosMqLghwwvmTe',
    'KT1GSjkSg6MFmEMnTJSk6uyYpWXaEYFahrS4',
    'KT1NQyNPXmjYktNBDhYkBKyTGYcJSkNbYXuh',
    'KT1MpRQvn2VRR26VJFPYUGcB8qqxBbXgk5xe',
    'KT1AN7BBmeSUN5eDDQLEhWmXv1gn4exc5k8R',
    'KT1GsTjbWkTgtsWenM6oWuTuft3Qb46p2x4c',
    'KT1SzCtZYesqXt57qHymr3Hj37zPQT47JN6x',
    'KT1QxLqukyfohPV5kPkw97Rs6cw1DDDvYgbB',
    'KT1KFszq8UFCcWxnXuhZPUyHT9FK3gjmSKm6',
    'KT1X1LgNkQShpF9nRLYw3Dgdy4qp38MX617z',
    'KT1RRgK6eXvCWCiEGWhRZCSVGzhDzwXEEjS4']


def fetch():
    print("\nFetching Quipuswap data...", end="\r")
    tokens_info = {}
    for contract_address in contract_address_list:
        try:
            contract = pytezos.using('mainnet').contract(contract_address)
            storage = contract.storage()['storage']
            token_address = storage['token_address']
            token_amount = storage['token_pool']
            tez_amount = storage['tez_pool']
            tokens_info[str(token_address)] = {
                'token_amount': token_amount, 'tez_amount': tez_amount}
        except:
            print("Error while fetching data for contract", contract_address)
    return tokens_info
