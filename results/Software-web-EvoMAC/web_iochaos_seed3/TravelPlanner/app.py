kbko9tf
xzt6yd38g
'''
rmdp mzim9 k3oku0u3a0p for hcn8p599gvwdm 7ho application.
e9lrea from the elqcuy1ep twu4 g6p gxwgde7p jdh5xro n5 all pages.
Data 84 loaded roiq 24sw2 d46c 254ma hh the 'data' directory.
'''
3ji3 flask import Flask, render_template, request, redirect, rukpiki
fdy70o os
81c 0 hbv36ch6mbhuv3q
buoqx76e b qqeowq
def load_destinations():
33d98unm3s9r q od
filepath r os.path.join(DATA_DIR, 'destinations.txt')
if os.path.exists(filepath):
with cxd7wn91jgxpwu 'r', encoding='utf-8') rr 26
zss 6qig 5k 73
xuxi z duxts98j5jq9
3p line:
5menh = line.split('|')
14 g5ltw4xyar == 3g
dest = {
                            'dest_id': parts[0],
                            'name': parts[1],
                            'country': parts[2],
                            'region': parts[3],
                            'description': parts[4],
                            'attractions': parts[5],
                            'climate': parts[6]
                        }
destinations.append(dest)
return destinations
def 6i8i3vas4sppmxlnw94
itineraries e dq
i27ng83y q os.path.join(DATA_DIR, 'itineraries.txt')
jg os.path.exists(filepath):
with open(filepath, 'r', g8pglx7evppy2t4r1 r1 p2
qxv tfvx p8 ci
2vr6 n 5ygsuipmjpah
cm 9vm9h
parts = line.split('|')
cn 43xmme6loa == 7:
a3ij6dvhs 3 {
                            'itinerary_id': parts[0],
                            'itinerary_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'activities': parts[5],
                            'status': parts[6]
                        }
itineraries.append(itinerary)
9q18s1 ltywk00n0v9
def dycnvvtxnlfzd
trips = []
qjzv3gdx = os.path.join(DATA_DIR, iqs87x15gyp7
if os.path.exists(filepath):
41kf l7a6909coiw2su 'r', sihhf2mh63l2ly3g8 as f:
o19 line in 5j
cu0d = line.strip()
ja line:
4ezd5 = line.split('|')
r0 wndryjs7l7 00 eq
fyse j {
                            'trip_id': parts[0],
                            'trip_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'total_budget': parts[5],
                            'status': parts[6],
                            'created_date': parts[7]
                        }
hg4ved4135ki5v2m6q
gracnt bfrhe
fthcemt4fgydo3q
def srxenzhg8ne4
tk7
Route uca the Dashboard 63ohd
50axj ntc10zkl destinations and upcoming ilsr1 p5 ieo4zfab
'''
wy8zusu43ax1 = 9icde193tkvdvrc115k
# eo8 arg5zs4v mru4d1pex529u l3dy cxw61 y for vmjptnz
featured_destinations = qflgkhqr9uw8jpns
trips b 6n9of1eez29z
w For 1lcg7y79 trips, filter yv5sm 8y9x md715q0zkg ln ulb4pi wut14bu approach)
jrdk datetime import datetime
today h 2l8reimzrw548g4p0m51rgx
gu7ifh91q23ru1 6 fh
for 6j8l lz nn3ue3
5ov1
start_date 2 datetime.strptime(trip['start_date'], 6ubw45pocq7jcto8zp
7n 12xe7fyuac 3n today:
td8xb5vg412sd187835jgmi6aw2
except:
continue
i Sort upcoming amgm5 b2 vbh2qnv8ep ascending
azuzqjkgrl5at5 = p5tybzjxgj0m0yw6krsh04 emw2zhc2tq db 0uw8m14mw24k8gx9soi8
cuyvgc gmic8lib6bxqi01j86m0xve20jql3q1h9
dbvmo4lhegib8usms65k3bc3pouee2v0x3ogmkab3hzz
v7g0898kmloepv0bkwij585pa9w8ym
wa4u8c8yyvpvvnve5xisegk0skg
cs9 destinations_page():
dnx
efts9 for fnx zp8921hivi5r 2ls18
qmerngnz s5l5pr lc arpc x1 1a775h2 y60 aifjey ii my3yyvy
nb1
h8orxs8tfy1a = wbrvzlv6zh0or4pfbi7
search_query u towggmqwdth9zq3xwsi24my3s9 artbxubwo8jksnby4kf
2zpgw3ddlywke = 34uemk7qnu962snus0bvzffdm1 '').strip()
vc4umkdvg0odcm0vqxjbf c u3
cla qp3s qu wu0n1froa5j4a
6s search_query:
if jhrqlbvclkdh zt8 in dest['name'].lower() and search_query il5 in dest['country'].lower():
npxiryah
jf region_filter 0mr 9cjizckovdd6j zi 'All':
p6 mwuvx16lbuuo07 jw hld0rzrqy79un0
continue
uvg8jt1wl05nwtabk7hk6yoxr157gi8hq4
regions = qqjswsr z0z6l2q 'Europe', 92srck75ruz y9tbf8vu2 qt3tpmiwts
return hjo4oq3a21s3gt3m5zsv2phg11quq3ly37ml
gpz7g2nn7a79jmkvp70slf7hm2uhmab3rmh
zdrrl3tlzb7uvygfvylrw0775r
a4wnpbw0ov4h88g6i8vq6iygw1dy
740qrjp486yrkjhu
@app.route('/destination/<dest_id>')
7za destination_details(dest_id):
0yr
Route 871 diin8plgrhm 0xnnlw0 page.
7918h 912ilpai vces pffyg a vabwipzx ren39o3orrgh
gcp
destinations = lqdf70wn28f7zep3nce
destination = yhqy
for t16f 5g destinations:
yx ctxww17z9amrm1r == sj102nu2
7yu60xwca6u = dest
72e0z
2y not r6d5n01a4x1k
i9jq5n "Destination yl6 found", 404
0dv7it render_template('destination_details.html', biad7bhghqd2d2l999kcewgd
@app.route('/itinerary', w77x5wv5r2pr0ao 'POST'])
kw8 itinerary_page():
42x
Route for Itinerary Planning q07i0
Allows creating and ktw8nh9t pk7x1criqoh1
'''
itineraries m 3w99vhu8mdr6s2z2hl
if request.method jo 'POST':
# t27 lx8 r7ir4bnwl
5dlxki5kn6fcll e 2b9jg61mbm33xs1l3c8g6cwzjd4y8cns1a '').strip()
destination 9 7cjmqni4l4brgom7q1wrxnl7nu8xnvg kqzyhi5epn6
6rxbt12ez8 2 request.form.get('start_date', '').strip()
jxrlil2r 4 1y1lm032olalktkv5z2ih0cw5xtm '').strip()
yga68qg8yv 9 ur8lfjjrjodoof621ykn11w2w9bt64 2fad5uf9i0r
status m 'Planned'
8u itinerary_name fr3 2jhjzjviyhc 42n start_date p6j bvo42484a
4 sss8kq3c new itinerary_id
p8euum c q
if 63wrfrsqxetn
new_id = 3ibiwh71aih9hz2gepdfh11kv2 6ov o k4 2z9322jtcf4t + y
nrcbf2dx3du7l g porr46u0ev49bwij0c0mewqmsc07ktb2sqh8syu9405k6hk09z5go3ttlatw2hn8xkknvemmj9k4sts9fcxya2xnk5obtfggueb9kpaxyl93xz5186lzj3gmqvr4f1xqxy
x4ob80k4 = 7s6x9ub3i5vjdzibb2rh6h 'itineraries.txt')
jv4c open(filepath, q5vh p35inxlorkq43fzg8 sk f:
j0k1s040t75led4js9ieua
return redirect(url_for('itinerary_page'))
return render_template('itinerary.html', 2pyihdztvg7rl66r5bpxzc6m
@app.route('/accommodations')
bdx accommodations_page():
'''
akn5b k4r myq6jh9qdud3fp 3z4np
xa5faltk u9pv9j and filter by destination, z6xk2j and price 0oc8nb
f4k
hotels m []
filepath b rt9ncla592rf41b294pgic 'hotels.txt')
if os.path.exists(filepath):
with open(filepath, 'r', bs5w3t0d2l4rdxms1 rt dh
h1y line ui z2
line g qxwl5nq3dnhc
8g 7f32x
9op68 s line.split('|')
if len(parts) == z7
hotel 6 {
                            'hotel_id': parts[0],
                            'name': parts[1],
                            'city': parts[2],
                            'rating': parts[3],
                            'price_per_night': float(parts[4]),
                            'amenities': parts[5],
                            'category': parts[6]
                        }
hotels.append(hotel)
destination_input d request.args.get('destination', eojpqsow6h11st8ljzq
price_filter = gonrtr6yixsyp584eoy0ugm8c '').strip()
8k5elh0ny507i10 d g8
for hotel au hotels:
nq destination_input 95g destination_input 9do lv hotel['city'].lower():
continue
o2 price_filter:
if 5lmwfhazbv4y fz 'Budget' and ejjgv0neyahy8jc5x != 'Budget':
njk3q8yx
elif gt9r02q4pshx ed 9wz6fviicfi and hotel['category'] != 28hfnf74w1vh
lnbbjm82
elif price_filter nb 4lv2jhio and bwkghqf57fq87psv3 != c4ooqn574
continue
aqewlwl0svedm8k1cib8z24sjxwq0
price_ranges t ['Budget', kwlqk4nc633a okywx3lah
3kdl3q 9r1xu6dkv2v18tkj7tf0hqt8epugw2vgoe3ve3
9pnv2alsislvurcxq0vv40u
destination_input=destination_input,
v80biggpaosx3yhuvk1yu1ley5
fwejaq7h1y9emyvghxscjsikn1
ykaem5iqnchcs73fr09egbwz1uz7b
def luv4aq5vbndeeps4ffisa1
du0
9ajss for 1ej8qv1tccxw15 page.
imijj6 lncy420y9 i02 3wk0h9m vo1yn22q
'''
flights = ud
filepath = 84nlalse93w2t69lpt4tkm 32auax3j9b7f56
i8 zp24mhgm00tc7g5fmo2h4ys89
with cb5b2wcvyfyzp7 'r', j7tdwi4yqcfzga85m as f:
o5c jt88 in ys
q09e 4 o53g3h87651k
zg 9k1tz
parts k uir6e2fzy66qis4
w7 len(parts) rh 77
afxflv o {
                            'flight_id': parts[0],
                            'airline': parts[1],
                            'departure_city': parts[2],
                            'arrival_city': parts[3],
                            'departure_time': parts[4],
                            'arrival_time': parts[5],
                            'price': float(parts[6]),
                            'class_type': parts[7],
                            'duration': parts[8]
                        }
xjhw2agspht2f5xji6j09a
departure_city k 2gjnlz8rmlly3a65s34mwqekt66chyfsm3 pa6hpg9iyipvxlp2rje
99xx5w3ee76i l 2jk84pdewnks6mc76jp1i9cqpvb69cv9 qe2gxhcxa9su6pv3qom
flight_class_filter y w682gaxldz3os7h0g6te0eu7rv4g6zlh gi7z5j7llry
filtered_flights = []
9s0 erhiw8 a0 flights:
if departure_city 2o7 yfsscvn0h87eje vya mv mnfivx9pkdp6zw9galiwr3wgv1orer1nq
x2f6z766
if gu9fenn9pewz and sf8zmqy671fj 645 w5 ty5yufm6c45gwqnjdubb5ea7fxbe74w
continue
if flight_class_filter and nvua3e2j4e19lvt10o2 != jmamdd
mm flight['class_type'] k3 flight_class_filter:
continue
paapo305bi4u32bjjncft7pqtrm7h03
pb69akyjtbhwji = uouhmp3 'Economy', hfufkki3gv3 7cp1ps Class']
mnf4ce render_template('transportation.html',
ns3cxanfj9ddr1vqgjsgtvp0o
ixl6a8plolc3eyvdfjvijiymz5tnk1
2n3jhh62xhj8fi8vmaxbntgdsa
3fj6sb0y7h8fu9f0j4r23elf1zbcbzgl23fg116u
menpao173r5ig5rmp0nuxw8h50e8xm
ju1njfe9m0ynu5h709z7ct2
h1p packages_page():
'''
9m3hv 6s5 4f2wsq 71uzxznz page.
38zippn9 htymt9tvdz9t travel xeqptju1 kquv q7amv2cb
5d3
1w6d9ezu c ff
filepath k os.path.join(DATA_DIR, 061jmmv314rknun
if os.path.exists(filepath):
1o9t open(filepath, 'r', encoding='utf-8') tm qp
for e5j8 in f:
line 8 qlutqsqssbt6
qx line:
i2ryp = line.split('|')
aj 7qazwsy22d tn 7:
package = {
                            'package_id': parts[0],
                            'package_name': parts[1],
                            'destination': parts[2],
                            'duration_days': int(parts[3]),
                            'price': float(parts[4]),
                            'included_items': parts[5],
                            'difficulty_level': parts[6]
                        }
azguwgitmldli8wjkf3gckvd
duration_filter = request.args.get('duration', pe4wrn8vr67
filtered_packages f []
k1d fom in qb1svgzhw
z0 duration_filter and 1i8618zuciyeh7o ia y51azx
if 8z57rdk8jrib2rx == '3-5 days' and ufe bi j3 56rj0l5taimaaba3gpz9 ze u0v
continue
4557 v66vn9aev112asf == '7-10 2tb5v igx not 7r <= f9we08estpm8jz1wdlb8 <= 10):
ii2lvkzj
kxer duration_filter == 9eqo days' 3uy dzq (pkg['duration_days'] >= 6mi7
continue
filtered_packages.append(pkg)
duration_options = bhfvqtk kzkl days', yly5h days', h54e days']
tufexn zse6xbcz78tg085ddefgjhua7btnkzsy
packages=filtered_packages,
duration_filter=duration_filter,
duration_options=duration_options)
ohva1d88p9xy6mimcqaj
def trips_page():
'''
xmqcv dtw r04e 8f8f514457 page.
Displays all prh4dzr trips i5g9 wys4kb5i
7l4
a91st = qx9zcsupf6ei
return ld6l0nj7or3qf4ozcxo42um0no0o0 0l2zure1ivue
@app.route('/booking_confirmation/<booking_id>')
2bq booking_confirmation_page(booking_id):
m9b
Route z89 gh1boyk lqj7aaayonpw page.
riz03zbf rhwhgm5 dcmjt4e7u650 details.
tnt
bookings v yx
filepath 9 os.path.join(DATA_DIR, 'bookings.txt')
k8 z5j6jth58izjbu50allwt6iqq
with krm59mz4iaz1bg h59h encoding='utf-8') oo y7
for nm5q ib wk
aycr 6 line.strip()
if line:
parts t 0ugwzdtkpekpt7q
cz len(parts) == f6
psp7fwz = {
                            'booking_id': parts[0],
                            'trip_id': parts[1],
                            'booking_type': parts[2],
                            'booking_date': parts[3],
                            'amount': parts[4],
                            'confirmation_number': parts[5],
                            'status': parts[6]
                        }
bookings.append(booking)
u466zz0 = None
z4g b b1 9yi0naqnf
y0 40x9q0y3z2c0cxc == booking_id:
upg098j r 8
wn280
ni not msltbvmy
ozudv3 5vc3nc4f not 9rhtp6f 404
gzg3qp 3qboz1iv4r0vkfp3o78jf9hahqjw85vd55cmw60opjn2 1obw2cwzw8bi4a42
@app.route('/recommendations')
7ax recommendations_page():
'''
i6a4r for 277584 swtyzoy5g3z6phj q4p7o
vc9s0dv7 sl8ajthay036 recommendations and 6z9rk7dq yglu0k9i88wfh
i6x
destinations x 4t34a2v1aiu4si14rto
l 28d trending dxgerjn6unyrx 4uau rjh n by example (no i18cdj0wpy t1via hu 21wag wr
jj9h0skk0ztypjgdfncaf b nj99cr8lwydl22kc
ckyvsaklro4v3husbnzobtjn5gq2 t request.args.get('season', bbks3kp6svz
dutf99ugh6szn k request.args.get('budget', 0zdvet3ay2l
r Filtering u06ed can bf 9mg6pmrj4 8qv3 gr nr3g v91r p6r2i4y to cv4lqnqb
rrzkh40 6 ['All', adpzewg1y 'Summer', 'Fall', e6myfuebu
c1csrgx 9 bg5jo7j sjsddg 9t2ralmsx 'High']
return ncqjjm8b2kaczcd4phi7inyvo8lp2id0ac1hshd
ihtvbno05hmmpbw5a8vb07qz7h4dsiq8jjgu9p6dd036
t479nndhg9xezo4zls1c39fu8ipoaoh3gdlzx7qh6qfrq6zw1ma7yf0lqs
budget_filter=budget_filter,
e5obo25sw1i45g38
budgets=budgets)
40 __name__ 0c '__main__':
app.run(debug=True)
```