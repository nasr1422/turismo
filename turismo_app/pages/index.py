"""Página de Inicio – Turismo RD."""
from __future__ import annotations
import reflex as rx
from turismo_app.state import AppState
from turismo_app.components import (
    navbar, footer, oferta_card, section_title,
    TEAL, TEAL_DARK, TEAL_LIGHT, GOLD, DARK, GRAY, LIGHT_BG,
)


def hero_section() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute", top="0", left="0", right="0", bottom="0",
            background="linear-gradient(135deg, rgba(15,23,42,0.85) 0%, rgba(13,148,136,0.4) 100%)",
            z_index="1",
        ),
        rx.vstack(
            rx.text("REPÚBLICA DOMINICANA", color=TEAL_LIGHT, font_size="0.85rem",
                    font_weight="600", letter_spacing="0.2em"),
            rx.text("Vive el Caribe", font_size="3.5rem", font_weight="900", color="white",
                    text_align="center", line_height="1.15"),
            rx.text("Auténtico", font_size="3.5rem", font_weight="900", color=GOLD,
                    text_align="center", line_height="1.15"),
            rx.text(
                "Descubre destinos paradisíacos, aventuras únicas y experiencias que duran para siempre.",
                color="#CBD5E1", text_align="center", max_width="500px", line_height="1.7",
            ),
            rx.hstack(
                rx.button(
                    "Explorar destinos",
                    on_click=rx.scroll_to("ofertas"),
                    background=f"linear-gradient(135deg, {TEAL}, {TEAL_DARK})",
                    color="white", border_radius="8px", padding="12px 28px",
                    font_weight="600", cursor="pointer", border="none",
                    _hover={"opacity": "0.9"},
                ),
                rx.link(
                    rx.button(
                        "Hacer reserva",
                        background="transparent", color="white",
                        border="2px solid white", border_radius="8px",
                        padding="12px 28px", font_weight="600", cursor="pointer",
                        _hover={"background": "white", "color": DARK},
                    ),
                    href="/reservas",
                ),
                spacing="4", flex_wrap="wrap", justify="center",
            ),
            spacing="5", align_items="center", position="relative", z_index="2",
            padding="100px 32px", max_width="700px", margin="0 auto",
        ),
        position="relative",
        background_image="url('https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=1600')",
        background_size="cover", background_position="center",
        min_height="90vh", display="flex", align_items="center", justify_content="center",
        width="100%",
    )


def search_bar() -> rx.Component:
    return rx.center(
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text("DESTINO", font_size="0.65rem", font_weight="700", color=GRAY,
                            letter_spacing="0.1em"),
                    rx.input(
                        placeholder="¿A dónde vas?",
                        value=AppState.busqueda_destino,
                        on_change=AppState.set_busqueda_destino,
                        border="none", background="transparent",
                        font_size="0.9rem", _focus={"outline": "none"},
                        width="100%", height="28px",
                    ),
                    spacing="1", flex="1", min_width="150px",
                ),
                rx.divider(orientation="vertical", height="36px", border_color="#E2E8F0"),
                rx.vstack(
                    rx.text("PRECIO MÁX. (USD)", font_size="0.65rem", font_weight="700",
                            color=GRAY, letter_spacing="0.1em"),
                    rx.input(
                        placeholder="Ej: 500",
                        value=AppState.busqueda_precio_max,
                        on_change=AppState.set_busqueda_precio_max,
                        type_="number", border="none", background="transparent",
                        font_size="0.9rem", _focus={"outline": "none"},
                        width="100%", height="28px",
                    ),
                    spacing="1", flex="1", min_width="150px",
                ),
                rx.button(
                    "🔍 Buscar",
                    on_click=AppState.cargar_ofertas,
                    background=f"linear-gradient(135deg, {TEAL}, {TEAL_DARK})",
                    color="white", border_radius="8px", padding="10px 24px",
                    font_weight="700", cursor="pointer", border="none",
                    _hover={"opacity": "0.9"}, white_space="nowrap", flex_shrink="0",
                ),
                spacing="4", align_items="center", width="100%", flex_wrap="wrap",
            ),
            background="white", border_radius="14px", padding="18px 24px",
            box_shadow="0 16px 48px rgba(0,0,0,0.14)", width="100%", max_width="800px",
        ),
        width="100%",
        padding_x="16px",
        margin_top="-50px",
        position="relative",
        z_index="10",
    )


def stats_section() -> rx.Component:
    stats = [
        ("10K+", "Viajeros felices"),
        ("50+", "Destinos disponibles"),
        ("8", "Años de experiencia"),
        ("4.9★", "Calificación promedio"),
    ]
    return rx.center(
        rx.hstack(
            *[rx.vstack(
                rx.text(v, font_size="1.8rem", font_weight="900", color=TEAL),
                rx.text(l, color=GRAY, font_size="0.8rem", text_align="center"),
                align_items="center", spacing="1",
            ) for v, l in stats],
            spacing="9", flex_wrap="wrap", justify="center",
        ),
        padding="48px 24px",
        background=LIGHT_BG,
        width="100%",
    )


