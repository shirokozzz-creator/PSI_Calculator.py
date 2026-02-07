import streamlit as st
from fpdf import FPDF
import random
import io

# --- 1. PDF 產出函數 (支援中文路徑偵測) ---
def generate_psi_pdf(age, height, weight, body_fat, total_score, diagnosis_title, diagnosis_msg):
    pdf = FPDF()
    pdf.add_page()
    try:
        # 確保 msjh.ttc 已從 Brian-car-ai 下載並上傳至本專案根目錄
        pdf.add_font('MSJH', '', 'msjh.ttc')
        pdf.set_font('MSJH', size=14)
        title = "PSI 派大星指數 - 航太級個人鑑定報告"
        result_label = f"最終 PSI 指數：{total_score}%"
        diag_label = "專家鑑定結論："
    except:
        pdf.set_font("Arial", size=12)
        title = "PSI Diagnosis Report"
        result_label = f"Final PSI Score: {total_score}%"
        diag_label = "Diagnosis:"

    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font_size(11)
    pdf.cell(200, 10, txt=f"受測者數據：{height}cm / {weight}kg / {body_fat}% 體脂", ln=True)
    pdf.cell(200, 10, txt=f"受測年齡：{age} 歲", ln=True)
    pdf.ln(5)
    pdf.set_font_size(16)
    pdf.cell(200, 15, txt=result_label, ln=True)
    pdf.ln(5)
    pdf.set_font_size(12)
    pdf.multi_cell(0, 10, txt=f"{diag_label} \n{diagnosis_title}\n{diagnosis_msg}")
    pdf.ln(20)
    pdf.set_font_size(10)
    pdf.cell(200, 10, txt="Brian Aerospace Data Car Selection Office - 2026", ln=True, align='R')
    return pdf.output()

# --- 2. 介面設定 ---
st.set_page_config(page_title="PSI 派大星指數 - 航太級數據鑑定", page_icon="🚀", layout="wide")

# 初始化隨機權重 (防止作弊，強化真相)
if 'weights' not in st.session_state:
    st.session_state.weights = [random.sample([0, 5, 10], 3) for _ in range(10)]

st.title("🚀 PSI 派大星指數 (Brian 航太數據監控版)")
st.markdown("""
**目標**：透過數據化分析，診斷您是否正被「平庸環境」吞噬。  
**風格**：中肯、穩重、有一說一。
---
""")

# --- 3. 基礎數據 (側邊欄) ---
st.sidebar.header("📊 硬體數據同步")
age = st.sidebar.number_input("年齡", value=41) #
height = st.sidebar.number_input("身高 (cm)", value=181.0) #
weight = st.sidebar.number_input("體重 (kg)", value=74.0) #
body_fat = st.sidebar.number_input("體脂率 (%)", value=19.5, step=0.1) #

# --- 4. 診斷測驗 ---
st.header("📝 認知與熵增水平測驗")
questions = [
    ("1. 關於財務 1000 萬目標，你的思維是？", ["追求絕對穩定，風險越低越好", "在穩定中尋求自我價值的突破", "主動擁抱變動，視危機為槓桿"]),
    ("2. 關於下班後的閒暇時間利用？", ["主要用於娛樂放鬆、舒緩壓力", "隨意安排，看當天心情而定", "有系統地學習新技能或經營複利資產"]),
    ("3. 面對 Prius 3 維修（如 EGR/ABS）等技術難題時？", ["傾向交給專家處理，不深究細節", "嘗試理解原理，但遇到困難會停下", "運用底層邏輯拆解，直到徹底掌握"]),
    ("4. 你對目前生活環境的『危機感』程度？", ["非常安逸，覺得現狀可以維持一輩子", "偶爾焦慮，但不知如何行動", "具備強烈積極不適感，並轉化為產出"]),
    ("5. 關於個人資產配置？", ["沒有規劃，領薪水後隨意開支", "有儲蓄習慣，靠勞力換取報酬", "精算資產，致力將消費轉化為資產"]),
    ("6. 社交圈的內容通常圍繞在？", ["抱怨政策、明星八卦或瑣碎日常", "生活情報、美食或一般娛樂", "財富增長、技術進步與哲學思考"]),
    ("7. 面對身體素質（體態/數據）管理？", ["順其自然，不刻意節制", "有意識管理，但缺乏數據監控", "視體態為競爭力，嚴格數據化管理"]),
    ("8. 學習新知識的頻率與深度？", ["很久沒有讀完一整本專業書籍", "被動接受資訊碎片，隨看隨忘", "每天主動攝取高金量知識並內化"]),
    ("9. 對於『時間』的認知？", ["時間是用來換取金錢或娛樂的資源", "覺得時間過得很快，產出不明確", "時間是最珍貴資產，極度排斥熵增"]),
    ("10. 如果現在失去國營事業/穩定收入？", ["會陷入恐慌，因為缺乏生存技能", "雖然擔心，但能支撐一段時間", "充滿信心，因為具備強大市場競爭力"])
]

responses = []
with st.form("psi_form"):
    for i, (q_text, opts) in enumerate(questions):
        st.write(f"**{q_text}**")
        choice = st.radio(f"Select_{i}", opts, label_visibility="collapsed")
        responses.append(opts.index(choice))
    submitted = st.form_submit_button("執行航太級數據分析")

# --- 5. 結果呈現與衝擊視覺 ---
if submitted:
    total_score = sum(st.session_state.weights[i][responses[i]] for i in range(10))
    
    # 決定顏色與衝擊標語
    if total_score <= 25:
        color, title, msg = "#28a745", "【 航太級靈魂 】", "你成功抵禦了環境熵增，目前依然掌控著自己的航太引擎。"
    elif total_score <= 50:
        color, title, msg = "#ffc107", "【 認知生鏽預警 】", "警報：平庸感正在侵蝕你的神經，你快要變成派大星了！"
    else:
        color, title, msg = "#dc3545", "【 深度海星狀態 】", "危險！你的大腦已進入靜態損壞，再不行動就真的變成了廢柴中油大叔！"

    # 震撼 UI 輸出
    st.markdown(f"""
        <div style="text-align: center; padding: 40px; border: 10px solid {color}; border-radius: 30px; background-color: #f8f9fa;">
            <h1 style="color: {color}; font-size: 50px; margin-bottom: 0;">{title}</h1>
            <p style="font-size: 120px; font-weight: 900; color: {color}; margin: 0; line-height: 1;">{total_score}%</p>
            <h2 style="color: #666; letter-spacing: 5px;">PSI 派大星指數</h2>
            <div style="background-color: {color}; color: white; padding: 15px; font-size: 24px; font-weight: bold; border-radius: 10px;">
                {msg}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 全球對照表
    st.subheader("📊 全球數據比對分析")
    st.table({
        "群體分類": ["專業工程師", "Brian 當前狀態", "一般上班族", "長期安逸者"],
        "平均 PSI 指數": ["10-20%", "25-35%", "45-60%", "75-100%"],
        "評語": ["高強度對抗熵增", "認知生鏽警戒期", "習得性平庸起點", "完全海星化"]
    })

    # PDF 下載
    pdf_bytes = generate_psi_pdf(age, height, weight, body_fat, total_score, title, msg)
    st.download_button(
        label="📥 領取航太級數據鑑定報告 (PDF)",
        data=bytes(pdf_bytes),
        file_name=f"PSI_Report_{age}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
