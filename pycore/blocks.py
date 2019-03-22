from pycore.tikzeng import *


def block_2ConvPool(
    name, connect_in, connect_out, output_size=256, n_filters=64, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5
):
    if output_size > 500:
        pool_offset = 1.5
    elif output_size > 200:
        pool_offset = 1.3
    elif output_size > 100:
        pool_offset = 1.20
    else:
        pool_offset = 0.95

    block = [
        to_ConvConvRelu(
            name="ccr_{}".format(name),
            output_size=str(output_size),
            n_filters=(n_filters, n_filters),
            offset=offset,
            to="({}-east)".format(connect_in) if connect_in is not None and connect_in != "None" else "(0,0,0)",
            width=(size[2], size[2]),
            height=size[0],
            depth=size[1],
        ),
        to_Pool(
            name="{}".format(connect_out),
            output_size=int(output_size / 2),
            n_filters=n_filters,
            offset="(%s,0,0)" % pool_offset,
            to="(ccr_{}-east)".format(name),
            width=size[2],
            height=int(size[0] * .7),
            depth=int(size[1] * .7),
            opacity=opacity,
        ),
        to_connection("ccr_{}".format(name), "{}".format(connect_out)),
    ]

    if connect_in is not None:
        block.append(to_connection("{}".format(connect_in), "ccr_{}".format(name)))

    return block


def block_Upscale2Conv(
    name, connect_in, output_size=256, n_filters=64, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5
):

    if output_size < 100:
        conv_offset = "(0.95,0,0)"
    elif output_size < 200:
        conv_offset = "(1.3,0,0)"
    elif output_size < 500:
        conv_offset = "(1.5,0,0)"
    else:
        conv_offset = "(1.7,0,0)"

    return [
        to_UnPool(
            name='unpool_{}'.format(name),
            n_filters=str(n_filters),
            output_size=str(output_size),
            offset=offset,
            to="({}-east)".format(connect_in),
            width=1,
            height=size[0],
            depth=size[1],
            opacity=opacity
        ),
        to_Concat(
            name='concat_{}'.format(name),
            n_filters=n_filters,
            output_size=str(output_size),
            offset=conv_offset,
            to="(unpool_{}-east)".format(name),
            width=size[2],
            height=size[0],
            depth=size[1],
            opacity=0.5,
        ),
        to_ConvConvRelu(
            name="ccr_{}".format(name),
            output_size=str(output_size),
            n_filters=(n_filters, n_filters),
            offset=conv_offset,
            to="(concat_{}-east)".format(name),
            width=(size[2], size[2]),
            height=size[0],
            depth=size[1],
        ),
        to_connection("{}".format(connect_in), "unpool_{}".format(name)),
        to_connection("unpool_{}".format(name), "concat_{}".format(name)),
        to_connection("unpool_{}".format(name), "ccr_{}".format(name)),
    ]


def block_Unconv(
    name, connect_in, connect_out, output_size=256, n_filters=64, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5
):
    return [
        to_UnPool(
            name='unpool_{}'.format(name),
            n_filters=str(n_filters),
            offset=offset,
            to="({}-east)".format(connect_in),
            output_size=str(output_size),
            width=1,
            height=size[0],
            depth=size[1],
            opacity=opacity
        ),
        to_ConvRes(
            name='ccr_res_{}'.format(name),
            offset="(0,0,0)",
            to="(unpool_{}-east)".format(name),
            output_size=str(output_size),
            n_filters=str(n_filters),
            width=size[2],
            height=size[0],
            depth=size[1],
            opacity=opacity
        ),
        to_Conv(
            name='ccr_{}'.format(name),
            offset="(0,0,0)",
            to="(ccr_res_{}-east)".format(name),
            output_size=str(output_size),
            n_filters=str(n_filters),
            width=size[2],
            height=size[0],
            depth=size[1]
        ),
        to_ConvRes(
            name='ccr_res_c_{}'.format(name),
            offset="(0,0,0)",
            to="(ccr_{}-east)".format(name),
            output_size=str(output_size),
            n_filters=str(n_filters),
            width=size[2],
            height=size[0],
            depth=size[1],
            opacity=opacity
        ),
        to_Conv(
            name='{}'.format(connect_out),
            offset="(0,0,0)",
            to="(ccr_res_c_{}-east)".format(name),
            output_size=str(output_size),
            n_filters=str(n_filters),
            width=size[2],
            height=size[0],
            depth=size[1]
        ),
        to_connection("{}".format(connect_in), "unpool_{}".format(name))
    ]


def block_Res(
    num,
    name,
    connect_in,
    connect_out,
    output_size=256,
    n_filters=64,
    offset="(0,0,0)",
    size=(32, 32, 3.5),
    opacity=0.5
):
    lys = []
    layers = [*['{}_{}'.format(name, i) for i in range(num - 1)], top]
    for name in layers:
        ly = [
            to_Conv(
                name='{}'.format(name),
                offset=offset,
                to="({}-east)".format(connect_in),
                output_size=str(output_size),
                n_filters=str(n_filters),
                width=size[2],
                height=size[0],
                depth=size[1]
            ),
            to_connection("{}".format(connect_in), "{}".format(name))
        ]
        connect_in = name
        lys += ly

    lys += [
        to_skip(of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys
