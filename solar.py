import numpy as np
import math
import plotly.graph_objects as go


def spheres(size, clr, dist=0):
    # Set up 100 points. First, do angles
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)

    # Set up coordinates for points on the sphere
    x0 = dist + size * np.outer(np.cos(theta), np.sin(phi))
    y0 = size * np.outer(np.sin(theta), np.sin(phi))
    z0 = size * np.outer(np.ones(100), np.cos(phi))

    # Set up trace without colorscale
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, clr], [1, clr]], showscale=False, opacity=0.9, surfacecolor=np.full(x0.shape, 1))
    return trace


def orbits(dist, offset=0, clr='white', wdth=2):
    # Initialize empty lists for each set of coordinates
    xcrd = []
    ycrd = []
    zcrd = []

    # Calculate coordinates
    for i in range(0, 361):
        xcrd.append((round(np.cos(math.radians(i)), 5)) * dist + offset)
        ycrd.append((round(np.sin(math.radians(i)), 5)) * dist)
        zcrd.append(0)

    trace = go.Scatter3d(x=xcrd, y=ycrd, z=zcrd, marker=dict(size=0.1), line=dict(color=clr, width=wdth))
    return trace


def annot(xcrd, zcrd, txt, xancr='center'):
    strng = dict(showarrow=False, x=xcrd,
                 y=0, z=zcrd, text=txt,
                 xanchor=xancr, font=dict(color='white', size=14))
    return strng


diameter_km = [200000, 4878, 12104, 12756, 6787, 142796, 120660, 51118, 48600]
diameter = [((i / 12756) * 2) for i in diameter_km]
distance_from_sun = [0, 57.9, 108.2, 149.6, 227.9, 778.6, 1433.5, 2872.5, 4495.1]

# Create spheres for the Sun and planets with more distinct colors
trace0 = spheres(diameter[0], '#ffcc00', distance_from_sun[0])  # Sun
trace1 = spheres(diameter[1], '#7f7f7f', distance_from_sun[1])  # Mercury
trace2 = spheres(diameter[2], '#ff8c00', distance_from_sun[2])  # Venus
trace3 = spheres(diameter[3], '#00bfff', distance_from_sun[3])  # Earth
trace4 = spheres(diameter[4], '#ff4500', distance_from_sun[4])  # Mars
trace5 = spheres(diameter[5], '#ffffe0', distance_from_sun[5])  # Jupiter
trace6 = spheres(diameter[6], '#e3c6a2', distance_from_sun[6])  # Saturn
trace7 = spheres(diameter[7], '#00ffff', distance_from_sun[7])  # Uranus
trace8 = spheres(diameter[8], '#8a2be2', distance_from_sun[8])  # Neptune

# Set up orbit traces with lighter colors
trace11 = orbits(distance_from_sun[1], clr='lightgray')  # Mercury
trace12 = orbits(distance_from_sun[2], clr='lightyellow')  # Venus
trace13 = orbits(distance_from_sun[3], clr='lightblue')  # Earth
trace14 = orbits(distance_from_sun[4], clr='lightcoral')  # Mars
trace15 = orbits(distance_from_sun[5], clr='lightgoldenrodyellow')  # Jupiter
trace16 = orbits(distance_from_sun[6], clr='lightyellow')  # Saturn
trace17 = orbits(distance_from_sun[7], clr='lightcyan')  # Uranus
trace18 = orbits(distance_from_sun[8], clr='plum')  # Neptune

# Use the same to draw a few rings for Saturn
trace21 = orbits(23, distance_from_sun[6], '#d2b48c', 3)
trace22 = orbits(24, distance_from_sun[6], '#d2b48c', 3)
trace23 = orbits(25, distance_from_sun[6], '#d2b48c', 3)
trace24 = orbits(26, distance_from_sun[6], '#d2b48c', 3)
trace25 = orbits(27, distance_from_sun[6], '#d2b48c', 3)
trace26 = orbits(28, distance_from_sun[6], '#d2b48c', 3)

layout = go.Layout(title='Solar System', showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
                   scene=dict(xaxis=dict(title='Distance from the Sun',
                                         titlefont_color='white',
                                         range=[-7000, 7000],
                                         backgroundcolor='black',
                                         color='white',
                                         gridcolor='gray'),
                              yaxis=dict(title='Distance from the Sun',
                                         titlefont_color='white',
                                         range=[-7000, 7000],
                                         backgroundcolor='black',
                                         color='white',
                                         gridcolor='gray'),
                              zaxis=dict(title='',
                                         range=[-7000, 7000],
                                         backgroundcolor='black',
                                         color='white',
                                         gridcolor='gray'),
                              annotations=[annot(distance_from_sun[0], 40, 'Sun', xancr='left'),
                                           annot(distance_from_sun[1], 5, 'Mercury'),
                                           annot(distance_from_sun[2], 9, 'Venus'),
                                           annot(distance_from_sun[3], 9, 'Earth'),
                                           annot(distance_from_sun[4], 7, 'Mars'),
                                           annot(distance_from_sun[5], 30, 'Jupiter'),
                                           annot(distance_from_sun[6], 28, 'Saturn'),
                                           annot(distance_from_sun[7], 20, 'Uranus'),
                                           annot(distance_from_sun[8], 20, 'Neptune')]
                              ))

# Set up the figure with improved data
fig = go.Figure(data=[trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8,
                      trace11, trace12, trace13, trace14, trace15, trace16, trace17, trace18,
                      trace21, trace22, trace23, trace24, trace25, trace26],
                layout=layout)

# Show the figure
fig.show()
