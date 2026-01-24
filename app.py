import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Sahifa sozlamaraniki
st.set_page_config(
    page_title="IMDb Top Movies Analysis",
    page_icon="🎬",
    layout="wide"
)

# Title
st.title("🎬 IMDb Top Movies Dashboard")
st.markdown("IMDb Top kinolar ma’lumotlari asosida interaktiv tahlil")

# ma'lumotlarni yuklash
@st.cache_data  # “Agar data o‘zgarmagan bo‘lsa, qayta o‘qima, tez ishlat” , Streamlitga shunaqa deb aytadi.
def malumotlar():
    df = pd.read_csv("top_1000ta_kino.csv")
    # Keraksiz ustunlarni olib tashlash
    columns_to_drop = [
        "Position",
        "Const",
        "Modified",
        "Created",
        "Description",
        "Original Title",
        "URL",
        "Title Type",
        "Release Date"
    ]
    df = df.drop(columns=columns_to_drop)
    return df
df = malumotlar()



# Yon panel filtrlari
st.sidebar.header("🎛 Filterlar")

min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider(
    "📅 Yil oralig‘i",
    min_year,
    max_year,
    (min_year, max_year)
)

min_rating, max_rating = float(df["IMDb Rating"].min()), float(df["IMDb Rating"].max())
rating_range = st.sidebar.slider(
    "⭐ Reyting oralig‘i",
    min_rating,
    max_rating,
    (min_rating, max_rating)
)

# Ma'lumotlarni filtrlash
filtered_df = df[
    (df["Year"].between(year_range[0], year_range[1])) &
    (df["IMDb Rating"].between(rating_range[0], rating_range[1]))
]

# Maʼlumotlar toʻplamini koʻrsatish
st.subheader("📄 Filtrlangan ma’lumotlar")
st.dataframe(filtered_df, use_container_width=True)

st.markdown("""
ℹ️ **Izoh:**  
Ushbu jadval tanlangan yil va reyting oralig‘iga mos keluvchi filmlarni ko‘rsatadi.  
Filterlar yordamida foydalanuvchi ma’lumotlarni dinamik ravishda tahlil qilishi mumkin.
""")


# Ko'rsatkichlar
col1, col2, col3 = st.columns(3)
col1.metric("🎬 Jami filmlar", len(filtered_df))
col2.metric("⭐ O‘rtacha reyting", round(filtered_df["IMDb Rating"].mean(),2), "↑0.2")
col3.metric("🗳 Jami ovozlar", f"{filtered_df['Num Votes'].sum():,}")

# Grafiklar
st.markdown("---")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



col_left, col_right = st.columns(2)

# ⭐Reytingni taqsimlash
with col_left:
    st.subheader("⭐ Reyting taqsimoti")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df["IMDb Rating"], bins=10, kde=True, ax=ax)
    ax.set_xlabel("IMDb reytingi")
    ax.set_ylabel("Soni")
    st.pyplot(fig)

    st.markdown("""
    📌 **Tahlil:**  
    Grafikdan ko‘rinib turibdiki, filmlarning katta qismi **IMDb 7.5–9.0** oralig‘ida joylashgan.  
    Bu dataset tasodifiy filmlar emas, balki **eng sifatli va mashhur filmlar**dan tuzilganini ko‘rsatadi.  
    Past reytingli filmlarning kamligi IMDb Top ro‘yxatining tanlab olinishi bilan izohlanadi.
    """)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Yiliga filmlar
