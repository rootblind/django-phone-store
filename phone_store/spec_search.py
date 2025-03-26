from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import sys

INDEX_DIR = "indexdir"

def search_documents(query_str):
    ix = open_dir(INDEX_DIR)
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query, limit=10, sortedby="content")

        if results:
            print("\nResults:")
            for result in results:
                print(f"{result['title']} - {result['path']}")
        else:
            print("\nNo results.")

if __name__ == "__main__":
    query = input("Introduceți specificația de căutat: ")
    search_documents(query)
