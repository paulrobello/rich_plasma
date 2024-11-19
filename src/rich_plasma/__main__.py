import math
import time
import os

from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()
console.clear()

colors = ["#000000", "#000077", "#0000ff", "#0077ff", "#00ffff", "#ffffff"]
minus_colors = ["#000000", "#770000", "#ff0000", "#ff0777", "#ff00ff", "#ffffff"]
values = " ▝▞▟▟█"


def txy(t: float, x: float, y: float)-> float:
    t *= 2e-3
    x *= 0.5 * (0.5 + 0.25 * math.sin(t * 0.01))
    y *= 0.5 * (0.5 + 0.25 * math.sin(t * 0.01))

    n1 = 0.6 + 0.4 * math.sin(x * 0.2) * math.cos(y * 0.2)

    return (
        n1
        * math.sin(x * 0.7 + t - math.sin(y + t * 0.1 + math.cos(x + t * 1e-3)))
        * math.cos(y * 0.5 + t + math.sin(x + t * 0.1 - math.cos(y + t)))
    )


def paint(t: float) -> Text:
    height = os.get_terminal_size().lines
    width = os.get_terminal_size().columns
    result = Text()

    for y in range(height):
        for x in range(width):
            r = txy(t, x, y)
            v = min(len(values) - 1, max(0, int(abs(r) * len(values))))
            cv = minus_colors[v] if r < 0 else colors[v]
            result.append(values[v], style=cv)
        if y < height - 1:
            result.append("\n")
    return result

def main():
    t: float = 0
    with Live(paint(t), vertical_overflow="crop", auto_refresh=False) as live:
        for _ in range(600):
            t += 20
            time.sleep(1 / 30)
            live.update(paint(t))
            live.refresh()

if __name__ == "__main__":
    main()
