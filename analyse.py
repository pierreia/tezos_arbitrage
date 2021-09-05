import fetch_quipuswap
import fetch_plenty


def price(x, y, a):
    return ((x+0.997*a)/(0.997*y))


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
                                quipuswap_data[(token_address, token_id)]['tez_amount'], a) * a
        amount_plenty = price(
            plenty_data[(token_address, token_id)]['plenty_amount'],
            plenty_data[(token_address, token_id)]['token_amount'], amount_received) * amount_received
        max_amount_plenty = max(max_amount_plenty, amount_plenty)
        if amount_plenty == max_amount_plenty:
            best_path = (token_address, token_id)

    print("Max $PLENTY amount", max_amount_plenty/10000000000000)

    # print(
    #     'XTZ at the end:',
    #      (max_amount_plenty *
    #       quipuswap_data['KT1GRSvLoikDsXujKgZPsGLX8k8VvR2Tq95b']['tez_amount'])
    #     / (quipuswap_data['KT1GRSvLoikDsXujKgZPsGLX8k8VvR2Tq95b']['token_amount']+max_amount_plenty))
    print('Path: XTZ ->', best_path, ' -> PLENTY -> XTZ', '\n')


if __name__ == "__main__":
    analyse()
