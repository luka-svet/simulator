# Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance
#
# Copyright 2018-2019 Pedro HC David <https://github.com/Kronopt> and SimulATe contributors
# Copyright 2019-2023 Luka Svet <luka.svet@kuleuven.be>
#
# The following code is a derivative work of the code from the Mercurial project,
# which is licensed under GPLv3. This code therefore is also licensed under the terms
# of the GNU General Public License, version 3.


def xy_max_resize(plot, graph_widget, axis_type="linear"):

    def resize_x(which_widget):
        which_widget.xmax += 10
        which_widget.x_ticks_major += 1

    def resize_y_linear(which_widget):
        which_widget.ymax += 20
        which_widget.y_ticks_major += 4

    def resize_y_log(which_widget):
        which_widget.ymax *= 10

    def lambda_func(_plot, _graph_widget, _axis_type):
        # x-axis
        # x represents time, and, in this case, is always linear
        if _plot.points[-1][0] > _graph_widget.xmax:
            resize_x(_graph_widget)

        # y-axis
        if _axis_type == "linear":
            if _plot.points[-1][1] > _graph_widget.ymax:
                resize_y_linear(_graph_widget)
        elif _axis_type == "log":
            if _plot.points[-1][1] > _graph_widget.ymax:
                resize_y_log(_graph_widget)

    return lambda _: lambda_func(plot, graph_widget, axis_type)
