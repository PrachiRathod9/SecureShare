import streamlit as st

def inject_custom_css():
    """Injects custom CSS to turn Streamlit into an exact visual replica of the reference UI design."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Main Root Reset & Font */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #f8fafc !important;
        color: #1e293b !important;
    }

    /* Hide default Streamlit headers, footers & hamburger menu */
    header[data-testid="stHeader"] { visibility: hidden; height: 0; }
    footer { visibility: hidden; height: 0; }
    #MainMenu { visibility: hidden; }

    /* Remove default top padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1200px !important;
    }

    /* Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b1324 !important;
        width: 260px !important;
        border-right: 1px solid #1e293b;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding: 1.5rem 1rem !important;
    }

    /* Sidebar Logo Header */
    .sidebar-logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 2rem;
        padding: 0 8px;
    }
    
    .shield-badge {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }

    .logo-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.25rem;
        letter-spacing: -0.5px;
    }

    .logo-title span {
        color: #60a5fa;
    }

    /* Custom Navigation Buttons in Sidebar */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    .nav-btn > button {
        width: 100% !important;
        background-color: transparent !important;
        color: #94a3b8 !important;
        border: none !important;
        text-align: left !important;
        padding: 10px 14px !important;
        font-size: 0.95rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }

    .nav-btn > button:hover {
        background-color: #1e293b !important;
        color: #f8fafc !important;
    }

    .nav-btn-active > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }

    /* Main Section Titles */
    .page-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .page-subtitle {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* Auth Page Split Screen */
    .auth-container {
        display: flex;
        min-height: 80vh;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        background: #ffffff;
    }

    .auth-left {
        flex: 1;
        background: #0b1324;
        background-image: radial-gradient(circle at 50% 50%, #1e293b 0%, #0b1324 100%);
        padding: 3rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
        position: relative;
    }

    .auth-left-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4);
    }

    .auth-left h1 {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .auth-left p {
        color: #94a3b8;
        font-size: 1rem;
    }

    .auth-right {
        flex: 1;
        padding: 3.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: #ffffff;
    }

    /* Dashed Upload Box */
    .upload-box {
        border: 2px dashed #cbd5e1;
        background-color: #ffffff;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        transition: border-color 0.2s ease;
        margin-bottom: 1rem;
    }

    .upload-box:hover {
        border-color: #2563eb;
    }

    .upload-icon {
        font-size: 48px;
        color: #64748b;
        margin-bottom: 1rem;
    }

    /* Primary Action Buttons */
    .btn-primary > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 12px 28px !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }

    .btn-primary > button:hover {
        background-color: #1d4ed8 !important;
    }

    .btn-secondary > button {
        background-color: #e0e7ff !important;
        color: #3730a3 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        border: none !important;
    }

    .btn-secondary > button:hover {
        background-color: #c7d2fe !important;
    }

    /* Risk Badges */
    .risk-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .risk-badge-high {
        background-color: #fee2e2;
        color: #dc2626;
        border: 1px solid #fca5a5;
    }

    .risk-badge-medium {
        background-color: #fef3c7;
        color: #d97706;
        border: 1px solid #fcd34d;
    }

    .risk-badge-low {
        background-color: #dcfce7;
        color: #16a34a;
        border: 1px solid #86efac;
    }

    /* Metric Summary Cards */
    .metric-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #f1f5f9;
    }

    .metric-card-aadhaar { background: #fef2f2; border-color: #fee2e2; }
    .metric-card-pan { background: #fffbe5; border-color: #fef08a; }
    .metric-card-password { background: #eff6ff; border-color: #dbeafe; }
    .metric-card-apikey { background: #f3e8ff; border-color: #e9d5ff; }

    .metric-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #475569;
    }

    .metric-count {
        font-size: 1.25rem;
        font-weight: 700;
    }

    /* Detected Table Styling */
    .detected-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: #ffffff;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        margin-top: 1rem;
    }

    .detected-table th {
        background: #f8fafc;
        padding: 14px 20px;
        font-weight: 600;
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid #e2e8f0;
        text-align: left;
    }

    .detected-table td {
        padding: 16px 20px;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.95rem;
        color: #334155;
    }

    .detected-table tr:last-child td {
        border-bottom: none;
    }

    /* Action Cards (Remove vs Encrypt) */
    .action-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .action-icon {
        width: 64px;
        height: 64px;
        border-radius: 16px;
        background: #eff6ff;
        color: #2563eb;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        margin-bottom: 1.25rem;
    }

    .action-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }

    .action-desc {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 1.75rem;
        line-height: 1.5;
    }

    /* Processing Pipeline Steps */
    .pipeline-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 3rem;
    }

    .pipeline-step {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
    }

    .pipeline-step-active {
        color: #2563eb;
    }

    .pipeline-icon-complete {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #2563eb;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
    }

    .pipeline-icon-active {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 3px solid #2563eb;
        background: white;
    }

    .pipeline-icon-empty {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 2px solid #cbd5e1;
        background: white;
    }

    .pipeline-line {
        height: 2px;
        width: 40px;
        background: #e2e8f0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
