# auto-ontology-learner (temporary name)

A Final Year Project.

# Preliminary Design Thoughts

Components breakdown:
0. Parsing of web page
1. Terms and Entities extraction
2. Relations extraction
3. Terms and Relations Mapping
4. Storage and Query support

# Research and Preparation Notes

A very good survey: https://78462f86-a-c00374d1-s-sites.googlegroups.com/a/medelyan.com/www/files/WIDM1097.pdf?attachauth=ANoY7coE4_96Ke-GZF_Qox3ApYPTKglXUOZjdJuIIRypJrojlNXjJHS81wpLZ9fp03g---LXt7hSfAPTjimhMWsdQn7xZdR3cqSsHMysJQeuKsvLlXnS9sHkRMNRgRmhTpfg3lCEKnYx4L0LVLIkNZKEH7uyiy1SYpo3PO0Ly7LuOxBWpqqwnBwTPCv6Pgrr4VsbL6blIBhYuygrZdUC0TuXr__48bCfwg%3D%3D&attredirects=0

## Terms extraction

"Identifying terminology is a preliminary step towards constructing a more expressive knowledge structure" 

 --- Gillam L, Tariq M, Ahmad K. Terminology and the construction of ontology. Terminology 2005, 11:55– 81.

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

The first approach relies on the statistical significance of a word. 

The second approach can be further divided into supervised and unsupervised approaches (refer to https://explosion.ai/blog/part-of-speech-pos-tagger-in-python)

To achieve automation, unsupervised approach is more appropriate.

Analysis of common algorithms:
1. tf-idf
2. TextRank [davidadamojr/TextRank](https://github.com/davidadamojr/TextRank/)
3. RAKE [aneesha/RAKE](https://github.com/aneesha/RAKE) | [csurfer/rake-nltk](https://github.com/csurfer/rake-nltk)
4. n-gram
5. pos tagger (based on syntactical regex example provided by NLTK, search for regex for tags)

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

strength: unsupervised, consider keywords from text only, does not require external corpus.
probably the most suitable cases to build. But there are weakness, which could likely be countered by the lingusitic methods such as POS-tagging and improved on the prepprocessing steps. Since there are a lot noise in web documents, simply removing the HTML tags and removing special characters is not going to be enough and besides, the connection between tags should be utilised. (tag type, depth)


### POS-Tagging - https://stevenloria.com/pos-tagging/ using this tagger implementation by matthew honnibal

data obtained from http://conll.cemantix.org/2012/data.html

1. POS-Tagging is enhanced with lingusitic features. 
2. Natural language is living and constantly changing
3. 3 methods are discussed and presented: HMM, Constraint Grammar Framework, TBL
4. Problem faced by POS tagging

- resolve ambiguity (uses the sequence of the tags and lexicial properties of that word)
- stochastic vs rule-based. Stochastic more favorable because the amount of data we are able to gather now is vast.
```
Stochastic techniques of natural language processing has been widely discussed and also criticized since its early days of use in the 1960's. The arguments against stochastic POS-tagging are mainly that the method in itself is considered too static to cope with the dynamics of natural language and that its impossible to find a corpus for training of the model that is large enough to represent the entire language of a specific population. However, the tremendous advances of computer capabilities combined with the ever increasing amount of digitalized texts since the 1960's has weakened those arguments and made stochastic POS-tagging techniques more and more favorable.
```

Use POS-tagging to locate all possible keys first. Text around it would be treated as possible information.

http://www8.cs.umu.se/education/examina/Rapporter/ErikKjellqvist.pdf

## Concepts Extraction

compare candidate words with Wikipedia  (dbpedia)

1. parse and store data
2. 

### NER

https://ac.els-cdn.com/S1877042811024232/1-s2.0-S1877042811024232-main.pdf?_tid=3146de3c-585c-4e68-8cba-a818d97742cd&acdnat=1522147067_8d0880783ce0e14cc3a18e06d4ad08ac


https://pdfs.semanticscholar.org/02df/3c6291b22ced6f8e1fb4e8a9c3a36cd149c0.pdf




## Relation Extraction

https://cs.nyu.edu/courses/spring17/CSCI-GA.2590-001/DependencyPaths.pdf

Good intro to relation extraction

http://www.cs.cmu.edu/~nbach/papers/A-survey-on-Relation-Extraction.pdf

http://aclweb.org/anthology/W17-2322
Stanford Relation Extractor
MITIE
OpenIE
GATE
Two main approaches: 

1. rule-based by identifying the keywords (heuristic))
2. Machine learning approach (described below)


http://ceur-ws.org/Vol-1064/Nebhi_Rule-Based.pdf

Three main approaches: supervised / distant supervised and unsupervised

1. traditional supervised approaches mostly taken kernel-based approaches, with the recent help
of lexcial and syntactic features support

2. Distant supervision introduced by utilising exsiting community contribution such as FreeBase and Dbpedia.
Problem: data noisy, hard to generate negative examples. To improve, (Riedel, S., Yao, L., McCallum, A.: Modeling relations and their mentions without
labeled text. In Proceedings of ECML, 2010.) and (Surdeanu, M. et al.: Multi-instance Multi-label Learning for Relation Extraction.
In Proceedings of EMNLP-CoNLL, 2012.) uses multi-label learning

3. Unsuperivised approach focuses more on the text itself, by collect co-occurrences of word pairs with strings
between them. But this is not applicable to a web scenario since the amount of data is small and 
not similar to each other. This provides challenges to identify the co-occurrences.


# Implementation Logic

### experimentation status

- [x] heuristic pattern summarisation for POS tagging
- [x] parsing of a given URL
- [ ] NER for short text
- [ ] Anchor text for short text
- [ ] extraction of keywords from long text
- [ ] extraction of sentences
- [ ] extraction of triples from sentences
- [ ] storage of graph
- [ ] construction of knowledge graph based on triples and keywords
- [ ] sample query of keywords and possible return

### prototyping status (if have time, otherwise will show simplified version)

- [ ] simple web front end for showing execution logging and sample output
- [ ] performance evaluation

# Final Report Layout

1. Introduction - similar to interim with more insights
2. Lit review on the following topics

- keywords extraction and algorithm
- NER
- relation extraction and triples extraction (for relation search)
- storage and search of knowledge

3. Project

Scalability 

1. Crawler Robustness
    1. Defense and attack
    2. Dedup Queue Algo
    
2. 

# Contribution as an open sourced project

# Thoughts

TODO: indexing of HTML tree

grouping of short keywords to form linked short text (achieve by using `find_siblings` if have time)

Data should be stored in 3 different tables.

One for anchor text

one for short text and its group

one for long text and for triples

self-learning on pos pattern for various web elements
if crawling to slow in demo use MT

# Future

a pre step towards true generic web parsing, must harvest the power of NLP, and using heuristic classifiction simplifies 
the problem such as phyicists do and derive their formula with assumptions.
We could not achieven 100% accuracy, even in 20 years time.


# Things still need to review
NER
Relationship extraction

# To run GUI

```bash
export FLASK_APP=PycharmProjects/auto-ontology-learner/src/gui/main.py
python3 -m flask run
```

