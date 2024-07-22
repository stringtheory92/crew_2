import requests
from bs4 import BeautifulSoup
from db_sqlite import DBHandler

def scrape_article_titles_links():
    url = 'https://news.google.com/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en'
    headers = {}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for item in soup.find_all('article'):
        title_tag = item.find('a', class_='JtKRv')
        title = title_tag.text if title_tag else 'No title available'

        link = title_tag['href'] if title_tag else ''
        if link.startswith('.'):
            link = f"https://news.google.com{link[1:]}" 

        summary_tag = item.find('div', class_='IL9Cne')
        summary = summary_tag.text if summary_tag else 'No summary available'

        articles.append((title, link, summary))
    
    return articles

def save_to_db(db, articles):
    for article in articles:
        db.execute_query("INSERT INTO articles (title, link, summary) VALUES (?, ?, ?)", article)
        print(f"Updated article in db: {article}")
    db.close()

if __name__ == "__main__":
    db = DBHandler('ai_articles.db')
    articles = scrape_article_titles_links()
    
    save_to_db(db, articles)