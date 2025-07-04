import numpy as np
import matplotlib.pyplot as plt

# Constants
T0 = 288.15
P0 = 101325
rho0 = 1.225
R = 287.05
g = 9.80665
L = -0.0065

def atmos(alt_ft):
    alt_m = alt_ft * 0.3048
    if alt_m <= 11000:
        T = T0 + L * alt_m
        P = P0 * (T / T0) ** (-g / (L * R))
    else:
        T = 216.65
        P = P0 * (216.65 / T0) ** (-g / (L * R)) * np.exp(-g * (alt_m - 11000) / (R * T))
    rho = P / (R * T)
    a = np.sqrt(1.4 * R * T)
    return rho, a

def ias_to_tas(ias_kt, rho):
    ias_mps = ias_kt * 0.51444
    tas_mps = ias_mps * np.sqrt(rho0 / rho)
    return tas_mps * 1.94384

# Define phases
alt_climb = np.arange(0, 30001, 1000)
alt_cruise = np.arange(30500, 39001, 1000)
alt_descent = np.arange(38500, -1, -1000)

phases = {
    "Climb": alt_climb,
    "Cruise": alt_cruise,
    "Descent": alt_descent
}

colors = {"Climb": "blue", "Cruise": "green", "Descent": "red"}
markers = {"Climb": "o", "Cruise": "^", "Descent": "s"}

# Data containers
tas_all = []
mach_all = []
alt_all = []
phase_all = []

for phase, altitudes in phases.items():
    for alt in altitudes:
        rho, a = atmos(alt)
        if phase == "Climb":
            ias = 290
            tas = ias_to_tas(ias, rho)
            mach = (tas * 0.51444) / a
        elif phase == "Cruise":
            mach = 0.78
            tas = mach * a * 1.94384
        else:  # Descent
            # mach = max(0.6, 0.78 - 0.00001 * (alt - 39000))
            # tas = mach * a * 1.94384
            # Better descent model
            ias = 230  # constant IAS during descent
            tas = ias_to_tas(ias, rho)
            mach = (tas * 0.51444) / a

        alt_all.append(alt)
        tas_all.append(tas)
        mach_all.append(mach)
        phase_all.append(phase)

# Plot
fig, ax1 = plt.subplots(figsize=(12, 6))

for phase in phases:
    indices = [i for i, p in enumerate(phase_all) if p == phase]
    alt = [alt_all[i] for i in indices]
    tas = [tas_all[i] for i in indices]
    ax1.plot(alt, tas, marker=markers[phase], color=colors[phase], linestyle='None',
             label=phase)

# Mach number line
ax2 = ax1.twinx()
ax2.plot(alt_all, mach_all, '--', color='gray', linewidth=2, label="Mach number")
ax2.set_ylabel("Mach number", fontsize=12, color='gray')
ax2.tick_params(axis='y', labelcolor='gray')

# Axis labels and title
ax1.set_xlabel("Altitude (ft)", fontsize=12)
ax1.set_ylabel("True Airspeed (kt)", fontsize=12)
ax1.set_title("A320 TAS and Mach vs Altitude — Phases with Markers", fontsize=14)
ax1.grid(True)

# Combined legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='blue',  label='Climb',   markersize=8),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='green', label='Cruise',  markersize=8),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='red',   label='Descent', markersize=8),
    Line2D([0], [0], color='gray', linestyle='--', label='Mach number')
]
ax1.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.show()




# ******************************************************
# FR version
# import numpy as np
# import matplotlib.pyplot as plt

# # Constants atmosphériques
# T0 = 288.15       # Température au sol (K)
# P0 = 101325       # Pression au sol (Pa)
# rho0 = 1.225      # Densité de l'air au sol (kg/m^3)
# R = 287.05        # Constante des gaz pour l'air (J/kg/K)
# g = 9.80665       # Gravité (m/s²)
# L = -0.0065       # Gradient thermique (K/m)

