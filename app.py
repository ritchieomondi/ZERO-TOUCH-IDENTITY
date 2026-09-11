import streamlit as st
import pandas as pd
import time
from provisioner import run_provisioning_pipeline

st.set_page_config(
    page_title="Identity Provisioner",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Header
st.markdown("## Identity")
st.caption("Zero-Touch Active Directory & Entra ID Provisioning")

# 1. File Uploader
uploaded_file = st.file_uploader("Upload HR CSV File", type=["csv"], label_visibility="collapsed")

if uploaded_file is not None:
    df_input = pd.read_csv(uploaded_file)

    st.markdown("##### Staged HR Records")
    st.dataframe(df_input, use_container_width=True, hide_index=True)

    st.write("")

    # 2. Trigger Button
    if st.button("Run Zero-Touch Provisioning"):
        progress_text = st.empty()
        progress_bar = st.progress(0)

        def update_progress(percent):
            progress_bar.progress(percent)
            progress_text.caption(f"Processing batch... {int(percent * 100)}%")

        try:
            results_df = run_provisioning_pipeline(df_input, progress_callback=update_progress)
            
            time.sleep(0.2)
            progress_text.empty()
            progress_bar.empty()

            st.success("✨ Provisioning Completed!")
            st.dataframe(results_df, use_container_width=True, hide_index=True)

            # Convert audit log to CSV for export
            csv_report = results_df.to_csv(index=False).encode('utf-8')

            st.write("")
            st.download_button(
                label="S DOWNLOAD Audit Report (CSV)",
                data=csv_report,
                file_name="provisioning_audit_report.csv",
                mime="text/csv"
            )

        except Exception as e:
            progress_text.empty()
            progress_bar.empty()
            st.error(f"Execution Error: {str(e)}")

else:
    st.info(" Please upload your `employees.csv` file to begin.")