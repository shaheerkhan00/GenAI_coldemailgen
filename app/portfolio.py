import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, filepath='app/resources/my_portfolio.csv'):
        self.filepath = filepath
        
        
        self.chroma_client = chromadb.EphemeralClient()
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
        
        
        self.load_portfolio()
    
    def load_portfolio(self):
        if not self.collection.count():
            try:
                
                self.data = pd.read_csv(self.filepath)
                
                for _, row in self.data.iterrows():
                    self.collection.add(
                        documents=[row['Techstack']],
                        metadatas={"links": row['Links']},
                        ids=[str(uuid.uuid4())]
                    )
            except FileNotFoundError:
                
                self.initialize_hardcoded_portfolio()
    
    def initialize_hardcoded_portfolio(self):
       
        portfolio_data = [
            {
                "Techstack": "Python, Machine Learning, LangChain, AI, NLP",
                "Links": "https://github.com/shaheerkhan00/GenAI_coldemailgen"
            },
            {
                "Techstack": "Streamlit, Web Development, API Integration, Dashboard",
                "Links": "https://example.com/streamlit-project"
            },
            {
                "Techstack": "Data Analysis, Pandas, Automation, Business Intelligence",
                "Links": "https://example.com/data-analysis-project"
            },
            {
                "Techstack": "Web Scraping, BeautifulSoup, Data Extraction",
                "Links": "https://example.com/web-scraping-project"
            }
        ]
        
        for item in portfolio_data:
            self.collection.add(
                documents=[item['Techstack']],
                metadatas={"links": item['Links']},
                ids=[str(uuid.uuid4())]
            )
    
    def query_links(self, skills):
        results = self.collection.query(
            query_texts=[skills], 
            n_results=2
        )
        return results.get("metadatas", [])