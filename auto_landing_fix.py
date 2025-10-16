import pygame
import math
from rocket_env import SimpleRocketEnv

env = SimpleRocketEnv(render_mode="human")
obs, _ = env.reset()
clock = pygame.time.Clock()

done = False
print("🚀 AUTOPILOT AKTIF — hanya thrust utama (no rotasi kanan/kiri besar)\n")

while not done:
    x, y, vx, vy, sin_t, cos_t, w, dx, dy = obs
    θ = math.atan2(sin_t, cos_t)  # orientasi roket
    
    # --- PARAMETER KONTROL ---
    target_x = dx
    target_y = dy
    Kp_x = 0.001     # gain kontrol horizontal (semakin kecil semakin lembut)
    Kp_y = 0.03      # gain kontrol vertikal
    Kp_angle = 1.5   # gain untuk menjaga vertikal
    
    # --- HITUNG ARAH HORIZONTAL ---
    desired_angle = -Kp_x * dx  # sedikit miring ke arah target
    
    # Batasi sudut maksimum agar tidak terlalu banting
    desired_angle = max(min(desired_angle, math.radians(10)), math.radians(-10))
    
    # Koreksi rotasi supaya roket tetap stabil
    angle_error = desired_angle - θ
    
    # --- PILIH AKSI ---
    # 0: no thrust, 1: main thrust, 2: left, 3: right
    action = 0  
    
    # Koreksi orientasi kecil saja
    if angle_error > 0.1:
        action = 3  # kanan
    elif angle_error < -0.1:
        action = 2  # kiri
    else:
        # Hanya thrust utama, sesuaikan kecepatan vertikal
        if vy < -10:   # jatuh terlalu cepat
            action = 1
        elif dy > 20:  # masih jauh di atas target
            action = 1
        else:
            action = 0
    
    # Jalankan langkah
    obs, reward, done, truncated, info = env.step(action)
    env.render()

    # Info autopilot
    print(f"AUTO | X={x:.1f} Y={y:.1f} Vx={vx:.1f} Vy={vy:.1f} θ={math.degrees(θ):.2f}", end="\r")

    clock.tick(60)

print("\n✅ Misi selesai — roket sudah mendarat (atau keluar layar).")
env.close()
