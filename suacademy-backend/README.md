
# 🧠 SU Academy Backend

> Bir kuni bir backend developer bor edi..
> U `DEBUG=True` bilan production’ga chiqib yubordi…  
> Mana shu repo o‘sha xatolardan keyin tug‘ilgan 😄

![Backend Life](https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif)

---

## 🧩 Bu repo nima qiladi?

Bu — **SU Academy** platformasining backend qismi.  
U quyidagi vazifalarni bajaradi:

- 👤 User authentication (login, register, verify)
- 🌍 Multi-language support (🇺🇿 Uzbek, 🇯🇵 Japanese)
- 📊 Admin panel (Jazzmin bilan chiroyli)
- 🔐 Xavfsiz API (token based)
- 🧪 Xatolarga chidamli (deyarli 😅)

---

## 🛠 Texnologiyalar

- 🐍 Python
- 🌐 Django & DRF
- 🎨 Jazzmin (admin panel)
- 🌍 i18n / l10n
- 🗂 PostgreSQL (prod)
- 🧪 SQLite (dev)

---

## 🚀 Ishga tushirish

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# suacademy-backend
