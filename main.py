#!/usr/bin/python3
import json
from base64 import b64decode
from urllib.parse import urlparse, parse_qs

import requests
import rsa
from google.protobuf.json_format import MessageToJson

from QueryCurrRegionHttpRsp_pb2 import QueryCurrRegionHttpRsp

RSA_DISPATCH_KEYS = {
    '1': b"""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxAde3Gos++LVlw2vvW5OiziD97fVvA3Y6GLY0xMd4d7LpnHr
fwuO7+60IZA9zR6QOFkrMrxNMTf2UbEJsnfbnUyhsQJr8bHR6PfUj6d/YUceM8YW
cjpCyZGM2mKuVBXYqWO8gU81bwQOKgHSytvIrXtsk+3+g+pfkSKZOakiPzosSXCt
GSPrVRJlumCmiXjTiKiwKqR+BBk8tZSuINl+r/aTfgu5xkfcB6YOYIIsNfkhpyZT
cO0TNk7A3gRhikySyfxZX/T7lBDqUUKMMoCPy8MPGHvc66YyW1xsf02zdkAHXDzc
hj6TrzApvzrUzEcl9rwxzCEtGWh5wjIV1a/sJQIDAQABAoIBAQCzHTD2ISXdOdSD
4wOTCPlHiGo8rILlA5oQLFGF+8+wFIzsFudg/ESswuVgTZXKmISamA86mofF0yaE
WklMAuxt/Bk5zcan3xy3y8szP47KadsU34ie8tEXsKCM4uH6/sMrc3BIjwF54LC4
fVYH+W6R5Va+jBWkn0CXMo/i+cHLFlYV8YScblO+nmhjxI4O9sy8b6grQ1/EMHi8
ioOi+4w0VZLD52GVsQ56tAf75EOFAsZgzldMHTNCdvDAy1NeNXgniN6qFv7vrqCf
R1DWh4jLyzeLdk6c4zakozSiElnY+PORuzPWu+GABZ6qYMDpDlGAriRG1Y8lG0O4
nJK+T4J5AoGBAPx3A8d5MhxXArTl3n2xNdCKDcSZu4MG5BCxmc70yrC4+MUXhMos
81vyUtz9s4HRcJlqoI+2tr0JptVaEWjN++VFKYVW4i+nX+YTbqndQ1tgXqXXGuLT
g6ffemQtwmKoOmNfq5FXMuCzySG0+YMp+lRuhHaTCDT5mvhFngpkUjWfAoGBAMbG
DhT+KcbvJABn1P5/eS2cnDebbcBUEVE0UTF8jWsrGNQdPj6oV2XpjfjlPR5ybRJb
eJI8uDdPUUAeyr4TNOwnJvyM7T1sxkm8zmLIUo6vsNXQT/HYyaFFTKftYAA9V3AB
37etSALKH4g5UVG6lfZuJlp08wPlGq84zv3/i5+7AoGALFvQ+yxtRJN5M0WsWRNY
7EJFdwS38Ka2TcSWzMkwD+sAMskWGNvbCo3CR3gAIVAmY55bhcTJyN84RAZmRq7i
kn8bc4U3ir3y2J8Tc58f5Z9CIgtweuhFGqrme1Ga9PCwCaPWplvW4apVLan5qTUn
+cvNVHQzHfO5aeP5h8PmuesCgYAzcVR5qGGlg4R8umKMTu9Ml6hyV75qtRcaPgD5
XrO21ZuCYeMXEjg0PuKoVKOhuplx08x7hE1kuxlbD90Gni/nIibb25kWeY1DziJX
vGJpXRzV6SiXfbSJEUdKeouK5FU5vrJodecaGbdZaQQbs79V3KH+bR/rlSJ30Kr5
X2aCOwKBgQCB9Cjp8RPuLEez8ISbsqaar/s1l6XVbPAX77XeVukJjXKXf3SN4Rat
Bi/OALSkd9TxcIrqfQ8TJtDicz8CJC379/hhfx9nxN/ZSyAf60qZ4KRc7qEtTTIt
GxpdYCz7pAUXR74D5w1T6Ob5TYIyMi2WefdzDx+Io0yZqUjEbqudLw==
-----END RSA PRIVATE KEY-----""",
    '2': b"""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAz/fyfozlDIDWG9e3Lb29+7j3c66wvUJBaBWP10rB9HTE6prj
fcGMqC9imr6zAdD9q+Gr1j7egvqgi3Da+VBAMFH92/5wD5PsD7dX8Z2f4o65Vk2n
VOY8Dl75Z/uRhg0Euwnfrved69z9LG6utmlyv6YUPAflXh/JFw7Dq6c4EGeR+Kej
FTwmVhEdzPGHjXhFmsVt9HdXRYSf4NxHPzOwj8tiSaOQA0jC4E4mM7rvGSH5GX6h
ma+7pJnl/5+rEVM0mSQvm0m1XefmuFy040bEZ/6O7ZenOGBsvvwuG3TT4FNDNzW8
Dw9ExH1l6NoRGaVkDdtrl/nFu5+a09Pm/E0ElwIDAQABAoIBAQCtH17Cck+KJQYX
j29xqG4qykNUDawbILiKCMkBE7553Wq/UcjmuuR4bVnML8ucS3mgR/BgHV3l8vUK
nxvqRx/oGZkWNazbiuwL+ThAblLWqrEmYuZVCoQcAnvkT8tIqDWz7fhDEuZnnkMz
ZcATIZzgZUSa5IfP3u3rP+MrVbyaCdzJEeI0Yrv1XT+M5ddkKQrYgqC5kRiYi/Lj
NcLJhqSVt8p37CdJx1PGHFjKKb4MZpANlNRgeTtWpGVfS0PJLzaiI1NyPSJv7xWZ
gVhbK9+wQxqSG6KmZ4vpEvRI1zKiov5BsAFN+GfuD5mpn1Xo9CpzTfj/sO13VpHH
+Mt80+yBAoGBAPYXVEcXug5zqkqXup4dp1S05saz1zWPhUhQm+CrbhgeTqpjngJJ
EB79qMrGmyki0P/cGtbTcrHf8+i7gDlIGW0OMb4/jn4f5ACVD00iyvkHSGPn0Aim
MoNOMbkGot7SkSnncwxXdawwDyTu2dofXuBr72+GYqgRAG52IuA0C0pRAoGBANhX
p/UyW/htB27frKch/rTKQKm12kBV20AkkRUQUibiiQyWueWKs+5bVaW5R5oDIhWx
qftJtnEFWUvWaTHpHsB/bpjS3CJ6WknqNbpa3QIScpV1uw8V+Etz/K2/ftjyZzFo
nqc+Jud5364xFdIlOsRj9gZnK83Wcui6EFxAer5nAoGBAJzTzzSjLUHqejqhKR98
nFeCFZPJpjuO5AxqunvaJAYgwlcZtueT8j8dvgTDvrvfYTu85CnFhNFQfFrzqspW
ZUW3hwHL9R3xatboJ2Er7Bf5iSuJ3my0pXpCSbO1Q/QmUrZWtl3GGsqJsg0CXjkA
RvFUN7ll9ddPRmwewykIYa2RAoGAcmKuWFNfE1O6WWIELH4p6LcDR3fyRI/gk+KB
nyx48zxVkAVllrsmdYFvIGd9Ny4u6F9+a3HG960HULS1/ACxFMCL3lumrsgYUvp1
m+mM7xqH4QRVeh14oZRa5hbY36YS76nMMMsI0Ny8aqJjUjADCXF81FfabkPTj79J
BS3GeEMCgYAXmFIT079QokHjJrWz/UaoEUbrNkXB/8vKiA4ZGSzMtl3jUPQdXrVf
e0ofeKiqCQs4f4S0dYEjCv7/OIijV5L24mj/Z1Q4q++S5OksKLPPAd3gX4AYbRcg
PS4rUKl1oDk/eYN0CNYC/DYV9sAv65lX8b35HYhvXISVYtwwQu/+Yg==
-----END RSA PRIVATE KEY-----""",
    '3': b"""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA02M1I1V/YvxANOvLFX8R7D8At40IlT7HDWpAW3t+tAgQ7sqj
CeYOxiXqOaaw2kJhM3HT5nZll48UmykVq45Q05J57nhdSsGXLJshtLcTg9liMEoW
61BjVZi9EPPRSnE05tBJc57iqZw+aEcaSU0awfzBc8IkRd6+pJ5iIgEVfuTluani
zhHWvRli3EkAF4VNhaTfP3EkYfr4NE899aUeScbbdLFI6u1XQudlJCPTxaISx5Zc
wM+nP3v242ABcjgUcfCbz0AY547WazK4bWP3qicyxo4MoLOoe9WBq6EuG4CuZQrz
Knq8ltSxud/6chdg8Mqp/IasEQ2TpvY78tEXDQIDAQABAoIBAQC4uPsYk4AsSe75
0Au6Dz7kSfIgdDhJ44AisvTmfLauMFZLtfxfjBDhCwTxuD7XnCZAxHm97Ty+AqSp
Km/raQQsvtWalMhBqYanzjDYMRv2niJ1vGjm3WrQxBaEF+yOtvrZsK5fQTslqInI
qknIQH7fgjazJ7Z28D18sYNj37qfFWSSymgFo+SoS/BKEr200lpRA/oaGXiHcyIO
jJidP6b7UGes7uhMXUvLrfozmCsSqslxXO5Uk5XN/fWl4LxCGX7mpNfPZIT5YBSj
HliFkNlxIjyJg8ORLGi82M2cuyxp39r93F6uaCjLtb+rdwlGur7npgXUkKfWQJf9
WE7uar6BAoGBAPXIuIuYFFUhqNz5CKU014jZu6Ql0z5ZA08V84cTJcfLIK4e2rqC
8DFTldA0FtVfOGt0V08H/x2pRChGOvUwGG5nn9Dqqh6BjByUrW4z2hnXzT3ZuSDh
6eapiCB1jl9meJ0snhF2Ps/hqWGL2b3SkCCe90qVTzOVOeLO6YUCIOq9AoGBANws
fQkAq/0xw8neRGNTrnXimvbS+VXPIF38widljubNN7DY5cIFTQJrnTBWKbuz/t9a
J8QX6TFL0ci/9vhPJoThfL12vL2kWGYgWkWRPmqaBW3yz7Hs5rt+xuH3/7A5w5vm
kEg1NZJgnsJ0rMUTu1Q6PM5CBg6OpyHY4ThBb8qRAoGAML8ciuMgtTm1yg3CPzHZ
xZSZeJbf7K+uzlKmOBX+GkAZPS91ZiRuCvpu7hpGpQ77m6Q5ZL1LRdC6adpz+wkM
72ix87d3AhHjfg+mzgKOsS1x0WCLLRBhWZQqIXXvRNCH/3RH7WKsVoKFG4mnJ9TJ
LQ8aMLqoOKzSDD/JZM3lRWkCgYA8hn5Y2zZshCGufMuQApETFxhCgfzI+geLztAQ
xHpkOEX296kxjQN+htbPUuBmGTUXcVE9NtWEF7Oz3BGocRnFrbb83odEGsmySXKH
bUYbR/v2Ham638UOBevmcqZ3a2m6kcdYEkiH1MfP7QMRqjr1DI1qpfvERLLtOxGu
xU5WAQKBgQCaVavyY6Slj3ZRQ7iKk9fHkge/bFl+zhANxRfWVOYMC8mD2gHDsq9C
IdCp1Mg0tJpWLaGgyDM1kgChZYsff4jRxHC4czvAtoPSlxWXF2nL31qJ3vk2Zzzc
a4GSHAInodXBrKstav5SIKosWKT2YysxgHlA9Sm2f4n09GjFbslEHg==
-----END RSA PRIVATE KEY-----""",
    '4': b"""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAyaxqjPJP5+Innfv5IdfQqY/ftS++lnDRe3EczNkIjESWXhHS
OljEw9b9C+/BtF+fO9QZL7Z742y06eIdvsMPQKdGflB26+9OZ8AF4SpXDn3aVWGr
8+9qpB7BELRZI/Ph2FlFL4cobCzMHunncW8zTfMId48+fgHkAzCjRl5rC6XT0Yge
6+eKpXmF+hr0vGYWiTzqPzTABl44WZo3rw0yurZTzkrmRE4kR2VzkjY/rBnQAbFK
KFUKsUozjCXvSag4l461wDkhmmyivpNkK5cAxuDbsmC39iqagMt9438fajLVvYOv
pVs9ci5tiLcbBtfB4Rf/QVAkqtTm86Z0O3e7DwIDAQABAoIBAQCyma226vTW35LE
N5zXWuAg+hhcxk6bvofWMUMXKvGF/0vHPTMXlvuSkDeDNa4vBivneRthBNPMgb3q
DuTWxrogQMOOI8ZdhY3DFexfDvcQD2anDJuSqSmg9Nd36q+yxk3xIoXB5Ilo23dd
vTnJXHhsBNovv7zRLO134cAHFqDoKzt5EEHre0skUcn6HjHOek6c53jvpKr5LSrr
iwx5gMuY/7ZSIUDo9WGY70qbQFGY6bOlX9x8uNjcFF+7SztEVQ+vhJ/+7EvwqaJr
ysweo0l91TKM9WaMuwoucKeceVWuynEw6GGTw8UTLtltekLGe6bS8YxY8fVwnKkT
RwJYwAJRAoGBAP2rhcfOA+1Ja37hUHKebfp9rHsex4+pGyt3Kdu7WdqOn4sexmya
BuiHQcUchPDVla/ruQZ20+8LHgzBDo0m8sY7gpf715UV9NSVIRD0wu26SKRklOFz
J4HBOwU9hBGLSnRUJzyvVlt5O7E9hAv61SCrvWBEcow2YnKNQLwvjMVJAoGBAMuG
oSb3A/ulqtp2zpxVAclYe/bSItZZTOUWP6Vb4hOiHxIJ0n1H9ap6grOYkJ/Yn4gg
yYzKm/noF1wXP7Rj/xOahnvMkzhGdmOabvE9LH5HwQTWxBBWTkZzgBbYtbg+J5MT
cKqJaychSRjJj+xX+d90rtlSu/c27chlSRKAHXWXAoGAFTcIHDq9l1XBmL3tRXi8
h+uExlM/q2MgM5VmucrEbAPrke4D+Ec1drMBLCQDdkTWnPzg34qGlQJgA/8NYX61
ZSDK/j0AvaY1cKX8OvfNaaZftuf2j5ha4H4xmnGXnwQAORRkp62eUk4kUOFtLrdO
pcnXL7rpvZI6z4vCszpi0okCgYEAp3lZEl8g/+oK9UneKfYpSi1tlGTGFevVwozU
QpWhKta1CnraogycsnOtKWvZVi9C1xljwF7YioPY9QaMfTvroY3+K9DjM+OHd96U
fB4Chsc0pW60V10te/t+403f+oPqvLO6ehop+kEBjUwPCkQ6cQ3q8xmJYpvofoYZ
4wdZNnECgYBwG8Vrv7Z+kX9Zuh1FvcRoY57bYLU0cWW92SA3Nvi8pZOIEaLHrQyZ
pvvaLIicR1m9+KsOAmii7ru0zL7KsrGW+5migQsaDi4gzahKQpad/R7MLKi/L53r
Ymo0aZKARLHW82GbomQ0zxdRoo9vaqfGNpXkxyyt3k3GGDunmrskYw==
-----END RSA PRIVATE KEY-----""",
    '5': b"""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAsJbFp3WcsiojjdQtVnTuvtawL2m4XxK93F6lCnFwcZqUP39t
xFGGlrogHMqreyawIUN7E5shtwGzigzjW8Ly5CryBJpXP3ehNTqJS7emb+9LlC19
Oxa1eQuUQnatgcsd16DPH7kJ5JzN3vXnhvUyk4Qficdmm0uk7FRaNYFi7EJs4xyq
FTrp3rDZ0dzBHumlIeK1om7FNt6Nyivgp+UybO7kl0NLFEeSlV4S+7ofitWQsO5x
YqKAzSzz+KIRQcxJidGBlZ1JN/g5DPDpx/ztvOWYUlM7TYk6xN3focZpU0kBzAw/
rn94yW9z8jpXfzk+MvWzVL/HAcPy4ySwkay0NwIDAQABAoIBADzKWpawbVYEHaM4
lLb7oCjAPXzE9zx7djLDvisfLCdfoINPedkoe52ty1o+BtRpWB7LXTY9pFic1FLE
5wvyy6zyf8hH3ZsysqNhWFxhh4FnLmx/UGokAir+anaK5mYVJ1vQtxzjlV1HAbQs
kRyrklKoHDdRFqiFXOwiib97oDNWhD+RxfyGwwJnynZZSXdLbLSiz/QHQNr/+Ufk
KRBaxt0CfU7mOLZxoy6fNAxHdBcBJPHCyh+aDvEbix7nSncSU8Ju/48YJ8DrglbZ
sXCYoA5Uz8NMDuaEMgoNWCFQVoEcRkEUoaH7BlWd3UUFRPnDZ1B4BmkrVoRE8a58
3OqSwakCgYEA19wQUISXtpnmCrEZfbyZ6IwOy8ZCVaVUtbTjVa8UyfNglzzJG3yz
cXU3X35v5/HNCHaXbG2qcbQLThnHBA+obW3RDo+Q49V84Zh1fUNH0ONHHuC09kB/
/gHqzn/4nLf1aJ2O0NrMyrZNsZ0ZKUKQuVCqWjBOmTNUitcc8RpXZ8sCgYEA0W09
POM/It7RoVGI+cfbbgSRmzFo9kzSp5lP7iZ81bnvUMabu2nv3OeGc3Pmdh1ZJFRw
6iDM6VVbG0uz8g+f8+JT32XdqM7MJAmgfcYfTVBMiVnh330WNkeRrGWqQzB2f2Wr
+0vJjU8CAAcOWDh0oNguJ1l1TSyKxqdL8FsA38UCgYEAudt1AJ7psgOYmqQZ+rUl
H6FYLAQsoWmVIk75XpE9KRUwmYdw8QXRy2LNpp9K4z7C9wKFJorWMsh+42Q2gzyo
HHBtjEf4zPLIb8XBg3UmpKjMV73Kkiy/B4nHDr4I5YdO+iCPEy0RH4kQJFnLjEcQ
LT9TLgxh4G7d4B2PgdjYYTkCgYEArdgiV2LETCvulBzcuYufqOn9/He9i4cl7p4j
bathQQFBmSnkqGQ+Cn/eagQxsKaYEsJNoOxtbNu/7x6eVzeFLawYt38Vy0UuzFN5
eC54WXNotTN5fk2VnKU4VYVnGrMmCobZhpbYzoZhQKiazby/g60wUtW9u7xXzqOd
M/428YkCgYBwbEOx1RboH8H+fP1CAiF+cqtq4Jrz9IRWPOgcDpt2Usk1rDweWrZx
bTRlwIaVc5csIEE2X02fut/TTXr1MoXHa6s2cQrnZYq44488NsO4TAC26hqs/x/H
bVOcX13gT26SYngAHHeh7xjWJr/KgIIwvcvgvoVs6lu7a8aLUvrOag==
-----END RSA PRIVATE KEY-----"""
}


