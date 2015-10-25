# coding=utf-8
import re


def get_price_list(price_list_string):
    out = []
    for l in price_list_string.strip().splitlines():
        count, price = l.split("|")
        count_min, count_max = count.split('-')

        child_price = 0
        adult_price = 0
        add_price = 0

        if u"всех" in price:
            temp = re.sub(r"\D", "", price)
            if temp:
                add_price = int(temp)
        else:
            price = price.split("/")
            if len(price) == 2:
                temp = re.sub(r"\D", "", price[0])
                if temp:
                    child_price = int(temp)
                temp = re.sub(r"\D", "", price[1])
                if temp:
                    adult_price = int(temp)
            elif len(price) == 1:
                temp = int(re.sub(r"\D", "", price[0]))
                if temp:
                    adult_price = child_price = temp
            else:
                continue

        count_min = int(count_min)
        count_max = int(count_max)
        out.append((count_min, count_max, child_price, adult_price, add_price))
    return out