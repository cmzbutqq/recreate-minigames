import pygame

pygame.init()

w, h = 800, 600
x, y = 100, 100
rec = pygame.Rect(x, y, 50, 50)

screen = pygame.display.set_mode((w, h))

run = True
while run:
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 255, 255), rec)

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        rec.move_ip(-1, 0)
    if key[pygame.K_d]:
        rec.move_ip(1, 0)
    if key[pygame.K_w]:
        rec.move_ip(0, -1)
    if key[pygame.K_s]:
        rec.move_ip(0, 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
