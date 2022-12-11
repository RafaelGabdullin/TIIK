from decimal import Decimal
from typing import List, Dict, AnyStr


class ArithmeticEncoding:
    def __init__(self, frequency_table: Dict):
        self.probability_table = self.get_probability_table(frequency_table)

    def get_probability_table(self, frequency_table):

        total_frequency = sum(list(frequency_table.values()))

        probability_table = {}
        for key, value in frequency_table.items():
            probability_table[key] = value / total_frequency

        return probability_table

    def get_encoded_value(self, encoder: List):
        last_stage = list(encoder[-1].values())
        last_stage_values = []
        for sublist in last_stage:
            for element in sublist:
                last_stage_values.append(element)

        last_stage_min = min(last_stage_values)
        last_stage_max = max(last_stage_values)

        return (last_stage_min + last_stage_max) / 2

    def process_stage(self, stage_min, stage_max):
        stage_probs = {}
        stage_domain = stage_max - stage_min
        for term_idx in range(len(self.probability_table.items())):
            term = list(self.probability_table.keys())[term_idx]
            term_prob = Decimal(self.probability_table[term])
            cum_prob = term_prob * stage_domain + stage_min
            stage_probs[term] = [stage_min, cum_prob]
            stage_min = cum_prob
        return stage_probs

    def encode(self, msg: AnyStr):
        """
        Encodes a message.
        """

        encoder = []

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for msg_term_idx in range(len(msg)):
            stage_probs = self.process_stage(stage_min, stage_max)

            msg_term = msg[msg_term_idx]
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            encoder.append(stage_probs)

        stage_probs = self.process_stage(stage_min, stage_max)
        encoder.append(stage_probs)

        encoded_msg = self.get_encoded_value(encoder)

        return encoder, encoded_msg

    def decode(self, encoded_msg: AnyStr, msg_length: int):
        decoder = []
        decoded_msg = ""

        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for idx in range(msg_length):
            stage_probs = self.process_stage(stage_min, stage_max)

            for msg_term, value in stage_probs.items():
                if encoded_msg >= value[0] and encoded_msg <= value[1]:
                    break

            decoded_msg = decoded_msg + msg_term
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            decoder.append(stage_probs)

        stage_probs = self.process_stage(stage_min, stage_max)
        decoder.append(stage_probs)

        return f"Изначальное сообщение - {decoded_msg}, сам процесс расшифровки - {decoder}"


if __name__ == '__main__':
    # a b c d e
    alphabet: List = input('Введите алфавит: ').split()
    # 0.2 0.1 0.3 0.2 0.2
    propabilities: List[Decimal] = [Decimal(x) for x in input('Введите таблицу вероятностей: ').split()]
    frequency_table = dict(list(zip(alphabet, propabilities)))
    ae = ArithmeticEncoding(frequency_table=frequency_table)
    # decbaceda
    encoder, encoded_msg = ae.encode(input('Введите слово, которое хотите закодировать: '))

    print(f"Закодированное сообщение - {encoded_msg}")

    # 0.7745385280
    print(ae.decode(encoded_msg, 9))
