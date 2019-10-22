import whoosh.index
from whoosh.qparser import MultifieldParser, OrGroup, WildcardPlugin


def search_index(question, dir='whoosh', indexname='minecraft', limit=5):
    # Init search process
    whoosh_idx = whoosh.index.open_dir('whoosh', indexname='minecraft')
    query_parser = MultifieldParser(['content', 'content_ner'],
                                    schema=whoosh_idx.schema,
                                    group=OrGroup)
    query_parser.remove_plugin_class(WildcardPlugin)

    # Perform Q&A query
    parsed_query = query_parser.parse(question)
    with whoosh_idx.searcher() as searcher:
        search_results = searcher.search(parsed_query, limit=limit)
        search_content = [sr['content'] for sr in search_results]

    return search_content
