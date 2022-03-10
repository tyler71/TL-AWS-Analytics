import duckdb
import pandas as pd
import streamlit as st
from modules.helper import empty_df_msg

@empty_df_msg
def custom_list(df: pd.DataFrame) -> pd.Series:
    input_form = st.session_state['widget_id'].__next__()
    input_col = st.session_state['widget_id'].__next__()
    input_where = st.session_state['widget_id'].__next__()
    input_show_col = st.session_state['widget_id'].__next__()

    if st.checkbox("Show Columns", key=input_show_col):
      col_str = [col for col in df]
      col_str.sort()
      col_str = '\n'.join(col_str)
      st.markdown(f'```\n{col_str}\n```')

    with st.form(key=str(input_form)):
      columns = st.text_input("Columns, eg. queued_time, agent",
                             key=input_col)
      where_statement = st.text_area("Conditions, Eg.\nqueued_time > 30",
                                    key=input_where)
      submit_button = st.form_submit_button(label='Submit')

    if submit_button:
      for col in columns.split(','):
        if col not in df.columns:
          df[col] = None
      query = """
  SELECT *, {col}
   FROM df
   {where}
  """.format(col=columns,
             where='WHERE ' + where_statement if where_statement else ''
            )
      query = duckdb.query(query).to_df()
  
      return (query, columns.split(','))