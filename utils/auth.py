import streamlit as st

def _get_admin_password() -> str:
    # إذا عندك Streamlit Secrets حطي: ADMIN_PASSWORD هناك
    if "ADMIN_PASSWORD" in st.secrets:
        return str(st.secrets["ADMIN_PASSWORD"])
    return "admin123"  # مؤقتًا غيّريها


def is_logged_in() -> bool:
    return bool(st.session_state.get("logged_in", False))


def login_form():
    st.subheader("🔐 تسجيل الدخول للمسؤول")

    password = st.text_input("كلمة المرور", type="password")

    if st.button("تسجيل الدخول", use_container_width=True):
        if password == _get_admin_password():
            st.session_state["logged_in"] = True
            st.success("✅ تم تسجيل الدخول بنجاح")
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")


def logout_button():
    if st.button("تسجيل الخروج", use_container_width=True):
        st.session_state["logged_in"] = False
        st.rerun()


def require_login():
    """
    استخدميها في الصفحات المحمية (رفع البيانات).
    إذا المستخدم غير مسجل دخول، تظهر فورًا شاشة الدخول داخل نفس الصفحة وتوقف التنفيذ.
    """
    if not is_logged_in():
        st.warning("هذه الصفحة للمسؤول فقط. الرجاء تسجيل الدخول للمتابعة.")
        login_form()
        st.stop()
