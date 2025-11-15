import pygame
import sys

pygame.init()

# --- Window settings ---
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wprowadzanie danych")

FONT = pygame.font.SysFont("segoeui", 24)
SMALL_FONT = pygame.font.SysFont("segoeui", 20)
TITLE_FONT = pygame.font.SysFont("segoeui", 30)

BG = (28, 28, 40)
FIELD = (45, 45, 65)
FIELD_ACTIVE = (70, 70, 110)
TEXT = (220, 220, 230)
ACCENT = (120, 200, 255)
BTN = (80, 150, 250)
BTN_HOVER = (120, 180, 255)


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
    "Długość sekcji A:",
    "Warunek A:",
    "Długość sekcji B:",
    "Warunek B:",
    "Warunek C:"
]

boxes = []
y = 90
for _ in labels:
    boxes.append(InputBox(330, y, 140, 32))
    y += 55

selected_index = 0
boxes[0].active = True

results = []


def checkCondition(current_section,current_condition, next_condition, section_max_lenght):
    if current_condition <  next_condition:
        return current_section < section_max_lenght
    return current_section + current_condition < section_max_lenght


def calculate(full_lenght, a_lenght, a_condition, b_lenght, b_condition, c_condition):
    current_section = 0
    best_division = 5000
    best_a_division = 0
    best_b_division = 0
    best_c_division = 0
    best_a_distance = 0
    best_b_distance = 0
    best_c_distance = 0

    a_division = 0
    b_division = 0
    c_division = 0
    for i in range (100):
        for j in range(100):
            a_division = 0
            b_division = 0
            c_division = 0
            current_section = 0
            current_condition = a_condition + i
            next_condition = b_condition + j
            while checkCondition(current_section, current_condition,next_condition, a_lenght):
                current_section += current_condition
                a_division +=1
            while checkCondition(current_section, next_condition,c_condition, a_lenght+b_lenght):
                current_section += next_condition
                b_division+=1

            i = 0
            a = full_lenght -  (current_section *2 )
            b = c_condition
            
            while a%b != 0 and i < 50:
                i+=1
                b-=1
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

        return [
            f"allDivisions: {best_division}",
            f"a_division: {best_a_division}   distance: {best_a_distance}",
            f"b_division: {best_b_division}   distance: {best_b_distance}",
            f"c_division: {best_c_division}   distance: {best_c_distance}",
        ]



button_scale = 1.0
button_center_y = 450  # <- przesunięty nieco niżej

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            btn_top = button_center_y - 20
            btn_bottom = button_center_y + 20
            if 220 <= event.pos[0] <= 380 and btn_top <= event.pos[1] <= btn_bottom:
                if all(b.text for b in boxes):
                    vals = list(map(int, [b.text for b in boxes]))
                    results = calculate(*vals)

    title = TITLE_FONT.render("Wprowadź dane", True, ACCENT)
    screen.blit(title, (30, 30))

    y = 95
    for lbl in labels:
        screen.blit(SMALL_FONT.render(lbl, True, TEXT), (30, y))
        y += 55

    for box in boxes:
        box.draw(screen)

    # Button animation
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

    # Results panel
    pygame.draw.rect(screen, (40, 40, 55), (20, 490, 560, 140), border_radius=10)
    pygame.draw.rect(screen, ACCENT, (20, 490, 560, 140), 2, border_radius=10)

    y = 510
    for r in results:
        screen.blit(SMALL_FONT.render(r, True, ACCENT), (40, y))
        y += 28

    pygame.display.flip()

pygame.quit()
sys.exit()
