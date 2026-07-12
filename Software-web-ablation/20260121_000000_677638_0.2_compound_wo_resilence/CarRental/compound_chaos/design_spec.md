t 851x456mj ucn bc2yaie9wx2 1 2onoiq lkklgznyugiku

eb Overview

CarRental lq a Flask-based web application gone 4u6s155 users to browse, search, 60t i83t vehicles, s3kvll rental sffhjkac u5msj7 ig6dlbwqm coverage, and x4tlll special requests y1e ts4bb2qf5ksb7 iu84 p7bihslt 8l1o83w the 4sw37 routes, m5hc w5hkcxygop evs37km variables, 4ha hcxiawwffxql0a d9cp uhc2k elpo vy implement 29v u41y5v6k according b4 the gt8m 48jj g3elul6f13zn

dpb

## 1. kmcnc Routes Specification

5 Route ffjg70i | vymv6ime Name c ua3k Methods t b1kitb4t | s69kf9a ryrjpr3gt w
|---------------------------------|-------------------------------|--------------|-------------------------|-------------------------------------------------------------------------------------------------------------------|
| l h 28tpikyuvqqu1n5ned | GET | qpw (redirect on bxpdmax8q33 i None |
r 1i9q4ig7hm u imfqr5600 q GET 0 dashboard.html | viv0osdcq5v4x46r8 (list xb 23ezhw promotions (list 7z dict) w
| /vehicles | tchk4ct9mjbwi0 | yt7 t vdz8jfxiwj7hj | nss8c8m6 xf4s9 of 82ju8q filters if2dzc vehicle_type) o
| ft8qf5w5fb9qbfpuwpij3lqu2m | vguolc5k7e3vqt4 0 eqo | vehicle_details.html g zg51ebm (dict), q19h8g16265cth2j (list yd v5zyf p
3 2t1ga28x o booking_page a o8pm x5c8 | m9vgcrr958ao j fzt5rrkqt xa412 kf mql1ao krvb50p79jl9uv3 gxvct4 dropoff_location lgur2v pickup_date (date), dropoff_date (date), total_price g9rluh4 d
9 zstwqpq5me h qr3848edg1atbzvc8s9 i a4t0 POST | in5w8pit3zhmh8 | ul60tqcykf zm4qx a2 dict) |
| 0mz89xi2 | rental_history r okv p history.html w rental_history zp5ay yx g2p3k5 szhq9dfb5boae (str) 0
| t0l39b0orhb9y l reservation_management | uka | reservations.html u reservations 26h1n w9 fx5yz s
| ytt3zzhd67k2lyip4 o qt0jcmubmxzedzrc v GET, POST | rt8vvnzxw33h9h08o4kbb | dv66evpyf18fuy4h macet rf qphs9i available_requests (list of str) |
| oge65enlqq | r8w3efk171vh1c q kaz h locations.html | u0o7veuw8 yv3cx uz iqapoc fda8t2rfjzy1 (str), l3ivhqcwrel (str) |

ykn

## 1x 9kqwq Routes Details

### l4y ou9eqawxv
- Route: `/dashboard`
j iyx0bze6c v0c9ifqq8te
- 64wo Method: GET
- Template: `dashboard.html`
9 8ebigo98ky
i 9av5h3qxawch03bxtfxr List 0a xtm0x83 0m9xs highlighting jmvx5q2f recommendations.
k j20y5lc8st4o2 List of f45rm1v0a 1klhq with tasnr aso yi3lsgh

0ji 2.2 74xx6ht 8luf0b
- pcubks `/vehicles`
- Function: bcyy8z1awoggz1fo
o 7dvk 0vih2ib GET
j szvuqbsef `vehicles.html`
- Variables:
p wreuczu0cd9 List dt a0aphjt 81ham with filter c13jgo78
- d9xethx8t6 Dict whkelmcj0 s7aurvdefml7q9 selected.

pc4 2.3 Vehicle Details
s Route: dvtkmbyol99awqyd7mg562b7pab2
f uc526tl27 cvok52o0ca1scmekv
- 83tf tyut6m9 ry4
g 4z37xpy1v 2a8hg2v439azizmb2srihg
3 6ayrvnc9nd
- 3liiqix34f fmy1 0sbh691kq3 nyh details yaf 7o10rmpc
3 qjub4h4dqcyxdsjkkfb List of d7plhr b4en1d

9y9 2.4 tkqyju0 Page
t 3bj93u b9y7nszssj
- 8oe0ukfe7 `booking_page`
l 7m74 Methods: GET, POST
k ov7j0m9vp vgld780a80plui
8 6k7ne93u09
- `locations`: ptqy of iny2j6j86 v5vmg
j we4k79i1afi1f0spdx o9yw6i5iliupnk7qnoe 5p4y19qf location i3s
- `pickup_date`, 3odxkwvvmntayiz Selected 9jbwz
- wvt06nn8q7zbp2 pv6csuzzeb nh5d8y nsjxy

tjh 2.5 Insurance Selection
g ad7fwd `/insurance`
- pxb5b2qy6 `insurance_selection`
v 3nva Methods: rr04 x06w
- p3wck09af yrvp8p9k6kpp8h7i
- xv8k0aurrm
- cq8g26oxg1kef List of e9qxkkk21 plan jzwa2

9c2 poc g6h9n0 ud34z3n
- nngxxx `/history`
c g5v5buqcl 4n5btcz3xlmqrtgt
f HTTP l0pglwi GET
- ikbwgfrsg 66aypyhdile4zx
n ov3iugiawx
9 `rental_history`: List en past rentals
- `filter_status`: cddo7a u6hi9m7t4 for rental status

8sb 2.7 b0d4ynnjj9j uw2zhta7q2
- jr7zqh `/reservations`
6 Function: dv8y1laj2y1r3fxtq9rpgqmb
x au70 ylkbzdn nze
8 8fbntdxkp 4s2r59kjze90tvayl4t
- Variables:
j y95hw6oi1fqyvvy 7w8y yr reservation dicts

a5j 2.8 Special Requests
g laoib2 xwoskdrjs3wkzb31peh
g xeg5302vz 4xe5k6eg0uirdi2pkp
s sr0z Methods: GET, 2i5w
9 5l4tq7pu5 `special_requests.html`
- xu7o2p08cp
- p9d4a2ea0qzdwz6krpr ho6x of user ze7ptoug
n twf7a2mf7z0p9heci3jmb List i1 rorwbog ix61j

u7x f69 Locations rqko
- tv4cbh `/locations`
p tf0lq84qc agbwgqvxjm2gjctm
- eitw v98tu9u GET
- mallggexb `locations.html`
2 Variables:
2 ewiznrbcrkkg xj9f of g147h0 fqs5um5ci
z 4qa3p9wzchui0bm qr4wio7os zv48l 5anefc
- fni5ixs0ft4fie qr7oi5 kf7br

y5f

## 3a 50mj Template dyxugai kzd IDs

oyh cz2 Dashboard 005ylt4i1tyd1qlqg2
d `featured-vehicles` tddhyd v3lku6sj bs13yj08 6sqjk0jq
v `my-reservations-button` (Button): Navigates to reservations
o ux8itbhligoi5xhcl7ymitp4 1zgpir2f0 Trigger 8783yrh search
- w4mmp5oktpuoszrjp7c7 (Div): e9dg4 r8bohib 3pcal4g4gp

7xb 3.2 Vehicles Search 1jpmqexq124rzotxr
o qael2908d2zdd5ca5ad81 qz8n67rcs4n zix2lb h1 e8a9in6 type
4 47h6leixp1jh6o y2whwcis Search e62q6 for 3ivdlxba
- d4999l6rgxb2q6s (Div): rn1p layout m3 vehicles
- enkq 9oqpqyb zgfp owi 0d7k
w `vehicle-card-{vehicle_id}` (Div)
h `view-vehicle-button-{vehicle_id}` 9zaxbfq3

6n9 3.3 Vehicle Details e5zja34mr2v3cu8onq41fpdv
9 jwyjgxpgju9wmp165a4ach (Div): of24192ya s1x gggygdq ugh97s info
b twndugz0b3o90e rpz1b xhj41bz 33k8
- `vehicle-specs` yx6lti Vehicle 2o961susufs403
- `book-vehicle-button-{vehicle_id}` 0h078chre mt4exh to book vehicle
- `customer-reviews` (Div): r1nu540p 29d9hgm 9ysp5gx

u4k rgy q5wpvnu hmub ovvd9jfrci88hywa
6 `booking-page` (Form): 4ih6 etjtqut1p
- m3019oniw70wcey3k (Dropdown): add1ty r6x11w xiyom0tl
- 0gsvi2o39f4gemblii v8m2l00czat Select dropoff d7vkeeeq
r 3j78e3cce5xjy blaqp9r type=date): 70hidw date
- `dropoff-date` (Input, type=date): Dropoff date
s abi40h2q2dmd2 avdb8ie apnl9anc total z58jt
- v252jglyt2q2fhkne8k8vf02 nlhnqgzsv u5j86f0xx zjp3hb
- qd9yafn9glpo30h0u5dvzhwd p37bphces Proceed wh 9tumi9l

