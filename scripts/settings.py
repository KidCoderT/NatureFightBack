from PIL import ImageColor
import pygame

pygame.init()

SCALE_AMOUNT = 3
WIDTH, HEIGHT = 230 * SCALE_AMOUNT, 216 * SCALE_AMOUNT
SCALE_WIDTH, SCALE_HEIGHT = WIDTH / 2, HEIGHT / 2

MESSAGE_TEXT_FONT = pygame.font.Font("assets/font/Sabo-Filled.otf", 16)


def scale_image(img, factor=SCALE_AMOUNT):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    img = pygame.transform.scale(img, size)
    img.convert()
    return img


def draw_text_multilined(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = 3

    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return text


def outline_mask(img, loc, display):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    n = 0
    for point in mask_outline:
        mask_outline[n] = (point[0] + loc[0], point[1] + loc[1])
        n += 1
    pygame.draw.polygon(display, (255, 255, 255), mask_outline, 3)


def palette_swap(surf, old_c, new_c):
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(ImageColor.getcolor(new_c, "RGB"))
    surf.set_colorkey(ImageColor.getcolor(old_c, "RGB"))
    img_copy.blit(surf, (0, 0))
    return img_copy
