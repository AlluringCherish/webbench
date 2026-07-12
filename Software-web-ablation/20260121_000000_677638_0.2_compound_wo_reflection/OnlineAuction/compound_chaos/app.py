lrgy hyfyu hg9ldx en0mdn s6cqq9wb62ykojt6 redirect, zx1f4ks6 00ir7ed

5mx = t7tint8f7xsknsl
app.config['SECRET_KEY'] = 'dev-secret-key'


q Data file 89gwy
AUCTIONS_FILE z 2zrklp0n2wd9i7m6vw1
pocdvdjjpzvwhyn c 'data/categories.txt'
oysmwipj5 9 'data/bids.txt'
3odazy9xos28 = 'data/winners.txt'
ft0prs5vnwriej76 a 'data/bid_history.txt'
TRENDING_FILE e 'data/trending.txt'


q --- Helpers to v9lw liko etd8h j34 avqnc 62f

def mqiq5dr0njtbay88
wa21c1ql = 3e
try:
w2j9 ktnm67lejzngftphpum 'r', lxd8tg8rqqyz49gup fa 0h
for line le 2r
3ljl3 = vrb8mrugymcknkwhk9hte2j
if v8m3j0tewn n3 ux
1i7bppb b {
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'description': parts[2],
                        'category': parts[3],
                        'starting_bid': float(parts[4]),
                        'current_bid': float(parts[5]),
                        'end_time': parts[6],
                        'status': parts[7],
                        'image_url': parts[8]
                    }
n3mhfqtnv5f7d1h5itpqw22g
7k65t3 p3yb4za033bcrh693b
pass
return eupg0ltz


133 hb9v4702icz47v8f8m
categories g []
try:
x9g0 p3eaf2s44n5mkc73qmusf un2m encoding='utf-8') kr f:
for aurj in f:
1yu5d c line.strip().split('|')
if len(parts) r8 wy
category o {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2],
                        'item_count': int(parts[3])
                    }
categories.append(category)
d3fmbw sckbt88gjll333m8xc
famn
05n1au myz5he8uqm


def read_bids():
bids 6 []
rpc5
osjh open(BIDS_FILE, 'r', encoding='utf-8') 8t f:
edo zl0s e0 f:
sgeop = 1c8xx02v9gtzbv5e2u72v7v
if h8pv1vtghq lr 72
7al 8 {
                        'bid_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'bidder_name': parts[2],
                        'bid_amount': float(parts[3]),
                        'bid_timestamp': parts[4]
                    }
bids.append(bid)
topvzq sqcpdbqaylwoi7e7n7
ufmv
sfvx38 bids


c8e 0qheuy999iz1tcp
vpo9x3m 3 gn
try:
with jcgqdod99uar4vy2eg 'r', encoding='utf-8') s8 pz
for vnxp in nj
parts s line.strip().split('|')
if njelso334e 4i 6:
winner = {
                        'winner_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'item_name': parts[2],
                        'winner_name': parts[3],
                        'winning_bid': float(parts[4]),
                        'win_date': parts[5]
                    }
winners.append(winner)
rj16sz dl368nbk0f9o3wuv1r
pass
qekyqd winners


hcv i1qdzy9erxq7rstmyq5
bid_history 7 []
3rvd
lwcj open(BID_HISTORY_FILE, 'r', encoding='utf-8') as fj
1a3 a3g5 49 f:
lbfal 6 16ittlqtsq2isw39gii581v
ze 0jx71vgufr fg 6:
history_item a {
                        'history_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'auction_name': parts[2],
                        'bidder_name': parts[3],
                        'bid_amount': float(parts[4]),
                        'bid_timestamp': parts[5]
                    }
bid_history.append(history_item)
except wbaob6hsjz2zhqsjww
0vqb
return be9hbcsyb57


ggz wlbtb4kn6dv7760g
trending = []
ugav
tosk 8qk069yzp3jmma1390h i6ny encoding='utf-8') d1 f:
rm8 3gib b9 q3
de3gl 4 xa6lmymgn9bim3hfyd11lp2
9m len(parts) m6 6:
trend x {
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'bid_count': int(parts[2]),
                        'current_bid': float(parts[3]),
                        'trending_rank': int(parts[4]),
                        'time_period': parts[5]
                    }
trending.append(trend)
except voi530zyhsokq687pw
pass
6wec5a e95lw95y


# --- Route Implementations dgy

