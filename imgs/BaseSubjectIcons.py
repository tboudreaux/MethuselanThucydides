###################################################
# This Python script is intended to be run from   #
# Inkscape's Simple Inkscape Scripting extension. #
###################################################

# Prepare the canvas.
#canvas.true_width = 40637.48031
#canvas.true_height = 1935.11811
#canvas.viewbox = [0.0, 0.0, 10752.0, 512.0]

# Generate an image.

from functools import wraps
filter8481 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter8481.add('GaussianBlur', stdDeviation=10.08207)
filter5795 = filter_effect(pt1=(-0.19066744, -0.48239441), pt2=(1.19066746, 1.48239439), color_interpolation_filters='sRGB')
filter5795.add('GaussianBlur', stdDeviation=29.145129)
filter4218 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter4218.add('GaussianBlur', stdDeviation=10.08207)
filter3676 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter3676.add('GaussianBlur', stdDeviation=15.68454)
filter3434 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter3434.add('GaussianBlur', stdDeviation=10.08207)
filter6121 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter6121.add('GaussianBlur', stdDeviation=15.68454)
filter6165 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter6165.add('GaussianBlur', stdDeviation=10.08207)
filter1438 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter1438.add('GaussianBlur', stdDeviation=15.68454)
filter3779 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter3779.add('GaussianBlur', stdDeviation=10.08207)
filter6445 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter6445.add('GaussianBlur', stdDeviation=15.68454)
filter2531 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter2531.add('GaussianBlur', stdDeviation=10.08207)
filter5899 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter5899.add('GaussianBlur', stdDeviation=15.68454)
filter9017 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter9017.add('GaussianBlur', stdDeviation=10.08207)
filter6264 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter6264.add('GaussianBlur', stdDeviation=15.68454)
filter8035 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter8035.add('GaussianBlur', stdDeviation=10.08207)
filter4703 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter4703.add('GaussianBlur', stdDeviation=15.68454)
filter3243 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter3243.add('GaussianBlur', stdDeviation=10.08207)
filter5605 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter5605.add('GaussianBlur', stdDeviation=15.68454)
filter7857 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter7857.add('GaussianBlur', stdDeviation=10.08207)
filter7227 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter7227.add('GaussianBlur', stdDeviation=15.68454)
filter1656 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter1656.add('GaussianBlur', stdDeviation=10.08207)
filter4838 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter4838.add('GaussianBlur', stdDeviation=15.68454)
filter4231 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter4231.add('GaussianBlur', stdDeviation=10.08207)
filter3655 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter3655.add('GaussianBlur', stdDeviation=15.68454)
filter65 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter65.add('GaussianBlur', stdDeviation=10.08207)
filter6380 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter6380.add('GaussianBlur', stdDeviation=15.68454)
filter7138 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter7138.add('GaussianBlur', stdDeviation=10.08207)
filter7596 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter7596.add('GaussianBlur', stdDeviation=15.68454)
filter2445 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter2445.add('GaussianBlur', stdDeviation=10.08207)
filter3567 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter3567.add('GaussianBlur', stdDeviation=15.68454)
filter9646 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter9646.add('GaussianBlur', stdDeviation=10.08207)
filter6491 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter6491.add('GaussianBlur', stdDeviation=15.68454)
filter3049 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter3049.add('GaussianBlur', stdDeviation=10.08207)
filter7203 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter7203.add('GaussianBlur', stdDeviation=15.68454)
filter7135 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter7135.add('GaussianBlur', stdDeviation=10.08207)
filter9992 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter9992.add('GaussianBlur', stdDeviation=15.68454)
filter3486 = filter_effect(pt1=(-0.05247186, -0.05247186), pt2=(1.05247184, 1.05247184), color_interpolation_filters='sRGB')
filter3486.add('GaussianBlur', stdDeviation=10.08207)
filter4279 = filter_effect(pt1=(-0.10260827, -0.25960202), pt2=(1.10260823, 1.25960198), color_interpolation_filters='sRGB')
filter4279.add('GaussianBlur', stdDeviation=15.68454)


