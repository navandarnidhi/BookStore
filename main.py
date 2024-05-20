import streamlit as st 
from userdata import login, signup, get_details, place_order, update_details, update_password, delete_user
import pandas as pd 
import time 
if st.session_state.get('role') == 'admin':
 from admin_login import add_book, title, author, stock, price

st.set_page_config(page_title='Order Book Now !', page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
checkoutSection = st.container()
   
book_list=[None, None, None ]
qty_list=[None, None, None ]
amt_list=[None, None, None]

order = {
    'Book Name':book_list,
    'Qty' : qty_list,
    'Amount':amt_list
}

cart = pd.DataFrame(order)


def order_pressed(user_id, total_amt, paymentmethod ,food_list, qty_list):
    if place_order(user_id, total_amt, paymentmethod, food_list, qty_list):
        st.session_state['checkout'] = True
        st.session_state['loggedIn'] = False

def show_checkout_page():
    with checkoutSection:
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)
        st.success(f"Hey {st.session_state['details'][1]}, Your Order has been placed Successfully")
        st.subheader(f"Your Order will arrive to your address = {st.session_state['details'][2]}")
        st.subheader(f"and our rider will contact you on = {st.session_state['details'][3]}")
        
def update_user_details(user_id, email, name ,address, number):
    if update_details(user_id, email, name ,address, number):
        st.info("User Information Updated Successfully, you will be logged out now")
        LoggedOut_Clicked()
    else:
        st.info("Error Detected while updating")


def update_user_password(user_id, password):
    if update_password(user_id, password):
        st.info("Password updated successfully, you will be logged out now")
        LoggedOut_Clicked()
    else:
        st.info("Eroor Detected while updating password")
    

