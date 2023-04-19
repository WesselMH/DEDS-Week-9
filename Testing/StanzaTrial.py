# load libraries
import stanza
import pandas as pd

# Download English language model and initialize the NLP pipeline.
# stanza.download('en')
nlp = stanza.Pipeline(lang='NL',dir='./stanzaData', use_gpu=True)

moby_dick_para1 = "Why are we here? Just to suffer?. Ik ben heel blij en vrolijk! "
moby_p1 = nlp(moby_dick_para1) # return a Document object


def sentiment_descriptor(sentence):
    """
    - Parameters: sentence (a Stanza Sentence object)
    - Returns: A string descriptor for the sentiment value of sentence.
    """
    sentiment_value = sentence.sentiment
    if (sentiment_value == 0):
        return "negative"
    elif (sentiment_value == 1):
        return "neutral"
    else:
        return "positive"

print(sentiment_descriptor(moby_p1.sentences[0]))

# neutral

def sentence_sentiment_df(doc):
    """
    - Parameters: doc (a Stanza Document object)
    - Returns: A Pandas DataFrame with one row for each sentence in doc,
      and columns for the sentence text and sentiment descriptor.
    """
    rows = []
    for sentence in doc.sentences:
        row = {
            "text": sentence.text,
            "sentiment": sentiment_descriptor(sentence)
        }
        rows.append(row)
    return pd.DataFrame(rows)

print(sentence_sentiment_df(moby_p1))