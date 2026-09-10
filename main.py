import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("---")


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)

    # 날짜 열을 datetime 형식으로 변환 (YYYYMMDD -> YYYY-MM-DD)
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

    return df


df = load_data()

# -------------------------------------------------------------------
# 구역 1: 영화별 일별 관객수 변화 (선 그래프)
# -------------------------------------------------------------------
st.header("1. 영화별 일관객수 추이")

# 영화 목록 추출 (오름차순 정렬)
movie_list = sorted(df["영화명"].dropna().unique())

# 영화 선택 드롭다운
selected_movie = st.selectbox(
    "관객수 변화를 확인할 영화를 선택하세요:", movie_list
)

# 선택한 영화 데이터 필터링
movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

if not movie_df.empty:
    # Plotly 선 그래프 생성
    fig1 = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        title=f"<{selected_movie}> 일별 관객수 변화",
        labels={"날짜": "날짜", "일관객": "일일 관객수 (명)"},
        markers=True,
    )

    # 마우스 오버(툴팁) 레이아웃 설정
    fig1.update_traces(
        hovertemplate="<b>날짜</b>: %{x|%Y-%m-%d}<br><b>일관객수</b>: %{y:,}명<extra></extra>"
    )
    fig1.update_layout(hovermode="x unified")

    st.plotly_chart(fig1, use_container_width=True)

    # 그래프 해석 문구 자리
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 특정 영화의 개봉 후 관객수 증감 추이와 주말/평일 관객수 차이를 한눈에 파악할 수 있습니다."
    )
else:
    st.warning("선택한 영화의 데이터가 없습니다.")

st.markdown("---")

# -------------------------------------------------------------------
# 구역 2: 추후 그래프 추가 구역 (예시 레이아웃)
# -------------------------------------------------------------------
st.header("2. 추가 그래프 구역 (예정)")
st.caption("앞으로 시간 축 기반의 다양한 그래프가 이곳에 추가될 예정입니다.")

# 추후 그래프 추가 예시 틀
# fig2 = ...
# st.plotly_chart(fig2, use_container_width=True)
# st.info("💡 **이 그래프로 알 수 있는 것:** [여기에 설명 문구를 작성하세요]")
