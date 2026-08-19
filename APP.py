import io
import re
import pandas as pd
import streamlit as st
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="RIESTI - 인보이스 제품명 정밀 검수 시스템",
    page_icon="🔍",
    layout="wide",
)

# ---------------------------------------------------------
# [1] 베트남 공표확인서 기준 정식 제품명 데이터베이스 (DB)
# ---------------------------------------------------------
OFFICIAL_DB = {
    "KLAVUU": [
        "KLAVUU WHITE PEARLSATION IDEAL ACTRESS BACKSTAGE CREAM 3 SPF30 PA++ MINT",
        "KLAVUU WHITE PEARLSATION IDEAL ACTRESS BACKSTAGE CREAM SPF30 PA++ ROSE",
        "KLAVUU White Pearlsation Ideal Actress Backstage Cream Spf30 Pa++Lavender",
        "KLAVUU BLUE PEARLSATION HIGH COVERAGE MARINE COLLAGEN AQUA CUSHION 21 SPF50+ PA+++ SUNSCREEN",
        "KLAVUU BLUE PEARLSATION HIGH COVERAGE MARINE COLLAGEN AQUA CUSHION 23 SPF50+ PA+++ SUNSCREEN",
        "KLAVUU BLUE PEARLSATION HIGH COVERAGE MARINE COLLAGEN AQUA CUSHION",
        "KLAVUU URBAN PEARLSATION HIGH COVERAGE TENSION CUSHION EX 21 LIGHT BEIGE SPF50+ PA++++",
        "KLAVUU URBAN PEARLSATION HIGH COVERAGE TENSION CUSHION EX 23 MEDIUM BEIGE SPF50+ PA++++",
        "KLAVUU URBAN PEARLSATION HIGH COVERAGE TENSION CUSHION EX",
        "KLAVUU VEGAN ZINC SUNCREAM SPF50+PA++++",
        "KLAVUU Real Vegan Collagen Ampoule",
        "KLAVUU Real Vegan Collagen Cream",
        "KLAVUU Real Vegan Hyaluronic Acid Ampoule",
        "KLAVUU Real Vegan Vitamin Ampoule",
        "KLAVUU Nourishing Care Lip Sleeping Pack Berry",
        "KLAVUU Nourishing Care Lip Sleeping Pack Coconut",
        "KLAVUU Nourishing Care Lip Sleeping Pack Vanilla",
        "KLAVUU PHYTONCIDE QUICK CLEANSING PAD",
        "KLAVUU PHYTONCIDE MILD CLEANSING FOAM",
        "KLAVUU GREEN PEARLSATION TEATREE CARE BODY SPRAY",
        "KLAVUU URBAN PEARLSATION SPARKLE EYESHADOW #SP1 MARIGOLD PEACH",
        "KLAVUU URBAN PEARLSATION SPARKLE EYESHADOW #SP2 SILVER LILAC",
        "KLAVUU URBAN PEARLSATION SPARKLE EYESHADOW #SP3 CRYSTAL GOLD",
        "KLAVUU URBAN PEARLSATION SPARKLE EYESHADOW #SP4 GLAM BROWN",
        "KLAVUU URBAN PEARLSATION SPARKLE EYESHADOW #SP5 MIDNIGHT PINK",
    ],
    "TIRTIR": [
        "TIRTIR WATERISM GLOW TINT 01 MAUVE ROSE",
        "TIRTIR WATERISM GLOW TINT 02 MERRY CORAL",
        "TIRTIR WATERISM GLOW TINT 03 SAND MOND",
        "TIRTIR WATERISM GLOW TINT 04 FIG PEACH",
        "TIRTIR WATERISM GLOW TINT 05 SCOTCH SHOT",
        "TIRTIR WATERISM GLOW TINT 06 HONEY NUT",
        "TIRTIR WATERISM GLOW TINT 07 CASSIS PLUM",
        "TIRTIR WATERISM GLOW TINT 09 SALMON SYRUP",
        "TIRTIR WATERISM GLOW TINT 13 LIKELY",
        "TIRTIR WATERISM GLOW TINT 14 ROSE BELL",
        "TIRTIR WATERISM GLOW TINT 16 TANGERINGN",
        "TIRTIR WATERISM GLOW TINT 17 ALIVEN",
        "TIRTIR WATERISM GLOW TINT 18 CHERRID",
        "TIRTIR WATERISM GLOW TINT 19 BAD ROSY",
        "TIRTIR WATERISM GLOW TINT 20 FEVER RED",
        "TIRTIR WATERISM GLOW TINT 21 FIG ME",
        "TIRTIR WATERISM GLOW TINT 22 SNOWY PEACH",
        "TIRTIR WATERISM GLOW TINT 23 PEACHRICOT",
        "TIRTIR WATERISM GLOW TINT 24 LOVABLY",
        "TIRTIR WATERISM GLOW TINT 25 NUTTY PINK",
        "TIRTIR WATERISM GLOW TINT 26 BAREBLE",
        "TIRTIR WATERISM GLOW TINT 27 MUTY ROSE",
        "TIRTIR WATERISM GLOW TINT 28 WINTERY",
        "TIRTIR WATERISM GLOW TINT 29 EVENY",
        "TIRTIR WATERISM GLOW TINT 30 MAUVE BLUSH",
        "TIRTIR MASK FIT RED CUSHION 17C PORCELAIN",
        "TIRTIR MASK FIT RED CUSHION 17N VANILLA",
        "TIRTIR MASK FIT RED CUSHION 17W FRENCH VANILLA",
        "TIRTIR MASK FIT RED CUSHION 21C COOL IVORY",
        "TIRTIR MASK FIT RED CUSHION 21N IVORY",
        "TIRTIR MASK FIT RED CUSHION 21W NATURAL IVORY",
        "TIRTIR MASK FIT RED CUSHION 22C PEACH BEIGE",
        "TIRTIR MASK FIT RED CUSHION 22N SHELL BEIGE",
        "TIRTIR MASK FIT RED CUSHION 22W SHEER BEIGE",
        "TIRTIR MASK FIT RED CUSHION 23N SAND",
        "TIRTIR MASK FIT RED CUSHION 24N LATTE",
        "TIRTIR MASK FIT RED CUSHION 24W SOFT BEIGE",
        "TIRTIR MASK FIT RED CUSHION 27C COOL BEIGE",
        "TIRTIR MASK FIT RED CUSHION 27N CAMEL",
        "TIRTIR MASK FIT RED CUSHION 28N OAT",
        "TIRTIR MASK FIT RED CUSHION 29C TAUPE BEIGE",
        "TIRTIR MASK FIT RED CUSHION 29N NATURAL BEIGE",
        "TIRTIR MILK SKIN TONER",
        "TIRTIR SOS SERUM",
    ],
    "K-SECRET": [
        "K-SECRET SEOUL 1988 SERUM  RETINAL LIPOSOME 2% + BLACK GINSENG",
        "K-SECRET SEOUL 1988 EYE CREAM  RETINAL LIPOSOME 4% + FERMENTED BEAN",
        "K-SECRET SEOUL 1988 CREAM  RETINAL LIPOSOME 1% + FERMENTED RICE",
        "K-SECRET SEOUL 1988 SUN  PINE TREE + CERAMIDE",
        "K-SECRET SEOUL 1988 ESSENCE  SNAIL MUCIN 97% + RICE",
        "K-SECRET SEOUL 1988 CLEANSING FOAM  PINE CICA 1% + PROBIOTICS",
        "K-SECRET INSTANT RELIEF EYE GEL PATCHES",
        "K-SECRET EXTRA ILLUMINATING EYE GEL PATCHES",
        "K-SECRET ADVANCED REGENERATING EYE GEL PATCHES",
    ],
    "UNPA": [
        "unpa Bubi Bubi Bubble Lip Scrub",
        "unpa Bubi Bubi Bubble Lip Scrub Red",
        "unpa Bubi Bubi Butter Lip Balm",
        "unpa Bubi Bubi Lip Ampoule",
        "unpa Bubi Bubi Lip Mask",
    ],
}

