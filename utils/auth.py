import hmac
import streamlit as st

def _get_secret(key: str, default=None):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default

def is_admin() -> bool:
    return bool(st.session_state.get("is_admin", False))

def logout():
    st.session_state["is_admin"] = False
    st.session_state.pop("admin_user", None)

def login_form():
    """
    نموذج تسجيل دخول للأدمن.
    يعتمد على:
      - ADMIN_PASSWORD في secrets
    اختياري:
      - ADMIN_USERS في secrets (مثال: "sahar,manager") لتقييد أسماء المستخدمين
    """
    admin_password = _get_secret("ADMIN_PASSWORD", None)
    if not admin_password:
        st.error("⚠️ ADMIN_PASSWORD غير موجود في Secrets. أضيفيه في Streamlit Cloud → Settings → Secrets.")
        st.stop()

    allowed_users_raw = _get_secret("ADMIN_USERS", "")
    allowed_users = [u.strip().lower() for u in allowed_users_raw.split(",") if u.strip()] if allowed_users_raw else []

    st.subheader("🔐 تسجيل دخول الأدمن")
    user = st.text_input("اسم المستخدم", value="", placeholder="مثال: admin")
    pwd = st.text_input("كلمة المرور", type="password", value="")

    c1, c2 = st.columns([1, 1])
    with c1:
        submit = st.button("دخول", use_container_width=True)
    with c2:
        st.button("تسجيل خروج", use_container_width=True, on_click=logout)

    if submit:
        user_clean = (user or "").strip().lower()

        if allowed_users and (user_clean not in allowed_users):
            st.error("اسم المستخدم غير مسموح.")
            return

        # مقارنة آمنة
        if hmac.compare_digest(str(pwd), str(admin_password)):
            st.session_state["is_admin"] = True
            st.session_state["admin_user"] = user_clean or "admin"
            st.success("✅ تم تسجيل الدخول")
            st.rerun()
        else:
            st.error("كلمة المرور غير صحيحة.")

def require_admin():
    """
    استخدميها في صفحات التعديل.
    """
    if not is_admin():
        st.warning("هذه الصفحة للأدمن فقط. سجلي الدخول أولاً من صفحة 🔐 تسجيل الدخول.")
        st.stop()