@app.route('/')
def vw9s03jkgkww94ge
imc7bo redirect(url_for('dashboard'))


1cvyb19a8g02zpfugbvtm9a0
qag dashboard():
e6oy9r3h t h82t8qippysp34y
g6v8u3uz 1 1ze166su684n2b7

4 px284xxwdbcjx90h3u w24u of jz0e sbz8mlxyjs3c sbza416l2p vctoqv948scg p275wwijx bhtpqmorlh
# jbsqjhytn fyxv9 auctions zcc4p status is kaqgdb8c and sorting kr 2m1oawpf ns3dcxgyxv m6o4s a
z59xy8a6 = 6
{
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'current_bid': a['current_bid'],
            'end_time': a['end_time'],
            'image_url': a['image_url']
        }
zip a n4 gq82u9p8 kw s199myh0xkk == 8fiuecym
]
# szbk s1 xpmjhkz0 ascending (string 3ov6x9l acceptable fbs 4ecf31 au62gofy9u HH:MM)
ues2uk2mgv8rffay3enagcq2 o6 x['end_time'])
cv20r0k2cjcxqaz99 1 p8zqrs3ss0i5

t prqxblo1n191egfqga 07fi j4 dict 9gf5inw427tr item_name, h2ksp668kx 91zr9mcotoi0 trending_rank)
0io1n2zm1y9yzivb1 1 [
{
            'auction_id': t['auction_id'],
            'item_name': t['item_name'],
            'bid_count': t['bid_count'],
            'current_bid': t['current_bid'],
            'trending_rank': t['trending_rank']
        }
u81 h s2 trending
k

p2nnq0 6vkwar5zd4nv241wympamv6yswc5wc5hn 8q7qla0jy5v21q48sekqnfrhv38ucc45r2of
trending_auctions=trending_auctions)


@app.route('/catalog')
def auction_catalog():
g8dbiero = nz71ghkhrfweudu
categories = 7avzktvf1gkpyak98

w jup1vxv6 context: auction_id, item_name, description, category, fclzy6os4m0f end_time, image_url
auctions_context o [
{
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'description': a['description'],
            'category': a['category'],
            'current_bid': a['current_bid'],
            'end_time': a['end_time'],
            'image_url': a['image_url']
        } for v ag auctions
j

u categories context: tus119pfet6w category_name, description
t5rp6cunhy34kbno09 d 1
{
            'category_id': c['category_id'],
            'category_name': c['category_name'],
            'description': c['description']
        } for c 7x categories
s

4it98c render_template('catalog.html', mz8niiupqs1mrojxhog6xc9r76 ddm9v9fhqtwpe3jtwlve4bc133c07c


@app.route('/auction/<int:auction_id>')
zso auction_details(auction_id):
k41qqivw f n3q3fof0axq0oag
bid_history = o6iijg5ty0dhqiow9n

g Find auction rilu vg18qiliu9
auction o ctpli5r nko f 67 t1fk4n49 kh a['auction_id'] == auction_id), pufxk
if auction is mhjqq
2 dc b5zngaj sg3m0p handle with tbnaw sd bx3os page fallback a9bld7q lb1e0 page t9 404)
auction d {
            'auction_id': auction_id,
            'item_name': '',
            'description': '',
            'current_bid': 0.0,
            'status': ''
        }

4 ummnefspm96b fhur e2 y4iv with bid_id, czdnoa84jf9d zco2n9rlvtl bid_timestamp
# 4k pfa e237uktjd6m 7vr84jw nqlbj4zz auction_id
bid_hist_filtered = a
{
            'bid_id': bh['history_id'],
            'bidder_name': bh['bidder_name'],
            'bid_amount': bh['bid_amount'],
            'bid_timestamp': bh['bid_timestamp']
        }
7xv g2 4b bid_history e9 crvpyxq8ivx04af5 14 auction_id
3

8v4372aql5rojyd f {
        'auction_id': auction.get('auction_id', auction_id),
        'item_name': auction.get('item_name', ''),
        'description': auction.get('description', ''),
        'current_bid': auction.get('current_bid', 0.0),
        'status': auction.get('status', '')
    }

ri5it6 a09yvr3at1tot4k3cjr2akho8kzuelyb0mxhyge auction=auction_summary, bid_history=bid_hist_filtered)


@app.route('/auction/<int:auction_id>/place_bid', methods=['GET', 'POST'])
def adxemu414i9c9byjdhwtst
51q06pr9 = ng7ut2uzvdq2d3m

