import Levenshtein

class Cer:

    @staticmethod
    def cer(predicted: str, target: str):
        """
        Вычислияет CER(Character Error Rate) между двумя строками.

        :param predicted: str
        :param target: str
        :return: float
        """

        different = Levenshtein.distance(predicted, target)
        return different / len(predicted)

test1 = 'Arsenal is the best club in the world'
test2 = 'ManUnited is the best club in the world'

dif = Cer.cer(test1, test2)
print(dif)
