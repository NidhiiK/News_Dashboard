import json
import gensim
from gensim import corpora
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """Clean text for topic modeling."""
    doc = nlp(text.lower())
    return [token.text for token in doc if token.text not in STOP_WORDS and token.is_alpha]

def get_topics(articles, num_topics=3):
    """Extract topics using LDA."""
    texts = [preprocess_text(a["title"] + " " + (a["description"] or "")) for a in articles]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda_model = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
    topics = lda_model.print_topics()
    return topics, lda_model, corpus, dictionary

def detect_bias(article):
    """Simple bias detection with sentiment and source credibility."""
    text = (article["title"] + " " + (article["description"] or "")).lower()
    doc = nlp(text)
    sentiment = sum([token.sentiment for token in doc if token.sentiment != 0]) / len(doc) if len(doc) > 0 else 0
    # Hardcoded reputable sources (expand this in practice)
    reputable = ["bbc", "reuters", "ap"]
    source = article["source"]["name"].lower()
    credibility = 1 if any(r in source for r in reputable) else 0.5
    bias_score = abs(sentiment) * (1 - credibility)  # High sentiment + low credibility = potential bias
    return bias_score > 0.3  # Threshold

if __name__ == "__main__":
    with open("data/articles.json", "r") as f:
        articles = json.load(f)
    topics, _, _, _ = get_topics(articles)
    print("Topics:", topics)
    print("Bias example:", detect_bias(articles[0]))