import fetch_quipuswap
import fetch_plenty
import fetch_token_name
import fetch_vortex
import numpy as np

#from tezos_arbitrage import fetch_quipuswap, fetch_plenty, fetch_token_name, fetch_vortex
import numpy as np

def price(x, y, a, fee):
    return ((1-fee)*y*a/(x+(1-fee)*a))

MUTEZ = 10e6



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

def analyse2(quipuswap_data,plenty_data,vortex_data, tez_amount):
    print("Starting arbitrage...")

    quipuswap_tokens = quipuswap_data.keys()
    plenty_tokens = plenty_data.keys()
    vortex_tokens = vortex_data.keys()

    exchanges = ['Quipu', 'Vortex']
    opportunities = []

    # intersection = list(set(quipuswap_tokens) & set(plenty_tokens))

    intersection = [x for x in quipuswap_tokens if (x in plenty_tokens and x in vortex_tokens)]

    print("Common pools: ", len(intersection))

    print("Fetching decimals...")
    decimals = {}

    for token in intersection:
        decimals[token] = fetch_token_name.get_decimals(*token)
        print(token, decimals[token])
    print("Total decimals feetched: ", len(decimals))

    print("Decimals fetched")



    for (token_address, token_id) in intersection:
        token = (token_address, token_id)
        print("Trying: ", (token_address, token_id))
        #SWAP 1
        amount_quipu = price(quipuswap_data[(token_address, token_id)]['xtz_amount']/10e6,
                                quipuswap_data[(token_address, token_id)]['token_amount']/(10**(decimals[token]+1)), tez_amount, 0.003)
        amount_vortex = price(float(vortex_data[(token_address, token_id)]['xtz_amount']),
                                float(vortex_data[(token_address, token_id)]['token_amount'])/(10**(decimals[token])), tez_amount, 0.0028)

        first_ex_id = np.argmax([amount_quipu, amount_vortex])
        first_ex = exchanges[first_ex_id]

        tokenA_amount = max(amount_quipu, amount_vortex)
        tokenA = token_address
        tokenAId = token_id

        #SWAP 2
        plenty_amount = price(
            plenty_data[(token_address, token_id)]['token_amount']/(10**decimals[(tokenA, tokenAId)]),
            plenty_data[(token_address, token_id)]['plenty_amount']/10e18, tokenA_amount, 0.0035)

        #SWAP 3
        for (token_address2, token_id2) in intersection:
            token2 = (token_address2, token_id2)
            tokenB_amount = price(
                plenty_data[(token_address2, token_id2)]['plenty_amount']/10e18,
                plenty_data[(token_address2, token_id2)]['token_amount']/(10**(decimals[token2])), plenty_amount, 0.0035)

            tokenB = token_address2
            tokenBId = token_id2
            final_amount_quipu = price(quipuswap_data[(token_address2, token_id2)]['token_amount']/(10**(decimals[token2]+1)),
                                 quipuswap_data[(token_address2, token_id2)]['xtz_amount']/10e6, tokenB_amount, 0.003)
            final_amount_vortex = price(float(vortex_data[(token_address2, token_id2)]['token_amount'])/(10**(decimals[token2])),
                                  float(vortex_data[(token_address2, token_id2)]['xtz_amount']), tokenB_amount, 0.0028)

            tokenA_name = fetch_token_name.get_token_name(tokenA, tokenAId)
            tokenB_name = fetch_token_name.get_token_name(tokenB, tokenBId)

            final_tez_amount = (max(final_amount_vortex, final_amount_quipu))

            if final_tez_amount > tez_amount:
            #if True:
                second_ex_id = np.argmax([final_amount_quipu, final_amount_vortex])
                second_ex = exchanges[second_ex_id]
                print('Opportunity found: XTZ -> {} on {}, {} -> PLENTY -> {} on PLENTY, {} -> XTZ on {}'.format(
                    tokenA_name, first_ex, tokenA_name, tokenB_name, tokenB_name, second_ex
                ))
                print('{} amount: {}'.format(tokenA_name, tokenA_amount))
                print('{} amount: {}'.format('PLENTY', plenty_amount))
                print('{} amount: {}'.format(tokenB_name, tokenB_amount))
                print('Final amount: {}'.format(final_tez_amount))


#analyse2(quipuswap_data,plenty_data,vortex_data)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("tezos_amount", help="Initial Tezos Amount",
                        type=float)
    args = parser.parse_args()
    analyse2(quipuswap_data,plenty_data,vortex_data, args.tezos_amount)
