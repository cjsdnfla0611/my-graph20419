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
st.header("1. 개별 영화 일관객수 추이")

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
# 구역 2: 누적 관객 상위 5개 영화 비교 (주말 음영 표시)
# -------------------------------------------------------------------
st.header("2. 기간 내 관객수 TOP 5 영화의 일일 관객수 비교 (주말 강조)")

# 전체 기간 내 총 일관객 합계 상위 5개 영화 추출
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .nlargest(5)
    .index.tolist()
)

# TOP 5 영화 데이터만 필터링
top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

if not top5_df.empty:
    # Plotly 선 그래프 생성 (영화명별 색상 구분)
    fig2 = px.line(
        top5_df,
        x="날짜",
        y="일관객",
        color="영화명",
        title="기간 내 일관객수 합계 TOP 5 영화 추이 비교 (음영 구간: 주말)",
        labels={"날짜": "날짜", "일관객": "일일 관객수 (명)", "영화명": "영화 제목"},
        markers=False,
    )

    # 주말(토요일, 일요일) 구간 찾아서 배경 음영 추가
    # 전체 날짜 범주 추출
    unique_dates = pd.date_range(start=df["날짜"].min(), end=df["날짜"].max(), freq="D")
    
    # 주말 세로 영역 추가 (토요일 00:00 ~ 일요일 23:59 영역 강조)
    for single_date in unique_dates:
        if single_date.weekday() == 5:  # 토요일인 경우
            fig2.add_vrect(
                x0=single_date - pd.Timedelta(days=0.5),
                x1=single_date + pd.Timedelta(days=1.5),
                fillcolor="gray",
                opacity=0.15,
                line_width=0,
                layer="below",
            )

    # 마우스 오버 툴팁 및 범례 클릭 설정 (Plotly 기본 기능으로 범례 클릭 시 토글 가능)
    fig2.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
    )
    fig2.update_layout(
        hovermode="x unified",
        legend_title_text="영화 (클릭하여 켜기/끄기)",
    )

    st.plotly_chart(fig2, use_container_width=True)

    # 그래프 해석 문구 자리
    st.info(
        "💡 **이 그래프로 알 수 있는 것:** 흥행 상위 영화들의 흥행 피크 시점 차이와 회색으로 표시된 주말마다 일관객수가 급증하는 박스오피스의 주말 집중 현상을 확인할 수 있습니다."
    )

st.markdown("---")

# -------------------------------------------------------------------
# 구역 3: 추후 그래프 추가 구역
# -------------------------------------------------------------------
st.header("3. 추가 그래프 구역 (예정)")
st.caption("앞으로 시간 축 기반의 다양한 그래프가 이곳에 추가될 예정입니다.")
