
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad


def f(x):
    return x ** 2

left_bound = 0
right_bound = 2

random_generator = np.random.default_rng(42)


def monte_carlo_integral(n, random_generator):
    max_height = f(right_bound)

    random_x = random_generator.uniform(left_bound, right_bound, n)
    random_y = random_generator.uniform(0, max_height, n)

    points_under_curve = np.sum(random_y <= f(random_x))

    rectangle_area = (right_bound - left_bound) * max_height

    return rectangle_area * points_under_curve / n



plot_points_count = 1000
max_height = f(right_bound)

plot_x = random_generator.uniform(left_bound, right_bound, plot_points_count)
plot_y = random_generator.uniform(0, max_height, plot_points_count)

under_curve = plot_y <= f(plot_x)

x = np.linspace(-0.5, 2.5, 400)

fig, ax = plt.subplots(figsize=(7, 5))

ax.plot(x, f(x), "r", linewidth=2)

integration_x = np.linspace(left_bound, right_bound)
ax.fill_between(integration_x, f(integration_x), color="gray", alpha=0.3)

ax.scatter(plot_x[under_curve], plot_y[under_curve],
           s=6, color="green", label="під кривою")

ax.scatter(plot_x[~under_curve], plot_y[~under_curve],
           s=6, color="blue", label="над кривою")

ax.set_xlim([x[0], x[-1]])
ax.set_ylim([0, max(f(x)) + 0.1])

ax.set_xlabel("x")
ax.set_ylabel("f(x)")

ax.axvline(x=left_bound, color="gray", linestyle="--")
ax.axvline(x=right_bound, color="gray", linestyle="--")

ax.set_title(f"Monte Carlo method for f(x) = x^2 on [{left_bound}, {right_bound}]")
ax.legend()
ax.grid()

plt.savefig("monte_carlo_plot.png", dpi=120)



exact_integral = (right_bound ** 3 - left_bound ** 3) / 3
quad_value, quad_error = quad(f, left_bound, right_bound)


print("\nКількість точок | Монте-Карло | Абсолютна похибка | Відносна похибка")

for n in [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]:
    mc_integral = monte_carlo_integral(n, random_generator)
    absolute_error = abs(mc_integral - exact_integral)
    relative_error = absolute_error / exact_integral * 100

    print(f"{n} | {mc_integral:.6f} | {absolute_error:.6f} | {relative_error:.4f}%")


print("\nКількість точок | Середнє значення | Стандартне відхилення")

for n in [100, 1_000, 10_000, 100_000]:
    results = np.array([monte_carlo_integral(n, random_generator) for _ in range(200)])
    print(f"{n} | {results.mean():.5f} | {results.std():.5f}")
