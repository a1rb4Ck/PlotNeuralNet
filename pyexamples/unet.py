import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    #input
    to_input('../examples/fcn8s/cats.jpg'),

    #block-001
    to_ConvConvRelu(
        name='ccr_b1',
        output_size=500,
        n_filters=(64, 64),
        offset="(0,0,0)",
        to="(0,0,0)",
        width=(2, 2),
        height=40,
        depth=40
    ),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),
    *block_2ConvPool(
        name='b2',
        connect_in='pool_b1',
        connect_out='pool_b2',
        output_size=256,
        n_filters=128,
        offset="(1,0,0)",
        size=(32, 32, 3.5),
        opacity=0.5
    ),
    *block_2ConvPool(
        name='b3',
        connect_in='pool_b2',
        connect_out='pool_b3',
        output_size=128,
        n_filters=256,
        offset="(1,0,0)",
        size=(25, 25, 4.5),
        opacity=0.5
    ),
    *block_2ConvPool(
        name='b4',
        connect_in='pool_b3',
        connect_out='pool_b4',
        output_size=64,
        n_filters=512,
        offset="(1,0,0)",
        size=(16, 16, 5.5),
        opacity=0.5
    ),

    #Bottleneck
    #block-005
    to_ConvConvRelu(
        name='ccr_b5',
        output_size=32,
        n_filters=(1024, 1024),
        offset="(2,0,0)",
        to="(pool_b4-east)",
        width=(8, 8),
        height=8,
        depth=8,
        caption="Bottleneck"
    ),
    to_connection("pool_b4", "ccr_b5"),

    #Decoder
    *block_Unconv(
        name="b6",
        connect_in="ccr_b5",
        connect_out='end_b6',
        output_size=64,
        n_filters=512,
        offset="(2.1,0,0)",
        size=(16, 16, 5.0),
        opacity=0.5
    ),
    to_skip(of='ccr_b4', to='ccr_res_b6', pos=1.25),
    *block_Unconv(
        name="b7",
        connect_in="end_b6",
        connect_out='end_b7',
        output_size=128,
        n_filters=256,
        offset="(2.1,0,0)",
        size=(25, 25, 4.5),
        opacity=0.5
    ),
    to_skip(of='ccr_b3', to='ccr_res_b7', pos=1.25),
    *block_Unconv(
        name="b8",
        connect_in="end_b7",
        connect_out='end_b8',
        output_size=256,
        n_filters=128,
        offset="(2.1,0,0)",
        size=(32, 32, 3.5),
        opacity=0.5
    ),
    to_skip(of='ccr_b2', to='ccr_res_b8', pos=1.25),
    *block_Unconv(
        name="b9",
        connect_in="end_b8",
        connect_out='end_b9',
        output_size=512,
        n_filters=64,
        offset="(2.1,0,0)",
        size=(40, 40, 2.5),
        opacity=0.5
    ),
    to_skip(of='ccr_b1', to='ccr_res_b9', pos=1.25),
    to_ConvSoftMax(
        name="soft1",
        output_size=512,
        offset="(0.75,0,0)",
        to="(end_b9-east)",
        width=1,
        height=40,
        depth=40,
        caption="SOFT"
    ),
    to_connection("end_b9", "soft1"),
    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
