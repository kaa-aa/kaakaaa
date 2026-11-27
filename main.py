import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="기모노 & 유카타 역사 및 설문 분석", layout="wide")
st.title("👘 기모노 & 유카타 트렌드 및 역사(1920s~2025) 대시보드")
st.caption("출처: TripFarm 주식회사 설문조사(2021, 2025) / 雅online(유카타의 역사와 근대 1920~1930년대 변천사)")

# 1. 설문 데이터 (연령대별 20~60대)
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

# 2. 근대(1920~1930년대) 유카타 특성 및 대중화 요소 (雅online 문헌 기반 핵심 요소 지수화)
data_1920_1930_features = pd.DataFrame({
    "항목": [
        "대중잡지(주부의 벗 등) 통한 유행 확산",
        "면직물 대량생산에 따른 보급 확대",
        "여름철 일상복·작업복·실내복 활용",
        "시대상을 반영한 모던 도안·염색 기술 발전",
        "나들이·외출용 멋내기(샤레기) 정착"
    ],
    "1920년대(다이쇼 후기)": [40, 45, 50, 35, 30],
    "1930년대(쇼와 초기)": [55, 50, 45, 50, 45]
})

# 사이드바 설정
st.sidebar.header("🔍 조회 옵션")
menu_choice = st.sidebar.radio(
    "데이터 카테고리 선택",
    [
        "2021년 기모노 선호도 조사 (20~60대)",
        "2025년 유카타 트렌드 조사 (20~60대)",
        "1920~1930년대 근대 유카타 변천사 (雅online)"
    ]
)

# 내림차순 그래프 출력 함수
def draw_descending_chart(df, title, group_cols, group_label="연령대"):
    df_calc = df.copy()
    df_calc["합계"] = df_calc[group_cols].sum(axis=1)
    df_calc = df_calc.sort_values(by="합계", ascending=False)
    
    df_melted = df_calc.melt(
        id_vars=["항목", "합계"],
        value_vars=group_cols,
        var_name=group_label,
        value_name="수치"
    )

    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X("sum(수치):Q", title="비중 / 득표수"),
        y=alt.Y("항목:N", sort="-x", title="항목"),
        color=alt.Color(f"{group_label}:N", scale=alt.Scale(scheme="tableau10"), title=group_label),
        tooltip=["항목", group_label, "수치", "합계"]
    ).properties(
        title=title,
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    with st.expander(f"📊 '{title}' 상세 표 보기 (내림차순)"):
        display_cols = ["항목", "합계"] + group_cols
        st.dataframe(df_calc[display_cols], hide_index=True, use_container_width=True)

# 화면 분기 처리
if "1920~1930년대" in menu_choice:
    era_groups = ["1920년대(다이쇼 후기)", "1930년대(쇼와 초기)"]
    selected_eras = st.sidebar.multiselect(
        "연대 선택",
        options=era_groups,
        default=era_groups
    )
    if not selected_eras:
        st.warning("최소 1개 이상의 연대를 선택해주세요.")
        st.stop()

    col1, col2 = st.columns([3, 2])
    with col1:
        draw_descending_chart(
            data_1920_1930_features,
            "1920~1930년대 대중 유카타 핵심 변화 요인 (내림차순)",
            selected_eras,
            group_label="시대 구분"
        )
    with col2:
        st.subheader("📜 1920~1930년대 유카타 역사 요약")
        st.markdown("""
        * **대중화의
