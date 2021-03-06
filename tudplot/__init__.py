import os

import numpy
import matplotlib as mpl
from matplotlib import pyplot
from cycler import cycler

from .xmgrace import export_to_agr, load_agr_data
from .tud import tudcolors, nominal_colors, sequential_colors
from .utils import facet_plot, CurvedText as curved_text


def activate(scheme='b', full=False, sequential=False, cmap='blue-red', **kwargs):
    """
    Activate the tud design.

    Args:
        scheme (opt.): Color scheme to activate, default is 'b'.
        full (opt.):
            Activate the full color palette. If False a smaller color palette is used.
            If a number N is given, N colors will be chosen based on a interpolation of
            all tudcolors.
        sequential (opt.): Activate a number of sequential colors from a color map.
        cmap (opt.):
            Colormap to use for sequential colors, can be either from `~tudplot.tud.cmaps`
            or any matplotlib color map. Range of the color map values can be given as
            cmap_min and cmap_max, respectively.
        **kwargs: Any matplotlib rc paramter may be given as keyword argument.
    """
    mpl.pyplot.style.use(os.path.join(os.path.dirname(__file__), 'tud.mplstyle'))

    if full:
        if isinstance(full, int):
            cmap = mpl.colors.LinearSegmentedColormap.from_list('tud{}'.format(scheme),
                                                                tudcolors[scheme])
            colors = [cmap(x) for x in numpy.linspace(0, 1, full)]
        else:
            colors = tudcolors[scheme]
    elif sequential:
        colors = sequential_colors(sequential, cmap=cmap, min=kwargs.pop('cmap_min', 0),
                                   max=kwargs.pop('cmap_max', 1))
    else:
        colors = nominal_colors[scheme]

    mpl.rcParams['axes.prop_cycle'] = cycler('color', colors)


def saveagr(filename, figure=None, convert_latex=True):
    """
    Save the current figure in xmgrace format.

    Args:
        filename: Agrfile to save the figure to
        figure (opt.):
            Figure that will be saved, if not given the current figure is saved
    """
    figure = figure or pyplot.gcf()
    export_to_agr(figure, filename, convert_latex=convert_latex)


def markfigure(x, y, s, ax=None, **kwargs):
    if ax is None:
        ax = pyplot.gca()
    kwargs['transform'] = ax.transAxes
    kwargs['ha'] = 'center'
    kwargs['va'] = 'center'
    # kwargs.setdefault('fontsize', 'large')
    ax.text(x, y, s, **kwargs)


def marka(x, y):
    markfigure(x, y, '(a)')


def markb(x, y):
    markfigure(x, y, '(b)')
