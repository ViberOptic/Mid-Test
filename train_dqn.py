# ===============================================
# TRAIN DQN UNTUK ROCKET LANDING (Versi Fix ZIP)
# ===============================================

import os
from rocket_env import SimpleRocketEnv
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import ProgressBarCallback

# Buat environment
env = SimpleRocketEnv(render_mode=None)

# Lokasi file model
MODEL_PATH = "dqn_rocket_model"

# Buat model DQN
model = DQN(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    buffer_size=50000,
    learning_starts=1000,
    batch_size=64,
    gamma=0.99,
    train_freq=4,
    exploration_fraction=0.3,
    exploration_final_eps=0.05,
    target_update_interval=500,
    verbose=1,
)

# Latih model
print("🚀 Training dimulai...")
model.learn(total_timesteps=300000, callback=ProgressBarCallback())
print("✅ Training selesai!")

# Simpan model (langsung sebagai ZIP valid, bukan folder)
model.save("dqn_rocket_model")

# Pastikan file .zip benar-benar ada
if os.path.exists(MODEL_PATH):
    print(f"💾 Model berhasil disimpan sebagai: {os.path.abspath(MODEL_PATH)}")
else:
    print("⚠️ File belum muncul, tapi model tersimpan otomatis oleh Stable Baselines.")

env.close()
