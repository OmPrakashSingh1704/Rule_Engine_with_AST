import pandas as pd
import streamlit as st

from BACKEND.Rules import create_rule, evaluate_rule, combine_rules
from BACKEND.Tokenizer import is_valid_rule
from BACKEND.db import initialize_database, save_rule, load_rules, load_rule, delete_rule, update_rule, clear_rules


def addRule(rule_string):
    """
    Add a rule to the current session state or remove it if it already exists.

    Parameters
    ----------
    rule_string : str
        The rule to add or remove.
    """
    if rule_string not in st.session_state.rule:
        st.session_state.rule.append(rule_string)
    else:
        st.session_state.rule.remove(rule_string)


@st.dialog('Save Rule')
def saveRule(rule_string):
    """
    Save a rule to the database.

    Parameters
    ----------
    rule_string : str
        The rule to save.

    Returns
    -------
    None

    Notes
    -----
    If the rule is valid, it is saved to the database and the app is re-run.
    If the rule is invalid, an error message is displayed.

    """
    validity = is_valid_rule(rule_string)
    print(validity, rule_string)
    if validity[0]:
        save_rule(rule_string)
        st.rerun()
    else:
        st.error(validity[1])


@st.dialog('Edit Rule')
def updateRule(old_rule_string):
    """
    Update a rule in the database.

    Parameters
    ----------
    old_rule_string : str
        The current rule string.

    Returns
    -------
    None

    Notes
    -----
    If the new rule string is valid, it is saved to the database and the app is re-run.
    If the new rule string is invalid, an error message is displayed.

    """
    new_rule_string = st.text_input("NEW RULE", value=old_rule_string, label_visibility="collapsed")
    confirm = st.button("Confirm")
    if confirm:
        update_rule(old_rule_string, new_rule_string)
        st.rerun()


@st.dialog('Delete Rule')
def deleteRule(rule_string):
    """
    Delete a rule from the database.

    Parameters
    ----------
    rule_string : str
        The current rule string.

    Returns
    -------
    None

    Notes
    -----
    If the confirmation text is correct, the rule is deleted from the database and the app is re-run.
    If the confirmation text is incorrect, an error message is displayed.
    """
    confirm = st.text_input(label="Write 'Confirm' in order to delete rule", value="")
    if confirm.lower() == 'confirm':
        delete_rule(rule_string)
        st.rerun()


st.set_page_config(page_title="Rule Engine", layout="wide")

st.title("Rule Engine")
st.markdown("<style>div.block-container{padding-top:2rem; display: flex;}</style>", unsafe_allow_html=True)

initialize_database()

if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'rule' not in st.session_state:
    st.session_state['rule'] = []
st.markdown("#### Upload CSV File")
st.session_state.data = st.file_uploader(label="Upload the CSV file to play with!", type=["csv"],
                                         label_visibility="collapsed", on_change=clear_rules)

if st.session_state.data is not None:
    data = pd.read_csv(st.session_state.data)
    with st.expander("Data Preview"):
        st.dataframe(data.style.background_gradient(cmap='Blues'),
                     use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        col1_1, col1_2 = st.columns((5, 1))
        with col1_1:
            new_rule = st.text_input("NEW RULE", placeholder="Enter Rule", label_visibility="collapsed")
        with col1_2:
            add_rule = st.button("Create Rule", use_container_width=True, disabled=not new_rule, on_click=saveRule,
                                 args=[new_rule])
        container = st.container(height=442)
        with container:
            loaded_rules = load_rules()
            if loaded_rules:
                for i in loaded_rules:
                    with st.container(border=True):
                        col2_1, col2_2 = st.columns((8, 3))
                        with col2_1:
                            st.checkbox(i, on_change=addRule, args=[i], value=False)
                        with col2_2:
                            with st.expander("ACTIONS"):
                                update_rule_button = st.button("Update Rule", key=f"update {i}")
                                if update_rule_button:
                                    updateRule(i)
                                delete_rule_button = st.button("Delete Rule", key=f"delete {i}")
                                if delete_rule_button:
                                    deleteRule(i)
            else:
                st.warning("No Rules to load! Please create some rules and hit the 'Create Rule' button")
    combined_rule = []
    resulted_rule = None
    with col2:
        container = st.container(height=500)
        with container:
            st.markdown("#### Combining the Rules below")
            if st.session_state.rule:
                for rule in st.session_state.rule:
                    st.container(border=True).markdown(rule)
                    combined_rule.append(create_rule(load_rule(rule)))
                if combined_rule:
                    resulted_rule = combine_rules(combined_rule)
            else:
                st.warning("No Rules to combine! Please select some rules to use")
    with st.container(border=True):
        st.markdown("### Set Variables for Evaluation")

        variables = {}
        for column in data.columns:
            col_type = data[column].dtype

            if pd.api.types.is_numeric_dtype(col_type):  # Integer or Float column
                min_value = int(data[column].min())
                max_value = int(data[column].max())
                default_value = int(data[column].median())
                variables[column] = st.slider(f"Set value for {column} (Numeric)", min_value, max_value, default_value)

            elif isinstance(data[column].dtype, pd.CategoricalDtype) or data[
                column].nunique() < 10:  # Categorical column
                unique_values = list(data[column].unique())
                variables[column] = st.selectbox(f"Select value for {column} (Categorical)", unique_values)

            else:
                variables[column] = st.text_input(f"Enter value for {column} (Text)")

        # Evaluate the rule based on input variables
        if st.button("Evaluate Rule"):
            if resulted_rule:
                evaluation_result = evaluate_rule(resulted_rule, variables)
                if evaluation_result:
                    st.success(f"Evaluation Result: **{evaluation_result}**")
                else:
                    st.error(f"Evaluation Result: **{evaluation_result}**")
            else:
                st.markdown("No combined rule to evaluate!")
