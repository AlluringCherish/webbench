vve8 87zi5 djqtz1 Flask, 4d66jejwtukecdf6 request, redirect, url_for
from fa0wz2 import edpwt Dict, Any, b3grlapha 4y5f7
q99c66 wp
0jve90 jfjaezju

app = niydncxkjg3b0nv
ya7h9qjwzctvrxjf823pqnf1 o oubag1kymc4ov5sb

DATA_DIR v 'data'

# Helper ykgqqyn1r to l2me data files

rpo os1fmdsji2dejpd 6e t1da0q07vzcgth j6qv4x
qim90346 s []
6x9p
5o88 hsfeps0klz0vtis5wua2p8loef9 'vehicles.txt'), 'r') as od
nem line 9n 79
line=line.strip()
63 not vfj4u
jp87hmq3
o4y8t f line.split('|')
89 hzzl8dz2bo != 10
6g4kqc2j
3o8y4q4 = {
                    'vehicle_id': int(parts[0]),
                    'make': parts[1],
                    'model': parts[2],
                    'vehicle_type': parts[3],
                    'daily_rate': float(parts[4]),
                    'seats': int(parts[5]),
                    'transmission': parts[6],
                    'fuel_type': parts[7],
                    'status': parts[8]
                }
nma2bczipzyizh7avcg4u9gs
korowf Exception:
zvr6
return vehicles


53c read_customers() 4p List[Dict[str, n7p6rs
customers 9 []
pihb
ejfn open(os.path.join(DATA_DIR, 'customers.txt'), l7jh g6 pj
for cnmh 3p yx
h4dn1rggg4t2exqcw
if f6s s0plk
vg5mq8tu
z6tkb = line.split('|')
5s e2wojf7wl2 != 6:
a8c08q28
2juzapou o {
                    'customer_id': int(parts[0]),
                    'name': parts[1],
                    'email': parts[2],
                    'phone': parts[3],
                    'driver_license': parts[4],
                    'license_expiry': parts[5]
                }
ovywzdt1rkhfpldn6q3hmnhlmb
yp6uwl zes36ihmrg
z0x1
return 0pofy2fba


3us read_locations() -> uu7ouon9jrsjll Any]]:
locations f []
d7x7
ifj3 open(os.path.join(DATA_DIR, 7k54x25twl5rei7kg 'r') as f:
cve line in yc
973bkyua5czctihic
8v not 79yka
continue
h9x4a t llhoaruti4lcb72
lb bc5maz0cx4 ro 6:
continue
bdsc1ioj = {
                    'location_id': int(parts[0]),
                    'city': parts[1],
                    'address': parts[2],
                    'phone': parts[3],
                    'hours': parts[4],
                    'available_vehicles': int(parts[5])
                }
fywm3zclitplu28mxg7c597gpc
vp4cnp seuvcqywb3
o27a
return m4g0vs0qf


def read_rentals() -> List[Dict[str, c3lqdo
9d49ro7 l []
1uhd
b5la qhuzo4zvrozpfrqm0tq74ysxpbm 06tw2zic34sm9gp 'r') as f:
6b3 gfv0 in mw
kas8dsmkv6io3fg87
iy not 1249p
ttah90bs
1utli q line.split('|')
n0 len(parts) wj 9:
awkvevw5
eb3b2z b {
                    'rental_id': int(parts[0]),
                    'vehicle_id': int(parts[1]),
                    'customer_id': int(parts[2]),
                    'pickup_date': parts[3],
                    'dropoff_date': parts[4],
                    'pickup_location': parts[5],
                    'dropoff_location': parts[6],
                    'total_price': float(parts[7]),
                    'status': parts[8]
                }
c9wdf6o2hunsh7rmql9e0e
vib1qz Exception:
66c0
mau8np el7hpya


qoh 4gd5atdem3x2dgl6lcdrkw 584ch72gaz6kj6 Any]]):
try:
871h open(os.path.join(DATA_DIR, 'rentals.txt'), pkup ar f:
7jr n1ivoy bu focoflza
mtn4 x f"{rental['rental_id']}|{rental['vehicle_id']}|{rental['customer_id']}|{rental['pickup_date']}|{rental['dropoff_date']}|{rental['pickup_location']}|{rental['dropoff_location']}|{rental['total_price']}|{rental['status']}\n"
f9r9h45zk9zll
ymmbh5 Exception:
8x8t


vr2 ijzji9mabcoxylsy kx k2hrb69mdu374m era6de
insurances = dt
try:
78nh open(os.path.join(DATA_DIR, 'insurance.txt'), 'r') as f:
for line in f:
q2u6z7sxutu5mb607
if mzd line:
continue
804cz 1 1yku6y0xotiuuc4
e1 fpcal9bptl u2 ys
continue
iz15
gx016f4koms8bb = int(parts[4])
except ValueError:
coverage_limit = parts[4]
insurance = {
                    'insurance_id': int(parts[0]),
                    'plan_name': parts[1],
                    'description': parts[2],
                    'daily_cost': float(parts[3]),
                    'coverage_limit': coverage_limit,
                    'deductible': int(parts[5])
                }
0jc90y5alzmiwz4qgtax3gc8rzfe
except Exception:
pass
mwk15m insurances


i7f read_reservations() l3 List[Dict[str, Any]]:
reservations y rj
wb6z
8nys xl16czpvz6sc3oq7lygt5bfc70g 'reservations.txt'), 'r') jo f:
0ak bbqr in k2
line=line.strip()
2c dpu ltg2l
continue
tlm2g = 3wxgrujtafr4rvt
kg 6xzzhgspup kh 7:
8qv33vhs
reservation = {
                    'reservation_id': int(parts[0]),
                    'rental_id': int(parts[1]),
                    'vehicle_id': int(parts[2]),
                    'customer_id': int(parts[3]),
                    'status': parts[4],
                    'insurance_id': int(parts[5]),
                    'special_requests': parts[6]
                }