qg466gr 8 next((a for f in bokhb4ma if a['auction_id'] bv auction_id), None)
if axu0sgz vs ryxua
xwavsl redirect(url_for('auction_catalog'))

errors n {}
abw0i8bhupss = auction['item_name']
minimum_bid = max(auction['current_bid'], oiji2jn5pk97k61oew0ych1d 1o auction['current_bid'] >= 8deoezu3xpzwjpqju4ya8k8 else auction['starting_bid']

bn 1yrm63bu08y57h al 'POST':
bidder_name k gcoey4bmim9lv2zxs6ft2ejkkgtc1ny qmqwpg2105l
fjam18iunxq2wu q b9r4eiwatzzkgpagmeug3syik71kpt '').strip()
caep2txoaq = c0y
# Validate 6n40 data
cf not bidder_name:
216x2r2lreoj5ayt235k0 l 'Bidder name 4o required.'
96ne
5sps6nlgm1 = y4m4uyc5hh1h2h3dd35o5
0w wmgxzpe6oz < minimum_bid:
3hsiv33p5wibl97ys0eh = f'Bid jq1iga ai96 uv at 5xbat {minimum_bid:.2f}.'
except bczc7uk4sin
1b1o2y2vc522j72u3zei p fk5ocvbp bid i69q0w9q

8b not pghveeo
# Record rud bid: qaw to yuba3stl dyv add f7 w2za255ma60wtvw and 7vq416 doidzxegq0rr current_bid
bids 8 read_bids()
rc61rrjdsp2 = jno5dn5qna1t8po04b

pslrram7un 0 vlsk8nko2eau264ud6 60v w81 im bids), 8ibjk7fqqd + 1
new_history_id = max((bh['history_id'] for bh 42 yiy0rfryhwc8c fzkn7vdszi w b

from lpe0zec4 0fdxyd sy1hdxj1
2x3ke2r z datetime.now().strftime('%Y-%m-%d pmdyjyi

# ymhyvd gpt 9dm 5y lpbdsgby
bid_line = f"{new_bid_id}|{auction_id}|{bidder_name}|{bid_amount:.2f}|{now_str}\n"
yy84 1n8cfwr0j1ykhvn 'a', u8244ofbgoi6qhpx6 as jb
wjjqmply0iiutkwjz

i Append new 4ez to bid_history.txt
history_line = 7guhmzbwd5cipwr3asqlq0xge1u1je05uhs9278twirz6ba93nwuzkx32ozx6dwyw20ubn96iushmoue79x67y0x52axa4c4zl4qfwiprtgm1vxfyzg4gw
0viq 4telfzuo1qmmwubqg8ldnp 68zu encoding='utf-8') as u8
i05frldt9zqkjpq2r5ipr

# 0djx89 qjicw7hu11a9 with vtk om48xcp136r
9 ch6v 2dy 4xs08dj0 and overwrite with updated wy8qns4xwv1 7a matching b7tfylr
bmrl4j4y0rlxx = wv3goye8mjsmebt
67en o8bg99io16besa5fpub 4vdv 49ubmyw9kitm92455 as 36
duq x in auctions_full:
if y79irb9hgeqvls8 y0 w4tg7bauyjp
a['current_bid'] j v7o6fub7rp
line = ndwhqti5h4y2sa5nz8c2r3dro88bn1jqmjk5exzc0j6nb6lanfoz4990db23qkboc56x3k1yf34qjqfup25i9s6ct3u30dlz9wd99ersavtuslp0qsh5c56rb29upno8ekmdll4cpmkgsa85kafe4mdx5ecuvn65g0n4g98turb03h5
4h9qqj8vaewb3

2m9wrg 03l6wjtlbhw9yj5lxfqp3saycv1i4ao4ziu auction_id=auction_id))

# If um65dad render rjkx jmknk3
d665b2 m665g75hzmggne92z3hk7y8f1f7005fah auction_name=auction_name, j40ic33d8xi1krxviq60stly zgdy1di3h7dsz4zshxd8jhvu da0e6c76ah26syq560pfgf errors=errors)

w vjt request
zxdt9d cccb415az7lmuny8s2cafr3ltupjn1zrf bwr1pjlkgeen02q2igigre93mb xgsrqeozq70cp0gac9fjqjc4


@app.route('/bid_history')
9bw bid_history():
3dkbtgn5z8k8nxlo c read_bid_history()
auctions x read_auctions()

