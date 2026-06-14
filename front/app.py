import streamlit as st
import requests

st.set_page_config(page_title="SDVX Recommender", layout="wide")

st.title("사운드볼텍스 18레벨 추천")
st.markdown("### 학번: 2023204058 / 이름: 이재현")
st.divider()

# 사용자 입력
st.subheader("곡 조건 설정")
col1, col2 = st.columns(2)

with col1:
    lv_range = st.slider("선호 레벨대", 18.0, 18.8, (18.1, 18.5), 0.1)

with col2:
    pattern_list = ["노브", "원핸드", "계단", "폭타", "연타", "트릴"]
    user_patterns = st.multiselect("선호 패턴", pattern_list, default=["노브"])

st.write("") 

# 추천 요청
if st.button("곡 추천", use_container_width=True):
    if not user_patterns:
        st.warning("선호 패턴을 최소 1개 이상 선택하세요.")
    else:
        req_data = {
            "min_lv": lv_range[0],
            "max_lv": lv_range[1],
            "patterns": user_patterns
        }
        
        try:
            res = requests.post("http://backend:8000/recommend", json=req_data)
            data = res.json()
            
            # 결과
            st.divider()
            st.subheader("결과")
            
            if data["status"] == "success":
                st.success("조건에 맞는 곡입니다.")
                
                songs = data["recommendations"]
                cols = st.columns(len(songs))
                
                for i, s in enumerate(songs):
                    with cols[i]:
                        st.info(f"**{s['title']}**")
                        st.metric(label="Level", value=s["level"])
                        st.metric(label="BPM", value=s["bpm"])
                        st.caption(f"주 패턴: {', '.join(s['patterns'])}")
            else:
                st.error(data["message"])
                
        except Exception:
            st.error("서버 연결 실패.")