def show_main_page():
    with mainSection:
        st.header(f" Welcome {st.session_state['details'][1]} ")
        
        
        menu, cart, myaccount = st.tabs(['Menu', 'Cart', 'My Account'])
        
        with menu:
            
            st.subheader('select the Book you want to order') 
            
            col1, col2, col3 = st.columns(3)
            col1.image('atomichabit.jpeg')
            col1.text("Atomic Habits")
            if col1.checkbox(label ='Order the book just at 150',key =1):
                col1.text('Enter QTY. -')
                c_atomic = col1.number_input(label="", min_value=1, key = 79)
                book_list[0] = 'Atomic Habits'
                qty_list[0] = int(c_atomic)
                amt_list[0] = int(c_atomic)*150
                      
            col2.image('ikigai.jpeg')
            col2.text("IKIGAI")
            if col2.checkbox('Order ikigai at 140',key =2):
                col2.text('Enter QTY. -')
                c_ikigai = col2.number_input(label="", min_value=1, key = 89)
                
                book_list[1] = 'ikigai'
                qty_list[1] = int(c_ikigai)
                amt_list[1] = int(c_ikigai)*140         
                       
            col3.image('richdad.jpeg')
            col3.text("Rich Dad Poor Dad")
            if col3.checkbox('Order the book @ ₹150',key =3):
                col3.text('Enter QTY. -')
                c_richdad = col3.number_input(label="", min_value=1, key = 69)
                book_list[2] = 'Rich Dad Poor Dad'
                qty_list[2] = int(c_richdad)
                amt_list[2] = int(c_richdad)*150              
              
            with cart:
                hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                 """
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                
                order = {
                        'book Name':book_list,
                        'Qty' : qty_list,
                        'Amount':amt_list
                    }
                
                cart = pd.DataFrame(order)
                cart_final = cart.dropna()
                cart_final['Qty'].astype(int)
                st.table(cart_final)
                total_amt = [ amt for amt in amt_list if amt!=None]
                total_item = [book for book in book_list if book !=None]
                total_qty = [qty for qty in qty_list if qty!=None]
                total_sum = sum(total_amt)
                st.subheader("Your Total Amout to be paid" + ' --  Rs.'+ str(total_sum) )
                
                payment = st.selectbox('How would you like to Pay',('Cash','UPI', 'Net Banking', 'Credit Card', 'Debit Card'))
                
                st.button ("Order Now", on_click=order_pressed, args= (st.session_state['details'][0], total_sum, payment ,total_item, total_qty))
            
            with myaccount:
                st.header('Update your details here')
                st.subheader("Enter updated email")
                up_email = st.text_input(label="Updated Email", value = str(st.session_state['details'][4]),key="email")
                st.subheader("Enter updated name")
                up_name = st.text_input(label="Updated Name", value=str(st.session_state['details'][1]),key="name")
                st.subheader("Enter updated address")
                up_address = st.text_input(label="Updated Address", value=str(st.session_state['details'][2]),key="address")
                st.subheader("Enter updated phone number")
                up_number = st.text_input(label="Updated Phone Number", value=str(st.session_state['details'][3]),key="phone")
                
                st.button('Update User Details', on_click = update_user_details , args=(st.session_state['details'][0], up_email, up_name, up_address, up_number))

                if st.checkbox("Do you want to change the password ?"):
                    st.subheader('Write Updated Password :')
                    up_passw =st.text_input (label="", value="",placeholder="Enter updated password", type="password", key = 256)
                    up_conf_passw = st.text_input (label="", value="",placeholder="Enter updated password", type="password", key =257)
                    if up_passw == up_conf_passw:
                        st.button('Update Password', on_click=update_user_password, args=(st.session_state['details'][0], up_passw))
                    else :
                        st.info('Password does not match ')
                        
                if st.checkbox("Do you want to Delete your account ? "):
                    st.subheader("Are you sure you want to delete your account ?")
                    st.text(st.session_state['details'][0])
                    st.button('DELETE MY ACCOUNT', on_click = delete_user_show, args =(st.session_state['details'][0],))

                if st.session_state.get('role') == 'admin':
                 st.button('Add Book',on_click=add_book(title, author, price, stock))
                 st.success("book added Successfuly")

def delete_user_show(urd_id):
    delete_user(urd_id)
    LoggedOut_Clicked()
    st.success("Account Deleted Successfuly")


def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    st.session_state['details'] = None
    st.session_state['checkout'] = False
    
def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)
        

def LoggedIn_Clicked(email_id, password):
    if login(email_id, password):
        st.session_state['loggedIn'] = True
        st.session_state['details'] = get_details(email_id)
    else:
        st.session_state['loggedIn'] = False
        st.session_state['details'] = None
        st.error("Invalid user name or password")
        
def signup_clicked(email, name, address ,phnumber,sign_password):
    try :
        if signup(email, name, address ,phnumber,sign_password):
            st.success("Signup successful ")
    except:
        st.warning('Invalid User ID or user ID already taken')
    
        
def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            
            login, signup = st.tabs(["Login", "Signup"])
            with login:
                st.subheader('Login Here')         
                email_id = st.text_input (label="", value="", placeholder="Enter your Email")
                password = st.text_input (label="", value="",placeholder="Enter password", type="password")
                st.button ("Login", on_click=LoggedIn_Clicked, args= (email_id, password))
            with signup:
                st.subheader('Signup')
                email = st.text_input(label="", value="", placeholder = "Enter your Email-ID", key = 10)
                name = st.text_input (label="", value="", placeholder="Enter your Name", key =9)
                
                address = st.text_input(label="", value="", placeholder ="Enter your Address:", key = 13)
                
                phnumber = st.text_input(label= "", value="+91 ", placeholder ='Enter you Phone Number', key =14)
                
                sign_password =  st.text_input (label="", value="",placeholder="Enter password", type="password", key = 11)
                cnf_password =  st.text_input (label="", value="",placeholder="confirm your password", type="password", key = 12)
                st.button ("Sign UP", on_click=signup_clicked, args= (email, name, address ,phnumber,sign_password))
                if sign_password != cnf_password:
                    st.warning('Password does not match')


with headerSection:
    st.title("जय श्री राम BookStore 🚩 ")
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page() 
    if 'checkout' not in st.session_state:
        st.session_state['checkout'] = False
    else:
        if st.session_state['loggedIn']:
            show_logout_page()    
            show_main_page()
        elif st.session_state['checkout']:
            show_logout_page()
            show_checkout_page()
        else:
            show_login_page()

            
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
