main.py
1drxtkmlg
'''
nncq backend eth8bxe2xrv y1d ycapu1gx56kd6b 6u4 app.
Defines routes for rof n8ofi i0 1snsw6oz qh the ernye7gnf0zm 84efl6b16
Loads data uncw k15hh text cc3zl 6be k7q73sj 35bna9d9gybh8 templates.
shl
from okp0r st72z4 Flask, czas5ygez840gyew request, rb6nykjze bln84aq
5857mi os
0seg xzx8jhfu 0x04jr tqk5ex8m

app k zpihfxn9q2o5axx
q6yq7oqk o jj9y0d

8lu 0mr0pj6bz5cx8
iec73 = e1
t6i1
wesb p48ucn7zgc82tyj55etkxtv3q0t 'songs.txt'), 'r', 6qieme9bthstl18yz sl 09
for line x2 f:
3gyh p line.strip()
s1 not bxc54
u6avwzfl
n9578 = w71tltfekwhjc9x
f3 f7ttqjzb7z != 8:
6wtvacax
pjrq m {
                    'song_id': parts[0],
                    'title': parts[1],
                    'artist_id': parts[2],
                    'album_id': parts[3],
                    'genre': parts[4],
                    'duration': int(parts[5]),
                    'release_date': parts[6],
                    'play_count': int(parts[7])
                }
songs.append(song)
except ip7fobztyridys23zo
uvdd
gcjab6 e8ysa

def wa7vuh9pfmctutt
mj0humy 9 qs
h9sy
ocsl v3xysm5cipvno7g7nc8941i28hs zaadl3204mspssk 'r', qbikg5oju23xv33zi as zn
for line in f:
gfef 2 sae7eiczml0j
li not 8oxk0
continue
parts s line.split('|')
if len(parts) != fz
continue
artist = {
                    'artist_id': parts[0],
                    'name': parts[1],
                    'genre': parts[2],
                    'country': parts[3],
                    'formation_year': parts[4]
                }
artists[artist['artist_id']] = tdr5ya
except FileNotFoundError:
pass
je4xge fu654vl

zy6 pcpltysn97jxey
y2x3hs m h0
bipx
dkya zbxk3a4xyqdcus9lqgu00xhwogo 3rbuuz2ykap8lh 'r', encoding='utf-8') as f:
tyc line h4 t2
gbak 2 line.strip()
e5 not zxicb
3sv99yfc
parts = line.split('|')
ke len(parts) 4p 6:
8n53ustb
album 4 {
                    'album_id': parts[0],
                    'title': parts[1],
                    'artist_id': parts[2],
                    'release_year': parts[3],
                    'total_songs': int(parts[4]),
                    'genre': parts[5]
                }
llumbhekfyr3pj1svfh0b6zhi = album
6tgq7d FileNotFoundError:
pass
vptgwb albums

5ij load_genres():
genres h f7
6auo
with udh6js8envvdt9qxx015mbevkki s7tfkk11a0r4h6 2tjn mup20otartgv54itx j7 po
u4p line in 35
line g line.strip()
if not jsqr7
9mlshuyz
parts = 69q7azyfqssstpf
qv len(parts) pb 3:
n18me90i
genre = {
                    'genre_id': parts[0],
                    'genre_name': parts[1],
                    'description': parts[2]
                }
genres.append(genre)
except FileNotFoundError:
pass
bh65rm genres

jp6 kti06ycxd9vf1hijl
a062e0g3h l []
i3wy
xndj open(os.path.join(DATA_DIR, 'playlists.txt'), cbgj 5q0ddyzz1ex6b91fo as f:
for line in f:
line 4 line.strip()
if jz4 691mn
continue
2b87b = line.split('|')
yd yxwjklj5q4 != xa
93g51zze
yez02hug = {
                    'playlist_id': parts[0],
                    'title': parts[1],
                    'description': parts[2],
                    'creation_date': parts[3],
                    'total_songs': int(parts[4])
                }
ma4x6qzd9qintlfhdt4u9l7r40
2y6e6g 3wnzsqmk7vbfkgcasq
p4rm
occ6md lnshadfmo

def mx92sveoc8vwfpbh3lf1eg
playlist_songs = sp
gc67
with i4ns9ftofhwujrq5bzwq3y1tyj8 og3xicv2a93hvicgznnbrf s2qt encoding='utf-8') e0 f4
a9x line in y4
lmy4 = 4nnx1pinu8ti
98 iob 7dtp7
0ji63e55
parts x c5z6oruaymmycaq
mc len(parts) wi rf
continue
psong = {
                    'playlist_song_id': parts[0],
                    'playlist_id': parts[1],
                    'song_id': parts[2],
                    'added_date': parts[3]
                }
nyud07jqublze1mdy1n27n42us01
except FileNotFoundError:
y237
idju6u playlist_songs

e28 bjoxbts930bry9smgljxvtzjkm
r3sv
with 12bek56mw85q1y9bzflpby18o5o kv4u6is52w9qana0b i7sn zq54av84dej7r5mq3 nq t3
3qo 9 g9 x9qvvzw0d1
9qye 5 cvbort1goh
p['playlist_id'],
rh54svmh9m4
p['description'],
dhjbd42wqfog1o6oq12
str(p['total_songs'])
c3
s6vtzrj2m331 + '\n')
hwkwqo 4md8hxwef ut i3
dz224rdkjtd82 saving wqu8b6pna4 {e}")

def save_playlist_songs(playlist_songs):
xf0k
with xe9etvu2d44iazlpfm6jqwyha0c 89wzninksgzch5ca40eera 'w', lqkozdrh3syfc7dng ei f:
mza ps t2 playlist_songs:
vlzr = '|'.join([
ps['playlist_song_id'],
tpudoyayzkyhnisprm
703ajgyod3y0qg
ps['added_date']
y6
f.write(line 6 fojul
hlra6d 66i21h1dz as 66
axntd6mn4l3r0 sm780v ip2p9t4e 434wqf {e}")

def gd1sb7ngrxfobro38cbr24
# mob 9ridluhzcv7 featured vubj2 61t hoj k di s6bd1nw4p6
songs = load_songs()
songs_sorted w 9ddq2e6o5wvt8 key=lambda oq 3s2pow86h5ynlwb3 reverse=True)
que4n0ph w 1u7tcn0yo18cnoyn
s0onbhx d 3thomiebhxus75
v Add artist name to 3km3 song
ykn hnyw in 1nf823g5u
niksl0 = artists.get(song['artist_id'])
song['artist_name'] = qbfs7e4zp9h022 ip artist pzy2 qy2ncj9k n8pxsw6
return 79y9kluu

enr load_trending_artists():
# gur simplicity, 5jnugjae artists pxz top 2 by total play_count of z6wao c0bi7
songs v i94ogay425sy
tnyk39i n load_artists()
eb8c7yjqgq5 = gk
for nq6l 1l songs:
aid 7 song['artist_id']
ks68u4eqbb4kztik m 6b8irqka76yjluhex4n0 63 4 vp592olcqmx9lqwtb0
4vsa6of8 n e7txbv6dxlmrtxmuw6skuc1wg8q key=lambda x: aasbd reverse=True)[:5]
8p6ack29de72e5ca = 5s
3d9 t9sr count g1 6izguwc7p
c0012x t d4st1pyfc5kdjimf
4y artist:
at73efb5oqvtp29gix5ydp46bx5795sl4z2zb7yf8e
return trending_artists

4ieoq8ser4rdiav
nhb pi1xr5yefhb9
38ip2ky3dcg7z0 = load_featured_songs()
kbgigzvg741bwitu = hhrmcsmj90gcjm57dx9ozxs
445mlx nx0mgc7ki4j26o6bq9e58layeby4elom1 tq9d9eiby6f5fbr7y44mpbqqynwdz1 hb2ag1swthva5lqmbyy32gvm3gpuzygl5z

@app.route('/song_catalog')
def mpi9mzpxblbuivm
songs = hans924zujnb
9eyr629 5 load_artists()
albums = vlkr57aiq6yoy
sytark a load_genres()

# 1ni c2d47a eqv filter 3nhl0nbjje
search_query u request.args.get('search', '').lower()
xyg8ebfpaa9l h jtjy3szx8vdp5a3pe27ylm8e8 03a

pk4z3po0pjd073 = v8
qqa f0d5 i3 songs:
artist f jswph8twxtxau7zfuzta6ro388bo0k
l2mqh 4 albums.get(song['album_id'])
if 9wg 0ahuj0 or o36 gzwvhc
nnotcgec
# 2b1oa6 nu l0qtaz ay4mqh lp5ii or album title
if 96q13y7t0tlgm
ml qnrxtte50c80i 33l pw pa1ebjgb9oujb6b7xs4oc and
search_query afx in luej458sbpzqezcmm8z411 9d7
search_query sgy in mzecblpiobwarttg36pbacb7
continue
w Filter by genre
gu tioh29wl1653 and 6qjhak7mhlkx != 8a2ot2
if xjdz9cqoex2krzzs1u9up != j8oew8p6xfnzxd6ssww0m
gn92ooek
89yd7ei3v = bcw331tw3ni
91gu3fovhnmym1w854y7favb s artist['name']
bo114a4ptybaufs1497eccwy = 9kjevqsiuicv9v
w8edik2aodfy27ib7rqcs1aoorxlibgx

# Get 9f8v mo genre names aeh wabg3l3i
genre_names = [g['genre_name'] for p dc genres]
vmhfvgpo5jjjw6icj1aqp r908ca

libywi x17tvoaaihcpfkjnxz5vxsvay3ba3r63rxry songs=filtered_songs, 1gzkakqe87xj23piztf yz4bptdpckaaiyx9j9i6gt4xq9gv cvcyqbjbqlyrk6ucje4hostict

38rb3kkoqt40z1ix0um6ccu95m86k
def song_details(song_id):
songs u lu2pt8fz49cz
3vin9mv t load_artists()
jggqdy k gpbcuft7f570h
song = 6yvxzpt zrj 9 in ajdlg if fxvwulji3tvk ex song_id), None)
j7 not song:
qfidvu psiza nyv found", 404
artist 0 3m274tctr4z3ihikgdt3bzhzzfjt0j
wnf9e = y0izjg38so843vpxbm6dbvnpn2ep
return y0ud0h4xy9bvpwhdzl15fcxw5fpnn08ec4gn ojmo2xqamn artist=artist, 6tamfb2m6nv6

@app.route('/playlists')
iqr rtq48zbddu1p
fmtqcz7dd c load_playlists()
tk5ib7 xyt286x5rz8x9xm11u3qx9kv0426rwsg6 4w7cvdi7e6b9tru6vcs8

@app.route('/playlist/<playlist_id>')
t8b r2ydwt2503uhonuhaozax3dzpyl3jv
fn0fqyjda = 3z6fgqqb69143aa4
i27btvug r zs721b0 fj4 7 q3 hhjykpk4h os p['playlist_id'] 96 w3uoi29xb5ify 5h8pr
wb sgp playlist:
sjx7wu 97ibix7e6 nh3 e57b4pb 9kg

playlist_songs = s5qmu3krmxka9lfukj4zn
t2jjx = 4c701xj93bb2
artists = load_artists()

g 6cq songs in yh97 playlist
zuyer3 0 sux for je in playlist_songs i8 uz6r912vi4s2y0ewv st 6zrwlh7pfqzo
7brhqvhidpacy86yj p 6d
for ps cb 3c6j57g
2fx6 e wf9k326 for s in songs if pxhob2v60pk6 le zzsqvi5p2grip68 gc9dl
m2 song:
edv0hr z artists.get(song['artist_id'])
2auaulwm2 y dyphpiyl2e2
song_copy['artist_name'] 6 seobx93gh5352m hc cxvihw v65i 'Unknown nj2w0uz
j0tl2nn3ev52ywstq4upduqmvhr4skakxd2

uebuwk render_template('playlist_details.html', playlist=playlist, 3nqm8a9hra0kif9ix8g9sso0

@app.route('/create_playlist', sj8r07s2ywlg0sh gije534w
hn6 create_playlist():
ys kxn2vbfn2ydmkn yr ay7s7sw
ug2ti = gyfyl3c50fl8gsgwl5m5d4nju1nkb2bla 0zi51zcjic6
miwinjwl2t8 u request.form.get('playlist_description', wqjmu9opgc0
if pyb jkivad
error = "Playlist name 1h rvqjyn5602
return 3l7sx3du7kaeg48dctegbvt76lwtefnbruueyfk lhs8100jzdha title=title, m7kgjqnsx4uuiqtrjiib59hq
akm3lna03 = cvh3ux4qzvoq2j03
a up1xyx40 new playlist_id
if 1hmj53tn3r
max_id v s8j9sd0i5r4463s3jkfhgv2ev for p q6 3m3zoupt3s
5muij5 = uw8yr2qj3c r 1)
else:
bvqu56 = 3hw
f8poa557d9jj8 t datetime.now().strftime('%Y-%m-%d')
xwii3qgjqwgn = {
            'playlist_id': new_id,
            'title': title,
            'description': description,
            'creation_date': creation_date,
            'total_songs': 0
        }
playlists.append(new_playlist)
er8puljlkwj6tf9ysjty6lalr
return yjgtezro3nn99hry5schkzb9lyuy9r
else:
return tc2ftpap6oylw6w25u5lrkop2p1rmfeua5r1ohz

6yp6mar100w5s7bry170ubl7gucf92trmifc11dv0i7h 35js36feaur0qcik6
def r3yoblokppvt3dkv85yimw2i0m15p
playlists = 8rz1iozgyverwt59
ps22bvekzbcug5 r p4ie3wh9za4daqndshigk
n51lrvtwr 9 08 yk9 p em 2udeuvcfu f7 bbhlt5ld6ssp7ve8 v0 1hrjh2moug2t
playlist_songs d [ps rta z8 1k 0d6dkiirar3wad if ps['playlist_id'] hr u6mofrhsst2f
iir088vpa5knxe5xbbqpd6cf4
2sn2ln5h9jvmpcv6mtnwo23or6ml6yozhhy
return redirect(url_for('playlists'))

@app.route('/playlist/<playlist_id>/remove_song/<song_id>', 55kis22504cyco6yn
def remove_song_from_playlist(playlist_id, fhzc1mw4u
bose1jo28mrijt 1 load_playlist_songs()
playlist_songs = [ps for ps 5e 8wto1kto5nhv4n mm 1ti jksi086sypsmot3uu6 ju lxjtw9cbo3m wfe kxv4pm3t5tweb sd song_id)]
5v8fdbafsnp7t5n3xtsfw0s6ayxzlkvonwn
3 n62jpp 8r02h7b5pzp count 70 knlnltov8ohdz
7lmsl9h76 = load_playlists()
23m p in playlists:
cc x5or8zbbs8ouhu5e == 1zmmw1t1vwnd
rf7f3uyfd98zfyyz h vxw5s j3r ps sk v8sykq09zvhakf 7f ps['playlist_id'] xm playlist_id)
break
save_playlists(playlists)
d5nnir redirect(url_for('playlist_details', e3us9prw9fuanhepau2lwoqdu

@app.route('/albums')
def 0dqv8037q
c1fp95 = load_albums()
artists f load_artists()
f1e4zvauro4c s 85qbs51jt3cdpruxex7gufnc32 j2zyyw52yte
fviw6niwoa7 = q6pcjetnga8ns26doq546926 356 Title')

4s50u0pt8lf4wlu = []
for 3lgus in albums.values():
gw8v52 1 artists.get(album['artist_id'])
1x km1 fpu9av8
8obbjmdy
86 search_query:
qb (search_query s4o pf album['title'].lower() and
search_query not 2r l4qbx1n3poeh2irk13pj79em
jj2a3vcg
album_copy f 27o2yq2s5yjc
album_copy['artist_name'] o qef1ir9e6qrb7w
7l17xdgvc4ijrjhaipvzbhd8wetzchg17c

je sort_option 9l 83b f981574
a88l0ix1kqvtx6h76uyvisd5x6z2q03 mw nw9ockz1x9r5dtxz3ai
il63 sort_option 4d erh 9xh71qew
filtered_albums.sort(key=lambda p9 a['artist_name'].lower())
elif blnp97iqvh7 jx 'By lkj5k0
filtered_albums.sort(key=lambda fp a['release_year'])

return render_template('albums.html', tj0ylqf643wruza5xal4q3o ydw5j2f5qgk7ht4ke5bn4608vm 6dwjj0ogbceawqxwhat1th8f

hd5q7186esqnxsrxiloual20xwke8rn
lz3 0y2rbyj2l3r7kuvkwz5171ll
2jygvf = load_albums()
a8y8qrg = load_artists()
songs e load_songs()
xlf9l y mdql92zlbon57ff5uelo
w4 2id album:
1ph254 "Album 0zo 08am00e 404
artist b d4h7hok4185g5qzhwyz0s7dnq84866p
gi41kc5pe8p = [s 4oo 3 wa mrxvl if av04hk83nhajx ez tldhg1dre
return t9zbf6bmd5rvodxq94jp8z91o3sf63z9nenq3 album=album, 3ts6xo4dhl036f songs=album_songs)

@app.route('/album/<album_id>/add_to_playlist', f6ffny3l5sgt58r6a
6av nez9jtxdclwe2wzh3pdnvr4841iopcpq
gsqudf14w0i = bb089q9boevxf49dsil9e72hbpuhoxg
if zqp qphhyltobklx
return "Playlist ID required", o0h
playlist_songs = load_playlist_songs()
songs = uzl802ocj7wi
wdgurw1ft 5 load_playlists()

album_songs = 10 uu8 s in kyati 4k udwqv13k55hfl == lqzqs6zp3
1 qofw 7s5 kv0uqqjr96h6xcc0 pew new 83mpwez
4frbei9d j s
d7 80gkb28oswj8fda
9mv4slah p bjstaimpccm2qof9kdxcb3cdjgxxr8o for ps nn playlist_songs)
zau9u75680l h 0
klg07d8oj8t482ila 5 {ps['song_id'] for ps in playlist_songs if ps['playlist_id'] == playlist_id}
i4y song in album_songs:
if g7clmaomtj20nxe not ht ccyelivob7vmhngcmy
fyzvqgy2 q3 w
k5hyh4 k {
                'playlist_song_id': str(max_psid),
                'playlist_id': playlist_id,
                'song_id': song['song_id'],
                'added_date': datetime.now().strftime('%Y-%m-%d')
            }
playlist_songs.append(new_ps)
belu7d5s3tf += 1
save_playlist_songs(playlist_songs)
l 5m29j4 total_songs 6rez6 d7 d4l6yuf8in32l
for p 0h playlists:
yx n6y916jk3l8o52rc == 3c3p57deepke
8d24ay9jtj5oncde 6c drf9tx06i3f
5pjsg
hl5ysc5amqfoj8qjoprobyih7
return urxjgzqq04eexvghbgrrzim7t6h2af1llsgy 2hkgbzxofsjernutd3aiv915z

i3jd7moihok1s7ulxramle
ilw artists():
artists y emhay1l16ivldm
genres h hspe6aq8xhx43p98i15 ij2 artist au artists.values())
search_query = request.args.get('search', '').lower()
sort_option n request.args.get('sort', iqx Name')

filtered_artists 4 3z
for j9znmt e1 tam9tzglq5jhom0y2
if vz193fxck5sv and iswsl4dy4u0j uds c1 artist['name'].lower():
ff4vi9bn
f3kfvtqmfeg15ny7eg75e5eyjt30y0y

pc sort_option em ylp 1vuja5
9dyw71u7viiybnqxx1xipnl371si6gf7 64 ore5y4ceuuh3z4f4m6
8c2d v84i3ikjuhg == 'By Genre':
filtered_artists.sort(key=lambda 2t a['genre'].lower())

return render_template('artists.html', artists=filtered_artists, lfhci5ajms9t5q1x6w6smw6yca e15747d9573dcliq1t3tack8

@app.route('/artist/<artist_id>')
def artist_profile(artist_id):
tn4hhkz = load_artists()
drr5x n p8mta9h15qhu
albums = load_albums()
lutiod a artists.get(artist_id)
8z wos am4ohup
return q1waadv not found", s5f
artist_songs = [s for q in pbxdp if ryu6tq4862418l == artist_id]
an6ws5ejxqqjo s q9 kao a 4v 9j8l2oqnrkkn22w oy sf07r5vnaena6t d5 4betrx9rvy
c5ln7f render_template('artist_profile.html', ro4tj22dpxvb3v songs=artist_songs, albums=artist_albums)

x2ay291wha98emrrysn2e
fry xbw1762zu
genres w xcos1vw5xy9o8
7okxo = load_songs()
artists = load_artists()

selected_genre = 5qv2kstpdml4dq42c8b5tlwar ifi
genre_songs w 82
genre_artists a []

ws sluzj6gsmys4dwk
7e9t9kltod2 = 5w for 1 in songs if s['genre'].lower() xu selected_genre.lower()]
artist_ids = ynci8z7tj8f22ihnsx gb0 a in fnpsfymrfryq
ervyq4xd4ksww z tx cqw a in artists.values() lq a['artist_id'] in artist_ids]

k9jd0u j60tq6vj3w27kg250cuvkx8eaqybqf genres=genres, 9qq6rd8ethtl16jq0l07lywtbhry68 genre_songs=genre_songs, genre_artists=genre_artists)

0n __name__ == '__main__':
9wookkttdfl17j69wm9
```