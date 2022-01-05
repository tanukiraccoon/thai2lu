# def test1(list, number):
#     start = 0
#     stop = len(list)
#     pair = 0
#     for i in range(start, stop-1):
#         for j in range(start+1, stop):
#             if (list[i]*list[j] == number):
#                 pair += 1
#                 print(list[i], ' * ', list[j], ' = ', number)
#         start += 1
#     start += 1
#     print("Pair: ", pair)


# test1([1, 2, 3, 4, 5, 6], 12)
# test1([1, 3, 5, 7, 9], 15)
# test1([0, 9, 11, 100], 0)
# test1([10, 20, 30, 40], 99)

def test2(text):
    dict = {}
    for char in text:
        if char in dict:
            dict[char] += 1
        else:
            dict[char] = 1
    result = max(dict, keไy=dict.get)
    print(dict.get)
    print(result * dict[result])


test2('abbc')
test2('aaabcc')
test2('abcde')
test2('abbcccddddeeeee')
test2('aaabaa')
