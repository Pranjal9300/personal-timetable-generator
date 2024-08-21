import streamlit as st
import pandas as pd

def load_excel(file):
    # Load the entire Excel file
    return pd.read_excel(file, sheet_name=None)

def get_section_timetable(timetable_sheet, section):
    # Define where each section starts based on the section name
    section_start = {
        'A': 0,
        'B': 14,
        'C': 28
    }
    
    start_row = section_start.get(section)
    end_row = start_row + 12 if start_row is not None else None

    if start_row is not None and end_row is not None:
        section_timetable = timetable_sheet.iloc[start_row:end_row]
        return section_timetable
    else:
        return None

def filter_timetable_by_subjects(timetable, selected_subjects):
    # Filter the timetable to only include selected subjects
    filtered_timetable = timetable[timetable.apply(lambda row: any(sub in str(row.values) for sub in selected_subjects), axis=1)]
    return filtered_timetable

def main():
    st.title("Personal Timetable Generator")

    uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

    if uploaded_file:
        sheets = load_excel(uploaded_file)
        timetable_sheet = sheets.get("MBA 2023-25_3RD SEMESTER")
        subjects_sheet = sheets.get("FACULTY DETAILS")

        if timetable_sheet is not None and subjects_sheet is not None:
            sections = ['A', 'B', 'C']
            selected_section = st.selectbox("Select your Section", sections)

            if selected_section:
                st.subheader("Select Your Subjects")
                # Combine course title and abbreviation for selection
                subjects = subjects_sheet[['Cours Code', 'Course Title', 'Abbreviation']].drop_duplicates()
                subjects['Display'] = subjects['Course Title'] + " (" + subjects['Abbreviation'] + ")"
                subject_options = subjects['Display'].tolist()

                selected_subjects = st.multiselect("Subjects", subject_options)

                if selected_subjects:
                    # Extract just the abbreviations to filter the timetable
                    selected_abbreviations = [sub.split('(')[-1].replace(')', '') for sub in selected_subjects]

                    # Get the timetable for the selected section
                    section_timetable = get_section_timetable(timetable_sheet, selected_section)

                    if section_timetable is not None:
                        # Filter the timetable by the selected subjects
                        personal_timetable = filter_timetable_by_subjects(section_timetable, selected_abbreviations)
                        st.subheader("Your Personal Timetable")
                        st.dataframe(personal_timetable)
                    else:
                        st.error(f"Timetable for Section {selected_section} not found.")
                else:
                    st.warning("Please select at least one subject.")
        else:
            st.error("The required sheets are not found in the uploaded file.")

if __name__ == "__main__":
    main()
