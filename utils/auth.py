import streamlit as st

def require_admin() -> bool:
    """
    Admin gate using Streamlit secrets:
    In Streamlit Cloud -> App settings -> Secrets:
    ADMIN_PASSWORD="ضع_كلمة_مرور"
    """
    admin_password = st.secrets.get("ADMIN_PASSWORD", None)
    if not admin_password:
        st.error("ADMIN_PASSWORD غير موجود في Secrets. أضيفيه في إعدادات Streamlit Cloud.")
        st.stop()

    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    if st.session_state.is_admin:
        return True

    with st.sidebar.expander("🔐 دخول الأدمن", expanded=True):
        pw = st.text_input("كلمة مرور الأدمن", type="password")
        if st.button("دخول"):
            if pw == admin_password:
                st.session_state.is_admin = True
                st.success("تم الدخول كأدمن ✅")
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة")

    st.warning("هذه الصفحة للأدمن فقط.")
    st.stop()