with col_right:
    st.subheader("📅 Yillar bo‘yicha filmlar soni")
    fig, ax = plt.subplots()
    filtered_df["Year"].value_counts().sort_index().plot(kind="line", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies")
    st.pyplot(fig)

    st.markdown("""
    📌 **Tahlil:**  
    Yillar bo‘yicha filmlar soni doimiy emas, ayrim davrlarda keskin o‘sish kuzatiladi.  
    Bu davrlar kino sanoatining rivojlangan bosqichlari yoki texnologik yutuqlar bilan bog‘liq bo‘lishi mumkin.  
    Ayrim yillarda pasayish esa urushlar yoki iqtisodiy inqirozlar bilan izohlanadi.
    """)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# Eng mashhur filmlar
st.markdown("---")
st.subheader("🏆 Eng yuqori reytingli Top 10 filmlar")

top_10 = filtered_df.sort_values("IMDb Rating", ascending=False).head(10)
st.table(
    top_10[["Title", "Year", "IMDb Rating", "Num Votes", "Directors"]]
)

st.markdown("""
📌 **Xulosa:**  
Ushbu ro‘yxatda IMDb reytingi va ovozlar soni juda yuqori bo‘lgan filmlar jamlangan.  
Bu filmlar kino tarixidagi eng muvaffaqiyatli va tomoshabinlar tomonidan eng ko‘p e’tirof etilgan asarlar hisoblanadi.
""")



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# Eng kop ovoz olgan top 10 film
st.subheader("🔥 Eng ko‘p ovoz olgan Top 10 filmlar")

top_votes = filtered_df.sort_values("Num Votes", ascending=False).head(10)
st.table(top_votes[["Title", "Year", "Num Votes", "IMDb Rating"]])

st.markdown("""
📌 **Tahlil:**  
Ushbu filmlar eng ko‘p tomoshabin tomonidan baholangan bo‘lib, ularning ommabopligi juda yuqori.
""")
st.markdown("""
📌 **Tahlil:**  
Bu filmlar eng ko‘p tomoshabin tomonidan baholangan bo‘lib, ularning ommabopligi juda yuqori.  
Ko‘p ovozlar filmning mashhurligini bildiradi, lekin har doim ham yuqori reytingni kafolatlamaydi.  
Bu ko‘rsatkich auditoriya qamrovini baholashda muhim rol o‘ynaydi.
""")

st.success("🏆 Top 10 filmlar tahlili tayyor")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



st.subheader("📊 Eng ko‘p ko‘rilgan rejissyorlar (Top 10)")

# Ba'zi filmlarda bir nechta rejissyor bo‘lishi mumkin → split qilamiz
directors_df = df.copy()
directors_df["Directors"] = directors_df["Directors"].str.split(", ")
directors_df = directors_df.explode("Directors")

# Har bir rejissyor bo‘yicha umumiy votes
top_directors_votes = (
    directors_df.groupby("Directors")["Num Votes"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_votes = px.bar(
    top_directors_votes,
    x="Directors",
    y="Num Votes",
    title="Top 10 rejissyor — filmlarining umumiy ovozlar soni",
)


st.plotly_chart(fig_votes, use_container_width=True)

st.markdown("""
📌 **Tahlil:**  
Grafik ayrim rejissyorlarning filmlari juda katta auditoriyani jalb qilganini ko‘rsatadi.  
Bu holat ularning filmlari ommabop mavzularni qamrab olgani yoki keng tarqalgan franchayzlar bilan bog‘liq.  
Ovozlar soni mashhurlikni bildiradi, lekin sifatni to‘liq ifodalamaydi.
""")



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




st.subheader("⭐ Rejissyorlar bo‘yicha o‘rtacha IMDb reyting")

top_directors_rating = (
    directors_df.groupby("Directors")["IMDb Rating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_rating = px.bar(
    top_directors_rating,
    x="Directors",
    y="IMDb Rating",
    title="Top 10 rejissyor — o‘rtacha IMDb reyting",
)

st.plotly_chart(fig_rating, use_container_width=True)

st.markdown("""
📌 **Tahlil:**  
Bu grafik rejissyorlarning filmlari sifat jihatdan qanchalik yuqori baholanganini ko‘rsatadi.  
Ba’zi rejissyorlar kam film suratga olgan bo‘lsa ham, ularning reytingi yuqori.  
Bu sifat har doim miqdordan ustun bo‘lishi mumkinligini ko‘rsatadi.
""")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



st.header("🎭 Janrlar va yillar bo‘yicha tahlil")
st.subheader("📅 Yillar bo‘yicha janrlar taqsimoti")

# Janrlarni alohida qatorlarga ajratamiz
genres_df = df.copy()
genres_df["Genres"] = genres_df["Genres"].str.split(", ")
genres_df = genres_df.explode("Genres")

# Yil + janr bo‘yicha filmlar soni
genre_year_count = (
    genres_df.groupby(["Year", "Genres"])
    .size()
    .reset_index(name="Movie Count")
)

# Eng ko‘p uchraydigan 5 ta janrni olamiz (grafik chiroyli bo‘lishi uchun)
top_genres = (
    genre_year_count.groupby("Genres")["Movie Count"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

filtered_data = genre_year_count[genre_year_count["Genres"].isin(top_genres)]

fig_genre_year = px.line(
    filtered_data,
    x="Year",
    y="Movie Count",
    color="Genres",
    title="Yillar bo‘yicha eng mashhur janrlar",
)

st.plotly_chart(fig_genre_year, use_container_width=True)

st.markdown("""
📌 **Tahlil:**   
Ushbu grafik turli yillarda qaysi janrdagi filmlar ko‘proq suratga olinganini ko‘rsatadi.  
Ayrim davrlarda Drama va War janrlarining keskin oshgani kuzatiladi.  
Bu holat tarixiy voqealar, xususan Ikkinchi jahon urushi va undan keyingi ijtimoiy jarayonlar bilan bog‘liq bo‘lishi mumkin.
""")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



st.subheader("🏭 Eng ko‘p film suratga olingan yillar")

movies_per_year = (
    df.groupby("Year")
    .size()
    .reset_index(name="Movie Count")
    .sort_values("Movie Count", ascending=False)
    .head(10)
)

fig_years = px.bar(
    movies_per_year,
    x="Year",
    y="Movie Count",
    title="Top 10 eng sermahsul yillar",
)

st.plotly_chart(fig_years, use_container_width=True)
st.markdown("""
📌 **Tahlil:**   
Bu grafik eng ko‘p film suratga olingan yillarni ko‘rsatadi.  
Bu davrlar kino sanoatining rivojlanishi, texnologik yutuqlar yoki jamiyatda kino orqali fikr bildirish ehtiyoji kuchaygan davrlarga to‘g‘ri kelishi mumkin.
""")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



st.header("🎯 Janrlar bo‘yicha(Top 5), eng sermahsul yillar")

# Janrlarni alohida qatorlarga ajratamiz
genre_peak_df = df.copy()
genre_peak_df["Genres"] = genre_peak_df["Genres"].str.split(", ")
genre_peak_df = genre_peak_df.explode("Genres")

# Janr + yil bo‘yicha filmlar soni
genre_year_counts = (
    genre_peak_df.groupby(["Genres", "Year"])
    .size()
    .reset_index(name="Movie Count")
)

# Har bir janr uchun eng ko‘p film olingan yil
idx = genre_year_counts.groupby("Genres")["Movie Count"].idxmax()
genre_peak_years = genre_year_counts.loc[idx].sort_values("Movie Count", ascending=False)

# Faqat eng yuqori 8 janrni olish
genre_peak_years = genre_peak_years.head(5)

# Natijalarni chiqarish
for _, row in genre_peak_years.iterrows():
    st.markdown(f"""
> 🎭 **{row['Genres']}**  
> 📅 Eng ko‘p film olingan yil: **{int(row['Year'])}**  
> 🎬 Film soni: **{row['Movie Count']} ta**
""")

# Umumiy izoh
st.markdown("""
💡 **Izoh:** Ushbu janrlarning eng sermahsul yillari o‘sha davrdagi ijtimoiy, tarixiy yoki madaniy jarayonlar bilan bog‘liq bo‘lishi mumkin.
""")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# IMDb reytingi va ovozlar soni farqi
st.subheader("📊 IMDb reyting va ovozlar soni o‘rtasidagi bog‘liqlik")

fig, ax = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="Num Votes",
    y="IMDb Rating",
    ax=ax
)
ax.set_xlabel("Ovozlar soni")
ax.set_ylabel("IMDb reytingi")
st.pyplot(fig)

st.markdown("""
📌 **Tahlil:**  
Ko‘p ovozga ega filmlar odatda barqaror reytingga ega ekanini ko‘rish mumkin.  
Ammo ayrim filmlar kam ovoz bilan yuqori reyting olgan — bu tor auditoriyaga mo‘ljallangan filmlar bo‘lishi mumkin.  
Demak, reyting va mashhurlik har doim ham bir xil bo‘lmaydi.
""")


# +++++++++++++++++++++++++++++++++++++++++-++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# Filmlar davomiyligi taqsimoti
st.subheader("⏱ Film davomiyligi taqsimoti")

fig, ax = plt.subplots()
sns.histplot(filtered_df["Runtime (mins)"], bins=15, ax=ax)
ax.set_xlabel("Davomiyligi (daqiqa)")
ax.set_ylabel("Filmlar soni")
st.pyplot(fig)

st.markdown("""
📌 **Tahlil:**  
Filmlarning katta qismi 90–180 daqiqa oralig‘ida joylashgan.  
Bu kino sanoatida optimal davomiylik mavjudligini ko‘rsatadi.  
Juda qisqa yoki juda uzun filmlar kam uchraydi, chunki ular tomoshabin e’tiborini yo‘qotishi mumkin.
""")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




# Eng yaxshi rejiseorlar va filmlari soni
st.subheader("🎬 Eng yaxshi rejissyorlar (o‘rtacha reyting)")

director_df = filtered_df.copy()
director_df["Directors"] = director_df["Directors"].str.split(", ")
director_df = director_df.explode("Directors")

top_directors = (
    director_df.groupby("Directors")
    .agg(
        avg_rating=("IMDb Rating", "mean"),
        movie_count=("Title", "count")
    )
    .query("movie_count >= 2")
    .sort_values("avg_rating", ascending=False)
    .head(10)
)

st.dataframe(top_directors)

st.markdown("""
📌 **Tahlil:**  
Ushbu jadval bir nechta film suratga olgan va o‘rtacha IMDb reytingi yuqori bo‘lgan rejissyorlarni ko‘rsatadi.  
Bu rejissyorlar filmlarida **sifat barqarorligi** kuzatiladi va ularning ishlari tomoshabinlar tomonidan yuqori baholanadi.
""")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# Yillar buyicha filmlar tahlili
st.subheader("📅 O‘n yilliklar bo‘yicha filmlar tahlili")

filtered_df["Decade"] = (filtered_df["Year"] // 10) * 10

decade_stats = (
    filtered_df.groupby("Decade")
    .agg(
        avg_rating=("IMDb Rating", "mean"),
        movie_count=("Title", "count")
    )
)

st.dataframe(decade_stats)

st.markdown("""
📌 **Tahlil:**  
Jadvaldan ko‘rinib turibdiki, ayrim o‘n yilliklarda filmlar soni va o‘rtacha reyting yuqoriroq bo‘lgan.  
Bu davrlar kino sanoatining eng faol va samarali bosqichlari ekanini ko‘rsatadi.
""")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# _____________________________________________________________________________________________________________________

# st.sidebar.markdown("---")

# with st.sidebar.expander("👨‍💻 Developers"):
#     st.markdown("""
# > **👤 Suhrob Panjiyev**  
# > _Python • Data Analysis • Streamlit_  
# > 🔗 [GitHub](https://github.com/Panjiyevsuhrob84parol)  
# > 📬 [Telegram](https://t.me/atlet_bro)  
# > 🎛️ [Instagram](https://instagram.com/suhrob_panjiyev_)
# ---
# > **👤 Komilova Charos**  
# > _Python • Data Analysis • Streamlit • AI_  
# > 🔗 [GitHub](https://github.com/USERNAME)  
# > 📬 [Telegram](https://t.me/Charos123340)  
# > 🎛️ [Instagram](https://instagram.com/USERNAME)
# ---
# > **👤 Saidov Alisher**  
# > _Python • Data Analysis • Streamlit • AI_  
# > 🔗 [GitHub](https://github.com/USERNAME)  
# > 📬 [Telegram](https://t.me/Saidov_1004)  
# > 🎛️ [Instagram](https://instagram.com/USERNAME)
# ---
# > **👤 Samadova Sarvara**  
# > _Python • Data Analysis • Streamlit • AI_  
# > 🔗 [GitHub](https://github.com/USERNAME)  
# > 📬 [Telegram](https://t.me/Hadria1300)  
# > 🎛️ [Instagram](https://instagram.com/USERNAME)
# """)
    

# ***************************************************************************

st.sidebar.markdown("---")

with st.sidebar.expander("👨‍💻 Developers"):
    st.markdown("""
<div style="line-height:1.8; font-size:14px;">
<b>👤 Suhrob Panjiyev</b><br>
Python • Data Analysis • Streamlit<br>
<a href="https://github.com/Panjiyevsuhrob84parol" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/25/25231.png" width="20"> GitHub
</a> &nbsp; 
<a href="https://t.me/atlet_bro" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/2111/2111646.png" width="20"> Telegram
</a> &nbsp; 
<a href="https://instagram.com/suhrob_panjiyev_" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/2111/2111463.png" width="20"> Instagram
</a>
<hr>
<b>👤 Komilova Charos</b><br>
Python • Data Analysis • Streamlit • AI<br>
<a href="https://github.com/charoskomilova1041-hub" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/25/25231.png" width="20"> GitHub
</a> &nbsp; 
<a href="https://t.me/Charos123340" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/2111/2111646.png" width="20"> Telegram
</a> &nbsp; 
<a href="https://instagram.com/USERNAME" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/2111/2111463.png" width="20"> Instagram
</a>
<hr>
<b>👤 Saidov Alisher</b><br>
Python • Data Analysis • Streamlit • AI<br>
<a href="https://github.com/Saidov-Alisher" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/25/25231.png" width="20"> GitHub
</a> &nbsp; 
<a href="https://t.me/Saidov_1004" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/2111/2111646.png" width="20"> Telegram
</a> &nbsp; 
<a href="https://instagram.com/saidov_1004" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/2111/2111463.png" width="20"> Instagram
</a>
<hr>
<b>👤 Samadova Sarvara</b><br>
Python • Data Analysis • Streamlit • AI<br>
<a href="https://github.com/USERNAME" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/25/25231.png" width="20"> GitHub
</a> &nbsp; 
<a href="https://t.me/Hadria1300" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/2111/2111646.png" width="20"> Telegram
</a> &nbsp; 
<a href="https://instagram.com/USERNAME" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/24/2111/2111463.png" width="20"> Instagram
</a>
</div>
""", unsafe_allow_html=True)


# ___________________________________________________________________________________________________________________

    st.markdown("---")
st.subheader("📝 Umumiy Xulosa (Summary)")

st.markdown("""
**IMDb Top Movies Dashboard tahlili yakuniy xulosasi:**  

1. **Dataset sifati:** Dataset eng mashhur va yuqori reytingli filmlardan tashkil topgan.  
2. **Reyting va Ovozlar:** Ko‘p ovoz olgan filmlar odatda yuqori va barqaror reytingga ega, kam ovozli filmlarda reyting subyektiv bo‘lishi mumkin.  
3. **Janrlar:** Drama va Crime janrlari eng ko‘p uchraydi, bu jiddiy va syujetga boy filmlarning ustunligini ko‘rsatadi.  
4. **Rejissyorlar:** Eng ko‘p yuqori reytingga ega filmlarga ega rejissyorlar kino sifatini barqaror saqlab kelmoqda.  
5. **Film davomiyligi:** Filmlarning aksariyati 90–180 daqiqa oralig‘ida, davomiylik va reyting o‘rtasida kuchli bog‘liqlik yo‘q.  
6. **Davr bo‘yicha tahlil:** Ayrim o‘n yilliklar kino tarixida eng samarali davr bo‘lganini ko‘rsatadi.  
7. **Top 10 filmlar:** Eng yuqori reytingga ega filmlar kino tarixida klassik va tomoshabinlar tomonidan e’tirof etilgan.  

📌 Ushbu dashboard interaktiv filterlar, grafiklar, xulosalar va developers bo‘limi bilan ta’minlangan, shuning uchun foydalanuvchi **ma’lumotlarni o‘rganishi va tahlil qilishi** mumkin.
""")


st.markdown(
    """
    <div style="
        text-align:center;
        padding:25px 0;
        color:#777;
        font-size:14px;">
        🎬 Designed by <b>Suhrob Panjiyev</b><br>
        Python • Streamlit • Data Analysis • AI
    </div>
    """,
    unsafe_allow_html=True
)



# 55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555



st.sidebar.markdown("---")

st.sidebar.image(
    "logo_brand.png",
    use_container_width=True
)

st.sidebar.markdown("""
<div style="text-align:center; font-size:14px; color:gray;">
<b>AI TEAM</b><br>
Data • Streamlit • AI
</div>
""", unsafe_allow_html=True)



