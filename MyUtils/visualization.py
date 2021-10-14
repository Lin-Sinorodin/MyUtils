import matplotlib.pyplot as plt


class SetPlotOptions:
    def __init__(self):
        self._restore_default_options()
        self._use_latex_if_available()
        self._set_plot_style()

    @staticmethod
    def _restore_default_options():
        """Restore Matplotlib default rc parameters"""
        plt.rcParams.update(plt.rcParamsDefault)

    @staticmethod
    def _use_latex_if_available():
        """Source: https://stackoverflow.com/a/40895025"""
        from distutils.spawn import find_executable
        if find_executable('latex'):
            plt.matplotlib.rc('text', usetex=True)

    @staticmethod
    def _set_plot_style():
        plt.matplotlib.rc('figure', figsize=(9, 5))
        plt.matplotlib.rc('grid', linestyle='dashed', linewidth=1, alpha=0.25)
        plt.matplotlib.rc('font', family='serif', size=12)
        plt.matplotlib.rc('legend', fontsize=12)

        # Change ticks
        plt.rcParams['xtick.major.size'] = 7.0
        plt.rcParams['xtick.minor.size'] = 3.0
        plt.rcParams['xtick.direction'] = 'inout'
        plt.rcParams['ytick.major.size'] = 7.0
        plt.rcParams['ytick.minor.size'] = 3.0
        plt.rcParams['ytick.direction'] = 'inout'
