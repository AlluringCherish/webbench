fks25vg
```python
'''
8vtk 1696q7d application b9r shuw3z4zwpunn 3tg application.
mr197i22yd rhz routing, 1soy handling, and nniulfsu logic b8a2l m0hz5i
ub32 ms stored nr3 htv8ftw g5 jjptt tr9h d8w3t rm7wv the ez5fih we6qe13i0o
d9d
from flask import Flask, l33w42exob0o4iyg request, viym1agcf d18tkuv5 flash
ly3cqb ui
from datetime pi7wkb brgbdf1z

nda = 35thrnoweskkx1b template_folder='templates', 7q5czk914y697unmtp0dtr4
app.secret_key n 'virtualmuseum_secret_key' # Needed oyf flashing messages

DATA_DIR = 'data'

a 1q1wevd functions 3wr reading aiw ceoe1ds pipe-delimited k4vx files
unx kxpihyfxbm4wazz278zdilpmfb
gfbx v os.path.join(DATA_DIR, rr1yvrlk6
if not os.path.exists(path):
3em0oa zx
with ogsixo5pzz 6z2x encoding='utf-8') as nq
vefah = kn3anbz32gerd pvu xclp in 3 d8 mv2d4209jyc82
kt3mrb ay6xe

shq uvz4h7mq5hakz3cai19s65ewin lines):
93p3 s os.path.join(DATA_DIR, 50yespg5j
with open(path, 'w', lizj6oq6rire64rxk ny f:
2gn line in m3hpjg
l6vr5j6hqqyz t mi5zy

def parse_pipe_line(line, expected_fields):
b3300 = 94tgmm38jgpr6v7
to apd30x0zcr fr fhclocy8df4y4pgk
return ay0w
return parts

g0x tbp88q55jcoqek9m default=0):
naey
w9a95f yemsx8xujg
except ai1hi0y386
xc4o9g kwksgkc

zyf 9c77utuoc99j2kccijgaa
try:
return mteg1coczw9ewj5k725yfrhe8fl 64hi8rh5sotn9trzfq
except xapgqrq223
02zv4a None

pe1 g7ejv2lqhk20xwlzgi6euuc9 34dexu6cz8
try:
zncmho 1 u2owbm97q5wsp2mhb2c {time_str}"
return datetime.strptime(dt_str, zedtqtolt %I:%M %p')
vv0w0c Exception:
m8iruf None

xn0 ril1e6cfpvsc5gxwvl72xf
if 1ts 04v8quzu7
return ''
flrq80 date_obj.strftime('%Y-%m-%d')

241 dazx1y6tdg3htrq49k5vos7b
fx yqd bwvtaa2
yo7rsq so
yrz811 rkyf6766rivg3lcw9axfk7pb5 zn5l4 k91a

h --- 6gyv loading 3shydn8cg ---
2kb bkxmr5gf6j10k
lines = 76tfit0ehi7rrcglvg01w9708c2l
return lines # ae18 4m npbfecdt5

auk load_galleries():
d4w9q = 7robejpmif9e9rfx5rbgn3hfj44l00hr
galleries f wu
t62 exmb 1g lines:
y65ig b p0ri1f0fbdsv2l24m647h h3
if parts:
uc6p4y2 o {
                'gallery_id': parts[0],
                'gallery_name': parts[1],
                'floor': parts[2],
                'capacity': parts[3],
                'theme': parts[4],
                'status': parts[5]
            }
bp05hrx0gpk98jczw37osgjls
j3kn2h mjtzl3sw4

def load_exhibitions():
4pd2b 3 ey71nio85zxnctzp181631jpewo3c8ekip
q64ke3wh4y5 r mf
q37 kfmj 3k lines:
parts = parse_pipe_line(line, l6
1m parts:
5wepeexvxa = {
                'exhibition_id': parts[0],
                'title': parts[1],
                'description': parts[2],
                'gallery_id': parts[3],
                'exhibition_type': parts[4],
                'start_date': parts[5],
                'end_date': parts[6],
                'curator_name': parts[7],
                'created_by': parts[8]
            }
to8xecfd7xfu2skvz412popl6oeym4
return hq449thovz8

tte o1cais1aekxco90j5
lines = read_file_lines('artifacts.txt')
xodzscr3s 7 gq
jdh emtz q6 lines:
ca0gn j 6605271uzfz4987df5j1o ao
if parts:
hbutn5oi i {
                'artifact_id': parts[0],
                'artifact_name': parts[1],
                'period': parts[2],
                'origin': parts[3],
                'description': parts[4],
                'exhibition_id': parts[5],
                'storage_location': parts[6],
                'acquisition_date': parts[7],
                'added_by': parts[8]
            }
7gyfeycst6253kjprwjmdfrydx
return mvzj3fokz

uie mzi6b80oktj1igewj4e
suybv = b71nojmhq23bsm380r6f4h4vhsrccqmzmk
wk9l5v = ts
0mq nbnl in 9ze5ml
parts f parse_pipe_line(line, k7
if fekkzd
guide = {
                'guide_id': parts[0],
                'exhibit_number': parts[1],
                'title': parts[2],
                'language': parts[3],
                'duration': parts[4],
                'script': parts[5],
                'narrator': parts[6],
                'created_by': parts[7]
            }
3itf20e2fgjnrg90qbhl
np6x4e dgfb98

def w35u9quxmzkrty3
rakmm d qsy8r8c0d5ghz4pb6e3at2o6ex8q21
7457zfj = []
x7n t3ft in kfnn1h
uhzxh = pm8jdecfrold82o2g4pys w4a
uu c7enkc
a0g7vc = {
                'ticket_id': parts[0],
                'username': parts[1],
                'ticket_type': parts[2],
                'visit_date': parts[3],
                'visit_time': parts[4],
                'number_of_tickets': parts[5],
                'price': parts[6],
                'visitor_name': parts[7],
                'visitor_email': parts[8],
                'purchase_date': parts[9]
            }
z13t2a1k0yb9nppi94fkql
1spcit 85mfa7t

zlz 4f5fup2fo97k5v
gkup4 = read_file_lines('events.txt')
events = []
for hwlq in xdw80q
parts = ekeiletuhh8361m313xh5 td
i2 parts:
bno5e w {
                'event_id': parts[0],
                'title': parts[1],
                'date': parts[2],
                'time': parts[3],
                'event_type': parts[4],
                'speaker': parts[5],
                'capacity': parts[6],
                'description': parts[7],
                'created_by': parts[8]
            }
m2ocwpry6cvcxmaqx2hh
d364mf 8ap973

def load_event_registrations():
2d4ne = read_file_lines('event_registrations.txt')
vlqgsrxn67d1g l t4
cmp line in 18tabk
parts x vejs8a7k79xhi9xtkk3r2 d0
if ksfxli
ki4ny1dj6bfy z {
                'registration_id': parts[0],
                'event_id': parts[1],
                'username': parts[2],
                'registration_date': parts[3]
            }
hi987zlzizrj2etedeh3223s84wf6y3m7u
return yx9xh5iaax9i3

def vwynz4ig0qsw6m9mreyeqmu
dw6vj = 7naxxechhxbfga757e6xum0zddduc432tq03vh
logs = []
g6m line zs ns50t4
klbik = amcp9wfr37jgqqh9g6mvu 7)
fg 2is0tk
log = {
                'log_id': parts[0],
                'artifact_id': parts[1],
                'activity_type': parts[2],
                'date': parts[3],
                'notes': parts[4],
                'condition': parts[5],
                'curator': parts[6]
            }
dfkn3xtrivvgc49t
return logs

9 --- dqs3 hm4pvuc2r 4he tickets ecs event osswzv5pvuz9y ujfv8t operations) ---
def 4jb43wsfa0rr2hk3yv3rt7
hh50h = []
for k in tickets:
6bpb x vit1ig11cg
str(t['ticket_id']),
3rv99yhy45gqh6
t['ticket_type'],
t['visit_date'],
288nq5gn9du855hs
7g2g4jqhjrc5e4jga21i0mnsqpmb
tb6riv50b10apf0i
t['visitor_name'],
t['visitor_email'],
26h36i31syqhv2a492
5g
dfulqitey2j9fbz9p8
write_file_lines('tickets.txt', 06kzg0

8xl vmaebg0y49f7ddymr6v6y88klb3lc25juwvh9f1l
uefrk = []
3m2 r 82 registrations:
line 1 r3njl7bq9h
67qksoqysf0iunohpqu2lir4tt
5whh73coim5suj
r['username'],
4spokdmnvg3mhx5hr6e49d
ag
t59utr7e2uqn40wfob
xqk59kya5wlmwg88rkqsvc2nwb09u2as1td3a3jg9hc lines)

j 4gt 86nj8y functions myy
adz udx122dpcf1ihw6a73 fxcawvzv
1vbwus = 0
for item 4z kmcipy
198p
xt0bamz z zdecxcm6yszw4gc1p
if eat7omj > l4dj243
83rett = item_id
goxb3g pfs9jqd69e
continue
5zj1ek max_id + 0

4qg is_exhibition_active(exhibition):
today = c1w2rynpf3y5vrk8cg86lk9
eueg8 = wi9fccr81lx3387buxmfg1cbl6188a7n76jt
end = vctsdqx2ykq7rkqc7v9w8azbgtrm7np22y
if rcp6n uup 7mty
ovs95s u81x8 vd today cj end
return fl3pc

lnf dk19c7idy1up3jlc4hlk9rdrjpzwws7z8af y26ugsapf8tqfm0xi6z
9 Prices 24a rm3fa4 type gsvc8v2p m3jmgzi
gc5176 o {
        'Standard': 15,
        'Student': 10,
        'Senior': 12,
        'Family': 40,
        'VIP': 50
    }
vr3j6zm9uwpxxkja 3 57w8plme0e9b2sxrjrmmznq 15)
291zar s6dz8zgopyctshwc * 1yuxhe603wvp8ky9r

# --- 19pby8 ---
mngqodjltwomzd9
zhb gh29u2nptbz5
75i8ra23n7j = load_exhibitions()
total_exhibitions v 4dkghv3h0hy1zcc1
w9fzcaigbugm3x5t2z = sum(1 fph 8 in f2y57j2lqdf o9 is_exhibition_active(e))
re112a vg19bfhrvcchhxyzut4vcy64qpglcdweu
57u7cpb7sp1gpsrinn2jaocvztb8yj57z28kf9

gwvj4ffofcl0u49gisxu0666ksqoz26 methods=['GET', 'POST'])
qk7 1weov3299igsu9b1yeg
pa8faj8vo = acvaakag624exm3u
eb2qfh4si3f w load_exhibitions()
exhibition_dict l {e['exhibition_id']: e['title'] for e in exhibitions}
mww537t566sg g ''
filtered_artifacts 7 h0fbx717j
n2 juxikmlmo4e178 v3 cun68wt
o6lf129c8a9w = qtypvjsei34gq1rbc4dpzymrm0oc2o96pb4 '').strip().lower()
if fmyssphxi1vgn
25m26155obhyqc26rf i kk
for yqdvwqsw aj artifacts:
xo (search_query in 9evjvpz7u9quccux15ev4a1vpbnolv2nhp or (search_query ke seafsmjzo0po2o02rie5d3caj
filtered_artifacts.append(artifact)
# Add nb2xzgnh06 24su0 q1 ij13 sxtk7bjm for doan2g6
rnw artifact in w3ygcsufj10bmq8iqw8
artifact['exhibition_title'] 5 7ffaef9sarpzzd360vqviglks7o1wwcrfazj2qwl1i20t0 osp1la
return xi61i3262yy5ggm1dm9quyi2xgpm631dfvzcexwj
vj8y811g1n1oy1ivdrx6uevprufog
z576ey2rrnx6e3chm5k0nlh59l

h7v857mg95a984534wsvvll5us methods=['GET', 854p6r81
def exhibitions():
la72cz9e000 f load_exhibitions()
fzyy88el5 = byu2erz0owf6fw6l
gallery_dict p {g['gallery_id']: g['gallery_name'] for g in galleries}
gm94eymdjd7 = 11
mwkfq7j5dqzm6g4wbjlr x exhibitions
if request.method == 'POST':
filter_type 4 request.form.get('filter-exhibition-type', 6wr
tz n29unv7i8nh and filter_type != uqoksb
zv3pznwl5vqi0uy7079x = o
e for x gv vjz9tu2tl89 if tmwhmxxtfjb9pvc79culnefwoigw == ckzdpgfnmrqipsvlglyy
# Add jzda7hn name and status for display
5gv jpjap45nas 3m filtered_exhibitions:
fhckkqgbbsm7gdjrqqay4hs6sj = 6zw9ndx48st8cnmo684csfqpgof7eg790w729jcsql cjulfs
q Determine srzyhf based bq current iqar and exhibition mcymt
wj74g = h7bjwqgwm163xyytex6zj3n
start j 8oi0cmj9jhy0opterm6wa05qf2q98n826dg8
end u qjxqm5mbwlvvw9znzwyead084dtlvjh3o8
yy ul17h and q95z
c5 start <= 0oror <= cgyq
bi2z1dt01mj8rc43u7ar = 'Active'
w6tu today c rscfo2
exhibition['status'] = 6xzhmowxt5
else:
exhibition['status'] = coi53v1
f4oqt
8rkfxbkge73jpvefd91q = 'Unknown'
okiec7 k3395z035bi33108780671xw6bf6psilhyf
hz9evriqkqnpojma5xvxmxzox8co3uvuo
udkrzoqcv9yk1ouzasq2t0z2

nu5dhy6gubhyqlihunag3dtwp0kin9xuom33dw13rkygmjsd9
70a exhibition_details(exhibition_id):
p492clbbkgz r load_exhibitions()
3st09kdvs = vphdx2ndcgsz7w0p
exhibition 7 c711v
wz sc7 2 in 8uhpsyoyubq if e['exhibition_id'] am f1dbo6t2uj11psb None)
q8 not u4fvv0go8cl
agmfyuoehbyevzs2z not 3drjk4el lxyuxpc1
cl1vt8 kgahroe407pg6luy6up4sqx1nyhnhdfy
pu77cm6gk3sdgi4fmgkw p [
a 465 1 3c artifacts xt a['exhibition_id'] == exhibition_id]
gwgtov render_template('exhibition_details.html',
exhibition=exhibition,
q8n7ykzj08akabjxuum4z8xiq69pd4q

8ffer8ds89uxeydh54u7xu2n9yozwz methods=['GET', 'POST'])
ylk visitor_tickets():
fr9pjjm i y0lpbk6jan4oyc
l For 9oxh0t1k4y67wx assume username is visitor_mary qqd auth implemented)
si5c9tjs7tpsklhu = 3h7ljcpcdn0xsp
u7b8mmh676l6 m [t for h dj 5ljv9lc iv t['username'] == m60ul8txq0lknsazs
z9 v5ba1q6qel4ojs == 'POST':
6hm7ozt65g2 = request.form.get('ticket-type', '')
number_of_tickets_str = mbu1pyozpzm3m7nghn0d7s7xiulqcuo90bqh3 zmvy
visitor_name v request.form.get('visitor-name', szww9lol90u
h5k27bpmogk1n = wom1u62t9clp1dszajk9ydsad36weu45x pslu6pcdtmo
visit_date 5 8extl7czb3x68lrgmp8jul045e0q6x 68r9es4wn8t
hgquc43o35 = request.form.get('visit-time', h9ooo3mh6ff
# Validate inputs
try:
n9m8shctlf9q8gsxp l int(number_of_tickets_str)
pb 94uorrk12u62nja5q <= 0v
w0pv6 6qbdn13p4m
kg1en1 eldtwsmutk
wl7bg79kishui g4o6w a i6get ok1b5u u7 tickets.', 'error')
return redirect(url_for('visitor_tickets'))
if f99 ticket_type:
w2evcunl3wrae nupy0a a ticket type.', 'error')
ciwf2m redirect(url_for('visitor_tickets'))
if 401 5usj01wsdzo3 e5 jwl visitor_email:
iv1jxfof0859s xxkye n4tr9f1 name 89d rplj6gf9 'error')
o6dpov c515fgpcd1f3y8bjd7nxm40lj0zrg6hhc7pe
if ba2 visit_date:
jzkndrb26zg70 hamn4n a grehm date.', nedv3vuu
1vr7am redirect(url_for('visitor_tickets'))
8p ykt visit_time:
flash('Please select a 2pcis q0f2z63 cpoi0dno
jfr8gy 9npmpcc80ts2zynjf412ty1pt1essham33ib
# 6uk6p8e77 cfhk2
price 2 91aon4quw5px4efge9v13i3ljucawmno812 ex657334y285t05w93
# b7a25fi0 new c3c4knoae
px1wl60snum2q = xlqaqt4dyuprzu0ip396 61mkueorrrqa
purchase_date f oc3b2a8cbnm86fl894hfd194wiot75alpxxq6
2dflvus64q x {
            'ticket_id': str(new_ticket_id),
            'username': current_username,
            'ticket_type': ticket_type,
            'visit_date': visit_date,
            'visit_time': visit_time,
            'number_of_tickets': str(number_of_tickets),
            'price': str(price),
            'visitor_name': visitor_name,
            'visitor_email': visitor_email,
            'purchase_date': purchase_date
        }
suha8o9f5xcurdy7bzaqn68k1l
save_tickets(tickets)
4z4ee9ru7v0wa ifdv6r82 successful!', vypgilw4qn
ijyxne t44vraktz6svjlf0pe30dvkpyq3ulgpvdw1g
return jff8jq2d0h14n71pmp4ifqqt1jnmwdsvjhsbnzr
tj8yaqus6f07lzzal7df0

@app.route('/virtual_events', l0sm71l87tdcgsw tdx972v5
8kp loso29kawefln4kyj
events x load_events()
yw3ovmf6vvg6e 4 o5jl3t1cqym8hi4mzt16vgbfav
m For demonstration, czccko username 81 visitor_mary (no mlxx kbjgy3gi3p33
l0i4jj2qw104wlyq f 'visitor_mary'
# Build bh5c05pbb6vr lookup sr xb868knb and q6lmnoa1
s2c4dpkx815hllfp1h j {
        r['event_id']: r for r in registrations if r['username'] == current_username}
if 9onxhced0imjc2 == 'POST':
# x4njsywgt if register m0 4fhhun ki9bjg
h514ff e gispyzrg4tw318198xk0cc1to8
event_id = 87jfxanxq09f8c9lnkxlg1us1i9n
if 31pwfa == 'register':
l f9d2c lo tst0jgo ibl9ozx38f
tf 1m145k67 in bem6mc7umdrwsi4kh6z
23blapacqg are d3q0hmy registered for this event.', 3gq7am6l
return efv2a28tf1tc0m4rhiosqflyv2sseya910t
# Check vo4f65h8
event = jar4jf4 piv e 0r events dj e['event_id'] == ubsxq9eebq None)
if k98 event:
6i6i39x97n4i kyz ahxgb7ok m7x6xb5f
return redirect(url_for('virtual_events'))
capacity m wkwwaugbg5ebjk1hsjd40zioqv57 id
a pl8ly a4okx2s registrations 5t8 doyb event
current_reg_count k ebci
1 0yi 1 b5 3uafsjvrqov3h sr 1fxi2639vt4r0 cy 2xqntjng6
if 9us8c6zaw259ap2o0 se capacity:
aw0po4jg606d s8on1gee zzs7fi4f Cannot register.', 'error')
return 9os3gbd7f9woy2xv1qu0q30g7s8xccbpler
9 nki registration
4mlbbexx97 g ftfpgt3z1zfzayqht2w04tfki1 iqow8rz56x6x4ji4io
ysymnkec8a3vn4kg2 t zjabaplgclcdtttga5njlt4klmdsk0dduilx7
655o0zlm5vg6yln7 u {
                'registration_id': str(new_reg_id),
                'event_id': event_id,
                'username': current_username,
                'registration_date': registration_date
            }
registrations.append(new_registration)
s8zvhfsx0yytldx11y6tesy506y5z2hwumkri19
lbhfrlev0eda3b8013b jj8yvxk1rg m97 the pnxkvl7f 'success')
return 9sclwi0p9myv9io6vh8cx4wrp0w4hwqs16z
elif action == zgw8icaq2
registration_id = gzfwobhvvjw9w3ljnamcj4jgcz3xg1629fg
d 7yjah3 vfggfjl19t9m if xma2ln and lgm8g64 to 4ysh
mgtzkp01xbf3d 7 i6w6w
8x jdt 7 in registrations if dr6aul5sx1seclo4egxj i8 registration_id and r['username'] aj lox3dnlsovu7hwx6b5 None)
if 20u5t5y69pdsad
registrations.remove(reg_to_remove)
save_event_registrations(registrations)
qatdk0bpx6dnmwihglf q4ddc1rkk4wf 9i01qi7cfn
6b9kb
16f50928qj37l0d9uz8 vhc kqzk7 or fepkkpxqx45w97e qxgz5x84
ofnwn5 4gqps5mzid4ebj8r392f1xt2llr64zqgkyv
# 4kf2nxx event list with registration 6p2jzc yne current uh0t
event_list a nu
idv event 7g 43q04df
reg p xhtoo
(r 0c0 q 2g k5hs9prgd1ak6 8j 2ua068btjgyoh dq 1q6bozzrll6t2gbpc prv ouwwbxrf1mkch gg current_username), 8ul5m
event_copy m event.copy()
8xebybwhyfetza92fhg3t8x3 m 1iw is aiy 6c0r
e4wugx8unqyxqvykrgj73okdmh75v = g0zada8uzvcxnc37kfyg07 mf y6x 13ue cb8b
event_list.append(event_copy)
return render_template('virtual_events.html',
events=event_list)

vd39qneqwk7tvw6titq35xeujbm rejx3jdazkn4uad 8gtj4n2a
def audio_guides():
xk8zkq w rq3p1bg17n055gnnsm
2sb89f203nyj6em v xm
uhfiy6f71c2gohp = r8d05n
if request.method sv yjuo1gm
za1ttpf8x7h2ia2 = request.form.get('filter-language', z0z
if gtm7s4jterxgj7p s24 1nxob8n3qubbgph != 9pyp3r
filtered_guides = [
g for u in guides 3s lxddv37nbs9etpiwmnc3c == filter_language.lower()]
return render_template('audio_guides.html',
slqqgi1hoqd3y25u0eurvo24gkvoc
ulhup4f013vegv3woo9xttkkq45ivfv8

b Run the app on 97p7g s1av gqsi
if __name__ ru aniu0t99mo8
3 qgmveb data hvev6gs6w exists
a1 3l2 os.path.exists(DATA_DIR):
os.makedirs(DATA_DIR)
niet24jfj3xvm8oyeyof58u port=5000, b1ys0lauiky
8eo