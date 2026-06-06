import json
import streamlit as st
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="iTeach · School Management",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root tokens ── */
:root {
    --ink:       #0f1117;
    --ink-soft:  #4a5068;
    --paper:     #f7f6f2;
    --card:      #ffffff;
    --accent:    #c0392b;
    --accent2:   #2c3e6b;
    --gold:      #d4a843;
    --border:    #e2dfd8;
    --radius:    14px;
    --shadow:    0 4px 24px rgba(15,17,23,.08);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}
.stApp { background: var(--paper); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--accent2) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    letter-spacing: .02em;
    padding: 6px 0;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.15) !important; }

/* ── Sidebar logo block ── */
.sidebar-logo {
    text-align: center;
    padding: 28px 0 22px;
}
.sidebar-logo .logo-icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 6px;
}
.sidebar-logo .logo-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 700;
    letter-spacing: .04em;
    color: #fff;
}
.sidebar-logo .logo-sub {
    font-size: 0.72rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: rgba(255,255,255,.55);
    margin-top: 2px;
}

/* ── Page header ── */
.page-header {
    background: var(--card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 28px 36px;
    margin-bottom: 28px;
    border-left: 5px solid var(--accent);
    display: flex;
    align-items: center;
    gap: 18px;
}
.page-header .ph-icon { font-size: 2.4rem; }
.page-header .ph-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.75rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--accent2);
}
.page-header .ph-sub {
    font-size: 0.85rem;
    color: var(--ink-soft);
    margin-top: 3px;
}

/* ── Stat cards ── */
.stat-row { display: flex; gap: 20px; margin-bottom: 28px; flex-wrap: wrap; }
.stat-card {
    flex: 1;
    min-width: 160px;
    background: var(--card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 22px 28px;
    border-top: 4px solid var(--gold);
}
.stat-card.alt { border-top-color: var(--accent); }
.stat-card.alt2 { border-top-color: var(--accent2); }
.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1;
}
.stat-label {
    font-size: 0.78rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--ink-soft);
    margin-top: 4px;
}

/* ── Form card ── */
.form-card {
    background: var(--card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 32px 36px;
    margin-bottom: 20px;
}
.form-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: var(--accent2);
    margin-bottom: 22px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border-radius: 9px !important;
    border: 1.5px solid var(--border) !important;
    background: var(--paper) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 10px 14px !important;
    transition: border-color .2s;
    color: #0f1117 !important;
}
.stTextInput > div > div > input::selection,
.stNumberInput > div > div > input::selection {
    color: #0f1117 !important;
    background: #b3c8f5 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--accent2) !important;
    box-shadow: 0 0 0 3px rgba(44,62,107,.12) !important;
}
label[data-testid="stWidgetLabel"] {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    color: var(--ink-soft) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent2) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: .04em !important;
    padding: 10px 28px !important;
    transition: background .2s, transform .15s !important;
    box-shadow: 0 2px 10px rgba(44,62,107,.3) !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    transform: translateY(-1px) !important;
}

/* ── Success / error banners ── */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Data table ── */
.stDataFrame { border-radius: var(--radius) !important; overflow: hidden; }

/* ── Student/teacher detail card ── */
.detail-card {
    background: var(--card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 28px 36px;
    margin-top: 16px;
}
.detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.95rem;
}
.detail-row:last-child { border-bottom: none; }
.detail-key {
    font-weight: 600;
    color: var(--ink-soft);
    font-size: 0.82rem;
    letter-spacing: .07em;
    text-transform: uppercase;
}
.detail-val { font-weight: 500; color: var(--ink); }
.badge {
    display: inline-block;
    background: var(--accent2);
    color: #fff;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: .06em;
}
.badge.gold { background: var(--gold); color: var(--ink); }
.badge.red  { background: var(--accent); }

/* ── Section divider ── */
.section-sep {
    height: 1px;
    background: var(--border);
    margin: 28px 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--paper); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Data helpers ──────────────────────────────────────────────────────────────
DATABASE = "school+data.json"
_DEFAULT  = {"Student": [], "Teacher": []}

def load_data():
    p = Path(DATABASE)
    if p.exists():
        raw = p.read_text()
        if raw:
            return json.loads(raw)
    return _DEFAULT.copy()

