import fetch_quipuswap
import fetch_plenty
import fetch_token_name
import fetch_vortex
import numpy as np

#from tezos_arbitrage import fetch_quipuswap, fetch_plenty, fetch_token_name, fetch_vortex

def price(x, y, a, fee):
    return ((1-fee)*y*a/(x+(1-fee)*a))


def analyse():
    quipuswap_data = fetch_quipuswap.fetch()
    plenty_data = fetch_plenty.fetch()
    print("\nData fetched ! \U0001F389\n")

    quipuswap_tokens = quipuswap_data.keys()
    plenty_tokens = plenty_data.keys()

    # intersection = list(set(quipuswap_tokens) & set(plenty_tokens))

    intersection = [x for x in quipuswap_tokens if x in plenty_tokens]

    max_amount_plenty = 0
    best_path = intersection[0]
    a = 10

    for (token_address, token_id) in intersection:
        amount_received = price(quipuswap_data[(token_address, token_id)]['token_amount'],
                                quipuswap_data[(token_address, token_id)]['xtz_amount'], a, 0.003) * a
        amount_plenty = price(
            plenty_data[(token_address, token_id)]['plenty_amount'],
            plenty_data[(token_address, token_id)]['token_amount'], amount_received, 0.0035) * amount_received
        max_amount_plenty = max(max_amount_plenty, amount_plenty)
        if amount_plenty == max_amount_plenty:
            best_path = (token_address, token_id)

    print("Max $PLENTY amount", max_amount_plenty/10000000000000)
    print(best_path[0],best_path[1])
    symbol_best_path = fetch_token_name.get_token_name(
        best_path[0], best_path[1])
    print('Path: XTZ ->', symbol_best_path, '-> PLENTY -> XTZ', '\n')


def fetch_tokens():
    print('Fetching Quipuswap...\n')
    quipuswap_data = fetch_quipuswap.fetch()
    print('Fetching Plenty...\n')
    plenty_data = fetch_plenty.fetch()
    print('Fetching Vortex...\n')
    vortex_data = fetch_vortex.fetch()
    print("\nData fetched ! \U0001F389\n")

    return quipuswap_data, plenty_data, vortex_data

quipuswap_data, plenty_data, vortex_data = fetch_tokens()

def analyse2(quipuswap_data,plenty_data,vortex_data):
    print("Starting arbitrage...")

    quipuswap_tokens = quipuswap_data.keys()
    plenty_tokens = plenty_data.keys()
    vortex_tokens = vortex_data.keys()

    exchanges = ['Quipu', 'Vortex']
    opportunities = []

    # intersection = list(set(quipuswap_tokens) & set(plenty_tokens))

    intersection = [x for x in quipuswap_tokens if (x in plenty_tokens and x in vortex_tokens)]

    print("Common pools: ", len(intersection))

    max_tez_amount = 0
    best_path = intersection[0]
    tez_amount = 0.5

    for (token_address, token_id) in intersection:
        print("Trying: ", (token_address, token_id))
        #SWAP 1
        amount_quipu = price(float(quipuswap_data[(token_address, token_id)]['xtz_amount']),
                                float(quipuswap_data[(token_address, token_id)]['token_amount']), tez_amount, 0.003)
        amount_vortex = price(float(vortex_data[(token_address, token_id)]['xtz_amount']),
                                float(vortex_data[(token_address, token_id)]['token_amount']), tez_amount, 0.0028)

        first_ex_id = np.argmax([amount_quipu, amount_vortex])
        first_ex = exchanges[first_ex_id]

        tokenA_amount = max(amount_quipu, amount_vortex)
        tokenA = token_address
        tokenAId = token_id

        #SWAP 2
        plenty_amount = price(
            plenty_data[(token_address, token_id)]['token_amount'],
            plenty_data[(token_address, token_id)]['plenty_amount'], tokenA_amount, 0.0035)

        #SWAP 3
        for (token_address2, token_id2) in intersection:
            tokenB_amount = price(
                plenty_data[(token_address2, token_id2)]['plenty_amount'],
                plenty_data[(token_address2, token_id2)]['token_amount'], plenty_amount, 0.0035)

            tokenB = token_address2
            tokenBId = token_id2
            final_amount_quipu = price(float(quipuswap_data[(token_address2, token_id2)]['token_amount']),
                                 float(quipuswap_data[(token_address2, token_id2)]['xtz_amount']), tez_amount, 0.003)
            final_amount_vortex = price(float(vortex_data[(token_address2, token_id2)]['token_amount']),
                                  float(vortex_data[(token_address2, token_id2)]['xtz_amount']), tez_amount, 0.0028)

            tokenA_name = fetch_token_name.get_token_name(tokenA, tokenAId)
            tokenB_name = fetch_token_name.get_token_name(tokenB, tokenBId)
            if max(final_amount_vortex, final_amount_quipu) > tez_amount:
                second_ex_id = np.argmax([final_amount_quipu, final_amount_vortex])
                second_ex = exchanges[second_ex_id]
                print('Opportunity found: XTZ -> {} on {}, {} -> PLENTY -> {} on PLENTY, {} -> XTZ on {}'.format(
                    tokenA_name, first_ex, tokenA_name, tokenB_name, tokenB_name, second_ex
                ))
                print('{} amount: {}'.format(tokenA_name, tokenA_amount))
                print('{} amount: {}'.format('PLENTY', plenty_amount))
                print('{} amount: {}'.format(tokenB_name, tokenB_amount))
                print('Final amount: {}'.format(max(final_amount_vortex, final_amount_quipu)))


analyse2(quipuswap_data,plenty_data,vortex_data)

if __name__ == "__main__":
    analyse()
