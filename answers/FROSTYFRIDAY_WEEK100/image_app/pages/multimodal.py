import streamlit as st
import os
import pandas as pd

st.title("🔍 マルチモーダル分析")

sql_query = """
SELECT
    ID,
    DESCRIPTION,
    FL_GET_RELATIVE_PATH(FILE_COL) AS REL_PATH,
    FL_GET_CONTENT_TYPE(FILE_COL) AS CONTENT_TYPE,
    SNOWFLAKE.CORTEX.AI_COMPLETE(
        'gemini-3.1-pro',
        'この画像または動画の内容を100文字以内の日本語で説明してください。',
        FILE_COL
    ) AS AI_SUMMARY,
    GET_PRESIGNED_URL(
        @FROSTYFRIDAY_DB.WEEK100.MEDIA_STAGE,
        FL_GET_RELATIVE_PATH(FILE_COL),
        3600
    ) AS PRESIGNED_URL
FROM FROSTYFRIDAY_DB.WEEK100.MEDIA_TABLE
"""
with st.expander("実行しているSQL"):
    st.code(sql_query)

conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
session = conn.session()

@st.cache_data
def fetch_media_with_analysis(_session) -> pd.DataFrame:
    return _session.sql(sql_query).to_pandas()

df = fetch_media_with_analysis(session)

options = df["DESCRIPTION"].tolist()
selected = st.selectbox("メディアを選択", options)
if selected is None:
    st.stop()

row = df[df["DESCRIPTION"] == selected].iloc[0]

st.subheader(f"📄 {row['DESCRIPTION']}（{row['REL_PATH']}）")

content_type = row["CONTENT_TYPE"]
url = row["PRESIGNED_URL"]

if content_type.startswith("image/"):
    st.image(url)
elif content_type.startswith("video/"):
    st.video(url)

st.subheader("🤖 Geminiによる分析結果")
st.info(row["AI_SUMMARY"])
