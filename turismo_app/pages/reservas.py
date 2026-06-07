"""Página de Reservas – Turismo RD."""
from __future__ import annotations
import reflex as rx
from turismo_app.state import AppState
from turismo_app.components import (
    navbar, footer,
    TEAL, TEAL_DARK, GOLD, DARK, GRAY, LIGHT_BG, TEAL_LIGHT,
    BTN_PRIMARY,
)

INPUT_STYLE = {
    "background": "white", "border": "1.5px solid #E2E8F0", "border_radius": "8px",
    "padding": "12px 16px", "font_size": "0.88rem", "color": DARK,
    "_placeholder": {"color": "#94A3B8"},
    "_focus": {"border_color": TEAL, "outline": "none", "box_shadow": f"0 0 0 3px {TEAL}20"},
    "width": "100%", "transition": "all 0.2s",
}

LABEL_STYLE = {"font_size": "0.82rem", "font_weight": "700", "color": DARK,
               "text_transform": "uppercase", "letter_spacing": "0.08em"}


def field(label: str, component) -> rx.Component:
    return rx.vstack(rx.text(label, **LABEL_STYLE), component,
                     align_items="flex-start", spacing="1", width="100%")


def exito_card() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.text("🎉", font_size="4rem"),
            rx.text("¡Reserva Confirmada!", font_size="1.8rem", font_weight="800", color=DARK),
            rx.text(f"Tu reserva #{AppState.reserva_id} ha sido registrada exitosamente.",
                    color=GRAY, text_align="center"),
            rx.box(
                rx.vstack(
                    rx.text("¿Qué sigue?", font_weight="700", color=DARK),
                    rx.text("✉️ Recibirás un email de confirmación en las próximas 24h.", color=GRAY, font_size="0.9rem"),
                    rx.text("📞 Un asesor te contactará para confirmar los detalles.", color=GRAY, font_size="0.9rem"),
                    rx.text("💳 El pago se procesará al confirmar disponibilidad.", color=GRAY, font_size="0.9rem"),
                    align_items="flex-start", spacing="2",
                ),
                background=f"{TEAL}0F", border_radius="10px", padding="20px",
                border_left=f"4px solid {TEAL}", width="100%",
            ),
            rx.hstack(
                rx.button("Nueva reserva", on_click=AppState.nueva_reserva, **BTN_PRIMARY),
                rx.link(rx.button("Ver más destinos", background="white", color=TEAL,
                                  border=f"2px solid {TEAL}", border_radius="8px",
                                  padding="10px 24px", font_weight="600", cursor="pointer"),
                        href="/"),
                spacing="3",
            ),
            align_items="center", spacing="4", max_width="540px", text_align="center",
        ),
        padding="60px 24px",
    )


