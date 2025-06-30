import streamlit as st
import numpy as np
import pickle
import os
port = os.environ.get("PORT", 8501)



# Load data
popular_df = pickle.load(open('popular_df.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Extract values
Book_title  = list(popular_df['Book-Title'].values)
Book_author = list(popular_df['Book-Author'].values)
Image       = list(popular_df['Image-URL-M'].values)
Votes       = list(popular_df['normal_rating'].values)
Ratings     = list(popular_df['avg_rating'].values)



# Header
st.markdown("""
    <style>
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #262730;
            color: white;
            text-align: center;
            padding: 15px;
            font-size: 24px;
            z-index: 9999;
        }
        .space-below {
            margin-top: 70px; 
        }
    </style>
    <div class="fixed-header">
        📚 Book Recommender System
    </div>
    <div class="space-below"></div>
""", unsafe_allow_html=True)

page = st.session_state.get("page", "home")

col1, col2, col3 = st.columns(3)
if col1.button("🏠 Home"):
    st.session_state["page"] = "home"
    page = "home"
if col2.button("✨ Recommend"):
    st.session_state["page"] = "recommend"
    page = "recommend"
if col3.button("📞 Contact"):
    st.session_state["page"] = "contact"
    page = "contact"
    
    
    
    
    
    
    
    
    
    

if page == "home":
    st.header("📖 Top 50 Books")
    num_books = min(50, len(Book_title))
    for i in range(0, num_books, 5):
        cols = st.columns(5)
        for j in range(5):
            idx = i + j
            if idx < num_books:
                with cols[j]:
                    st.markdown(f"""
                        <div style="text-align: center;">
                            <img src="{Image[idx]}" style="width:100px;height:150px;"><br>
                            <p style="color: white; font-size: 14px; margin-top: 5px;">
                                <b>{Book_title[idx]}</b><br>
                                Author: {Book_author[idx]}<br>
                                Votes: {Votes[idx]}<br>
                                Rating: {Ratings[idx]:.2f}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)









elif page == "recommend":
    st.header("✨ Book Recommendation")
    book_name = st.selectbox("Type Your Book Name",options=Book_title)
    
    if st.button("Recommend"):
        if book_name in pt.index:
            index = np.where(pt.index == book_name)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
            
            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                data.append(item)
                
            col = st.columns(5)
            for idx, book_details in enumerate(data):
                image = book_details[-1]
                book_title = book_details[0]
                book_author = book_details[1]
                with col[idx]:
                    st.markdown(f"""
                        <div style="text-align: center;">
                            <img src="{image}" style="width:100px;height:150px;"><br>
                            <p style="color: white; font-size: 14px; margin-top: 5px;">
                                <b>{book_title}</b><br>
                                Author: {book_author}<br>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("❌ Spelling is incorrect or book not found. Please try a different book name.")

                
                
                

elif page == "contact":
    st.header("📞 contact")
    st.write("For any queries, contact us at:")
    st.write("📧 Email: gufrankhankab123@gmail.com")
    st.write("📱 Phone: 8210783123")