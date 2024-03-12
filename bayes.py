import sys
import random 
import itertools 
import numpy as np
import cv2 as cv 

MAP_FILE = 'cape_python.png'
SA1_CORNERS = (130,265,180,315)
SA2_CORNERS = (80,255,130,305)
SA3_CORNERS = (105,205,155,255)

class Search():
    def __init__(self, name):
        self.name = name 
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR) #imread 메소드를 호출한 결과를 self.img 에트리뷰트에 대입한다. 
        
        if self.img is None:
            print('Could not load map file{}'.format(MAP_FILE),file=sys.stderr)
            sys.exit(1)
        self.area_actual = 0
        self.sailor_actual = [0,0]
        self.sa1 = self.img[SA1_CORNERS[1]: SA1_CORNERS[3], SA1_CORNERS[0] : SA1_CORNERS[2]]
        self.sa2 = self.img[SA2_CORNERS[1]: SA2_CORNERS[3], SA2_CORNERS[0] : SA2_CORNERS[2]]
        self.sa3 = self.img[SA3_CORNERS[1]: SA3_CORNERS[3], SA3_CORNERS[0] : SA3_CORNERS[2]]

        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0 #지와, 표시할텍스트, 텍스트의 왼쪽좌표아래튜플, 폰트 이름, 폰트 크기, 텍스트색을 인자로 남긴다. 

    def draw_map(self, last_known):
        cv.line(self.img, (20,370), (70,370),(0,0,0),2)
        cv.putText(self.img, '0', (8,370),cv.FONT_HERSHEY_PLAIN,1,(0,0,0))
        cv.putText(self.img, '50 Nautical Miles', (71,370), cv.FONT_HERSHEY_PLAIN, 1,(0,0,0))
        cv.rectangle(self.img, (SA1_CORNERS[0], SA1_CORNERS[1]),(SA1_CORNERS[2],SA1_CORNERS[3]),(0,0,0),1) # 첫 번째 수색 지역을 직사각형으로 그린다. 
        cv.putText(self.img, '1', (SA1_CORNERS[0]+3,SA1_CORNERS[1]+15),cv.FONT_HERSHEY_PLAIN,1,0) # 마지막으로 알려진 선원 위치를 +로 표시합니다. 
        cv.rectangle(self.img, (SA2_CORNERS[0],SA2_CORNERS[1]),(SA2_CORNERS[2],SA2_CORNERS[3]),(0,0,0),1)
        cv.putText(self.img, '2', (SA3_CORNERS[0]+3,SA3_CORNERS[1]+15),cv.FONT_HERSHEY_PLAIN,1,0)
        cv.putText(self.img, '+' , (last_known),cv.FONT_HERSHEY_PLAIN,1,(0,0,255))
        cv.putText(self.img, '+',(last_known),cv.FONT_HERSHEY_PLAIN,1,(0,0,255))
        cv.putText(self.img, '*=Actual Position',(275,370),cv.FONT_HERSHEY_PLAIN, 1,(255,0,0))
        cv.imshow('Search Area', self.img)
        cv.moveWindow('Search Area',750,10)
        cv.waitKey(500)
    
    def sailor_final_location(self, num_search_areas):
        self.sailor_actual[0] = np.random.choice(self.sa1.shape[1])
        self.sailor_actual[1] = np.random.choice(self.sa1.shape[0])
        area = int(random.triangular(1, num_search_areas+1))

        if area==1:
            x = self.sailor_actual[0] +SA1_CORNERS[0]
            y = self.sailor_actual[1] +SA1_CORNERS[1]
            self.area_actual = 1
        elif area ==2:
            x = self.sailor_actual[0] +SA2_CORNERS[0]
            y = self.sailor_actual[1] +SA2_CORNERS[1]
            self.area_actual =2
        elif area ==3:
            x = self.sailor_actual[0] + SA3_CORNERS[0]
            y = self.sailor_actual[1] + SA3_CORNERS[1]
            self.area_actual=3
        return x, y
    
    def calc_search_efectiveness(self):
        self.sep1 = random.uniform(0.2,0.9)
        self.sep2 = random.uniform(0.2,0.9)
        self.sep3 = random.uniform(0.2,0.9)
        
    def conduct_search(self, area_num, area_array, effectiveness_prob):
        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])
        coords = list(itertools.product(local_x_range, local_y_range)) # itertools 파이썬 표준 라이브러리에서 효율적으로 루프를 수행하는 이터레이터를 만들어주는 함수들로 이루어지다. 
        random.shuffle(coords)
        coords = coords[:int((len(coords)*effectiveness_prob))]
        loc_actual = (self.sailor_actual[0], self.sailor_actual[1])
        if area_num == self.area_actual and loc_actual in coords:
            return 'Found in Area {}'.format(area_num), coords 
        else:
            return 'Not Found', coords
    def revise_target_probs(self): #
        denom = self.p1 * (1- self.sep1) + self.p2*(1-self.sep2) + self.p3*(1-self.sep3)
        self.p1 = self.p1 * (1-self.sep1) / denom 
        self.p2 = self.p2 * (1-self.sep2)/ denom 
        self.p3 = self.p3 * (1-self.sep3)/denom 

