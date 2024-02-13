import foillib as fl
import matplotlib.pyplot as plt


LW = 1
COLOR = "b"

# --- NACA 4-SERIES ("0012") --------------------------------------------------+

fig, ax = plt.subplots(figsize=(10, 5))
x, y = fl.naca("0012")
plt.plot(x, y, c=COLOR, lw=LW)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.axis("off")
plt.savefig("naca0012.png", dpi=100, bbox_inches="tight")


# --- NACA 4-SERIES ("2312") --------------------------------------------------+

fig, ax = plt.subplots(figsize=(10, 5))
x, y = fl.naca("2312", finite_te=False)
plt.plot(x, y, c=COLOR, lw=LW)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.axis("off")
plt.savefig("naca2312.png", dpi=100, bbox_inches="tight")


# --- NACA 5-SERIES ("24012") -------------------------------------------------+

fig, ax = plt.subplots(figsize=(10, 5))
x, y = fl.naca("24012")
plt.plot(x, y, c=COLOR, lw=LW)
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.axis("off")
plt.savefig("naca24012.png", dpi=100, bbox_inches="tight")


# --- BEZIER (CAMBERED) -------------------------------------------------------+

cps_top = [(0.19, 0.17), (0.5, 0.2), (0.81, 0.1)]
cps_bot = [(0.085, -0.02), (0.3, 0.06), (0.6, 0.08)]
cps_le = [0.05, 0.02]

x, y = fl.bezier(cps_le, cps_top, cps_bot)
fig, ax = plt.subplots(figsize=(10, 5))
plt.plot(x, y, c=COLOR, lw=LW)

# plot control points for top surface
x_cp, y_cp = list(zip(*cps_top))
x_cp = [0] + list(x_cp) + [1]
y_cp = [cps_le[0]] + list(y_cp) + [0.00252 / 2]
plt.plot(
    x_cp,
    y_cp,
    marker="o",
    c="k",
    zorder=5,
    linewidth=1,
    fillstyle="none",
    markersize=8,
    markeredgecolor="r",
)

# plot control points for bottom surface
x_cp, y_cp = list(zip(*cps_bot))
x_cp = [0] + list(x_cp) + [1]
y_cp = [-cps_le[1]] + list(y_cp) + [-0.00252 / 2]
plt.plot(
    x_cp,
    y_cp,
    marker="o",
    c="k",
    zorder=5,
    linewidth=1,
    fillstyle="none",
    markersize=8,
    markeredgecolor="r",
)

ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.axis("off")
plt.savefig("bezier_cambered.png", dpi=100, bbox_inches="tight")


# --- BEZIER (SYMMETRIC) ------------------------------------------------------+

cps_top = [(0.19, 0.17), (0.5, 0.2), (0.81, 0.1)]
cps_le = [0.05]

fig, ax = plt.subplots(figsize=(14, 5))
x, y = fl.bezier(cps_le, cps_top)
plt.plot(x, y, c=COLOR, linewidth=LW)

x_cp, y_cp = list(zip(*cps_top))
x_cp = [0] + list(x_cp) + [1]
y_cp = [cps_le[0]] + list(y_cp) + [0.00252 / 2]
plt.plot(
    x_cp,
    y_cp,
    marker="o",
    c="k",
    zorder=5,
    linewidth=1,
    fillstyle="none",
    markersize=8,
    markeredgecolor="r",
)

ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.axis("off")
plt.savefig("bezier_symmetric.png", dpi=100, bbox_inches="tight")
