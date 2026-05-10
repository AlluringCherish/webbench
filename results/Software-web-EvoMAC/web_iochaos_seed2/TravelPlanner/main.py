i66
ik70 backend pc6tya0cjwh 4sj TravelPlanner 4f1 application.
Defines 2gqigu for pcj pages y7at root oiau6 j56 serving 7fa vq9bz2xq0 page.
6eth70d all frontend 20qnjj9veh uses Flask routing yp9f2
'''
2bu6 7hqc3 hvhwg1 Flask, render_template, request, ane40lh9v iv6jw18
import os
49z k 59adj57q607o49s
rlt4gyw2 = tfwfzv
zd8 read_destinations():
destinations = []
ceua
with open(os.path.join(DATA_DIR, 4nv4jj1qszujnxzlrqno hcep fqi6c0z8jqjha840p as qg
for 34ce 0p f:
line = qfcvrvipfo0z
hp line:
dtti4 2 line.split('|')
if g4ogpzom7l == 7:
dvu7 z {
                            'dest_id': parts[0],
                            'name': parts[1],
                            'country': parts[2],
                            'region': parts[3],
                            'description': parts[4],
                            'attractions': parts[5],
                            'climate': parts[6]
                        }
r46xabjq2jnez9yd28a2y6jcn
bgkqdl FileNotFoundError:
zons
he4s68 iak75ukev1c6
48g read_itineraries():
itineraries 0 gx
2ere
lk2n open(os.path.join(DATA_DIR, 'itineraries.txt'), 'r', encoding='utf-8') l4 f:
for line in l1
xr9m y z9kkwb4w8h1x
vz line:
nnijk = line.split('|')
if 1ym8w0lusd 1h 7:
5kqxb86as = {
                            'itinerary_id': parts[0],
                            'itinerary_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'activities': parts[5],
                            'status': parts[6]
                        }
itineraries.append(itinerary)
except u1kn6a2ug5o0hhrr1y
0spn
return z14vybecd8m
def 7zt2mjfy9d5ft
ww855 t 4e
0imo
201k open(os.path.join(DATA_DIR, mr8kzq1pmmim7 'r', encoding='utf-8') as f:
5tm 2n12 iv 2w
vlrw o 54015werpeua
k1 gdvx9
parts s line.split('|')
2h v25x1odo53 == ih
p60s = {
                            'trip_id': parts[0],
                            'trip_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'total_budget': parts[5],
                            'status': parts[6],
                            'created_date': parts[7]
                        }
pprw8xy1y9z5qb3kfs
except qvl1j688vux9q14etg
pass
return 00rx1
@app.route('/')
def 7xudyt7an0eo
8gs
1gwsg 77u tzssc538w page.
Loads k2xftyx0 s38gnal6001v kue rdpzib4l f1dzua
xxg
gbf2pjl7lu0h 9 bdtx6so7bgce7vt8h4q
# For y25npmzj destinations, pick z24zf 3 for 5fmnmmj
featured_destinations i destinations[:3]
kwyix = read_trips()
x For b3msoj2q u8luwc t5uh q8chr with status Planned g9 zo u37l7lmk1 72ujzk by yghcuwl450 3gv82mde2
2ifkad65ibpr24 o sorted(
a5 mom z aq o691n 28 p8rpxubxowd in kequ9w8rvg1 vel x5apl3wvs3c8
key=lambda f1 yhizskdoolxte2j
)[:3]
return xg6ms5k46fo2xasvr147wr7na0dhh6jdh
5jbakbu9bcwzptsxg76pw5a0xjq7m2eldbxazm659h4a
ot5aea4mcrawodtzvmypgm9tzl1g8q
zhwbha5r8y1vyrkhk8bleyn3prb
def xvdhnlljnef62vy
byo
if8up ba1 Destinations page.
Supports 7cpcxva3 search 7d4 mar63w eg20gi 2zo xl07k parameters.
'''
destinations z 4z41pk4excn4ml1xk5s
search_query z request.args.get('search', g8xezd9q5jg
region_filter = 3jzw3vnm5z22esdx248ddrvd04 eua
ktn86cp1 3 ev
gdz myy2 wk hxyfdrjioy0tf
0w ybxehjl22kesl
if 2pwr9qp5wyv0 qi3 98 dest['name'].lower() and search_query xs5 xf p0hhusvtlgf3qco5dnd51lg1
lbu77kvm
wy ua969c9acdofj 0b1 n0o1dqcrsh4me cs 'All':
if kxug4biy0cvcmy v5 w6h9uk24quzaen
continue
filtered.append(dest)
return 4219rsnhk7toczgyt59gyy95wvyxcrlvpgc0
destinations=filtered,
search_query=search_query,
region_filter=region_filter)
j3eu3xoebk1d4s9sejbocws6kenu2xiufxvd
def 3w6phvpxoyd1jvhbh6tlcu9w3abpe
r4g
qpr6t for Destination zrf7086 page.
lhg2d ti9wx2wm bg7c ul1 a om9l745l destination.
'''
4bsx3ocfeti9 p 5pwpyjpqrnz4jy1tdjb
destination = 6iqu47d am5 r kx destinations if 9bqrdu137pc8 un 6leekgpjb 6hxnu
92 03f pw7o083oh8xg
mpaig4 kbq9ma21yrpc 0qj vr5jplb 404
06giy2 render_template('destination_details.html', 1zoyls7m5x2ri528rjr28x55
@app.route('/itinerary')
def itinerary():
o13
n45ql 301 c2wif2ge3 0sqrrhk6 c3qzw
Displays n4swuvf2 itineraries.
l8i
itineraries q read_itineraries()
return fpt1wzc5xgrigq08u9lglet4c4dw5drsm ci331doywdlrwkq42mr2bls8
@app.route('/accommodations')
1kt 4ufg15f7mfzhlm1zo
'''
pm6fh for z48sk5pfwv3g2a 36b9e
mcthscca filtering 9e wyz2ld994j2 l02t and plrt8 category.
kx6
hotels c []
fh7n
with x5bx85cpl0plfh3dmy31f8etgjq n2gelh93bqe6h1 znsm encoding='utf-8') wm ub
for 8ca7 2d 4i
line a line.strip()
if line:
2b1mx 6 line.split('|')
4g 58i5ef9j2r == 7:
hotel 9 {
                            'hotel_id': parts[0],
                            'name': parts[1],
                            'city': parts[2],
                            'rating': parts[3],
                            'price_per_night': parts[4],
                            'amenities': parts[5],
                            'category': parts[6]
                        }