def ofertas_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            section_title(
                "Nuestros Destinos",
                "Explora las mejores ofertas turísticas cuidadosamente seleccionadas para ti",
            ),
            rx.cond(
                AppState.cargando,
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3"),
                        rx.text("Cargando ofertas...", color=GRAY),
                        align_items="center", spacing="3",
                    ),
                    padding="60px",
                ),
                rx.grid(
                    rx.foreach(AppState.ofertas, oferta_card),
                    columns=rx.breakpoints({"base": "1", "sm": "2", "lg": "3", "xl": "4"}),
                    gap="24px", width="100%",
                ),
            ),
            on_mount=AppState.cargar_ofertas,
            align_items="center", width="100%",
        ),
        id="ofertas",
        padding="80px 24px",
        width="100%",
        max_width="1280px",
        margin="0 auto",
    )


def why_us_section() -> rx.Component:
    features = [
        ("🏆", "Calidad Garantizada", "Solo trabajamos con los mejores proveedores y hoteles certificados."),
        ("💰", "Mejor Precio", "Garantizamos el precio más bajo o te devolvemos la diferencia."),
        ("🛡️", "Viaje Seguro", "Seguro de viaje incluido y atención 24/7 durante tu estadía."),
        ("🌟", "Experiencias Únicas", "Actividades exclusivas que no encontrarás en ningún otro lugar."),
    ]
    return rx.center(
        rx.vstack(
            section_title("¿Por qué elegirnos?"),
            rx.grid(
                *[rx.vstack(
                    rx.text(icon, font_size="2.2rem"),
                    rx.text(title, font_weight="700", color=DARK, font_size="0.95rem"),
                    rx.text(desc, color=GRAY, text_align="center", font_size="0.82rem", line_height="1.6"),
                    align_items="center", spacing="2", padding="24px 16px",
                    background="white", border_radius="12px",
                    box_shadow="0 2px 16px rgba(0,0,0,0.06)",
                    transition="all 0.3s",
                ) for icon, title, desc in features],
                columns=rx.breakpoints({"base": "1", "sm": "2", "lg": "4"}),
                gap="20px", width="100%",
            ),
            align_items="center", width="100%",
        ),
        padding="80px 24px",
        width="100%",
    )


def contact_section() -> rx.Component:
    return rx.center(
        rx.box(
            rx.vstack(
                rx.grid(
                    rx.vstack(
                        rx.text("¿Tienes preguntas?", font_size="1.8rem", font_weight="800",
                                color="white"),
                        rx.text(
                            "Nuestro equipo está disponible para ayudarte a planificar el viaje perfecto.",
                            color="#94A3B8", line_height="1.7",
                        ),
                        rx.text("📧 info@turismord.com", color=TEAL_LIGHT, font_size="0.9rem"),
                        rx.text("📞 +1 (809) 555-0123", color=TEAL_LIGHT, font_size="0.9rem"),
                        align_items="flex-start", spacing="3",
                    ),
                    rx.vstack(
                        rx.input(
                            placeholder="Tu nombre",
                            value=AppState.contacto_nombre,
                            on_change=AppState.set_contacto_nombre,
                            background="#1E293B", border="1px solid #334155",
                            border_radius="8px", color="white", padding="10px 14px",
                            font_size="0.9rem",
                            _placeholder={"color": "#64748B"},
                            _focus={"border_color": TEAL, "outline": "none"},
                            width="100%",
                        ),
                        rx.input(
                            placeholder="Tu email",
                            value=AppState.contacto_email,
                            on_change=AppState.set_contacto_email,
                            type_="email",
                            background="#1E293B", border="1px solid #334155",
                            border_radius="8px", color="white", padding="10px 14px",
                            font_size="0.9rem",
                            _placeholder={"color": "#64748B"},
                            _focus={"border_color": TEAL, "outline": "none"},
                            width="100%",
                        ),
                        rx.text_area(
                            placeholder="¿En qué podemos ayudarte?",
                            value=AppState.contacto_mensaje,
                            on_change=AppState.set_contacto_mensaje,
                            background="#1E293B", border="1px solid #334155",
                            border_radius="8px", color="white", padding="10px 14px",
                            font_size="0.9rem", rows="4",
                            _placeholder={"color": "#64748B"},
                            _focus={"border_color": TEAL, "outline": "none"},
                            width="100%", resize="none",
                        ),
                        rx.cond(
                            AppState.contacto_enviado,
                            rx.box(
                                rx.text("✅ ¡Mensaje enviado!", color=TEAL_LIGHT, font_size="0.9rem"),
                                padding="10px", background=f"{TEAL}20",
                                border_radius="8px", border=f"1px solid {TEAL}50", width="100%",
                            ),
                            rx.button(
                                "Enviar mensaje",
                                on_click=AppState.enviar_contacto,
                                background=f"linear-gradient(135deg, {TEAL}, {TEAL_DARK})",
                                color="white", border_radius="8px", width="100%",
                                padding="11px", font_weight="600", cursor="pointer",
                                border="none", _hover={"opacity": "0.9"},
                            ),
                        ),
                        spacing="3", width="100%",
                    ),
                    columns=rx.breakpoints({"base": "1", "md": "2"}),
                    gap="48px", width="100%",
                ),
                width="100%",
            ),
            width="100%", max_width="960px", padding="60px 32px",
        ),
        id="contacto",
        background=f"linear-gradient(135deg, {DARK} 0%, #1E293B 100%)",
        width="100%",
    )


def index_page() -> rx.Component:
    return rx.box(
        navbar(),
        hero_section(),
        search_bar(),
        stats_section(),
        ofertas_section(),
        why_us_section(),
        contact_section(),
        footer(),
        width="100%",
        overflow_x="hidden",
    )
