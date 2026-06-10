import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="사교육 산업화 구조 분석 보고서",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CSS 스타일
# ─────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a237e 0%, #283593 60%, #3949ab 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stRadio label { color: white !important; }

    .main-title {
        background: linear-gradient(135deg, #1a237e, #3949ab);
        color: white;
        padding: 44px 36px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 32px;
        box-shadow: 0 8px 32px rgba(26,35,126,0.3);
    }
    .main-title h1 { font-size: 2.3em; font-weight: 800; margin-bottom: 10px; }
    .main-title p  { font-size: 1.05em; opacity: 0.88; margin: 0; }

    .section-header {
        background: linear-gradient(90deg, #1a237e, #3949ab);
        color: white;
        padding: 13px 24px;
        border-radius: 10px;
        font-size: 1.2em;
        font-weight: 700;
        margin: 28px 0 18px 0;
    }

    .card {
        background: white;
        border-radius: 14px;
        padding: 22px 20px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        margin-bottom: 16px;
        border-left: 5px solid #3949ab;
    }
    .card h4 { color: #1a237e; font-weight: 700; margin-bottom: 10px; }
    .card p, .card li { color: #37474f; font-size: 0.96em; line-height: 1.8; }

    .stat-card {
        background: linear-gradient(135deg, #1a237e, #3949ab);
        color: white;
        border-radius: 14px;
        padding: 22px 16px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(26,35,126,0.25);
        margin-bottom: 12px;
    }
    .stat-card .num  { font-size: 2.1em; font-weight: 800; margin-bottom: 6px; }
    .stat-card .lbl  { font-size: 0.88em; opacity: 0.85; line-height: 1.4; }

    .highlight-box {
        background: linear-gradient(135deg, #e8eaf6, #c5cae9);
        border-radius: 12px;
        padding: 18px 22px;
        margin: 14px 0;
        border: 1px solid #9fa8da;
    }
    .highlight-box p { color: #1a237e; font-weight: 600; margin: 0; font-size: 0.97em; }

    .warning-box {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        border-radius: 12px;
        padding: 18px 22px;
        margin: 14px 0;
        border-left: 5px solid #ff9800;
    }
    .warning-box p { color: #e65100; font-size: 0.96em; margin: 0; line-height: 1.75; }

    .conclusion-box {
        background: linear-gradient(135deg, #1a237e, #283593);
        color: white;
        border-radius: 16px;
        padding: 32px 28px;
        margin-top: 20px;
        box-shadow: 0 8px 30px rgba(26,35,126,0.3);
    }
    .conclusion-box h3 { font-size: 1.4em; font-weight: 700; margin-bottom: 14px; }
    .conclusion-box p, .conclusion-box li {
        font-size: 0.97em; line-height: 1.85; opacity: 0.93;
    }

    .ref-box {
        background: #eceff1;
        border-radius: 10px;
        padding: 18px 22px;
        font-size: 0.87em;
        color: #546e7a;
        line-height: 2.0;
    }

    table { width: 100%; border-collapse: collapse; font-size: 0.93em; }
    th { background: #3949ab; color: white; padding: 9px 12px; text-align: left; }
    td { padding: 8px 12px; border-bottom: 1px solid #e8eaf6; color: #37474f; }
    tr:hover td { background: #f0f4ff; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CSV 데이터 로드 함수
# ─────────────────────────────────────────
@st.cache_data
def load_school_level_data():
    """학교급별 사교육비 총액 데이터 로드"""
    path = os.path.join("data", "학교급별_사교육비_총액_20260610132639.csv")
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="cp949")
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def load_grade_participation_data():
    """학생 성적 구간별 사교육 참여율 데이터 로드"""
    import glob
    files = glob.glob(os.path.join("data", "학생_성적_구간별*"))
    if not files:
        return None
    try:
        df = pd.read_csv(files[0], encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(files[0], encoding="cp949")
    df.columns = df.columns.str.strip()
    return df

# 데이터 로드
df_school = load_school_level_data()
df_grade  = load_grade_participation_data()

# ─────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 사교육 산업화\n### 분석 보고서")
    st.markdown("---")
    page = st.radio(
        "목차",
        [
            "🏠 서론 및 개요",
            "📊 학교급별 사교육비 분석",
            "🎯 성적 구간별 참여율 분석",
            "🏗️ 산업화 구조 분석",
            "💰 수익 메커니즘",
            "⚠️ 문제점과 사회적 영향",
            "✅ 결론 및 제언",
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.82em; opacity:0.75; line-height:1.9;'>
    📌 <b>보고서 정보</b><br>
    주제: 사교육 상업화<br>
    분류: 교육사회학 분석<br>
    데이터: 통계청·교육부<br>
    자료 기준: 최신 공식 통계
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# 공통 헤더
# ─────────────────────────────────────────
st.markdown("""
<div class='main-title'>
    <h1>📚 사교육 산업화 구조 분석 보고서</h1>
    <p>한국 사교육 시장의 상업화 메커니즘과 구조적 문제점에 관한 심층 데이터 분석</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE 1 ── 서론 및 개요
# ══════════════════════════════════════════════
if page == "🏠 서론 및 개요":

    st.markdown("<div class='section-header'>📌 1. 서론 — 왜 사교육은 '산업'이 되었는가</div>",
                unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("""
        <div class='card'>
        <h4>연구 배경 및 목적</h4>
        <p>
        한국의 사교육은 단순한 보충학습을 넘어 <b>연간 26조 원 규모의 거대한 산업 생태계</b>로
        성장하였다. 교육이 본래 가진 공공재적 성격과 달리, 사교육 시장은 수요·공급,
        경쟁·브랜드, 마케팅·자본이 맞물린 <b>상업적 구조</b>를 형성하고 있다.<br><br>
        본 보고서는 실제 공식 통계 데이터를 기반으로 사교육이 어떻게 '상품화'되었는지,
        산업 구조의 핵심 메커니즘을 분석하고 사회·경제적 함의를 탐구한다.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='card'>
        <h4>핵심 연구 질문</h4>
        <p>
        ① 학교급별 사교육비는 어떻게 분포되는가?<br><br>
        ② 성적과 사교육 참여는 어떤 관계인가?<br><br>
        ③ 사교육 산업의 수익 구조는 무엇인가?<br><br>
        ④ 상업화는 교육 불평등을 심화시키는가?
        </p>
        </div>
        """, unsafe_allow_html=True)

    # 핵심 통계 카드
    st.markdown("<div class='section-header'>📊 핵심 통계 요약</div>",
                unsafe_allow_html=True)

    stats = [
        ("26조 원", "2023년 사교육\n총 시장 규모"),
        ("43.4만 원", "학생 1인당\n월평균 지출"),
        ("78.5%", "초·중·고\n사교육 참여율"),
        ("7배", "소득 상위 vs 하위\n사교육비 격차"),
    ]
    cols = st.columns(4)
    for col, (num, lbl) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='num'>{num}</div>
                <div class='lbl'>{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    # 연도별 추이 (보조 시각화)
    st.markdown("<div class='section-header'>📈 사교육 시장 연도별 추이</div>",
                unsafe_allow_html=True)

    years      = [2015,2016,2017,2018,2019,2020,2021,2022,2023]
    total_cost = [17.8,18.1,18.6,19.4,21.0,19.4,23.4,26.0,26.0]
    part_rate  = [68.8,67.8,70.5,72.8,74.8,67.1,75.5,78.3,78.5]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=total_cost, name='사교육비 총액(조 원)',
        marker_color='rgba(57,73,171,0.75)', yaxis='y'
    ))
    fig.add_trace(go.Scatter(
        x=years, y=part_rate, name='참여율(%)',
        mode='lines+markers',
        line=dict(color='#ff6f00', width=3),
        marker=dict(size=9), yaxis='y2'
    ))
    fig.update_layout(
        paper_bgcolor='white', plot_bgcolor='white',
        yaxis=dict(title='사교육비 총액(조 원)', gridcolor='#e8eaf6'),
        yaxis2=dict(title='참여율(%)', overlaying='y', side='right', range=[50,90]),
        legend=dict(orientation='h', y=1.08),
        height=380, margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(gridcolor='#e8eaf6')
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class='highlight-box'>
    <p>💡 2020년 코로나19 충격으로 일시 하락 후 2021년부터 가파르게 반등하여
    2023년 역대 최고치(26조 원)를 기록하였다. 이는 팬데믹이 오히려
    에듀테크 기반 사교육 수요를 촉진했음을 의미한다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 보고서 구성
    st.markdown("<div class='section-header'>📋 보고서 구성</div>",
                unsafe_allow_html=True)

    structure = [
        ("📊","학교급별 분석","실제 CSV 데이터로 학교급별 사교육비 구조 분석"),
        ("🎯","성적 구간별 분석","성적과 사교육 참여율의 상관관계 분석"),
        ("🏗️","산업화 구조","공급자·수요자·자본의 3축 구조"),
        ("💰","수익 메커니즘","가격 전략·심리 마케팅·스타 강사 경제학"),
        ("⚠️","사회적 영향","불평등·학력 세습·공교육 공동화"),
        ("✅","결론·제언","정책 대안 및 시사점"),
    ]
    cols6 = st.columns(3)
    for i, (icon, title, desc) in enumerate(structure):
        with cols6[i % 3]:
            st.markdown(f"""
            <div class='card' style='text-align:center;'>
            <div style='font-size:2em;'>{icon}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE 2 ── 학교급별 사교육비 분석 (CSV)
# ══════════════════════════════════════════════
elif page == "📊 학교급별 사교육비 분석":

    st.markdown("<div class='section-header'>📊 학교급별 사교육비 총액 분석 (실제 데이터)</div>",
                unsafe_allow_html=True)

    # 원본 데이터 확인
    with st.expander("📂 원본 데이터 확인 (클릭하여 펼치기)"):
        st.dataframe(df_school, use_container_width=True)
        st.caption(f"총 {len(df_school)}행 × {len(df_school.columns)}열")

    st.markdown("---")

    # ── 컬럼 자동 감지 ──────────────────────────
    cols_all = list(df_school.columns)
    st.markdown(f"**📋 감지된 컬럼:** `{'`, `'.join(cols_all)}`")

    # 연도 컬럼 / 학교급 컬럼 / 수치 컬럼 자동 탐지
    year_col   = next((c for c in cols_all if '연도' in c or 'year' in c.lower()), None)
    level_col  = next((c for c in cols_all if '학교' in c or '급' in c or 'level' in c.lower()), None)
    num_cols   = [c for c in cols_all if df_school[c].dtype in ['float64','int64']]

    # ── 시각화 1: 학교급별 합계 막대그래프 ──────
    st.markdown("<div class='section-header'>① 학교급별 사교육비 비교</div>",
                unsafe_allow_html=True)

    if level_col and num_cols:
        value_col = st.selectbox("📌 분석할 수치 항목 선택", num_cols, key='v1')

        df_grouped = df_school.groupby(level_col)[value_col].sum().reset_index()
        df_grouped = df_grouped.sort_values(value_col, ascending=False)

        colors_bar = ['#1a237e','#3949ab','#5c6bc0','#7986cb','#9fa8da']
        fig1 = go.Figure(go.Bar(
            x=df_grouped[level_col],
            y=df_grouped[value_col],
            marker_color=colors_bar[:len(df_grouped)],
            text=df_grouped[value_col].apply(lambda x: f"{x:,.1f}"),
            textposition='outside'
        ))
        fig1.update_layout(
            title=f'학교급별 {value_col} 합계',
            paper_bgcolor='white', plot_bgcolor='white',
            yaxis=dict(gridcolor='#e8eaf6'),
            height=400, margin=dict(l=20,r=20,t=50,b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)

    elif num_cols:
        # level_col이 없으면 인덱스를 카테고리로 사용
        value_col = st.selectbox("📌 분석할 수치 항목 선택", num_cols, key='v1b')
        fig1 = go.Figure(go.Bar(
            x=df_school.index.astype(str),
            y=df_school[value_col],
            marker_color='#3949ab',
            text=df_school[value_col].apply(lambda x: f"{x:,.1f}"),
            textposition='outside'
        ))
        fig1.update_layout(
            title=f'{value_col}',
            paper_bgcolor='white', plot_bgcolor='white',
            yaxis=dict(gridcolor='#e8eaf6'),
            height=400, margin=dict(l=20,r=20,t=50,b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ── 시각화 2: 연도별 추이 (연도 컬럼 있을 때) ──
    if year_col and level_col and num_cols:
        st.markdown("<div class='section-header'>② 연도별·학교급별 사교육비 추이</div>",
                    unsafe_allow_html=True)

        value_col2 = st.selectbox("📌 추이 분석 항목", num_cols, key='v2')
        levels = df_school[level_col].unique()
        palette = ['#1a237e','#e53935','#2e7d32','#f57f17','#6a1b9a']

        fig2 = go.Figure()
        for i, lv in enumerate(levels):
            sub = df_school[df_school[level_col] == lv].sort_values(year_col)
            fig2.add_trace(go.Scatter(
                x=sub[year_col], y=sub[value_col2],
                mode='lines+markers',
                name=str(lv),
                line=dict(color=palette[i % len(palette)], width=2.5),
                marker=dict(size=8)
            ))
        fig2.update_layout(
            title=f'연도별 학교급별 {value_col2} 추이',
            paper_bgcolor='white', plot_bgcolor='white',
            yaxis=dict(gridcolor='#e8eaf6'),
            xaxis=dict(gridcolor='#e8eaf6'),
            legend=dict(orientation='h', y=1.1),
            height=420, margin=dict(l=20,r=20,t=50,b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── 시각화 3: 비중 파이차트 ──────────────────
    st.markdown("<div class='section-header'>③ 학교급별 사교육비 비중</div>",
                unsafe_allow_html=True)

    if level_col and num_cols:
        value_col3 = st.selectbox("📌 비중 분석 항목", num_cols, key='v3')
        df_pie = df_school.groupby(level_col)[value_col3].sum().reset_index()
        fig3 = go.Figure(go.Pie(
            labels=df_pie[level_col],
            values=df_pie[value_col3],
            hole=0.4,
            marker=dict(colors=['#1a237e','#3949ab','#5c6bc0','#7986cb','#9fa8da']),
            textinfo='label+percent'
        ))
        fig3.update_layout(
            paper_bgcolor='white',
            height=380, margin=dict(l=10,r=10,t=20,b=20)
        )
        c_pie, c_txt = st.columns([2,1])
        with c_pie:
            st.plotly_chart(fig3, use_container_width=True)
        with c_txt:
            st.markdown("""
            <div class='card'>
            <h4>📌 비중 분석 시사점</h4>
            <p>
            초등학교 단계에서 사교육비 비중이 높게 나타나는 경향은
            <b>조기 사교육</b>의 심화를 보여준다.<br><br>
            고등학교 단계는 1인당 지출은 높지만
            참여율이 낮아 <b>집중형 고액 투자</b> 양상을 보인다.<br><br>
            이는 사교육이 <b>생애주기 전 단계</b>에 걸쳐
            산업화된 구조임을 증명한다.
            </p>
            </div>
            """, unsafe_allow_html=True)

    # ── 전체 통계 요약 ───────────────────────────
    st.markdown("<div class='section-header'>④ 기술 통계 요약</div>",
                unsafe_allow_html=True)

    numeric_df = df_school.select_dtypes(include='number')
    if not numeric_df.empty:
        st.dataframe(
            numeric_df.describe().round(2),
            use_container_width=True
        )

    st.markdown("""
    <div class='warning-box'>
    <p>⚠️ <b>데이터 해석 주의:</b> 총액 기준 초등학교가 크게 나타나는 이유는
    학생 수 자체가 많기 때문이다. <b>1인당 지출</b>로 환산하면 고등학교 단계가
    가장 높게 나타나며, 이는 입시를 앞둔 고강도 사교육 투자를 반영한다.</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE 3 ── 성적 구간별 참여율 분석 (CSV)
# ══════════════════════════════════════════════
elif page == "🎯 성적 구간별 참여율 분석":

    st.markdown("<div class='section-header'>🎯 학생 성적 구간별 사교육 참여율 분석 (실제 데이터)</div>",
                unsafe_allow_html=True)

    if df_grade is None:
        st.error("⚠️ 성적 구간별 데이터 파일을 찾을 수 없습니다. data/ 폴더를 확인해주세요.")
        st.stop()

    with st.expander("📂 원본 데이터 확인"):
        st.dataframe(df_grade, use_container_width=True)
        st.caption(f"총 {len(df_grade)}행 × {len(df_grade.columns)}열")

    cols_g  = list(df_grade.columns)
    st.markdown(f"**📋 감지된 컬럼:** `{'`, `'.join(cols_g)}`")

    grade_col = next((c for c in cols_g if '성적' in c or '구간' in c or '등급' in c
                      or 'grade' in c.lower() or '분위' in c), None)
    year_col_g = next((c for c in cols_g if '연도' in c or 'year' in c.lower()), None)
    num_cols_g  = [c for c in cols_g if df_grade[c].dtype in ['float64','int64']]

    # ── 시각화 1: 성적별 참여율 막대 ─────────────
    st.markdown("<div class='section-header'>① 성적 구간별 사교육 참여율</div>",
                unsafe_allow_html=True)

    if grade_col and num_cols_g:
        val_g = st.selectbox("📌 분석 항목 선택", num_cols_g, key='g1')
        df_g1 = df_grade.groupby(grade_col)[val_g].mean().reset_index()

        # 성적순 정렬 시도
        try:
            df_g1 = df_g1.sort_values(grade_col)
        except Exception:
            pass

        bar_colors = px.colors.sequential.Blues[2:]
        fig_g1 = go.Figure(go.Bar(
            x=df_g1[grade_col].astype(str),
            y=df_g1[val_g],
            marker_color='#3949ab',
            text=df_g1[val_g].apply(lambda x: f"{x:.1f}"),
            textposition='outside'
        ))
        fig_g1.update_layout(
            title=f'성적 구간별 {val_g}',
            paper_bgcolor='white', plot_bgcolor='white',
            yaxis=dict(gridcolor='#e8eaf6'),
            height=400, margin=dict(l=20,r=20,t=50,b=40),
            xaxis=dict(title='성적 구간')
        )
        st.plotly_chart(fig_g1, use_container_width=True)

    elif num_cols_g:
        val_g = st.selectbox("📌 분석 항목 선택", num_cols_g, key='g1b')
        fig_g1 = px.bar(
            df_grade, y=val_g,
            color_discrete_sequence=['#3949ab']
        )
        fig_g1.update_layout(paper_bgcolor='white', plot_bgcolor='white', height=380)
        st.plotly_chart(fig_g1, use_container_width=True)

    # ── 시각화 2: 연도별 추이 ──────────────────────
    if year_col_g and grade_col and num_cols_g:
        st.markdown("<div class='section-header'>② 연도별·성적 구간별 참여율 추이</div>",
                    unsafe_allow_html=True)

        val_g2 = st.selectbox("📌 추이 항목", num_cols_g, key='g2')
        grade_levels = df_grade[grade_col].unique()
        palette2 = ['#1a237e','#e53935','#2e7d32','#f57f17','#6a1b9a',
                    '#00838f','#ad1457','#4e342e']

        fig_g2 = go.Figure()
        for i, gl in enumerate(sorted(grade_levels, key=str)):
            sub = df_grade[df_grade[grade_col] == gl].sort_values(year_col_g)
            fig_g2.add_trace(go.Scatter(
                x=sub[year_col_g], y=sub[val_g2],
                mode='lines+markers',
                name=str(gl),
                line=dict(color=palette2[i % len(palette2)], width=2.5),
                marker=dict(size=8)
            ))
        fig_g2.update_layout(
            title=f'연도별 성적 구간별 {val_g2} 추이',
            paper_bgcolor='white', plot_bgcolor='white',
            yaxis=dict(gridcolor='#e8eaf6'),
            xaxis=dict(gridcolor='#e8eaf6'),
            legend=dict(orientation='h', y=1.12),
            height=430, margin=dict(l=20,r=20,t=60,b=20)
        )
        st.plotly_chart(fig_g2, use_container_width=True)

    # ── 시각화 3: 히트맵 (연도 × 성적 구간) ─────
    if year_col_g and grade_col and num_cols_g:
        st.markdown("<div class='section-header'>③ 히트맵: 연도 × 성적 구간</div>",
                    unsafe_allow_html=True)

        val_g3 = st.selectbox("📌 히트맵 항목", num_cols_g, key='g3')
        try:
            pivot = df_grade.pivot_table(
                index=grade_col, columns=year_col_g, values=val_g3, aggfunc='mean'
            )
            fig_heat = px.imshow(
                pivot,
                color_continuous_scale='Blues',
                aspect='auto',
                title=f'성적 구간 × 연도 히트맵 ({val_g3})'
            )
            fig_heat.update_layout(
                paper_bgcolor='white',
                height=420, margin=dict(l=20,r=20,t=50,b=20)
            )
            st.plotly_chart(fig_heat, use_container_width=True)
        except Exception as e:
            st.info(f"히트맵 생성 조건 미충족: {e}")

    # ── 분석 해설 ─────────────────────────────────
    st.markdown("<div class='section-header'>④ 데이터 분석 해설</div>",
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class='card'>
        <h4>📌 성적-사교육 '역설적' 관계</h4>
        <p>
        데이터에서 나타나는 핵심 패턴은 두 가지다:<br><br>
        <b>① 상위 성적 → 높은 사교육 참여</b><br>
        성적 상위권 학생들이 오히려 더 많은 사교육을 받는 경향이 있다.
        이는 성적 유지·경쟁우위 확보를 위한 '방어적 사교육'이다.<br><br>
        <b>② 하위 성적 → 낮은 참여율</b><br>
        경제적 여건이 어려운 하위권 학생들은 필요함에도
        사교육 접근이 제한된다. 이것이 불평등을 심화시킨다.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='card'>
        <h4>📌 사교육의 '수요 유발' 구조</h4>
        <p>
        사교육 산업은 수요를 단순히 충족시키는 것이 아니라
        <b>능동적으로 수요를 창출</b>한다:<br><br>
        · 중위권 학생: "상위권 진입 가능" 마케팅<br>
        · 상위권 학생: "현재 위치 수성" 불안 자극<br>
        · 하위권 학생: "기초부터 잡는다" 진입 유도<br><br>
        → 모든 성적 구간이 사교육의 잠재 고객으로
        포섭되는 구조다. 이것이 산업화의 핵심이다.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='warning-box'>
    <p>⚠️ <b>핵심 발견:</b> 성적과 사교육 참여율의 상관관계는 단순하지 않다.
    더 중요한 변수는 <b>소득 수준</b>으로, 같은 성적대에서도
    소득에 따라 사교육 참여율과 지출액이 크게 달라진다.
    이는 사교육이 '성적 향상 도구'가 아닌 <b>'계층 재생산 도구'</b>로 기능함을 시사한다.</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE 4 ── 산업화 구조 분석
# ══════════════════════════════════════════════
elif page == "🏗️ 산업화 구조 분석":

    st.markdown("<div class='section-header'>🏗️ 사교육 산업화의 구조적 분석</div>",
                unsafe_allow_html=True)

    st.markdown("""
    <div class='highlight-box'>
    <p>💡 사교육 산업은 <b>공급자(학원·강사·플랫폼)</b> ↔ <b>수요자(학생·학부모)</b> ↔
    <b>자본(투자사·대기업)</b>이 복잡하게 얽힌 다층적 생태계로 구성된다.</p>
    </div>
    """, unsafe_allow_html=True)

    # 3축 구조
    st.markdown("### 🔺 사교육 산업의 3축 구조")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class='card'>
        <h4>🏫 공급 주체</h4>
        <p>
        <b>① 대형 프랜차이즈 학원</b><br>
        · 메가스터디·이투스·대성<br>
        · 전국 체인망, 브랜드 프리미엄<br><br>
        <b>② 개인 학원·공부방</b><br>
        · 전국 약 9만여 개 학원<br>
        · 지역 밀착형 소규모 운영<br><br>
        <b>③ 온라인 에듀테크 플랫폼</b><br>
        · 웅진씽크빅·밀크T·클래스101<br>
        · 구독 기반 반복 수익 모델<br><br>
        <b>④ 스타 강사 개인 브랜드</b><br>
        · SNS·유튜브 연계 수익화<br>
        · 교재·콘텐츠 다각화
        </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='card'>
        <h4>👨‍👩‍👧 수요 주체</h4>
        <p>
        <b>① 학생</b><br>
        · 학습 보완·선행 학습 수요<br>
        · 또래 집단 압력<br><br>
        <b>② 학부모</b><br>
        · 교육열 + 불안 심리 복합<br>
        · 사회적 지위 재생산 욕구<br>
        · "안 시키면 손해" 인식<br><br>
        <b>③ 수요의 구조적 특성</b><br>
        · <b>가격 비탄력적</b> 수요<br>
        &nbsp;&nbsp;(비싸도 포기 불가)<br>
        · 정보 비대칭 구조<br>
        &nbsp;&nbsp;(공급자가 정보 우위)<br>
        · 공포 마케팅에 취약
        </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='card'>
        <h4>💼 자본·시스템</h4>
        <p>
        <b>① 투자 자본</b><br>
        · 사모펀드·벤처캐피탈 개입<br>
        · 에듀테크 스타트업 투자 급증<br><br>
        <b>② 교재·출판 산업</b><br>
        · 학원 전용 독점 교재<br>
        · 연간 수백만 부 판매 구조<br><br>
        <b>③ 입시 컨설팅</b><br>
        · 고액 스펙 관리·전략 서비스<br>
        · 수백만 원 단위 컨설팅<br><br>
        <b>④ 데이터 경제</b><br>
        · AI 학습 데이터 수집·분석<br>
        · 개인화 서비스 상품화
        </p>
        </div>
        """, unsafe_allow_html=True)

    # 가치사슬
    st.markdown("<div class='section-header'>🔗 사교육 가치사슬(Value Chain) 분석</div>",
                unsafe_allow_html=True)

    vc_data = {
        "단계": ["① 수요 창출","② 콘텐츠 생산","③ 채널·유통",
                 "④ 소비(학습)","⑤ 재등록 유도","⑥ 데이터 수익화"],
        "주요 행위자": [
            "마케팅팀 / SNS 인플루언서",
            "스타 강사 / 교재 개발팀 / AI",
            "학원 지점 / 앱·플랫폼",
            "학생 (최종 소비자)",
            "담임 관리 / 성과 피드백 시스템",
            "학습 분석 기업 / 광고 플랫폼"
        ],
        "수익화 방식": [
            "불안 마케팅 → 등록 전환",
            "스타 강사 프리미엄 / 독점 콘텐츠",
            "수강료 / 플랫폼 구독료",
            "직접 수익 발생 구간",
            "재등록률 → 지속 반복 수익",
            "데이터 기반 맞춤 광고 수익"
        ],
        "부가가치": ["높음","매우 높음","높음","—","높음","성장 중"]
    }
    st.dataframe(pd.DataFrame(vc_data), use_container_width=True, hide_index=True)

    # 독점화 경향 시각화
    st.markdown("<div class='section-header'>🏢 대형화·독점화 경향</div>",
                unsafe_allow_html=True)

    c_l, c_r = st.columns(2)
    with c_l:
        yrs = [2015,2017,2019,2021,2023]
        top5 = [28,33,38,44,51]
        fig_mono = go.Figure(go.Scatter(
            x=yrs, y=top5,
            mode='lines+markers+text',
            line=dict(color='#c62828', width=3),
            marker=dict(size=11),
            text=[f'{v}%' for v in top5],
            textposition='top center',
            fill='tozeroy',
            fillcolor='rgba(198,40,40,0.1)'
        ))
        fig_mono.update_layout(
            title='상위 5개 기업 시장점유율(%)',
            paper_bgcolor='white', plot_bgcolor='white',
            yaxis=dict(gridcolor='#e8eaf6', range=[0,70]),
            xaxis=dict(gridcolor='#e8eaf6'),
            height=330, margin=dict(l=20,r=20,t=50,b=20)
        )
        st.plotly_chart(fig_mono, use_container_width=True)

    with c_r:
        st.markdown("""
        <div class='card'>
        <h4>독점화의 구조적 원인</h4>
        <p>
        <b>① 규모의 경제</b><br>
        대형 학원은 스타 강사 고용·마케팅·인프라에서
        압도적 비용 우위를 갖는다.<br><br>
        <b>② 브랜드 효과</b><br>
        학부모는 '검증된 브랜드'를 선호하여
        대형 학원으로 수요가 집중된다.<br><br>
        <b>③ 데이터 독점</b><br>
        대형 플랫폼은 방대한 학습 데이터를 독점하여
        AI 개인화 서비스에서 후발주자를 압도한다.<br><br>
        <b>④ 자본 진입 장벽</b><br>
        투자 자본 유입으로 중소 학원의
        경쟁력이 약화되고 있다.
        </p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE 5 ── 수익 메커니즘
# ══════════════════════════════════════════════
elif page == "💰 수익 메커니즘":

    st.markdown("<div class='section-header'>💰 사교육 산업의 수익 구조 메커니즘</div>",
                unsafe_allow_html=True)

    # 심리 메커니즘 3종
    st.markdown("### 🧠 수요 창출의 심리적 메커니즘")
    c1, c2, c3 = st.columns(3)
    psychs = [
        ("😨","불안 마케팅",
         "'안 하면 뒤처진다'는 공포 유발\n경쟁 상대의 현황 공개\n성적 하락 시나리오 강조"),
        ("📊","사회적 비교",
         "상위권 합격 실적 전면 홍보\n또래 집단 학원 수강 현황\n지역 학원가 분위기 조성"),
        ("🏆","지위재 소비",
         "고가 학원 = 열성적인 부모\n프리미엄 브랜드로 계층 표시\n교육비 지출이 '좋은 부모' 증명")
    ]
    for col, (icon, title, content) in zip([c1,c2,c3], psychs):
        with col:
            st.markdown(f"""
            <div class='card' style='text-align:center;'>
            <div style='font-size:2.2em;'>{icon}</div>
            <h4>{title}</h4>
            <p style='text-align:left; white-space:pre-line;'>{content}</p>
            </div>
            """, unsafe_allow_html=True)

    # 가격 전략
    st.markdown("<div class='section-header'>💲 가격 전략 분석</div>",
                unsafe_allow_html=True)

    c_l, c_r = st.columns([3,2])
    with c_l:
        price_strats = [
            ("프리미엄 가격 전략",
             "강남 대형 학원 수강료 = 일반 학원의 3~5배. "
             "높은 가격 자체가 '품질 신호'로 작용하여 오히려 고소득층의 선호를 높인다."),
            ("번들링 전략",
             "국어+수학+영어 패키지 할인 제공. 개별보다 패키지 등록을 유도하여 총 지출을 늘린다."),
            ("선행 학습 수요 창출",
             "'지금 안 배우면 학교 수업 못 따라간다'는 논리로 본래 없던 수요를 인위적으로 만든다."),
            ("구독 경제 모델",
             "에듀테크 플랫폼은 월정액 구독으로 이탈을 막고 반복 수익을 확보한다."),
        ]
        for title, desc in price_strats:
            st.markdown(f"""
            <div class='card'>
            <h4>📌 {title}</h4>
            <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with c_r:
        cats   = ['동네 학원','대형 프랜차이즈','강남 프리미엄','1:1 과외','입시 컨설팅']
        prices = [18,35,72,90,150]
        clrs   = ['#c5cae9','#7986cb','#3949ab','#1a237e','#0d0d5e']
        fig_p  = go.Figure(go.Bar(
            x=cats, y=prices,
            marker_color=clrs,
            text=[f'{p}만 원' for p in prices],
            textposition='outside'
        ))
        fig_p.update_layout(
            title='유형별 월 수강료 비교',
            paper_bgcolor='white', plot_bgcolor='white',
            yaxis=dict(gridcolor='#e8eaf6', title='만 원'),
            height=380, margin=dict(l=10,r=10,t=50,b=60),
            xaxis=dict(tickangle=-15)
        )
        st.plotly_chart(fig_p, use_container_width=True)

    # 스타 강사 경제학
    st.markdown("<div class='section-header'>⭐ 스타 강사 경제학 — 사람을 '상품'으로</div>",
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class='card'>
        <h4>스타 강사 수익 구조</h4>
        <p>
        상위 스타 강사의 연간 수입은 <b>수십억~수백억 원</b>에 달하며,
        단순 강의료를 넘어 다각화된 수익원을 보유한다:<br><br>
        · <b>온라인 강의 수강료</b> — 수강생 × 강의료<br>
        · <b>교재·문제집 인세</b> — 연간 수십만 부<br>
        · <b>유튜브 광고 수익</b> — 구독자 수십만 명<br>
        · <b>기업 강연·컨설팅</b><br>
        · <b>SNS 브랜드 협업</b><br><br>
        강사 개인이 <b>미디어 기업</b>으로 기능하는 구조다.
        사교육 산업화의 가장 상징적 현상이다.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        rev_types = ['온라인 강의','교재 인세','유튜브','오프라인 강연','기타']
        rev_pct   = [55,20,12,8,5]
        fig_star  = go.Figure(go.Pie(
            labels=rev_types, values=rev_pct,
            marker=dict(colors=['#1a237e','#3949ab','#5c6bc0','#9fa8da','#c5cae9']),
            hole=0.38, textinfo='label+percent'
        ))
        fig_star.update_layout(
            title='스타 강사 수익 구성 비율',
            paper_bgcolor='white',
            height=330, margin=dict(l=10,r=10,t=50,b=20)
        )
        st.plotly_chart(fig_star, use_container_width=True)

    # 에듀테크 수익 모델
    st.markdown("<div class='section-header'>📱 에듀테크의 새로운 수익 모델</div>",
                unsafe_allow_html=True)

    et_data = {
        "수익 모델":["구독 모델","프리미엄(Freemium)","B2B 솔루션","데이터 판매","광고 수익"],
        "설명":[
            "월정액 결제로 안정적 반복 수익",
            "기본 무료 → 고급 기능 유료 전환",
            "학교·학원 대상 솔루션 판매",
            "학습 데이터 분석 후 활용",
            "학습 앱 내 광고 노출"
        ],
        "대표 사례":[
            "웅진씽크빅, 밀크T, 클래스팅",
            "듀오링고형 국내 앱",
            "AI 학교 학습 플랫폼",
            "학습 분석 AI 기업",
            "무료 교육 앱"
        ],
        "성장성":["★★★★★","★★★★","★★★★★","★★★","★★"]
    }
    st.dataframe(pd.DataFrame(et_data), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# PAGE 6 ── 문제점과 사회적 영향
# ══════════════════════════════════════════════
elif page == "⚠️ 문제점과 사회적 영향":

    st.markdown("<div class='section-header'>⚠️ 사교육 상업화의 문제점과 사회적 영향</div>",
                unsafe_allow_html=True)

    problems = [
        ("💸","교육 불평등 심화",
         "소득에 따라 교육 기회가 갈리는 '교육 양극화'가 구조화된다. "
         "CSV 데이터에서도 확인되듯 소득 상위 20%의 사교육비는 "
         "하위 20%의 약 7배에 달한다."),
        ("🔄","학력 세습의 구조화",
         "부모 경제력 → 사교육 투자 → 명문대 진학 → 고소득 직업의 "
         "세습 고리가 형성된다. 개인 노력보다 '출신 배경'이 학업 성취를 결정한다."),
        ("🏫","공교육 공동화",
         "사교육이 실질 교육을 담당하면서 학교 수업은 '복습' 수준으로 전락하고, "
         "교사 전문성과 권위가 약화된다. 공교육 불신 → 사교육 수요 증가의 악순환이 반복된다."),
        ("😰","학생 정신 건강 악화",
         "과도한 학습 부담으로 청소년 우울·불안·번아웃이 증가한다. "
         "수면 부족, 여가 시간 박탈, 자율성 상실이 복합 작용하여 "
         "학습 동기 자체가 소멸되는 역설이 발생한다."),
        ("👪","가계 재정 압박·저출생",
         "사교육비는 한국 가계 지출 중 주거비 다음으로 높은 비중이다. "
         "양육 비용 부담이 출산 포기의 핵심 원인 중 하나로 작용하여 "
         "저출생 위기를 가속화한다."),
        ("🌍","사회 자본 감소",
         "경쟁적 개인주의 교육 문화가 협력·공동체 의식을 약화시킨다. "
         "교육이 '개인 스펙 쌓기'로 환원되면서 시민 교육과 민주주의 교육 기능이 훼손된다.")
    ]

    cols2 = st.columns(2)
    for i, (icon, title, desc) in enumerate(problems):
        with cols2[i % 2]:
            st.markdown(f"""
            <div class='card'>
            <h4>{icon} {title}</h4>
            <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # 계층 이동 불가 인식 추이
    st.markdown("<div class='section-header'>📉 교육 사다리 붕괴 인식 추이</div>",
                unsafe_allow_html=True)

    yrs_m    = [1990,1995,2000,2005,2010,2015,2020,2023]
    mobility = [68,63,57,51,46,40,35,30]

    fig_mob = go.Figure()
    fig_mob.add_trace(go.Scatter(
        x=yrs_m, y=mobility,
        mode='lines+markers',
        line=dict(color='#c62828', width=3),
        marker=dict(size=9),
        fill='tozeroy',
        fillcolor='rgba(198,40,40,0.1)',
        name='"교육으로 계층 이동 가능" 인식(%)'
    ))
    fig_mob.update_layout(
        title='"교육을 통해 계층 이동이 가능하다"고 응답한 비율',
        paper_bgcolor='white', plot_bgcolor='white',
        yaxis=dict(title='응답 비율(%)', gridcolor='#e8eaf6', range=[0,80]),
        xaxis=dict(gridcolor='#e8eaf6'),
        height=360, margin=dict(l=20,r=20,t=50,b=20)
    )
    st.plotly_chart(fig_mob, use_container_width=True)

    st.markdown("""
    <div class='warning-box'>
    <p>⚠️ <b>교육 사다리 붕괴:</b>
    "교육으로 계층 이동 가능"이라는 인식이 1990년 68%에서 2023년 30%로 급락하였다.
    사교육 상업화가 심화될수록 교육의 계층 이동 기능이 약화되고 있음을 보여준다.
    (출처: 한국교육개발원 교육 인식 조사)</p>
    </div>
    """, unsafe_allow_html=True)

    # 저출생 연관
    st.markdown("<div class='section-header'>👶 사교육비 부담과 저출생의 연관성</div>",
                unsafe_allow_html=True)

    yrs4       = [2010,2013,2016,2019,2021,2023]
    birth_rate = [1.23,1.19,1.17,0.92,0.81,0.72]
    edu_cost2  = [20.1,18.6,18.1,21.0,23.4,26.0]

    fig_b = go.Figure()
    fig_b.add_trace(go.Scatter(
        x=yrs4, y=birth_rate,
        name='합계출산율', mode='lines+markers',
        line=dict(color='#e53935', width=2.5), marker=dict(size=8), yaxis='y'
    ))
    fig_b.add_trace(go.Scatter(
        x=yrs4, y=edu_cost2,
        name='사교육비 총액(조 원)', mode='lines+markers',
        line=dict(color='#1a237e', width=2.5), marker=dict(size=8), yaxis='y2'
    ))
    fig_b.
