import json
from config import settings
from aes_sign import encrypt, decrypt, sign, sign_verify

query_dict = {
    'caseId': '3bf681e0b38c4d458742f35aff2907c3',
    'appKey': settings.appKey,
    'timestamp': '1605769182292',
    'transCode': 210,
    'clientName': '苏州农行',
    'clientId': 'USER0000',

    'bjbh': 'bjbh000',
    'zl': '相城区黄埭镇观湖湾家园4幢1410室',
    'bjqx': '320507',
    'ytmc': '普通住宅',
    'mj': 88.00,

    'bdcqzh': '',
    'qlrmc': '',
    'bdcdyh': '',
    'fwlxmc': '',
    'fwxzmc': '',
    'jgsj': '',
    'zcs': '',
    'szc': '',
    'tdmj': 0,
    'tdqlxzmc': '',
    'tdsyjssj': '',
    'tdytmc': '',
    'gyfsmc': '',
    'fj': '',
}

query_json = json.dumps(query_dict, ensure_ascii=False)
# print(query_json)

query_res_dict = {
    'caseId': '3bf681e0b38c4d458742f35aff2907c3',
    'transCode': 210,
    'code': 1,
    'message': '无数据',
    'companyName': '拓普森',

    'bjbh': 'bjbh000',
    'totalPrice': 1248700,
    'unitPrice': 12000,
}

query_res_json = json.dumps(query_res_dict, ensure_ascii=False)
# print(query_res_json)


confirm_dict = {
    'caseId': '3bf681e0b38c4d458742f35aff2907c3',
    'appKey': 'PfsNQBz6SDFSMGac',
    'timestamp': '1605769182292',
    'transCode': 211,
    'clientName': '苏州农行',
    'clientId': 'USER0000',

    'bjbh': 'bjbh000',
    'zl': '相城区黄埭镇方桥路8号观湖湾家园4幢1410室',
    'count': 1,

    'bdcqzh': '',
    'qlrmc': '',
    'bdcdyh': '',
    'ytmc': '',
    'mj': 0,
    'callbackUrl': 'callbackUrl',
    'telNo': '',
    'fwlxmc': '',
    'fwxzmc': '',
    'jgsj': '',
    'zcs': '',
    'szc': '',
    'tdmj': 0,
    'tdqlxzmc': '',
    'tdsyjssj': '',
    'tdytmc': '',
    'gyfsmc': '',
    'fj': '',
}

confirm_res_dict = {
    'caseId': '3bf681e0b38c4d458742f35aff2907c3',
    'transCode': 210,
    'code': 1,
    'message': '无数据',
    'companyName': '拓普森',

    'bjbh': 'bjbh000',
    'totalPrice': 1248700,
    'unitPrice': 12000,
    'delayTime': 10,
    'preEnquiryCaseId': '苏拓评(2022)第10023号'
}

x = {
    "data": "oqD1E0EefgFbgOfPkIBj8d0ACyM3f8AsB5M6p2Mf3YjCx4v6aKJJ3HzDUrK51oiRUgq4XPkfBYBdY07X1T120rVBE3QRZnQuxvRdhJutor7lY82R1Ek3Yi/5Fbh97qWSmXsftie6p2XCxaPDbI6ad/TyHF03LReoesT9e2BHovC5l4tnx0mnpNPeOnI05vVQlnRDaxUgJAnPYk79ZGERuqRjbBZoxVnd5e2eHqHJyP06EB6d0H6HXKcAWOCeZvr1Z1QYrkr4L/IBuLEJNdXJSoR/RA+pE8ONoXJwgItq1ZYSrPnvopDZbCLCUaRus98O/A38JHRuv2cnoNI6vzgWtPp1+YB/BOudk6Lkqxhva7NgPSDHE1lBXSnVrww/65nOfzJR79B2B5jWAuSXzFvjtSZL4PTU7//ZyCBt4dpyp63EEyt/nYWcI13aNtYQ/7kuvhLetEB6Dq5kGT5U1/Om1WwoSvKs3dsv7BBMEul/gE74glItjhQAF7hZZTnPa9o6AhHQlKP6j58x0sF2Gc2e7rr0fDIqo/ypCI0lJpL8RNAPFL1kuk0GrtgmIc8dACfGJZ2MsvDkMa85KPbEdYaAMDwAvLB5DOZy5Of5ANset5kR+eT9sCNsnx/Q3hoyNZn+e529Lih6fePQuS+wEQCfEw==",
    "sign": "QIvOMhhJRwH9j2r2wXPOotOw4Hbed/zqKLhJDyGLw2PCtuHybTD7MH+5dlo0NHdkgRpqhj5GNdLY9JRHSXaoVWmE6KcliG0qaR98vycqhoWK7+/jWGXkmAGlZ/BYs7iSFwKMTMA1NfuQssG3F2tkfu3wCGg8PT3+ubZB7rNqhNQo9mm1ExJeMbn8mONZ8ZmWX/pznJpRwpgRtbbb0TdaE24y+FG35PXs16M3Xx+KS3I7qZadzworpNzT/7kBf4KjumKsOwFKkNsMYgSNm8APULF4u7/Tx9R3hu2K0RyG8gcd9fTMLDagT7xAlH8Qo0C4Go1EA17dwVKtF94e29i7JA=="
}

