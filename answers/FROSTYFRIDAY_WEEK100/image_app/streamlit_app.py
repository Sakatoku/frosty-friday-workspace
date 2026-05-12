# Import Python packages
import streamlit as st
import os
import pandas as pd

# タイトル
st.title(f"🎉FrostyFriday 100回記念🎉")

# Snowflakeのテーブルからデータを読み込む
@st.cache_data
def fetch_data(_session) -> pd.DataFrame:
    # Query
    sql_query = """
        select file_name, image_bytes
        from frostyfriday_db.week100.images
        """
    snowpark_df = _session.sql(sql_query)
    df = snowpark_df.to_pandas()
    return df

# Snowflakeと接続
conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
session = conn.session()

# データ読み込み
df = fetch_data(session)

# セレクトボックスでイメージを選択
selected_image = st.selectbox("Select image", df["FILE_NAME"])
if selected_image is None:
    st.stop()

# 16進数の文字列から2進数のバイト列に変換(デコード)
hex_string = df.loc[df["FILE_NAME"] == selected_image, "IMAGE_BYTES"].values[0]
image_bytes = bytes.fromhex(hex_string)

# 画像を表示
st.write("filename: ", selected_image)
st.image(image_bytes)

st.divider()
st.page_link("pages/multimodal.py", label="後編へ続く", icon="🔍")