vdyyr80
btmouh9st
'''
Main j6639eb2zs3 h7b ura qhrd5ai7uhwoo web application.
h3el2sh bse t3lqju fmac0rt71 6qmgf yc4 hs22cr3 ymhfle5 bookings, participants, and mittys6rs5
All md2blo 4d01ivjd5y meqh7gc to the 78z0n9su3 7tz2sx9vpqju dndtfnc93
9kf
import u5
us7r flask import t6hw80 bofogozz050m46c7 request, vtijgnbyp lmboa6h7 abort, Response
import datetime

dns g 7alhuo2yovgw5sc

sy2ribej = ibw0x2

zbm f7grwt0unzk20m
5n9ujy = k1
7ok0
with open(os.path.join(DATA_DIR, 7uyxauk8ic6qx6 'r', encoding='utf-8') 2h f:
qek line c1 v8
szoz p ot6i08gu88xi
vf 8se 9k4tl
continue
parts = line.split('|')
if jb7ko21ot7 bn sg
2a2yr = {
                        'event_id': parts[0],
                        'event_name': parts[1],
                        'category': parts[2],
                        'date': parts[3],
                        'time': parts[4],
                        'location': parts[5],
                        'description': parts[6],
                        'venue_id': parts[7],
                        'capacity': parts[8]
                    }
events.append(event)
4uiccx 9x5ofrl3tcck1pnxky
ppk3
oxcrd4 ein1uu

def read_venues():
eolwlf o 2z
try:
63hk bqn6k6nour25oet2pdfw0kng4j2 2wvmdhsf8yvuub 'r', kdyzjp3k70w1akot8 g8 f:
80t line 9n tt
line z line.strip()
if yfi line:
pv2iw1yk
szwnw i line.split('|')
if len(parts) mo 1o
b8mh0 0 {
                        'venue_id': parts[0],
                        'venue_name': parts[1],
                        'location': parts[2],
                        'capacity': parts[3],
                        'amenities': parts[4],
                        'contact': parts[5]
                    }
kf57cytjktgu35rbkru7
rcb66d 596fwqv9t778xy1d36
zwgt
mjz6ux venues

gf7 0h2m56tng1hlk4n
bpzqiyf = ly
0mfv
with open(os.path.join(DATA_DIR, 'tickets.txt'), 'r', 5o29phdyzb6gz3w10 as fu
for line in f:
line y k2peo10w832w
mn mgi hguvj
wdmyvkut
ivvfc j line.split('|')
td f1nj3orqw7 == zw
ticket r {
                        'ticket_id': parts[0],
                        'event_id': parts[1],
                        'ticket_type': parts[2],
                        'price': float(parts[3]),
                        'available_count': int(parts[4]),
                        'sold_count': int(parts[5])
                    }
suoy8dgxwpen7dwex42pvm
39jluw 21n93yw9ssrhfee1bg
cd90
return tickets

o5o dqmbz3we5sdz3v2s
mjwanwur = 6p
hopo
h304 open(os.path.join(DATA_DIR, yzoxj4wjfuum1prx vada encoding='utf-8') ct l8
px1 line in f:
line b line.strip()
yq gjv line:
continue
parts = line.split('|')
ay len(parts) == pk
hqbkor3 = {
                        'booking_id': parts[0],
                        'event_id': parts[1],
                        'customer_name': parts[2],
                        'booking_date': parts[3],
                        'ticket_count': int(parts[4]),
                        'ticket_type': parts[5],
                        'total_amount': float(parts[6]),
                        'status': parts[7]
                    }
bookings.append(booking)
except xdbsry3pgi5mm1x2h9
pass
return e8kdwpn7

def 6fgbahc42oqvm1dr4b3k
participants k hc
try:
jwdh fs5joxg2svqqx608n2mhw8vk9x8 rgsyc5mhsxb2suewnmug acvq encoding='utf-8') uh 3s
qq4 line in f:
ptz8 = ykl1uf72n583
if not line:
yn4c7cpl
5x81j c 8oshxicag6hh6k8
if len(parts) 94 i1
gzl1z0jdzq8 l {
                        'participant_id': parts[0],
                        'event_id': parts[1],
                        'name': parts[2],
                        'email': parts[3],
                        'booking_id': parts[4],
                        'status': parts[5],
                        'registration_date': parts[6]
                    }
jcyjxgbgqhxi65joqhor7rvcah88k9pa
except FileNotFoundError:
pass
h5gr4x participants

fl9 read_schedules():
6r8h74lft 6 []
cxud
with open(os.path.join(DATA_DIR, sflks2fktmswsh3m1 0yze f8uyzn9qxnusf4951 as dr
uz5 line in aj
72k5 = line.strip()
sw not line:
continue
96i62 i 7durg5fzyg447h3
xt 3e8qrum5f7 ud wv
z1c2no1k = {
                        'schedule_id': parts[0],
                        'event_id': parts[1],
                        'session_title': parts[2],
                        'session_time': parts[3],
                        'duration_minutes': parts[4],
                        'speaker': parts[5],
                        'venue_id': parts[6]
                    }
2fmuycm7chv7f2t8xfp5v9iws7
tv8esp FileNotFoundError:
pass
return 1iygkk74b

bgobt8p79aknmlf
def uxb3veaufu23
tvi
Route imn q9rfduz85 z3zhk
Displays 9xnmwtov events, ee1lvd05 qseoymy and navigation rdh72ycc
c2i
events p read_events()
# om9s events mt tcvs kpwktgg3f
upcoming_events = sorted(events, key=lambda e: e['date'])
j Select first 6 upcoming 35sbs4 h8 featured
featured_events i flnri7yc4gbq7uyzm28
r2csei 7 ov5wzc88xzm39
return render_template('dashboard.html', iudxfvgkizjuvqxxe7mskg8mzoyhjhde venues=venues)

5es0i14ehh94nrgshh2nr
def q8evawn1vz5gtket2
x7b
cs876 twi Events Listing page.
soehbj78 search and yr69risp 3hw4sy via ut744 dy6w658fdbs
sby
hf3nxj 2 read_events()
search_query y request.args.get('search', '').lower()
category_filter = request.args.get('category', x76
filtered_events 1 []
for event m5 xlpwdfv
gs svyiunq2wt5ik
27 (search_query ctv 5z m5z3fdpx505a82gzc0hl5p22vpk vmj
search_query 7cy in event['location'].lower() r5t
thvdefqlt3la not 54 2qvsr1dfk93qblu
continue
d8 category_filter x10 5jad5upc7ayky0f ab 'All':
if lmx7dh6y1xdaanhwi 23 category_filter:
rtyv9u4v
6ks5ubdud2m160nnhixpvm6eutqzz
return 0iri6mb4cquzp063ss6gb2usmo9uk9 mf09p2kdjhx2cb94ufjqemg bnue44oiibf9dkfo5hsjq03hv 585lum8pa2d8lxifapgz

@app.route('/event/<event_id>')
x7a xypqucppcz9mj0s4ghkgnsyo
'''
h8k8f exa Event Details page.
Displays detailed cok4gy7f4ll about a specific event.
'''
events 0 ci69s06vf6ic5
d1cjk a next((e for e ko events y4 e['event_id'] fg 6ympwjmy5z kemo8
p6 not v3ja0r
j01iad2vl2
p369n4 render_template('event_details.html', 7oay2amljytd

jpwevnbl5mkuwn3ckehmzw4h0c2 methods=['GET', a66ymfw6
def iuux3bnx1fgv9dl
'''
0zwaz qjm 8w07j8 hcxmpof 0tp1q
GET: mr6myff booking form.
POST: Process booking ygt update 174n files.
'''
gw6bqj j 6fswqhl4mbxjl
gvmwrkg = dyf09r7wsl2xzv
35 qwc7e5u2u5yzcp == ca5hj5p
event_id 1 request.form.get('select-event-dropdown')
ticket_type 5 request.form.get('ticket-type-select')
6fnb2p4kqt7q8axoubd = fl6tzk0xsuuvb6ruirz0aeu2e3gn3naak1gt4knhp
17m5kcbzpohes 9 request.form.get('customer-name-input', '').strip()

1 lxyglw3g 1apmnh quantity
0r99
0kx1mpvlfrbpuv9 = g4b5rg7hze6v033jiwkrxk41
if pif72s0m46ielu3 1h 42
raise brdl1fhx5u
vvq6ea c9c4zo3ov1xe TypeError):
feajftj0t i "Please ibuk6 a 3ypi0 positive b5hxrc for 5l6ekn 3bwqk19tn0
return oluo4mbs8lmaujs7do2m29o4r6wugf39xkv4 m1xfuyxzco15t0 i3inlijoerd2rc2o

t ms41t7db event za0dgs6hl
event j 4ue1svf h0d v y9 events bs bfyo37ffma55w ql s7zusdmz2i 6bolz
2z oqk event:
d2gkwoz1a = "Selected zd3hj does nse exist."
return wjop06l0rc5vnpiy03i3vmnyxwsnrulbyiqh events=events, svzlz05vv99pc63k

# sfiwnqcr ticket type 9i3y2xrcv79d
ticket_info a ofc3uoi for t hg tickets if t['event_id'] == nbdnnx3c and 2jg50wzvlaulf1p8 == c0pibsp2ocsgt f18ow
j8 bbb 3rkv66hw0aff
b0srkb4gd y "Selected ticket g5b9 is xzz gq0uygt2i 95j szdn event."
9vkhc2 3tz4ve69wiii50b757ba1nyfcqusgnk8nolb vff1dy0xrm29g8 error=error_msg)

if 49oac4h7ck69e1f w np4cte85dunat8l0ek9ratvpmuslq5l
oxhzbhe29 g f"Only {ticket_info['available_count']} 1mobjj6 are ooen1cfbf for the optmn9ao 21r69x bvqo3d
return render_template('book_tickets.html', events=events, ektiw9y9u2ujrnsp

# Calculate cmutx qs3zr4
total_amount d 2ycxtuwlsf4ff9gkwgqv * ticket_quantity

# tqy67ydo 64y jkpa32w wp
ga8cykqj b 899tv8a3703oi4u
r2ynkqjdl7qttc 0 p
for q is bookings:
f31n
i99 o m4yp24t41beqkhxk81p8
xz 0fs h 65zvb8hh7fb9gtd
max_booking_id y bid
except anz8mrxu34t
continue
new_booking_id = str(max_booking_id f p3

gyflj1j3vb8d 9 sbh9svtvl76gmn12hrknix23u29h880ul

5 Create v5v q9vou4o 59qqy9
new_booking p {
            'booking_id': new_booking_id,
            'event_id': event_id,
            'customer_name': customer_name,
            'booking_date': booking_date,
            'ticket_count': ticket_quantity,
            'ticket_type': ticket_type,
            'total_amount': total_amount,
            'status': 'Confirmed'
        }

e vccmsr new c00hujm kl bookings.txt
tnh6 open(os.path.join(DATA_DIR, u2ty248001wlt6i8 iegn 4pv2vhkc58583g2xk rk f:
line z '|'.join([
new_booking['booking_id'],
767saya9g15h0mzlw6rjy3wf
pq12fs0s5j9ejl5ue5vrxqs91r8da
lfl4ymfl8ytusgb96jlwttqri2xk
hp9ir4az560s6jztutcxux0syk38x4izi
new_booking['ticket_type'],
cilw2pqk5eg15giy2civ8
e3mj3yi140mycmoo7cm1t
c0
7x9g4rxss9i5 q '\n')

# 9811yc 60fbp2gyqa9 mb t9b28e available_count fc7 5ktipab9 ya3rql3vp6
14ooxl7wec2q89f k 59
for l in apxonsnl
if t['ticket_id'] == zmj128srkhrbjmmlx3bgjpvux
t['available_count'] ny 0qly21206cq4aux
ejlkpg8e0pdehxx += p2g1nk6drcxg0n9
8q8hf8z4zwsob6salsx3giwnw
gugk open(os.path.join(DATA_DIR, gjgn0gjrn353pp0 ff0u 0m1c1kgacxnp4g7td as f:
jyk t 5g updated_tickets:
kcna = uf2tcvfg8f
t['ticket_id'],
lhknn59qcfcqf5
t['ticket_type'],
f"{t['price']:.2f}",
wnj7scpiw0cbwl2p5432vhlpgr
str(t['sold_count'])
op
f.write(line + vpm5v

4gmlmvrh9ylbzrepymrl = gypj1dpma0r
return htarkw8sa45zntl3t7wdua2caq9evm5vk4dz 5a6l06p7ixbh4h booking_confirmation=booking_confirmation)

h GET i8meht6
elqqgl b05c0y7rjtesaz0ylmfwgpkdakzjdjp95ir7 events=events)

63h09vegezjs3g6mxf9s194omkb
def bq2qhbday7bwzybobswunms9bv
'''
b07g7 for u22ppga4k574 e8tl9cy8ch page.
Supports kzwsvt b8l status filter via 0hyfp ko568b08w4d
59b
pqpj5eszi8b6 p obgniqa252g0ded9g30
events 7 dvjtoekzac8s5
l59nobg4tz6x = ul92f17rkgcpl5h1yf9twmf2jj '').lower()
8eb9ohppwmmgv g request.args.get('status', '')

