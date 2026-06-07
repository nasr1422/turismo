"""Componentes compartidos de UI."""
from __future__ import annotations
import reflex as rx
from turismo_app.state import AppState

TEAL = "#0D9488"
TEAL_DARK = "#0F766E"
TEAL_LIGHT = "#CCFBF1"
GOLD = "#F59E0B"
DARK = "#0F172A"
GRAY = "#64748B"
LIGHT_BG = "#F8FAFC"

NAV_STYLE = {
    "background": "rgba(15,23,42,0.97)",
    "backdrop_filter": "blur(12px)",
    "position": "sticky",
    "top": "0",
    "z_index": "999",
    "border_bottom": f"1px solid {TEAL}30",
}

BTN_PRIMARY = {
    "background": f"linear-gradient(135deg, {TEAL}, {TEAL_DARK})",
    "color": "white",
    "border_radius": "8px",
    "font_weight": "600",
    "cursor": "pointer",
    "border": "none",
    "_hover": {"opacity": "0.9", "transform": "translateY(-1px)"},
    "transition": "all 0.2s",
}

BTN_OUTLINE = {
    "background": "transparent",
    "color": TEAL,
    "border": f"2px solid {TEAL}",
    "border_radius": "8px",
    "font_weight": "600",
    "cursor": "pointer",
    "_hover": {"background": TEAL, "color": "white"},
    "transition": "all 0.2s",
}


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.text("🌴", font_size="1.6rem"),
                rx.vstack(
                    rx.text("Turismo RD", font_size="1.2rem", font_weight="800",
                            color="white", letter_spacing="0.05em"),
                    rx.text("República Dominicana", font_size="0.65rem", color=TEAL,
                            letter_spacing="0.15em", text_transform="uppercase"),
                    spacing="0", align_items="flex-start",
                ),
                spacing="2", align_items="center",
            ),
            rx.spacer(),
            rx.hstack(
                rx.link("Inicio", href="/", color="white", font_weight="500",
                        _hover={"color": TEAL}, transition="color 0.2s"),
                rx.link("Destinos", href="/#ofertas", color="white", font_weight="500",
                        _hover={"color": TEAL}, transition="color 0.2s"),
                rx.link("Reservas", href="/reservas", **BTN_PRIMARY),
                spacing="6", align_items="center",
            ),
            align_items="center", width="100%", max_width="1200px",
            margin="0 auto", padding="0 24px",
        ),
        padding_y="16px",
        **NAV_STYLE,
    )


def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.text("🌴", font_size="1.4rem"),
                        rx.text("Turismo RD", color="white", font_weight="700", font_size="1.1rem"),
                        spacing="2",
                    ),
                    rx.text("Tu puerta al paraíso caribeño.", color="#94A3B8", font_size="0.85rem"),
                    align_items="flex-start", spacing="2",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text("Contacto", color="white", font_weight="600"),
                    rx.text("📧 info@turismord.com", color="#94A3B8", font_size="0.85rem"),
                    rx.text("📞 +1 (809) 555-0123", color="#94A3B8", font_size="0.85rem"),
                    rx.text("📍 Santo Domingo, RD", color="#94A3B8", font_size="0.85rem"),
                    align_items="flex-start", spacing="1",
                ),
                rx.vstack(
                    rx.text("Navegación", color="white", font_weight="600"),
                    rx.link("Inicio", href="/", color="#94A3B8", font_size="0.85rem", _hover={"color": TEAL}),
                    rx.link("Reservas", href="/reservas", color="#94A3B8", font_size="0.85rem", _hover={"color": TEAL}),
                    rx.link("API Docs", href="http://localhost:8000/docs", color="#94A3B8",
                            font_size="0.85rem", _hover={"color": TEAL}, is_external=True),
                    align_items="flex-start", spacing="1",
                ),
                width="100%", max_width="1200px", margin="0 auto",
                padding="0 24px", flex_wrap="wrap", gap="32px",
            ),
            rx.divider(border_color="#1E293B"),
            rx.text("© 2025 Turismo RD · Todos los derechos reservados",
                    color="#475569", font_size="0.8rem", text_align="center"),
            width="100%", spacing="4", padding_y="40px",
        ),
        background="#0F172A", margin_top="auto",
    )


def oferta_card(oferta: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.image(src=oferta["imagen_url"], width="100%", height="200px", object_fit="cover"),
                rx.box(
                    rx.text(f"${oferta['precio']:.0f}", color="white", font_weight="800", font_size="1.3rem"),
                    rx.text("USD / persona", color=TEAL_LIGHT, font_size="0.7rem"),
                    position="absolute", bottom="12px", right="12px",
                    background="rgba(15,23,42,0.85)", padding="8px 12px",
                    border_radius="8px", backdrop_filter="blur(4px)",
                ),
                rx.box(
                    rx.text(f"⏱ {oferta['duracion_dias']} días", color="white",
                            font_size="0.75rem", font_weight="600"),
                    position="absolute", top="12px", left="12px",
                    background=f"{TEAL}DD", padding="4px 10px", border_radius="20px",
                ),
                position="relative", overflow="hidden", width="100%", flex_shrink="0",
            ),
            rx.vstack(
                rx.text(oferta["titulo"], font_size="1.05rem", font_weight="700",
                        color=DARK, line_height="1.3"),
                rx.hstack(
                    rx.text("📍", font_size="0.8rem"),
                    rx.text(oferta["destino"], color=GRAY, font_size="0.82rem"),
                    spacing="1",
                ),
                rx.text(oferta["descripcion"], color=GRAY, font_size="0.83rem",
                        line_height="1.6", no_of_lines=3),
                rx.spacer(),
                rx.hstack(
                    rx.button("Ver detalles",
                              on_click=AppState.seleccionar_oferta(oferta["id"]),
                              **BTN_OUTLINE, font_size="0.82rem"),
                    rx.button("Reservar →",
                              on_click=AppState.ir_a_reserva(oferta["id"]),
                              **BTN_PRIMARY, font_size="0.82rem"),
                    width="100%", justify="between",
                ),
                align_items="flex-start", spacing="3",
                padding="16px", height="100%", width="100%",
            ),
            spacing="0", height="100%", align_items="stretch",
        ),
        background="white", border_radius="12px", overflow="hidden",
        box_shadow="0 4px 20px rgba(0,0,0,0.08)", border="1px solid #E2E8F0",
        transition="all 0.3s",
        _hover={"transform": "translateY(-4px)", "box_shadow": f"0 12px 32px rgba(13,148,136,0.2)"},
        height="100%",
    )


def section_title(title: str, subtitle: str = "") -> rx.Component:
    return rx.vstack(
        rx.text(title, font_size="2rem", font_weight="800", color=DARK,
                text_align="center", letter_spacing="-0.02em"),
        rx.cond(
            subtitle != "",
            rx.text(subtitle, color=GRAY, text_align="center",
                    max_width="600px", line_height="1.7"),
        ),
        rx.box(width="60px", height="4px",
               background=f"linear-gradient(90deg, {TEAL}, {GOLD})",
               border_radius="2px"),
        align_items="center", spacing="3", margin_bottom="40px",
    )
