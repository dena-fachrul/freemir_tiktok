import streamlit as st
import pandas as pd
import re
import io
import os
import xlsxwriter

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="freemir TikTok Pre-Sales Calculation",
    page_icon="📊",
    layout="centered"
)

# --- CUSTOM CSS FOR LIGHT BLUE BACKGROUND ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #E6F3FF;
    }
    div.stButton > button:first-child {
        background-color: #0066CC;
        color: white;
        border-radius: 10px;
    }
    div.stButton > button:hover {
        background-color: #004C99;
        color: white;
    }
    .main-header {
        font-size: 2.5rem;
        color: #003366;
        text-align: center;
        font-weight: 700;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #333;
        text-align: center;
        margin-bottom: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- LOGIC FUNCTIONS (ADAPTED FOR WEB) ---

def process_sku_data(uploaded_file):
    try:
        # Read Excel directly from the uploaded file object
        df = pd.read_excel(uploaded_file, header=1)
        
        if len(df.columns) < 10:
             st.error("Error: Less than 10 columns found. Please check file format.")
             return None

        col_status = df.columns[1]  # Column B
        col_sku = df.columns[6]     # Column G
        col_qty = df.columns[9]     # Column J

        # Filter for status "To Ship" (case insensitive)
        df_filtered = df[df[col_status].astype(str).str.lower() == 'to ship'].copy()
        # Convert QTY to numeric
        df_filtered[col_qty] = pd.to_numeric(df_filtered[col_qty], errors='coerce').fillna(0)

        sku_counter = {}

        # Split & Count
        for index, row in df_filtered.iterrows():
            qty_row = row[col_qty]
            raw_sku_string = str(row[col_sku])
            
            if qty_row <= 0: continue

            # Regex split
            sku_list = re.split(r'[+\-/\s,|]+', raw_sku_string)

            for sku in sku_list:
                sku_clean = sku.strip()
                if len(sku_clean) > 10:
                    sku_counter[sku_clean] = sku_counter.get(sku_clean, 0) + qty_row

        result_df = pd.DataFrame(list(sku_counter.items()), columns=['SKU', 'QTY'])
        return result_df

    except Exception as e:
        st.error(f"Error processing PO data: {e}")
        return None

def enrich_with_tat_data(sku_df, tat_file_path="TAT.xlsx"):
    # Check if TAT file exists in the repo/directory
    if not os.path.exists(tat_file_path):
        st.warning(f"⚠️ Warning: Master data file '{tat_file_path}' not found in repository. Showing SKU and QTY only.")
        sku_df['No'] = range(1, 1 + len(sku_df))
        sku_df['English Name'] = "-"
        sku_df['Chinese Name'] = "-"
        return sku_df[['No', 'SKU', 'QTY', 'English Name', 'Chinese Name']]

    try:
        tat_df = pd.read_excel(tat_file_path, sheet_name='AT1', header=0)
        
        # Get Column A, B, D
        tat_subset = tat_df.iloc[:, [0, 1, 3]].copy()
        tat_subset.columns = ['SKU_REF', 'English Name', 'Chinese Name']

        sku_df['SKU'] = sku_df['SKU'].astype(str).str.strip()
        tat_subset['SKU_REF'] = tat_subset['SKU_REF'].astype(str).str.strip()

        # Merge
        merged_df = pd.merge(sku_df, tat_subset, left_on='SKU', right_on='SKU_REF', how='left')

        merged_df['English Name'] = merged_df['English Name'].fillna('-')
        merged_df['Chinese Name'] = merged_df['Chinese Name'].fillna('-')

        # Sort & Reorder
        merged_df = merged_df.sort_values(by='QTY', ascending=False).reset_index(drop=True)
        merged_df.insert(0, 'No', range(1, 1 + len(merged_df)))
        
        final_cols = ['No', 'SKU', 'QTY', 'English Name', 'Chinese Name']
        return merged_df[final_cols]

    except Exception as e:
        st.error(f"Failed to read TAT.xlsx: {e}")
        return sku_df

def convert_df_to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Summary', index=False, startrow=1, header=False)
    
    workbook = writer.book
    worksheet = writer.sheets['Summary']
    
    # Formats
    header_format = workbook.add_format({
        'bold': True, 'text_wrap': False, 'valign': 'vcenter',
        'fg_color': '#D3D3D3', 'border': 1, 'align': 'center'
    })
    cell_format = workbook.add_format({'border': 1, 'valign': 'vcenter', 'align': 'center'})
    no_wrap_format = workbook.add_format({'border': 1, 'valign': 'vcenter', 'text_wrap': False})

    # Write Header
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
        
    # Write Data
    for row_num in range(len(df)):
        worksheet.write(row_num + 1, 0, df.iloc[row_num, 0], cell_format)
        worksheet.write(row_num + 1, 1, df.iloc[row_num, 1], cell_format)
        worksheet.write(row_num + 1, 2, df.iloc[row_num, 2], cell_format)
        worksheet.write(row_num + 1, 3, df.iloc[row_num, 3], no_wrap_format)
        worksheet.write(row_num + 1, 4, df.iloc[row_num, 4], no_wrap_format)

    # Column Widths
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 8)
    worksheet.set_column('D:E', 35)

    writer.close()
    return output.getvalue()

# --- MAIN APP LAYOUT ---

st.markdown('<div class="main-header">freemir TikTok Pre-Sales Calculation</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload your "TT To Ship" file to generate the SKU summary.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose Excel File (TT To Ship...)", type=['xlsx'])

if uploaded_file is not None:
    with st.spinner('Processing data...'):
        # 1. Process Logic
        raw_df = process_sku_data(uploaded_file)
        
        if raw_df is not None and not raw_df.empty:
            # 2. Enrich with TAT (Looking for TAT.xlsx in the same folder)
            final_df = enrich_with_tat_data(raw_df)
            
            st.success(f"✅ Processing Complete! Found {len(final_df)} unique SKUs.")
            
            # 3. Preview
            st.dataframe(final_df, use_container_width=True)
            
            # 4. Download Button
            excel_data = convert_df_to_excel(final_df)
            
            st.download_button(
                label="📥 Download Result as Excel",
                data=excel_data,
                file_name="SKU_Analysis_Result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No valid data found or processed. Please check your input file.")

# Footer info
st.markdown("---")
st.caption("Backend powered by Python | TAT Database linked via GitHub Repository")
