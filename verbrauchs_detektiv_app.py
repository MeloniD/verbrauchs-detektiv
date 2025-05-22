
import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Verbrauchs-Detektiv", layout="centered")
st.title("🕵️ Verbrauchs-Detektiv")
st.write("Lade zwei Bilder hoch: ein Vorher- und ein Nachherbild deiner Essenskiste. Der Detektiv vergleicht den Verbrauch automatisch und berechnet den Wert in CHF.")

vorher = st.file_uploader("Vorher-Bild", type=["jpg", "jpeg", "png"], key="before")
nachher = st.file_uploader("Nachher-Bild", type=["jpg", "jpeg", "png"], key="after")

preise = {
    "Brötli": 1.50,
    "Gipfeli": 1.40
}

lower_brot = np.array([10, 50, 50])
upper_brot = np.array([25, 255, 255])
lower_gipfeli = np.array([20, 100, 100])
upper_gipfeli = np.array([35, 255, 255])

def count_items(image_np, lower_color, upper_color):
    hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)

if vorher and nachher:
    before_image = Image.open(vorher).convert("RGB")
    after_image = Image.open(nachher).convert("RGB")

    before_np = np.array(before_image)
    after_np = np.array(after_image.resize(before_image.size))

    broetli_before = count_items(before_np, lower_brot, upper_brot)
    broetli_after = count_items(after_np, lower_brot, upper_brot)
    gipfeli_before = count_items(before_np, lower_gipfeli, upper_gipfeli)
    gipfeli_after = count_items(after_np, lower_gipfeli, upper_gipfeli)

    broetli_diff = broetli_before - broetli_after
    gipfeli_diff = gipfeli_before - gipfeli_after

    total = 0.0
    st.subheader("🍽️ Verbrauch")

    if broetli_diff > 0:
        betrag = broetli_diff * preise["Brötli"]
        total += betrag
        st.write(f"- {broetli_diff} Brötli → {betrag:.2f} CHF")
    if gipfeli_diff > 0:
        betrag = gipfeli_diff * preise["Gipfeli"]
        total += betrag
        st.write(f"- {gipfeli_diff} Gipfeli → {betrag:.2f} CHF")

    st.markdown(f"**Total: {total:.2f} CHF**")

    if broetli_diff <= 0 and gipfeli_diff <= 0:
        st.info("Kein Verbrauch festgestellt oder mehr Produkte im Nachher-Bild als im Vorher-Bild.")
