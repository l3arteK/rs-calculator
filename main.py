import pygame
import sys
import time

pygame.init()


WIDTH, HEIGHT = 600, 670
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rozstawy strzemion")

FONT = pygame.font.SysFont("segoeui", 24)
SMALL_FONT = pygame.font.SysFont("segoeui", 20)
TITLE_FONT = pygame.font.SysFont("segoeui", 30)
VERY_SMALL_FONT = pygame.font.SysFont("segoeui", 14)

BG = (28, 28, 40)
FIELD = (45, 45, 65)
FIELD_ACTIVE = (70, 70, 110)
TEXT = (220, 220, 230)
ACCENT = (120, 200, 255)
BTN = (80, 150, 250)
BTN_HOVER = (120, 180, 255)

best_division = sys.maxsize
best_a_division = 0
best_b_division = 0
best_c_division = 0
best_a_distance = 0
best_b_distance = 0
best_c_distance = 0


class TwoValueSelector:
    def __init__(self, x, y, size=32, spacing=12, values=(1, 5)):
        self.x = x
        self.y = y
        self.size = size
        self.spacing = spacing
        self.values = values
        self.active = values[0]  
        self.font = pygame.font.Font(None, 28)

        self.rects = []
        px = x
        for _ in values:
            self.rects.append(pygame.Rect(px, y, size, size))
            px += size + spacing

    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, r in enumerate(self.rects):
                if r.collidepoint(event.pos):
                    self.active = self.values[i]

    def draw(self, screen):
        for i, r in enumerate(self.rects):
            value = str(self.values[i])

            if self.active == self.values[i]:
                pygame.draw.rect(screen, (90, 200, 120), r, border_radius=6)
                pygame.draw.rect(screen, (255, 255, 255), r, 2, border_radius=6)
            else:
                pygame.draw.rect(screen, (70, 70, 90), r, border_radius=6)
                pygame.draw.rect(screen, (120, 120, 150), r, 2, border_radius=6)

            text = self.font.render(value, True, (230, 230, 240))
            screen.blit(text, (r.centerx - text.get_width() // 2,
                               r.centery - text.get_height() // 2))

    def get_value(self):
        return self.active




class InputBox:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = FIELD
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        self.color = FIELD_ACTIVE if self.active else FIELD
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
        pygame.draw.rect(surface, ACCENT, self.rect, 2, border_radius=6)
        txt_surface = SMALL_FONT.render(self.text, True, TEXT)
        text_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, text_rect)


labels = [
    "Całkowita długość:",
    "Długość odcinka lt1:",
    "Maksymalny rozstaw dla odcinka lt1:",
    "Długość odcinka lt2:",
    "Maksymalny rozstaw dla odcinka lt2:",
    "Rozstaw konstrukcyjny:",
    'Sprawdzaj rozstaw co: '
]

boxes = []
y = 90
for _ in labels[:-1]:
    boxes.append(InputBox(370, y, 140, 32))
    y += 55

selected_index = 0
boxes[0].active = True

results = []


def checkCondition(current_section,current_condition, next_condition, section_max_lenght, ):
    if current_condition <  next_condition:
        return current_section < section_max_lenght
    return current_section + current_condition < section_max_lenght


def calculate(full_lenght, a_lenght, a_condition, b_lenght, b_condition, c_condition, resolution):
  start = time.perf_counter()
  best_division = sys.maxsize
  best_a_division = 0
  best_b_division = 0
  best_c_division = 0
  best_a_distance = 0
  best_b_distance = 0
  best_c_distance = 0 
  

  for i in range (int(a_condition/resolution)):
    for j in range(int(b_condition/resolution)):
        a_division = 0
        b_division = 0
        c_division = 0
        current_section = 0
        current_condition = a_condition - i * resolution
        next_condition = b_condition - j * resolution
        while checkCondition(current_section, current_condition,next_condition, a_lenght):
            current_section += current_condition
            a_division +=1
        while checkCondition(current_section, next_condition,c_condition, a_lenght+b_lenght):
            current_section += next_condition
            b_division+=1

        k = 0
        a = full_lenght -  (current_section *2 )
        b = c_condition
        
        while a%b != 0 and k < int(50/resolution):
            k+=1
            b-=1 * resolution
        if a%b == 0:
            c_division = a/b
            if(2*(a_division + b_division) + c_division < best_division):
                best_division = 2*(a_division + b_division) + c_division
                best_a_division = a_division
                best_b_division = b_division
                best_c_division = c_division
                best_a_distance = current_condition
                best_b_distance = next_condition
                best_c_distance = b

    end = time.perf_counter()
    if best_division != sys.maxsize:
        return [
            f"Liczba wszystkich odcinków: {best_division}",
            f"Liczba odcinków lt1: {best_a_division}   Rozstaw lt1: {best_a_distance}",
            f"Liczba odcinków lt2: {best_b_division}   Rozstaw lt2: {best_b_distance}",
            f"Liczba odcinków konstrukcyjnych: {best_c_division}   Rozstaw konstrukcyjny: {best_c_distance}",
        ]
    else:
        return 'Nie znaleziono rozwiązania - upewnij się, że wprowadziłeś prawidłowe wartości'



button_scale = 1.0
button_center_y = 480
toggle = TwoValueSelector(400, 420)
running = True
while running:
    screen.fill(BG)
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            boxes[selected_index].active = False 
            selected_index = (selected_index + 1) % len(boxes)
            boxes[selected_index].active = True

        for box in boxes:
            box.handle_event(event)

        toggle.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            btn_top = button_center_y - 20
            btn_bottom = button_center_y + 20
            if 220 <= event.pos[0] <= 380 and btn_top <= event.pos[1] <= btn_bottom:
                if all(b.text for b in boxes):
                    vals = list(map(int, [b.text for b in boxes]))
                    vals.append(toggle.get_value())
                    results = calculate(*vals)

    title = TITLE_FONT.render("Wprowadź dane", True, ACCENT)
    screen.blit(title, (30, 30))

    y = 95
    for lbl in labels:
        screen.blit(SMALL_FONT.render(lbl, True, TEXT), (30, y))
        y += 55

    for box in boxes:
        box.draw(screen)
    toggle.draw(screen)


    mx, my = pygame.mouse.get_pos()
    btn_top = button_center_y - 20
    btn_bottom = button_center_y + 20
    hover = 220 <= mx <= 380 and btn_top <= my <= btn_bottom

    if hover:
        button_scale = min(1.12, button_scale + 0.04)
    else:
        button_scale = max(1.0, button_scale - 0.04)

    btn_width = int(160 * button_scale)
    btn_height = int(40 * button_scale)
    btn_x = 300 - btn_width // 2
    btn_y = button_center_y - btn_height // 2

    col = BTN_HOVER if hover else BTN
    pygame.draw.rect(screen, col, (btn_x, btn_y, btn_width, btn_height), border_radius=10)

    btn_text = FONT.render("OBLICZ", True, (0, 0, 20))
    txt_rect = btn_text.get_rect(center=(btn_x + btn_width // 2, btn_y + btn_height // 2))
    screen.blit(btn_text, txt_rect)

    panel_y = 510  
    panel_height = 140

    pygame.draw.rect(screen, (40, 40, 55), (20, panel_y, 560, panel_height), border_radius=10)
    pygame.draw.rect(screen, ACCENT, (20, panel_y, 560, panel_height), 2, border_radius=10)

    y = panel_y + 20  
    for r in results:
        screen.blit(VERY_SMALL_FONT.render(r, True, ACCENT), (40, y))
        y += 28

    pygame.display.flip()

pygame.quit()
sys.exit()