def formulario_reserva() -> rx.Component:
    return rx.box(
        rx.cond(
            AppState.reserva_exitosa,
            exito_card(),
            rx.vstack(
                rx.vstack(
                    rx.text("Completa tu Reserva", font_size="1.8rem", font_weight="800", color=DARK),
                    rx.text("Todos los campos marcados con * son obligatorios.", color=GRAY, font_size="0.88rem"),
                    align_items="flex-start", spacing="1", padding_bottom="8px",
                ),
                rx.divider(border_color="#E2E8F0"),
                # Oferta seleccionada
                rx.cond(
                    AppState.oferta_seleccionada != {},
                    rx.box(
                        rx.hstack(
                            rx.image(src=AppState.oferta_seleccionada["imagen_url"],
                                     width="80px", height="80px", object_fit="cover", border_radius="8px"),
                            rx.vstack(
                                rx.text(AppState.oferta_seleccionada["titulo"], font_weight="700", color=DARK),
                                rx.text(AppState.oferta_seleccionada["destino"], color=GRAY, font_size="0.85rem"),
                                rx.text(f"${AppState.oferta_seleccionada['precio']:.0f} USD · {AppState.oferta_seleccionada['duracion_dias']} días",
                                        color=TEAL, font_weight="700"),
                                align_items="flex-start", spacing="1",
                            ),
                            spacing="4", align_items="center",
                        ),
                        background=f"{TEAL}0A", border_radius="12px", padding="16px",
                        border=f"1px solid {TEAL}30", width="100%",
                    ),
                    rx.box(
                        rx.text("⚠️ Sin oferta seleccionada. ", color=GOLD, font_weight="600", display="inline"),
                        rx.link("Elige un destino →", href="/", color=TEAL, font_weight="600"),
                        padding="16px", background="#FFFBEB", border_radius="10px",
                        border=f"1px solid {GOLD}50", width="100%",
                    ),
                ),
                # Contacto
                rx.text("1. Datos de Contacto", font_size="1rem", font_weight="700", color=TEAL, padding_top="8px"),
                rx.grid(
                    field("Nombre completo *",
                          rx.input(placeholder="Ej: Juan Pérez", value=AppState.form_nombre,
                                   on_change=AppState.set_form_nombre, **INPUT_STYLE)),
                    field("Correo electrónico *",
                          rx.input(placeholder="juan@email.com", type_="email",
                                   value=AppState.form_email, on_change=AppState.set_form_email, **INPUT_STYLE)),
                    columns=rx.breakpoints({"base": "1", "md": "2"}), gap="16px", width="100%",
                ),
                field("Teléfono / WhatsApp",
                      rx.input(placeholder="+1 (809) 000-0000", type_="tel",
                               value=AppState.form_telefono, on_change=AppState.set_form_telefono, **INPUT_STYLE)),
                # Detalles
                rx.text("2. Detalles de la Actividad", font_size="1rem", font_weight="700", color=TEAL),
                rx.grid(
                    field("Fecha de viaje *",
                          rx.input(type_="date", value=AppState.form_fecha,
                                   on_change=AppState.set_form_fecha, **INPUT_STYLE)),
                    field("Cantidad de personas *",
                          rx.input(type_="number", placeholder="1", value=AppState.form_personas,
                                   on_change=AppState.set_form_personas, min_="1", max_="20", **INPUT_STYLE)),
                    columns=rx.breakpoints({"base": "1", "md": "2"}), gap="16px", width="100%",
                ),
                field("Notas especiales",
                      rx.text_area(placeholder="Alergias, preferencias, peticiones especiales...",
                                   value=AppState.form_notas, on_change=AppState.set_form_notas,
                                   rows="3", resize="none", **{**INPUT_STYLE, "padding": "12px 16px"})),
                # Pago
                rx.text("3. Método de Pago", font_size="1rem", font_weight="700", color=TEAL),
                rx.grid(
                    *[rx.box(
                        rx.vstack(
                            rx.text(icon, font_size="1.8rem"),
                            rx.text(label, font_weight="600", font_size="0.88rem", color=DARK),
                            rx.text(desc, font_size="0.75rem", color=GRAY, text_align="center"),
                            align_items="center", spacing="1",
                        ),
                        padding="16px", border_radius="10px",
                        border=rx.cond(AppState.form_metodo_pago == value,
                                       f"2px solid {TEAL}", "2px solid #E2E8F0"),
                        background=rx.cond(AppState.form_metodo_pago == value, f"{TEAL}0F", "white"),
                        cursor="pointer", on_click=AppState.set_form_metodo_pago(value),
                        text_align="center", transition="all 0.2s", _hover={"border_color": TEAL},
                    ) for icon, label, desc, value in [
                        ("💳", "Tarjeta", "Visa / Mastercard", "tarjeta"),
                        ("🏦", "Transferencia", "Banco local", "transferencia"),
                        ("💵", "Efectivo", "Pago en oficina", "efectivo"),
                        ("📱", "PayPal", "Pago digital", "paypal"),
                    ]],
                    columns=rx.breakpoints({"base": "2", "md": "4"}), gap="12px", width="100%",
                ),
                # Error
                rx.cond(
                    AppState.error_mensaje != "",
                    rx.box(rx.text(f"⚠️ {AppState.error_mensaje}", color="#DC2626", font_size="0.9rem"),
                           background="#FEF2F2", border_radius="8px", padding="12px 16px",
                           border="1px solid #FECACA", width="100%"),
                ),
                rx.button("Confirmar Reserva →", on_click=AppState.enviar_reserva,
                          **BTN_PRIMARY, width="100%", font_size="1.05rem", margin_top="8px"),
                rx.text("🔒 Tu información está protegida con encriptación SSL",
                        color=GRAY, font_size="0.78rem", text_align="center"),
                align_items="flex-start", spacing="4", width="100%",
            ),
        ),
        background="white", border_radius="16px",
        padding=rx.breakpoints({"base": "24px", "md": "40px"}),
        box_shadow="0 8px 40px rgba(0,0,0,0.08)", border="1px solid #F1F5F9",
        width="100%", max_width="720px",
    )


