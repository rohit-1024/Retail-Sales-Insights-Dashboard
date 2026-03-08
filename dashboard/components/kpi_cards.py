import streamlit as st

def kpi_card(title, value, delta=None, up=True):

    arrow = "▲" if up else "▼"
    delta_color = "#22c55e" if up else "#ef4444"

    delta_html = ""
    if delta:
        delta_html = f"""
        <p style="margin:0; font-size:14px; color:{delta_color};">
        {arrow} {delta}
        </p>
        """

    st.markdown(
        f"""
        <div style="
            padding:22px;
            border-radius:12px;
            background-color:#1f2937;
            border:1px solid #374151;
            box-shadow:0px 4px 10px rgba(0,0,0,0.3);
            text-align:center;
        ">

        <p style="
            margin:0;
            font-size:15px;
            color:#9ca3af;
            font-weight:500;
        ">
        {title}
        </p>

        <p style="
            margin:6px 0 0 0;
            font-size:32px;
            font-weight:700;
            color:white;
        ">
        {value}
        </p>

        {delta_html}

        </div>
        """,
        unsafe_allow_html=True
    )