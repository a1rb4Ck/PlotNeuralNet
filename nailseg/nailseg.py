import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *


NUM_CHANNELS = [32, 16, 24, 32, 64, 96, 160, 320]
NUM_BOTTLENECK = [1, 1, 2, 3, 4, 3, 3, 1]
STRIDES = [2, 1, 2, 2, 2, 1, 1, 1]
DILATIONS = [1, 1, 1, 1, 1, 1, 2, 2]

STRIDES_HIGH = [2, 1, 2, 2]


lowres_blocks = []
res = 448
total_stride = 2
downsample = to_Pool(name='low_downsample',
                     offset="(0,0,0)",
                     to="(0,0,0)",
                     width=1,
                     height=40,
                     depth=40,
                     opacity=0.5,
                     caption="Down x2")
lowres_blocks.append(downsample)
lowres = res//2
for i, (c, n, s, d) in enumerate(zip(NUM_CHANNELS, NUM_BOTTLENECK, STRIDES, DILATIONS)):
    block = to_Conv(name=f'low_stg{i}',
                    s_filer=lowres,
                    n_filer=c,
                    offset='(1,0,0)',
                    to='(low_downsample-east)' if i == 0 else f'(low_stg{i - 1}-east)',
                    width=round(c/16),
                    height=40/total_stride,
                    depth=40/total_stride,
                    caption=" ")
    lowres //= s
    total_stride *= s
    lowres_blocks.append(block)
    if i > 0:
        to_conn = to_connection(f'low_stg{i - 1}', f'low_stg{i}')
    else:
        to_conn = to_connection('low_downsample', f'low_stg{i}')
        input_conn = r"""
        \draw [connection]  (-3,0,0)    -- node {\midarrow} (low_downsample-west);
        """
        lowres_blocks.append(input_conn)
    lowres_blocks.append(to_conn)


highres_blocks = []
total_stride = 1
for i, (c, n, s, d) in enumerate(zip(NUM_CHANNELS, NUM_BOTTLENECK, STRIDES_HIGH, DILATIONS)):
    block = to_Conv(name=f'high_stg{i}',
                    s_filer=res,
                    n_filer=c,
                    offset="(0,-6,0)" if i == 0 else '(1,0,0)',
                    to="(low_downsample-south)" if i == 0 else f'(high_stg{i - 1}-east)',
                    width=round(c/16),
                    height=40/total_stride,
                    depth=40/total_stride,
                    caption=" ")
    res //= s
    total_stride *= s
    highres_blocks.append(block)
    if i > 0:
        to_conn = to_connection(f'high_stg{i - 1}', f'high_stg{i}')
        highres_blocks.append(to_conn)
    if i == 0:
        input_conn = r"""
        \draw [connection]  (-3,0,0)    -- node {\midarrow} (-3,-10,0);
        """
        highres_blocks.append(input_conn)
        input_conn = r"""
        \draw [connection]  (-3,-10,0)    -- node {\midarrow} (0,-10,0);
        """
        highres_blocks.append(input_conn)


decoder_blocks = []
c7_up = to_Pool(name='c7_up',
                offset="(0,-3,0)",
                to="(low_stg7-south)",
                width=1,
                height=40/16,
                depth=40/16,
                opacity=0.5,
                caption="Up x2")
decoder_blocks.append(c7_up)
corner = r"""
\node[inner sep=0pt] (corner_c7_up) at (low_stg7-east) [yshift=-3.1cm] {};
"""
decoder_blocks.append(corner)
to_conn = r"""
\draw [connection]  (low_stg7-east)    -- node {\midarrow} (corner_c7_up) -- node {\midarrow} (c7_up-east);
"""
decoder_blocks.append(to_conn)

corner = r"""
\node[inner sep=0pt] (corner_c3_proj) at (low_stg3-east) [yshift=-3.1cm] {};
"""
decoder_blocks.append(corner)
f1_16 = to_Box(name='f1_16',
               offset="(3,0,0)",
               to="(corner_c3_proj)",
               width=40/16,
               height=40/16,
               depth=40/16,
               caption="Fusion 0")
decoder_blocks.append(f1_16)
to_conn = r"""
\draw [connection]  (low_stg3-east)    -- node {\midarrow} (corner_c3_proj) -- node {\midarrow} (f1_16-west);
"""
decoder_blocks.append(to_conn)
to_conn = r"""
\draw [connection]  (c7_up-west)    -- node {\midarrow} (f1_16-east);
"""
decoder_blocks.append(to_conn)

f1_16_up = to_Pool(name='f1_16_up',
                   offset="(-0.5,-3,0)",
                   to="(f1_16-south)",
                   width=40/8,
                   height=1,
                   depth=40/8,
                   opacity=0.5,
                   caption="Up x2")
decoder_blocks.append(f1_16_up)


f1_8 = to_Box(name='f1_8',
              offset="(3.9,0,0)",
              to="(high_stg3-east)",
              width=40/8,
              height=40/8,
              depth=40/8,
              caption="Fusion 1")
decoder_blocks.append(f1_8)

to_conn = r"""
\draw [connection]  (f1_16-south)    -- node {\midarrow} (f1_16_up-north);
"""
decoder_blocks.append(to_conn)
to_conn = r"""
\draw [connection]  (f1_16_up-south)    -- node {\midarrow} (f1_8-north);
"""
decoder_blocks.append(to_conn)
to_conn = r"""
\draw [connection]  (high_stg3-east)    -- node {\midarrow} (f1_8-west);
"""
decoder_blocks.append(to_conn)

out_pool = to_Pool(name='out_pool',
                   offset="(3,0,0)",
                   to="(f1_8-east)",
                   width=1,
                   height=40,
                   depth=40,
                   opacity=0.5,
                   caption="Up x8")
decoder_blocks.append(out_pool)
to_conn = r"""
\draw [connection]  (f1_8-east)    -- node {\midarrow} (out_pool-west);
"""
decoder_blocks.append(to_conn)
pathfile = '/home/bduke/work/nails-presentation/polished_after.png'
output = r"""
\node[canvas is zy plane at x=4] (temp) at (out_pool-east) {\includegraphics[width=8cm,height=8cm]{"""+ pathfile +"""}};
"""
decoder_blocks.append(output)
to_conn = r"""
\draw [connection]  (out_pool-east)    -- node {\midarrow} (temp);
"""
decoder_blocks.append(to_conn)


arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    #input
    to_input('/home/bduke/work/nails-presentation/polished_before.png'),

    #block-001
    *lowres_blocks,

    *highres_blocks,
    *decoder_blocks,

    to_end()
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
