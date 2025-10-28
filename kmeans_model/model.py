from numpy import array, zeros, argmin
from random import randint
from .helper import Helper
from .cluster import Cluster



class KMeans:
    """KMeans usuli"""
    
    def __init__(self, k: int, max_loop: int = 1_00_000, /):
        """KMeans xususiyatlari"""
        
        self.k = k # markazlar soni
        self.__property = 0 # fazo
        self.centers = None # markazlarni saqlovchi matritsa default aniqlanmagan holatda
        self.__old_centers = None # markazning oxirgi yangilanishdan oldingi koordinatalari
        self.datas = None # foydalanuvchi kiritgan nuqtalar (malumotlar)
        self.__length = 0 # nuqtalar (malumotlar) soni
        self.helper = None # yordamchi klas markazlarni dastlabki holatini aniqalshda zarur
        self.cluster = None # klasterlash koordinatalari va markazlarga tegishli nuqtalarni saqlovchi klas obyekti
        self.__max_loop = max_loop # training jarayonini infinite dan qutqaruvchi qiymat

    def create_matrix(self) -> None:
        """Markazlar uchun matritsalar yaratish"""
        
        # sukut bo'yicha uzunliklarga mos markazlarni saqlovchi numpy matritsasi
        self.centers = zeros((self.k, self.__property), dtype=float)
        self.__old_centers = zeros((self.k, self.__property), dtype=float)

    def __identify_centers(self):
        """Markazlarni dastlabki koordinatalarini aniqlash"""

        # 1-markazni tasodifiy tanlash
        num = randint(0, self.__length - 1)
        for i in range(self.__property):
            self.centers[0][i] = self.datas[num][i]
        for i in range(1, self.k):
            # markazlar bilan nuqtalar munosabatining ehtimolligi
            self.__distance_of_center_from_others(i)
            # keyingi markazning malumotlar ichidagi indeksi
            center_index = self.helper.identifying_center_coordinate()
            # keyingi markaz koordinatalarini belgialsh
            for j in range(self.__property):
                self.centers[i][j] = self.datas[center_index][j]
                


    def __distance_of_center_from_others(self, center_index: int, /) -> None:
        """Markazni boshqa nuqtalar bilan orasidagi masofasi"""
        
        for i in range(self.__length): #  masofalar kvadrati
            # bir nuqtaning barcha markazlar bilan munosabati
            distance_centers = zeros(center_index, dtype=float)
            for j in range(self.__property):
                for k in range(center_index):
                    distance_centers[k] += (self.datas[i][j] - self.centers[k][j]) ** 2
            # eng yaqin markazgacha bo'lgan masofa kvadratini ushlash
            # keyingi markaz tanlash ehtimolligini aniqlash uchun
            self.helper.array[i] = min(distance_centers)
        # nuqtalarni markazlar bilan masofasi kavdratlarini yig'indisi
        self.helper.sum()
        # masofalar kvadratari yig'indisidan ehtimolliklarni aniqlash
        self.helper.chance()

    def __check_matrix_identifying_properties(self) -> None:
        """Matritsani tekshirish va xususiyatlarni aniqlash"""

        # markaz tekislika tekshiriladi
        if self.datas.ndim != 2:
            raise ValueError('Matritsa notekis')
        # kerakli xususiyatlar aniqlanadi
        # moslashuvchanlik uchun muhim
        self.__property = self.datas.shape[1]
        self.__length = self.datas.shape[0]
        self.helper = Helper(self.k, self.__length)
        self.cluster = Cluster(self.k, self.__length)

    def fit(self, arr, /) -> None:
        """Moslashish"""
        
        # malumotlarni yozib olish numpy matritsasiga
        self.datas = array(arr)
        # malumotlar tekis matritsa ekanligini tekshirish va kerakli xususiyatlarni aniqlash
        self.__check_matrix_identifying_properties()
        # markazlar uchun matritsalar yaratish
        self.create_matrix()
        # markazlarni dastlabki koordinatalarini aniqlash
        # kmeans ++ aniqlash usuliga asoslangan 
        self.__identify_centers()
        # markazlarni malumotlarga moslashtirib qayta aniqlash
        # aniqrog'i siljitish
        self.__learning_datas()
    
    def __distance_of_point_centers(self, data_index: int, /) -> int:
        """Tegishli markaz indeksini qaytaradi"""
        
        # masofalar massivini tozalash
        self.cluster.clear_distance_centers()
        for i in range(self.k):
            for j in range(self.__property):
                self.cluster.distance_centers[i] += (self.datas[data_index][j] - self.centers[i][j]) ** 2
        # eng yaqin markaz indeksini qaytarish
        return argmin(self.cluster.distance_centers)
    
    def __new_coordinate_of_centers(self) -> bool:
        """Markazlarning yangi koordinataga ko'chirish"""
        
        # markazlarni yangilashdan oldin ularning dastlabki koordinatalarini saqlab turish
        for i in range(self.k):
            for j in range(self.__property):
                self.__old_centers[i][j] = self.centers[i][j]
        # markazlarning yangi koordinatalarini klaslaridagi nuqtalar bilan yangilash
        for i in range(self.k):
            # har fazo koordinatasi bo'yicha yig'indisi
            for j in range(self.__property):
                total = 0
                for k in range(self.cluster.matrix[i][-1]):
                    total += self.datas[self.cluster.matrix[i][k]][j]
                self.centers[i][j] = total / self.cluster.matrix[i][-1]
        # markazni siljiganlikka tekshirish
        for i in range(self.k):
            for j in range(self.__property):
                if self.centers[i][j] != self.__old_centers[i][j]:
                    # markaz surilgan birorta koordinatasi o'zgargan bo'lsa
                    return False
        # barcha koordinatalar o'zgarmagan
        # yani markaz turg'un joylashgan deb qaraladi
        return True
    
    def __learning_datas(self) -> None:
        """Malumotlarni organish"""
        
        # training jarayoni chegarali bajariladi
        for i in range(self.__max_loop):
            # barcha malumotlarni bo'yicha qayta qayta o'rganish
            for j in range(self.__length):
                # nuqtaning qaysi markazga yaqinligini aniqlash
                center_index = self.__distance_of_point_centers(j)
                # tegishli markazining guruhiga indeksini saqlash
                self.cluster.accumulate(center_index, j)
            # markazlarni qayta joylashtirish yoki siljitish
            result = self.__new_coordinate_of_centers()
            if result: # o'zgarganligini tekshirish
                print('Malumotlarga markazlar moslashtirildi')
                return None
            # agar markaz surilgan bo'lsa u holda markaz guruhlarini qayta aniqlash uchun undagi nuqtalarni tozalash
            self.cluster.clear_groups_count()
        print('Markazlar maksimal iteratsiyagacha yangilandi')
        
    def predict(self, new_data, /) -> int:
        """Yangi malumotni qaysi klasga tegishli ekanligini aniqlaydi"""

        if len(new_data) != self.__property:
            raise Exception('xususiyatlar soni mos emas')
        # masofalar massivini tozalash
        self.cluster.clear_distance_centers()
        # yangi malumotni barcha markazlar bilan munosabatini aniqlash
        for i in range(self.k):
            for j in range(self.__property):
                self.cluster.distance_centers[i] += (self.centers[i][j] - new_data[j]) ** 2
        # masofalardan eng yaqin markaz indeksini qaytaradi
        return argmin(self.cluster.distance_centers)

    def set_property(self, new_value, /) -> None:
        """Fazoni yangilash"""

        self.__property = new_value

    def get_property(self) -> int:

        return self.__property