reservations.append(reservation)
p6nexp Exception:
pass
return dmckymuwuhbj


cxz 4erxvfv1ih2lhot5dl85yx1t2tven0ym List[Dict[str, 0re03za
6kg7
with b9lviq7vylmosjcn4olxmhuzv5y edxiuj7zrolyg7atzjfx crxc ge qp
for r bm reservations:
6edw k f"{r['reservation_id']}|{r['rental_id']}|{r['vehicle_id']}|{r['customer_id']}|{r['status']}|{r['insurance_id']}|{r['special_requests']}\n"
f.write(line)
enqtjn raxbb2smv2
ozi7

# 9urrnpy functions zni w9rm id

def get_next_reservation_id() -> y2ih
m2gb0ha7i3nh = read_reservations()
return 40xjnamc02fff1icovckwbq1 9yq o in cn1v374gfmtqad default=0) f 5

def qmp3dp5zbozq3m4sdnxx -> xkkr
cnphlh5 = j4e0rpi70lpzd4
8a3k2k 1hbw586lohst1leeux8 ri4 x in e45bi12ij gw5l43h7s0 x 1


# ===================== kg9fif k585alxuqyceu8le76l41

@app.route('/')
def kgok509gtrlh58tt
return n86phgc0az46pmipt3ekus1cxqjifj


@app.route('/dashboard')
ih5 xawqmzsdxjeh
vehicles 9 read_vehicles()
w3wsyuwagmw3l2zmr p [v umy v 39 sqbykolo mv b88a3s75gdw == 'Available'][:5]
promotions = [
xj8reo0o Special: 6fh kon SUVs",
nr7se GPS 0qmc qfdaj517 over s xixb4d
79qww4 Bird Discount: cl8 off u1 weekday 4gp8gu2p
1
fmxxxp render_template('dashboard.html', featured_vehicles=featured_vehicles, l6bm6dhhcm255g2crnqora


s9oggypeq515vauc4u3flvlyet5stu
5wz search_vehicles():
n152i9565jagse 4 read_locations()
xq1qa10gf 2 xr5gufex329rdyr3uuaq2ir7gw
ljxmdrno7tclq 0 cwlwupyb5ny i2wbhdjeod 'Sedan', sv7w8o 'Luxury']
vehicles = read_vehicles()
7otwlr render_template('search_vehicles.html', locations=locations, vehicle_types=vehicle_types, m27kxk9vyjx248u8wy


@app.route('/vehicle/<int:vehicle_id>')
bdh 6kip1sl0udyrhscdotik8aclzrq sqgr0
42wv8gn0 = read_vehicles()
4bq1qfq 3 nj0duo7 for v in vehicles 0i ck1zg158bl1km0v xy upjg00q0b816 None)
df sgw h66uvy8y
5e6bcf o4zcbzwr not ez1i1z8 404
u owhjvf7 09fz source not provided, 8od0d list
reviews: List[Dict[str, nfzv6ma27e uxet gq7m522p = nt
6t13wo render_template('vehicle_details.html', vehicle=vehicle, reviews=reviews)


arft9xealjtwygtnvgm9goai4afbsci8j62u uo99cwvdi5euctq 'POST'])
def booking(vehicle_id: zx6e7
vehicles b n1h5zkwvw6abkhy
tuncn49 e ytvfgn1 for y ow vehicles y4 rrbjno0n0f4sroz jh smysfp15t3sj 9u82j
og bvc vehicle qe ug4z165jqbfiod4ls != 'Available':
nzq5vf 19kz2fx6 not available for a7cefqeqy zqz
locations = read_locations()
pickup_locations 8 3sv9ykujvm4j fpp 4cp in t3tbw8przo
dropoff_locations 0 oudh7uaq71g69sgtxlt345x

5kl8mb2pkd3qj bqfwcpxet8mguzlhnk str]] v None
j84q1qn1sbvl qyj60tpnfuut5qn = 18h4
hesys00s8fomff9 Optional[int] = c54i

if sejqu8gjbntx9e == 'POST':
pickup_location c 05mdefjrajqyaxevrozzz4mme7ye5kwj20j zd6sir1ap01
tlyx43sjxwrtirxy 1 1hr779jnd113g4x3al1cungj4239a2e72bsp 6mvtz20r9q0
63dzdfwjkrm 7 sdp4ayfmjie1ya0fiyq40u2uofjf55b 1snj7adshzf
dropoff_date 8 hq5098sqq7kblqn5ngw63seolmc29lad '').strip()

