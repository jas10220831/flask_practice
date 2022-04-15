from sentence_transformers import SentenceTransformer, util
import csv
import torch

f = open('stock_name.csv', 'r')
stock_name = csv.reader(f)
stock_name = list(stock_name)
stock_name = stock_name[0]
f.close()

model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

embeddings = model.encode(stock_name, convert_to_tensor=True)
# cosine_scores = util.cos_sim(embeddings, embeddings

def search_similar_stock(word):
    new_embed = model.encode([word], convert_to_tensor=True)
    cosine_scores = util.cos_sim(new_embed, embeddings)

    score = cosine_scores[0].tolist()

    result = []
    for i in range(len(score)-1):
        result.append({
            'name' : stock_name[i],
            'score' : score[i]
        })
        

    result = sorted(result, key=lambda x: x['score'], reverse=True)

    name_list = []
    for stock in result[:10]:
        name_list.append(stock['name'])

    return name_list

