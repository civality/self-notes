# A: The car is driven on the road.
# B: The truck is driven on the highway.
#
# TF
# the in A  =2
# car in A  =1
# car in B  =0
# 
# IDF 
# document_count / num_occurence
# the  = log( 2 / 2 )
# car  = log( 2 / 1 )
# relevance is not linear. log is used to approximate this number to a sub-linear function
# say football is appeared in 100 documents and soccer in 1 document, 
# it would be wrong to claim that football is 100 times less relevant than soccer
# 
# There several variations of tf-idf formula
#
# idf(t) = log [ n / df(t) ] + 1 
# idf(t) = log [ n / df(t) + 1 ]
# + 1 is for not ignoring a term if it occurs in all documents
#
# idf(t) = log [ (1 + n) / (1 + df(t)) ] + 1
# to prevent zero division, pretend an extra document was seen 
# containing every term in the collection exactly one
#
# tf(t,d) can also be used after transforming 1 + log(tf)
#
#
# In the working example #1 for TF, we dynamically expand nested dicts 
# for each document and each term respectively
#
# docs = ['the car is driven on the road',
#          'the truck is driven on highway']
#
# vocab: {'road', 'highway', 'is', 'truck', 'the', 'driven', 'on', 'car'}
#
# dict_doc:
#        {0: {'the': 2, 'car': 1, 'is': 1, 'driven': 1, 'on': 1, 'road': 1},
#         1: {'the': 1, 'truck': 1, 'is': 1, 'driven': 1, 'on': 1, 'highway': 1}}
#
# dict_vocab_idf:
# 
#		 {'road': 1, 'highway': 1, 'is': 2, 'truck': 1, 'the': 2, 'driven': 2, 'on': 2, 'car': 1}

import math

# Working example # 1; dict of dicts are dynamically generated

def get_tf_idf(docs):

    dict_doc = dict()

    vocab = set()

    for i, doc in enumerate(docs):
        dict_term = dict()

        for term in doc.split(' '):
            if not term in dict_term:
                dict_term[term] = 1
            else:
                dict_term[term] += 1

            vocab.add(term)

        dict_doc[i] = dict_term

    dict_vocab_idf = dict()

    for term in vocab:
        for doc in docs:
            if term in doc.split(' '):
                if not term in dict_vocab_idf:
                    dict_vocab_idf[term] = 1
                else:
                    dict_vocab_idf[term] += 1

    for term in dict_vocab_idf:
        dict_vocab_idf[term] = math.log( len(docs) / dict_vocab_idf[term] )

    return dict_doc, vocab, dict_vocab_idf


docs = ['the car is driven on the road',
        'the truck is driven on highway']

dict_doc, vocab, dict_vocab_idf = get_tf_idf(docs)
print(dict_doc)
print(vocab)
print(dict_vocab_idf)


# for tf, just allocate a memory for 2D matrix, because this is what we deliver.
# for allocation, you need one pass of all terms in corpus, to build vocab
# dict_vocab does not need initialization because a key will be assigned only once
# dict_vocab_idf keys initiated with 0 to get rid of 'if key exist in dict' checks


# Working example # 1; 2D array is pre-allocated
import numpy as np

def get_tf_idf(docs):
    
    vocab = set()
    for doc in docs:
        for term in doc.split(' '):
            vocab.add(term)
    
    array_tf = np.zeros( ( len(vocab), len(docs)) )
    
    dict_vocab = dict()
    dict_vocab_idf = dict( zip(vocab, [0] * len(vocab) ) )
    
    for i, vocab_term in enumerate(vocab):

        dict_vocab[vocab_term] = i

        for j, doc in enumerate(docs):
            for term in doc.split(' '):
                if vocab_term == term:
                    array_tf[i][j] += 1 

        for doc in docs:
            if vocab_term in doc.split(' '):
                dict_vocab_idf[vocab_term] += 1

    for term in dict_vocab_idf:
        dict_vocab_idf[term] = math.log( len(docs) / dict_vocab_idf[term] )
    
    return vocab, dict_vocab, array_tf, dict_vocab_idf

docs = ['the car is driven on the road',
        'the truck is driven on highway']

vocab, dict_vocab, array_tf, dict_vocab_idf = get_tf_idf(docs)

print(vocab)
print(dict_vocab)
print(array_tf)
print(dict_vocab_idf)