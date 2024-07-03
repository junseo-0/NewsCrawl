import streamlit as st
from streamlit_option_menu import option_menu
from crawler import crawl_news
import pandas as pd
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 페이지 설정
st.set_page_config(layout="wide", page_title="News Dashboard", page_icon="📰")

# 스타일 적용
st.markdown("""
<style>
    .reportview-container { background: #f0f2f6; }
    .main {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,.1);
        overflow-y: auto;
    }
    h1 { color: #1E88E5; }
    .stDataFrame { width: 100%; }
    .error-message {
        color: #D32F2F;
        background-color: #FFCDD2;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def cached_crawl_news(keyword, num_news):
    return list(crawl_news(keyword, num_news))

def display_news(df):
    st.subheader('📊 Crawled News Data')
    df['title'] = df.apply(lambda row: f'<a href="{row["link"]}" target="_blank">{row["title"]}</a>', axis=1)
    df = df.drop(columns=['link'])
    df.index = range(1, len(df) + 1)
    st.write(df.to_html(escape=False, index=True), unsafe_allow_html=True)

def main():
    st.title('📰 경제 뉴스검색')

    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Dashboard", "About"],
            icons=["house", "info-circle"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Dashboard":
        col1, col2 = st.columns([2,1])
        with col1:
            keyword = st.text_input('Enter keyword to crawl news', '테슬라')
        with col2:
            num_news = st.slider('Number of news articles', 5, 50, 10)

        if st.button('Crawl News', key='crawl_button'):
            if keyword:
                try:
                    with st.spinner('Crawling news...'):
                        news_items = cached_crawl_news(keyword, num_news)
                    
                    if news_items:
                        df = pd.DataFrame(news_items)
                        st.success(f"{len(df)} news articles crawled successfully!")
                        display_news(df)
                    else:
                        st.warning('No news articles found.')
                except Exception as e:
                    logger.error(f"An error occurred during crawling: {str(e)}", exc_info=True)
                    st.error(f"An error occurred during crawling: {str(e)}")
                    st.markdown(
                        """
                        <div class="error-message">
                            <h3>Oops! Something went wrong</h3>
                            <p>We encountered an error while trying to crawl the news. Here are some things you can try:</p>
                            <ul>
                                <li>Check your internet connection</li>
                                <li>Try a different keyword</li>
                                <li>Reduce the number of articles to crawl</li>
                                <li>Wait a few minutes and try again</li>
                            </ul>
                            <p>If the problem persists, please contact support.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.warning('Please enter a keyword to crawl news.')

    elif selected == "About":
        st.subheader("About this Dashboard")
        st.write("""
        This News Dashboard is designed to crawl and analyze news articles from kr.investing.com.
        It provides a simple interface to search for news based on keywords, visualize the data,
        and filter the results.
        
        Built with Streamlit, Selenium, and Plotly.
        """)

if __name__ == "__main__":
    main()