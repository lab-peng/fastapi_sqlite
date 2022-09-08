import json
import math
import re
from typing import List
import requests
import fastapi
import sqlalchemy.orm as orm
import uvicorn

import schemas
import services
from database import DB
from aes_sign import encrypt, decrypt, sign, sign_verify

app = fastapi.FastAPI()


# services.create_db()


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: orm.Session = fastapi.Depends(services.get_db)):
    db_user = services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail='“A user with that email already exists.')
    return services.create_user(db=db, user=user)


@app.get('/users/', response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: orm.Session = fastapi.Depends(services.get_db)):
    users = services.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get('/user/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    user = services.get_user(db=db, user_id=user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail='not found')
    return user


@app.post('/user/{user_id}/posts/', response_model=schemas.Post)
def create_post(user_id: int, post: schemas.PostCreate, db: orm.Session = fastapi.Depends(services.get_db)):
    user = services.get_user(db=db, user_id=user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail='The user with this id does not exist.')
    return services.create_post(user_id=user_id, post=post, db=db)


@app.get('/posts/', response_model=List[schemas.Post])
def get_posts(skip: int = 0, limit: int = 10, db: orm.Session = fastapi.Depends(services.get_db)):
    posts = services.get_posts(db=db, skip=skip, limit=limit)
    return posts


@app.get('/post/{post_id}', response_model=schemas.Post)
def get_post(post_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    post = services.get_post(db=db, post_id=post_id)
    if not post:
        raise fastapi.HTTPException(status_code=404, detail='not found')
    return post


@app.put('/post/{post_id}/', response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: orm.Session = fastapi.Depends(services.get_db)):
    services.update_post(post_id=post_id, post=post, db=db)
    return services.update_post(post_id=post_id, post=post, db=db)


@app.delete('/post/{post_id}')
def delete_post(post_id: int, db: orm.Session = fastapi.Depends(services.get_db)):
    services.delete_post(post_id=post_id, db=db)
    return {'message': f'You have deleted the post with id {post_id} successfully.'}


district_dict = {
    '320505': '虎丘区',
    '320506': '吴中区',
    '320507': '相城区',
    '320508': '姑苏区',
    '320509': '吴江区',
    '320513': '工业园区',
    '320581': '常熟市',
    '320582': '张家港市',
    '320583': '昆山市',
    '320585': '太仓市'
}

industry_land_dict = {
    # 建筑面积	土地面积
    '姑苏区': (1500, 940),
    '工业园区': (1500, 550),
    '虎丘区': (1500, 550),
    '吴中区': (1500, 400),
    '相城区': (1500, 400),
    '吴江区': (1500, 550),
    '常熟市': (1500, 500),
    '张家港市': (1500, 500),
    '昆山市': (1500, 400),
    '太仓市': (1500, 400)
}


def get_department_room(address):
    department = ''
    room = ''
    if '幢' in address:
        department_room_list = address.split('幢')
        department = re.findall('[a-zA-Z0-9-]*$', department_room_list[0])[0]
        if department_room_list[1]:
            room = re.findall('[a-zA-Z0-9-]*', department_room_list[1])[0]
    else:
        if '室' in address and '号' in address:
            room = address[address.index('号') + 1: address.index('室')]
    return department, room


@app.post('/')
async def raw_query(q: schemas.Query):
    bjbh = q.dict()['bjbh']
    zl = q.dict()['zl']
    bjqx = district_dict[q.dict()['bjqx']]
    department, room = get_department_room(zl)[0], get_department_room(zl)[1]
    print(department, room)
    # print(type(department), type(room))
    ytmc = q.dict()['ytmc']
    mj = q.dict()['mj']
    tdmj = q.dict()['tdmj']

    res = {
        'bjbh': bjbh,
        'unitPrice': 0,
        'totalPrice': 0
    }

    if ytmc in ['普通住宅', '别墅', '工业用房']:
        if ytmc == '工业用房':
            print('工业用房')
            totalPrice = round((industry_land_dict[bjqx][0] * mj + industry_land_dict[bjqx][1] * tdmj) / 100) * 100
            res = {
                'bjbh': bjbh,
                'unitPrice': 0,
                'totalPrice': totalPrice
            }
        else:
            # 如果可以精确搜索到产证地址
            query_a = f'''
                select c.price_1, r.floor_adjust, r.area_adjust, r.depreciation, r.location, r.side_adjust
                from category c, department d, room r
                where c.id = d.category_id and
                r.zl = "{zl}" and
                d.id = r.department_id;
            '''
            rows = await DB.fetch_all(query_a)
            if rows:
                print('精确查找成功')
                res['unitPrice'] = round(math.prod(rows[0]))
                res['totalPrice'] = round(res['unitPrice'] * mj / 100) * 100
            else:
                # 如果可以模糊反搜到小区名, 然后通过精确搜素到department幢号, room房号
                query_b = f'''
                    select distinct c.price_1, r.floor_adjust, r.area_adjust, r.depreciation, r.location, r.side_adjust
                    from estate e, category c, department d, room r
                    where instr("{zl}", e.name) and
                        d.code = '{department}' and r.code = '{room}' and
                        e.id = c.estate_id and
                        c.id = d.category_id and
                        d.id = r.department_id;
                '''
                rows = await DB.fetch_all(query_b)
                if rows:
                    print('模糊反搜到小区名, 然后通过精确搜素到department幢号, room房号成功')
                    res['unitPrice'] = round(math.prod(rows[0]))
                    res['totalPrice'] = round(res['unitPrice'] * mj / 100) * 100
                else:
                    # 如果可以模糊反搜到小区名, 然后通过精确搜素到department幢号
                    query_c = f'''
                        select distinct c.price_1, d.floor_adjust, d.area_adjust, d.depreciation, d.location, d.side_adjust
                        from estate e, category c, department d
                        where instr("{zl}", e.name) and
                            d.code = '{department}' and
                            e.id = c.estate_id and
                            c.id = d.category_id;
                    '''
                    rows = await DB.fetch_all(query_c)
                    if rows:
                        print('模糊反搜到小区名, 然后通过精确搜素到department幢号成功')
                        res['unitPrice'] = round(math.prod(rows[0]))
                        res['totalPrice'] = round(res['unitPrice'] * mj / 100) * 100
                    # 如果只能模糊反搜到小区名
                    query_d = f'''
                        select distinct e.price_1, d.floor_adjust, d.area_adjust, d.depreciation, d.location, d.side_adjust
                        from estate e, category c, department d
                        where instr("{zl}", e.name) and
                            e.id = c.estate_id and
                            c.id = d.category_id;
                    '''
                    rows = await DB.fetch_all(query_d)
                    if rows:
                        print('模糊反搜到小区名成功')
                        res['unitPrice'] = round(rows[0][0])
                        res['totalPrice'] = round(res['unitPrice'] * mj / 100) * 100
                    else:
                        # 如果连小区名到搜不到, 坐标寻找最近小区均价
                        print(zl)
                        print(zl, '| 模糊反搜小区不成功')
                        result_1 = requests.get(
                            f'https://api.map.baidu.com/geocoding/v3/?address={zl}&city=苏州市&output=json&ak=e2yoTRwCPRwuaRXDmNfVN9LyCBbcAHAF&callback=showLocation')
                        location = json.loads(result_1.text[27:-1])['result']['location']
                        x = location['lng']
                        y = location['lat']
                        print(x, y)

                        query_e = '''
                            select price_1, x, y, name from estate where x not null and y not null;
                        '''
                        rows = await DB.fetch_all(query_e)
                        min_dis = rows[0]
                        for r in rows:
                            if (r[1] - x) ** 2 + (r[2] - y) ** 2 < (min_dis[1] - x) ** 2 + (min_dis[2] - y) ** 2:
                                min_dis = r
                        print(min_dis)
                        res['unitPrice'] = round(min_dis[0])
                        res['totalPrice'] = round(res['unitPrice'] * mj / 100) * 100

    print(res)
    return res


# 询价
@app.post('/query/')
async def query(payload: schemas.Data):
    raw_data = payload.dict().get('data')
    signature = payload.dict().get('sign')
    params = json.loads(decrypt(raw_data))
    caseId = params['caseId']
    transCode = params['transCode']

    bjbh = params['bjbh']
    zl = params['zl']
    department, room = get_department_room(zl)[0], get_department_room(zl)[1]
    bjqx = params['bjqx']
    ytmc = params['ytmc']
    mj = params['mj']

    response = {
        'caseId': caseId,
        'transCode': transCode,
        'code': 1,
        'message': '',
        'companyName': '拓普森',

        'bjbh': bjbh,
        'totalPrice': 0,
        'unitPrice': 0
    }
    if not sign_verify(signature, raw_data):
        response['code'] = 0
        response['message'] = '签名错误'
    else:
        # 如果可以精确搜索到产证地址
        query_a = f'''
            select c.price_1, r.floor_adjust, r.area_adjust, r.depreciation, r.location, r.side_adjust
            from category c, department d, room r
            where c.id = d.category_id and
            r.zl = "{zl}" and
            d.id = r.department_id;
        '''
        rows = await DB.fetch_all(query_a)
        if rows:
            response['message'] = '成功'
            response['unitPrice'] = round(math.prod(rows[0]))
            response['totalPrice'] = round(response['unitPrice'] * mj / 100) * 100
        else:
            # 如果可以模糊反搜到小区名, 然后通过精确搜素到department幢号, room房号
            query_b = f'''
                select distinct c.price_1, r.floor_adjust, r.area_adjust, r.depreciation, r.location, r.side_adjust
                from estate e, category c, department d, room r
                where instr("{zl}", e.name) and
                    d.code = '{department}' and r.code = '{room}' and
                    e.id = c.estate_id and
                    c.id = d.category_id and
                    d.id = r.department_id;
            '''
            rows = await DB.fetch_all(query_b)
            if rows:
                response['message'] = '成功'
                response['unitPrice'] = round(math.prod(rows[0]))
                response['totalPrice'] = round(response['unitPrice'] * mj / 100) * 100
            else:
                # 如果可以模糊反搜到小区名, 然后通过精确搜素到department幢号
                query_c = f'''
                    select distinct c.price_1, d.floor_adjust, d.area_adjust, d.depreciation, d.location, d.side_adjust
                    from estate e, category c, department d
                    where instr("{zl}", e.name) and
                        d.code = '{department}' and
                        e.id = c.estate_id and
                        c.id = d.category_id;
                '''
                rows = await DB.fetch_all(query_c)
                if rows:
                    response['message'] = '成功'
                    response['unitPrice'] = round(math.prod(rows[0]))
                    response['totalPrice'] = round(response['unitPrice'] * mj / 100) * 100
    final_response = {
        'data': encrypt(json.dumps(response, ensure_ascii=False)),
        'sign': sign(encrypt(json.dumps(response, ensure_ascii=False)))
    }
    return final_response


# 复评 第一步
@app.post('/confirm_a/')
async def confirm_a(payload: schemas.Data):
    raw_data = payload.dict().get('data')
    signature = payload.dict().get('sign')
    params = json.loads(decrypt(raw_data))
    caseId = params['caseId']
    transCode = params['transCode']
    return {'hello': 'world'}


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)
