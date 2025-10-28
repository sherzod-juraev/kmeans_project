from numpy import zeros, sum as nm_sum, argmax


class Helper:
    """Yordamchi klas"""

    def __init__(self, k: int, length: int, /):
        """Yordamchining xususiyatlari"""

        self.length = length # barcha malumotlar soni
        self.array = zeros(length, dtype=float) # markazlar ehtimolliklari nuqtalar bilan munosabatdagi
        self.total = 0 # markazlarni nuqtalar bilan orasidagi masofa kvadratining yig'indisi
        self.lower = .3 # quyi chegara
        self.high = .6 # yuqori chegara

    def sum(self) -> None:
        """Markazlar bilan nuqtalar orasidagi masofa kvadratlari yig'indisi"""

        self.total = nm_sum(self.array)

    def chance(self) -> None:
        """Ehtimolliklarni hisoblash"""
        
        self.array /= self.total
        
    def identifying_center_coordinate(self) -> int:
        """Navbatdagi markaz koordinatasini aniqlash"""
        
        for i in range(self.length):
            if self.lower < self.array[i] and self.array[i] < self.high:
                return i
        return argmax(self.array)