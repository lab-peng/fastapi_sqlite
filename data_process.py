import pandas as pd
from sqlalchemy import create_engine
from config import settings

DATABASE_URL = settings.database_url

engine = create_engine('sqlite:///./db.sqlite3')

# x = engine.execute('select * from district')
# for i in x:
#     print(i)

# engine.execute('ALTER TABLE estate ADD y float;')
# x = engine.execute('select * from estate where name = "阊胥路121号"')
# for i in x:
#     print(i)

# x = engine.execute('''
#     SELECT name, COUNT(name)
#     FROM estate
#     GROUP BY name
#     HAVING COUNT(name) > 1
# ''')
# for i in x:
#     print(i)

# y = engine.execute('select * from category where estate_id = 1828;')
# for i in y:
#     print(i)

# engine.execute('''
# UPDATE street SET name = "周市镇", district_id = 9
# WHERE id = 67;
# ''')

# engine.execute('''
# update estate set street_id = 26
# where name = "文卫新村";
# ''')

df = pd.read_excel('E:\\abc_admin\\20220831\\小区估值数据0816上传.xlsm')
df.loc[df['区域'] == '常熟', '区域'] = '常熟市'
df.loc[df['区域'] == '太仓', '区域'] = '太仓市'
df.loc[df['区域'] == '张家港', '区域'] = '张家港市'
df.loc[df['区域'] == '昆山', '区域'] = '昆山市'

df = df.drop_duplicates(subset=['区域', '街道'], keep='last')
print(df)
x = engine.execute('''
    select d.name, s.name
    from district as d
    inner join street as s 
    on d.id = s.district_id;
''')
s = set()
for i in x:
    s.add(i)
print(s, len(s))

t = set()
for r in df.iterrows():
    t.add((r[1]['区域'], r[1]['街道']))
print(t, len(t))


print(t.difference(s), len(t.difference(s)))

for i in t.difference(s):
    print(i[0])




# for row in df.iterrows():
#     print(row[1]['街道'], row[1]['小区名称'], row[1]['坐标'].split(',')[0], row[1]['坐标'].split(',')[1])
#     counter += 1
#     break
# print(counter)

# x = df[(df["街道"] == '虎丘街道') & (df["小区名称"] == 'MOMA现代美墅')]
# print(x['坐标'].values[0])

# estates = engine.execute('select s.name, e.name from estate as e inner join street as s where s.id = e.street_id')
# count = 0
# estate_list = []
# for e in estates:
#     estate_list.append(e[1])
# print(estate_list)


# for e in estate_list:
#     # x = df[(df["街道"] == e[0]) & (df["小区名称"] == e[1])]
#     x = df[df['小区名称'] == e]
#     if len(x) != 0:
#         estate_x = float(x['坐标'].values[0].split(',')[0])
#         estate_y = float(x['坐标'].values[0].split(',')[1])
#         print(e, estate_x, estate_y)
#         engine.execute(f'''
#             UPDATE estate
#             SET x = {estate_x}, y = {estate_y}
#             WHERE name = "{e}";
#         ''')
#     count += 1
# print(count)