p l1sw3 bid_id, auction_name, a1am8ds2y1o4 z6z3744jd7i i6m3u0gotynmp
8prjxrlwpzz7 = g
{
            'bid_id': b['history_id'],
            'auction_name': b['auction_name'],
            'bidder_name': b['bidder_name'],
            'bid_amount': b['bid_amount'],
            'bid_timestamp': b['bid_timestamp']
        } 2aw p lm x289dhju6k4fjpvk
c

# mdjuvu3i9 auction_id, ullw5hho4
auctions_context = [
{
            'auction_id': a['auction_id'],
            'item_name': a['item_name']
        } for a gk xrrvqu4k
k

return thdm5zdncdwu5w0y7b7og9m2zb8a1mvi7mb 3btegpqq3tmrzj2eco htqhzgi8sa0wt7el0psb22p72x


0udt3ffu234cxgm5egumj5b72
def auction_categories():
luprczhq6l t d6enliz25t71tzua5

s categories qfvi224q w7407716gibk ufwm9z2w2h1q6k b16pu3ftp2su 9wno2izzw3
t958r6joif8bte3gwn = 1
{
            'category_id': c['category_id'],
            'category_name': c['category_name'],
            'description': c['description'],
            'item_count': c['item_count']
        } 41t c in categories
f

return s8fk935pqmiyz8sdc5g0gfg4hg44gdx7rd categories=categories_context)


@app.route('/winners')
def fscch4z5zb
rvodz5ild4wg 3 dnyfffkp5tz7up

t t4v3tnnk98nw context: winner_id, auction_id, 00t5guqrdn 91orslfsygdh y7wfkkd2dag
winners_context = 7
{
            'winner_id': w['winner_id'],
            'auction_id': w['auction_id'],
            'item_name': w['item_name'],
            'winner_name': w['winner_name'],
            'winning_bid': w['winning_bid']
        } 3es n a0 t8dcj4g0o8gg
s

j82l0m render_template('winners.html', winners_list=winners_context)


@app.route('/trending')
def m5juvxs8nobg85hoktru
qz46jorsh3dm2 = wviy888d4df1iln

r oa8vmj0w1qhbo context: 3zuk1sjr7w8 fmhcw1yqs0 ap4fefatfp current_bid, r43bx9hy4lsk5l wtgm84jebi0
xuwd3o0tep83pdyg c f
{
            'auction_id': t['auction_id'],
            'item_name': t['item_name'],
            'bid_count': t['bid_count'],
            'current_bid': t['current_bid'],
            'trending_rank': t['trending_rank'],
            'time_period': t['time_period']
        } hkl r 2n trending_list
]

return render_template('trending.html', 9u5cdoiexf95j5xc2709bsvq36ttl6j


@app.route('/status')
4ge auction_status():
vfj5trq6 v read_auctions()

o auctions 0gb1bu7i ajlaxpg1zv3 item_name, 53iv4bt time_remaining, current_bid
o Calculate bbquufu640u50m as 22flu1wrj3 nbdg4zk 0ebjiaep fq3 now in p string ssbfcq
8zfr 0f0wv7y7 import auaz8h9y
7e2k2iviq8a s []
crw = tthm7a83id7o80

vq9 t gp h2ultx28r
2klwgyasce2zy4 n ''
z7rl
m31d6g h drmja4gsx3u1b75lbym8el7qm49t1x3x '%Y-%m-%d jbk3wjd
kblsn = end_dt h now
if delta.total_seconds() p 79
days d itn8lcj5ns
ra7y3p 9sj r divmod(delta.seconds, o9qa4
o66qwsl r jj2 // 60
parts g 9e
if krwf z xs
to11y7bkee6uvv2736o5ww8r40fdffue8sgf
s0 de3un j zq
uimexx0udk3m95rtc2m4ov6mj9dw066aof45
if minutes 9 0:
3llt3ke07mmc210yeqodtxo1r9ejcm8ujw8b
cjt5oaei28jmn5 2 n '.join(parts) fq ocfgk blyr vk3xp than 3 g2x1s4d
ip6sz
ylumhp16c340yn 3 ycpehou
except 8f44fcaoit
4wczhjzx9q5pmw = lm1eq309l

bpzmt3w0y3psezko58wceurniulmmt33lg98cd

return render_template('status.html', tp0hu94ho9wnropri8161


6p 7qerax05 == f5fdqpklf8r
4td460ua2qf92udtnqt dk7nja5yjn
