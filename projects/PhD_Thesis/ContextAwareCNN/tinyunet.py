import sys

sys.path.append('../../../')

from pycore.blocks import to_head
from pycore.blocks import to_cor
from pycore.blocks import to_begin
from pycore.blocks import to_end
from pycore.blocks import to_generate

from pycore.blocks import to_input
from pycore.blocks import to_ConvConvRelu
from pycore.blocks import block_2ConvPool
from pycore.blocks import to_connection
from pycore.blocks import block_Upscale2Conv
from pycore.blocks import to_skip
from pycore.blocks import to_ConvSoftMax

arch = [
    to_head('../../..'),
    to_cor(),
    to_begin(),

    # input
    *to_input('Class5_0978.PNG', width=6.5, height=6.5, name="net_in"),

    *block_2ConvPool(
        name='b1',
        connect_in=None,
        connect_out='pool_b1',
        output_size=512,
        n_filters=32,
        offset="(-1.5,0,0)",
        size=(32, 32, 2.5),
        opacity=0.5
    ),
    *block_2ConvPool(
        name='b2',
        connect_in='pool_b1',
        connect_out='pool_b2',
        output_size=256,
        n_filters=32,
        offset="(2,0,0)",
        size=(22, 22, 2.5),
        opacity=0.5
    ),
    *block_2ConvPool(
        name='b3',
        connect_in='pool_b2',
        connect_out='pool_b3',
        output_size=128,
        n_filters=64,
        offset="(2,0,0)",
        size=(15, 15, 3.5),
        opacity=0.5
    ),
    *block_2ConvPool(
        name='b4',
        connect_in='pool_b3',
        connect_out='pool_b4',
        output_size=64,
        n_filters=128,
        offset="(1.5,0,0)",
        size=(10, 10, 4.5),
        opacity=0.5
    ),

    # Bottleneck
    # block-005
    to_ConvConvRelu(
        name='ccr_b5',
        output_size=32,
        n_filters=(256, 256),
        offset="(1.5,0,0)",
        to="(pool_b4-east)",
        width=(7, 7),
        height=7,
        depth=8,
        caption="Bottleneck"
    ),
    to_connection("pool_b4", "ccr_b5"),

    # Decoder
    *block_Upscale2Conv(
        name="b6",
        connect_in="ccr_b5",
        output_size=64,
        n_filters=512,
        offset="(1.5,0,0)",
        size=(10, 10, 5.0),
        opacity=0.5
    ),
    to_skip(of='ccr_b4', to='concat_b6', pos=1.25),
    *block_Upscale2Conv(
        name="b7",
        connect_in="ccr_b6",
        output_size=128,
        n_filters=256,
        offset="(2,0,0)",
        size=(15, 15, 4.5),
        opacity=0.5
    ),
    to_skip(of='ccr_b3', to='concat_b7', pos=1.25),
    *block_Upscale2Conv(
        name="b8",
        connect_in="ccr_b7",
        output_size=256,
        n_filters=128,
        offset="(2.5,0,0)",
        size=(22, 22, 3.5),
        opacity=0.5
    ),
    to_skip(of='ccr_b2', to='concat_b8', pos=1.25),
    *block_Upscale2Conv(
        name="b9",
        connect_in="ccr_b8",
        output_size=512,
        n_filters=64,
        offset="(3,0,0)",
        size=(32, 32, 2.5),
        opacity=0.5
    ),
    to_skip(of='ccr_b1', to='concat_b9', pos=1.25),
    to_ConvSoftMax(
        name="soft1",
        output_size=512,
        n_channels=1,
        offset="(2,0,0)",
        to="(ccr_b9-east)",
        width=1,
        height=32,
        depth=32,
        caption="Sigmoid"
    ),
    to_connection("ccr_b9", "soft1"),
    to_end()
]

if __name__ == '__main__':
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')