def draw_menu(search_num):
    print('\nSearch {}'.format(search_num))

    print(
        """
        Choose next areas to search:

        0 - Quit
        1- Search Area 1 twice
        2- Search Area 2 twice
        3- Search Area 3 twice
        4- Search Area 1 & 2
        5 -Search Area 1 & 3
        6- Search Area 2 & 3
        7 - Start Over
    """
    )

def main():
    app = Search('cape_python')
    app.draw_map(last_known=(160, 290))
    sailor_x, sailor_y = app.sailor_final_location(num_search_areas=3)
    print("-"*65)
    print("\nInitial Target (P) Probabilities:")
    print("PI = {:.3f}, P2={:.3f}, P3={:.3f}".format(app.p1,app.p2,app.p3))
    search_num = 1

    while True:
        app.calc_search_efectiveness()
        draw_menu(search_num)
        results_1 = "Not Found"
        results_2 = "Not Found"
        choice = input("Choice: ")

        if choice == '0':
            sys.exit()
        if choice == '1':
            results_1, coords_1 = app.conduct_search(1, app.sa1, app.sep1)
            resutls_2, coords_2 = app.conduct_search(1, app.sa1, app.sep2)
            app.sep1 = (len(set(coords_1 + coords_2))) / (len(app.sa1)**2)
            app.sep2 = 0
            app.sep3 = 0
        elif choice == "2":
            results_1, coords_1 = app.conduct_search(2, app.sa2, app.sep2)
            results_2, coords_2 = app.conduct_search(2, app.sa2, app.sep2)
            app.sep1 = 0
            app.sep2 = (len(set(coords_1+coords_2))) / (len(app.sa2)**2)
            app.sep3 = 0
        elif choice == "3":
            results_1, coords_1 = app.conduct_search(3, app.sa3, app.sep3)
            results_2, coords_2 = app.conduct_search(3, app.sa3, app.sep3)
            app.sep1 = 0
            app.sep2 = 0
            app.sep3 = (len(set(coords_1+coords_2))) / (len(app.sa3)**2)
        elif choice == "4":
            results_1, coords_1 = app.conduct_search(1, app.sa1, app.sep1)
            results_2, coords_2 = app.conduct_search(2, app.sa2, app.sep2)
            app.sep3 = 0
        elif choice == '5':
            results_1, coords_1 = app.conduct_search(1, app.sa1, app.sep1)
            results_2, coords_2 = app.conduct_search(3, app.sa3, app.sep3)
            app.sep2 = 0
        elif choice == '6':
            results_1, coords_1 = app.conduct_search(2, app.sa2, app.sep2)
            resutls_2, coords_2 = app.conduct_search(3, app.sa3, app.sep3)
            app.sep1 = 0
        elif choice == '7':
            main()
        else:
            print("\nSorry, but that isn't a valid choie.",file=sys.stderr)
            continue
        app.revise_target_probs()
        print("\nSearch{} Results 1 = {}".format(search_num, results_1), file=sys.stderr)
        print("Search {} Resutls 2 ={}\n".format(search_num, results_2), file=sys.stderr)
        print("Search {} Effectiveness (E):".format(search_num))
        print("E1 = {:.3f}, E2 = {:.3f}, E3={:.3f}".format(app.sep1,app.sep2,app.sep3))
        if results_1 == "Not Found" and results_2 =="Not Found":
            print("\nNew Terminal Probabilities (P) for Search {}:".format(search_num+1))
            print("P1 = {:.3f}, P2 = {:.3f}, P3 = {:.3f}".format(app.p1, app.p2, app.p3))
        else:
            cv.circle(app.img, (sailor_x[0], sailor_y[0]),3,(255,0,0),-1)
            cv.imshow('Search Area', app.img)
            cv.waitKey(1500)
            main()
        search_num += 1
if __name__ == '__main__':
    main()          