# 모든 정식 제품명을 1차원 리스트로 통합
ALL_OFFICIAL_NAMES = [
    name for sublist in OFFICIAL_DB.values() for name in sublist
]


def normalize_text(text):
    """대소문자/특수문자 제외 비교용 정규화 함수"""
    if not isinstance(text, str):
        return ""
    return re.sub(r"[^A-Za-z0-9]", "", text).lower()


def find_best_match(invoice_name):
    """인보이스 제품명과 가장 잘 일치하는 정식 DB 제품명 탐색"""
    if invoice_name in ALL_OFFICIAL_NAMES:
        return invoice_name, "100% 완벽 일치", "PASS"

    norm_inv = normalize_text(invoice_name)

    # 대소문자/특수문자 제외 후 완전 일치 여부 확인
    for official in ALL_OFFICIAL_NAMES:
        if norm_inv == normalize_text(official):
            return (
                official,
                "대소문자 / 띄어쓰기 / 특수문자 차이",
                "WARNING",
            )

    # 포함 관계 확인
    for official in ALL_OFFICIAL_NAMES:
        if norm_inv in normalize_text(official) or normalize_text(
            official
        ) in norm_inv:
            return official, "부분 일치 (단어/옵션 차이 가능성)", "WARNING"

    return "매칭되는 정식 DB 명칭 없음", "미등록 제품 (DB 확인 필요)", "FAIL"


