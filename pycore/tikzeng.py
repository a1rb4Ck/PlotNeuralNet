import os


def to_head(projectpath):
    pathlayers = os.path.join(projectpath, 'layers/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone}
\usepackage{import}
\subimport{""" + pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image
"""


def to_cor():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\ConcatColor{rgb:blue,1;red,1;white,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:pink,5;white,1}
"""


def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
"""


# layers definition


def to_input(pathfile, to='(-3,0,0)', width=8, height=8, name="net_in"):
    return r"""
\node[canvas is zy plane at x=0] (""" + name + """) at """ + to + """
    {\includegraphics[
        width=""" + str(width) + "cm" + """,
        height=""" + str(height) + "cm" + """
    ]{""" + pathfile + """}};
"""


# Conv
def to_Conv(
    name, output_size=256, n_filters=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "
):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """
    {Box={
        name=""" + name + """,
        caption=""" + caption + r""",
        xlabel={{""" + str(n_filters) + """, }},
        zlabel=""" + str(output_size) + """,
        fill=\ConvColor,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu(
    name,
    output_size=256,
    n_filters=(64, 64),
    offset="(0,0,0)",
    to="(0,0,0)",
    width=(2, 2),
    height=40,
    depth=40,
    caption=" "
):
    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """
    {RightBandedBox={
        name=""" + name + """,
        caption=""" + caption + """,
        xlabel={{ """ + str(n_filters[0]) + """, """ + str(n_filters[1]) + """ }},
        zlabel=""" + str(output_size) + """,
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height=""" + str(height) + """,
        width={ """ + str(width[0]) + """ , """ + str(width[1]) + """ },
        depth=""" + str(depth) + """
        }
    };
"""


# Pool
def to_Pool(
    name,
    output_size=256,
    n_filters=64,
    offset="(0,0,0)",
    to="(0,0,0)",
    width=1,
    height=32,
    depth=32,
    opacity=0.5,
    caption=" "
):
    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """
    {Box={
        name=""" + name + """,
        caption=""" + caption + r""",
        fill=\PoolColor,
        opacity=""" + str(opacity) + """,
        xlabel={{""" + str(n_filters) + """, }},
        zlabel=""" + str(output_size) + """,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


# unpool
def to_UnPool(
    name,
    n_filters,
    offset="(0,0,0)",
    to="(0,0,0)",
    output_size=256,
    width=1,
    height=32,
    depth=32,
    opacity=0.5,
    caption=" "
):
    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """
    {Box={
        name=""" + name + r""",
        caption=""" + caption + r""",
        fill=\UnpoolColor,
        opacity=""" + str(opacity) + """,
        xlabel={{""" + str(n_filters) + """, }},
        zlabel=""" + str(output_size) + """,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


# concat
def to_Concat(
    name,
    n_filters,
    offset="(0,0,0)",
    to="(0,0,0)",
    output_size=256,
    width=1,
    height=32,
    depth=32,
    opacity=0.5,
    caption=" "
):
    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """
    {Box={
        name=""" + name + r""",
        caption=""" + caption + r""",
        fill=\ConcatColor,
        opacity=""" + str(opacity) + """,
        xlabel={{""" + str(n_filters) + """, }},
        zlabel=""" + str(output_size) + """,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


def to_ConvRes(
    name,
    output_size=256,
    n_filters=64,
    offset="(0,0,0)",
    to="(0,0,0)",
    width=6,
    height=40,
    depth=40,
    opacity=0.2,
    caption=" "
):
    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """
    {RightBandedBox={
        name=""" + name + """,
        caption=""" + caption + """,
        xlabel={{ """ + str(n_filters) + """, }},
        zlabel=""" + str(output_size) + r""",
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity=""" + str(opacity) + """,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


# ConvSoftMax
def to_ConvSoftMax(
    name, output_size=40, n_channels=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "
):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """
    {Box={
        name=""" + name + """,
        caption=""" + caption + """,
        xlabel={{ """ + str(n_channels) + """, }},
        zlabel=""" + str(output_size) + """,
        fill=\SoftmaxColor,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


# SoftMax
def to_SoftMax(
    name, output_size=10, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8, caption=" "
):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """
    {Box={
        name=""" + name + """,
        caption=""" + caption + """,
        xlabel={{" ","dummy"}},
        zlabel=""" + str(output_size) + """,
        fill=\SoftmaxColor,
        opacity=""" + str(opacity) + """,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""


def to_connection(of, to):
    return r"""
\draw [connection]  (""" + of + """-east)    -- node {\midarrow} (""" + to + """-west);
"""


def to_skip(of, to, pos=1.25):
    return r"""
\path (""" + of + """-southeast) -- (""" + of + """-northeast) coordinate[pos=""" + str(pos) + """] (""" + of + """-top) ;
\path (""" + to + """-south)  -- (""" + to + """-north)  coordinate[pos=""" + str(
        pos
    ) + """] (""" + to + """-top) ;
\draw [copyconnection]  (""" + of + """-northeast)
-- node {\copymidarrow}(""" + of + """-top)
-- node {\copymidarrow}(""" + to + """-top)
-- node {\copymidarrow} (""" + to + """-north);
"""


def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""


def to_generate(arch, pathname="file.tex"):
    with open(pathname, "w") as f:
        for c in arch:
            f.write(c)
