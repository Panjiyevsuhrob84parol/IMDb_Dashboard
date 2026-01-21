# 🎬 IMDb Top Movies Dashboard

**Streamlit** yordamida yaratilgan interaktiv **ma’lumotlarni tahlil qilish va vizualizatsiya qilish** web-ilovasi.  
Ilova IMDb Top filmlar dataseti asosida qurilgan.

Ushbu loyiha real IMDb ma’lumotlari yordamida eng yuqori reytingli filmlarni tahlil qiladi va ularni chiroyli, tushunarli grafiklar va jadvallar orqali ko‘rsatadi.

---

## 🚀 Live Preview (Jonli ko‘rish)

👉 https://imdb-dashboard-suhrob.streamlit.app/

---

## 📊 Dataset haqida

Dataset **IMDb Top 1000 ta film** haqidagi quyidagi ma’lumotlarni o‘z ichiga oladi:

- 🎞️ Film nomi va original nomi  
- ⭐ IMDb reytingi  
- 🗳️ Ovozlar (votes) soni  
- 📅 Chiqarilgan yil va sana  
- ⏱️ Film davomiyligi (daqiqalarda)  
- 🎭 Janrlar  
- 🎬 Rejissyor(lar)  

---

## 🔍 Bajarilgan tahlillar

Ilovada quyidagi analizlar amalga oshirilgan:

### ⭐ IMDb reytinglar taqsimoti
- Filmlar reytinglari qanday taqsimlanganini ko‘rsatadi  
- Yuqori va past reytinglar zichligini tahlil qiladi  

### 📅 Yillar bo‘yicha filmlar soni
- Har bir yil nechta top film chiqqanini ko‘rsatadi  
- Kino tarixidagi eng faol davrlarni aniqlashga yordam beradi  

### 🏆 Eng yuqori reytingli Top 10 filmlar
- IMDb reytingiga asoslangan  
- Eng mashhur va eng yuqori baholangan filmlar ro‘yxati  

### 📊 Reyting va ovozlar soni o‘rtasidagi bog‘liqlik
- Film sifati (reyting) va mashhurligi (ovozlar soni) o‘rtasidagi aloqani tahlil qiladi  

### 🎭 Janrlar tahlili
- Eng ko‘p uchraydigan janrlar  
- Janrlar bo‘yicha taqsimot vizualizatsiyasi  

### ⏱️ Film davomiyligi tahlili
- O‘rtacha film davomiyligi  
- Film uzunliklari taqsimoti  

---

## 🛠️ Ishlatilgan texnologiyalar

- **Python**
- **Streamlit**
- **Pandas**
- **Matplotlib / Plotly**
- **CSV Dataset**

---

## 📁 Loyiha tuzilishi

```text
IMDb_Dashboard/
│
├─ app.py                 # Asosiy Streamlit ilova
├─ top_1000ta_kino.csv    # Dataset
├─ requirements.txt       # Kutubxonalar ro‘yxati
└─ README.md              # Loyiha hujjati
```
▶️ Lokal kompyuterda ishga tushirish

1. Repository’ni klon qiling:

git clone https://github.com/USERNAME/IMDb_Dashboard.git


2. Loyiha papkasiga o‘ting:

cd IMDb_Dashboard


3. Kerakli kutubxonalarni o‘rnating:

pip install -r requirements.txt


4. Streamlit ilovani ishga tushiring:

streamlit run app.py

👨‍💻 Dasturchilar

✅ Suhrob Panjiyev

✅ Komilova Charos

✅ Saidov Alisher

✅ S Sarvara

