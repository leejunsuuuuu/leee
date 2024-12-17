import streamlit as st
import pandas as pd

# Streamlit 앱 제목
st.title("학원 정보 제공 플랫폼")
st.write("공공 데이터를 기반으로 학원의 정보를 검색하세요.")

# 데이터 불러오기
file_path = "academy.csv"

try:
    academy_df = pd.read_csv(file_path, encoding='cp949')  # 파일 로드
except FileNotFoundError:
    st.error("학원 데이터 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
    st.stop()

# 데이터 전처리: 결측치 제거
academy_df.dropna(subset=['학원명', '도로명주소'], inplace=True)

# 중복 데이터 처리: 학원명과 도로명주소 기준으로 중복 제거
academy_df.drop_duplicates(subset=['학원명', '도로명주소'], inplace=True)

# 사용자 입력: 시도교육청명 (지역명)
region = st.text_input("지역을 입력하세요 (예: 강남구, 안동시)").strip()

# 검색 버튼
if st.button("검색", key="search_button_unique"):
    if region:
        # 입력된 지역명으로 데이터 필터링
        filtered_data = academy_df[academy_df["행정구역명"].str.contains(region, na=False)]

        # 결과 출력
        if not filtered_data.empty:
            st.success(f"{len(filtered_data)}개의 학원을 찾았습니다.")
            for _, row in filtered_data.iterrows():
                st.subheader(row["학원명"])
                st.write(f"교습과정: {row['교습과정명']}")
                st.write(f"주소: {row['도로명주소']}")
                st.write(f"전화번호: {row['전화번호']}")
                st.write("---")
        else:
            st.warning("검색 결과가 없습니다.")
    else:
        st.warning("지역명을 입력하세요.")