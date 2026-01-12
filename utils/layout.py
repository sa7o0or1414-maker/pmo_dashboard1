import streamlit as st

# ✅ غيّري كلمة المرور هنا (لاحقًا نخليها في Secrets)
ADMIN_PASSWORD = "admin123"


def is_logged_in() -> bool:
    return bool(st.session_state.get("logged_in", False))


def login_form():
    st.subheader("🔐 تسجيل الدخول للمسؤول")

    password = st.text_input("كلمة المرور", type="password")

    if st.button("تسجيل الدخول", use_container_width=True):
        if password == ADMIN_PASSWORD:
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
    استدعِ هذه الدالة داخل الصفحات المحمية (مثل رفع البيانات).
    إذا ما كان المستخدم مسجل دخول، تظهر له فورًا صفحة تسجيل الدخول داخل نفس الصفحة.
    """
    if not is_logged_in():
        st.warning("هذه الصفحة للمسؤول فقط. الرجاء تسجيل الدخول للمتابعة.")
        login_form()
        st.stop()