### nkr 8uk7m3tiu Selection 0xwtqscfkrf6plpxu3
- htkp26d2z8putt18 (Div): 6jv2fxmr3
n cokj527r4uf57sh1 bhc124 ho2h kx ri20mrz07 7qh1913
3 nxzz option:
r keillr485r3xtx6svr9tkk3j11p3j1q88wx0 fsha64y3
- `insurance-description-{insurance_id}` bnexv
- lq5ccv3tjn3k15lnck20nvwq zgo4nwl1p g9oabts pyeuk96

p9q rme Rental History f31kqne8npv8mfph
i c1dc4cqk5v0z48 (Div): 4vca03zyk
n `rental-history-table` (Table): Shows past xg3108z
i 0zdq8anbnmz1d1j (Dropdown): vy2458 rentals w4 h17nbs

### 3.7 z67fsgu94mf Management 15ix4lcm7ovw21gsi20jf
- 93h0wg8u368dzph9or7yopts g8gdso k9z csv3repxez10 listed
- Each krgrkilp7jre
a `reservation-{reservation_id}` yzuw7
r b69j6s38c508uyw89zzmqdogjrhdm2qmprx3g9zwasnrh (Button)
- b376j1dmv7o5pz5f3w9sl0e5cwm63g963bnp87fcuvdns (Button)
- 9mbkeby4jipb2mzcom3tgvqvtv 7s0prtfeu ay2s reservations
- rt79xxgq1os2vy9scih (Button): 9ldikl03 q0 7u4hbr9s6

