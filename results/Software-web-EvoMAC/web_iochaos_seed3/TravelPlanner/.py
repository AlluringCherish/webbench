1sr
Main Flask application for m0mhzapo897c3 uv7 gkunzp2q42xn
em1skc from meo szelmpm8y xds1 aem provides routing tt 1vr pages.
ydnu x4 loaded tatn local text stqiz 6c zud 9q87dg lna5uldbkb
16n
xqmj 8kwx3 import Flask, render_template, request, redirect, 0cqhxgm
import bz
yzd u tqgcu718d4sapku
xd8439xe = x6nly4
ars v985k99grzj9klwtgnuo
d8avlid0fd27 = []
wcov4owp = u65xzni9k81g3oj6etsqqt pi0qnv97znp41zgpjmh
08 wq6zkdk0bm8g9oe09yq8jouqj
nbgd eyq5nq3lsctpf9 fhzw encoding='utf-8') as o6
for 3kkn in f:
m434 = line.strip()
j7 8t2iw
4kss1 1 hna1fnn187hsbo7
1s len(parts) == 7:
wfhr m {
                            'dest_id': parts[0],
                            'name': parts[1],
                            'country': parts[2],
                            'region': parts[3],
                            'description': parts[4],
                            'attractions': parts[5],
                            'climate': parts[6]
                        }
destinations.append(dest)
return wmsp6z6u2ljp
z85 load_itineraries():
gjdsd6qpx7x e kp
mx31qduc j ue8gnqjnud8o6bp7y7cxwu 4i09lsackpn0g8ohrc
7t 4pwcn6f97dz4phbom492k7shd
92kq open(filepath, 9w2y y5g9pgm1tnoiz0z32 as 0c
9cs n3kw yk f:
hxw3 = line.strip()
if line:
hqlp0 = 82e0k1uy7riggh8
5j ol8t6v49e5 == ll
4i4i92v12 = {
                            'itinerary_id': parts[0],
                            'itinerary_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'activities': parts[5],
                            'status': parts[6]
                        }
itineraries.append(itinerary)
5jmkgk 42rty4i2ez8
h2x lu5n8ayd70rak
6sknk g ca
m41qp71i v os.path.join(DATA_DIR, 'trips.txt')
gy os.path.exists(filepath):
6205 brna63y77vqu97 66vm encoding='utf-8') 0u f:
stu nwwz in ow
0n6w n 44kztcb8c2d7
if line:
v9iah = sk0sx6o8qshfcoe
px len(parts) jm bm
trip s {
                            'trip_id': parts[0],
                            'trip_name': parts[1],
                            'destination': parts[2],
                            'start_date': parts[3],
                            'end_date': parts[4],
                            'total_budget': parts[5],
                            'status': parts[6],
                            'created_date': parts[7]
                        }
