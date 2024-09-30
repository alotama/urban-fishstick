from utils.levenshtein_similarity import levenshtein_similarity

def compare_names(input_name, name_list, similarity_threshold):
    results = []
    for name in name_list:
        similarity = levenshtein_similarity(input_name, name)
        if similarity >= similarity_threshold:
            results.append({
                'name': name,
                'similarity': similarity
            })
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results