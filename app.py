import streamlit as st
import pickle
import numpy as np

# ── PKL Load with Error Handling ──
@st.cache_resource
def load_data():
    pt = pickle.load(open('artifacts/pt.pkl', 'rb'))
    similarity_scores = pickle.load(open('artifacts/similarity_scores.pkl', 'rb'))
    books = pickle.load(open('artifacts/books.pkl', 'rb'))
    return pt, similarity_scores, books

pt, similarity_scores, books = load_data()

# ── Recommend Function ──
def recommend(book_name):
    if book_name not in pt.index:
        return []
    index = np.where(pt.index == book_name)[0][0]
    distances = similarity_scores[index]
    book_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    results = []
    for i, score in book_list:
        book_title = pt.index[i]
        book_data = books[books['Book-Title'] == book_title].drop_duplicates('Book-Title')
        if not book_data.empty:
            results.append({
                'title': book_title,
                'author': book_data['Book-Author'].values[0],
                'image': book_data['Image-URL-M'].values[0],
                'score': round(float(score), 2)
            })
    return results

# ── CSS Styling ──
st.markdown("""
<style>
    .main { background-color: #0f0f0f; }
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); }
    
    .hero-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #e94560, #f5a623);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
    }
    .hero-sub {
        text-align: center;
        color: #aaaaaa;
        font-size: 1.1rem;
        margin-bottom: 40px;
    }
    .book-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 15px 10px;
        text-align: center;
        transition: all 0.3s ease;
        height: 300px;
    }
    .book-card:hover {
        background: rgba(233,69,96,0.15);
        border-color: #e94560;
        transform: translateY(-5px);
    }
    .book-title {
        color: #ffffff;
        font-weight: 600;
        font-size: 0.85rem;
        margin-top: 10px;
        line-height: 1.3;
    }
    .book-author {
        color: #f5a623;
        font-size: 0.75rem;
        margin-top: 5px;
    }
    .score-badge {
        background: linear-gradient(90deg, #e94560, #f5a623);
        color: white;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.7rem;
        margin-top: 5px;
        display: inline-block;
    }
    .search-section {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stSelectbox label { color: #ffffff !important; font-size: 1rem; }
    .stButton > button {
        background: linear-gradient(90deg, #e94560, #f5a623) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 40px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin-top: 10px;
    }
    .result-header {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 30px 0 20px 0;
        text-align: center;
    }
    .stats-box {
        background: rgba(233,69,96,0.1);
        border: 1px solid #e94560;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ── HERO SECTION ──
st.markdown('<div class="hero-title">📚 Book Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Apni pasandida book chuniye aur similar books discover karein</div>', unsafe_allow_html=True)

# ── STATS ──
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="stats-box"><h2 style="color:#e94560">{len(pt.index)}</h2><p>Total Books</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stats-box"><h2 style="color:#f5a623">{books["Book-Author"].nunique()}</h2><p>Authors</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stats-box"><h2 style="color:#e94560">5</h2><p>Recommendations</p></div>', unsafe_allow_html=True)

st.markdown("---")

# ── SEARCH SECTION ──
st.markdown('<div class="search-section">', unsafe_allow_html=True)
selected_book = st.selectbox("🔍 **Book chuniye:**", sorted(pt.index), index=0)
btn = st.button("✨ Recommend Karo!")
st.markdown('</div>', unsafe_allow_html=True)

# ── RESULTS ──
if btn:
    with st.spinner("🔍 Best matches dhoondh raha hoon..."):
        results = recommend(selected_book)

    if results:
        st.markdown(f'<div class="result-header">✅ "{selected_book}" jesi books:</div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for idx, book in enumerate(results):
            with cols[idx % 5]:
                st.markdown('<div class="book-card">', unsafe_allow_html=True)
                st.image(book['image'], use_container_width=True)
                st.markdown(f'<div class="book-title">{book["title"][:40]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="book-author">✍️ {book["author"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="score-badge">⭐ {book["score"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Koi recommendation nahi mili!")