import streamlit as st
from openai import OpenAI
#from sk import my_sk  # Importing the API key securely

# Initialize the OpenAI API with your key
# client = OpenAI(api_key=my_sk)
client = OpenAI(api_key=st.secrets["api_key"])

st.set_page_config(layout="wide")

def add_date_to_notes():
    selected_date = st.session_state['meeting_date']
    formatted_date = selected_date.strftime('%Y-%m-%d')  # Format the date as you prefer
    add_helper_text(f"{formatted_date}")
    
def add_helper_text(helper_text):
    # This function appends helper text to the existing notes
    current_notes = st.session_state.notes
    if current_notes is not None:
        st.session_state.notes = f"{current_notes}\n{helper_text}"
    else:
        st.session_state.notes = helper_text

def add_emoji_to_notes(emoji):
    current_notes = st.session_state.notes
    if current_notes is not None:
        st.session_state.notes = f"{current_notes}\n{emoji}"
    else:
        st.session_state.notes = emoji
    
def process_notes(notes):
    try:
        prompt = 'You are a helpful assistant. You will do the minutes of a meeting precisely. The output would be with markdown'
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": notes}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Define the function to set a flag for copying, instead of copying directly
def prepare_copy_processed_to_notes():
    st.session_state.copy_processed = True

    

if 'notes' not in st.session_state:
    st.session_state.notes = ''
if 'processed_notes' not in st.session_state:
    st.session_state.processed_notes = ''
if 'previous_notes' not in st.session_state:
    st.session_state['previous_notes'] = ''


st.subheader("Meeting Notes Enhancer")

with st.expander("Welcome to **Meeting Notes Enhancer**! This tool is designed to make your meeting documentation process as efficient and effective as possible.Get started now and transform your meeting notes into powerful resources!"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🕒 Save Time**
        - Automate the structuring of meeting notes.
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        **🔍 Enhance Clarity**
        - Use templates and emojis for clearer notes.
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        **💼 Improve Productivity**
        - Edit formatted minutes for precise documentation.
        """, unsafe_allow_html=True)
st.write (" ")

with st.sidebar:
    
    st.write("**Quick actions**")  
    col1, col2, col3 = st.columns(3)
    
    with col1:    
        st.write ("Templates")
    with col2:
        if st.button("Short"):
          add_helper_text("""
                ## Meeting Summary
                - **Date:** 
                - **Participants:** 
                - **Agenda:** 
                ## Key Points
                ## Action Items
                """)
    with col3:
        if st.button("Long"):
            add_helper_text("""
            ## Meeting Details
            - **Date:** 
            - **Participants:** 
            - **Location:** 
            - **Agenda:** 
            ### Discussion Points
            ### Decisions Made
            ### Action Items
            - [ ] Action 1: Assigned to 
            - [ ] Action 2: Assigned to 
            ### Notes
            """)
            
    #st.header("Emojsdfis")
    with st.expander("Emojis",expanded=True):
        # Define your emojis
        meeting_emojis = ["📅", "🔑", "✅", "❌", "👥", "🔄", "💡", "📝", "🔔", "⏰",
                          "📈", "📉", "💬", "🔒", "🔓", "📎", "🖇️", "🧾", "✉️", "📚"]
        
        # Create a grid layout for emojis within the expander
        emoji_groups = [meeting_emojis[i:i + 5] for i in range(0, len(meeting_emojis), 5)]
        
        for group in emoji_groups:
            cols = st.columns(len(group))  # Adjust number of columns based on group size
            for col, emoji in zip(cols, group):
                if col.button(emoji, key=f"emoji_{emoji}"):
                    add_emoji_to_notes(emoji)

    meeting_date = st.date_input("Select Meeting Date", key="meeting_date", on_change=add_date_to_notes)
  

    #st.header("Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Action"):
            add_helper_text("### Next Action\n- ")
    with col2:
        if st.button("🤝 Agree"):
            add_helper_text("### Agreement\n- ")
    with col3:
        if st.button("👤 Person"):
            add_helper_text("### Participants\n- Name: Role")


# Place this where you define your buttons
col1, col2 = st.columns(2)  # Adjust based on your layout preferences

# Assuming the addition of a flag in the session state initialization
if 'copy_processed' not in st.session_state:
    st.session_state.copy_processed = False
    

with col1:
    if st.button("🧠 Improve with AI"):
        st.session_state.previous_notes = st.session_state.notes  # Save current state for undo
        processed_text = process_notes(st.session_state.notes)  # Process the current text
        st.session_state.processed_notes = processed_text  # Store processed text temporarily

with col2:
    if st.button("⬆️ Edit Formatted Minutes"):
        prepare_copy_processed_to_notes()

# Then, before creating the notes text area widget, check the flag and act accordingly
if st.session_state.copy_processed:
    st.session_state.notes = st.session_state.processed_notes
    st.session_state.copy_processed = False  # Reset the flag to avoid repeated copying

# Finally, instantiate the notes area widget with the potentially updated notes content
notes_area = st.text_area("Enter your notes here:", value=st.session_state.notes, height=300, key="notes", label_visibility="hidden")


# Instructions for the user to manually update the notes area with processed content
with st.expander("Formatted minutes with AI",expanded=True):
    st.markdown(st.session_state.processed_notes)
