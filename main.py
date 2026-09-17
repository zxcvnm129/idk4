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

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일을 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # |가 있으면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("알 수 없음")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    # 숫자 데이터 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    )

    df["first_scrn"] = pd.to_numeric(
        df["first_scrn"],
        errors="coerce"
    )

    df["first_week_audi"] = pd.to_numeric(
        df["first_week_audi"],
        errors="coerce"
    )

    return df


df = load_data()

# 데이터 요약
st.subheader("📋 데이터 요약")
st.write(f"분석 대상 영화: **{len(df)}편**")


# ==================================================
# 그래프 1. 장르별 영화 편수
# ==================================================
st.divider()
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화 편수"]

fig1 = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="label",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    height=500,
    legend_title="장르"
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "어떤 장르의 영화가 1년간 박스오피스 10위권에 가장 많이 등장했는지 한눈에 비교할 수 있습니다."
)


# ==================================================
# 그래프 2. 장르별 영화 트리맵
# ==================================================
st.divider()
st.header("2. 장르별 영화 트리맵")

treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].dropna().copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객 수"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=650,
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "각 장르에 어떤 영화가 포함되어 있는지와 영화별 총 관객 규모의 차이를 면적을 통해 비교할 수 있습니다."
)


# ==================================================
# 그래프 3. 총 관객 수 히스토그램
# ==================================================
st.divider()
st.header("3. 총 관객 수 분포")

hist_df = df[
    ["movieNm", "total_audi"]
].dropna().copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    height=500,
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수"
)

st.plotly_chart(fig3, use_container_width=True)

# 가장 많은 영화가 들어 있는 구간 계산
counts, bin_edges = pd.cut(
    hist_df["total_audi"],
    bins=20,
    retbins=True
)

bin_counts = counts.value_counts().sort_index()
most_common_bin = bin_counts.idxmax()

low = most_common_bin.left
high = most_common_bin.right

# 총 관객이 가장 많은 영화
top_movie = hist_df.loc[
    hist_df["total_audi"].idxmax()
]

st.info(
    f"💡 이 그래프로 알 수 있는 것: "
    f"대부분의 영화는 약 **{low:,.0f}명 ~ {high:,.0f}명** 구간에 몰려 있으며, "
    f"총 관객이 가장 많은 영화는 **{top_movie['movieNm']}**로 "
    f"**{top_movie['total_audi']:,.0f}명**의 관객을 기록했습니다."
)


# ==================================================
# 그래프 4. 개봉일 스크린 수와 총 관객의 관계
# ==================================================
st.divider()
st.header("4. 개봉일 스크린 수와 총 관객의 관계")

scatter_df = df[
    ["movieNm", "genre", "first_scrn", "total_audi"]
].dropna().copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    }
)

fig4.update_traces(
    marker=dict(size=10, opacity=0.75),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,}개<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    height=600,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    legend_title="장르"
)

st.plotly_chart(fig4, use_container_width=True)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "개봉일에 확보한 스크린 수와 영화의 총 관객 수가 어떤 관계를 보이는지, 그리고 장르별 영화들이 어떻게 분포하는지 살펴볼 수 있습니다."
)


# ==================================================
# 그래프 5. 장르별 총 관객 수 상자 그림
# ==================================================
st.divider()
st.header("5. 장르별 총 관객 수 상자 그림")

# 장르별 영화 편수 계산
genre_movie_counts = df["genre"].value_counts()

# 영화가 10편 이상인 장르만 선택
selected_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index

box_df = df[
    df["genre"].isin(selected_genres)
][
    ["genre", "movieNm", "total_audi"]
].dropna().copy()

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객 수 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{x}<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=600,
    xaxis_title="장르",
    yaxis_title="총 관객 수"
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "영화가 10편 이상인 장르끼리 총 관객 수의 중앙값과 분포 범위를 비교하고, 특히 다른 영화보다 관객 수가 크게 높은 이상치를 확인할 수 있습니다."
)


# ==================================================
# 그래프 6. 첫 주 관객을 크기로 나타낸 버블 그래프
# ==================================================
st.divider()
st.header("6. 개봉일 스크린 수 · 총 관객 · 첫 주 관객")

bubble_df = df[
    ["movieNm", "genre", "first_scrn", "total_audi", "first_week_audi"]
].dropna().copy()

# 음수 값 제거
bubble_df = bubble_df[
    (bubble_df["first_scrn"] >= 0) &
    (bubble_df["total_audi"] >= 0) &
    (bubble_df["first_week_audi"] >= 0)
]

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=45,
    title="개봉일 스크린 수와 총 관객 수 — 버블 크기는 첫 주 관객",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객",
        "genre": "장르"
    }
)

fig6.update_traces(
    opacity=0.7,
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    height=650,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    legend_title="장르"
)

st.plotly_chart(fig6, use_container_width=True)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "개봉일 스크린 수와 총 관객 수의 관계를 살펴보면서 버블 크기를 통해 첫 주 관객 규모까지 함께 비교할 수 있습니다."
)
# ==================================================
# 그래프 7. 제작 국가 → 장르 선버스트
# ==================================================
st.divider()
st.header("7. 제작 국가에서 장르로 내려가는 선버스트")

sunburst_df = df[
    ["nation", "genre"]
].copy()

# 결측값 처리
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("알 수 없음")
    .astype(str)
)

sunburst_df["genre"] = (
    sunburst_df["genre"]
    .fillna("알 수 없음")
    .astype(str)
)

# 제작 국가 → 장르별 영화 편수 계산
sunburst_counts = (
    sunburst_df
    .groupby(["nation", "genre"])
    .size()
    .reset_index(name="movie_count")
)

fig7 = px.sunburst(
    sunburst_counts,
    path=["nation", "genre"],
    values="movie_count",
    title="제작 국가 → 장르별 영화 편수",
    labels={
        "nation": "제작 국가",
        "genre": "장르",
        "movie_count": "영화 편수"
    }
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    height=700,
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig7, use_container_width=True)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "제작 국가별로 어떤 장르의 영화가 많이 만들어졌는지와 각 국가·장르에 속한 영화 편수의 규모를 한눈에 비교할 수 있습니다."
)
# ==================================================
# 그래프 8. 10위권에 오래 머문 영화는 총 관객도 많은가
# ==================================================
st.divider()
st.header("8. 10위권에 오래 머문 영화는 총 관객도 많은가")

scatter_df2 = df[
    ["movieNm", "days_in_top10", "total_audi"]
].copy()

# 숫자로 변환
scatter_df2["days_in_top10"] = pd.to_numeric(
    scatter_df2["days_in_top10"],
    errors="coerce"
)

scatter_df2["total_audi"] = pd.to_numeric(
    scatter_df2["total_audi"],
    errors="coerce"
)

# 필요한 데이터가 있는 행만 사용
scatter_df2 = scatter_df2.dropna()

fig8 = px.scatter(
    scatter_df2,
    x="days_in_top10",
    y="total_audi",
    hover_name="movieNm",
    title="10위권에 오래 머문 영화는 총 관객도 많은가",
    labels={
        "days_in_top10": "10위권에 머문 날수",
        "total_audi": "총 관객 수"
    }
)

fig8.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "10위권에 머문 날수: %{x}일<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig8.update_layout(
    height=600,
    xaxis_title="10위권에 머문 날수",
    yaxis_title="총 관객 수"
)

st.plotly_chart(fig8, use_container_width=True)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "영화가 10위권에 머문 날수와 총 관객 수가 어떤 관계를 보이는지 영화별로 비교할 수 있습니다."
)
