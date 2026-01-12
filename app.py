from pathlib import Path

def render_logo():
    if not logo.get("enabled", True):
        return

    st.markdown("<div class='pmo-logo-wrap'>", unsafe_allow_html=True)

    # 1) لو فيه لوقو مرفوع مؤقت من السايدبار (اختياري)
    if uploaded_logo:
        st.image(uploaded_logo, width=int(logo.get("width", 160)))
    else:
        # 2) اقرأ اللوقو المحفوظ في data/
        saved_logo = Path(logo.get("file_path", "data/logo.png"))
        # 3) أو fallback لوقو ثابت داخل الريبو
        repo_logo = Path("assets") / "logo.png"

        if saved_logo.exists():
            st.image(str(saved_logo), width=int(logo.get("width", 160)))
        elif repo_logo.exists():
            st.image(str(repo_logo), width=int(logo.get("width", 160)))

    st.markdown("</div>", unsafe_allow_html=True)


# مكان اللوقو
if logo.get("location", "header") == "sidebar":
    with st.sidebar:
        render_logo()
else:
    render_logo()

st.markdown(
    """
    <h1 style="margin-bottom:0;">PMO Portal</h1>
    <p style="opacity:0.85;margin-top:6px;">تحديث أسبوعي عبر Excel + داشبورد تفاعلي + صلاحيات</p>
    """,
    unsafe_allow_html=True
)

st.info("من القائمة الجانبية: رفع البيانات → الداشبورد → الإعدادات (للأدمن فقط)")
