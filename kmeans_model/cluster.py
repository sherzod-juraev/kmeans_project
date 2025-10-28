from numpy import zeros

class Cluster:
    """Klasterlash klas"""
    
    def __init__(self, k: int, length: int, /):
        """Klasterlash xususiyatlari"""
        
        self.k = k
        # markazlarga tegishli nuqtalar uchun matritsa
        self.matrix = zeros((k, length + 1), dtype=int)
        # bir nuqtaning barcha markazlar bilan munosabatini saqlovchi massiv
        self.distance_centers = zeros(k, dtype=float)
        
    def accumulate(self, center_index: int, new_index: int, /) -> None:
        """Markaz guruhiga yangi malumot indeksini saqlash"""
        
        self.matrix[center_index][self.matrix[center_index][-1]] = new_index
        # har bir markaz massivlarining oxirgi elementi nuqtalar sonini saqlaydi
        self.matrix[center_index][-1] += 1
    
    def clear_groups_count(self) -> None:
        """Guruhlardagi elementlar sonini tozalash"""
        
        for i in range(self.k):
            self.matrix[i][-1] = 0
    
    def clear_distance_centers(self):
        """Markazlar bilan nuqta orasidagi masofalarni tozalash"""
        
        for i in range(self.k):
            self.distance_centers[i] = 0