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
        self.img = cv2.imread("messi.jpg")
        self.img2 = self.img.copy()  

        self.mask = np.zeros((self.img.shape[:2]), np.uint8)
        self.output = np.zeros((self.img.shape), np.uint8)

        black = (0, 0, 0)
        white = (255, 255, 255)
        green = (0, 255, 0)
        red = (0, 0, 255)

        self.bg = {"color" : black , "value" : 0}
        self.fg = {"color" : white , "value" : 1}
        self.prob_bg = {"color" : red , "value" : 2}
        self.prob_fg = {"color" : green , "value" : 3}

        self.draw = 0
        self.rect = 0
        self.rect_draw = 0
        self.value = self.fg
        self.rect_or_mask = None

    def mouse_rect(self, event, x, y, flags, param):
        if event == cv2.EVENT_RBUTTONDOWN:
            if self.rect == 0:
                self.rect_draw = 1
                self.xi, self.yi = x, y
                
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.rect_draw == 1:
                self.img = self.img2.copy()
                cv2.rectangle(self.img, (self.xi, self.yi), (x, y), (255, 0, 0), 2 )
                
        elif event == cv2.EVENT_RBUTTONUP:
            self.rect_draw = 0
            self.rect = 1
            self.rect_or_mask = 0
            self.img = self.img2.copy()
            cv2.rectangle(self.img, (self.xi, self.yi), (x, y), (255, 0, 0), 2)
            self.rect_value = (min(self.xi, x), min(self.yi, y), abs(self.xi - x), abs(self.yi - y))

        if event == cv2.EVENT_LBUTTONDOWN:
            if self.draw == 0:
                self.draw = 1
                cv2.circle(self.img, (x, y), 3, self.value["color"], -1)
                cv2.circle(self.mask, (x, y), 3, self.value["value"], -1)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.draw == 1:
                cv2.circle(self.img, (x, y), 3, self.value["color"], -1)
                cv2.circle(self.mask, (x, y), 3, self.value["value"], -1)
        
        elif event == cv2.EVENT_LBUTTONUP:
            self.draw = 0
            cv2.circle(self.img, (x, y), 3, self.value["color"], -1)
            cv2.circle(self.mask, (x, y), 3, self.value["value"], -1)
    
    def run(self):
        cv2.namedWindow("input")
        cv2.namedWindow("output")
        cv2.setMouseCallback("input", self.mouse_rect)

        while True:
            cv2.imshow("input", self.img)
            cv2.imshow("output", self.output)
            key = cv2.waitKey(1)

            if key == ord("0"):
                self.value = self.bg
            elif key == ord("1"):
                self.value = self.fg
            elif key == ord("2"):
                self.value = self.prob_bg
            elif key == ord("3"):
                self.value = self.prob_fg
            elif key == ord("s"):
                cv2.imwrite("output.jpg", self.output)
            elif key == ord("g"):
                self.grabcut()
            elif key == ord("q"):
                break
            
    def grabcut(self):
        bgdmodel = np.zeros((1, 65), np.float64)
        fgdmodel = np.zeros((1, 65), np.float64)
        if self.rect_or_mask == 0:
            cv2.grabCut(self.img2, self.mask, self.rect_value, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)
            self.rect_or_mask = 1
        elif self.rect_or_mask == 1:
            cv2.grabCut(self.img2, self.mask, self.rect_value, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_MASK)

        mask2 = np.where((self.mask==1) + (self.mask==3), 255, 0).astype('uint8')
        self.output = cv2.bitwise_and(self.img2, self.img2, mask=mask2)
            
            
if __name__ == "__main__":
    start = Segmentation()
    start.run()
    cv2.destroyAllWindows()



















    