def save_data(d):
    Path(DATABASE).write_text(json.dumps(d, indent=4))

def validate_email(e):
    return "@" in e and "." in e

def grade_badge(avg):
    if avg >= 90: return "A+", "gold"
    if avg >= 80: return "A", "gold"
    if avg >= 70: return "B", ""
    if avg >= 60: return "C", ""
    return "D", "red"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🎓</span>
        <div class="logo-title">iTeach</div>
        <div class="logo-sub">School Management</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["📊  Dashboard",
         "🧑‍🎓  Register Student",
         "👩‍🏫  Register Teacher",
         "📝  Add / Update Grade",
         "🔍  Student Details",
         "🔍  Teacher Details",
         "📋  All Records"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    data = load_data()
    st.markdown(f"<div style='font-size:.78rem;color:rgba(255,255,255,.6);text-align:center'>Students: <b style='color:#fff'>{len(data['Student'])}</b> &nbsp;|&nbsp; Teachers: <b style='color:#fff'>{len(data['Teacher'])}</b></div>", unsafe_allow_html=True)


# ── Helper: page header ───────────────────────────────────────────────────────
def page_header(icon, title, subtitle=""):
    st.markdown(f"""
    <div class="page-header">
        <div class="ph-icon">{icon}</div>
        <div>
            <div class="ph-title">{title}</div>
            <div class="ph-sub">{subtitle}</div>
        </div>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  PAGES
# ════════════════════════════════════════════════════════════════════════════

# ── 1. Dashboard ──────────────────────────────────────────────────────────────
if page == "📊  Dashboard":
    data = load_data()
    page_header("📊", "Dashboard", "A bird's-eye view of your institution")

    n_students = len(data["Student"])
    n_teachers  = len(data["Teacher"])
    all_grades  = [g for s in data["Student"] for g in s["grades"].values()]
    avg_all     = round(sum(all_grades)/len(all_grades), 1) if all_grades else 0

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-num">{n_students}</div>
            <div class="stat-label">Students Enrolled</div>
        </div>
        <div class="stat-card alt">
            <div class="stat-num">{n_teachers}</div>
            <div class="stat-label">Teachers on Staff</div>
        </div>
        <div class="stat-card alt2">
            <div class="stat-num">{avg_all}</div>
            <div class="stat-label">Overall Class Average</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{len(all_grades)}</div>
            <div class="stat-label">Grades Recorded</div>
        </div>
    </div>""", unsafe_allow_html=True)

    if data["Student"]:
        import pandas as pd
        rows = []
        for s in data["Student"]:
            g = s["grades"]
            avg = round(sum(g.values())/len(g), 1) if g else 0
            rows.append({
                "Name": s["name"],
                "Roll No": s["roll_no"],
                "Age": s["age"],
                "Subjects Graded": len(g),
                "Average (%)": avg,
            })
        df = pd.DataFrame(rows).sort_values("Roll No")

        st.markdown("#### 🧑‍🎓 Student Overview")
        st.dataframe(df, use_container_width=True, hide_index=True)

    if data["Teacher"]:
        import pandas as pd
        rows = [{"Name": t["name"], "Emp ID": t["emp_id"], "Age": t["age"], "Subject": t["subject"]} for t in data["Teacher"]]
        st.markdown("#### 👩‍🏫 Teacher Overview")
        st.dataframe(pd.DataFrame(rows).sort_values("Emp ID"), use_container_width=True, hide_index=True)


# ── 2. Register Student ───────────────────────────────────────────────────────
elif page == "🧑‍🎓  Register Student":
    page_header("🧑‍🎓", "Register Student", "Add a new student to the system")

    st.markdown('<div class="form-card"><div class="form-card-title">Student Information</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name    = st.text_input("Full Name")
        email   = st.text_input("Student Email")
        roll_no = st.number_input("Roll Number", min_value=1, step=1, format="%d")
    with col2:
        age         = st.number_input("Age", min_value=5, max_value=100, step=1, format="%d")
        parentemail = st.text_input("Parent Email")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✅  Register Student"):
        data = load_data()
        ok = True
        if not name.strip():
            st.error("Name cannot be empty."); ok = False
        elif not validate_email(email):
            st.error("Student email is invalid."); ok = False
        elif not validate_email(parentemail):
            st.error("Parent email is invalid."); ok = False
        elif any(s["roll_no"] == int(roll_no) for s in data["Student"]):
            st.warning("A student with this roll number already exists."); ok = False
        if ok:
            data["Student"].append({
                "name": name.strip(), "age": int(age), "email": email.strip(),
                "parentemail": parentemail.strip(), "roll_no": int(roll_no), "grades": {}
            })
            save_data(data)
            st.success(f"🎉 **{name}** has been registered successfully! (Roll No: {int(roll_no)})")


# ── 3. Register Teacher ───────────────────────────────────────────────────────
elif page == "👩‍🏫  Register Teacher":
    page_header("👩‍🏫", "Register Teacher", "Add a new faculty member")

    st.markdown('<div class="form-card"><div class="form-card-title">Teacher Information</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name    = st.text_input("Full Name")
        email   = st.text_input("Email Address")
        emp_id  = st.number_input("Employee ID", min_value=1, step=1, format="%d")
    with col2:
        age     = st.number_input("Age", min_value=18, max_value=100, step=1, format="%d")
        subject = st.text_input("Subject Taught")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✅  Register Teacher"):
        data = load_data()
        ok = True
        if not name.strip():
            st.error("Name cannot be empty."); ok = False
        elif not validate_email(email):
            st.error("Email is invalid."); ok = False
        elif not subject.strip():
            st.error("Please enter the subject."); ok = False
        elif any(t["emp_id"] == int(emp_id) for t in data["Teacher"]):
            st.warning("Employee ID already registered."); ok = False
        if ok:
            data["Teacher"].append({
                "name": name.strip(), "age": int(age), "email": email.strip(),
                "emp_id": int(emp_id), "subject": subject.strip()
            })
            save_data(data)
            st.success(f"🎉 **{name}** has been registered as a teacher!")


# ── 4. Add / Update Grade ─────────────────────────────────────────────────────
elif page == "📝  Add / Update Grade":
    page_header("📝", "Add / Update Grade", "Record or update a student's subject marks")
    data = load_data()

    if not data["Student"]:
        st.info("No students registered yet. Please register students first.")
    else:
        st.markdown('<div class="form-card"><div class="form-card-title">Grade Entry</div>', unsafe_allow_html=True)

        options = {f"{s['name']}  (Roll {s['roll_no']})": s["roll_no"] for s in data["Student"]}
        selected = st.selectbox("Select Student", list(options.keys()))
        roll_no  = options[selected]

        col1, col2 = st.columns(2)
        with col1:
            subject = st.text_input("Subject")
        with col2:
            marks = st.number_input("Marks (%)", min_value=0.0, max_value=100.0, step=0.5, format="%.1f")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("💾  Save Grade"):
            if not subject.strip():
                st.error("Please enter the subject name.")
            else:
                for s in data["Student"]:
                    if s["roll_no"] == roll_no:
                        s["grades"][subject.strip()] = float(marks)
                        save_data(data)
                        st.success(f"Grade saved — **{subject}**: {marks}% for **{s['name']}**")
                        break

        # Preview existing grades
        for s in data["Student"]:
            if s["roll_no"] == roll_no and s["grades"]:
                st.markdown("---")
                st.markdown(f"**Current grades for {s['name']}**")
                import pandas as pd
                gdf = pd.DataFrame(list(s["grades"].items()), columns=["Subject", "Marks (%)"])
                st.dataframe(gdf, use_container_width=True, hide_index=True)


# ── 5. Student Details ────────────────────────────────────────────────────────
elif page == "🔍  Student Details":
    page_header("🔍", "Student Details", "Look up a student's full profile")
    data = load_data()

    if not data["Student"]:
        st.info("No students registered yet.")
    else:
        options = {f"{s['name']}  (Roll {s['roll_no']})": s["roll_no"] for s in data["Student"]}
        selected = st.selectbox("Select Student", list(options.keys()))
        roll_no  = options[selected]

        for s in data["Student"]:
            if s["roll_no"] == roll_no:
                grades = s["grades"]
                avg    = round(sum(grades.values())/len(grades), 1) if grades else 0
                ltr, badge_cls = grade_badge(avg)

                badge_html = f'<span class="badge {badge_cls}">{ltr}</span>' if grades else '<span class="badge">N/A</span>'

                st.markdown(f"""
                <div class="detail-card">
                    <div class="detail-row"><span class="detail-key">Name</span><span class="detail-val">{s['name']}</span></div>
                    <div class="detail-row"><span class="detail-key">Roll Number</span><span class="detail-val">{s['roll_no']}</span></div>
                    <div class="detail-row"><span class="detail-key">Age</span><span class="detail-val">{s['age']} yrs</span></div>
                    <div class="detail-row"><span class="detail-key">Email</span><span class="detail-val">{s['email']}</span></div>
                    <div class="detail-row"><span class="detail-key">Parent Email</span><span class="detail-val">{s['parentemail']}</span></div>
                    <div class="detail-row"><span class="detail-key">Average</span><span class="detail-val">{avg}% &nbsp;{badge_html}</span></div>
                </div>""", unsafe_allow_html=True)

                if grades:
                    st.markdown("#### 📚 Subject-wise Grades")
                    import pandas as pd
                    gdf = pd.DataFrame(
                        [{"Subject": k, "Marks (%)": v, "Grade": grade_badge(v)[0]} for k, v in grades.items()]
                    )
                    st.dataframe(gdf, use_container_width=True, hide_index=True)
                else:
                    st.info("No grades recorded for this student yet.")
                break


# ── 6. Teacher Details ────────────────────────────────────────────────────────
elif page == "🔍  Teacher Details":
    page_header("🔍", "Teacher Details", "Look up a faculty member's profile")
    data = load_data()

    if not data["Teacher"]:
        st.info("No teachers registered yet.")
    else:
        options = {f"{t['name']}  (ID {t['emp_id']})": t["emp_id"] for t in data["Teacher"]}
        selected = st.selectbox("Select Teacher", list(options.keys()))
        emp_id   = options[selected]

        for t in data["Teacher"]:
            if t["emp_id"] == emp_id:
                st.markdown(f"""
                <div class="detail-card">
                    <div class="detail-row"><span class="detail-key">Name</span><span class="detail-val">{t['name']}</span></div>
                    <div class="detail-row"><span class="detail-key">Employee ID</span><span class="detail-val">{t['emp_id']}</span></div>
                    <div class="detail-row"><span class="detail-key">Age</span><span class="detail-val">{t['age']} yrs</span></div>
                    <div class="detail-row"><span class="detail-key">Email</span><span class="detail-val">{t['email']}</span></div>
                    <div class="detail-row"><span class="detail-key">Subject</span><span class="detail-val"><span class="badge">{t['subject']}</span></span></div>
                </div>""", unsafe_allow_html=True)
                break


# ── 7. All Records ────────────────────────────────────────────────────────────
elif page == "📋  All Records":
    page_header("📋", "All Records", "Complete roster of students and teachers")
    data = load_data()
    import pandas as pd

    tab1, tab2 = st.tabs(["🧑‍🎓  Students", "👩‍🏫  Teachers"])

    with tab1:
        if not data["Student"]:
            st.info("No students registered yet.")
        else:
            rows = []
            for s in data["Student"]:
                g = s["grades"]
                avg = round(sum(g.values())/len(g), 1) if g else 0
                rows.append({
                    "Roll No": s["roll_no"], "Name": s["name"], "Age": s["age"],
                    "Email": s["email"], "Parent Email": s["parentemail"],
                    "Subjects": len(g), "Average (%)": avg
                })
            st.dataframe(pd.DataFrame(rows).sort_values("Roll No"), use_container_width=True, hide_index=True)

    with tab2:
        if not data["Teacher"]:
            st.info("No teachers registered yet.")
        else:
            rows = [{"Emp ID": t["emp_id"], "Name": t["name"], "Age": t["age"],
                     "Email": t["email"], "Subject": t["subject"]} for t in data["Teacher"]]
            st.dataframe(pd.DataFrame(rows).sort_values("Emp ID"), use_container_width=True, hide_index=True)