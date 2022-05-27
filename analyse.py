import fetch_quipuswap
import fetch_plenty
import fetch_token_name


def price(x, y, a, fee):
    return ((x+(1-fee)*a)/((1-fee)*y))


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


if __name__ == "__main__":
    analyse()