def resumen_lateral() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.text("Resumen del Pedido", font_weight="700", color=DARK, font_size="1rem"),
                rx.divider(border_color="#E2E8F0"),
                rx.cond(
                    AppState.oferta_seleccionada != {},
                    rx.vstack(
                        rx.hstack(rx.text("Destino", color=GRAY, font_size="0.85rem"), rx.spacer(),
                                  rx.text(AppState.oferta_seleccionada["destino"],
                                          font_weight="600", color=DARK, font_size="0.85rem"), width="100%"),
                        rx.hstack(rx.text("Duración", color=GRAY, font_size="0.85rem"), rx.spacer(),
                                  rx.text(f"{AppState.oferta_seleccionada['duracion_dias']} días",
                                          font_weight="600", color=DARK, font_size="0.85rem"), width="100%"),
                        rx.hstack(rx.text("Precio/persona", color=GRAY, font_size="0.85rem"), rx.spacer(),
                                  rx.text(f"${AppState.oferta_seleccionada['precio']:.0f} USD",
                                          font_weight="600", color=DARK, font_size="0.85rem"), width="100%"),
                        rx.divider(border_color="#E2E8F0"),
                        rx.hstack(rx.text("Total estimado", font_weight="700", color=DARK), rx.spacer(),
                                  rx.text(f"${AppState.oferta_seleccionada['precio']:.0f}+ USD",
                                          font_weight="800", color=TEAL, font_size="1.1rem"), width="100%"),
                        align_items="flex-start", spacing="3", width="100%",
                    ),
                    rx.text("Selecciona un destino para ver el resumen.", color=GRAY, font_size="0.85rem"),
                ),
                align_items="flex-start", spacing="3", width="100%",
            ),
            background="white", border_radius="12px", padding="24px",
            box_shadow="0 4px 20px rgba(0,0,0,0.07)", border="1px solid #E2E8F0", width="100%",
        ),
        rx.box(
            rx.vstack(
                rx.text("🛡️ Reserva Segura", font_weight="700", color=DARK, font_size="0.9rem"),
                rx.text("• Cancelación gratuita hasta 48h antes", color=GRAY, font_size="0.82rem"),
                rx.text("• Sin cargos ocultos", color=GRAY, font_size="0.82rem"),
                rx.text("• Soporte 24/7 incluido", color=GRAY, font_size="0.82rem"),
                rx.text("• Seguro de viaje incluido", color=GRAY, font_size="0.82rem"),
                align_items="flex-start", spacing="2",
            ),
            background=f"{TEAL}08", border_radius="12px", padding="20px",
            border=f"1px solid {TEAL}20", width="100%",
        ),
        spacing="4", width="100%", position="sticky", top="100px",
    )


def reservas_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.box(
            rx.vstack(
                rx.text("Reserva tu Aventura", font_size="2.2rem", font_weight="900",
                        color="white", text_align="center"),
                rx.text("Completa el formulario y nuestro equipo se encargará del resto.",
                        color="#94A3B8", text_align="center"),
                align_items="center", spacing="2",
            ),
            background=f"linear-gradient(135deg, {DARK}, #1E293B)",
            padding="64px 24px", width="100%", text_align="center",
        ),
        rx.box(
            rx.hstack(
                formulario_reserva(),
                rx.box(resumen_lateral(),
                       display=rx.breakpoints({"base": "none", "lg": "block"}),
                       width="320px", flex_shrink="0"),
                align_items="flex-start", spacing="8", width="100%",
                max_width="1100px", margin="0 auto",
            ),
            padding=rx.breakpoints({"base": "32px 16px", "md": "48px 24px"}),
            width="100%", background=LIGHT_BG,
        ),
        footer(),
        spacing="0", width="100%", overflow_x="hidden",
    )