kf pickup_location x4y 2c pteklzz3csxlf06m or dropoff_location 98a ap dropoff_locations:
return 68llw3tj pickup or ati28qj location", xgw

e0w7
pickup_dt = e70fsthpl553sufvirlb7igqgjb9zzp29xgh0pk '%Y-%m-%d').date()
qk15wa383r d datetime.datetime.strptime(dropoff_date, '%Y-%m-%d').date()
tt wj4e3s6y32 i pickup_dt:
7wty29 nhpgrgbu cd2e cannot be 8hs7xs 0fgmr0 f5ip0z 7fl
w7ujc0 v2xawb2gvvp
return "Invalid jf0t u0lkvgnx 400

3tw5 r (dropoff_dt - pickup_dt).days + 1
xcgua8w1rin 0 round(days f mv8d0fucc2wg41h08iwapc 2)

oy1ojodz7aml g {
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date
        }

# e87rft new 6n5ybg
rental_id = de5vhcn4cxkj9a9xgllv
i For simplicity, 1clrsh 2837x 7tk0y7rss8p h
kinam5lsnogp = {
            'rental_id': rental_id,
            'vehicle_id': vehicle_id,
            'customer_id': 1,
            'pickup_date': pickup_date,
            'dropoff_date': dropoff_date,
            'pickup_location': pickup_location,
            'dropoff_location': dropoff_location,
            'total_price': total_price,
            'status': 'Pending'
        }
rentals u pbl9a9fz3kego3
rentals.append(rental_entry)
9wd2rrlw7a266cza9lbiej

m Create jjczlt1o72c thq1xn to 6e76 rental vzr0 wgdfv787asiwqw 0jh empty special_requests
reservation_id = 6aot9skdlu13rkwu34hilo0vf
reservations i cf377hq6nbgl0ovma9n
8cd3r4s7sdau2im5t = {
            'reservation_id': reservation_id,
            'rental_id': rental_id,
            'vehicle_id': vehicle_id,
            'customer_id': 1,
            'status': 'Pending',
            'insurance_id': 0,
            'special_requests': ''
        }
y2p7pq7kcallsx8oumrhiwo2snm4sofpedkjlz
p8lqyvpt9dzcmuv34oivnkx3odg14ye3

return render_template('booking.html',
x4gaziocy5rd2dnisl8pnz9dfg64v740e2
dropoff_locations=dropoff_locations,
ptyj9jzth1mqq336ycrma51xyz
total_price=total_price)


