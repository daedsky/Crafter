import flet as ft
import flet_ads
from typing import Callable

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import CrafterApp
# type hinting <end>

ID_INTERSTITIAL_AD: str = "ca-app-pub-3940256099942544/1033173712"
ID_BANNER_AD: str = "ca-app-pub-3940256099942544/9214589741"


def get_new_banner_ad():
    return ft.Container(
        content=flet_ads.BannerAd(unit_id=ID_BANNER_AD),
        width=320, height=50, bgcolor=ft.Colors.TRANSPARENT
    )


def handle_interstitial_ad_close(app: 'CrafterApp', e):
    app.page.overlay.remove(e.control)
    app.interstitial_ad = get_new_interstitial_ad(app=app)
    app.page.overlay.append(app.interstitial_ad)
    app.page.update()


def get_new_interstitial_ad(app: 'CrafterApp'):
    print(f'get_int_ad, {app = }')
    return flet_ads.InterstitialAd(
        unit_id=ID_INTERSTITIAL_AD,
        on_close=lambda x: handle_interstitial_ad_close(app=app, e=x)
    )


def show_interstitial_ad(function: Callable):
    def wrapper(*args, **kwargs):
        if args: app = args[0].app
        else: app = list(kwargs.values())[0].app
        if app.page.platform == ft.PagePlatform.ANDROID:
            app.interstitial_ad.show()
        return function(*args, **kwargs)

    return wrapper