# ---------------------------------------------------------
# [2] Streamlit UI 화면 구성
# ---------------------------------------------------------
st.title("🛡️ RIESTI - 베트남 통관용 INVOICE 검수 시스템")
st.subheader(
    "인보이스 엑셀 파일의 제품명이 베트남 공표확인서 정식 제품명과 100% 일치하는지 검수합니다."
)
st.write("---")

# 사이드바: 정식 DB 현황 표시
st.sidebar.header("📚 등록된 브랜드 DB 현황")
for brand, items in OFFICIAL_DB.items():
    st.sidebar.markdown(f"**{brand}**: `{len(items)}개 SKU`")

# 파일 업로드 컨트롤
uploaded_file = st.file_uploader(
    "📂 검수할 INVOICE 엑셀 파일(.xlsx)을 선택하세요", type=["xlsx"]
)

if uploaded_file is not None:
    try:
        # 엑셀 읽기
        df_raw = pd.read_excel(uploaded_file, sheet_name=0)

        # 인보이스에서 Description 항목 추출 (row 27부터 감지)
        items_list = []
        for idx, row in df_raw.iterrows():
            no_val = str(row.iloc[0]).strip()
            desc_val = str(row.iloc[1]).strip()

            # 숫자 연번으로 시작하는 품목 행 추출
            if no_val.isdigit() and desc_val and desc_val != "nan":
                items_list.append(
                    {"No": int(no_val), "Invoice_Name": desc_val}
                )

        if not items_list:
            st.error(
                "❌ 인보이스에서 제품목록(Description of Goods)을 추출하지 못했습니다. 서식을 확인해 주세요."
            )
        else:
            results = []
            pass_cnt, warn_cnt, fail_cnt = 0, 0, 0

            for item in items_list:
                no = item["No"]
                inv_name = item["Invoice_Name"]
                best_match, reason, status = find_best_match(inv_name)

                if status == "PASS":
                    pass_cnt += 1
                    status_label = "✅ 정상 (Pass)"
                elif status == "WARNING":
                    warn_cnt += 1
                    status_label = "⚠️ 불일치 (Warning)"
                else:
                    fail_cnt += 1
                    status_label = "❌ 미등록 (Fail)"

                results.append(
                    {
                        "No": no,
                        "검수 상태": status_label,
                        "인보이스 기재 제품명": inv_name,
                        "공표확인서 정식 제품명 (DB)": best_match,
                        "불일치 사유": reason,
                    }
                )

            df_result = pd.DataFrame(results)

            # 상단 결과 요약 대시보드
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("총 검수 품목", f"{len(results)}건")
            col2.metric("✅ 100% 일치", f"{pass_cnt}건")
            col3.metric("⚠️ 수정 필요 (불일치)", f"{warn_cnt}건")
            col4.metric("❌ DB 미등록", f"{fail_cnt}건")

            st.write("### 📋 세부 검수 결과")

            # 테이블 색상 하이라이트 함수
            def highlight_status(val):
                if "정상" in str(val):
                    return "background-color: #d4edda; color: #155724; font-weight: bold;"
                elif "불일치" in str(val):
                    return "background-color: #fff3cd; color: #856404; font-weight: bold;"
                else:
                    return "background-color: #f8d7da; color: #721c24; font-weight: bold;"

            st.dataframe(
                df_result.style.map(
                    highlight_status, subset=["검수 상태"]
                ),
                use_container_width=True,
            )

            # 엑셀 결과 다운로드 버튼 제공
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df_result.to_excel(
                    writer, index=False, sheet_name="Invoice_Check_Result"
                )
            excel_data = output.getvalue()

            st.download_button(
                label="📥 검수 결과 보고서 엑셀 다운로드",
                data=excel_data,
                file_name="INVOICE_검수결과_보고서.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        
TEMPLATE_FILE_PATH = "RIESTI Global Invoice sample.xlsx"

if os.path.exists(TEMPLATE_FILE_PATH):
    with open(TEMPLATE_FILE_PATH, "rb") as file:
        st.download_button(
            label="📥 RIESTI 표준 인보이스 양식 다운로드 (.xlsx)",
            data=file,
            file_name="RIESTI Global Invoice Standard Form.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.info("💡 등록된 표준 인보이스 양식 파일이 없습니다.")

DB_FILE = "official_db.json"

DEFAULT_DB = {
    "KLAVUU": [
        "KLAVUU VEGAN ZINC SUNCREAM SPF50+PA++++",
        "KLAVUU Real Vegan Collagen Ampoule",
        "KLAVUU Real Vegan Collagen Cream",
        # ... (기존 DB 항목들)
    ],
    "TIRTIR": [
        "TIRTIR MASK FIT RED CUSHION 21N IVORY",
        # ...
    ],
    "K-SECRET" :[
"K-SECRET SEOUL 1988 SERUM  RETINAL LIPOSOME 2% + BLACK GINSENG",
        # ...
    ],
    "UNPA" :[

        "unpa Bubi Bubi Bubble Lip Scrub",
        # ...
    ],

    
    "BRAYE" :[

        
    ],

}


def load_db():
    """저장된 JSON 파일이 있으면 불러오고, 없으면 기본 DB 사용"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_DB


def save_db(db_data):
    """DB 변경사항을 JSON 파일로 저장"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db_data, f, ensure_ascii=False, indent=4)


# 세션 상태에 DB 저장
if "OFFICIAL_DB" not in st.session_state:
    st.session_state["OFFICIAL_DB"] = load_db()

# ---------------------------------------------------------
# ➕ [사이드바] 신규 제품명/브랜드 DB 추가 기능
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("➕ 공표확인서 정식 DB 추가")

db_dict = st.session_state["OFFICIAL_DB"]

# 1. 브랜드 선택 또는 직접 입력
brand_option = st.sidebar.radio(
    "브랜드 선택 방식", ["기존 브랜드 선택", "새 브랜드 직접 입력"]
)

if brand_option == "기존 브랜드 선택":
    selected_brand = st.sidebar.selectbox("브랜드 선택", list(db_dict.keys()))
else:
    selected_brand = st.sidebar.text_input("새 브랜드명 입력 (예: BRAYE)")

# 2. 정식 제품명 입력
new_product_name = st.sidebar.text_input(
    "추가할 정식 제품명 입력",
    placeholder="예: KLAVUU GREEN PEARLSATION TEATREE SPOT",
)


if st.sidebar.button("💾 DB에 제품명 추가하기"):
    if not selected_brand or not new_product_name:
        st.sidebar.warning("⚠️ 브랜드명과 제품명을 모두 입력해 주세요.")
    else:
        brand_key = selected_brand.strip().upper()
        prod_name = new_product_name.strip()

        # 전체 DB 내 중복 여부 확인 (대소문자/공백 무시 정확 검사)
        all_products_lower = {
            item.strip().lower(): b_name
            for b_name, items in db_dict.items()
            for item in items
        }

        # ❌ 1) 이미 등록되어 있는 경우 -> ERROR 팝업 출력
        if prod_name.lower() in all_products_lower:
            existing_brand = all_products_lower[prod_name.lower()]
            st.sidebar.error(
                f"🚨 등록 불가: 이미 [{existing_brand}] 브랜드에 등록되어 있는 제품명입니다!"
            )

        # ✅ 2) 중복이 없는 경우 -> 정상 등록 진행
        else:
            if brand_key not in db_dict:
                db_dict[brand_key] = []

            db_dict[brand_key].append(prod_name)
            save_db(db_dict)  # 파일 저장
            st.session_state["OFFICIAL_DB"] = db_dict

            st.sidebar.success(
                f"✅ [{brand_key}] {prod_name}\n\n등록이 완료되었습니다!"
            )
            st.rerun()

st.sidebar.header("📚 등록된 브랜드 DB 현황")
st.sidebar.caption("브랜드별 버튼을 누르면 정식 제품명 목록(.txt)을 다운로드합니다.")

db_dict = st.session_state["OFFICIAL_DB"]

for brand, items in db_dict.items():
    col_text, col_btn = st.sidebar.columns([3, 2])
    
    # 1. 브랜드명 및 SKU 수 표시
    col_text.markdown(f"**{brand}** (`{len(items)}개`) ")
    
    # 2. TXT 파일 내용 생성 (줄바꿈 구분)
    txt_content = "\n".join(items)
    
    # 3. 브랜드별 TXT 다운로드 버튼
    col_btn.download_button(
        label="📄 TXT",
        data=txt_content,
        file_name=f"{brand}_공표확인서_정식제품명 목록.txt",
        mime="text/plain",
        key=f"download_{brand}"  # 고유 키 지정
    )

st.sidebar.markdown("---")