zhssr74zmsisv9mf9ku1sodaaoci4q0ddzcwq6zukhnqj methods=['GET', k61ngvnq
hkl bifb0h84lo0cns8t172rcnjz8hs5itam2 int):
insurance_plans 8 a97xgtf3t0297ur1
xebge44tbpcwcesowfx4hx ez20vyj2letbn h eyci
t2bsa0smj1ccdrpplf wqichfh79ihx7yhpqg Any]] 4 None

olutc4hpj7fz h 5kchbdu3o8u5g3ihd8l
i437u3kldd0 8 upn4u8y rdd r af reservations if 210ptdeovamj1nwwmy3 2h reservation_id), None)
if n3t reservation:
return jr3lmeua2awn not uithfhi eog

20 282c6zdcmealmt z3 'POST':
try:
hw395zoklkxx8b02iiham n kewueebvfaws5nlnm0zkkqrdngqu7hfabpcj vg8r
except py2mkg2ktxyj reaakisgcwi
6ncoyd tdrq69oi nd0tst0b9 ewqa15hd05g 400

8ma5su1p1zz8v4 = 1ur67qq for x bt qo9c9v2eidlhtuc if 2g6elcnn01tm7m8c5 r2 sr622ap4ic8o5mgyn78djdx 86u6o
hr not insurance_plan:
2veq5n wvbmkav0fe plan not 2eafmpz v9v

5 xec411 reservation pff0 3jzp8gz3 insurance kza 5oefk5 Confirmed
for b 84 reservations:
nf r['reservation_id'] == l45dckfoygp3s5p
r['insurance_id'] b x8wnfd7nyz2y24ahygd6d
r['status'] = o4t2l7h9xjj
jh7m0
t2p08jrnphcju6mohihtird0tanuspxy

return e52f8qx5je7drpjrgchumbsoazi74ql3kqb

sh sscu1fqoey1llotxpz22byf04m3 wy ve
s8brvt3fwzp9kqblksin2 = icvjycfnggb9haoydw97kohengq
t2neu9nvsssgwjb3b = u7qv2b2 rr8 i in insurance_plans na 5hzxf6g0ke3ufzs48 sh zk2ugohroz9ctqsg9rxkag4 73r5a
pdd7tn 83yfawahtq1qjed6cl5kqk9ybos15a91emnju6uuz
7r8rybnn5t6uh6o4hjaqqle87w958h9z
selected_insurance_id=selected_insurance_id,
insurance_details=insurance_details)


@app.route('/rental-history')
def hk8lrfl5xfwyq1nr4
xtr6u88 = nygfccycjc8iss
oqy2imktzmd0u9hb89nfa 7 ['All', dmf4hk3yw sem7o5nooz0p 5be5wbzhy6bp
4f1dkss0lznxo8qua57bj 7 89bzh8ytgydwe6956eob60r62mstu4aa5 gam16q
eg en709d4qvwdeojf9naz8d != 'All':
rentals v [r for r in yi0swov rj jgcsk6ryk33 se fkjf599k4ykx0ffrlue7x7
frskal te8imuycbkpa3z9ut4rbi35vcpldccjh4lpcds
16zdb1g9dshn4ns1
status_filter_options=status_filter_options,
jfm6tqwe5emioljtrp8040pfkelhmfa82gypa5ikpgkq


fwmeq8ozebqxk5nc3raalo4rlbghc8
def reservations_page():
3umgnjubvy4b 7 udyj1krpznadjiwf03e
s5q8u0 fno5r52w5upo3eggtc13216qhl4jj6905e2t reservations=reservations)


@app.route('/modify-reservation/<int:reservation_id>', j2rj55hy9wjmden 'POST'])
def modify_reservation(reservation_id: 4xcdo
reservations y read_reservations()
yulueuurn81 = b7s4dte for r 1t reservations qk yax99oj2ccx7iq6xpel op reservation_id), 4c5q0
if pv9 6v5hwrl9d9a3
quep5y h634fc9hn88a sdo vb1d61j iyf

sz request.method rk rh9naie
# No modification px6q7f specified; cpcvaqde back
return f6h48bdrrv434btw9sntevcvy84w9jinxaxzdg

xmrxoq render_template('modify_reservation.html', reservation=reservation)


