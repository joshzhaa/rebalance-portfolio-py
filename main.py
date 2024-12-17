#!/usr/bin/env python3
'''Calculates the transactions needed to rebalance a portfolio.

The asset allocation and the tickers that belong to each asset class are defined
in allocation.json. Current prices are in price.json, and current share counts are
in quantity.json. The script takes no arguments and expects these files to be in
the current directory.
'''

from typing import Any
import json


def read_inputs() -> tuple[Any, Any, Any]:
    '''Read json inputs from expected locations'''

    with open('allocation.json', 'r', encoding='utf-8') as file:
        allocation = json.load(file)

    with open('price.json', 'r', encoding='utf-8') as file:
        price = json.load(file)

    with open('quantity.json', 'r', encoding='utf-8') as file:
        quantity = json.load(file)

    if list(price.keys()) != list(quantity.keys()):
        raise ValueError('expected price.json and quantity.json to have same keys')

    return allocation, price, quantity


def main() -> None:
    '''main program logic

    Determines the difference in total dollars in each asset class, then calculates
    the number of (fractional) shares would be needed to resolve the difference.
    '''
    allocation, price, quantity = read_inputs()

    values = {fund: quantity[fund] * price[fund] for fund in price.keys()}
    total_value = sum(values.values())
    total_value += float(input('extra contribution ($): '))

    for asset_class, allocation in allocation.items():
        target_value = allocation['proportion'] * total_value
        current_value = sum(values[fund] for fund in allocation['funds'])
        dollars_delta = target_value - current_value
        print(asset_class)
        print(f'dollars delta: {dollars_delta}')

        for fund in allocation['funds']:
            shares_to_buy = dollars_delta / price[fund]
            print(f'shares to buy: {shares_to_buy} of {fund}')


if __name__ == '__main__':
    main()
