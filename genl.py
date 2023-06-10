from PIL import Image, ImageDraw, ImageFont
import click
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def generate_logo(bg: str, fg: str, text: str,
                  size: int, filename: str = "logo.jpg"):
    icon = text
    sizes = (size, size)
    center_x, center_y = sizes[0]/2, sizes[1]/2

    image = Image.new('RGB', sizes, color=bg)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(resource_path("NotoEmoji.ttf"), int(300/512*size))

    text_width = draw.textlength(icon, font=font)
    text_bbox = font.getbbox(icon)
    text_height = text_bbox[3] - text_bbox[1]

    draw.text(((center_x) - (text_width/2), (center_y) - (text_height/2) - 20/512*size),
              icon, fill=fg, font=font)

    image.save(f"./{filename}")

@click.command()
@click.option('--background',"-bg",default="#ffffff", help='background color, hex')
@click.option('--foreground', '-fg', default="#000000", help='foreground color, hex')
@click.option('--size', '-s', default=512, help='icon size, default is 512')
@click.option('--batch', '-b', is_flag=True, help="make many files")
@click.argument('text')
def main(background, foreground, text, size, batch):
    """
    generate icon from emoji.
    ex) genl  🚀 -bg "#ffffff" -fg "#000000" -s 512
    don't use --batch and --size at the same time
    """
    if batch:
        generate_logo(background, foreground, text, 512, "logo-512.jpg")
        generate_logo(background, foreground, text, 256, "logo-256.jpg")
        generate_logo(background, foreground, text, 192, "logo-192.jpg")
    else:
        generate_logo(background, foreground, text, size)

if __name__ == '__main__':
    main()        
if getattr(sys, 'frozen', False):
    cli(sys.argv[1:])