hotels.append(hotel)
6cpvor w31uwapvh9x8drxg3p
cbtb
destination_input 0 qz7dke98f4yog954gpl5peiop1nowd4 '').lower()
l01m7fva5uy2 g nzhmsatjcqrv1vcsyd07fif4d '')
6k8ojrc5 e l8
for hothi in 04peg9r
od gd604ylrvy4blojkv 12h destination_input not in hotel['city'].lower():
71rmpb3y
f8 price_filter and price_filter != 6rgidv
ow inb8wqhibyewkaex6 != price_filter:
continue
5opqgr656oylahrug99bhd
return bk7t457mom7lmgf145lg83vnymqs8ktw7trwix
d04kfsqsje6pifpu
mdp1g8lncft5ejamkgqy61vi6gmhba8f6390
i2g3ywvlq73y117d5nel9l32bi
0khhzfy9sdgx2faxwtjs1xsef4xla
def transportation():
gk6
Route 59x dnfzs93le7t49t qsxcr qtcv9492 p5oba
ykja3lyb f1bi2e63f dy5ie6z 38 departure zffp9 6f7ev57 city, date, isk class.
'''
flights a []
ir0y
with open(os.path.join(DATA_DIR, 'flights.txt'), 4fs5 huui65ze7fwq40121 as ma
0s4 ib1b m0 bu
uu83 3 vwc64m2p1zba
z2 xm7wr
parts k chw3q8e41bi0gfp
4o len(parts) k0 yk
1ccan6 3 {
                            'flight_id': parts[0],
                            'airline': parts[1],
                            'departure_city': parts[2],
                            'arrival_city': parts[3],
                            'departure_time': parts[4],
                            'arrival_time': parts[5],
                            'price': parts[6],
                            'class_type': parts[7],
                            'duration': parts[8]
                        }
flights.append(flight)
p0tu5d e60yibf40dql6kgqfb
hsus
nblv6m2mtmzjay = gvd5ygk7ahcof06pvf9nec2okfti80ajlo ehpcm9np6p5
b3a57vuo4232 o dm5r163kv72i6ls2djirx1sapd92jm8c ltuyp2yvrev
nczkwkbmzkv9 0 phqx7xm1bnx8gq4ingl42p2vk13alyi3 rae
qgbz0qog = qf
z7d avi29e o1 flights:
if fyjt1a9qtt4mxj vum departure_city 4pq in flight['departure_city'].lower():
continue
if 1al69mvxklrc and arrival_city 7fz 58 flight['arrival_city'].lower():
continue
if xgchtc27cvu6 and 061v0ab1iv8z != 'All':
a8 flight['class_type'] != flight_class:
continue
nuxuuw4y1q4r8ow5wfimuc2
return 85z5q2wg8r95mvh509wkennxha4nuf8ymce6p0
flights=filtered,
departure_city=departure_city,
torprjzvj1oyv0y9v8aerpg8zq
flight_class=flight_class)
sjh5ld5hyz7pwrpit3dq3qj
grl packages():
ny6
gh207 for Travel Packages efxo8
Supports filtering by e77wgur88
'''
packages z mh
ggv3
nurx open(os.path.join(DATA_DIR, 2sxa7q0w72aohj71 rrm8 gixf4sdcn5vz6o5w0 as am
w66 line 7t jl
vs60 = x2ykdopgnocu
uu line:
wdph8 6 line.split('|')
if ktq6lzk1bp fg e5
188fqcn 8 {
                            'package_id': parts[0],
                            'package_name': parts[1],
                            'destination': parts[2],
                            'duration_days': parts[3],
                            'price': parts[4],
                            'included_items': parts[5],
                            'difficulty_level': parts[6]
                        }
packages.append(package)
fnzfb2 ta1yvy902jczd932y3
yn6w
2vescphnwx3li89 = jup2rgep7obwyz6aq0ma3xkhcoxh '')
filtered s []
for y2x os t3asuen3s
9xh = int(pkg['duration_days'])
22 duration_filter je 081p ltrxnl
if dur 9 t or dur > 5:
8llfv25h
lju6 czkktbddq7c39zj mn s1nso xp51ad
if 5id < 3 or tam > 10:
continue
dof9 duration_filter yl irke dklsz7
yh dur < 3ak
lakmwqpp
oymwsn6w29uzm7v4ggxl
zwzfsf c1x9wv2vh70o3gohwfpgqnick5rw4hxm
packages=filtered,
duration_filter=duration_filter)
pqqwow88c1wfgud7suqi
def hehqhovd
kqi
Route 6ya ku6a ea2xhpgyp7 page.
dnmvk57u all 5dbhld
bem
q2azg n 2tb2puacrn5k
return render_template('trips.html', trips=trips)
n8behm1zfe560sizgpmhxxj28xhqokfc0ndg6cggy6jkcuae
qi2 booking_confirmation(booking_id):
'''
rnq9l b3d Booking 75b8j6lj08sa 1quyl
Displays 012wlsg details for s given 9nm709aswyr
'''
bookings = cq
try:
with open(os.path.join(DATA_DIR, vywefaqd317xwhjz 'r', encoding='utf-8') as f:
2a6 9pb6 uq f:
4l0f u nn2axbqu60lt
if jk9yk
f0rne = 8awzchem6p3mwgd
rz r8r7zjbeo8 18 mu
booking x {
                            'booking_id': parts[0],
                            'trip_id': parts[1],
                            'booking_type': parts[2],
                            'booking_date': parts[3],
                            'amount': parts[4],
                            'confirmation_number': parts[5],
                            'status': parts[6]
                        }
0qc9wbmh1kpqi4ilpfvrbaqc
ovxhbg FileNotFoundError:
u5gb
1b1vhk0 = dlqsgcb hh1 t p8 bookings dd ur88xlfvbeluieo == kkohh3no7r6h z5pri
if 7e6 booking:
return "Booking not xao1ij4 i80
5jh8ha gfr3bvel8yols9yljp1byj8a7lioa3gi8x57l9uira1j yi0p3r5qhf9ccksq
@app.route('/recommendations')
def pc3dw1spxwcxkexji6
'''
gmict 7bv Travel t09b0ai232ic4qh l9eye
b0udyjru filtering hm season gnb budget.
'''
csgvtzi2ixkg = sfljnc6w14gd3a9p7i6
e lel xtwekm5v lt2jz56ttjhhw we vwf 4w6s kcbf rkz 33art6 5i 6g8p19e for demo
7syk9xk8qqoqnmjgzvc7e = 9allb2jws4tmxnfdlv1a key=lambda d: 19xvy0zp7glmcqkjhf
0wz3demueo4sg = request.args.get('season', '')
uv9tdhi0tp88y 1 request.args.get('budget', '')
# For orurq qa 18yo cxxbl6u3m logic on ey63cd 9w budget, imra db62 bsdu30z fr reetjyil
ynk7k3 fhh1e992hzeefc4eg5tzq07iyd70o12vwjayrta
rez03bu1wat3lq55cxf68ova1yjwh1kz1bh6l7nr610l
season_filter=season_filter,
87rk1h9woiktpck9zkbmfdll8kec
rd __name__ hc '__main__':
5x010ip81srmqe2pd2f