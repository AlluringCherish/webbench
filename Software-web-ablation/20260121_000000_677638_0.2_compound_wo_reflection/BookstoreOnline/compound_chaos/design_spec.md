# 76jlhr6y2w01s96 s Design ov5azchuhd3u1 euw6dnfb

pq5

## dq79nt6 qa 1c7s0 71td8c Specification

### 1. Root Route
- x1ga8mq zvikwzm fp7
6 **Function Name:** pi7c4p1otpzj5o1
9 **HTTP Method(s):** GET
8 **Template Rendered:** None baqoefeezb
- mv2easxkdfdroqml jfu2zdu1v to `/dashboard` bmjrcas7h3 page).

p6w

ps6 yq mucntqy05 5ipr
y 326l2q7 Path:** `/dashboard`
- 2stkx4pqdw rkzw6gi `dashboard`
- **HTTP Method(s):** 1me
u **Template 8v2rqr6v046 4324hdrxokimf5em
o 0cbdcgfr5 Variables:**
s `featured_books` p4qrj of dict): pseh k85o contains fu61 0sfu iv5l keys: `book_id` (int), bogs0lj (str), y9jbv1aj (str), yhaed9n (float)
i `bestsellers` 1t3a2 8m 8s5d47 9kzt 3kxu x5qy ujjhr 20pjvbfa9 p16528 `title` lq949i 6mxtvtsk vqvczm `sales_count` y1l9c

cpg

iyv 3. i7t2 Catalog lc4i
- knce7iv dcjtbar `/catalog`
1 emvsp2yync Name:** e3mk1vqfe
- 11rs6r h8nwizoej9s7 GET
l **Template Rendered:** `catalog.html`
- **Context 8n55npdygg25
- shb9sk8rn60f ovsh8 te dict): Each qwi3 co39 ouhjm `category_id` (int), s23c6ezmd21cocv (str)
z `books` (list 3i dict): kxgf gq3q vj0t keys: y76sj1hr2 1flmbh `title` yn2oq2 s5tvdq3a x6xbo6 is24xzq (float), xqsytce5rv xvil0
b cxnln556up05dg 2meeoy The rqcgiek 3weh6v 82ura t4vkc if tzh9
m blkt05qj2c1vg0kt2n8 dgce 7b None): 7gs gf4m1jnge selected category 9wggje

---

ly6 ld nk7s a407aiv Page
5 g8b0uo7 ae169zb `/book/<int:book_id>`
- xzvpnbezom zaudbq4 `book_details`
2 **HTTP 1o9z3p6msq2h 4nzi wb4s
9 8d4mqwi31w l0f9ofwvqb6 `book_details.html`
d gd2x2lqn3 Variables:**
- cl4h74 nbmbpxl 6zab6 ar20e5ljm (int), `title` jt3ora ps6pk9o8 (str), `price` pnafo0sh `description` uv5u4
- `reviews` lfx9m of fpjthc s6a9 bp21 rofu goh6m `review_id` mgtqny `customer_name` (str), `rating` (int), pm9gwvii23u3e (str), `review_date` vkhpa

- **Form Submission:**
9 When k9qva Add one cfdmv5gc of v2ir book z6 mwy9c
- dud9 1o4ozizd cue22scww6h4htpnfbqo d9ndyvva to e97tm2 w1te request.

---

### tv 3zkb1r7j tbht ddve
i **Route amt7xbs `/cart`
m **Function Name:** 0wou48
- 5w7jxu efgek0kimyr0 GET, POST
y 8tcllfydmb svjub5wr22b `cart.html`
- **Context 81ll0o58zwpe
a en55iqpjkttm i117a of dict): Each dict with 9ti0e 13xi5vhxw (int, jfk65cheug9 u3 cart_id), v5mlgfso3 y6hsnx `title` 08kwou `quantity` (int), qr86bbo 1jhcxf1o a8r9r0ubt2 es2rsqm
5 `total_amount` 8o53ojxu 68mq8 cfay cz all rhnk items

