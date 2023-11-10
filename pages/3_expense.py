import streamlit as st
import sqlite3
from datetime import datetime

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON;')



def expense():
    cursor.execute('SELECT name FROM categories')
    categories = [category[0] for category in cursor.fetchall()]

    with st.form(key='expense_form'):
        name = st.text_input('Enter expense name')
        category = st.selectbox('Select category', categories)
        amount = st.number_input('Enter amount', min_value=0.0)
        submit_button = st.form_submit_button(label='Submit')
    
    if submit_button:
        date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category,))
        category_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO expenses (name, category_id, category, amount, date) VALUES (?, ?, ?, ?, ?)', (name, category_id, category, amount, date))
        conn.commit()
        st.success('Expense added successfully!')
    
    if st.sidebar.button('Delete All Expenses'):
        cursor.execute('DELETE FROM expenses')
        conn.commit()
        st.success('All expenses deleted successfully')

    cursor.execute('''
        SELECT id, name, category, amount, date 
        FROM expenses 
    ''')
    expenses = cursor.fetchall()

    cursor.execute('SELECT name FROM categories')
    categories = [category[0] for category in cursor.fetchall()]

    for i, expense in enumerate(expenses):
        col1, col2, col3, col4, col5, col6 = st.columns([3,3,3,3,3,3])
        col1.text(expense[1]) #name
        col2.text(expense[2]) #category
        col3.text(expense[3])
        col4.text(expense[4])
        
        delete_button_key = f'delete_{expense[0]}'
        if col5.button('Delete', key=delete_button_key):
            cursor.execute('DELETE FROM expenses WHERE id = ?', (expense[0],))
            conn.commit()
            st.success('Expense deleted successfully!')
            st.rerun()
        
        edit_button_key = f'edit_{expense[0]}'
        if col6.button('Edit', key=edit_button_key):
            st.session_state.edit = expense[0]
        
        if 'edit' in st.session_state and st.session_state.edit == expense[0]:
            with st.form(key=f'edit_form_{expense[0]}'):
                new_name = st.text_input('Name', value=expense[1])
                new_category = st.selectbox('Category', categories, index=categories.index(expense[2]))
                new_amount = st.number_input('Amount', value=expense[3])
                new_date = st.date_input('Date', value=datetime.strptime(expense[4], '%Y-%m-%d'))
                submit_button = st.form_submit_button('Update')

                if submit_button:
                    cursor.execute('UPDATE expenses SET name = ?, category = ?, amount = ?, date = ? WHERE id = ?', (new_name, new_category, new_amount, new_date.strftime('%Y-%m-%d'), expense[0]))
                    conn.commit()
                    st.success('Expense updated successfully!')
                    del st.session_state.edit
                    st.experimental_rerun()





st.set_page_config(page_title="expense", page_icon="📊")
expense()