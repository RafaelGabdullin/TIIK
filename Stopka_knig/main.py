def coder(message, symboltable):
    sequence, pad = [], symboltable[::]
    for char in message:
        indx = pad.index(char)
        sequence.append(indx)
        pad = [pad.pop(indx)] + pad
    return sequence

def decoder(sequence, symboltable):
    chars, pad = [], symboltable[::]
    for indx in sequence:
        char = pad[indx]
        chars.append(char)
        pad = [pad.pop(indx)] + pad
    return ''.join(chars)


encode_message = coder('рдакраааабб', ['а', 'б', 'д', 'к', 'р'])
print(encode_message)
print(decoder([4, 3, 2, 4, 3, 2, 0, 0, 0, 4, 0], ['а', 'б', 'д', 'к', 'р']))