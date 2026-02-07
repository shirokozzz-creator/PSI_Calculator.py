import streamlit as st
from fpdf import FPDF
import random
import io

# 設定網頁標題
st.set_page_config(page_title="PSI 派大星指數 - 全球通用版", page_icon="🧬")

# 1. 初始化題目隨機權重 (放在 Session State 防止重新整理就跑掉)
if 'weights' not in st.session_state:
    # 為每題生成一個 (0, 5, 10) 的隨機排列
    st.session_state.weights = [random.sample([0, 5, 10], 3) for _ in range(10)]

st.title("🧬 PSI 派大星指數 (General Version)")
st.markdown("""
**目標**：診斷個體在當前環境下的「認知熵增」與「平庸化」程度。
---
""")

# --- 第一部分：基礎數據輸入 ---
st.header("👤 受測者基本資料")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("年齡", min_value=10, max_value=100, value=30)
    height = st.number_input("身高 (cm)", min_value=100, max_value=250, value=170)
with col2:
    weight = st.number_input("體重 (kg)", min_value=30, max_value=200, value=65)
    body_fat = st.number_input("體脂率 (%)", min_value=5.0, max_value=50.0, value=20.0, step=0.1)

# --- 第二部分：通用診斷題目 ---
st.header("📝 認知與環境診斷")

questions = [
    ("1. 對於目前的職業現狀，你的思維是？", ["追求絕對穩定，風險越低越好", "在穩定中尋求自我價值的突破", "主動擁抱變動，視危機為槓桿"]),
    ("2. 關於下班後的閒暇時間利用？", ["主要用於娛樂放鬆、舒緩工作壓力", "隨意安排，看當天心情而定", "有系統地學習新技能或經營複利資產"]),
    ("3. 面對複雜且未知的技術問題時？", ["傾向交給專家處理，不深究底層邏輯", "嘗試理解基本原理，但遇到困難會停下", "運用底層邏輯拆解，直到徹底掌握關鍵"]),
    ("4. 你對目前生活環境的『危機感』程度？", ["非常安逸，覺得現狀可以維持一輩子", "偶爾感到焦慮，但不知如何行動", "具備強烈積極不適感，並轉化為具體產出"]),
    ("5. 關於個人財務思維？", ["沒有具體規劃，領薪水後隨意開支", "有儲蓄習慣，主要靠勞力換取報酬", "精算資產配置，致力於將消費轉化為資產"]),
    ("6. 社交圈的內容大多圍繞在？", ["抱怨政策、明星八卦或瑣碎日常", "生活情報分享、美食或一般娛樂", "財富增長、技術進步與哲學思考"]),
    ("7. 面對身體素質（體態/健康）的自我管理？", ["順其自然，不刻意節制", "有意識地管理，但缺乏數據化監控", "視體態為個人競爭力，嚴格數據化管理"]),
    ("8. 學習新知識的頻率與深度？", ["很久沒有讀完一整本專業書籍", "被動接受資訊碎片，隨看隨忘", "每天主動攝取高含金量知識並內化"]),
    ("9. 對於『時間』的認知？", ["時間是可以用來換取金錢或娛樂的資源", "覺得時間過得很快，但不清楚產出為何", "時間是生命中最珍貴的資產，極度排斥熵增"]),
    ("10. 如果現在失去穩定的薪水收入？", ["會陷入恐慌，因為缺乏其他生存技能", "雖然擔心，但應該能勉強支撐一段時間", "充滿信心，因為具備強大的市場競爭力"])
]

user_responses = []
with st.form("psi_form"):
    for i, (q_text, opts) in enumerate(questions):
        st.write(f"**{q_text}**")
        # 顯示選項，但背後對應隨機權重
        choice = st.radio(f"Select_{i}", opts, label_visibility="collapsed")
        user_responses.append(opts.index(choice))
    
    submitted = st.form_submit_button("產出診斷報告")

# --- 第三部分：計算結果與 PDF 產出 ---
if submitted:
    # 計算分數
    total_score = sum(st.session_state.weights[i][user_responses[i]] for i in range(10))
    
    st.divider()
    st.subheader(f"📊 診斷結果：PSI 指數 {total_score}%")
    
    # 診斷語句
    diagnosis = ""
    if total_score <= 25:
        diagnosis = "【航太級靈魂】你具備強大的自我驅動力，完全在對抗熵增。"
        st.success(diagnosis)
    elif total_score <= 50:
        diagnosis = "【認知生鏽預警】環境已開始侵蝕你的意志，建議啟動神經重塑。"
        st.warning(diagnosis)
    else:
        diagnosis = "【深度海星狀態】警報！你已陷入習得性平庸，急需強烈外力干預。"
        st.error(diagnosis)

    # 生成 PDF
   def generate_pdf(age, height, weight, body_fat, total_score, diagnosis):
    pdf = FPDF()
    pdf.add_page()
    
    # 關鍵步驟：載入你上傳的字型檔
    # 確保檔案路徑與你在 GitHub 上傳的路徑一致
    try:
        pdf.add_font('MSJH', '', 'msjh.ttc') 
        pdf.set_font('MSJH', size=12)
        title_text = "PSI 派大星指數診斷報告"
        diagnosis_label = "診斷結果："
    except:
        # 如果字型載入失敗，退回標準字型（僅支援英文）
        pdf.set_font("Arial", size=12)
        title_text = "PSI Diagnosis Report"
        diagnosis_label = "Diagnosis: "

    pdf.cell(200, 10, txt=title_text, ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Age: {age}  |  Body Fat: {body_fat}%", ln=True)
    pdf.cell(200, 10, txt=f"Final PSI Score: {total_score}%", ln=True)
    
    # 處理中文顯示
    pdf.multi_cell(0, 10, txt=f"{diagnosis_label} {diagnosis}")
    
    return pdf.output()

# 在 Streamlit 下載按鈕處呼叫
if submitted:
    # ... (計算分數與診斷邏輯) ...
    pdf_bytes = generate_pdf(age, height, weight, body_fat, total_score, diagnosis)
    st.download_button(
        label="📥 下載 PDF 診斷報告",
        data=bytes(pdf_bytes),
        file_name="PSI_Report.pdf",
        mime="application/pdf"
    )
