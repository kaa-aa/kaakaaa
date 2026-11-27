import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Kimono & Yukata", layout="wide")
st.title("👘 기모노 & 유카타 분석 (1920s~2025)")

d_2021_c = pd.DataFrame({
    "항목": ["남색", "검정", "보라", "핑크", "하늘색", "파랑", "빨강", "흰색", "초록", "주황", "노랑"],
    "20대": [8, 5, 3, 8, 7, 4, 5, 2, 1, 2, 1],
    "30대": [12, 7, 6, 6, 5, 5, 4, 2, 2, 2, 1],
    "40대": [10, 6, 6, 4, 4, 4, 3, 2, 2, 1, 0],
    "50대": [7, 4, 4, 2, 2, 2, 2, 1, 1, 1, 0],
    "60대": [4, 2, 3, 1, 1, 1, 1, 0, 1, 0, 0]
})

d_2021_p = pd.DataFrame({
    "항목": ["무지", "벚꽃", "동백", "모란", "나비", "창포", "봉황", "송죽매", "부채", "학", "스트라이프"],
    "20대": [9, 8, 7, 6, 4, 1, 1, 1, 1, 1, 3],
    "30대": [10, 8, 6, 6, 4, 2, 2, 2, 2, 1, 2],
    "40대": [7, 6, 5, 5, 2, 3, 2, 2, 2, 2, 1],
    "50대": [4, 4, 3, 3, 1, 2, 2, 2, 2, 2, 1],
    "60대": [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 0]
})

d_2025_c = pd.DataFrame({
    "항목": ["남색", "검정", "파랑", "하늘색", "보라", "흰색", "초록", "핑크", "빨강"],
    "20대": [14, 7, 6, 7, 3, 5, 2, 4, 2],
    "30대": [18, 8, 7, 6, 5, 4, 3, 2, 1],
    "40대": [16, 6, 6, 4, 5, 3, 2, 1, 1],
    "50대": [11, 4, 4, 2, 3, 1, 1, 0, 0],
    "60대": [7, 2, 2, 1, 2, 1, 1, 0, 0]
})

d_2025_p = pd.DataFrame({
    "항목": ["디자인", "착용감", "가성비", "체형커버", "편의성", "트렌드", "코디", "사진발"],
    "20대": [24, 10, 14, 6, 5, 5, 3, 3],
    "30대": [25, 14, 12, 9, 8, 3, 2, 0],
    "40대": [19, 13, 10, 10, 9, 2, 1, 0],
    "50대": [11, 9, 5, 5, 6, 0, 1, 0],
    "60대": [7, 6, 3, 3, 4, 0, 0, 0]
})

d_1920 = pd.DataFrame({
    "항목": ["잡지유행", "면직물보급", "일상복활용", "모던도안", "외출복정착"],
    "1920년대": [40, 45, 50, 35, 30],
    "1930년대": [55, 50, 45, 50, 45]
})

menu = st.sidebar.radio(
    "메뉴 선택",
    ["2021 기모노(20~60대)", "2025 유카타(20~60대)", "1920~1930년대 역사"]
)

def show_chart(df, title, cols, g_name="연령대"):
    tmp = df.copy()
    tmp["합계"] = tmp[cols].sum(axis=1)
    tmp = tmp.sort_values(by="합계", ascending=False)
    m = tmp.melt(
        id_vars=["항목", "합계"],
        value_vars=cols,
        var_name=g_name,
        value_name="수치"
    )
    c = alt.Chart(m).mark_bar().encode(
        x=alt.X("sum(수치):Q", title="수치"),
        y=alt.Y("항목:N", sort="-x", title="항목"),
        color=alt.Color(f"{g_name}:N", title=g_name),
        tooltip=["항목", g_name, "수치", "합계"]
    ).properties(title=title, height=380)
    st.altair_chart(c, use_container_width=True)
    st.dataframe(tmp[["항목", "합계"] + cols], hide_index=True)

if "1920" in menu:
    eras = ["1920년대", "1930년대"]
    sel = st.sidebar.multiselect("연대", eras, default=eras)
    if sel:
        show_chart(d_1920, "1920~1930년대 유카타 특징", sel, "연대")
        st.info("1920~30년대: 주부의 벗 등 대중잡지와 면직물 대량생산으로 유카타가 대중 패션으로 정착했습니다.")
else:
    ages = ["20대", "30대", "40대", "50대", "60대"]
    sel = st.sidebar.multiselect("연령대", ages, default=ages)
    if sel:
        c1, c2 = st.columns(2)
        if "2021" in menu:
            with c1:
                show_chart(d_2021_c, "2021 기모노 색상", sel)
            with c2:
                show_chart(d_2021_p, "2021 기모노 무늬", sel)
        else:
            with c1:
                show_chart(d_2025_c, "2025 유카타 색상", sel)
            with c2:
                show_chart(d_2
