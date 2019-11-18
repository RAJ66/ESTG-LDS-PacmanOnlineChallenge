import pygame as pg


(width,heigth) = (1000,600)
screen = pg.display.set_mode((width,heigth))
background_colour = (255,255,255)
COLOR_INACTIVE = pg.Color('black')
COLOR_ACTIVE = pg.Color('black')
screen.fill(background_colour)
pg.display.flip()
pg.display.set_caption('Pacman Online Challenge')
pg.display.set_caption('Image')
image = pg.image.load(r'C:\Users\Hugo\Desktop\poc.png')
image = pg.transform.scale(image, (200, 100))
display_surface = pg.display.set_mode((300, 300 ))


running = True
print('||||||||||     ||||||||||     ||||||||||   |||\\\      ///|||   ||||||||||    |||\\\     |||')
print('|||     |||   |||      |||   |||           ||| \\\    /// |||  |||      |||   ||| \\\    |||')
print('|||     |||   |||      |||   |||           |||  \\\  ///  |||  |||      |||   |||  \\\   |||')
print('||||||||||    ||||||||||||   |||           |||   \\\///   |||  ||||||||||||   |||   \\\  |||')
print('|||           |||      |||   |||           |||           |||  |||      |||   |||    \\\ |||')
print('|||           |||      |||    ||||||||||   |||           |||  |||      |||   |||     \\\|||')
print('                                                                                             ')
print('                                    ||||||||||||||                          ||||||||||||                               ')
print('                                   |||||||||| O ||||                       |||| 0|||||0 |                                   ')
print('                                  ||||||||||||||||||         *****         ||||||||||||||                                         ')
print('                                 |||||||                    *******        ||||||||||||||                                        ')
print('                                  |||||                      *****         ||||||||||||||                            ')
print('                                   |||||||||||||||                         ||||||||||||||                                ')
print('                                    ||||||||||||||                         || |||  ||  ||                                ')

pg.init()
screen = pg.display.set_mode((640, 480))

FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)



def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((255, 255, 255))
        for box in input_boxes:
            box.draw(screen)

        screen.blit(image, (350, 170))
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()










