def levenshtein_distance(str1, str2):
    len_str1, len_str2 = len(str1), len(str2)
    matrix = [[0 for _ in range(len_str2 + 1)] for _ in range(len_str1 + 1)]

    for i in range(len_str1 + 1):
        matrix[i][0] = i
    for j in range(len_str2 + 1):
        matrix[0][j] = j

    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,        
                               matrix[i][j - 1] + 1,       
                               matrix[i - 1][j - 1] + cost)

    return matrix[len_str1][len_str2]