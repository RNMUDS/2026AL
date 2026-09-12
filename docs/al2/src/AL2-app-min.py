# いちばん小さい Streamlit アプリ
# ターミナルで  streamlit run app.py  と打つと、ブラウザに画面が出る
import streamlit as st

st.title("迷路アプリ")

size = st.slider("迷路の大きさ", 3, 10, 5)       # スライダーで数を選べる
st.write(f"{size} × {size} の迷路を作ります")

if st.button("解く"):                            # ボタンを押したときだけ動く
    st.success("ここに結果を表示する")
