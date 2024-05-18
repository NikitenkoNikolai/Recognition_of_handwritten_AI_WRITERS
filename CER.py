import Levenshtein

class CER:

    @staticmethod
    def cer(predicted: str, target: str) -> float:
        """
        Вычислияет CER (Character Error Rate) между двумя строками.

        predicted: Предсказанная строка.
        target: Целевая строка.
        return: CER
        
        """

        different = Levenshtein.distance(predicted, target)
        return different / len(predicted)

predicted = 'Arsenal is the best club in the world'
target = 'ManUnited is the best club in the world'

dif = CER.cer(predicted, target)
print(dif)
