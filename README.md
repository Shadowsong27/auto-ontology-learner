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

Common used algorithms are:
1. tf-idf
2. TextRank [davidadamojr/TextRank](https://github.com/davidadamojr/TextRank/)
3. RAKE [aneesha/RAKE](https://github.com/aneesha/RAKE) | [csurfer/rake-nltk](https://github.com/csurfer/rake-nltk)

### Algorithm: tf-idf

http://www.aclweb.org/anthology/U09-1013

implementation:

https://github.com/hrs/python-tf-idf a very simple algo on how tf-idf works
https://github.com/RaRe-Technologies/gensim production-level implementation for topical modelling

### Algorithm: TextRank

https://web.eecs.umich.edu/%7Emihalcea/papers/mihalcea.emnlp04.pdf

### Algorithm: Rapid Automatic Knowledge Extraction

https://www.researchgate.net/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents   

# Implementation Logic

# Novelty

# Acknowledgement

# Contribution as an open sourced project
