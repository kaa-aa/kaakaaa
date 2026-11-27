import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("👘 기모노 & 유카타 분석 (1920s~2025)")

d1 = pd.DataFrame({
    "항목": ["남색", "검정", "보라", "핑크", "하늘색", "파랑", "빨강", "흰색", "초록"],
    "20대": [8, 5, 3, 8, 7, 4, 5, 2, 1],
    "30대": [12, 7, 6, 6, 5, 5, 4, 2, 2],
    "40대": [10, 6, 6, 4, 4, 4, 3, 2, 2],
    "50대": [7, 4, 4, 2, 2, 2, 2, 1, 1],
    "60대": [4, 2, 3, 1, 1, 1, 1, 0, 1]
})

d2 = pd.DataFrame({
    "항목": ["무지", "벚꽃", "동백", "모란", "나비", "창포", "봉황", "송죽매", "부채"],
    "20대": [9, 8, 7, 6, 4, 1, 1, 1, 1],
    "30대": [10, 8, 6, 6, 4, 2, 2, 2, 2],
    "40대": [7, 6, 5, 5, 2, 3, 2, 2, 2],
    "50대": [4, 4, 3, 3, 1, 2, 2, 2, 2],
    "60대": [2, 2, 2, 2, 1, 1, 1, 1, 1]
})

d3 = pd.DataFrame({
    "항목": ["남색", "검정", "파랑", "하늘색", "보라", "흰색", "초록", "핑크", "빨강"],
    "20대": [14, 7, 6, 7, 3, 5, 2, 4, 2],
    "30대": [18, 8, 7, 6, 5, 4, 3, 2, 1],
    "40대": [16, 6, 6, 4, 5, 3, 2, 1, 1],
    "50대": [11, 4, 4, 2, 3, 1, 1, 0, 0],
    "60대": [7, 2, 2, 1, 2, 1, 1, 0, 0]
})

d4 = pd.DataFrame({
    "항목": ["잡지유행", "면직물보급", "일상복활용", "모던도안", "외출복정착"],
    "1920년대": [40, 45, 50, 35, 30],
    "1930년대": [55, 50, 45, 50, 45]
})

m = st.sidebar.radio("선택", ["2021 기모노", "2025 유카타", "1920~30년대"])

def plot(df, title, cols, g="연령대"):
    t = df.copy()
    t["합계"] = t[cols].sum(axis=1)
    t = t.sort_values("합계", ascending=False)
    ml = t.melt(["항목", "합계"], cols, g, "수치")
    c = alt.Chart(ml).mark_bar().encode(
        x="sum(수치):Q", y=alt.Y("항목:N", sort="-x"), color=f"{g}:N"
    ).properties(title=title, height=350)
    st.altair_chart(c, use_container_width=True)
    st.dataframe(t[["항목", "합계"] + cols], hide_index=True)

if "1920" in m:
    s = st.sidebar.multiselect("연대", ["1920년대", "1930년대"], default=["1920년대", "1930년대"])
    if s:
        plot(d4, "1920~1930년대 유카타 특징", s, "연대")
else:
    ages = ["20대", "30대", "40대", "50대", "60대"]
    s = st.sidebar.multiselect("연령대", ages, default=ages)
    if s:
        if "2021" in m:
            plot(d1, "2021 기모노 색상", s)
            plot(d2, "2021 기모노 무늬", s)
        else:
            plot(d3, "2025 유카타 색상", s)
