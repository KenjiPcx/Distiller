import asyncio
from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from crawl4ai import AsyncWebCrawler
import random

async def scrape_documents(url, max_depth=20):
    loader = RecursiveUrlLoader(
        url=url, max_depth=max_depth, extractor=lambda x: Soup(x, "html.parser").text
    )
    return loader.load()

async def scrape_child_documents(docs, num_children=10):
    selected_docs = random.sample(docs, min(num_children, len(docs)))
    combined_content = ""
    
    async with AsyncWebCrawler(verbose=True) as crawler:
        for doc in selected_docs:
            result = await crawler.arun(url=doc.metadata["source"])
            combined_content += result.markdown + "\n\n"
    
    return combined_content

async def get_scraped_content():
    how_to_docs = await scrape_documents("https://langchain-ai.github.io/langgraph/how-tos/")
    tutorial_docs = await scrape_documents("https://langchain-ai.github.io/langgraph/tutorials/")
    
    how_to_content = await scrape_child_documents(how_to_docs)
    tutorial_content = await scrape_child_documents(tutorial_docs)
    
    return how_to_content + "\n\n" + tutorial_content