# select c.id, c.estate_id, c.price_1, c.name,
#        d.id, d.category_id,
#        r.id, r.department_id
# from category c, department d, room r
# where r.zl = "苏州太湖国家旅游度假区香山街道伍相花园35幢904室" and
#       c.id = d.category_id and
#       d.id = r.department_id;


# 5.6.1
dict_56 = {
    'caseId': '3bf681e0b38c4d458742f35aff2907c3',
    'appKey': 'PfsNQBz6SDFSMGac',
    'timestamp': '1605769182292',
    'transCode': 215,
    'clientName': '苏州农行',
    'clientId': 'USER0000',

    'bjbh': 'bjbh',
    'callbackUrl': 'callbackUrl'
}

dict_56_payload = {
    'data': encrypt(json.dumps(dict_56, ensure_ascii=False)),
    'sign': sign(encrypt(json.dumps(dict_56, ensure_ascii=False)))
}

res_56 = {
    'caseId': '3bf681e0b38c4d458742f35aff2907c3',
    'transCode': 215,
    'code': 1,
    'message': '人工处理中',
    'companyName': '拓普森',

    'bjbh': 'bjbh',
    'verifyCode': ''  # how do you transfer sms message into a python program
}

# 5.6.2
# 如果选择接单, 需要填写验证码 向对方callbackUrl 发送
# 管理页面 填写验证码 点击确认接单
dict_562 = {
    'caseId': '3bf681e0b38c4d458742f35aff2907c3',
    'transCode': 215,
    'code': 1,
    'message': '人工处理中',
    'companyName': '拓普森',

    'bjbh': 'bjbh',
    'verifyCode': '5232'
}

# 5.2 复评
dict_52 = {
    'caseId': '3bf681e0b38c4d458742f35aff2907c3',
    'appKey': 'PfsNQBz6SDFSMGac',
    'timestamp': '1605769182292',
    'transCode': 211,
    'clientName': '苏州农行',
    'clientId': 'USER0000',

    'bjbh': 'bjbh000',
    'zl': '相城区黄埭镇方桥路8号观湖湾家园4幢1410室',
    'count': 1,

    'bdcqzh': '',
    'qlrmc': '',
    'bdcdyh': '',
    'ytmc': '',
    'mj': 0,
    'callbackUrl': 'callbackUrl',
    'telNo': '',
    'fwlxmc': '',
    'fwxzmc': '',
    'jgsj': '',
    'zcs': '',
    'szc': '',
    'tdmj': 0,
    'tdqlxzmc': '',
    'tdsyjssj': '',
    'tdytmc': '',
    'gyfsmc': '',
    'fj': '',
}

res_52 = {
    'bjbh': 'bjbh',
    'totalPrice': 3285400,
    'unitPrice': 25000,
    'delayTime': 10,
    'preEnquiryCaseId': 'bjbh'
}

# 5.3 获取与评估报告
dict_53 = {
    'transCode': 212,
    'bjbh': 'bjbh',
    'preEnquiryCaseId': 'bjbh',
    'exprice': 300.21
}
res_53 = {
    'bjbh': 'bjbh',
    'fileContent': 'whateverbase64',
    'delayTime': 0
}


