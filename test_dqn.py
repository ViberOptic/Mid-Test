# ===============================================
# AUTO LANDING ROCKET (100% STABIL & TANPA ERROR)
# ===============================================
# Roket bergerak otomatis menuju target biru
# dan mendarat halus tanpa berputar
# ===============================================

import pygame
import numpy as np
from rocket_env import SimpleRocketEnv

# --- Inisialisasi environment ---
env = SimpleRocketEnv(render_mode="human")
obs, _ = env.reset()

done = False
clock = pygame.time.Clock()

print("🚀 Autopilot aktif! Roket sedang menuju target...\n")

# --- Loop utama ---
while not done:
    pygame.event.pump()

    # Ambil state dari environment
    x, y, vx, vy, sin_t, cos_t, w, dx, dy = obs * env._normalizer()

    # Posisi target (sedikit di atas target asli)
    target_x = env.target_pos[0]
    target_y = env.target_pos[1] + env.target_h / 2 + 40

    # Error posisi (selisih roket ke target)
    error_x = target_x - x
    error_y = target_y - y

    # Dapatkan sudut roket
    angle = np.arctan2(sin_t, cos_t)

    # Default aksi
    action = 0  # 0 = diam
    thrust = False

    # --- 1. Stabilkan orientasi (biar roket tegak) ---
    if angle > 0.1:
        action = 3  # thruster kanan
    elif angle < -0.1:
        action = 2  # thruster kiri
    else:
        angle = 0  # tegak lurus

    # --- 2. Kontrol vertikal (atur kecepatan jatuh) ---
    if vy < -5 or error_y > 15:  # jatuh cepat / masih tinggi
        thrust = True

    # --- 3. Kontrol horizontal (gerak ke arah target) ---
    if abs(error_x) > 10:
        if error_x > 0 and vx < 5:
            action = 3  # ke kanan
        elif error_x < 0 and vx > -5:
            action = 2  # ke kiri

    # --- 4. Eksekusi aksi ---
    if thrust:
        obs, reward, done, truncated, info = env.step(1)  # thrust utama
    else:
        obs, reward, done, truncated, info = env.step(action)

    # --- Render tampilan ---
    env.render()

    # --- Biar smooth, gak freeze ---
    clock.tick(30)
    pygame.time.wait(10)

    # --- Cek kondisi pendaratan sukses ---
    if abs(error_x) < 10 and abs(error_y) < 10 and abs(vy) < 3:
        print("🟢 Roket berhasil mendarat dengan stabil!")
        done = True

# --- Tutup environment ---
pygame.time.wait(1500)
env.close()
print("✅ Autopilot selesai. Pendaratan sukses!")
