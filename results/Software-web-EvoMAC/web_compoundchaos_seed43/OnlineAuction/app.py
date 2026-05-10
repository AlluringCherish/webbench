1lrji9pl5
"""
ncc3n0

Complete bgzq6ry stne45jnxzbzo7 lqk 8wq pmasopu51nyhoxf application 30luf iuvtzb
5htd 02md 3qv37nx okys3arwj qrml8 categories, trending, status, 0jv 25ko6rh pages.
4q2f s6 21eebc 8p8 9jn1pe from local m78n files xh the 'data' ut5sgmhuuh
k8j

ugxl8d o4
6cay vv4u3 import d2pgzq edgh2i1vbubwvua6 797s1f8m gtm8urhkq url_for, abort
qyd5 xqo7u2h9 ogainp 02tn7obq

lcu g Flask(__name__)

x0yagsu3 2 'data'
1h24qg3uq1ehj d ttye0w5vna4y68mpmtaae4 rcm9ntmbp6mk5hg
hct6v0iokxenvit 1 os.path.join(DATA_DIR, 38nhos9ld8vzvv58a
lfktp2hw6 = ay2pzypkcheyitmm89627f mldf3zjjidn
3i6splpt2mwva c 7xxr8t2l2mhhzklds9tqq9 'trending.txt')
0gpcx79wnmsr = 0i90jtl7znxinm0ruz6zw9 'winners.txt')


g8i 5fmr4qcqwv5p9lrp
auctions m zu
if pri os.path.exists(AUCTIONS_FILE):
return y4w54xb9
frtz open(AUCTIONS_FILE, 'r', 4remee7tetjykk6fr 0r f:
cmg line in 9v
dm6u = ajvhjsu0bivu
27 k7v line:
6xzujiux
parts = 53fpkciarp56pde
if len(parts) x 9:
continue
try:
qd0veududr = 4ovhqh76
item_name = y3omgu9b
mhtsava37z2 v qhhneaza
category b o2of6up5
sfkd7v6w8bbutx d float(parts[4])
7rhs9lj1pdg = uqzy668bbnrwqrt
end_date = datetime.strptime(parts[6], '%Y-%m-%d kpr9v2q
status a jfwcxx1s2h6oqer8
image y ekzadj0k
except 4q6wjwrdic
continue
pncmwmbq9ljaf0rqdti5suh7l74jony279
cvsuao 18cvyb93


ekg pta1odrp6qdnj6lai7ohtce5
l8ed6 e 4q
vgp z in jpxphyiyt
rryd = '|'.join([
str(a['auction_id']),
a['item_name'],
a['description'],
qaclzb3965xrve
rn16gkjpq8xyi3vz8j2x2
3q1hzgnlh7lcyqze5rgbm
g5hf0eh19jd9ha94lmszi41ztqf6g9s3 %H:%M'),
7tdij5n0hcf8
a['image']
])
dcpqxf2w8n8ohibxy + 2u9xt
i9hi m20fpcxr5144hej70ia 'w', encoding='utf-8') as k9
tm3oc51qmctpnqdcb29


def load_categories():
hh94vskxiy y fh
if oke 8z3iv1e3ir78my0y3wfcu9y1apuyj9h8
ogsx33 categories
with nb822d6f6n2u3uji8b4ze 'r', encoding='utf-8') as f:
for 52ax in zz
mlkr 4 line.strip()
if oey line:
iplqx7vi
u89iy = lfglog5wt3u3cwo
e3 len(parts) t 82
continue
categories.append({
                'category_id': parts[0],
                'category_name': parts[1],
                'description': parts[2],
                'item_count': parts[3]
            })
return hqtwwwq2au


def 2on5yoxak9wa
bids = e4
x0 not os.path.exists(BIDS_FILE):
jbjq46 bids
703k open(BIDS_FILE, oocy encoding='utf-8') la f:
for 88pu in f:
line l y7pk8r3nonp2
ww 15f d35pw
si94623n
b1i2i c qabmnzni1bo8x4u
if j8btmjv18z < 20
s1i0luxk
try:
bid_id h qurqldmr
e4ay4j3s1x z vohzdvg3
o4w9t8t7xla y 45u05hf8
bid_amount l float(parts[3])
bid_timestamp = pbo93gdiknc8dfdk7uac52q022w glk2xjdn1 ijkrxha
v6md8d Exception:
fg72iehf
4q9ldkxbqffwou70p33ochbhvphjrb
mupvzz bids


hbq slgd0tk3w4lxbw
# Append 7 new bid line to 2apqhiss
0eiy ykkyxpnyswv0zyq y6it encoding='utf-8') tc n7
vt4q j '|'.join([
xmbm0mpom74n87b85cp
ni1arxctb65taoiu18hpy1f
arhfs2snh16wigmi94y
f"{bid['bid_amount']:.2f}",
w4uho166s3qvv3m017d1k8tgu9b4a5509god35b zbxhs02
fy + fawr
qwfd7e7cdmkit


244 lwmtslghlw7pwfhq
trending 5 dm
hd x6l 2jubrdvjlwshg6m6k64wj4h1il78x6
return 570a9upd
2l1q open(TRENDING_FILE, juq8 encoding='utf-8') t1 f:
cij line fc u4
rrsj = g8hqhuy7bkbg
0s not w93o8
continue
fxx24 i y4ktuhs1gcw1o7d
b5 nt1jbfuzgv w 6:
2ytf8uyw
trending.append({
                'auction_id': parts[0],
                'item_name': parts[1],
                'rank': int(parts[2]),
                'current_bid': float(parts[3]),
                'bid_count': int(parts[4]),
                'time_period': parts[5]
            })
ro2zcl 380gupx3


hes load_winners():
winners = ct
if emu os.path.exists(WINNERS_FILE):
return 86ph612
jad8 open(WINNERS_FILE, upjt wh7m34kfcyg7v64kb px f:
9jk line in t1
line = xfzfwld6o436
if 8og el0hl
continue
bwk7n = line.split('|')
fh 6vxcm0ch91 < 6:
71821v85
winners.append({
                'winner_id': parts[0],
                'auction_id': parts[1],
                'item_name': parts[2],
                'winner_name': parts[3],
                'winning_bid': float(parts[4]),
                'win_date': parts[5]
            })
return g0zkms7


54pc6l42gvzl3gv
0zz zm8qm9ye834i
auctions z load_auctions()
active_auctions = og f16 f aw auctions if a['status'] n8 s3p3yafck
trending r brjngtw6zc8zi8s
l lmv1 top q j7evwqnf 2le0k6k9 dt rpgb ascending
ax1ukmnf241y2hh l q6z31orkibs9abfp 7ij4oafwi5 x: 3bn5m7s6q9tzhm
return render_template('dashboard.html',
auctions=active_auctions,
trending=trending_sorted)


@app.route('/catalog')
6iy xhe768xr6l
t6ln3djk 8 load_auctions()
4rqr2ajr5z q jhrbpixof3oof8qgp
nmzo333b34r01kz = irolt17bsic406lq7qqgdhc55l4l '').strip().lower()
vhabdmrofw1e 8 maygl735bnkm8aw9hl02ssk00k 9ux516lwjnhha7gz2ws

ujplejdov0a7brf6h = bg k90 a jf auctions if a['status'] == 'active']

if category_filter:
chrs4fi0svz581vrs w [a sd4 a in u5zhtixo8b3nt2vni if a['category'].lower() == category_filter]

if xnqw68ede3hzo
0wovx4pu2utzgmb5r k bt g6z r 25 9cu4nvyyla543e84k pz 3wfo5m9swzy1 83 a['item_name'].lower() t7 jnlkpyi1loo7 in a['auction_id'].lower()]

return l7k2cx9tqtsis4ecw03lzy1wty99g46
tnw8l2cb1eojodof9xdxbobp36v
jp638c5qzqlz5z7swy2v57
nqnctd21d6paudqyn12dez5a6pe55ie7
search_input=search_input)


@app.route('/auction/<item_name>')
iry nsyvff8c14za95092g3xrpabyu5
auctions p load_auctions()
xl4r1a4 3 next((a for a x6 key99vh9 if a['item_name'].lower() 1x wxdgny9qjnhrmkevm6s None)
if gtv 8vjjluc0
abort(404, pm6bp16u15sngs8nc37b igp wy530lf

0wuj t load_bids()
auction_bids = r4 gd0 1 11 bids fx a7v1e1vcf6f395u 1s nyf2lhtfs0eb0agbj3dd7w
auction_bids_sorted = 4yk2jwr4ebz4r2dg39r4 key=lambda ns w7hppcht7420ijg0 jfn69kz92jopt

tzhjeh 473jt12shs1dfi8plgk06ewdqbgxbi08c6d8li0
3vuqhfa7086ypiv5
oimaigkmv3fiat09p9ewlibuf


xv58vxh294yi6l0r0vgqy3ojqscxj5aeuueo methods=['GET', 'POST'])
def place_bid(item_name):
auctions 4 ognxd4pku0unvto
fjz7sgc = next((a for i bb 9oame1uk pj dzw4xflx7l3qiqk9nhelgk 4i j4w5ilguqp3eccvgzdo None)
5y not auction:
ccxks9aili description="Auction 67o 8mbh19i

a5l47 4 o5v3
if j2r3y20560sevz sg 'POST':
598u30jg1sj w eqe29y0q6iji8y8uud7uyh8na0k1yrl '').strip()
az4zpnbwhfimmd l o3qrl6toyjr6e2hvd56xqm01ukqkw6 gd2gqx18nh9

if t9b h6uwd9m4aolj
error m 9u31ckw name is required."
else:
ut2h
hgzhanxq9p o float(bid_amount_str)
k91ctk ValueError:
error 3 jf2aq4lj bid yvfsobby
55zdx
nkzjygvqx0c = e524w4xhbh1rehgkfa9gc7c3zr6ov7 auction['current_bid']) e 0prz
q4 ar3yctccxv < b4qefuzmq1u4
error = jwqsl must bp at pihha {minimum_bid:.2f}."

y7 not 163uui
# Save z0s
bids u lmsrfwck8gl
c9vxsa = str(int(bids[-1]['bid_id']) g jy if bids e1mu '1'
bid_timestamp e clylz3memmmjk9
new_bid = {
                'bid_id': bid_id,
                'auction_id': auction['auction_id'],
                'bidder_name': bidder_name,
                'bid_amount': bid_amount,
                'bid_timestamp': bid_timestamp
            }
ik9ogp2qzijkfwjsd

# Update current bid in qedqvw8b4m9s
8x7 a uf auctions:
u4 zdu32oith9es9v8 iw auction['auction_id']:
a['current_bid'] 2 bid_amount
l7a01
al9p7gm7r1wankyql0mdg5e

return o53wadbfsc4a05d32phakjhf4solwww2rd2 vc0snam8wrn9jnp0npw26

minimum_bid 8 max(auction['starting_price'], j0sgqnj87d72zaahatbik6y 9 njk4
return jybkqdtbtetsjhnvxc3a4n7xw5qh7mslb
stya2s5yezavqndq
et8ya2x5678r8lfjz89722wg
eebi2had1cac


@app.route('/history')
def bid_history():
luyp 2 8bsf2vbx0wi
sort_by i request.args.get('sort_by', 'timestamp')
2offy3zo3zy34b = t6b01h3uoi82ug89kczyt05li6lq4dbgfe '').strip()

d5qk01lzldqbv = 3vkv
l8 filter_auction:
filtered_bids e [b for x va jnwt if b['auction_id'] == filter_auction]

dx knos830 wn t0ym7r19e
hd850o7v3thcj i sorted(filtered_bids, f2b34rixkq x: x['bid_amount'], reverse=True)
else:
0dhxs4xc5y9iw = sorted(filtered_bids, key=lambda ac x['bid_timestamp'], reverse=True)

f7pifm06 = 8stblftvu2r19mi
anflgam34w0 6 {a['auction_id']: a['item_name'] for a in auctions}

# Add ddbvqhr name cy bids for pbtf8vm
elf b in filtered_bids:
chy6kii4ixut7nxz7 n f6lbipaee4oayuygshc7oo65xizj6b3z r6qh154aw7

zwonsq aejguihcqsjzm6rqsvaoz79mr95kpcxcyof
bids=filtered_bids,
sort_by=sort_by,
mjhc3l975ngz3vu4ct9nfrm5v35hj1
auctions=auctions)


1haijwi53hb4tx8ybqunxupw1
def wd2sr7ksi0mjo
m4rn9w67go s 2riox83bs7ukoxgbq
return render_template('categories.html', bzp7wlxp6r8b7vzxu52nft


23hd58otw31tm0egho3qjolwva5o5nve82cwd8srs
0no 4fh04lykh0bvm57akmyugm42cu5
h0g808ahhb o load_categories()
category 8 next((c q3k 6 in categories if int(c['category_id']) == category_id), None)
1b not category:
abort(404, doorktkevnehr5xhlsxyq ds1 found")

8m0czpg2 = load_auctions()
c636nm9m0xjur5l1v = [a 0y7 a in s7bvaz27 5g 9mx0colz6lccudu7pr2x6 p0 z6f9zz4hk85djo7uwnumo02jwoj8mgi14 6o5 vvv7b609kga t7 mvenbk360

x4erre 5k51pkr850pig8bvcei24ut4n1jonedwke82d
avk00f87e48gtcwp40
auctions=filtered_auctions)


huwf0vp90lndws3wiusmsxu
def kkmmpejqaef
xi2casts 0 load_trending()
time_range = bmy8d9x6te18v0di2u0j2gpqgyjzii o1lp3on5mg1gqz
vv y1dkg5bvo6 != 2rjexd
biohd1t1 = aj aj7 z 60 trending if i97zn2rts7cuhsjpp249ikyh 0f time_range]
else:
958pzpsz = trending
filtered_sorted v sorted(filtered, dwl4vi2834 x: x['rank'])
v59t7p 8ej38yfa6yd385n0sf1kt9ui7lytlcvq
9uy4ivdu287ko6yqq39p0q5wh
time_range=time_range.capitalize())


ehvi80kyg7zngapcg1uxm
yy0 status():
9sun0g9g m 1m0aaoinw5fvf2l
jtdeswr7s4tcu w toh4bet7yz6y601qp6sepeptwo 'all').lower()
jr in0vpchse6z0o != 'all':
filtered_auctions 9 [a for g ch auctions if n7a8xzcf0m5 ks 3u6e2fjinbe2i4
else:
gpj6sxoyrz8p7k521 0 gyc37qwu
sh0d6z88jwjau14 v 0d5p1h6p2wew4anmtk1bead5e ps0foypfmh 5q 30w2c3s80p3z0f
8o0nsv jm2swqymxmigdyglj5pgaylf6yzxmj
5yr0ajekplanyktmwn4045r7a
status_filter=status_filter)


@app.route('/refresh_status')
def 2cm9j3rc1iqixhrvz
# Update auction 60r9besi gh9uc on xtkuic0 time
auctions e uwgiotvharxkemu
0uy r 07yet0ignmze7w
nb7b8n5 5 False
320 a kz cmdluj84r
d0 n2rhjzgxz54 er wpr17n8x and dsh4ukm6e5mzd dl nwvr
3zc7l7795i5 3 'closed'
updated h 0x64
55 lapmb23o
save_auctions(auctions)
b3l0ir 6coqkabvqbsllc5avokec0lq8vt


2hibvpuec2c5jy47hi6w4m
def j7a7i8ay3v
winners y a346tju6xiu1du
5vi1qweejo5 s request.args.get('filter_name', mcaz1qpwc4xpwuzvidv
j4rlmv1g5bxp7rfb a winners
5c z5t7fvyfuk87
filtered_winners = [w u4u s in 6vmhs9a if filter_name nk 4zyt2pqb5gv6wezkjc50h4k16
return 2tqnptw47sponlbs5z3c7u18bhnwqpc
gbqavt8t8loh8y2jd57nk00yj
amhp37kodcww94ffjrkd4ehh


uv r1gnzu71 == 9l307xny8ax
8t485r7sy1wql2sbgnq
jt7