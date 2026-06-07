"""Página de Descripción de Oferta Turística."""
from __future__ import annotations
import reflex as rx
from turismo_app.state import AppState
from turismo_app.components import (
    navbar, footer,
    TEAL, TEAL_DARK, TEAL_LIGHT, GOLD, DARK, GRAY,
    BTN_PRIMARY,
)


def descripcion_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        # Hero
        rx.box(
            rx.box(position="absolute", top="0", left="0", right="0", bottom="0",
                   background="linear-gradient(to top, rgba(15,23,42,0.9), rgba(15,23,42,0.3))",
                   z_index="1"),
            rx.image(src=AppState.oferta_seleccionada["imagen_url"],
                     position="absolute", top="0", left="0",
                     width="100%", height="100%", object_fit="cover", z_index="0"),
            rx.vstack(
                rx.link("← Volver a destinos", href="/", color=TEAL_LIGHT,
                        font_size="0.85rem", font_weight="600", _hover={"color": "white"}),
                rx.text(AppState.oferta_seleccionada["destino"], color=TEAL_LIGHT,
                        font_size="0.85rem", font_weight="600",
                        letter_spacing="0.15em", text_transform="uppercase"),
                rx.text(AppState.oferta_seleccionada["titulo"],
                        font_size="3rem", font_weight="900", color="white",
                        letter_spacing="-0.02em", line_height="1.1"),
                rx.hstack(
                    rx.box(rx.text(f"⏱ {AppState.oferta_seleccionada['duracion_dias']} días",
                                   color="white", font_size="0.85rem", font_weight="600"),
                           background=f"{TEAL}CC", padding="6px 14px", border_radius="20px"),
                    rx.box(rx.text(f"👥 {AppState.oferta_seleccionada['cupos_disponibles']} cupos",
                                   color="white", font_size="0.85rem", font_weight="600"),
                           background="rgba(255,255,255,0.15)", padding="6px 14px", border_radius="20px"),
                    spacing="3",
                ),
                align_items="flex-start", position="relative", z_index="2",
                padding="80px 48px", max_width="1200px", width="100%", margin="0 auto", spacing="3",
            ),
            position="relative", height="70vh", overflow="hidden",
        ),
        # Descripción + precio
        rx.box(
            rx.grid(
                rx.vstack(
                    rx.text("Descripción General", font_size="1.5rem", font_weight="800", color=DARK),
                    rx.box(width="50px", height="3px",
                           background=f"linear-gradient(90deg, {TEAL}, {GOLD})", border_radius="2px"),
                    rx.text(AppState.oferta_seleccionada["descripcion"],
                            color=GRAY, line_height="1.8"),
                    rx.vstack(
                        rx.text("✅ ¿Qué incluye?", font_weight="700", color=DARK),
                        rx.text(AppState.oferta_seleccionada["incluye"],
                                color=GRAY, font_size="0.9rem", line_height="1.7"),
                        align_items="flex-start", padding="16px",
                        background=f"{TEAL}0F", border_radius="10px",
                        border_left=f"4px solid {TEAL}", spacing="2", width="100%",
                    ),
                    align_items="flex-start", spacing="4",
                ),
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.text("Precio por persona", color=GRAY, font_size="0.85rem"),
                            rx.text(f"${AppState.oferta_seleccionada['precio']:.0f} USD",
                                    font_size="2.5rem", font_weight="900", color=TEAL, line_height="1"),
                            rx.divider(border_color="#E2E8F0"),
                            rx.hstack(rx.text("📅 Duración:", font_weight="600", color=DARK, font_size="0.9rem"),
                                      rx.text(f"{AppState.oferta_seleccionada['duracion_dias']} días",
                                              color=GRAY, font_size="0.9rem"), spacing="2"),
                            rx.hstack(rx.text("📍 Destino:", font_weight="600", color=DARK, font_size="0.9rem"),
                                      rx.text(AppState.oferta_seleccionada["destino"],
                                              color=GRAY, font_size="0.9rem"), spacing="2"),
                            rx.hstack(rx.text("👥 Cupos:", font_weight="600", color=DARK, font_size="0.9rem"),
                                      rx.text(f"{AppState.oferta_seleccionada['cupos_disponibles']} disponibles",
                                              color=GRAY, font_size="0.9rem"), spacing="2"),
                            rx.button("Reservar este paquete →",
                                      on_click=AppState.ir_a_reserva(AppState.oferta_seleccionada["id"]),
                                      **BTN_PRIMARY, width="100%", font_size="1rem"),
                            rx.text("Sin cargos ocultos · Cancelación flexible",
                                    color=GRAY, font_size="0.75rem", text_align="center"),
                            align_items="flex-start", spacing="4", width="100%",
                        ),
                        background="white", border_radius="16px", padding="28px",
                        box_shadow="0 8px 32px rgba(0,0,0,0.1)", border="1px solid #E2E8F0",
                        width="100%", position="sticky", top="100px",
                    ),
                ),
                columns=rx.breakpoints({"base": "1", "lg": "2"}),
                gap="48px", width="100%",
            ),
            padding="64px 48px", max_width="1200px", margin="0 auto",
        ),
        # Itinerario
        rx.box(
            rx.vstack(
                rx.text("Itinerario del viaje", font_size="1.5rem", font_weight="800", color=DARK),
                rx.box(width="50px", height="3px",
                       background=f"linear-gradient(90deg, {TEAL}, {GOLD})", border_radius="2px"),
                rx.text(AppState.oferta_seleccionada["itinerario"],
                        color=GRAY, line_height="2", font_size="0.95rem", white_space="pre-line"),
                align_items="flex-start", spacing="4", width="100%",
            ),
            padding="64px 48px", max_width="1200px", margin="0 auto", background="#F8FAFC",
        ),
        footer(),
        spacing="0", width="100%",
    )
