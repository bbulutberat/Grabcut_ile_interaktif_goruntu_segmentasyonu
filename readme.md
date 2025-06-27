## Grabcut Algoritması ile İnteraktif Segmantasyon
- Bu proje, OpenCV'nin GrabCut algoritmasını kullanarak kullanıcı etkileşimli bir görüntü segmentasyonu gerçekleştirir. Kullanıcı, görsel üzerinde dikdörtgen bölge belirleyip ardından farenin sol tuşuyla ön plan ve arka plan işaretlemesi yaparak segmentasyon sonucunu elde eder.

# GrabCut
- GrabCut algoritması, bir görüntüyü ön plan ve arka plan bölgelerine ayırmak için tasarlanmış grafik kesim tabanlı bir algoritmadır, bu da onu özellikle görüntü düzenleme ve nesne tanıma gibi uygulamalar için kullanışlı hale getirir.
Algoritma, segmentasyon sürecini başlatmak için kullanıcı etkileşimi gerektirir. Tipik olarak, görüntüdeki ilgilenilen nesnenin etrafına bir dikdörtgen çizilir. Algoritma daha sonra dikdörtgenin içindeki ve dışındaki renk ve doku bilgilerine dayalı olarak bu ilk segmentasyonu yinelemeli olarak iyileştirir.

**Avantajları**
- Kullanıcı sadece kaba bir dikdörtgen veya birkaç etiketle ön plan/arka plan işaretlemesi yapar, detayları algoritma belirler.
- Gri tonlamalı arka planlarda veya zayıf kontrasta rağmen ön planı iyi ayırt edebilir.
- Makine öğrenmesi eğitimi gerekmez.
- GMM (Gaussian Mixture Model) kullandığı için renk farklılıklarını oldukça etkili analiz eder.

**Dezavantajları**
- Başlangıçta verilen dikdörtgen, ön plan nesneyi kapsamazsa sonuç başarısız olur.
- Ön plan ve arka plan renkleri benzerse segmentasyon başarısı düşer.
- Nesne kenarlarında bulanıklık varsa veya sınırlar net değilse, segmentasyon hatalı olabilir.
- Büyük görsellerde veya fazla yineleme gerektiğinde işlem süresi artabilir.
- Kullanıcı müdahalesi olmadan çalışmaz; tam otomatik sistemler için uygun değildir.

# Nasıl Çalışır?
- Dikdörtgen çizmek için:
    Görsel üzerinde sağ tıklayıp (ve basılı tutup) nesneyi çevreleyecek şekilde bir dikdörtgen çizin. Bu adım, GrabCut algoritmasına ön planın nerede olduğunu belirtmek içindir.
- Manuel düzeltme yapmak için (sol tıklayarak çizebilirsiniz):
-
| Tuş | Açıklama           | Renk    |
| --- | ------------------ | ------- |
| `0` | Kesin arka plan    | Siyah   |
| `1` | Kesin ön plan      | Beyaz   |
| `2` | Muhtemel arka plan | Kırmızı |
| `3` | Muhtemel ön plan   | Yeşil   |
- İşlemler:
    - g → GrabCut algoritmasını çalıştırır.
    - s → Segmentasyon sonucunu output.jpg olarak kaydeder.
    - q → Uygulamadan çıkar, pencereleri kapatır.

# Requirements
- opencv - python
- numpy

# KOD AÇIKLAMASI