# def atmos(alt_ft):
#     """Retourne la densité et la vitesse du son à une altitude donnée en pieds"""
#     alt_m = alt_ft * 0.3048
#     if alt_m <= 11000:
#         T = T0 + L * alt_m
#         P = P0 * (T / T0) ** (-g / (L * R))
#     else:
#         T = 216.65
#         P = P0 * (216.65 / T0) ** (-g / (L * R)) * np.exp(-g * (alt_m - 11000) / (R * T))
#     rho = P / (R * T)
#     a = np.sqrt(1.4 * R * T)  # Vitesse du son
#     return rho, a

# def ias_to_tas(ias_kt, rho):
#     """Convertit IAS en TAS avec la densité actuelle"""
#     ias_mps = ias_kt * 0.51444
#     tas_mps = ias_mps * np.sqrt(rho0 / rho)
#     return tas_mps * 1.94384  # retourne TAS en kt

# # Génère les altitudes de 0 à 39 000 ft
# altitudes_ft = np.arange(0, 39001, 500)
# tas_list = []

# for alt in altitudes_ft:
#     rho, a = atmos(alt)

#     # Phase de montée : IAS constante
#     if alt < 30000:
#         ias = 290  # kt
#         tas = ias_to_tas(ias, rho)
#     # Croisière : Mach constant
#     elif 30000 <= alt <= 39000:
#         mach = 0.78
#         tas = mach * a * 1.94384  # converti m/s -> kt
#     tas_list.append(tas)

# # Affichage : Vitesse (Y) en fonction de l'altitude (X)
# plt.figure(figsize=(10, 6))
# plt.plot(altitudes_ft, tas_list, color='crimson', linewidth=2)
# plt.grid(True)
# plt.title("TAS (kt) de l'Airbus A320 en fonction de l'altitude (ft)", fontsize=14)
# plt.xlabel("Altitude (ft)", fontsize=12)
# plt.ylabel("Vitesse vraie TAS (kt)", fontsize=12)
# plt.tight_layout()
# plt.show()



# def atmos(alt_ft):
#     """Retourne la densité et la vitesse du son à une altitude donnée en pieds"""
#     alt_m = alt_ft * 0.3048
#     if alt_m <= 11000:
#         T = T0 + L * alt_m
#         P = P0 * (T / T0) ** (-g / (L * R))
#     else:
#         T = 216.65
#         P = P0 * (216.65 / T0) ** (-g / (L * R)) * np.exp(-g * (alt_m - 11000) / (R * T))
#     rho = P / (R * T)
#     a = np.sqrt(1.4 * R * T)  # Vitesse du son
#     return rho, a

# def ias_to_tas(ias_kt, rho):
#     """Convertit IAS en TAS avec la densité actuelle"""
#     ias_mps = ias_kt * 0.51444
#     tas_mps = ias_mps * np.sqrt(rho0 / rho)
#     return tas_mps * 1.94384  # retourne TAS en kt

# # Génère les altitudes de 0 à 39 000 ft
# altitudes_ft = np.arange(0, 40000, 500) #39001,
# tas_list = []

# for alt in altitudes_ft:
#     rho, a = atmos(alt)

#     # Phase de montée : IAS constante
#     if alt < 30000:
#         ias = 290  # kt
#         tas = ias_to_tas(ias, rho)
#     # Croisière : Mach constant
#     elif 30000 <= alt <= 39000:
#         mach = 0.78
#         tas = mach * a * 1.94384  # converti m/s -> kt
#     tas_list.append(tas)

# # Affichage du graphe
# plt.figure(figsize=(10, 6))
# # plt.plot(tas_list, altitudes_ft, color='blue', linewidth=2)
# plt.plot(tas_list, altitudes_ft, color='blue', linewidth=2)
# plt.gca().invert_yaxis()
# plt.grid(True)
# plt.title("Vitesse vraie (TAS) de l'Airbus A320 en fonction de l'altitude", fontsize=14)
# plt.xlabel("Vitesse vraie TAS (kt)", fontsize=12)
# plt.ylabel("Altitude (ft)", fontsize=12)
# plt.tight_layout()
# plt.show()

