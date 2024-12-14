import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_info = st.secrets["google_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

spreadsheet_name = "app"
worksheet_name_votes = "vote_counts"
worksheet_name_names = "voter_names"

sheet_votes = client.open(spreadsheet_name).worksheet(worksheet_name_votes)
sheet_names = client.open(spreadsheet_name).worksheet(worksheet_name_names)

def record_vote(voter_name, candidate):
    voters = sheet_names.col_values(1) 
    if voter_name in voters:
        st.error(f"{voter_name} さんは既に投票済みです。")
        return
    sheet_names.append_row([voter_name])  

  
    headers = sheet_votes.row_values(1)  
    if candidate in headers:
        col_index = headers.index(candidate) + 1
        current_votes = int(sheet_votes.cell(2, col_index).value or 0)
        sheet_votes.update_cell(2, col_index, current_votes + 1)

st.title("会長投票フォーム")
st.write("投票者は記録されますが、投票先は記録されません")

candidates = ["いっせい", "るい"]

with st.form("vote_form"):
    voter_name = st.text_input("あなたの名前を入力してください")
    candidate = st.selectbox("投票先を選んでください", candidates)
    submitted = st.form_submit_button("投票する")

if submitted:
    if not voter_name.strip():
        st.error("投票者名を入力してください。")
    else:
        record_vote(voter_name, candidate)
        st.success("投票が完了しました！ありがとうございました。")
