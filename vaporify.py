from PIL import Image, ImageFilter, ImageDraw
import cv2

EDGE_OPACITY = 70  # 35  # PERCENT (0 = Transparent)
EDGE_ALPHA = round(255 * (EDGE_OPACITY / 100))
GRADIENT_OPACITY = 45  # PERCENT (0 = Transparent)
GRADIENT_ALPHA = round(255 * (GRADIENT_OPACITY / 100))


def interpolate(f_co, t_co, interval):
    det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]


def apply_gradient(base, f_co, t_co):
    gradient = Image.new("RGBA", base.size, color=0)
    draw = ImageDraw.Draw(gradient)

    for i, color in enumerate(interpolate(f_co, t_co, base.width * 2)):
        draw.line([(i, 0), (0, i)], tuple(color), width=1)

    return Image.alpha_composite(base.convert("RGBA"), gradient)


def apply_edges(base, layers):
    baseEdgeLayer = base.copy().filter(ImageFilter.EDGE_ENHANCE).convert("RGBA")

    edges = [baseEdgeLayer.copy() for x in layers]

    for i in range(len(layers)):
        data = edges[i].getdata()
        newData = []
        for val in data:
            if val[:3] < (150, 150, 150):
                newData.append((0, 0, 0, 0))
                continue
            newData.append(layers[i])

        edges[i].putdata(newData)
    return edges


def apply_filter(file_location):
    base = Image.open(file_location)

    gradient_layer = apply_gradient(
        base,
        (148, 25, 255, GRADIENT_ALPHA),
        (255, 113, 206, GRADIENT_ALPHA),
    )

    edge_layers = apply_edges(base, [
        (255, 113, 206, EDGE_ALPHA),
        (1, 205, 254, EDGE_ALPHA),
        (5, 255, 161, EDGE_ALPHA)
    ])

    base.paste(gradient_layer)
    for i in range(len(edge_layers)):
        base.paste(edge_layers[i], (-2 * i, -2 * i), edge_layers[i])

    base.show()


def exec():
    pass


exec()

# apply_filter("./images/pre/night_watch.png")
# apply_filter("./images/pre/mona_lisa.png")
apply_filter("./images/pre/creation_of_adam.png")
