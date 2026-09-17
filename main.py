import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 제목
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화 216편의 데이터를 다양한 그래프로 살펴봅니다.")

# 데이터 불러오기
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일을 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d", errors="coerce")

    # 장르에 세로막대(|)가 있으면 첫 번째 장르만 사용
    df["genre"] = df["genre"].fillna("알 수 없음").astype(str).str.split("|").str[0]

    return df


df = load_data()

# 데이터 확인
st.subheader("📋 데이터 요약")
st.write(f"분석 대상 영화: **{len(df)}편**")

# --------------------------------------------------
# 그래프 1. 장르별 영화 편수
# --------------------------------------------------
st.divider()
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_counts.columns = ["장르", "영화 편수"]

fig = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수",
)

fig.update_traces(
    textinfo="label",
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

fig.update_layout(
    height=500,
    legend_title="장르"
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "어떤 장르의 영화가 1년간 박스오피스 10위권에 가장 많이 등장했는지 한눈에 비교할 수 있습니다."
)

# --------------------------------------------------
# 그래프 추가 예정 구역
# --------------------------------------------------
st.divider()
st.header("2. 다음 그래프")
st.write("여기에 두 번째 그래프를 추가할 수 있습니다.")

st.divider()
st.header("3. 다음 그래프")
st.write("여기에 세 번째 그래프를 추가할 수 있습니다.")