```
import cv2
import numpy as np

class Segmentation():
    
    def __init__ (self):
        print("""
        Dikdörtgen çizmek için mouse'un sol clickini kullanın
        Düzeltme yapmak için ->
        "0" -> kesin arka plan
        "1" -> kesin ön plan
        "2" -> muhtemel arka plan
        "3" -> muhtemel ön plan
        Grabcut işlemini yapmak için "g" tuşuna basınız.
        Çıktıyı kaydetmek için "s" tuşuna basınız
        Programdan çıkmak için "q" tuşuna basınız
        """)
        # Giriş görüntüsü ve kopyası alınır.
        self.img = cv2.imread("messi.jpg")
        self.img2 = self.img.copy()  

        # Grabcut algoritması için input ile aynı boyutlarda maske ve output görüntüsü oluşturulur.
        self.mask = np.zeros((self.img.shape[:2]), np.uint8)
        self.output = np.zeros((self.img.shape), np.uint8)

        # Renk kodları
        black = (0, 0, 0)
        white = (255, 255, 255)
        green = (0, 255, 0)
        red = (0, 0, 255)

        # Çizim yaparken belirtilen alanlar için renk ve maske için value değerleri oluşturulur.
        self.bg = {"color" : black , "value" : 0}
        self.fg = {"color" : white , "value" : 1}
        self.prob_bg = {"color" : red , "value" : 2}
        self.prob_fg = {"color" : green , "value" : 3}

        self.draw = 0 #Çizim flagi
        self.rect = 0 #Dikdörtgenin oluş oluşmadığını kontrol eden flag
        self.rect_draw = 0 #Dikdörtgen çizilme aşamasında mı kontrol eden flag
        self.value = self.fg #Kullanıcının çizimi hangi bölgeyi işaretliyor 
        self.rect_or_mask = None #Grabcut işleminde maske mi yoksa dikdörtgen mi kullanılacak

    #Mouse ile yapılan işlemler
    def mouse_rect(self, event, x, y, flags, param):
        # Mouse'nin sağ tuşuna basıldığında
        if event == cv2.EVENT_RBUTTONDOWN:
            if self.rect == 0: #eğer dikdörtgen çizilmediyse
                self.rect_draw = 1 #dikdörtgen çiziliyor
                self.xi, self.yi = x, y #dikdörtgenin başlangıç koordinatlarını al

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.rect_draw == 1: #dikdörtgen çizilmekte ise
                self.img = self.img2.copy() #her adımda input görseline dikdörtgen çizilmemesi için kopyası alınır.
                cv2.rectangle(self.img, (self.xi, self.yi), (x, y), (255, 0, 0), 2 ) #dikdörtgen çizdirilir.
                
        
        elif event == cv2.EVENT_RBUTTONUP:
            self.rect_draw = 0 #dikdörtgen çizme işlemi bitti
            self.rect = 1 #dikdörtgen artık çizildi
            self.rect_or_mask = 0 #grabcut dikdörtgeni kullanıcak
            self.img = self.img2.copy() 
            cv2.rectangle(self.img, (self.xi, self.yi), (x, y), (255, 0, 0), 2) #dikdörtgeni çiz

            #Grabcut için dikdörtgenin x,y,w,h bilgilerini al
            self.rect_value = (min(self.xi, x), min(self.yi, y), abs(self.xi - x), abs(self.yi - y)) 

        # Eğer sol tuşa basıldı ise
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.draw == 0: #çizim yapılmıyor ise
                self.draw = 1 #artık çizim yapılıyor

                # Mouse'un bulunduğu koordinatı merkez alan içi dolu bir daire çiz.
                cv2.circle(self.img, (x, y), 3, self.value["color"], -1)
                cv2.circle(self.mask, (x, y), 3, self.value["value"], -1)
        
        # Mouse harekete devam ediyorsa çizime devam et
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.draw == 1:
                cv2.circle(self.img, (x, y), 3, self.value["color"], -1)
                cv2.circle(self.mask, (x, y), 3, self.value["value"], -1)
        
        # Sol tuşa artık basılmıyorsa çizim flagini 0'a çekip son daireyi de çizer.
        elif event == cv2.EVENT_LBUTTONUP:
            self.draw = 0
            cv2.circle(self.img, (x, y), 3, self.value["color"], -1)
            cv2.circle(self.mask, (x, y), 3, self.value["value"], -1)
    
    def run(self):
        cv2.namedWindow("input") # İnput isimli pencere oluşturur.
        cv2.namedWindow("output") # Output isimli pencere oluşturur.

        # İnput penceresine mouse hareketleri için referans olarak mouse_Rect fonksiyonunu verir.
        cv2.setMouseCallback("input", self.mouse_rect) 

        while True:

            cv2.imshow("input", self.img)
            cv2.imshow("output", self.output)
            key = cv2.waitKey(1)

            #Kullanıcının bastığı tuş numarasına göre başlangıçta belirliten sözlükten kullanıcıya gösterilicek renk ve maskeye yazdırılıcak value değerleri ayarlanır.
            if key == ord("0"):
                self.value = self.bg
            elif key == ord("1"):
                self.value = self.fg        
            elif key == ord("2"):
                self.value = self.prob_bg
            elif key == ord("3"):
                self.value = self.prob_fg

            # Kullanıcı "s" tuşuna basarsa output görüntüsü "output.jpg" olarak kaydedilir.
            elif key == ord("s"):
                cv2.imwrite("output.jpg", self.output)
            
            #kullanıcı "g" tuşuna bastığında grabcut fonksiyonuna gidilir..
            elif key == ord("g"):
                self.grabcut()

            # kullanıcı q tuşuna bastığında döngüden çıkılır ve program sonlanır.
            elif key == ord("q"):
                break
            
    def grabcut(self):

        #grabcut algoritmasının kullanımı için gerekli diziler oluşturulur.
        bgdmodel = np.zeros((1, 65), np.float64)
        fgdmodel = np.zeros((1, 65), np.float64)

        # Dikdörtgen için grabcut işlemi uygulanır.
        if self.rect_or_mask == 0:
            cv2.grabCut(self.img2, self.mask, self.rect_value, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)
            self.rect_or_mask = 1

        # Kullanıcının çizimlerine göre grabcut işlemi tekrardan uygulanır.
        elif self.rect_or_mask == 1:
            cv2.grabCut(self.img2, self.mask, self.rect_value, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_MASK)

        # Maskedeki kesin ve muhtemel ön planlar 255, geri kalanlar 0 değerini alır ve bu maske mask2 değişkenine atanır.
        mask2 = np.where((self.mask==1) + (self.mask==3), 255, 0).astype('uint8')

        # Giriş görüntüsüne maske uygulanıp output değişkenine atanır.
        self.output = cv2.bitwise_and(self.img2, self.img2, mask=mask2)
            
            
if __name__ == "__main__":
    start = Segmentation()
    start.run()
    cv2.destroyAllWindows()
    ``` 



















    

