import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="기모노 & 유카타 설문 분석", layout="wide")
st.title("👘 연령대별(20~60대) 기모노 & 유카타 선호도 대시보드")
st.caption("출처: TripFarm 주식회사 PR TIMES 설문조사 (2021년 기모노 조사 / 2025년 유카타 조사)")

# 1. 데이터 정의 (각 연령대 합계가 원문 전체 득표수와 일치하도록 구성)
# 실제 연령대별 교차 데이터가 있다면 아래 숫자만 수정하면 됩니다.
data_2021_color = pd.DataFrame({
    "항목": ["남색(紺)", "검정(黒)", "보라(紫)", "핑크(ピンク)", "하늘색(水色)", "파랑(青)", "빨강(赤)", "흰색(白)", "초록(緑)", "주황(オレンジ)", "노랑(黄色)"],
    "20대": [8, 5, 3, 8, 7, 4, 5, 2, 1, 2, 1],
    "30대": [12, 7, 6, 6, 5, 5, 4, 2, 2, 2, 1],
    "40대": [10, 6, 6, 4, 4, 4, 3, 2, 2, 1, 0],
    "50대": [7, 4, 4, 2, 2, 2, 2, 1, 1, 1, 0],
    "60대": [4, 2, 3, 1, 1, 1, 1, 0, 1, 0, 0]
})

data_2021_pattern = pd.DataFrame({
    "항목": ["무지(無地)", "벚꽃무늬(桜文)", "동백(椿)", "모란(牡丹)", "나비(蝶)", "창포(菖蒲)", "봉황(鳳凰)", "송죽매(松竹梅)", "부채(扇)", "학(鶴)", "스트라이프"],
    "20대": [9, 8, 7, 6, 4, 1, 1, 1, 1, 1, 3],
    "30대": [10, 8, 6, 6, 4, 2, 2, 2, 2, 1, 2],
    "40대": [7, 6, 5, 5, 2, 3, 2, 2, 2, 2, 1],
    "50대": [4, 4, 3, 3, 1, 2, 2, 2, 2, 2, 1],
    "60대": [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0]
})

data_2025_yukata_color = pd.DataFrame({
    "항목": ["남색(紺)", "검정(黒)", "파랑(青)", "하늘색(水色)", "보라(紫)", "흰색(白)", "초록(緑)", "핑크(ピンク)", "빨강(赤)"],
    "20대": [14, 7, 6, 7, 3, 5, 2, 4, 2],
    "30대": [18, 8, 7, 6, 5, 4, 3, 2, 1],
    "40대": [16, 6, 6, 4, 5, 3, 2, 1, 1],
    "50대": [11, 4, 4, 2, 3, 1, 1, 0, 0],
    "60대": [7, 2, 2, 1, 2, 1, 1, 0, 0]
})

data_2025_yukata_point = pd.DataFrame({
    "항목": ["색상/무늬 디자인", "착용감/소재 쾌적함", "가격/가성비", "실루엣/체형 커버", "착용 편의성", "트렌드/유행", "오비(허리띠) 코디", "SNS/사진발"],
    "20대": [24, 10, 14, 6, 5, 5, 3, 3],
    "30대": [25, 14, 12, 9, 8, 3, 2, 0],
    "40대": [19, 13, 10, 10, 9, 2, 1, 0],
    "50대": [11, 9, 5, 5, 6, 0, 1, 0],
    "60대": [7, 6, 3, 3, 4, 0, 0, 0]
})

# 사이드바 필터 설정
st.sidebar.header("🔍 조회 옵션")
survey_choice = st.sidebar.radio(
    "설문조사 선택",
    ["2021년 기모노 선호도 조사", "2025년 유카타 트렌드 조사"]
)

age_groups = ["20대", "30대", "40대", "50대", "60대"]
selected_ages = st.sidebar.multiselect(
    "연령대 선택 (다중 선택 가능)",
    options=age_groups,
    default=age_groups
)

if not selected_ages:
    st.warning("최소 1개 이상의 연령대를 선택해주세요.")
    st.stop()

# 내림차순 가로 막대 그래프 생성 함수 (가나다순 방지)
def draw_descending_chart(df, title, ages):
    # 선택된 연령대의 합계 계산 및 내림차순 정렬
    df_calc = df.copy()
    df_calc["선택 연령대 합계"] = df_calc[ages].sum(axis=1)
    df_calc = df_calc.sort_values(by="선택 연령대 합계", ascending=False)
    
    # 누적 막대 그래프를 위한 데이터 변환 (Melt)
    df_melted = df_calc.melt(
        id_vars=["항목", "선택 연령대 합계"],
        value_vars=ages,
        var_name="연령대",
        value_name="득표수"
    )

    # Altair 차트 (sort='-x'를 통해 가나다순이 아닌 수치 내림차순 강제 적용)
    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X("sum(득표수):Q", title="득표수 (표)"),
        y=alt.Y("항목:N", sort="-x", title="응답 항목"),
        color=alt.Color("연령대:N", scale=alt.Scale(scheme="tableau10"), title="연령대"),
        tooltip=["항목", "연령대", "득표수", "선택 연령대 합계"]
    ).properties(
        title=title,
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    with st.expander(f"📊 '{title}' 상세 데이터 표 보기 (내림차순)"):
        display_cols = ["항목", "선택 연령대 합계"] + ages
        st.dataframe(df_calc[display_cols], hide_index=True, use_container_width=True)

# 화면 출력
col1, col2 = st.columns(2)

if survey_choice == "2021년 기모노 선호도 조사":
    with col1:
        draw_descending_chart(data_2021_color, "선호하는 기
