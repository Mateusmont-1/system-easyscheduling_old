import flet

from app import tela_login
from app.config import COLOR_BACKGROUND_PAGE

async def main(page:flet.Page):
    page.title = "EasyScheduling"
    page.bgcolor = COLOR_BACKGROUND_PAGE
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.theme_mode = "dark"
    
    await tela_login.main(page)

if __name__ == "__main__":
    #flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_path ='/sistema_exemplo_manicure'
    # flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
    # ft.app(name=flet_path, target=main, view=None, port=flet_port)    
    flet.app(target=main, assets_dir="assets", port=8080, view=flet.AppView.WEB_BROWSER, name=flet_path)
