import streamlit as st

# غيّري كلمة المرور هنا
ADMIN_PASSWORD = "admin123"


def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)


def login_form():
    st.subheader("🔐 تسجيل الدخول")

    password = st.text_input("كلمة المرور", type="password")

    if st.button("تسجيل الدخول"):
        if password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("تم تسجيل الدخول بنجاح ✅")
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة")


def logout_button():
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()


def require_login():
    """
    تستخدم فقط في الصفحات المحمية (رفع البيانات)
    """
    if not is_logged_in():
        st.warning("⚠️ هذه الصفحة مخصصة للمسؤول فقط. الرجاء تسجيل الدخول.")
        login_form()
        st.stop()
