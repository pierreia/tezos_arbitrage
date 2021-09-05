from pytezos import pytezos

contract_address_list = [
    'KT1XXAavg3tTj12W1ADvd3EEnm1pu6XTmiEF',
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


def fetch():
    print("\nFetching Plenty data...", end="\r")
    tokens_info = {}
    for contract_address in contract_address_list:
        try:
            contract = pytezos.using('mainnet').contract(contract_address)
            storage = contract.storage()
            token_address = storage['token2Address']
            token_id = storage['token2Id']
            token_amount = storage['token2_pool']
            plenty_amount = storage['token1_pool']
            tokens_info[(str(token_address), token_id)] = {
                'token_amount': token_amount, 'plenty_amount': plenty_amount}
        except:
            print("Error while fetching data for contract", contract_address)
    return tokens_info