def chunked(size, source):
    for i in range(0, len(source), size):
        yield source[i:i + size]


def main(args):
    curr = QueryCurrRegionHttpRsp()

    response = requests.get(args)
    if response.status_code != 200 or response.content == b"500":
        print(
            f"[!] Failed to fetch response from dispatch server; {{status_code={response.status_code}, content={response.content}}}")
        return

    qs = parse_qs(urlparse(args).query)
    if qs.get("key_id"):
        try:
            key_pkcs1 = rsa.PrivateKey.load_pkcs1(RSA_DISPATCH_KEYS[qs.get("key_id")[0]])
        except KeyError:
            print(f"[!] Unknown decryption key_id={qs.get('key_id')}")
            return

        decrypted = b""
        message = json.loads(response.content)["content"]
        print(message)
        for chunk in chunked(256, b64decode(message)):
            decrypted += rsa.decrypt(chunk, key_pkcs1)
        curr.ParseFromString(decrypted)
    else:
        curr.ParseFromString(b64decode(response.content))

    print(MessageToJson(curr, preserving_proto_field_name=True))


#
if __name__ == '__main__':
   main("https://cngfdispatch.yuanshen.com/query_cur_region?version=CNRELAndroid4.6.0&lang=2&platform=2&binary=1&time=949&channel_id=1&sub_channel_id=2&account_type=1&dispatchSeed=2a0793d37497c803&key_id=4&aid=104378518")
