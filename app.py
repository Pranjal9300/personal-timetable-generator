import streamlit as st
import pandas as pd

def load_excel(file):
    return pd.read_excel(file, sheet_name=None)

def generate_personal_timetable(timetable, subjects):
    # Filter the timetable based on the selected subjects
    personal_timetable = timetable[timetable['Subject Code'].isin(subjects)]
    return personal_timetable

def main():
    st.title("Personal Timetable Generator")

    uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

    if uploaded_file:
        sheets = load_excel(uploaded_file)
        timetable = sheets.get("MBA 2023-25_3RD SEMESTER")
        subjects_sheet = sheets.get("FACULTY DETAILS")

        if timetable is not None and subjects_sheet is not None:
            st.subheader("Select Your Subjects")
            subjects = subjects_sheet['Subject Code'].tolist()
            selected_subjects = st.multiselect("Subjects", subjects)

            if selected_subjects:
                personal_timetable = generate_personal_timetable(timetable, selected_subjects)
                st.subheader("Your Personal Timetable")
                st.dataframe(personal_timetable)
            else:
                st.warning("Please select at least one subject.")
        else:
            st.error("The required sheets are not found in the uploaded file.")

if __name__ == "__main__":
    main()
