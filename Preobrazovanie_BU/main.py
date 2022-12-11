def bwt_coder(message):
    bwt_matrix = []
    for i in range(len(message)):
        bwt_matrix.append(message[i:] + message[:i])

    bwt_matrix.sort()
    last_column = ''.join([word[-1] for word in bwt_matrix])

    # print(*bwt_matrix, sep='\n')
    return last_column, bwt_matrix.index(message)


def bwt_decoder(encoded_word, position):
    decode_matrix = list(sorted(encoded_word))
    for _ in range(len(encoded_word) - 1):
        for i in range(len(encoded_word)):
            decode_matrix[i] = encoded_word[i] + decode_matrix[i]
        decode_matrix.sort()
    # print(*decode_matrix, sep='\n')
    # print('________________________________')
    return decode_matrix[position]

# абракадабра
message = input()
print(f"Полученное кодовое сообщение и номер расположение искомового сообщения- {bwt_coder(message)}")
print('________________________________')
encoded_word, position = bwt_coder(message)
# рдакраааабб
# 2
print(f"Изначальное сообщение - {bwt_decoder(encoded_word, position)}")
