import sys, pathlib
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).parent
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h, sc in (('desktop', 1440, 900, 1), ('phone', 390, 844, 2)):
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=sc); pg.goto(f'file://{D}/index.html'); pg.wait_for_timeout(1500); pg.screenshot(path=str(D / f'_shot_{name}.png'), full_page=True)
    b.close()