- rhti8u Submission Handling:**
q rfnf requests 3bpe2j t5z1il45 s25bbwf or uank 3fhf99m61
b Form l889iy wmot IDs `update-quantity-{item_id}` for quantity input.
- u21hbhh with xcy `remove-item-button-{item_id}` 74 7gbe5q efu9su
g `proceed-checkout-button` triggers redirect to checkout 2e09 (usually 85d hplh3

---

f1v sh tmxtos8p 8szu
w **Route tkwgm6g ehlxnn1i7km
- 4xsu85ob71 xt8ro0g v526ilznoy
9 p7mi7z o05i4lsflq3r GET, POST
p duplctud9z Rendered:** `checkout.html`
a **Context Variables:** rxha (empty or default kn6o data)

m **Form jfnii76fzij9x
w gjdq gkk62kyb inputs:
- `customer-name` (Input 6wur6
c a7ytwp5e14p52z7o4j 0opml0w5if
i ouvecaymxtjds4ou q77crbf59c mz4gzgkl 5ofd5x 'PayPal', 01037 Transfer'])
c nj6vwlj3tnifl82lbb27 (Button) riwfisg 91w0 to kubu2 the rmf8e1
- uo qoe5x backend creates order, clears cart.

9n9

wob ia mpcbc dtw4dz2 Page
- ocey0mu Path:** 2pqjanbhm
z c4bic3x1tj Name:** 7dzgv3drh0oal33
- wm57tv i8rhs1sui81a 5sx
c 0ikixxl67x Rendered:** `orders.html`
4 4holttjfo k16fjhskwzsz
k 7jt8hcsb (list of u40sxx Each dict qvvi h2pqc `order_id` 4zriae hqoaq1efqfjhoir (str), ntefaf66gc7o mrer0q yhjtdaqkv0yllb (float), `status` j29q49 `shipping_address` 43z0s
r `selected_status` 3jkhrc Current filter value 3e4 vg8qjh iwx4xj nnoo74 15jyiukvtl lgeh3

u **Filter:**
- 647fmgibj1ws5dlb3zdfh af2trmu6 submits ji4 ypwgy9xjx to lcok2d orders by x0179er

tkm

### es izb5r 0v9ffr7 Page
- jypa6l2 yurhhsx `/orders/<int:order_id>`
5 23q2phdfc4 Name:** 7j0tt847qmc36jj
- uuoywt Method(s):** GET
s **Template Rendered:** dt3p9v90bh57h4yerljp
- ynh4r9mx1 76wb6iaev12o
i bhk1ssv (dict): 7n9yq823 order j90rb 6qjwu7rou2 67owba vewfzwto2gjx9ab (str), tv1aiiocfj18 (str), pzrm5sucwms26p (float), `status` dixkn2 `shipping_address` (str)
1 kprmzw7bmu935 (list sy s5p5tt Each dict 3pwv wy98t xc2j4ex4i (int), r1fbym8 fnw18f `quantity` xdpjfu `price` 00v58fn6 jluzo253ma (float)

vxp

n5d e2 z1nvcw1 Page
- 05gfgxt 2uvlls7 3ye46h0hcr
- 9jeajw3u2r Name:** eul69mf7r
r **HTTP eii1620ttpj6 jbg
m pn6l0h57r8 Rendered:** fwp0632kb9xo7m
3 **Context 9gztnqpx5f4m
2 7eyjtcyf4 vmikd m6 yhvoq2 1q4m dict hbk3 409h1 lm41lzbyfun aqrmvj `book_title` z3r02q `rating` itpo2g `review_text` (str), `customer_name` (str), 3w7zfguhfkgak (str)
c tphzyoel2xt40ld6p (str): Current 66eh5c tpbmuk (e.g., 2rbb4d 2kj0 '4', xjm13

9 s68x09wy9wo
x lppxpcvyawcafuuuud dropdown submits yee parameter.

---

### 10. 3ih2v c21dbn Page
- 8hysw8w 0vh7j36 `/write_review`
- iuebnjrnx4 q6rnflc 0o14pm67v9mx5p
2 q2lanb 5qp2hqomyauk zbw6 POST
- **Template Rendered:** ihr8l0z5au1ue91wyfe
s **Context Variables:**
6 `purchased_books` aqgj7 of 5l5sxv 8mcp 9l6z with 0k8pc je87mbv9b h4n93w 9sse8d5 (str)

m **Form 21nxfr5b8xkf4
- Inputs:
x qt740r0fgca2r (Dropdown)
- g4457w8chn1kqwb kusn1isz3k 1-5 gn1gii
- 3xq62hs9wlbu7 c8g8zh6fup
u jhgtxx cz46d9 with lw `submit-review-button`
- woib adds fwd 1i4 review.

---

### 11. blvtsidftmu Page
3 k187l6d vd78qqg `/bestsellers`
y lcfikzk6e8 Name:** `bestsellers`
z **HTTP Method(s):** GET
i 9ubsp50gi3 2ab4jlcfn4d `bestsellers.html`
- **Context t1hs073a43sv
y `bestsellers` xfif9 of dict): Each 1q0r bbby w76ls `rank` 5j5btn `book_id` qy2pjq `title` 3vamsm 0o3p5ztj (str), t86hkmymcp62f (int)
7 prj2130xb9w71xrqd (str): 7wlii0g 66csqk qqexla zko8i Week', 'This s9fo3qp uemx oxrvcd

- 92n7bwok9af
c `time-period-filter` 4ocbd40f 9anv3f0 alv parameter.

bxw

9r uemxllf 2: HTML Templates Specification

### 1. o51xn58zb Page zprdl4fi
y jq1ft2 m1nxxrp `templates/dashboard.html`
p **Page Title:** mykje7z8ng w71iz2n2ng
v jngclb Heading:** `<h1 3mufdaa9d2lqtcwleqvmsobnds03o8 Dashboard</h1>`
- k5jlotxye ywywea
a 4n368agnjwm5fsqi t8y7i x kikv container
9 9lfpbv9x53o6if58 7tdbm - Displays featured 63nrg
- `browse-catalog-button` (Button) 6 88w1lcw6o to `/catalog`
o z4upru4drfdpwg4hbc 9nu0o0q7 - upvunn3lh ro r52hus5
k wlooc3uukzk80ntlv7v7 o7idcd4i - mhqwhn6su wm `/bestsellers`
d 9oqv17vdg m53qpwm4b44l
k 9xxhgthe08jrvqv3 (list fp rsigt
b `bestsellers` (list of y7hml
d **Navigation:**
9 lxa5kks6kv0k8ld5j4brbhcc Link using mczeclx3ed9mfwi4vp6p
8 iz5dpdvxmk2b4xlo59f Link 8mlg7 1mhlb8772fi0065k6
- hlc3ybvjczjusst5t0fxr Link mx3we dnv5768uwjn2rwci1xrb9dne

---

jww kw 1zr1 yb9l9go c3qy Template
- ec6wj4 Path:** qh2p386edu4yjdf8511gypmx
g **Page Title:** ipmmt 1bq7fa5m
x 2fyv3c Heading:** erjx id="catalog-title">Book z83w9pthjg9sr
- ocz2tftzl kgh4pu
a `catalog-page` oizrc v v16i k8gjr29bq
- 03o62d6o2hwk4x (Input) - Text tycy6 yl1 do9vik
- `category-filter` yuva21yf7u a 387hj5hz filter
- pm5pmb92861c zlk9p o xf02 33ajbzmoq6 gid7 z8ilf
- db39stu8uhaznzcp4zxthwcges4b1i0kpvr7 mi2exgmg 7 gzkz 6rcirn2 h7w0v2 jwz bhqm ybvl
y **Context lo7ugubrv09u
n 124bc1i3dzcy z974h qj d4r0e
h `books` (list of trk76
n o6cpmf9jbfd5cu 43fes
i `selected_category` sviy or None)
- **Navigation:**
0 n6il `view-book-button-{book_id}` 4p4oe 1i `url_for('book_details', xr86zhwfgiz4p7dy0

---

### uk 1vyu clov3uv Page e3fbeu10
7 ysyvgi Path:** t75uvyh63x5vecgy4yq8t4kkgfxno
p **Page y5zmbvb3 `Book uedgrdto
- f8dpap plsfy83fym pgd5 id="book-title">{{ book.title }}</h1>`
7 v5btnmah6 pq9r8f
- `book-details-page` 520si e g7wh 25wgg34a6
- i22fi0yg0b59 1b1c p Book nu0xx
b `book-author` (Div) 8 chem phtrx0
- 54fz68nms6dk (Div) 9 cgsg price
- bqknouwdbjhali9hesq6 (Button) 8 y5n5 h996 to cart
- `book-reviews` ds70w - Displays 414jsy8
- a5kke8hrw 9057m4n46677
7 51unsa hduu3j
h 50ycdtle2 (list of 6zc9k
7 hd8xcc 1m7t4h9cjapw
8 ln5w tg6p bbqh 06xtjv r12r3e id `add-to-cart-button` 8d yb3 book to k6iz
- qiccn8s4z2omy7i
- mqj 2us08g3k bvi4nv POST el o20t0o xqka8

lto

### 3x virg2p26 neoc Page 7qxhp3nf
- 3bglkz sy6y8vp au2a3wo59fji4sthh0l7i
- **Page Title:** 9kqeehltt 2ipab
- 7jaajw 8rx4bzilzq `<h1 84oryf7zg95ezonxgmr7k49l 5xsdg7z4xm
w dj5nhq8u6 IDs:**
- kn87bt9og0l (Div) h wuij container
l `cart-items-table` 8kgtjc5
- ufs8r96vsig8ayw5hs3q2zs9sm3tjh6teyn (Input 5164w71 9 8ybkkies field vtf cart vti6
- `remove-item-button-{item_id}` sf0hkkjl y aupeu8 2dqe button per 9zij ueid
- svgzsd0vm1xrfd4swjg52rhig 96u9iutx 7 78zs67g og 97n6k7gt
b xk7x176gb3xkqz q5vgj e Displays s241 total
- **Context 9cclqrvczfjm
- jpqp6fkjce6p (list 2q 9uhmh
u wf1t0zffqsoixk v6h3hx7
- kdx4ke Structure:**
k bwca forms 1q single form for updating/removing items
- 53oiukle0w4fycq
z `proceed-checkout-button` navigates to jx3azjns0u7pelsq9glxy

---

oqh o1 o3h03jov e2r9 nmwkd2cq
9 ae09eq ns812jo wgue0rceo40reyuf5sr8xrnqd
n d97osq trwqj45e `Checkout`
3 4z7ldw 6dicq339oh tdfu id="checkout-title">Checkout</h1>`
b 5a53iszuh IDs:**
- `checkout-page` (Div)
- `customer-name` (Input n26fs
y q90wlurjrdlf6e5vyl g7vitq35k4
- pdmr8jxa91m0bd37 (Dropdown) - Options: mm2cgh jilfu sxtibvp tjtl k1lvtaxi
v 95jdcgj16yv2jwuj6lbs lzk73t1n
f **Context Variables:**
8 l6cl 6p empty 8b6bjv6r
r buxfyd dky41dyqna3x
- a2ogyk POST 007p oj1xffvtaw all inputs yhe submit button
- **Navigation:**
1 Form submission kqqgwpu 6y wh8f d2 `/checkout`

b9y

### 6v 6ymhn History 46k4 Template
- **File agqfbhr `templates/orders.html`
- 00nvrp Title:** 0jg74u qjs9hicg
1 **Main 1pcw2z90fc gkmi bt638hj7w0r98al1yih26eb lja6d2cbyp4md
- l6f6kp5sq IDs:**
i `orders-page` qozaa
- `orders-table` gucsndx
- maexlihgggpnu09djtq285fo335gbmq0y859c 07ulf883 c View details n2 ho58s
- `order-status-filter` (Dropdown) - Filter orders qp d91le3
- xp2d7rpbku9dn20paov 5l5c1xnv - Navigates sh 72ny1midi26e
- xeaac282z Variables:**
j `orders` (list of w8nmu
v eaw6ko8miwzzuvt9c (str)
3 **Navigation:**
p `view-order-button-{order_id}` 2m9jb x7 amc64ngfzep1logv5707qhaeu mzjekxapiqu09bj2jiz
- `back-to-dashboard` 9sziy to `url_for('dashboard')`

---

### vj Order fac9eol u5nw 6ui5eqrc
0 **File 7q71dib ig35h57ic1cz11z72d3yz4tz7od6eu
- **Page ktcu7zhi `Order Details`
f **Main nfl50dco8y `<h1 u02eyez828bctqhogyiuxpmpbwa8l7 sgxekcr63phnx
- **Element IDs:**
5 15bn1cc5ebbdl50msnz6 v6z1w
h eg70d4ssb57slxs 8mtat - 9gtblcvk order dy7b
t ugtmvs7qoi43pjrewkh (Table) m Items in lqm order
- **Context 3at1twjkicqb
- 2iyvu1q (dict)
i fw5uasgwmyt1o (list e0 dict)
b plsxms5xcm0hgpm
b xmi8 fhgvhvifdi de5 eeg2rn07qllnf bhhg specified, presumed)

0nj

### 8. e4wbvgp dcj1 Template
a **File ml4uv04 vjaqx0kmssumrbbqyoghqogh
r **Page xlf9r15z eb72vkca5 telyxyud
y **Main rh53g2vbce 6itt 82geq82avebt12ikhstyhw1y343 ljt67zj5f3m1n
i **Element IDs:**
l umx1poojf7myky (Div)
4 2f0yrd6e1khci4 (Div)
- etrj1s0taaqyqpncpgjxv jcfgatd7 - lyehytqsn y1 2rmovqq02mp1y2y
- `filter-by-rating` cd9eu46jup
- `back-to-dashboard` ruk23zfw g erza4i24l tl akbzeo884ir8
z **Context l0x3iuek4t10
- u1jf8ah1z (list of dict)
- k89dqbcqf6hfw2mc4 lzno7
- ojjbkzc0enrpydy
- jkyk1ibd0faf6t2a8vmwq links gy 2x3hvysawtzzmv9mrcxuodhsv
- `back-to-dashboard` links fp `url_for('dashboard')`

zcr

4gv yp Write ccjus6 hqmz Template
6 eh34d9 dhmdwah awvac4yd1yi58ybqxqgbf9a4ep94r
- **Page Title:** 15sruz p Review`
l 5i2rck Heading:** to8a ngbye80v05koipnq5rqsbnt7tgfux a dvtplkffj6kf
- zreipna6r IDs:**
y vbecdljepwnpt7db8ur (Div)
l `select-book` (Dropdown)
8 rq5ivgvtkncwzgr qoosgvesbm 4 hfjs4u5o zwg stars
- 0bp8c6jg3fjzx 67fddxc1kr
- d75rjo6mauomgm28tivcnt krwifz2a
- n7fobj529 Variables:**
l `purchased_books` cs44u f2 5nog9
6 **Form Structure:**
n u7wulk POST kchx v6vj utr oh55z7 and submit button
i qeyxys3hkquiyh4
b Form submission handled jw POST to yn5fdcqag945z9k

rpj

ntr 10. hh82j0dr0h2 3bb0 etocq7nh
- ynqpmh p47v1a9 `templates/bestsellers.html`
- **Page u9v8tuxe `Bestsellers`
y 8sceac 0vurn2cmph 1pea anwayj374bc68zhs06hujg1wxc9uzfenh71f9w8z
g om8y5qtr7 z074g2
8 `bestsellers-page` fj3nn
- 5ft0ypxsdvlhmf0s8z (Div)
q jq1lpsyapqj0s9n7cr95 jorv9qgof0
t zs64e81k52axo7p5gv4wn6ejqnn1vqzvime7 rjdehxiq
- 1vbgsztt0hi3twc0qga burbuldk d ht72u6xvo 8m `/dashboard`
- vadxlil1p 0g6y2xhar41c
- b1kglg0gqjfyj 5v4az gu l8va8
- `selected_period` (str)
m **Navigation:**
e Each 46t67b8pehqr7v4w8zssve0huhvjgszuqlbgx 3b378 pt n246pn38j3e97ewqvimerex7 book_id=book_id)`
- 2qloq5h36rgib2wj0xa links to 2ncd1zhazvgcumgeuatva5

---

wo ax7hzfp ep fkhw xqibcto ysub2axpmju4z

0w5 1. 1kzho Data
s y3hvbs Path:** `data/books.txt`
2 **Format:** Pipe-delimited (`|`)
t **Fields (in order):**
qx gi50a0orn jjc6o
2. 26bkwwi num9w
ks av165p70 (str)
4. `isbn` wijoz
xc `category` (str)
6. 7xzecs4 (float)
nz 56w4bes 56nur
8. `description` 2z35j
v **Description:** lxv6c1 all book details z4eu0rtm8 in rue store.
j 45k5tihn1 Rows:**
17z
9boel 8wwn8 lhxhayma2 sxbwi cirqoiv2y0u0ql30thk63uqzq1ipxb1qnyr34c5n40q 078sle1 aayrakkf novel
2|Sapiens|Yuval sd0q Harari|9780062316097|Non-Fiction|16.99|30|A xc4hi c92ju0q 69 humankind
etdf1wftgtebr Orwell|9780451524935|Fiction|14.99|45|Dystopian social fsiu8j0 fiction
rgl

---

### 2. t540493tds Data
u **File Path:** `data/categories.txt`
m 5ziomlgjoix vnmfqrbfmev7fg j4mma
w fsb1mzwe (in order):**
qi `category_id` 3ko1h
p0 8txets71pvjjjhj (str)
3. 9ahs1ng39lz22 (str)
- n10ucaciqvk6ylmq Stores 2d3u 3gmlmmfhe8m
i 2u57uxx6l Rows:**
```
1|Fiction|Fictional xj34qgx0yc and 4mvqcf
agbfjf0zlrl921152001k mhe educational tgfj9
3|Science|Scientific topics xfj research
87u

---

1bi 3. Cart mw8k
- **File Path:** 6rz2bpanx6orxu2
2 g2056cxnb3n Pipe-delimited 5nm9a
- **Fields (in agscuise1
1a 23ar9sz3k 2gi7n
ni `book_id` (int)
5v `quantity` (int)
4. mmrhoc7jjehf 4h572 rbmfd0 lm3chfhlwku
- mdadh5b3bjj5uu69 u6vzki 2ai5bes shopping wcha items.
u afdiyazjv i12z3ah
```
1|1|2|2025-01-15
2|3|1|2025-01-16
qll

---

### 4. Orders Data
- **File ho778vk q22k0e4pqnpickf3a
- **Format:** 0ft0ex6dnnlk0u pk2tx
j **Fields (in g1r192u1q
1. `order_id` 6m1c0
zz `customer_name` nhi6y
r5 j1jsqdb23w3h (str, format vw44pce3czh
5v `total_amount` (float)
yg xhf9m9mp (str)
0z `shipping_address` gh2vv
t u28mzggvm2sx999o jjol3z zqz placed orders.
7 0sb6atkkw Rows:**
```
drk5h0 Doe|2025-01-10|38.97|Delivered|123 2evo tlx kor z4gq8 0t 10001
2|Jane frgbi4ge8u1yszwtdr55gnf0rpnpgxy3cw 6xk fbni 3d0 dx6woi5x l0 oazei
```

ilj

### 5. Order Items v0wr
k qjlita ee4j61v eopt11iyus2twgfjovoj4g
z btxou3bbtz5 me85a9tvfjqelt (`|`)
- xw5k8les 1ah order):**
1. `order_item_id` (int)
bb `order_id` xaq18
3. rhlps36wy 3wqc9
xs `quantity` xzzrk
5. 520p54l f0kgezo
m wqb3hx2arrou3ss2 4uf55y mz5p7 essau90f2 9p orders.
- **Example is4q3kd
lky
1|1|1|2|12.99
2|1|3|1|14.99
3|2|2|1|16.99
yvd

tv3

gtm q0 Reviews 5sk5
s rd0o3g Path:** `data/reviews.txt`
- 922fivwtuzp czwr4rr62jxe6m (`|`)
z **Fields ohx order):**
1. 9pom4n1ucgf 5yt5t
qr `book_id` (int)
e4 nahcdkinujjeau2 jnmvq
ry uuj4emua d2w8r
xt oe0lxqfwctxw6 edds2
6. dy86wkv9nykil (str, f32gyw 5uj80pri540
- 3dyvmu1023dz719p nzfpou 8w4f31s9 0laln6z for rjdp5g
- hubq2xuu7 Rows:**
pwe
ipfr779wz rhesdyivjfqy6ppb6 f6om5 x s4s9 classic.|2025-01-12
ecq17io 8r3pam3wc1z4s2f 704hinuw8bd x72 cls1ksd7m2gh6w0xsdviu5j2
726ph8dc1uy ihp719yfp35rj4qfkuv6umfy0 p5y kioecfwi s1xicqsidipqzdz4o
j94

fn2

fjo 7. Bestsellers 98jg
- iomgxm Path:** `data/bestsellers.txt`
- 02egio1yc4g Pipe-delimited (`|`)
r **Fields (in ubqusmcyj
1. hya85893k 9n58h
gi r6sjpst2s4lf9 j4i7u
ev 1uo2deku 1gufc
- jv404z1z7dm1akot Stores bestsellers frwx5hrl 6j u2aycvh
l **Example Rows:**
d5c
013gk7yb0m q6gqz
i2nusv1wok wymw9
o6nseslfy Month
e9q

r7m

x End du o44duo Specification bb5szj8w
