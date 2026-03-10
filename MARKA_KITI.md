# TurkishSystems Marka Kiti

Bu dokuman, TurkishSystems'in dijital ve iletisim materyallerinde tutarli bir marka dili kullanilmasi icin hazirlanmistir.

## 1) Marka Ozeti
- Marka adi: `TurkishSystems`
- Konumlandirma: Kurumsal guven + muhendislik disiplini
- Marka hissi: Premium, teknik, sade, guven veren
- Ana vaat: Uzun omurlu, bakimi kolay, olceklenebilir yazilim cozumleri

## 2) Gorsel Kimlik
### Logo / Wordmark
- Wordmark kullanim formati: `{{ site.brand_name }}<em>{{ site.brand_highlight }}</em>`
- Vurgu parcasi (`brand_highlight`) italik ve altin tonda kullanilir.
- Wordmark fontu: `Playfair Display`, agirlik: `700`
- Minimum bosluk: Logonun etrafinda en az `x` (x = logodaki buyuk harf yuksekligi) bosluk birakilir.

### Yasakli Kullanimlar
- Altin vurguyu baska renkle degistirmeyin.
- Wordmark'i yatayda/solda sagda ezmeyin, oran bozmayin.
- Arka planla yetersiz kontrast olusturmayin.

## 3) Renk Paleti
Asagidaki renkler, mevcut tema degiskenlerinden alinmistir:

### Ana Renkler
- `--canvas`: `#0d0b09` (ana zemin)
- `--canvas-2`: `#131110` (ikincil zemin)
- `--canvas-3`: `#1a1714` (katmanli zemin)
- `--ink`: `#f0e8d6` (ana metin)
- `--ink-2`: `#c8bfb0` (ikincil metin)
- `--ink-3`: `#6e6458` (yardimci metin)

### Vurgu Renkleri
- `--gold`: `#c09a45` (ana vurgu)
- `--gold-lt`: `#debb72` (hover/parlak vurgu)
- `--gold-dk`: `#6b5322` (sinir/kontrast vurgu)
- `--rule`: `rgba(192,154,69,.15)`
- `--rule-lt`: `rgba(240,232,214,.06)`

### Renk Kullanim Kurallari
- CTA ve kritik aksiyonlarda `--gold` kullanin.
- Uzun metinlerde `--ink` ve `--ink-2` disina cikmayin.
- Arka plan gecislerinde yalnizca `canvas` ailesi kullanin.
- Buyuk alanlarda saf altini zemin olarak degil, vurgu olarak kullanin.

## 4) Tipografi
### Font Ailesi
- Display/Heading: `Playfair Display`
- Body: `DM Sans`
- Label/Technical: `DM Mono`

### Tipografi Hiyerarsisi
- H1/Hero: `Playfair Display`, yuksek agirlik (`700-900`), sik satir yuksekligi
- Basliklar: Serif agirlikli, premium his
- Govde metni: `DM Sans 300-400`, okunakli satir araligi (`~1.7-1.85`)
- Etiketler ve kucuk UI metinleri: `DM Mono`, buyuk harf, yuksek harf araligi

## 5) Bilesen Dili
### Butonlar
- Primary: `btn-gold`
- Secondary: `btn-ghost`
- Harf karakteri: Buyuk harf + monospace + genis tracking

### Kartlar ve Cizgiler
- Kart zeminleri `canvas-2`
- Cizgi/sinirlar `--rule` ve gerektiginde `--gold-dk`
- Hover davranisi: Minimal yukari kayma + sinir vurgusu

### Animasyon
- Icerik girisi: `fade-up`
- Grup gecisleri: `stagger`
- Animasyonlar dikkat dagitmayacak kadar sakin ve kisa olmali

## 6) Iletisim Dili
### Ses Tonu
- Teknik ama ulasilabilir
- Kendinden emin ama abartisiz
- Kisa, net, dogrudan

### Anahtar Ifadeler
- "Muhendislik disiplini"
- "Kurumsal guven standartlari"
- "Olceklenebilir sistem tasarimi"
- "Uzun omurlu yazilim mimarisi"

### Kopya Kurallari
- Jargon varsa sonuc odakli aciklama ile destekleyin.
- Bos superlatif yerine kanitli ifade kullanin (ornegin surec, test, destek).
- CTA metinleri tek eylem odakli olsun: `Teklif Al`, `Iletisime Gec`, `Detaylari Incele`.

## 7) Fotografi ve Gorsel Stil
- Koyu, dokulu, sinematik zeminler tercih edin.
- Metale/teknolojiye goze carpamayan ince referanslar kullanin.
- Asiri parlak, oyuncak/eglenceli renkli stock gorsellerden kacinin.

## 8) Dijital Uygulama Kontrol Listesi
Yayina cikmadan once:
- Renk tokenlari dogru kullanildi mi?
- Baslik/govde/etiket fontlari dogru mu?
- CTA hiyerarsisi net mi (1 primary, digerleri secondary)?
- Metin tonu marka diliyle uyumlu mu?
- Mobilde okunabilirlik ve bosluklar yeterli mi?

## 9) Kisa CSS Token Referansi
```css
:root {
  --canvas: #0d0b09;
  --canvas-2: #131110;
  --canvas-3: #1a1714;
  --ink: #f0e8d6;
  --ink-2: #c8bfb0;
  --ink-3: #6e6458;
  --gold: #c09a45;
  --gold-lt: #debb72;
  --gold-dk: #6b5322;
  --rule: rgba(192,154,69,.15);
  --rule-lt: rgba(240,232,214,.06);
}
```

---
Guncelleme notu: Bu marka kiti, `templates/main/base.jinja` icindeki aktif tasarim tokenlari baz alinarak olusturulmustur.
