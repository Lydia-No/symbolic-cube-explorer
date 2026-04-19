import plotly.graph_objects as go

VERTICES = {
    0: (0, 0, 0),
    1: (1, 0, 0),
    2: (0, 1, 0),
    3: (1, 1, 0),
    4: (0, 0, 1),
    5: (1, 0, 1),
    6: (0, 1, 1),
    7: (1, 1, 1),
}

EDGES = [
    (0, 1), (0, 2), (0, 4),
    (1, 3), (1, 5),
    (2, 3), (2, 6),
    (3, 7),
    (4, 5), (4, 6),
    (5, 7),
    (6, 7),
]


def plot_cube_walk(path, title="Cube Walk"):
    fig = go.Figure()

    for e in EDGES:
        x = [VERTICES[e[0]][0], VERTICES[e[1]][0]]
        y = [VERTICES[e[0]][1], VERTICES[e[1]][1]]
        z = [VERTICES[e[0]][2], VERTICES[e[1]][2]]

        fig.add_trace(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="lines",
                name=f"edge-{e[0]}-{e[1]}",
                showlegend=False,
            )
        )

    px = [VERTICES[v][0] for v in path]
    py = [VERTICES[v][1] for v in path]
    pz = [VERTICES[v][2] for v in path]

    fig.add_trace(
        go.Scatter3d(
            x=px,
            y=py,
            z=pz,
            mode="lines+markers+text",
            text=[str(v) for v in path],
            textposition="top center",
            name="walk",
        )
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )

    return fig