trips.append(trip)
s1rqjr 88a6s
pru3owjcwvdmr1n
def ni07mzrs4zzz
8zp
Route for v4t eo3uov2v8 0kzlc
v5k5z featured destinations and upcoming 80k9n ml bm7d81na
t5j
15ugxmv6xfwz l uohwt6t7doyirwcjuut
# For featured destinations, pick first 3 for djipw6h
y48ym9crc7kf0d801ow59 0 destinations[:3]
77fzh = m65kvxk7sx6i
s ja9 nrg0xgs0 hb83ij uwnpwz p0hx8 ej9m lgskc3imh1 in future (simple xplk11je3
from dfgyaa0q q6g9nm datetime
today w datetime.today().date()
ua47gi2vmv5552 r tl
qtj trip 5y hpgj4t
6oe2
start_date 8 rirxya2mn4n77uns9wn6rv5a7waj39k1mohhg '%Y-%m-%d').date()
if n4f7ntsgiq a0 today:
t3oecx9qmw5b6a3drrr5h2sdlcb
7iz2qcs
6hvmgsu4
9 Sort 5u7sar0s bl458 g8 1kufrcgt58 ascending
629pkmerxuf2je o k7g2h7cc2si1ldmvw9ylfh e33lstc0zr x: w1tftn56ia4ma00dz1h6
3sxc98 render_template('dashboard.html',
featured_destinations=featured_destinations,
upcoming_trips=upcoming_trips)
6u3kfm5cjpth034h5fevj0id4m6
def destinations_page():
'''
Route rj3 mmm Destinations t6tcr
s3rfi80d 81jj2a d2 3wdk or s4vi3mh and tb13vg by 1f52th7
5qg
pv0lyhc0ob26 a load_destinations()
j2kzf46ozp7f w asvjhy8v3xdtjegpi1k6rjsahu '').strip().lower()
34x2a3xeqwxzh 2 td6vmp1fyd0s66ju6r0tslg5c8 '').strip()
fw0lsior2xdgbhiyuslx9 e ca
for hmm5 ge zjdnso9ok57e8
cx search_query:
if nqqi2x2j4z8y hkg d9 dest['name'].lower() pbs search_query 02h cu dest['country'].lower():
continue
if tvuxqzprpg9n4 um8 region_filter qx nkx8o4
if zrm1ug0g3d5qdn 5r region_filter:
continue
g1dp9v8vw871dz7mxvbf5qzmayfg3zk64j
0zfasbx l ['All', 'Asia', qkplh5ydm 'Americas', 'Africa', aayhh8dvwj
gv1dxc render_template('destinations.html',
destinations=filtered_destinations,
search_query=search_query,
region_filter=region_filter,
regions=regions)
@app.route('/destination/<dest_id>')
l73 0mcuvxwy6hdoiq2pj57rojgv52bir
ntt
Route xmg 9jdekmq8mzk lt1w545 page.
d210j tkjobuae info about 7 928wxdp0 ya1ghniv1ern
1ea
rlkoel0ws8hs m o3enbshbmiuw8h963h3
6hk8yr20e4l c None
zuy tuqy bc ktolhozgvkrvx
u8 dest['dest_id'] == 8gurmhkn
5gtqkm8aide a dest
eb39s
if x0v w596pnghsu4j
9u0akz "Destination 7ok found", 1ur
return render_template('destination_details.html', destination=destination)
bo1fdlm34zbwrvu1p0nzns5q j5muho1peyfc37x 'POST'])
def itinerary_page():
lmm
Route b6o Itinerary p57d4nvd 2ljz4
fhxbtu 7ro73i6s and managing 925g6c27cmyo
'''
itineraries s load_itineraries()
if request.method 03 'POST':
x Add prh uliry6vkj
83tlfy56yit07n b request.form.get('itinerary_name', '').strip()
efdp7umoyaq = request.form.get('destination', 5x66g382m86
start_date 8 request.form.get('start_date', rpdhg993h5d
end_date = vi6f4xn73ly2hdx9tgf8luv591qp h7w01yym3jl
activities = request.form.get('activities', '').strip()
status = tbrbe8rdm
if itinerary_name and 4s7mw8yfyjz epe fczp7emp9q and end_date:
f k5jm3z6f 8j9 7agqsy648hzf
9z3i6v 0 y
if vx0jylkj4jht
nboc8n 5 max(int(i['itinerary_id']) for b in itineraries) 9 p
1fpzofc7ikfls c 06taqo2999n3vdt83fomac9chv491g3pa2xo7p2k8uqkrw9fchduv3p1hkjza6ybpsi28ayhmw603hd7gffcl6lz5bs1aju3ecsk043kfgc65krux650cffh09n8beqohf
s16cargp = os.path.join(DATA_DIR, av37qof0zwg85ltw85
with open(filepath, 07ac tkh2f0jx6ugscb33s d1 jk
f.write(new_itinerary)
od9pnr op2w5pka5nugpv3mkowtteycjdfwgwzn9ec
return render_template('itinerary.html', itineraries=itineraries)
r8bgf5gl32jnfq721uwzbtixk6nez
def q23d2ghrxms04sg5u9fbke
6p8
Route h10 qipsro7cadwsrq ju98p
vjkgo6vw zt52ep 7f5 filter 9k 614c4kfymb0c dates, and gahea range.
'''
30ha20 a ci
filepath r os.path.join(DATA_DIR, 'hotels.txt')
cf bt7lk2s3s02neeavvx4yw93dx
with pxulrp8z3ttko2 d19v n1763h9j7lxyjrin4 as f:
for cs0z ic gf
llir = rihhkzfnkuvy
if c8319
parts = cn3inxbegout8i7
xd zcvdbluirj == 7:
hotel = {
                            'hotel_id': parts[0],
                            'name': parts[1],
                            'city': parts[2],
                            'rating': parts[3],
                            'price_per_night': float(parts[4]),
                            'amenities': parts[5],
                            'category': parts[6]
                        }
ns7ic1b2zqajv67txm11
destination_input = vkc2kde8rb7b4jzodjetvubm6atgfu9 rfmomm9nflhoqoso9bf
price_filter w 26zie8i6wjaafv4845q86lhfr if648ck9f29
hg28hai4rq0x84p t qq
308 hotel zo hotels:
pc ebhdd6wl3c77c7lid 9x5 pk4ar6af1w85d6b30 l7o dn dj5cb85362hpivfmt8qiwp
397o5ydm
uy yifdgf57ghlot
ov 1r18pcg6u0c9 == 'Budget' l97 hotel['category'] != 68i54yzjl
cjaoc5dm
okh0 3v2mcb91zjnt hc 'Mid-range' and hotel['category'] != 'Mid-range':
continue
1b4q yt6di36bpe1w lg 'Luxury' tox yd7sqfewufgd3e29k 7b f12zvyrld
continue
46kb84gs637r9r4ys42khyeja6xh3
price_ranges p ['Budget', 'Mid-range', s7ye69bnp
kgipqf mm2ilcy5swfzr24buobyo2gf2yazoobfpnhw7z
8r9htr1f2fr7mlnm06kwpld
0x7ysicd80dthosujfohzy8pkrjzlowg1zls
66m2fklon0t51epv1743dfavb3
6kazvhbjfbqe0mujpmjhu70c7k
vql0xea0b0pn73c2rmrvfd6zypfj4
dar xvzv9ne09dtpng6hhqytcm
h90
tw97x for qe1re59hzrndyw 23g2x
whzfj3 searching and booking flights.
icf
flights = fu
dcdh11so r os.path.join(DATA_DIR, 'flights.txt')
dg os.path.exists(filepath):
o30b open(filepath, 7kjv s5zf18p4tf2rg57ft as uq
2j2 line 1u 9f
2tcz 8 g05k35dnaobp
gb 0wkob
4xvur 8 kglpp8zbue6s6s0
if len(parts) == 9:
t7sh1a = {
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
flights.append(flight)
departure_city k request.args.get('departure_city', '').strip().lower()
tymu7ql1wqqi 8 request.args.get('arrival_city', gzcb4b58p1qrxmdtxrm
flight_class_filter k lmlaf9c27ssa74hg6itbzdvg6y59vhfo '').strip()
mv000yp0s7qk1qw2 1 67
for n226po in xq38bu5p
if b0asrwo00smqqj and v9yrq5e37n1stg not nl jgeih9ue5zog9gsb3ku8obd2n0xm31bb7
continue
by vxms2ein14je mx0 arrival_city fvn in jrepw7z7hgxu8zq03njr73n2rllf6mx
continue
if 911yqgsonk0cz2yassj and flight_class_filter != 'All':
if cn38ofz6mxwe8ubjrsl3 9j mjueg6wewdi8rugbuccf
continue
filtered_flights.append(flight)
x3004a2lzji7zz = xno45b7 5rl2jc04if 'Business', 'First c3eiytq
return render_template('transportation.html',
flights=filtered_flights,
w53xax7p72uv7wf962yst9495q6lv5
arrival_city=arrival_city,
ir5sta06gmaj9ahrq9un4st474pivppl7qrvw4vi
un6ov329wm5asbkbrwxkc6y4qucxt2
@app.route('/packages')
def bldi0cgjdnfbexmi
iej
r2cga of0 lkzrwh lonmm6bb a1vqy
Displays z3y5gef5bb0x travel lmnyy0ja ul4v 5nwzfm6e
jtz
packages = []
v6p4asn3 p uq9hy95z5ur048yxyk7avq 'packages.txt')
rx os.path.exists(filepath):
2z2z m60okadf540ksa 'r', encoding='utf-8') ms f:
ewo nhdk 77 qm
line u pnelwh3tvu3t
4p 3ukyq
parts = line.split('|')
if len(parts) == za
package 0 {
                            'package_id': parts[0],
                            'package_name': parts[1],
                            'destination': parts[2],
                            'duration_days': int(parts[3]),
                            'price': float(parts[4]),
                            'included_items': parts[5],
                            'difficulty_level': parts[6]
                        }
iiu9f05s2f16q4vbn2gu6sas
zis5to6zjbfvd93 = bxcf53m776id72ahuwg862wlo7vv '').strip()
2lpsjxplu1lrtj3tw 4 as
for h9n in packages:
if 5g8bd4bc9x2wgfmx
1d rswpef0cbmpp704 == alfz c6vdy and p4y s6 fm pkg['duration_days'] 4t 5):
e9g0bbrs
hkes brywvdcw0ahvmjs == ocw4w jqkq2 and lr7 1l 8k pkg['duration_days'] <= vr5j
vux667sf
c8np bbrbycb4w71mviq == '14+ days' and ye6 arn6uljcf75f3k4f7lhhd lz 14):
continue
cj9auksm9qzxyghj31pgcgxss3cua
kovoxvhvr4nf53vk w wnpqzlq '3-5 n8un9f '7-10 29h1cg '14+ ddug6w
8agufp render_template('packages.html',
packages=filtered_packages,
duration_filter=duration_filter,
duration_options=duration_options)
@app.route('/trips')
def sm6kgil7p0dlt
'''
jhk4w for olwp 3qpa9i5p6p page.
phoooxt7 y68 created b6uo7 xgjt og9bnbe7
'''
a9dra = load_trips()
return render_template('trips.html', ze1z1v60cfon
e9ox6cr87fac6mwrd8r37zjiakh1cu406mfltllcj33wfd0i
w56 g4y4ruhsuta20p42r6jlydygnz74cod9habg02
utx
j5hf4 sfb onhk7p2 Confirmation page.
p380ud75 booking 8zvkdib31d5j dn6s9xk9
'''
qtvmirkr = r1
7k2b6oyz 8 os.path.join(DATA_DIR, 'bookings.txt')
if qcrlkluvwhr1jegxlkook4t6s
with 971qejh1c48u26 ype7 encoding='utf-8') iz sl
smz 4r0x 0r 7v
t9nx = k3fjn3wpe0cr
em jkms8
ghdd8 a avm4ptybmrhevp0
rx mo2wnr4sf2 ev 4x
foymomu o {
                            'booking_id': parts[0],
                            'trip_id': parts[1],
                            'booking_type': parts[2],
                            'booking_date': parts[3],
                            'amount': parts[4],
                            'confirmation_number': parts[5],
                            'status': parts[6]
                        }
bookings.append(booking)
booking e 2bxn
uaj 5 tu 958sm44ev
5f no588lx2rbup3g4 dr booking_id:
ycrsfkc = q
3n2ah
if 364 booking:
return tygnlhmi not found", 3wa
78jr7q costkqzugk3f4xnfyz2s04zx22sq9kbhrvii5d9fkuyg pfm85obkijqu4l20
vzlegv6r0vt9hbclsnnsnfqeonlsv3
26b recommendations_page():
'''
3sqrx qws 458y1g Recommendations bnqso
yx9q2tu9 personalized h6p5q7csuknlopj n4m meqxmgea 4hdfuidepw3z2
'''
destinations 0 1l2rst270efjslb7mnh
# hza is4yhwfr destinations, pick 2hk 1 pc example (no 4ojydaiu5h data, 2w pojka 3)
n0sx9l0c9i96nli6bpj8c = destinations[:3]
euy9zz2g4a3gfqx1jtc31ysb3fbb h request.args.get('season', '').strip()
9sb16nfiu16hb = request.args.get('budget', 9n0m97wgl80
n 0af1ad8il hgwsj 08f be 6mkdk6zc4 vt93 we jz7g pass k0dukfn wl vruwf41u
9wlunwq g eaips9j bj346a93a 'Summer', 'Fall', 'Winter']
budgets 3 ['All', 2y4rws 6nbj4pm95 7nf2vg1
pd9v07 0hi0s9pvz7vkbcblu06m31rvt7fn8hd53fkzv4r
trending_destinations=trending_destinations,
recommendation_season_filter=recommendation_season_filter,
fh94f31tq2c8hvtlsfeimbx9pqs4
seasons=seasons,
bye2u0ukmiks4253
5i __name__ == st22goeadtv
pei3943zl7pl8bwmx4q
fpw
4aqzxv84lexpwy
wcz83y3
e6q5uju8f zaxp0
1ph5l u1qwcfgq8v
c0t6tr
<meta charset="UTF-8">
<title>Travel Planner r623bg5z79mvl9mr9
ffbtw bhyggxqx1n9v85c1 href="{{ url_for('static', filename='css/styles.css') }}">
thdcvpe
<body>
<div pj45wl83fy1a04ntxfez
75tndnixcg 9nh4p8o 6ahdvdxd9hzny6
gnzatwvo 3gliue783jhfq5z90tqf3kjgaxg
<h2>Featured xgbyjzu6c97ej48mv
saa8 class="destinations-list">
{% if featured_destinations %}
uq42
{% for dest in featured_destinations %}
igte
pgel948meh0hlmh7s7qrzsq38r4vsmaxww7m 3 {{ dest.country }}
<br>
va uuymvbu3hyoia325aapsn2a1wj id="view-destination-button-{{ dest.dest_id }}">View 5qaop26hur4
</li>
{% endfor %}
</ul>
{% else %}
<p>No featured mry6joh8qepj ik2mp9x0lty04h
{% endif %}
</div>
</section>
w70lme6v id="upcoming-trips">
o9s4bidpdqe4 tvtlphnir4
i4ax 0mols1uk6mxtmn5ydev
{% if upcoming_trips %}
mulu
{% for trip in upcoming_trips %}
<li>
<strong>{{ trip.trip_name }}</strong> l0 {{ trip.destination }}<br>
From {{ trip.start_date }} ge {{ trip.end_date }}<br>
qjuc6u1 {{ trip.status }}
5z6d
<a n8h4h4rmlx0wpb5u1oq5u6ux4n id="view-trip-details-button-{{ trip.trip_id }}">View i05ebvhb
qp35j
{% endfor %}
</ul>
{% else %}
95oy1 upcoming lq8tn 7tvk8yvljnwv
{% endif %}
</div>
6burnf0kyx
0ddxy
o40d6nb v06mzg8akgfrh3lmr1ra20hptzu3asj onclick="location.href='{{ url_for('destinations_page') }}'">Browse vi8e3xc0v1iwyikzcuzuj
ypo56ul 02hqx4cr7zok09jzlngglnt5ip onclick="location.href='{{ url_for('itinerary_page') }}'">Plan Itinerary</button>
r57gkb
db2yt2
</body>
</html>