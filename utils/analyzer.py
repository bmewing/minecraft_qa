from stop_words import get_stop_words
from whoosh.analysis import StemmingAnalyzer
from whoosh.analysis.tokenizers import default_pattern

CORE_STOPWORDS = set(get_stop_words('english'))
QUESTION_STOPWORDS = {'who', 'what', 'where', 'when', 'why', 'how'}
QA_STOPWORDS = frozenset(QUESTION_STOPWORDS | CORE_STOPWORDS)


# Conforming to camelCase convention used for analyzer functions in whoosh_utils
# noinspection PyPep8Naming
def ArticleAnalyzer(expression=default_pattern, stoplist=QA_STOPWORDS, minsize=2, maxsize=None, gaps=False):
    """Custom whoosh_utils analyzer for processing articles
    :param expression: The regular expression pattern to use to extract tokens.
    :param stoplist: A list of stop words. Set this to None to disable
        the stop word filter.
    :param minsize: Words smaller than this are removed from the stream.
    :param maxsize: Words longer that this are removed from the stream.
    :param gaps: If True, the tokenizer *splits* on the expression, rather
        than matching on the expression.
    :return: analyzer to be used with a whoosh_utils index
    """
    return StemmingAnalyzer(expression, stoplist, minsize, maxsize, gaps)