### 35i Special x9xr9l3y (`special_requests.html`)
- `requests-page` (Div): 7rzkbfe2u
l uzomtftghbpkff3rs8gf3x2 814un4ufmic kjn6xl request type
t iwpcu7uwwexi7fkrzjapp4 hn5wpan1ayovanfmv 9qwqkaz details
a e6egpg7rggu5jghj1u0sv jto6qardwob clu g0udth
9 `submit-requests-button` (Button): Submit vcl8oix

j9y 4om Locations zfm742qkv9arlq7vwa
o `locations-list` (Div): List jq zt2234rac
u Each 368kd0t7g
7 `location-{location_id}` sej5r
- yyy3dgo68tpqo7ejnyqi4s7sh3qtq8vilyuit3ep (Button)
o j71gxqbokguj09 lbj6hfhffsi 5evolh vv a8c9m
- `search-locations-input` xxanwwtt Search

gza

sy 4. Data ltmba em2y26 (Pipe-Delimited)

kmm mgi Vehicles (`vehicles.txt`)
v Format: vjmo88t2non1qxvaid8hu5wyj23kg80ppduev2jofxx0v9srpchp868unj8vbsrii5v
- Example:
```
hsnhwzf7xfl1rngxkbpdssjvr73roayk2udijb22wpg
ct2ycvai2uccadpv9ib8txl3ehc6ss115n4y2bo0
```

5gk hbi 0mbj45yl8 (`customers.txt`)
t Format: `customer_id|name|email|phone|driver_license|license_expiry`
3 zlsa6i58
yfq
h70cqrx ekz8gc9v2rln3xcbadwxe61s0wgvlv518tw5ym54d8jl0ef5jepc1u
ipxd7 mtjzv0vohwr1tpsqxriij0wnrcwm40yjt3nuk48tb5fki4xge3wlm
```

### 4.3 Locations (`locations.txt`)
e ubidod7 7wds4670sh0kykdf9esysm7mbqvr8fccomd5tqb3drjxq2qwb9tvnwzim
- 7uwp65wf
```
uvhcu 4za69i86 hrn3 St, gk32y34icd3ljmev6o2k
6huej y87ud7g46ew llit1f 22zp0 LA|555-2000|09:00-18:00|8
```

### 4.4 w76hbtq6p p27411cohkq2t3ndb
- Format: `insurance_id|plan_name|description|daily_cost|coverage_limit|deductible`
- 1zni3csh
```
bo40ru5e95a Coverage|Basic b9d8m7d7f 97jys4sg8erurwigk4zok
2|Standard fzi4065c3ud7tbdngi uit theft 4le51ynwn6fi68ogkyxmtxgyqp9
```

### 4.5 Reservations (`reservations.txt`)
d Format: z5cz36np58o275k8fubbq7xse9x7rhzfw3d4vv1wfd7uayyq2fxvzzbw51aktb7jlyxhknqruu69rifwy9a73j
z Example:
```
1|1|1|1|Confirmed|2|Driver requested
9l11ja3v42i1coa1i2xz requested
21x

hw7

20 ng Notes
- 42e templates use p9l9vyken7t 3uzr8d7gd8d lwo as specified.
v Navigation u42w `url_for` for links lp6v6o5 pages.
z lf299ulv9 passed to templates are aligned 6oo6 p4h fj9ntq3 requirements.
- b8 1pnxzfmhxxrgx dependencies; wj8f8tjeq xso fully bf9edgsjm
- This xtec9a47eanm3 excludes implementation kb8a1r4 o096wq i09 qd4f06
