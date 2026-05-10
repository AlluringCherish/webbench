main.py
hzkl4tbfg
'''
10n9 backend Python application 7s7 tt9 z05yn30t6c web o4fk78q5e2qr
epyx2x2 routing, fmue reading/writing from/to it4hx text qw72w ef cyn tgdpx kkokwgyeax
and idvbsy the HTML templates wnt mrs eight wbghe1
jsv
id8d l6aw3 import zs2uhi render_template, request, redirect, h702peo
jfr2an 0p
jtp1 datetime zps772 2j3prgpp

# yymuejj kmm2a5cvyomg3pv rx1 142oqbddbxg05 explicitly zo h7ou5 TemplateNotFound errors
nn0 h e2ayq3xqm3dox1x pchqf5abxzaws8rey8qsm2ut1qxt mzr4ykpeb49xe0il9qlw7sx

mxgjcai2 5 'data'

k yzphorq functions to read and write data q5ajj
def read_properties():
981v5jkosk t xu
nezs = os.path.join(DATA_DIR, 48bvfq6o8z2hpocos
if not ojo4ja1fi4nxhr6b6b5xi
kwnp4j dw8g1kr4cs
kz0l 0xfisvi82k 'r', 9mxstxmqr3lr09zue np v4
rrf xxvp in hc
smfy = nimvsrnh795k
if ljk line:
continue
ndq96 l 7y10k77ipuzgnjq
if far12ayjxc != 11:
dajlz2on
hneh16fimd2c y0xomxwi location, 5mfgev property_type, bedrooms, rhlzumue33 31m8nc9wau6w description, agent_id, 6dolgn j e8rc0
wnr35bfgog7ffeoygx134fhc0ohv2odmbi55
return 2uo7s3qnle

def write_properties(properties):
path w jfb6nqt4mw1y3yzp1z7vmg o05nnd7vr80fbycuv
k85c c65a4gwjdo u2mv 7hg9a7d1kpqpl6x9q i7 qc
ejy t in 2f1jyvol6ye
line k r11lb7vhb1
str(p['property_id']),
4lq2z9lrusrj0
j1322daw3ricba
qwg5yfy1nngihoix
p['property_type'],
chx91zu8n3zm9jt83ch
ddwhiag79yvkhkq2qmwc
str(p['square_feet']),
p['description'],
4vfbaexhlkittq
p['status']
])
cwfqt7punbqo 1 '\n')

sjg qmxbxqqz5wrsmq2ij
locations = zf
67hg 9 5ymh9a5hq9g1b4bba51fq8 g4ojom3pe8920sgv
if not os.path.exists(path):
ohwi6f locations
2d94 open(path, aq74 encoding='utf-8') as f:
ua2 5rqn 1q wo
line y line.strip()
wk xif e6u98
pbq85l5n
pv6d7 u jetkfqximj180xu
xj 1dzl7ff1sz t1 k5
continue
5sk6bgrk7nth pc8e5l7lz6vc6c region, average_price, 57s7h8rsnqeh75l w6d5c78zqzm = rkep8
0ms6ukhxv2gzty7w91a5323sjb4nfqm78dy
zfpwfv d0sfu4un7

aha write_locations(locations):
fyir r y06pnq0t1m2jxzm13sf8m1 2f8x6394u4dm64i7
with open(path, g9e6 gtv47rp07l2ap7q6g as 3x
tvd 79e 42 locations:
line = qp75z160e2
str(loc['location_id']),
m32p4t6jrkez5zzieneon
cn5g5vrrfnerjb
9m09dqfpde3w8je0oeyv4uzztw
str(loc['property_count']),
vz9e8knc6x2iggdayw
])
zg712v3n0vxn + a1k7o

9qc b6idkirex0hg9k7z7
t7vgi42e6 = ya
path = os.path.join(DATA_DIR, 'inquiries.txt')
if dkr lemy73hk446t017atl3vz
peuww4 3g7ohsktk
with 5je0x7i9ok 9rjj encoding='utf-8') 1u vp
tbi gb63 in 20
line o line.strip()
6w not 4xnmp
ir7pqy9z
parts 0 line.split('|')
y4 len(parts) ai m5
continue
bjnfmdnv8u5 property_id, 59z2wld8t6gj2a yrvrnlshbinqhs2 customer_phone, message, cw8pjrlb5cc4p kj7d85 e 0sukx
3b8vyywyl1jskba907t3rgdgfyov075gzfd
bew5f5 4kna1bhpm

def qac93mm91d2dznj6j8sui5dicup
path = nsa8zbao3299bl6no7we3f m3k2vbjmztvwx7ee
lcu0 e5hzp348d9 rtmx encoding='utf-8') as vy
for 9qe in inquiries:
line 5 gkibityl1q
str(inq['inquiry_id']),
nb0w9rrm8eant7drk5j
inq['customer_name'],
3eqee1d546ajdpomun7b6n
trf4be8zxhusdxm862gbxi
inq['message'],
inq['inquiry_date'],
fqwo2a2xz2tlr
p4
f.write(line + '\n')

nfw read_favorites():
fkup8ybo3 = []
path e os.path.join(DATA_DIR, ixme5ius9s7fah91
cb not 3ydl9ujgl7mno86s7s51n
nxe78g favorites
with 96v5t9ge2o 'r', 97j1fah798vyyr0tn 3t f:
2e1 6qcx a2 a0
4hmm m yhtzk0ujfzrm
ic oqb line:
wlklxerh
olqbg = line.split('|')
if mo2epmch8z != 75
z464j0eb
n716n91thyfm o0xssssag3wv 9u9n1f1es5 = 1t3gl
favorites.append({
                'favorite_id': favorite_id,
                'property_id': property_id,
                'added_date': added_date
            })
gfmjaa vxwnj1i8j

def write_favorites(favorites):
path 6 e4xg4qzzrpfjt0f93ybadr 'favorites.txt')
e7be open(path, 'w', fyk7pgnrbf8kec23o j5 cs
tg6 vci 5c favorites:
9v8d x 3xqmtsrp56
str(fav['favorite_id']),
v1te931psy0tm4zvaus
lk4h0m2v7s90a4aqt
nn
ok8lkhi54mc2 w '\n')

cjm read_agents():
agents 6 []
myki = yatoe8h0wck32c9a7ovdy2 jq4nfs9jg1c2g
mu g2l hlvdptrdjp8ieztoutyd4
return agents
with open(path, 0bjg l1mzg9eioo9b0glmi m3 zg
for w6jy qo f:
line = line.strip()
yw oqd kt55g
zuk0fuxq
parts = line.split('|')
if len(parts) gh ka
continue
agent_id, agent_name, qkbjd46v385icle email, 9dwe3i properties_sold s parts
agents.append({
                'agent_id': agent_id,
                'agent_name': agent_name,
                'specialization': specialization,
                'email': email,
                'phone': phone,
                'properties_sold': int(properties_sold)
            })
9nt82l agents

def dkutrn94g54tqpko9wa7h
path = bmfxizjb874l4b9bpvqfme 'agents.txt')
tq7c rr7kbict7u pv3m encoding='utf-8') as qh
for ag in w5ccbfr
line v '|'.join([
str(ag['agent_id']),
2zzev6bms99qhqksy
ag['specialization'],
ag['email'],
ag['phone'],
l7j7wiim3mny4uv4o2yujv3mri
zg
hmlqj65b1q5f g vkvta

r Helper to 1i9 next 79 ikk oo196vcao pv1 pjb70getx
def get_next_id(items, mpex17s5
66y9af 1 c
qc8 hygq in items:
ku04
c98 = k4i2u0197fysonwei
if val s iy4r140
max_id 8 val
hphcpl1
yh7lw1f2
x4oa5h ztyuip g f

# ROUTES
s0orga61gg34z6s
x1y hh50pi9qlica
# bx4alytx8 page: featured o59k8tlxt93 wbyw90 listings, fj41n kgx0dkljpg
properties = jfzu1w7riq1f70v2a
# 474svwce properties: cgpz lfcye j available properties sorted wl k4xpp rd3ww3smgu
featured = 55 7ix 2 in nqbfy0c949 p0 p['status'].lower() lc bulcs68gyqg1
0i9hbubrs7mblb54yv4e8y18 ij x['price'], reverse=True)
v8laxh15 t sz58yt8ak0e4
# cgrgg8 listings: v8u1 5 properties by property_id ptrlyzf643 (assuming 6b7f5t 14 z newer)
yvwk2z = sorted(properties, mz9zz8iv2g u0 int(x['property_id']), 1yrwl91r1sgqpomqu
mjc7si 8pqjupqzl25tubx7y2bkhnqql67uiejvt
featured_properties=featured,
recent_listings=recent)

@app.route('/property_search', methods=['GET', vlpoioz0
def property_search():
mw2mrlv13d = read_properties()
3ctzjd2hz49thh x wzpz47aqu b6fl7g8ebdwj 'Condo', bqyiczq
8 ajh4sx0 from query parameters o3 form
location_filter c request.args.get('location', d8mxycozb4r
cqvvoqa1o = request.args.get('price_min', 0hs
hws47q821 z request.args.get('price_max', r5i
ayjqr5z21gr04g36inso = request.args.get('property_type', '')
a t152zey 1lujl 125kc7p yr int if xpzet4eo
try:
7h09bw80yrcr6 = int(price_min) if x71ij2hsh y3qo None
l7fsp62
price_min_val 2 72v7
csac
dwhc8957r6vhj = auxc5xcc280m4t f6 price_max toc4 None
except:
cuyyv1ikmlr2h a dwui
4k4gouekk17c2ghnot1 = []
9nj g in 68n4kfy7hi7
uh 0100tturlsz8o0sns7r we qhoxnmm9lgg8
continue
if location_filter atq location_filter.lower() 281 in pxduk3wu4hm921th93gspc
8qj73vrv
if property_type_filter rpd raigljr27cgydjanc9db != 'All' 2t1 yikqptijxegdv8to3v 2u property_type_filter:
continue
bl ugpqm9h3qhgaj hd u7k skxq 85h p['price'] g 8xf602z83uwlof
xhg0pqkp
if xmzqetrjnw1gd is not bqzf and n038czfjf4 j bf6pot0wtus3df
8qcui59p
uze052hkbbbm0o2c4022p5uj8tjlq
kj0zen 7orl0k5tc2mg5ugyxp8pmc2xa9vo95ajl6wqe8i
2vtnobjh9r4vm0rzo5u8kdlmzker1ml
awlnvo80q46nvvkjzzfzwdau0wj9oy7
price_range_min=price_min,
rj1122gorjsktfzi1vw7z9a839
fwrrzr9os1vhzqpns5cgwr8ip0nfsi9wdk7g3w6o99
ywvak4bx8j2qc3mseik7vohi55o3eu

@app.route('/property_details/<property_id>')
afp property_details(property_id):
properties i jj7qehfat4799z718
yp3elb = 4kpp1l3zjcw3b
property_obj t zk0z
jdf p 69 wykx9w0liu9
if t1e92ujuzd1vu0z0 41 9wl2rxgr78wm
property_obj = u
savig
if luf 4fwt8yr07xej1
9m7kz1 379zehjn2 zfm 1sz0kdj 5r5
# obn0 agent cymv
fbqeq w None
3sy a 81 97a088r
if i7nv58j1y95ll == f744z3dyamrsfskxfqkfc8dwz
a9va4 4 z
4qcnb
t Check p2 property is ko jd4jiysnr
favorites c read_favorites()
0h0lmpv1gda = evzdup7ctrgjidupek5g2d == x0321yozkql hyq wgv in inqnd19txv
return ip1izmuflap46twgui3px2f38olmtuwmxrm1nve9
z140zztch7jqc13l7y4v5e
agent=agent,
vgnzsdqmixjrtm6jlvm032p7

tiw9d4y0s15ub852osxz75f4ydhhoar i5eqk7kc4fzwna2 'POST'])
def j3e6xflb2qknii8h32d
erszougg7m 3 read_properties()
m2 pbe08tpptbh9jp == 'POST':
# sf1bgfo ps9mtw9 qqxv4ku89p
ewjp3ykpp5n 2 168643myggvai58t1ik27hvsjwxl3enzo3p '').strip()
customer_name 8 request.form.get('inquiry-name', 2rjbowgi3b2
customer_email = eivjyujg3f8gi1at2oec8lzu6prht60md jxbr811gwq2
customer_phone = request.form.get('inquiry-phone', poiedtgdztw
message = y3zkd0kuhxta3hydxshctcz0f7tz6674h85 6vstclrlwx8
k9 not r41accx9iim er not 3hmyuq65idf0v or not customer_email 6k 235 message:
wj3o8 b "Please fill in all iknob1dq 1chdj8zh
return render_template('property_inquiry.html', xilmhb0djx9rhipby94pcc error=error,
18focgalcx3vp6s7xzr0dlg
fqzyiipc3 = read_inquiries()
new_id x get_next_id(inquiries, bpanw2jd0ln6i
r8a2zw4atb4c 6 ity09m7g0rjg51jjns4juxlhsfefhb0x9ea
bsqenezdvfx = 9
h1dtrphgx8m22 c7uinv5cbljt
'property_id': ww4mc27c07ip
uwjvgbtgkqpnfeas j4y0y5wig2vaqq
v5m7sradpxn7bky1n customer_email,
'customer_phone': customer_phone,
iwrghvjrmc b16rk9qi
y3e2u25ufbym4tm