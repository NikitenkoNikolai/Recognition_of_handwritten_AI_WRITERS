import Levenshtein

class Cer:

    @staticmethod
    def cer(predicted: str, target: str) -> float:
        """
        Вычислияет CER(Character Error Rate) между двумя строками.

        predicted: Предсказанная строка.
        target: Ожидаемая строка.
        return: CER
        """

        different = Levenshtein.distance(predicted, target)
        return different / len(predicted)

test1 = 'Arsenal is the best club in the world'
test2 = 'ManUnited is the best club in the world'

dif = Cer.cer(test1, test2)
print(dif)
