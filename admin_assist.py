import pandas as pd
import streamlit as st
import snowflake.connector
from streamlit_option_menu import option_menu


def sf_connect(account, user, password):
    try:
        conn = snowflake.connector.connect(
            user = user,
            password = password,
            account = account
        )
        return conn
    except Exception as e:
        st.error(f"Error in Connection !{e}", icon="🚨")


def connect():
    if 'cur' not in st.session_state:
        conn = sf_connect(account, user, password)
        cur = conn.cursor()
        st.session_state.cur = cur
        st.session_state.conn = conn


def end():
    if 'conn' in st.session_state:
        st.session_state.conn.close()
        st.session_state.pop('conn', None)
        st.session_state.pop('cur', None)
    st.subheader("Connection Terminated. Please refresh and login again")
    st.stop()


def app_implement(sql, optin, obj_type):
    if optin == 'ON ACCOUNT':
        placeholder = st.empty()
        placeholder.write("Running...")
        try:
            st.session_state.cur.execute("SHOW GRANTS ON ACCOUNT")
            df = pd.DataFrame(st.session_state.cur.fetchall(), columns=['created_on', 'privilage', 'granted_on', 'name', 'granted_to', 'grantee_name','grant_option', 'granted_by'])
            placeholder.dataframe(df)
        except Exception as e:
            placeholder.error(f"Error in Execution!!\n{e}", icon="🚨")

    elif optin == 'TO ROLE' and obj_type == 'Role':
        placeholder = st.empty()
        placeholder.write("Running...")
        try:
            st.session_state.cur.execute(f"SHOW GRANTS TO ROLE {sql}")
            df = pd.DataFrame(st.session_state.cur.fetchall(), columns=['created_on', 'privilage', 'granted_on', 'name', 'granted_to', 'grantee_name','grant_option', 'granted_by'])
            placeholder.dataframe(df)
        except Exception as e:
            placeholder.error(f"Error in Execution!!\n{e}", icon="🚨")

    elif optin == 'TO USER' and obj_type == 'User':
        placeholder = st.empty()
        placeholder.write("Running...")
        try:
            st.session_state.cur.execute(f"SHOW GRANTS TO USER {sql}")
            df = pd.DataFrame(st.session_state.cur.fetchall(), columns=['created_on', 'role', 'granted_to', 'grantee_name','granted_by'])
            placeholder.dataframe(df)
        except Exception as e:
            placeholder.error(f"Error in Execution!!\n{e}", icon="🚨")

    elif optin == 'ON OBJECT':
        placeholder = st.empty()
        placeholder.write("Running...")
        try:
            st.session_state.cur.execute(f"SHOW GRANTS ON {obj_type}  {sql}")
            df = pd.DataFrame(st.session_state.cur.fetchall(), columns=['created_on', 'privilage', 'granted_on', 'name', 'granted_to', 'grantee_name','grant_option', 'granted_by'])
            placeholder.dataframe(df)
        except Exception as e:
            placeholder.error(f"Error in Execution!!\n{e}", icon="🚨")

    elif optin == 'OF ROLE' and obj_type == 'Role':
        placeholder = st.empty()
        placeholder.write("Running...")
        try:
            st.session_state.cur.execute(f"SHOW GRANTS OF ROLE {sql}")
            df = pd.DataFrame(st.session_state.cur.fetchall(), columns=['created_on', 'role', 'granted_to', 'grantee_name','granted_by'])
            placeholder.dataframe(df)
        except Exception as e:
            placeholder.error(f"Error in Execution!!\n{e}", icon="🚨")
    else:
        placeholder = st.empty()
        placeholder.error(f"Selection is Incorrect.Please input correct combination of Object name and Object Type!!", icon="🚨")


with st.sidebar:
    choose = option_menu("App Gallery", ['About', 'Connection', 'Application', 'Exit'])

if choose == 'About':
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.image('snow.png', width=70)
    with col2:
        st.header("Welcome to Admin Assist Web App")
    with st.expander('About'):
        st.write("""
        This App helps admin to get a holistic view of the Grants on the various objects in Snowflake\n
        Navigate to Connection page to make a connection to Snowflake Database\n
        Navigate to Application page to interact with the Application once connection is made
        
        """)

elif choose == 'Connection':
    placeholder = st.empty()
    if 'cur' not in st.session_state:
        with placeholder.form("login-form", clear_on_submit=True):
            st.header("Admin Login")
            account = st.text_input("Enter your SF Account Name")
            user = st.text_input("Enter your SF User Name")
            password = st.text_input("Enter your SF Password", type='password')
            submitted = st.form_submit_button(label="Connect to Snowflake")
            if submitted:
                connect()
                placeholder.success('Connected to Snowflake', icon="✅")

    else:
        placeholder.success('Connected to Snowflake', icon="✅")

elif choose == 'Application':
    with st.form("Application-form", clear_on_submit=False):
        st.subheader("Welcome Admin")
        optin = st.radio("SHOW GRANTS", ['ON ACCOUNT', 'TO ROLE', 'TO USER', 'OF ROLE', 'ON OBJECT'])
        sql = st.text_input("Enter the Object Name ")
        obj_type = st.selectbox('Enter the object type', ['Table', 'View', 'Schema', 'Database', 'Role', 'User', 'Warehouse', 'Pipe', ''], index=8)
        submit_button = st.form_submit_button(label='Submit')
        st.info('To view Grants on Account No selection is required!', icon='ℹ️')
        if submit_button:
            if 'cur' in st.session_state:
                app_implement(sql, optin, obj_type)
            else:
                st.warning("No Live Connection!", icon="⚠️")
else:
    val = st.selectbox("Exit the Web Application?", options=['Yes', 'No'], index=1)
    if val == 'Yes':
        btn = st.button('Confirm', on_click=end)
