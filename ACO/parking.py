
import math
import pygame

class Parking:
    ROAD_COLORS = [(255, 255, 255), (150, 150, 150)]
    MODELE_1 = "ACO/images/parking_1.png", "ACO/images/parking_1_info.png", (300, 580, 0), (579, 450, -90), [(541, 298),(76, 137)]
    MODELE_2 = "ACO/images/parking_2.png", "ACO/images/parking_2_info.png", (950, 400, -180), (579, 330, -90), [(541, 183),(76, 137)]

    def __init__(
            self,
            screen: pygame.Surface
            ) -> None:
        
        self.init(screen, Parking.MODELE_1)

    def __init__(self,
                 screen: pygame.Surface,
                 modele
                 ) -> None:
        
        self.screen = screen
        self.screen.fill(pygame.Color(100, 100, 100))

        self.img = pygame.image.load(modele[0])
        self.img_info = pygame.image.load(modele[1])
        self.start_pos = modele[2]
        self.end_pos = modele[3]

        self.space = pygame.Rect(modele[4][0], modele[4][1])

    def draw(self) -> None:
        self.screen.blit(self.img,(0, 0))

    def check_pos(
            self,
            pos: tuple,
            angle: int
            ) -> None:
        
        corners = []
        d = math.sqrt(106**2+56**2)/2 # distance between the center of the car and each corner
        for i in [[-1,-1],[-1,1],[1,-1],[1,1]]:
            new_angle = math.atan2(56, 106) - i[0]*i[1] * math.radians(angle)
            corners.append([pos[0]+i[0]*d*math.cos(new_angle), pos[1]+i[1]*d*math.sin(new_angle)])

        pt1 = ((corners[0][0]+corners[2][0])/2,(corners[0][1]+corners[2][1])/2)
        pt2 = ((corners[1][0]+corners[3][0])/2,(corners[1][1]+corners[3][1])/2)
        corners.extend([pt1,pt2])

        for pt in corners:
            if not (0<=int(pt[0])<1080 and 0<=int(pt[1])<720) or self.img_info.get_at((int(pt[0]), int(pt[1]))) == (0,0,0):
                return False
        return True
    
    def check_park(
            self,
            car: 'Car'
            ) -> bool:
        
        return self.space.contains(car)