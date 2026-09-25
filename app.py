import streamlit as st
import time
from pathlib import Path

# Set Page Config
st.set_page_config(
    page_title="SecureDoc AI - Sensitive Data Detection & Protection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Imports
from styles import inject_custom_css
from auth import login_user, register_user
from database import db
from pdf_processor import PDFProcessor
from detector import SensitiveDataDetector
from risk_assessor import RiskAssessor
from redactor import PDFRedactor
from encryptor import PDFEncryptor
from temp_manager import TempFileManager
from logger import log_activity, get_user_activity_logs, log_file_metadata, update_file_action, get_user_file_history

# Inject CSS
inject_custom_css()

# Session State Initialization
if "user" not in st.session_state:
    st.session_state.user = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

if "file_data" not in st.session_state:
    st.session_state.file_data = {
        "temp_uploaded_path": None,
        "filename": None,
        "pages_data": [],
        "total_pages": 0,
        "full_text": "",
        "detections": [],
        "summary_counts": {},
        "total_count": 0,
        "risk_level": "LOW",
        "risk_score": 0,
        "risk_desc": "",
        "processed_path": None,
        "selected_action": None,
        "file_id": None
    }

# Helper to reset file state
def reset_file_state():
    if st.session_state.file_data["temp_uploaded_path"]:
        TempFileManager.cleanup_file(st.session_state.file_data["temp_uploaded_path"])
    if st.session_state.file_data["processed_path"]:
        TempFileManager.cleanup_file(st.session_state.file_data["processed_path"])
        
    st.session_state.file_data = {
        "temp_uploaded_path": None,
        "filename": None,
        "pages_data": [],
        "total_pages": 0,
        "full_text": "",
        "detections": [],
        "summary_counts": {},
        "total_count": 0,
        "risk_level": "LOW",
        "risk_score": 0,
        "risk_desc": "",
        "processed_path": None,
        "selected_action": None,
        "file_id": None
    }

# Render Navigation Sidebar
def render_sidebar():
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-logo-container">
                <div class="shield-badge">🛡️</div>
                <div class="logo-title">SecureDoc <span>AI</span></div>
            </div>
        """, unsafe_allow_html=True)

        user = st.session_state.user
        if user:
            st.markdown(f"<p style='color:#94a3b8; font-size:0.85rem; padding:0 8px; margin-bottom:1.5rem;'>Logged in as: <b style='color:#ffffff;'>{user['name']}</b></p>", unsafe_allow_html=True)
            
            # Nav buttons
            curr = st.session_state.current_page
            
            if st.button("🏠  Home / Upload", key="nav_home", use_container_width=True):
                st.session_state.current_page = "upload"
                st.rerun()
                
            if st.button("📜  History & Logs", key="nav_history", use_container_width=True):
                st.session_state.current_page = "history"
                st.rerun()

            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            
            if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
                log_activity(user["user_id"], "User Logged Out", "")
                reset_file_state()
                st.session_state.user = None
                st.session_state.current_page = "login"
                st.rerun()

# --- 1. LOGIN & REGISTER SCREEN ---
def render_auth():
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown("""
        <div style="display: flex; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.08); margin-top: 2rem;">
            <div style="flex: 1; background: #0b1324; padding: 4rem 3rem; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; color: white;">
                <div style="width: 72px; height: 72px; background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 36px; margin-bottom: 1.5rem; box-shadow: 0 10px 25px rgba(37,99,235,0.4);">
                    🛡️
                </div>
                <h1 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #ffffff;">SecureDoc <span style="color:#60a5fa;">AI</span></h1>
                <p style="color: #94a3b8; font-size: 1rem; max-width: 280px; line-height: 1.5;">Detect. Protect. Share Safely.</p>
            </div>
            <div style="flex: 1.2; padding: 4rem 3.5rem; background: #ffffff;">
        """, unsafe_allow_html=True)

        if st.session_state.current_page == "login":
            st.markdown("<h2 style='font-size: 1.75rem; font-weight: 700; color: #0f172a; margin-bottom: 4px;'>Welcome Back</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #64748b; font-size: 0.95rem; margin-bottom: 2rem;'>Sign in to your account</p>", unsafe_allow_html=True)

            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Sign In", use_container_width=True)

                if submit:
                    success, res = login_user(email, password)
                    if success:
                        st.session_state.user = res
                        st.session_state.current_page = "upload"
                        st.success("Login successful!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(res)

            st.markdown("<p style='text-align: center; color: #64748b; margin-top: 1.5rem; font-size: 0.9rem;'>Don't have an account? </p>", unsafe_allow_html=True)
            if st.button("Sign Up", key="goto_signup", use_container_width=True):
                st.session_state.current_page = "register"
                st.rerun()

        elif st.session_state.current_page == "register":
            st.markdown("<h2 style='font-size: 1.75rem; font-weight: 700; color: #0f172a; margin-bottom: 4px;'>Create Account</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #64748b; font-size: 0.95rem; margin-bottom: 2rem;'>Get started with SecureDoc AI</p>", unsafe_allow_html=True)

            with st.form("register_form"):
                name = st.text_input("Full Name", placeholder="John Doe")
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Create Account", use_container_width=True)

                if submit:
                    success, res = register_user(name, email, password)
                    if success:
                        st.success("Account created successfully! Please sign in.")
                        time.sleep(1)
                        st.session_state.current_page = "login"
                        st.rerun()
                    else:
                        st.error(res)

            st.markdown("<p style='text-align: center; color: #64748b; margin-top: 1.5rem; font-size: 0.9rem;'>Already have an account? </p>", unsafe_allow_html=True)
            if st.button("Sign In", key="goto_signin", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)

# --- 2. UPLOAD DOCUMENT SCREEN ---
def render_upload():
    render_sidebar()
    
    st.markdown("<div class='page-title'>Upload Document</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Upload your PDF to scan for sensitive information.</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drag & drop your PDF here", type=["pdf"], key="pdf_uploader", label_visibility="collapsed")

    if uploaded_file is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info(f"📄 **Selected File:** {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
            
            if st.button("🔍 Scan Document", key="btn_scan", use_container_width=True):
                with st.spinner("Processing PDF and extracting text..."):
                    # Save temp file
                    temp_path = TempFileManager.save_uploaded_temp_file(uploaded_file)
                    
                    # Validate PDF
                    valid, msg = PDFProcessor.validate_pdf(temp_path)
                    if not valid:
                        st.error(msg)
                        TempFileManager.cleanup_file(temp_path)
                        return

                    # Extract text
                    pages_data, total_pages, full_text = PDFProcessor.extract_text(temp_path)

                    # Scan sensitive data
                    detections, summary_counts, total_count = SensitiveDataDetector.scan_pages(pages_data)

                    # Evaluate risk
                    risk_level, risk_score, risk_desc = RiskAssessor.evaluate_risk(summary_counts, total_count)

                    # Save scan metadata to DB
                    file_id = log_file_metadata(
                        user_id=st.session_state.user["user_id"],
                        filename=uploaded_file.name,
                        risk_level=risk_level,
                        detected_count=total_count,
                        action="Scanned"
                    )

                    log_activity(
                        st.session_state.user["user_id"],
                        f"Scanned PDF document (Risk: {risk_level}, Found: {total_count})",
                        uploaded_file.name
                    )

                    # Store in session
                    st.session_state.file_data.update({
                        "temp_uploaded_path": temp_path,
                        "filename": uploaded_file.name,
                        "pages_data": pages_data,
                        "total_pages": total_pages,
                        "full_text": full_text,
                        "detections": detections,
                        "summary_counts": summary_counts,
                        "total_count": total_count,
                        "risk_level": risk_level,
                        "risk_score": risk_score,
                        "risk_desc": risk_desc,
                        "file_id": file_id
                    })

                    st.session_state.current_page = "scan_results"
                    st.rerun()

    st.markdown("<p style='text-align:center; color:#94a3b8; font-size:0.85rem; margin-top:2rem;'>Only PDF files are supported.</p>", unsafe_allow_html=True)

# --- 3. SCAN RESULTS SCREEN ---
def render_scan_results():
    render_sidebar()
    fd = st.session_state.file_data

    # Header with Risk Badge
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("<div class='page-title'>Scan Results</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-subtitle'>Sensitive information detected in your document.</div>", unsafe_allow_html=True)
    with c2:
        r_cls = "risk-badge-high" if fd["risk_level"] == "HIGH" else "risk-badge-medium" if fd["risk_level"] == "MEDIUM" else "risk-badge-low"
        st.markdown(f"<div style='text-align:right; margin-top:10px;'><span class='risk-badge {r_cls}'>⚠️ {fd['risk_level']} Risk</span></div>", unsafe_allow_html=True)

    # Metric Summary Cards
    counts = fd["summary_counts"]
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric-card metric-card-aadhaar">
            <div style="font-size:20px;">🪪</div>
            <div class="metric-title">Aadhaar</div>
            <div class="metric-count" style="color:#dc2626;">{counts.get('Aadhaar', 0)} found</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card metric-card-pan">
            <div style="font-size:20px;">💳</div>
            <div class="metric-title">PAN</div>
            <div class="metric-count" style="color:#d97706;">{counts.get('PAN', 0)} found</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card metric-card-password">
            <div style="font-size:20px;">🔑</div>
            <div class="metric-title">Passwords</div>
            <div class="metric-count" style="color:#2563eb;">{counts.get('Password', 0)} found</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card metric-card-apikey">
            <div style="font-size:20px;">💻</div>
            <div class="metric-title">API Keys</div>
            <div class="metric-count" style="color:#9333ea;">{counts.get('API Key', 0)} found</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Detailed Detected Information Table
    st.markdown("<h3 style='font-size:1.1rem; font-weight:700; color:#0f172a;'>Detected Information</h3>", unsafe_allow_html=True)

    if fd["detections"]:
        rows_html = ""
        category_icons = {
            "Aadhaar": "🪪",
            "PAN": "💳",
            "Password": "🔑",
            "API Key": "💻",
            "Credit Card": "💳",
            "Phone Number": "📞",
            "Email": "✉️"
        }

        for item in fd["detections"]:
            icon = category_icons.get(item["type"], "⚠️")
            rows_html += f"""
            <tr>
                <td><span style="margin-right:8px;">{icon}</span> {item['type']}</td>
                <td style="font-family:monospace; letter-spacing:1px; font-weight:600;">{item['masked_value']}</td>
                <td>Page {item['page_num']}</td>
            </tr>
            """

        table_html = f"""
        <table class="detected-table">
            <thead>
                <tr>
                    <th>Type</th>
                    <th>Masked Pattern Preview</th>
                    <th>Location</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.success("🎉 No sensitive information detected in this document.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue to Protection Options ➔", key="goto_actions", use_container_width=True):
            st.session_state.current_page = "choose_action"
            st.rerun()

# --- 4. CHOOSE AN ACTION SCREEN ---
def render_choose_action():
    render_sidebar()
    st.markdown("<div class='page-title'>Choose an Action</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Select how you want to protect your document.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="action-card">
            <div>
                <div class="action-icon">🎭</div>
                <div class="action-title">Remove / Mask Sensitive Data</div>
                <div class="action-desc">Generate a clean PDF with sensitive information removed or permanently masked with black redaction annotations.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Clean PDF", key="btn_redact", use_container_width=True):
            st.session_state.file_data["selected_action"] = "Masked"
            st.session_state.current_page = "processing"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="action-card">
            <div>
                <div class="action-icon">🔒</div>
                <div class="action-title">Encrypt Entire PDF</div>
                <div class="action-desc">Secure your complete document with strong AES-256 password encryption preventing unauthorized opening.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔑 Set PDF Encryption Password", expanded=False):
            with st.form("pwd_form"):
                pdf_pwd = st.text_input("Enter Password", type="password")
                confirm_pwd = st.text_input("Confirm Password", type="password")
                sub_pwd = st.form_submit_button("Encrypt PDF", use_container_width=True)

                if sub_pwd:
                    if not pdf_pwd or len(pdf_pwd) < 4:
                        st.error("Password must be at least 4 characters.")
                    elif pdf_pwd != confirm_pwd:
                        st.error("Passwords do not match.")
                    else:
                        st.session_state.file_data["encryption_password"] = pdf_pwd
                        st.session_state.file_data["selected_action"] = "Encrypted"
                        st.session_state.current_page = "processing"
                        st.rerun()

# --- 5. PROCESSING SCREEN ---
def render_processing():
    render_sidebar()
    fd = st.session_state.file_data

    st.markdown("""
    <div style="text-align:center; padding: 4rem 1rem;">
        <div style="width:70px; height:70px; border: 5px solid #e0e7ff; border-top: 5px solid #2563eb; border-radius:50%; margin: 0 auto 1.5rem auto; animation: spin 1s linear infinite;"></div>
        <h2 style="font-size:1.75rem; font-weight:700; color:#0f172a; margin-bottom:8px;">Processing Document</h2>
        <p style="color:#64748b; font-size:1rem;">Please wait while we secure your document...</p>
        
        <div class="pipeline-container">
            <div class="pipeline-step"><div class="pipeline-icon-complete">✓</div> Extracting Text</div>
            <div class="pipeline-line"></div>
            <div class="pipeline-step"><div class="pipeline-icon-complete">✓</div> Detecting Sensitive Data</div>
            <div class="pipeline-line"></div>
            <div class="pipeline-step pipeline-step-active"><div class="pipeline-icon-active"></div> Applying Protection</div>
            <div class="pipeline-line"></div>
            <div class="pipeline-step"><div class="pipeline-icon-empty"></div> Finalizing</div>
        </div>
    </div>
    <style>
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)

    input_path = fd["temp_uploaded_path"]
    out_path = TempFileManager.get_output_temp_path(prefix="secured")

    action = fd.get("selected_action", "Masked")
    success = False

    if action == "Masked":
        success = PDFRedactor.redact_pdf(input_path, out_path, fd["detections"])
    elif action == "Encrypted":
        pwd = fd.get("encryption_password", "Secret123")
        success = PDFEncryptor.encrypt_pdf(input_path, out_path, pwd)

    time.sleep(1.2)  # Smooth transition feel

    if success:
        fd["processed_path"] = out_path
        if fd["file_id"]:
            update_file_action(fd["file_id"], action)
        
        log_activity(
            st.session_state.user["user_id"],
            f"Applied '{action}' protection to document",
            fd["filename"]
        )

        st.session_state.current_page = "ready"
        st.rerun()
    else:
        st.error("Document protection processing failed. Please try again.")

# --- 6. READY / DOWNLOAD SCREEN ---
def render_ready():
    render_sidebar()
    fd = st.session_state.file_data

    st.markdown("""
    <div style="text-align:center; padding: 4rem 1rem;">
        <div style="width:80px; height:80px; background:#dcfce7; color:#16a34a; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:40px; margin: 0 auto 1.5rem auto; box-shadow:0 10px 25px rgba(22,163,74,0.2);">
            ✓
        </div>
        <h2 style="font-size:2rem; font-weight:700; color:#0f172a; margin-bottom:8px;">Your PDF is Ready!</h2>
        <p style="color:#64748b; font-size:1.05rem; margin-bottom:2.5rem;">Your document has been successfully processed.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        processed_path = fd["processed_path"]
        if processed_path and Path(processed_path).exists():
            with open(processed_path, "rb") as f:
                pdf_bytes = f.read()

            file_prefix = "Redacted" if fd["selected_action"] == "Masked" else "Encrypted"
            dl_filename = f"{file_prefix}_{fd['filename']}"

            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=dl_filename,
                mime="application/pdf",
                use_container_width=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Scan Another Document", key="btn_another", use_container_width=True):
            reset_file_state()
            st.session_state.current_page = "upload"
            st.rerun()

# --- 7. HISTORY SCREEN ---
def render_history():
    render_sidebar()
    st.markdown("<div class='page-title'>History & Audit Logs</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Review past scanned files and security activity logs.</div>", unsafe_allow_html=True)

    user_id = st.session_state.user["user_id"]
    history = get_user_file_history(user_id)
    logs = get_user_activity_logs(user_id)

    tab1, tab2 = st.tabs(["📄 Processed Documents History", "📜 System Activity Logs"])

    with tab1:
        if history:
            rows_html = ""
            for item in history:
                r_cls = "risk-badge-high" if item['risk_level'] == "HIGH" else "risk-badge-medium" if item['risk_level'] == "MEDIUM" else "risk-badge-low"
                rows_html += f"""
                <tr>
                    <td><b>{item['original_filename']}</b></td>
                    <td><span class='risk-badge {r_cls}'>{item['risk_level']}</span></td>
                    <td>{item['detected_count']} items</td>
                    <td><span style="background:#e0e7ff; color:#3730a3; padding:4px 10px; border-radius:6px; font-weight:600; font-size:0.85rem;">{item['selected_action']}</span></td>
                    <td>{item['created_at']}</td>
                </tr>
                """
            st.markdown(f"""
            <table class="detected-table">
                <thead>
                    <tr>
                        <th>File Name</th>
                        <th>Risk Level</th>
                        <th>Detections Count</th>
                        <th>Action Performed</th>
                        <th>Date / Time</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)
        else:
            st.info("No file history recorded yet.")

    with tab2:
        if logs:
            log_rows = ""
            for log in logs:
                log_rows += f"""
                <tr>
                    <td>{log['timestamp']}</td>
                    <td><b>{log['action']}</b></td>
                    <td>{log['filename'] or '-'}</td>
                </tr>
                """
            st.markdown(f"""
            <table class="detected-table">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Action</th>
                        <th>Associated File</th>
                    </tr>
                </thead>
                <tbody>{log_rows}</tbody>
            </table>
            """, unsafe_allow_html=True)
        else:
            st.info("No activity logs available.")

# App Main Router
def main():
    if not db.connected:
        st.error(f"⚠️ MySQL Database Connection Failed:\n\n{db.connection_error}")
        st.warning("👉 Please ensure your MySQL server is running and update `DB_PASSWORD` in your `.env` file.")
        return

    if not st.session_state.user:
        render_auth()
    else:
        page = st.session_state.current_page
        if page == "upload":
            render_upload()
        elif page == "scan_results":
            render_scan_results()
        elif page == "choose_action":
            render_choose_action()
        elif page == "processing":
            render_processing()
        elif page == "ready":
            render_ready()
        elif page == "history":
            render_history()
        else:
            render_upload()

if __name__ == "__main__":
    main()
