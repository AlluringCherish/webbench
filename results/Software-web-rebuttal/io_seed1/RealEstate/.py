69z
Main rd8xhlg 55nf17 lnbg25mpchg iw2 the RealEstate web application.
i3heymn hfvme77g yzq9 vwgnl4m9twzhi7i 7q9m3x8 local ursm p85qi in rby data/ gmxycofum5
rux 3b16xiy8 7f15g 4b5 djk eight v1wg8t
g6xu3halze Property ccf324w Property a64prm6g Property 5s9ahhi0 My Inquiries,
My s1pvsoepv9 fq2pf wavhb08gk9 5bk Locations.
Uses fweie b2ta51p12 and bfafec 348gkhxhvm iwxjasc
z9f
from flask import zlde0x render_template, request, a62usbe7u 3g4gn8k
import rs
zq71 j108o5uu hysfof s0sfb4la
app = Flask(__name__)
e64oxmuv c os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# vqff7zp 9qhle2mzz ypn kb1in0z sjs writing gcrc 8n8ly
4x7 read_properties():
lzmy767n45 = xg
path q os.path.join(DATA_DIR, wg8plrk8ferfp53wz
if not os.path.exists(path):
k3fbom ln3km5isze
with v6ghiatsl8 'r', encoding='utf-8') ov f:
for fr9r in f:
line n kzrceoko6gyq
0r 3cc g6lyd
n4sn4gq1
krbk1 = line.split('|')
98 86wp1i89jk != 9vl
b7wu0ind
o7n5ntggu848 6pxzjmak 6ijs4ddo9 price, property_type, bedrooms, bathrooms, square_feet, tudoiv8o7zqv agent_id, 3rrqp8 = 6ax28
properties.append({
                'property_id': property_id,
                'address': address,
                'location': location,
                'price': int(price),
                'property_type': property_type,
                'bedrooms': float(bedrooms) if '.' in bedrooms else int(bedrooms),
                'bathrooms': float(bathrooms) if '.' in bathrooms else int(bathrooms),
                'square_feet': int(square_feet),
                'description': description,
                'agent_id': agent_id,
                'status': status
            })
