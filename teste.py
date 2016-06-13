# from random import choice
# from string import ascii_letters
#
# print()
import json
#
# x = [[1, 'a'], [2, 'aadasd'], [3, 'sdasda']]
# # x = json.dumps((1, "http://www.epocacosmeticos.com.br/makeup-eraser-"
# #                     "original-toalha-removedora-de-maquiagem/p"),
# #                        (2, "http://www.epocacosmeticos.com.br/joop-homme-wild-"
# #                     "eau-de-toilette-joop-perfume-masculino/p"),
# #                        (3, "http://www.epocacosmeticos.com.br/animale-animale-for-"
# #                     "men-eau-de-toilette-animale-perfume-masculino/p")
# #             )

a = b'[[416, "http://www.epocacosmeticos.com.br/jimmy-choo-man-eau-de-toilette-jimmy-choo-perfume-masculino/p"], 'b'[417, "http://www.epocacosmeticos.com.br/primed-pink-e-plush-set-clinique-kit-de-maquiagem/p"]]'
# x = json.dumps()
y = json.loads(a.decode('utf-8'))
print(len(y))

# json.loads(body.decode('utf-8'))
# print(json.loads(x.encode('utf-8')))
# print(json.loads(x))