# AGENT.md

# CCTV Stream Discovery Project

## Project Overview

Project ini merupakan bagian dari proses pembelajaran mengenai mekanisme streaming video yang digunakan pada website CCTV berbasis web.

Tujuan project **bukan** melakukan eksploitasi ataupun bypass keamanan.

Fokus project adalah memahami bagaimana sebuah website CCTV mengambil stream video, menemukan endpoint stream, kemudian mengolah informasi tersebut menjadi data yang dapat digunakan oleh aplikasi lain.

Project ini dikerjakan secara bertahap (milestone based).

AI harus memahami bahwa setiap milestone memiliki tujuan yang berbeda.

Jangan melompati milestone.

---

# Current Milestone

Saat ini project berada pada:

> **Milestone 1 — Stream Discovery**

Target milestone ini adalah menemukan informasi stream dari sebuah halaman CCTV.

Output akhirnya berupa JSON.

Belum ada player.

Belum ada proxy.

Belum ada websocket client.

Belum ada Flask ataupun FastAPI.

Fokus hanya discovery.

---

# Final Goal of Milestone 1

Dari sebuah URL CCTV seperti

https://stream.example.com/stream/xxxxxxxx

didapatkan output

```json
{
  "stream": {
    "uuid": "...",
    "server": "...",
    "channel": 0,
    "websocket": "wss://..."
  }
}
```

Tidak lebih.

---

# Scope

Project hanya melakukan

- mengambil HTML halaman CCTV
- membaca struktur HTML
- mengambil informasi stream
- membangun URL websocket
- menyimpan hasil dalam JSON

Project TIDAK melakukan

- membuka websocket
- memainkan video
- decode MSE
- bypass keamanan
- reverse engineering JavaScript secara penuh

Semua itu merupakan milestone berikutnya.

---

# Background

Website CCTV ini menggunakan arsitektur:

Browser

↓

HTML Page

↓

JavaScript

↓

WebSocket

↓

MediaSource API

↓

Video

Berbeda dengan project sebelumnya yang menggunakan HLS (.m3u8).

Project sebelumnya menggunakan:

Player

↓

Playlist (.m3u8)

↓

Segment (.ts/.jpg)

↓

AES Key

↓

Video

Sedangkan project sekarang menggunakan

Player

↓

JavaScript

↓

WebSocket

↓

Binary MP4 Fragment

↓

MediaSource

↓

Video

Karena itu seluruh parser HLS tidak boleh digunakan lagi.

---

# Architecture

Project dibagi menjadi beberapa modul.

```
stream-scraper/

main.py

config.py

scraper/

    __init__.py

    extractor.py

    parser.py

    models.py

    utils.py

output/

    stream.json

AGENT.md
```

---

# Responsibility

## main.py

Entry point project.

Flow:

Download HTML

↓

Parse HTML

↓

Generate websocket URL

↓

Save JSON

Tidak boleh berisi regex.

Tidak boleh berisi BeautifulSoup.

Tidak boleh berisi logic parsing.

Semua logic berada di folder scraper.

---

## config.py

Berisi konfigurasi project.

Misalnya

- TARGET_URL
- CHANNEL
- OUTPUT_FILE
- TIMEOUT

Tidak boleh berisi logic.

---

## scraper/models.py

Berisi model data.

Gunakan dataclass.

Contoh

```python
StreamInfo
```

---

## scraper/utils.py

Utility umum.

Contoh

download_html()

save_json()

logging()

Tidak boleh parsing.

---

## scraper/extractor.py

Module ini bertugas mengambil informasi dari HTML.

Tidak membangun websocket.

Tidak menghasilkan JSON.

Hanya mengambil data mentah.

Contoh

extract_uuid()

extract_server()

extract_title()

extract_iframe()

extract_metadata()

Jika suatu website berubah, cukup ubah extractor.

---

## scraper/parser.py

Parser bertugas mengubah hasil extractor menjadi object StreamInfo.

Parser membangun URL websocket.

Contoh

server

-

uuid

↓

wss://server/stream/{uuid}/channel/0/mse?uuid=...

Parser adalah satu-satunya tempat yang mengetahui format URL websocket.

---

# Expected Flow

```
Target URL

↓

download_html()

↓

BeautifulSoup

↓

extract_uuid()

↓

extract_server()

↓

build websocket url

↓

StreamInfo

↓

stream.json
```

---

# Extraction Strategy

Prioritas pencarian data adalah

1.

```
<input id="uuid">
```

2.

```
<input id="server">
```

3.

```
data-uuid
```

4.

```
data-server
```

5.

script inline

6.

regex

AI tidak boleh langsung menggunakan regex jika HTML sudah memiliki elemen yang jelas.

BeautifulSoup lebih diprioritaskan.

---

# Output

Output wajib berbentuk

```json
{
  "stream": {
    "uuid": "...",
    "server": "...",
    "channel": 0,
    "websocket": "wss://..."
  }
}
```

Jangan menambah field lain tanpa alasan.

---

# Coding Style

Gunakan

- Python 3.12+
- Type Hint
- Dataclass
- Fungsi kecil
- Modular
- Single Responsibility Principle

Hindari

- script panjang
- global variable berlebihan
- nested if berlebihan
- regex kompleks bila BeautifulSoup cukup

---

# Error Handling

Gunakan exception yang jelas.

Misalnya

```
UUIDNotFoundError

ServerNotFoundError

StreamNotFoundError
```

Jangan menggunakan

```
raise Exception(...)
```

---

# Current Website Pattern

Website target memiliki struktur seperti berikut

```html
<input id="uuid" value="0196ae81-..." />

<input id="server" value="stream.example.com" />
```

Kemudian JavaScript membangun websocket

```
wss://stream.example.com/stream/{uuid}/channel/0/mse?uuid={uuid}&channel=0
```

Project cukup menemukan dua nilai tersebut.

Tidak perlu menjalankan JavaScript.

---

# Important Notes

Project ini adalah project pembelajaran.

Fokus utama adalah memahami mekanisme stream discovery.

AI harus selalu mengutamakan solusi yang

- sederhana
- modular
- mudah dibaca
- mudah dikembangkan

daripada solusi yang terlalu kompleks.

---

# Future Milestones

Milestone 1 ✅

Discovery

- download HTML
- extract uuid
- extract server
- generate websocket
- output JSON

Milestone 2

Verification

- koneksi websocket
- memastikan stream aktif
- membaca codec

Milestone 3

Player

- MediaSource API
- appendBuffer()
- render video

Milestone 4

Backend API

- Flask
- endpoint JSON
- multiple camera support

Milestone 5

Dashboard

- daftar CCTV
- stream selector
- monitoring
- logging

---

# AI Behaviour

Saat memberikan solusi:

- jangan mengubah struktur project tanpa alasan.
- jangan memindahkan logic antar file jika tidak diperlukan.
- jangan membuat implementasi yang jauh dari milestone saat ini.
- selalu prioritaskan modularitas.
- jika ada perubahan arsitektur, jelaskan alasannya terlebih dahulu.
- jangan menambahkan dependency baru kecuali benar-benar diperlukan.

AI harus selalu menganggap project ini sebagai fondasi untuk milestone berikutnya, sehingga setiap perubahan harus mempertimbangkan kemudahan pengembangan di masa depan.