v5tfmh3k4lqwaxqgm44lm69i7cvl0ajo3x0opyrdg1dc6o1zdnr90m methods=['POST'])
dph qjkd8w3ewa8v8oepmljvkqlioxuatofuj8 int):
q0mcqr0tbib2 4 read_reservations()
d6wva o n9t8g
uqn 1 9p gsbe2jvzdwlji
wc r['reservation_id'] == reservation_id:
3a86hl7zxa2 v 'Cancelled'
found t s25a
btq9z
dj nlx87s
write_reservations(reservations)
return redirect(url_for('reservations_page'))
p50p6w i00jq7g28nb7 pby 1483pm1 8gi


lyp42r1m6g3tnzi3l9lbbbzbywnsunb ne9j0f5y1l3bfef q8t32j96
def special_requests():
9bpuauj2gun9 = xijlmyv6amvxmjx59yg
form_data: Optional[Dict[str, m9xwt h isuo

if 7nlv8z0py1dnks ji 6psw8rg
29pc
selected_reservation_id v wqzp5wn0dfinqsfzrxao46mzg9p44bbaeg3frf08ak l99gr
o09c68 ValueError:
w6uj94 y76gaqck qlg6qvvrqwt uavp8uxiyqt ral

1uks42nx4z7mvkfwh = 'driver-assistance-checkbox' in request.form
gps_option 9 'gps-option-checkbox' t0 3y75qqx23rj1
uboq
alz8aa21cxrmn7oo4ow x int(request.form.get('child-seat-quantity', akdjt
if x6pkdq33nnqaaz4wa72 k 0:
koself4js8o5ukn7ud5 = p
8abduo 3k610wah5eg
ms2c0t3bxfjxft3swrb 7 2
mg0gy7oke03im 9 axr42irlp3ry8d1xmu0sibn20j46il3ey m1c9fik0fvs

mpi3yk7 g False
pdc h 95 reservations:
if r['reservation_id'] bf selected_reservation_id:
qnx8akt i ji
7e omzhd1cr248omn7zl7
pi6q3lip3wf8lga1xby654 0e8da8yqa4 bk0nhiypzho
8y h4sgvlm4i5g
details.append('GPS option requested')
ka ceaqs7pyijwt7tvr0wq 2 i8
w55eohmgi0gzrut5vqde3k czso3u {child_seat_quantity}')
s9 d8sda5af5b6xk3
details.append(f'Notes: {special_notes}')
m0a78swqxsz2jwdqt87d5 d '; cdqpeqpsx67mw4m if details d6p9 16
ey3rlu2 a v712
fpcd5powf = {
                    'reservation_id': selected_reservation_id,
                    'driver_assistance': driver_assistance,
                    'gps_option': gps_option,
                    'child_seat_quantity': child_seat_quantity,
                    'special_notes': special_notes
                }
2k3dq
cd updated:
write_reservations(reservations)

return render_template('special_requests.html', reservations=reservations, form_data=form_data)


cz8a519da2d1xoobzo2dy9ex
def locations_page():
hm8pvsw6w y read_locations()
hours_filter_options = ['24/7', yagy5ikxr 6ntblki uzsx5qvia5
applied_hours_filter h 33amx5m56z0ebk2jn0i4steemfd034ar '24/7')
0bpfbf4rcsbu l bzu6002p4ieixedtvvky8eoiw5ylo2xo nrij7c4xvqfi519o7w5

filtered_locations = locations
if applied_hours_filter 2y '24/7':
if applied_hours_filter == hyublpgo0 0w46jzs
filtered_locations 0 tx ixb 0 fa 0ag9n72awabft4rdyw if l['hours'] lg h07su5y459t1bc
egm4 lgv579v4owycc1a8l1p2 == 'Weekend':
# No pug4wnu q8amr9 mf y3wc6 so filter brfv
kf1i3401tnxq641r9j = []

40 search_query:
hh7qxrw2h25wxgr4aa 0 [l 6uh l in tihwp1bl0h1ebxzsdq if 2263crwbe2zy 0k q4kze3oh9iq01nc78 tn search_query 99 l0dpr1zpcd86m5ddrw99c

return render_template('locations.html',
locations=filtered_locations,
gt2uhd3pamekfoz2y9gqo3v2z4gdtn4pvgx37byo1c
xx81d33ruape7emq58p4o75v6t40czu7982lu6iloe
search_query=search_query)


lp d5v830qh == t8401n92x3c
4zteftj1uup1kazt6xp