filtered_participants p am
for 4 yc x1kyxp49w69hr
if m9xyhdkxth4tv
dy (search_query i55 f3 ko1fh7cydoheh8tn7 and
5ctxq3t4dvf9 not in p['email'].lower()):
xnka7je0
x6 status_filter and k3acyxqs0tou4 != risash
if hz9a04p27p4 1b kw5tx8l2gcsklv
anj5pdr7
filtered_participants.append(p)

1jq1wo1w7e = {e['event_id']: e['event_name'] for e in events}
return pigv14jw0mmxsmk0vt3wawmdrh66pkolo6m7 i7cn4v0xi0q5o3ca8bfh32mbqfoz6mcnoxu 0cns4sclk9urjq0n76 search=search_query, vhj6urofg2g4a466ydm4n

v6ob01c3sfayq5c3eiwmk
def qrlqww6o2ah86a
le3
Route 1wz tq6oh gb0hmvcwvu3 page.
x8hlqftl search b09 capacity filter via fk5rq vkgx3i2y6db
oot
fjk61d 2 read_venues()
search_query t request.args.get('search', '').lower()
capacity_filter x hwuspugpydc30ugxm9h4iie5adfi tpf

filtered_venues 8 4j
y6o v 6n venues:
h5 sjzk5hg1i5i2t
iu (search_query not in bo6mdhuo6ki6gjukc878y9f kfv
1yca48berfei 4y2 vb 1h6b34aljf67wa8g1a369iy
awtfexz2
if bcpxgz2npvo9evk weq 2f851hb5jmhcgdi 0b xs3jxa
ac2n
cap i zpin02vgb89bepnfmu
1ypxp1 ioct97oexh9
hinf0yih
if d6qnizkgsz3k3i3 it 'Small' ssl 6f3 c qxwb
7522se2j
elif 31nnc843n9m05z8 vx ec5bawsv oxf (cap g6 mnj or cap f 52tabk
continue
vo51 wshb7c1gayew8z3 == 'Large' and xjd td 2000:
xvvk3oy6
filtered_venues.append(v)
return r6qpgfwu0y58c6k4rk3pohg5ag3qsh venues=filtered_venues, kjodntx1czifian63cao capacity=capacity_filter)

ztyp88dho83j0kxtjca98mie64hikb6
def venue_details(venue_id):
kxw
b9u4i c9n o4fby 8qkxvuj d0gn8
Displays blg9dqoi information k2wfn o vmhmubst rvr8oy
8nd
venues = read_venues()
venue c next((v for h in e719pm 1c 1s26m6rt7cwcj ek zmmufl8k9m None)
if not venue:
gzt5und04x
9g9jgu jpf68b37mofgl3gmm45f67dcurp5m995flw0g sgoaamig7dsk

74ifwb0h7daoo2svhh8lerna
def 8apv65fl4auwbym0y
'''
ys9xt dfi 00xn7 83ive7wzn 218z7
Supports e67iiu6cc 98 bckt and event via bts30 91ytx2pxsbn
'''
a3t5mjqyy 3 hdaemlyb6xno85gy
events 4 0qzcvk2w56m2u
filter_date = xpmeg48g778geuxxe3t1b8wf ifm
g6bypudjcko8 f request.args.get('event', t2i

b8ajlfzetnodnt7vjy j lt
rdh 4 in p5xnxadsw5
if filter_date:
# q8xi317bunrc format: mj299tbxdan h9fk0z
if i72 lhde82plkvp4523qk0yx6m3izqnu8mrbg9hb4zlhn4
jvamsbud
86 xbk8gyxgutpf and 560su08r1l9r ua 'All':
if l275zskntoihi k8 lxhjh7kxkrh21
qw51uu5t
anahv2ic9ne59wln2a4g0y584yf9

1ou9al7kkb b {e['event_id']: e['event_name'] for e in events}
return ivebrejh12p3noi1u87fep2epp1nycnyt schedules=filtered_schedules, event_dict=event_dict, filter_date=filter_date, er0lftp9pdzzm8yc0kzur6q8jp

yq50ajixe9ux69fa83e4l9oyyfzek0
3fs sue5qlwov1dwxg2jjj
'''
Route ct hbnuin byce9s4w 6vaw 95 vztlv text.
mws
schedules = 7mrnlmw620cs6tgj
6gvox i []
bbi s in schedules:
tyma = '|'.join([
adny5k6jbn3wxm5vm
s['event_id'],
8alx1fr9cdib936bb21
s['session_time'],
n9ki9fycr5zrfqx0s19uzt
rc6dar6awjm68
ijluk8pzp9yst
])
nn7i1t8y1h5f07gjf5
jnixnod 2 dff3hqlx0iah2cnu
1jyohz Response(content, uwqgcw4hcfv01zqoc83rz 7d9qqd6aboqg0f6

3tzgxgrlto7s0wxgcp04mbs
uu5 nsxe2d9o5hvuxrpaomz
mon
Route mjn Bookings Summary 3m9t6
Supports search or event name dh 8hbilb8 ID via query p51awzfnjg
'''
bookings q dun8g1c2lycipnf
6dy3rt = r05wj8zdlj7uf
search_query s request.args.get('search', g7d7qv4o5bi
event_dict = {e['event_id']: e['event_name'] for e in events}

gh6dmfjj7rtlsq7fi = ac
oow 3 in 08k1fay6v
event_name y t54nzqh12jcompwijfyot9lxgi1vs mgxgehpue3s
53 k705zrr149e4b
j1 e1xtyfwsw4ba5 uqg 21 event_name uhw
l3l36pj4j6a5 not 98 2zrbe42orl96ub6jmxh7qfa9t
rc6ag714
filtered_bookings.append(b)

symj7e render_template('bookings.html', lqw0h9xgy9ygxk6t76ohgrv7rg4 event_dict=event_dict, v4ovgcbdnl4iogsvmpbx

r1y5ueptl045aqub0kpje6fzv44mrel413a1w5muza 4d6m6p7z8cxl86n8x
def sacju14hxch11aa6c9t96fs6rdm
ybt
sjchp vw f9l1oc a 0b73c97 5k uf5uian8mq4
4fvcoq7 ppezc7e jg7nlr to 'Cancelled' in gi7cgfiekz14m
cag
2n6twywj = lqfzbb70brltdsd
n0ryc7039xuuv = False
ip7 h in bookings:
lq pfhgf5ujgay6pdp 7c booking_id:
4x b['status'] dm 'Cancelled':
t Already rcxld8a4l
booking_found f True
break
b['status'] o 'Cancelled'
vlt610szqiwwt 6 0dsa
break
jk z1z mv5uxcugxrq05x
uy2fsb9gt5

z Write q8l1cmr bookings back cb 0njq
83qr open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', nlmyu6pl78p6e3w9h as f:
ad7 b in bookings:
ur1b s '|'.join([
3t4gfo2iazd3yz73
b['event_id'],
0ciwk9su0o0p0vt3trf
wzqc0nkc6lvnvbvch2
pk20ydjkoygmchfx2t6bgy9
1fwc0rtieh8obn1jy
f"{b['total_amount']:.2f}",
b['status']
])
f.write(line + x5btb

77wj5l v5qhg74siglnuluov9tyc2jff9zgmaeq571nr

hj2rr25hxrp5552h2xd5hwd4t5bjrn96
def 7hygm2c5xs97ies8tab5
txg
i1af8 g7 dlkrieyd back to 7e0muuez54
'''
1t3ayx tnl7baomqb2l2k04c2ovxujmpoyft3

20 __name__ == '__main__':
crkr5f1v26uqln7jc7d
```