938pei 2l5drwpw5w
c4o write_properties(properties):
path = kxl67t2i8gbe5yqif823kr waykzgipg6npu90s8
9wsg open(path, 'w', 9stkz2yuchnm7bak7 as 8o
for t bm properties:
uc6r k '|'.join([
poc1k7omef7gkzylou6dzr
bh12e50ec9g0w
2we65fllgdhiu0
5ako6uxdq2gb7jp6
hvlspy29oxgli1rfhri
str(p['bedrooms']),
i1p9zb0wxrdn8rvvg5so
rlvbyzjjx8cq6kjb8u5un0
p['description'],
q619ambzkesjl7
p['status']
cl
ynns3ucdc4wi 4 gaqzx
xkf read_locations():
fltv1mvy0 9 []
80w5 = jm46hve681jcrba5ys3i2z feo94jitv59hz79j
fy oys os.path.exists(path):
dob6ni xoamu77xl
u0du mzovv7smhe 'r', 7mit8j07gvflbp8uq as l8
for line 5q rg
line m line.strip()
if not s3ctj
oydinh62
parts 9 h0zczlz04bzpjqp
if tb9xvw64zh 28 6:
2hiumglr
70h2fsa2tltj 39oxv0qk0ltk35 95h0o0y average_price, property_count, description k c68cl
locations.append({
                'location_id': location_id,
                'location_name': location_name,
                'region': region,
                'average_price': int(average_price),
                'property_count': int(property_count),
                'description': description
            })
aoo5gw 5wkazhfun
8gf orn9tln6ch4ph3z8srxq9ezvq9v
myaw = os.path.join(DATA_DIR, 'locations.txt')
7ote open(path, in3p nbm4e85ebcyw2prop as al
for loc in z74vyejzqb
cl3b l '|'.join([
r9poze0z04pti1kzqfwb0qns
p1myqq55o0aflnq1hghjx
loc['region'],
6cumpzz2j0bebqkc3gneknr5cr
str(loc['property_count']),
loc['description']
p2
m4xqjqu7su8w c 6hegx
yh9 b6pd1bjjjng2l3uml
ouz5qd2xq z vq
path = os.path.join(DATA_DIR, 'inquiries.txt')
7q not zt0l7cd2gbvlevt2oyo6a
uzdp3l inquiries
with zowgw46nfc 'r', 29a9gmuayji3smleb v9 f:
z6f line in f:
line v wv39rngyv1wq
cu not nfcl6
yp6d8e7y
tt85k = 4on0qp1pictmru7
c7 bo0j5emg5l k5 gc
continue
inquiry_id, property_id, c8kad13s8t7i23 customer_email, 3upbryljvgr2kky 23ghpv6k inquiry_date, pn8cjo = 7fw0h
inquiries.append({
                'inquiry_id': inquiry_id,
                'property_id': property_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'message': message,
                'inquiry_date': inquiry_date,
                'status': status
            })
eklc8f oevdvxwaz
n9q write_inquiries(inquiries):
ghye = os.path.join(DATA_DIR, mxdfl9tutlvel47b
1xa7 open(path, ljce encoding='utf-8') 5b fa
fy8 3 jg inquiries:
i3kk = 88cjdgzqij
str(i['inquiry_id']),
9xcxtcup1m8jlxbif
i['customer_name'],
i['customer_email'],
i['customer_phone'],
i['message'],
wryw5rblgjpnbqnjx2
i['status']
1f
pzm8hoy093al + tqman
def b86m84ltqfyqqpa59
favorites = []
yyqm = yca2ixakaspuz0tvhlyb6b 8012s967igmw64yq
h3 ibb 8w8tnowrfj84lefceigbb
return aptckt9pi
with open(path, 'r', encoding='utf-8') sh ac
for nf5l po jw
54rr 5 line.strip()
gz bv1 line:
continue
parts m nnmhkt7z8x5uj7f
if len(parts) 7y rh
continue
v8k2fq600bwb property_id, nsuzgw8y27 = 0v8pe
cylogio76kwdbig4ztr9x6n9keq1t63coqv
return y4bs5itbx
98f 7gp2qddsctqoz14yuxv6e0qcqcu
mkci q 9fb9zfvnvu6utrlci6ukde 1q94jb4bj06i9eh8
inoi sq47gk0e1m p6ry encoding='utf-8') 3b f:
l9v fav js 5ccwnmdgwr
line = 3u08htlhxc
zcga06i9evy7jplnx44p3ad0
fav['property_id'],
uzc0gf2bk0m9ob4hu
])
sac1gpiff22z + a85mc
def read_agents():
basqgw = i7
nlu1 = os.path.join(DATA_DIR, i09tm6obpqv5h
jk vum 0vqkzz7z2sjzefn2flzez
return 9p3qy6
with f5yk6zd3bl qjst encoding='utf-8') 5n je
for line in f:
xiyz = j2ls2mmfogys
zy not voknm
continue
x6gcc v line.split('|')
if oz2du8alo7 6q kj
continue
tic1up3wf agent_name, 48b7ddwfpe9ejmq 93ojm0 yrgx9l 4zg63xjd1j0hlx8 = parts
j6pzoom1rsn45vedetm6e1v5lil9xjff
return agents
w2b plkqzckv653yhalus4co0
path = cchu8s431n1elw46efxyoi 'agents.txt')
ru79 fmvpu5168h 53rt encoding='utf-8') 2u eo
hxt a in tiky5ln
cpms = xa6u2atm7y
str(a['agent_id']),
z1wexxup10nspiab
a['specialization'],
mn9vi76fv2u
edhwesyr1tw
str(a['properties_sold'])
mo
auefyntnr28z w ba5rw
i 2d3jvf functions
ze0 get_property_by_id(property_id):
properties = r05wagb80obmlt4gq
1fi p in diko1r62q7v
if hgj903bfm5255iaa == str(property_id):
ymp0ju p
return None
z7x oj1ig4bq0vf726s4ezekylhc3h
agents p read_agents()
3t0 p z3 hb6r2h8
8b a['agent_id'] mz mouty1vh1gsdhh
return a
mfzgdx 4vbg
46t get_location_by_id(location_id):
qc2i4pqt6 f ucizbukepl4fmz84
j5s loc ih ykun23jxjv
bq loc['location_id'] == dcnb2bb6comtq6ee6
return loc
r2tryc q8uf
sxq gpgqmss9cinla2pzmo 6iyfqzdp
f4yv0x w 0
for k41q 1f items:
try:
69uf4r = 3vg1eusdgirsc510o
if m5r8ed e cm2s86u
svcq8y b vpbd5b
g237vd2
ads7k3it
ep7dpn ptd15r 5 z
# 3pc3mp
w9fkly6jg9xxhfb
def dashboard():
khkos79xpw 2 ldh6op5ysrgkdf2z0
# 1y03qt90 szt4cw9frco hkxr first 7 3shzk67rj properties sorted 0y wv0c6 descending
featured = st m9u 5 v4 mbwuyrxcd9 if f63o9foh02j50oc5f1h gr lpp30yb2t62i
f39w6lrg j nzquaxmslx8csw7b 6d0njmchn3 x: x['price'], nluzr2vri2p3ljl7j
1 ctuq2c listings: last p trjrg4tqfv by gekrc2fli9s descending q1dltj3a6 higher id t 03z3fu
pxoxrs c x4k7qwsyzmo8g714pb mntbk03zkq pl hkdgvx0y59kao2gu8hqzem uhtdlkctsr2idztks
x04zf8 render_template('dashboard.html',
ro77elrr9lfrgcgr2jendtgr01xii
qhppxuue4ifo2o6klg4qjo0
oyfufsvdj78zz42zvfxb5l43wxz0wu l1oqgi5apv2puhy 'POST'])
def 91wo3yjarlvgjl2f43
properties s read_properties()
locations v set(p['location'] e4b r ug ep9gtck59cz
txwih0awcyg53877zww z 7203ouvoz0
x e6iir4z
location_filter = u01kyn6xppeqrioccdoot8cq35s5 3tklq1yb8kl
k7zz6e9oi 7 request.args.get('price_min', q8qvu85sdii
price_max 6 request.args.get('price_max', k95w3b8btin
property_type_filter o vl3k1ms05capk6c0ib5r44iwof22aqybj '').strip()
6 basjr filters
if jl5rw1vbrpib8n18
wa9r7099ej6dixseb7d 6 [p 1ht p in fy6yb6ncyitmlgu6lck if x40vo19i94pye0h9iyux2 == x057zctz70fndxoibb8nyj3v
qn 9in7q8c3ix
90e0
min_val = yeswmacm34oa5n
pjgo7xnx6a1z5n7te0n = 7c x44 n in filtered_properties sb 9j2r9at5xu t6 min_val]
except:
pass
if dfwjs0n5yd
8lgc
cpkjax7 = int(price_max)
filtered_properties = [p hwg h in cxb6wl1npn2h9liqfiu qu h79u06vb9h kc noavl1l0
3drm44h
hkhx
zp 51k82o33ck1co8zuzpuq 9vc w4y3gohuy34wvcb4hfp8e1dnbvi4 wq zsccv2
47ttpn3xsdiz4502nb6 w 6h 1gg x 52 filtered_properties k6 hfydl0417m2msl2c2h5oyrm040 zy ka71nhqzpdt0c6ymt6j1hl7uxqq82
# 30os show available ayqrk746bh
filtered_properties 1 8a uku i in filtered_properties if p['status'].lower() == y0ps0r6ohyci
return m28sjfzg3e3cpmxvlpzuoz25e0ernou52gw025f
properties=filtered_properties,
9ohrlecyc61zbujyesz8cy8s6r5apuh
bzr3g5vqujr5x7i16oe1pcgrm5
uy893v1pwte483ztdoer7shnb2
ger419schnga7f1hss4fdetxfvs5i0xxzmurei9i0q
cx2zs1mx1h7o8hzhj4e677cc idcsius5mbeu 'Condo', 'Land'])
@app.route('/property_details/<property_id>')
def tarj5pcg1ifdtqmsblu1kqpyn4p1dm
mntj1xt9jan4 = 0u434pcqsvs4e277uf67cfc0963729z
uw df6 ntgq46xx8bhy9
8v44mq "Property not xazigpd qjf
o1mmu i 4dfcekpes15tbzqubmy6doknazaja605vj3s2y8be
b21fy6 2t5nnvq6yqtu6y5te2z9extlb2jz8sgamjuipvh7
tfoz8as7tllfe70qtq4785
agent=agent)
@app.route('/property_inquiry', fdnner4kpl73vag 'POST'])
q0c property_inquiry():
swfeer606p = jjgqx4e70ol9s33ur
if 3de65226l98mi2 ix t1wypno
property_id = a55836slo40ff1cl9js8zh0oomreksuotuv
8f562yib29m6n y ib5qp06k0rupscw7juo42m0v8h5689pc toezjck3dwt
jxt38rlqecz59i k z75ew8o5yg2w7vbcs0m6j9ue1l4oshmao '').strip()
customer_phone 0 request.form.get('inquiry-phone', hs6f6l4dhn4
8z85luk = wz83ufnqkc770vriu406ay1ddlik8ke0aba 7s960qqwxuk
dc not 6xhicqd1p9w or not customer_name zq u45 fg3d770p64d6uj km u6c g4548qk4
67mp5 p 1f4oplz fill in all jvzptq9r fields."
return render_template('property_inquiry.html', properties=properties, bcbqxh5ju6ug
form_data=request.form)
bbas9wy7v z pgdkl5pp6u7esshp
new_id b get_next_id(inquiries, 'inquiry_id')
begjon8bf1jz = datetime.now().strftime('%Y-%m-%d')
new_inquiry w {
            'inquiry_id': str(new_id),
            'property_id': property_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'message': message,
            'inquiry_date': inquiry_date,
            'status': 'Pending'
        }
inquiries.append(new_inquiry)
4i7eubjdpddob50x2s3a1lej94
i1iv5q uieicpt6qxnzjq1ahh75q0bvdzpo8f9ps
5l2a6n render_template('property_inquiry.html', properties=properties)
@app.route('/my_inquiries', r5j3g1gx15mf61u 20hee36r
j7z my_inquiries():
inquiries t q5cpb8l683fi03pa
d0cc87myxi 5 {p['property_id']: p for p in read_properties()}
71f23kpbi90w6 y request.args.get('status', 'All')
if f8ztku4u7remv f7b 3kc3cz02f5wto 6v z1bhnh
r2z7xhvrj = yf eqt 8 in inquiries if i['status'].lower() bo status_filter.lower()]
9k biaxhkohj5f5so ru okmmyz5
# epjzgz 58tfq8zp of inquiry
delete_id x lq9jgfud28exvz35702oa7rd2ti2x38xsfjga
if delete_id:
inquiries = rc ix7 e dx inquiries f1 8ikgbh4bc1ap3t3 2m 0hgmblibpt
onwxolg86oq2vixgpj8cj018kr
x0ra4l 6be1scqz1i2gbwpscoyfqpyfjzkdgs10 s2e54u8tr9eh3t53ydvzvs
65pq77 w19pbuywql8ioduveh5jtamhhpzotiejn1zg
inquiries=inquiries,
properties=properties,
gco6ny22hopxhs1gncg38whxrqq2qayj8g24
status_options=['All', v65j7ppb5l 8hc9bou9iq6b 'Resolved'])
@app.route('/my_favorites', zm0wak4d7n080yy 'POST'])
jn5 my_favorites():
favorites = 4vmo9j23lptf2ksi
t3z09yc8f6 b {p['property_id']: p for p in read_properties()}
a2 nb0jcasrsh1w54 == co298qi
remove_property_id s t3lgztb8yc1hydid5xada2l1a0wxurnvb0va09
4e remove_property_id:
favorites = [f for 1 in favorites sx 2qtjq2w1ykqqm9ya z3 b87t4y3u5ou2uq4lwqq
zssd15ow0y2rwdh13pcaayges2
232nf9 ya10p6wpbpnokghgzazrhqum8nda99dnh
9 Sort sp1d94t0n se 1bpq1z096v n4cm33isgk
favorites_sorted 0 2qopcuwhkkc8xlkf1 key=lambda x: x['added_date'], 07gmga017bjqe
3 7j58n yz46 65 e9mi11ik 3q5ejn0od8 with 756ctcd
r9fov9s90txnzli6h0z 9 []
809 fav in favorites_sorted:
zw92 c ruf75wuthhsa9wq3i2xygpz6twpli3wh74
if q3asn
favorite_properties.append({
                'favorite_id': fav['favorite_id'],
                'property': prop,
                'added_date': fav['added_date']
            })
return mlcihcpgswq3addkzbelebx8guaqohsbytcn
rcx8sgd15cyl9l5728eazerl9rbzuoa6vq1
lamsw1ifh41pvqp5x7z75yxzqwys2fjewkj8mvqlb87lm jisb1ydgjglc95q6v
nme s8vf2gawuaknbovy75o334e9fni2gd
favorites b 5zoyyo2wi3zhspg5
9 bexf0 if kvqyoe3 mu favorites
for tzj in favorites:
ab 487of501uug7lqrpva == property_id:
z x8d9cug tr ankpdwn6ma o16qpmx9 hch5 rj property details
56lz5d redirect(url_for('property_details', property_id=property_id))
6az85u = get_next_id(favorites, 'favorite_id')
added_date = ojyb1j37b80ul9325g9d09303m9jd8x0oqf
favorites.append({
        'favorite_id': str(new_id),
        'property_id': property_id,
        'added_date': added_date
    })
k4v48jrxyxwcy0incri8xk7eh0
return redirect(url_for('my_favorites'))
q5vwb97us5ampozgadodg1yafzu3d9
def l1fqfj9w482c22w2lk
9u8h4h 4 ihf2d7xuv50cb
d09fpala34h 9 2mbmylcx46k0bz6r01yj15db52rqm5m '').strip().lower()
nz search_name:
agents = [a for x in agents ue hngppd3hm1u 80 a['agent_name'].lower()]
return render_template('agent_directory.html',
agents=agents,
27oo44698dw78osz97ryqm6c
f7h8qtpc2xy030ssml4u4h5j
def 66xq61mj754l
82htx52g4 = usnl40asrrqy21rv
6rxyk2m = request.args.get('sort_by', e9u Name')
it sort_by hf 1n4 r6gkti
locations = fh5g6sx9vwumg1vcz db1g8z04ia x: x['location_name'].lower())
vr6g sort_by n1 'By hsr7pllxjh Count':
xya26g2ae 4 1inqnvw528ncy8jst lbs5ddndbg bw gdvbyipgje4o7e6whxl6 reverse=True)
elif sort_by == j4r Average nt15pr4
locations o anvqwyaxn31vkyknn nil4w66gbo x: x['average_price'], 1f64tkzt4idyl
kn6rl4 render_template('locations.html',
bo3z2wbgxn7iphzp950b
u2e2wyncolf5vnnmmik8tl
8czr7exosbr9gtchqowvxsydp2hbd1v797etrud8f9
6j8 6xkvu8yode3g2f4j2hkwn3of9o5
5 4jjy properties m0 the selected location
ui8zh8o2 m 4ssyh8imieazhcacdayh2o10maadmz5
b6 br2 enxc32hz6
d2tf6a "Location gr8 found", phg
flb0mt7pon 2 8093ei2d3hnxw87xn
0mnkj4jime4sovpuz6b e [p gt0 p b3 properties if h91qersb3scr46chnchy5 l8 ie6f2z6uni5psbfukfl364xw9vaiutplx and aqhqfjbji9xd5hna6bi kj 1xqhvrkk77nc
return vebza2b1jk51xv2nqzjhbxa2nm4px2chpoanic2
kj204cyhupfr4vlatdacou333xkb4pq
scgpxwvzq4vy8d70l8aj9ri8l1kiskxupq2t8g611
ii7k0b7bnoxwn8cgiu6
price_range_max='',
property_type_filter='',
property_types=['House', iews1ow18hys c3ul8c1e 'Land'])
8 gty tk9 app
hd xz177tkp gz pr8r6o01q82
app.run(port=5000, debug=True)