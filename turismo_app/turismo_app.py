"""Punto de entrada de Reflex."""
import reflex as rx
from turismo_app.pages.index import index_page
from turismo_app.pages.descripcion import descripcion_page
from turismo_app.pages.reservas import reservas_page

app = rx.App(
    style={
        "font_family": "'Plus Jakarta Sans', sans-serif",
        "margin": "0",
        "padding": "0",
        "box_sizing": "border-box",
        "min_width": "100vw",
    },
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap",
        "global.css",
    ],
)

app.add_page(index_page, route="/", title="Turismo RD – Inicio")
app.add_page(descripcion_page, route="/descripcion/[id]", title="Turismo RD – Destino")
app.add_page(reservas_page, route="/reservas", title="Turismo RD – Reservas")
