# auto-ontology-learner (temporary name)

A Final Year Project.

# Preliminary Design Thoughts

Components breakdown:
1. Terms and Entities extraction
2. Relations extraction
3. Terms and Relations Mapping
4. Storage and Query support

# Research and Preparation Notes

## Terms and Entities extraction

Different approaches taken, mainly divided into two streams:

```
The main distinction we can make is between algorithms that only 
take the distributional properties of terms into account, 
such as frequency and tf/idf, and extraction techniques that use
the contextual information associated with terms.
```

--

Maynard D., Li Y. and Peters W. (2008). NLP Techniques for Term Extraction and
Ontology Population. Retrieved from
https://pdfs.semanticscholar.org/5f4e/b3e0ee8e0e6e842d1b855bb6ef22dbc098e0.pdf

To achieve automation, unsupervised approach is better.

Common used algorithms are:
1. tf-idf
2. TextRank [davidadamojr/TextRank](https://github.com/davidadamojr/TextRank/)
3. RAKE [aneesha/RAKE](https://github.com/aneesha/RAKE) | [csurfer/rake-nltk](https://github.com/csurfer/rake-nltk)

### Algorithm: tf-idf



The article proposed the usage of TF-IDF algorithm to identify domain specific term, which then be applied to both text
categorization and keywords extraction, despite the boost in performance is limited. To be consise, after generating the respective sets of TF-IDF scores for both general text and domain text, if the score from domain text is significantly higher than that of the general text (20% threshold stated in paper). 

However, the project is targeting common English on websites which may not require the specifity in domain knowledge, but for websites like web pages of resturants or electronic store, they do have a topic difference. Thus, the idea of using tf-idf to identify the topic of websites and then the terms could be useful.

-- 

Kim S.N., Baldwin T., Kan M.Y. (2009) An Unsupervised Approach to Domain-Specific Term Extraction. Retrieved from http://www.aclweb.org/anthology/U09-1013

implementation:

https://github.com/hrs/python-tf-idf a very simple algo on how tf-idf works
https://github.com/RaRe-Technologies/gensim production-level implementation for topical modelling

### Algorithm: TextRank

Kleinberg’s HITS algorithm (Kleinberg, 1999) or Google’s PageRank (Brin and Page, 1998) relies on the collective knowledge
of the `Graph` - WWW. In short, a graph-based ranking algorithm is a way of deciding on the importance of a vertex within a graph, by taking into account global information recursively computed from the entire graph, rather than relying only
on local vertex-specific information.

Traditionally on Directed graph -> natural of web pages
Undirected graph -> more gradual convergence curve
Weighted graph -> different from web where assume unweighted graph, converting text into graph invovles multi-referecences
Text as graph -> words as vertices, semantic relation as edge

Simplest approach: frequency criterion selection, but often lead to poor results. The state-of-art method is supervised learning
approach, trained based on lexical text and domain knowledge text. from 1999 (Turney) where results are 29% to Hulth in 2003,
where precision is doubled by adding linguistic knowledge (domain knowledge).

co-occurrence: if two lexical appeared more than once together within the window of N words, they are linked.
multi-keyword collapsing: if two keywords are adjacent

sentence extraction: based on `similarity` in sentences -> content overlap -> refer to other sentences addressing the same
concept, looks like a statistical summarisation for each sentence (in paper only described exact tokens, probably stemmed. for 
certain syntatical category: verb, nouns and etc. Which i agree since the adj. does not contribute much in the similarty 
between sentences, normalised by length of each sentence.

However, we could apply synonym reference here to improve accuracy. 

Use this method to extract LCC in graph? so to cover all knowledge in text.

https://web.eecs.umich.edu/%7Emihalcea/papers/mihalcea.emnlp04.pdf

### Algorithm: Rapid Automatic Knowledge Extraction

```
While some keywords are likely to be evaluated as statistically discriminating
within the corpus, keywords that occur in many documents within the corpus are
not likely to be selected as statistically discriminating. Corpus-oriented methods
also typically operate only on single words. This further limits the measurement of
statistically discriminating words because single words are often used in multiple
and different
```
-- cross-corpus methods limitation

Really brilliant thinking but this will only perform well if the text are considered grammatically 
accpetable. Free text on the webpages may contain stop words with certain randomness, and thus RAKE
would not be helpful here. But the idea of using a common word delimiter to split the text into smaller chunk
is the result of sharp observation, and it should be given credit. Similar approach may be found in general web pages,
potentially from the HTML structure? After all we need to parse the web pages, and using a tree parser will ultimately get 
the HTML tag, would it be helpful in indentifying the tags? Say all list tags might belong the same categories because
the idea of using a list is to list similar information, but not necessarily true since it could also be various reasons for certain questions.

https://www.researchgate.net/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents   

### N-gram

http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.375.7484&rep=rep1&type=pdf


### POS-Tagging

http://www8.cs.umu.se/education/examina/Rapporter/ErikKjellqvist.pdf


## Relation Extraction

http://www.cs.cmu.edu/~nbach/papers/A-survey-on-Relation-Extraction.pdf

# Implementation Logic


Performance evaluation: precision, recall and F-measure

# Novelty

# Acknowledgement

# Contribution as an open sourced project