params = {
"CSParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,160.15225, 284.90002,0.96726, 1.03385,'163.786px',160.15225, 284.90002,filter8481,filter5795],
"econParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,157.26285, 267.39825,0.948189, 1.05464,'98.8728px',157.26285, 267.39825,filter4218,filter3676],
"mathParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,136.37579, 269.43484,0.948189, 1.05464,'98.8728px',136.37579, 269.43484,filter3434,filter6121],
"astro_phParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,34.380787, 269.18494,0.948188, 1.05464,'98.8729px',34.380787, 269.18494,filter6165,filter1438],
"cond_matParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,34.380787, 269.18494,0.948188, 1.05464,'98.8729px',34.380787, 269.18494,filter3779,filter6445],
"nlinParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,147.06921, 270.43329,0.948189, 1.05464,'98.8728px',147.06921, 270.43329,filter4231,filter3655],
"physics_2Params" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,64.433762, 268.09824,0.948189, 1.05464,'98.8728px',64.433762, 268.09824,filter2445,filter3567],
"physics_3Params" : [254.76788, 254.76788,222.75264, 232.09076,0.53925, 1.85443,'278.719px',70.186707, 181.0031,437.046967, 326.00542,59.605301, 267.86227,0.948189, 1.05464,'98.8728px',59.605301, 267.86227,filter2445,filter3567],
"physics_4Params" : [254.76788, 254.76788,281.71262, 189.69679,0.440495, 2.27017,'229.989px',70.186707, 181.0031,437.046967, 326.00542,65.055626, 261.50784,0.948189, 1.05464,'98.8728px',65.055626, 261.50784,filter2445,filter3567],
"q_bioParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,130.13608, 269.12042,0.948189, 1.05464,'98.8728px',130.13608, 269.12042,filter3049,filter7203],
"q_finParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,117.90282, 269.93576,0.948189, 1.05464,'98.8728px',117.90282, 269.93576,filter7135,filter9992],
"statParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,144.68654, 270.80042,0.948189, 1.05464,'98.8728px',144.68654, 270.80042,filter3486,filter4279],
"gr_qcParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,33.460213, 260.39926,0.865128, 1.1559,'172.327px',33.460213, 260.39926,filter2531,filter5899],
"hep_exParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,35.360924, 251.31998,0.833397, 1.19991,'150.046px',35.360924, 251.31998, filter9017, filter6264],
"hep_latParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,39.442825, 235.54845,0.794067, 1.25934,'134.173px',39.442825, 235.54845, filter8035, filter4703],
"hep_phParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,35.184444, 253.74739,0.840662, 1.18954,'147.457px',35.184444, 253.74739,filter3243, filter5605],
"hep_thParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,34.568581, 258.71524,0.849227, 1.17754,'148.58px',34.568581, 258.71524,filter7857,filter7227],
"math_phParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,40.520992, 233.57677,0.786743, 1.27106,'137.104px',40.520992, 233.57677,filter1656,filter4838],
"nucl_exParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,31.128134, 247.33807,0.791745, 1.26303,'136.623px',31.128134, 247.33807,filter65,filter6380],
"nucl_thParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,37.973347, 251.40446,0.820707, 1.21846,'131.709px',37.973347, 251.40446,filter7138,filter7596],
"quant_phParams" : [254.76788, 254.76788,181.7791, 280.55972,0.651867, 1.53406,'355.1px',70.186707, 181.0031,437.046967, 326.00542,34.380787, 269.18494,0.948188, 1.05464,'98.8729px',34.380787, 269.18494,filter9646,filter6491]
}


def make_2_set_icon(params, shortName, longName):
    circle310 = circle((params[0], params[1]), 230.57091, stroke='none', fill='#5873a7', opacity=1, mix_blend_mode='normal', fill_opacity=1, filter=params[18])
    text314 = text('', (params[2], params[3]), transform=f'scale({params[4]}, {params[5]})', font_size=params[6], line_height=1.25, font_family='Space Mono', _inkscape_font_specification='Space Mono', fill='#000000', stroke='none', stroke_width=2.66325)
    text314.add_text(shortName, (params[2], params[3]), font_style='normal', font_variant='normal', font_weight='normal', font_stretch='normal', font_family='Fira Mono for Powerline', _inkscape_font_specification='Fira Mono for Powerline', fill='#ffffff', fill_opacity=1, stroke='none', stroke_width=2.66325)
    rect316 = rect((params[7], params[8]), (params[9], params[10]), stroke='none', fill='#5873a7', opacity=1, mix_blend_mode='normal', fill_opacity=1, filter=params[19])
    text320 = text(longName, (params[11], params[12]), transform=f'scale({params[13]}, {params[14]})', font_size=params[15], line_height=1.25, font_family='Space Mono', _inkscape_font_specification='Space Mono', fill='#000000', stroke='none', stroke_width=1.22839)
    text320.add_text('cs', (params[16], params[17]), font_style='normal', font_variant='normal', font_weight='normal', font_stretch='normal', font_family='Fira Mono for Powerline', _inkscape_font_specification='Fira Mono for Powerline', fill='#ffffff', fill_opacity=1, stroke='none', stroke_width=1.22839)
    icon = group([circle310, text314, rect316, text320], fill='#000000', stroke='none')

    return icon


for name, param in params.items():
    icon = make_2_set_icon(param, name[:3], name[4:])
    icon.translate(0, 0)
    icon.scale(0.5)

    




