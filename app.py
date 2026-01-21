import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

col_left, col_right = st.columns(2)

# Reytingni taqsimlash
with col_left:
    st.subheader("⭐ Reyting taqsimoti")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df["IMDb Rating"], bins=10, kde=True, ax=ax)
    ax.set_xlabel("IMDb Rating")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.markdown("""
    📌 **Tahlil:**  
    Grafikdan ko‘rinib turibdiki, filmlarning katta qismi yuqori IMDb reytinglariga ega.  
    Bu dataset asosan sifatli va mashhur filmlardan tashkil topganini ko‘rsatadi.
    """)


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
    Yillar bo‘yicha filmlar sonining o‘zgarishi kino sanoatining faol davrlarini ko‘rsatadi.  
    Ayrim yillarda mashhur va klassik filmlar ko‘proq suratga olinganini kuzatish mumkin.
    """)


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

# _____________________________________________________________________________________________________________________

# Eng kop ovoz olgan top 10 film
st.subheader("🔥 Eng ko‘p ovoz olgan Top 10 filmlar")

top_votes = filtered_df.sort_values("Num Votes", ascending=False).head(10)
st.table(top_votes[["Title", "Year", "Num Votes", "IMDb Rating"]])

st.markdown("""
📌 **Tahlil:**  
Ushbu filmlar eng ko‘p tomoshabin tomonidan baholangan bo‘lib, ularning ommabopligi juda yuqori.
""")
st.success("🏆 Top 10 filmlar tahlili tayyor")

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
Ko‘p ovozga ega filmlar odatda barqaror va ishonchli reytingga ega ekanini ko‘rish mumkin.
""")

# Filmlar davomiyligi taqsimoti
st.subheader("⏱ Film davomiyligi taqsimoti")

fig, ax = plt.subplots()
sns.histplot(filtered_df["Runtime (mins)"], bins=15, ax=ax)
ax.set_xlabel("Davomiyligi (daqiqa)")
ax.set_ylabel("Filmlar soni")
st.pyplot(fig)

st.markdown("""
📌 **Tahlil:**  
Filmlarning aksariyati 90–180 daqiqa oralig‘ida bo‘lib, bu kino sanoatidagi standart davomiylikni ko‘rsatadi.
""")

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
Bir nechta yuqori reytingli filmlarga ega bo‘lgan rejissyorlar kino sifatini barqaror saqlab kelmoqda.
""")

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
Ayrim o‘n yilliklar kino tarixida eng samarali davr bo‘lganini ko‘rish mumkin.
""")


# _____________________________________________________________________________________________________________________

st.sidebar.markdown("---")

with st.sidebar.expander("👨‍💻 Developers"):
    st.markdown("""
    **Suhrob Panjiyev**  
    Python • Data Analysis • Streamlit  

    🔗 [GitHub](https://github.com/USERNAME)  
    📬 [Telegram](https://t.me/USERNAME)
    🎛️ [Instagram](https://instagram.com/suhrob_panjiyev_)
    """)
    st.markdown("""
    **Aliyev Vali**  
    Python • Data Analysis • Streamlit • AI

    🔗 [GitHub](https://github.com/USERNAME)  
    📬 [Telegram](https://t.me/USERNAME)
    🎛️ [Instagram](https://instagram.com/suhrob_panjiyev_)
    """)

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
