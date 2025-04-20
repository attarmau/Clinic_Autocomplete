# Autocomplete with Elasticsearch
![image](https://github.com/user-attachments/assets/48d60a5b-4585-4492-816a-8536ad66fdf9)
Demo image sourced from Synapse Medicine (https://www.synapse-medicine.com/component/diagnoses-search)


•	Microservice: search-service

•	Use case: Product/user/content autocomplete

•	Backed by: Elasticsearch

•	Sync strategy: Update ES index on relevant DB updates via Kafka or change data capture (CDC)


# how to use UV

uv init

uv venv .venv/search

uv add -r requirements.txt

.venv/Scripts/activate

# docker 
- docker compose up --build

# import
- python import_movies.py

# test
- curl localhost:8000
- curl localhost:9200/_cat/health

# kibana


# carehero
DELETE carehero_medical_autocomplete_index
GET carehero_medical_autocomplete_index/_mapping
GET carehero_medical_autocomplete_index/_count
GET carehero_medical_autocomplete_index/_search# Prefix
GET carehero_medical_autocomplete_index/_search
{  
  "query": {    
    "prefix": {      
      "primary_name.keywordstring": "abdominal"    
     }
   }
}

#Ngram
GET carehero_medical_autocomplete_index/_search
{
  "query": {
    "match": {
      "primary_name.edgengram": "ab"
    }
  }
}

# Completion Suggester
GET carehero_medical_autocomplete_index/_search
{
  "suggest": {
    "keyword-suggest-fuzzy": {
      "prefix": "ab",
      "completion": {
        "field": "primary_name.completion",
        "fuzzy": {
          "fuzziness": 1
        },
        "skip_duplicates": true
      }
    }
  }
}
PUT carehero_medical_autocomplete_index
{
  "settings": {
    "index": {
      "analysis": {
        "filter": {},
        "analyzer": {
          "keyword_analyzer": {
            "filter": [
              "lowercase",
              "asciifolding",
              "trim"
            ],
            "char_filter": [],
            "type": "custom",
            "tokenizer": "keyword"
          },
          "edge_ngram_analyzer": {
            "filter": [
              "lowercase"
            ],
            "tokenizer": "edge_ngram_tokenizer"
          },
          "edge_ngram_search_analyzer": {
            "tokenizer": "lowercase"
          }
        },
        "tokenizer": {
          "edge_ngram_tokenizer": {
            "type": "edge_ngram",
            "min_gram": 2,
            "max_gram": 20,
            "token_chars": [
              "letter"
            ]
          }
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "primary_name": {
        "type": "text",
        "fields": {
          "keywordstring": {
            "type": "text",
            "analyzer": "keyword_analyzer"
          },
          "edgengram": {
            "type": "text",
            "analyzer": "edge_ngram_analyzer",
            "search_analyzer": "edge_ngram_search_analyzer"
          },
          "completion": {
            "type": "completion"
          }
        },
        "analyzer": "standard"
      }
    }
  }
}

# Autocomplete 

- Prefie 
- Edge Ngram
- Completion Suggester

Tutorial: [https://github.com/soumilshah1995/AutoComplete-Input-Elastic-Search-Python](https://www.youtube.com/watch?v=gDOu_Su1GqY)
Referencce:
https://anandharshit.medium.com/elasticsearch-autocomplete-a-story-worth-telling-7802c3499861
https://coralogix.com/blog/elasticsearch-autocomplete-with-search-as-you-type/
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html#completion-suggester
https://taranjeet.medium.com/elasticsearch-using-completion-suggester-to-build-autocomplete-e9c120cf6d87
https://medium.com/data-science-in-your-pocket/kag-enhanced-rag-and-graphrag-for-llm-based-retrieval-e84a66d6088c
