# Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance
#
# Copyright 2018-2019 Pedro HC David <https://github.com/Kronopt> and SimulATe contributors
# Copyright 2019-2023 Luka Svet <luka.svet@kuleuven.be>
#
# The following code is a derivative work of the code from the Mercurial project,
# which is licensed under GPLv3. This code therefore is also licensed under the terms
# of the GNU General Public License, version 3.

from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')
Config.set("graphics", "minimum_height", 520)
Config.set("graphics", "minimum_width", 720)
Config.set("graphics", "multisamples",
           '0')  # Kivy not detecting OpenGL version bug
Config.set("input", "mouse", "mouse, disable_multitouch")

from kivy.core.window import Window

Window.minimum_height = 520
Window.minimum_width = 720

import csv
import datetime
import os
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ObjectProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
import bin.global_variables as global_variables
from bin.functions.equations import calculate_next_time_step
from bin.functions.helper_functions import XMLTextParser

kivy.require('1.9.1')


class ExponentButton(Spinner):
    pass


class OptionText(Label):
    pass


class SmallerSlider(Slider):
    pass


class TreatmentType(BoxLayout):

    def clear_treatment_widget(self):
        self.ids.treatment_options.clear_widgets()

    def reset_button_states(self):
        self.ids.toggle_classic.state = "normal"
        self.ids.toggle_adaptive.state = "normal"
        self.ids.toggle_user.state = "normal"


class DefaultValuesButton(Button):

    @staticmethod
    def default_values(app):

        # reset sliders to default
        app.root.ids.initial_density_s.value = app.default_parameters[
            "sensitive_initial_density_value"]
        app.root.ids.initial_density_s_BF.value = app.default_parameters[
            "sensitive_initial_density_BF_value"]
        app.root.ids.growth_rate_s.value = app.default_parameters[
            "sensitive_growth_rate"]
        app.root.ids.growth_rate_s_BF.value = app.default_parameters[
            "sensitive_growth_rate_BF"]
        app.root.ids.attachment_rate_s.value = app.default_parameters[
            "sensitive_attachment_rate"]
        app.root.ids.detachment_rate_s.value = app.default_parameters[
            "sensitive_detachment_rate"]
        app.root.ids.antimicrobial_inhibition_s.value = app.default_parameters[
            "sensitive_antimicrobial_inhibition"]
        app.root.ids.antimicrobial_inhibition_s_BF.value = app.default_parameters[
            "sensitive_antimicrobial_inhibition_BF"]
        app.root.ids.mutation_rate_s.value = app.default_parameters[
            "sensitive_mutation_rate_value"]
        app.root.ids.mutation_rate_s_BF.value = app.default_parameters[
            "sensitive_mutation_rate_BF_value"]
        app.root.ids.initial_density_r.value = app.default_parameters[
            "resistant_initial_density"]
        app.root.ids.initial_density_r_BF.value = app.default_parameters[
            "resistant_initial_density_BF"]
        app.root.ids.growth_rate_r.value = app.default_parameters[
            "resistant_growth_rate"]
        app.root.ids.growth_rate_r_BF.value = app.default_parameters[
            "resistant_growth_rate_BF"]
        app.root.ids.attachment_rate_r.value = app.default_parameters[
            "resistant_attachment_rate"]
        app.root.ids.detachment_rate_r.value = app.default_parameters[
            "resistant_detachment_rate"]
        app.root.ids.antimicrobial_inhibition_r.value = app.default_parameters[
            "resistant_antimicrobial_inhibition"]
        app.root.ids.antimicrobial_inhibition_r_BF.value = app.default_parameters[
            "resistant_antimicrobial_inhibition_BF"]
        app.root.ids.lymphocyte_inhibition.value = app.default_parameters[
            "lymphocyte_inhibition"]
        app.root.ids.natural_death.value = app.default_parameters[
            "natural_death"]
        app.root.ids.density_host_death.value = app.default_parameters[
            "host_death_density_value"]
        app.root.ids.growth_limitation_density.value = app.default_parameters[
            "growth_limitation_density_value"]
        app.root.ids.growth_limitation_density_BF.value = app.default_parameters[
            "growth_limitation_density_BF_value"]
        app.root.ids.initial_density_n.value = app.default_parameters[
            "initial_precursor_cell_density_value"]
        app.root.ids.proliferation_rate.value = app.default_parameters[
            "immune_cell_proliferation_rate"]
        app.root.ids.half_maximum_growth.value = app.default_parameters[
            "immune_cell_half_maximum_growth"]
        app.root.ids.effector_cells_decay.value = app.default_parameters[
            "effector_decay_rate"]
        app.root.ids.memory_cells_conversion.value = app.default_parameters[
            "memory_cell_conversion_rate"]
        app.root.ids.mean_concentration.value = app.default_parameters[
            "antimicrobial_mean_concentration_value"]

        # reset exponent button to default
        app.root.ids.growth_limitation_density_exponent_button.text = app.default_parameters[
            "growth_limitation_density_exponent"]
        app.root.ids.growth_limitation_density_exponent_button.values.insert(
            0, ' e15')  # refresh value to refresh button
        app.root.ids.growth_limitation_density_exponent_button.values.pop(0)

        # reset exponent button to default
        app.root.ids.growth_limitation_density_BF_exponent_button.text = app.default_parameters[
            "growth_limitation_density_BF_exponent"]
        app.root.ids.growth_limitation_density_BF_exponent_button.values.insert(
            0, ' e15')  # refresh value to refresh button
        app.root.ids.growth_limitation_density_BF_exponent_button.values.pop(0)

        # reset exponent button to default
        app.root.ids.density_host_death_exponent_button.text = app.default_parameters[
            "host_death_density_exponent"]
        app.root.ids.density_host_death_exponent_button.values.insert(
            0, ' e14')  # refresh value to refresh button
        app.root.ids.density_host_death_exponent_button.values.pop(0)

        # reset exponent button sensitive intial density to default
        app.root.ids.sensitive_microbes_initial_density_exponent_button.text = app.default_parameters[
            "sensitive_initial_density_exponent"]
        app.root.ids.sensitive_microbes_initial_density_exponent_button.values.insert(
            0, ' e00')  # refresh value to refresh button
        app.root.ids.sensitive_microbes_initial_density_exponent_button.values.pop(
            0)

        # reset exponent button sensitive intial density to default
        app.root.ids.sensitive_microbes_initial_density_BF_exponent_button.text = app.default_parameters[
            "sensitive_initial_density_BF_exponent"]
        app.root.ids.sensitive_microbes_initial_density_BF_exponent_button.values.insert(
            0, ' e00')  # refresh value to refresh button
        app.root.ids.sensitive_microbes_initial_density_BF_exponent_button.values.pop(
            0)

        # reset exponent button mutation rate to default
        app.root.ids.sensitive_microbes_mutation_rate_exponent_button.text = app.default_parameters[
            "sensitive_mutation_rate_exponent"]
        app.root.ids.sensitive_microbes_mutation_rate_exponent_button.values.insert(
            0, ' e00')  # refresh value to refresh button
        app.root.ids.sensitive_microbes_mutation_rate_exponent_button.values.pop(
            0)

        # reset exponent button mutation rate to default
        app.root.ids.sensitive_microbes_mutation_rate_BF_exponent_button.text = app.default_parameters[
            "sensitive_mutation_rate_BF_exponent"]
        app.root.ids.sensitive_microbes_mutation_rate_BF_exponent_button.values.insert(
            0, ' e00')  # refresh value to refresh button
        app.root.ids.sensitive_microbes_mutation_rate_BF_exponent_button.values.pop(
            0)

        # reset exponent button initial precursor cell density to default
        app.root.ids.immune_system_initial_density_exponent_button.text = app.default_parameters[
            "initial_precursor_cell_density_exponent"]
        app.root.ids.immune_system_initial_density_exponent_button.values.insert(
            0, ' e02')  # refresh value to refresh button
        app.root.ids.immune_system_initial_density_exponent_button.values.pop(
            0)

        # reset exponent button mean concentration to default
        app.root.ids.antimicrobial_mean_concentration_exponent_button.text = app.default_parameters[
            "antimicrobial_mean_concentration_exponent"]
        app.root.ids.antimicrobial_mean_concentration_exponent_button.values.insert(
            0, ' e00')  # refresh value to refresh button
        app.root.ids.antimicrobial_mean_concentration_exponent_button.values.pop(
            0)

        # clear treatment type widget to allow parameters to reset to default
        app.root.ids.treatment_toggles.clear_treatment_widget()
        app.root.ids.treatment_toggles.reset_button_states()
        app.treatment_type = ""


class GraphsLayout(BoxLayout):

    microbes_graph = ObjectProperty(None)
    antimicrobial_graph = ObjectProperty(None)

    ###################
    # Values Scenario
    ###################

    # simulation progress values
    simulation_going_scenario_property = BooleanProperty(False)
    pause_scenario_property = BooleanProperty(False)
    restart_in_progress_scenario_property = BooleanProperty(False)

    # current button values
    button_values_scenario = {
        "start_button.state": "normal",
        "start_button.disabled": False,
        "restart_button.disabled": True,
        "pause_button.disabled": True,
        "pause_button.pause_value": False
    }

    # all dicts together
    button_values = {"scenario": button_values_scenario}

    def __init__(self, **kwargs):
        super(GraphsLayout, self).__init__()

        # Microbiomes and AntimicrobialAssortments
        self.scenario_microbes = global_variables.MICROBES_ASSORTMENT
        self.scenario_antimicrobials = global_variables.ANTIMICROBIAL_ASSORTMENT

    def button_states(self, start_bt, pause_bt, restart_bt, new_scenario,
                      new_microbiome, app):

        current_scenario = app.current_scenario  # str
        current_microbiome = app.current_microbiome  # str

        # check if scenario or microbiome changed
        if current_scenario != new_scenario or current_microbiome != new_microbiome:

            load_button_values = self.button_values[new_scenario]

            # save current button configuration for current screen
            if current_scenario != "":
                # pause current simulation
                new_pause_value = pause_bt.pause_value
                if not pause_bt.disabled and not pause_bt.pause_value:
                    pause_bt.was_pressed = True
                    pause_bt.pause_value = True
                    new_pause_value = True

                save_button_values["start_button.state"] = start_bt.state
                save_button_values["start_button.disabled"] = start_bt.disabled
                save_button_values[
                    "restart_button.disabled"] = restart_bt.disabled
                save_button_values["pause_button.disabled"] = pause_bt.disabled
                save_button_values[
                    "pause_button.pause_value"] = new_pause_value

            # load stored button configuration for new screen
            start_bt.state = load_button_values["start_button.state"]
            start_bt.disabled = load_button_values["start_button.disabled"]
            restart_bt.disabled = load_button_values["restart_button.disabled"]
            pause_bt.disabled = load_button_values["pause_button.disabled"]
            pause_bt.pause_value = load_button_values[
                "pause_button.pause_value"]

            # update current scenario and microbiome
            app.current_scenario = "scenario"
            app.current_microbiome = ""

    def scenario_graph(self, scenario="scenario", enterotype=""):

        if scenario == "scenario":
            self.microbes_graph.clear_widgets()
            self.antimicrobial_graph.clear_widgets()

            self.microbes_graph.add_widget(
                self.scenario_microbes.get_graph_widget())
            self.antimicrobial_graph.add_widget(
                self.scenario_antimicrobials.get_graph_widget())

    def update_labels(self, labels, **kwargs):

        update_microbes_graph_scenario = False
        update_antimicrobial_graph_scenario = False

        if "x_axis" in labels:
            self.scenario_antimicrobials.get_graph_widget(
            ).xlabel = labels["x_axis"]
            update_antimicrobial_graph_scenario = True
        if "microbes_y_axis" in labels:
            self.scenario_microbes.get_graph_widget(
            ).ylabel = labels["microbes_y_axis"]
            update_microbes_graph_scenario = True
        if "antimicrobial_y_axis" in labels:
            self.scenario_antimicrobials.get_graph_widget(
            ).ylabel = labels["antimicrobial_y_axis"]
            update_antimicrobial_graph_scenario = True

        # had to access protected methods to update language...
        if update_microbes_graph_scenario:
            self.scenario_microbes.get_graph_widget()._update_labels()
        if update_antimicrobial_graph_scenario:
            self.scenario_antimicrobials.get_graph_widget()._update_labels()


class PopupWarning(Popup):

    warning_text = StringProperty()

    def show_message(self, title, warning_text):

        self.title = title
        self.warning_text = warning_text
        self.open()

        return True


class TreatmentToggle(ToggleButton):

    classic_treatment = Builder.load_file(
        os.path.join('bin', 'ui', 'treatment_classic.kv'))
    adaptive_treatment = Builder.load_file(
        os.path.join('bin', 'ui', 'treatment_adaptive.kv'))
    user_treatment = Builder.load_file(
        os.path.join('bin', 'ui', 'treatment_user.kv'))

    def selected_treatment(self, treatment, app):

        options_widget = None

        if treatment == "Classic":
            options_widget = TreatmentToggle.classic_treatment
            options_widget.language = self.language
            options_widget.delay_value = app.default_parameters[
                "classic_delay"]
            options_widget.duration_value = app.default_parameters[
                "classic_duration"]

        elif treatment == "Adaptive":
            options_widget = TreatmentToggle.adaptive_treatment
            options_widget.language = self.language
            options_widget.exponent_value = app.default_parameters[
                "adaptive_symptoms_at_microbes_density_exponent"]
            options_widget.slider_value = app.default_parameters[
                "adaptive_symptoms_at_microbes_density_value"]

        elif treatment == "User":
            options_widget = TreatmentToggle.user_treatment
            options_widget.language = self.language
            options_widget.active_value = app.default_parameters["user_supp"]

        options_widget.add_widget(Widget())

        return options_widget


# Main App
class Simulator(App):

    # current scenario/microbiome
    current_scenario = StringProperty("")
    current_microbiome = StringProperty("")
    # simulation speed
    simulation_speed = NumericProperty(1 / (24 * 5.0))  # 24*5 steps per day

    ######################
    # Scenario variables
    ######################

    # function instances
    clock_add_points = None
    data_generator_instance = None

    # plots
    sensitive_microbes_plot = global_variables.MICROBES_ASSORTMENT.get_microbes(
    )["Sensitive"].get_plot()
    resistant_microbes_plot = global_variables.MICROBES_ASSORTMENT.get_microbes(
    )["Resistant"].get_plot()
    sensitive_microbes_BF_plot = global_variables.MICROBES_ASSORTMENT.get_microbes(
    )["SensitiveBF"].get_plot()
    resistant_microbes_BF_plot = global_variables.MICROBES_ASSORTMENT.get_microbes(
    )["ResistantBF"].get_plot()
    total_microbes_plot = global_variables.MICROBES_ASSORTMENT.get_microbes(
    )["Total"].get_plot()
    antimicrobial_plot = global_variables.ANTIMICROBIAL_ASSORTMENT.get_antimicrobials(
    )["Generic Antimicrobial"].get_plot()
    immune_system_plot = global_variables.IMMUNE_PLOT
    death_limit = global_variables.DEATH_LIMIT
    growth_limit = global_variables.GROWTH_LIMIT
    growth_limit_BF = global_variables.GROWTH_LIMIT_BF

    # scenario default parameters
    default_parameters = {
        "sensitive_initial_density_value": 10.0,
        "sensitive_initial_density_exponent": ' e00',
        "sensitive_initial_density_BF_exponent": ' e00',
        "sensitive_initial_density_BF_value": 0.0,
        "sensitive_growth_rate": 3.3,
        "sensitive_growth_rate_BF": 1.5,
        "sensitive_attachment_rate": 0.03,
        "sensitive_detachment_rate": 0.0003,
        "sensitive_antimicrobial_inhibition": 1.0,
        "sensitive_antimicrobial_inhibition_BF": 0.8,
        "sensitive_mutation_rate_value": 0.001,
        "sensitive_mutation_rate_BF_value": 0.05,
        "sensitive_mutation_rate_exponent": ' e00',
        "sensitive_mutation_rate_BF_exponent": ' e00',
        "resistant_initial_density": 0.0,
        "resistant_initial_density_BF": 0.0,
        "resistant_growth_rate": 1.1,
        "resistant_growth_rate_BF": 0.5,
        "resistant_attachment_rate": 0.03,
        "resistant_detachment_rate": 0.0003,
        "resistant_antimicrobial_inhibition": 0.1,
        "resistant_antimicrobial_inhibition_BF": 0.08,
        "lymphocyte_inhibition": 10**-5,
        "natural_death": 0.03,
        "host_death_density_value": 1.0,
        "host_death_density_exponent": ' e10',
        "growth_limitation_density_value": 1.0,
        "growth_limitation_density_exponent": ' e10',
        "growth_limitation_density_BF_value": 1.0,
        "growth_limitation_density_BF_exponent": ' e10',
        "initial_precursor_cell_density_value": 2.0,
        "initial_precursor_cell_density_exponent": ' e02',
        "immune_cell_proliferation_rate": 2.0,
        "immune_cell_half_maximum_growth": 10**5,
        "effector_decay_rate": 0.35,
        "memory_cell_conversion_rate": 0.1,
        "antimicrobial_mean_concentration_value": 10.0,
        "antimicrobial_mean_concentration_exponent": ' e00',
        "classic_delay": 3.5,
        "classic_duration": 7.0,
        "adaptive_symptoms_at_microbes_density_value": 1.0,
        "adaptive_symptoms_at_microbes_density_exponent": ' e06',
        "user_supp": False
    }

    # sensitive microbes options
    sensitive_initial_density_value = NumericProperty(
        default_parameters["sensitive_initial_density_value"])
    sensitive_initial_density_exponent = NumericProperty(10**int(
        default_parameters["sensitive_initial_density_exponent"][-2:]))
    sensitive_initial_density = NumericProperty(
        default_parameters["sensitive_initial_density_value"] *
        10**int(default_parameters["sensitive_initial_density_exponent"][-2:]))
    sensitive_initial_density_BF_value = NumericProperty(
        default_parameters["sensitive_initial_density_BF_value"])
    sensitive_initial_density_BF_exponent = NumericProperty(10**int(
        default_parameters["sensitive_initial_density_BF_exponent"][-2:]))
    sensitive_initial_density_BF = NumericProperty(
        default_parameters["sensitive_initial_density_BF_value"] * 10**int(
            default_parameters["sensitive_initial_density_BF_exponent"][-2:]))
    sensitive_growth_rate = NumericProperty(
        default_parameters["sensitive_growth_rate"])
    sensitive_growth_rate_BF = NumericProperty(
        default_parameters["sensitive_growth_rate_BF"])
    sensitive_attachment_rate = NumericProperty(
        default_parameters["sensitive_attachment_rate"])
    sensitive_detachment_rate = NumericProperty(
        default_parameters["sensitive_detachment_rate"])
    sensitive_antimicrobial_inhibition = NumericProperty(
        default_parameters["sensitive_antimicrobial_inhibition"])
    sensitive_antimicrobial_inhibition_BF = NumericProperty(
        default_parameters["sensitive_antimicrobial_inhibition_BF"])
    sensitive_mutation_rate_value = NumericProperty(
        default_parameters["sensitive_mutation_rate_value"])
    sensitive_mutation_rate_exponent = NumericProperty(10**int(
        default_parameters["sensitive_mutation_rate_exponent"][-2:]))
    sensitive_mutation_rate = NumericProperty(
        default_parameters["sensitive_mutation_rate_value"] *
        10**int(default_parameters["sensitive_mutation_rate_exponent"][-2:]))
    sensitive_mutation_rate_BF_value = NumericProperty(
        default_parameters["sensitive_mutation_rate_BF_value"])
    sensitive_mutation_rate_BF_exponent = NumericProperty(10**int(
        default_parameters["sensitive_mutation_rate_BF_exponent"][-2:]))
    sensitive_mutation_rate_BF = NumericProperty(
        default_parameters["sensitive_mutation_rate_BF_value"] * 10**int(
            default_parameters["sensitive_mutation_rate_BF_exponent"][-2:]))

    # resistant microbes options
    resistant_initial_density = NumericProperty(
        default_parameters["resistant_initial_density"])
    resistant_initial_density_BF = NumericProperty(
        default_parameters["resistant_initial_density_BF"])
    resistant_growth_rate = NumericProperty(
        default_parameters["resistant_growth_rate"])
    resistant_growth_rate_BF = NumericProperty(
        default_parameters["resistant_growth_rate_BF"])
    resistant_attachment_rate = NumericProperty(
        default_parameters["resistant_attachment_rate"])
    resistant_detachment_rate = NumericProperty(
        default_parameters["resistant_detachment_rate"])
    resistant_antimicrobial_inhibition = NumericProperty(
        default_parameters["resistant_antimicrobial_inhibition"])
    resistant_antimicrobial_inhibition_BF = NumericProperty(
        default_parameters["resistant_antimicrobial_inhibition_BF"])

    # all microbes options
    lymphocyte_inhibition = NumericProperty(
        default_parameters["lymphocyte_inhibition"])
    natural_death = NumericProperty(default_parameters["natural_death"])
    host_death_density_value = NumericProperty(
        default_parameters["host_death_density_value"])
    host_death_density_exponent = NumericProperty(10**int(
        default_parameters["host_death_density_exponent"][-2:]))
    host_death_density = NumericProperty(
        default_parameters["host_death_density_value"] *
        10**int(default_parameters["host_death_density_exponent"][-2:]))
    growth_limitation_density_value = NumericProperty(
        default_parameters["growth_limitation_density_value"])
    growth_limitation_density_exponent = NumericProperty(10**int(
        default_parameters["growth_limitation_density_exponent"][-2:]))
    growth_limitation_density = NumericProperty(
        default_parameters["growth_limitation_density_value"] *
        10**int(default_parameters["growth_limitation_density_exponent"][-2:]))
    growth_limitation_density_BF_value = NumericProperty(
        default_parameters["growth_limitation_density_BF_value"])
    growth_limitation_density_BF_exponent = NumericProperty(10**int(
        default_parameters["growth_limitation_density_BF_exponent"][-2:]))
    growth_limitation_density_BF = NumericProperty(
        default_parameters["growth_limitation_density_BF_value"] * 10**int(
            default_parameters["growth_limitation_density_BF_exponent"][-2:]))

    # immune cell options
    initial_precursor_cell_density_value = NumericProperty(
        default_parameters["initial_precursor_cell_density_value"])
    initial_precursor_cell_density_exponent = NumericProperty(10**int(
        default_parameters["initial_precursor_cell_density_exponent"][-2:]))
    initial_precursor_cell_density = NumericProperty(
        default_parameters["initial_precursor_cell_density_value"] *
        10**int(default_parameters["initial_precursor_cell_density_exponent"]
                [-2:]))
    immune_cell_proliferation_rate = NumericProperty(
        default_parameters["immune_cell_proliferation_rate"])
    immune_cell_half_maximum_growth = NumericProperty(
        default_parameters["immune_cell_half_maximum_growth"])
    effector_decay_rate = NumericProperty(
        default_parameters["effector_decay_rate"])
    memory_cell_conversion_rate = NumericProperty(
        default_parameters["memory_cell_conversion_rate"])

    # antimicrobial option
    antimicrobial_mean_concentration_value = NumericProperty(
        default_parameters["antimicrobial_mean_concentration_value"])
    antimicrobial_mean_concentration_exponent = NumericProperty(10**int(
        default_parameters["antimicrobial_mean_concentration_exponent"][-2:]))
    antimicrobial_mean_concentration = NumericProperty(
        default_parameters["antimicrobial_mean_concentration_value"] *
        10**int(default_parameters["antimicrobial_mean_concentration_exponent"]
                [-2:]))

    # treatment types
    treatment_type = StringProperty("")

    # treatment options
    classic_delay = NumericProperty(default_parameters["classic_delay"])
    classic_duration = NumericProperty(default_parameters["classic_duration"])
    adaptive_symptoms_at_microbes_density_value = NumericProperty(
        default_parameters["adaptive_symptoms_at_microbes_density_value"])
    adaptive_symptoms_at_microbes_density_exponent = NumericProperty(10**int(
        default_parameters["adaptive_symptoms_at_microbes_density_exponent"]
        [-1:]))
    adaptive_symptoms_at_microbes_density = NumericProperty(
        default_parameters["adaptive_symptoms_at_microbes_density_value"] *
        10**int(default_parameters[
            "adaptive_symptoms_at_microbes_density_exponent"][-1:]))
    user_supp = BooleanProperty(default_parameters["user_supp"])

    def start_simulation(self, graph_layout_instance, start_button,
                         restart_button, pause_button, popup_warning, root):

        if self.current_scenario == "scenario":
            if self.treatment_type != "":
                # buttons
                start_button.state = "down"
                start_button.disabled = True
                start_button.sliders_toggles_enabled = self.enable_disable(
                    "disable")
                restart_button.disabled = False
                pause_button.disabled = False

                # death limit
                self.death_limit.points = [(0, self.host_death_density),
                                           (10000, self.host_death_density)]

                # growth limit
                self.growth_limit.points = [
                    (0, self.growth_limitation_density),
                    (10000, self.growth_limitation_density)
                ]
                self.growth_limit_BF.points = [
                    (0, self.growth_limitation_density_BF),
                    (10000, self.growth_limitation_density_BF)
                ]

                # data generator
                self.data_generator_instance = self.data_generator()

                # clock
                self.clock_add_points = Clock.schedule_interval(
                    self.add_points(self.data_generator_instance,
                                    self.sensitive_microbes_plot,
                                    self.resistant_microbes_plot,
                                    self.antimicrobial_plot,
                                    self.immune_system_plot,
                                    self.total_microbes_plot,
                                    self.sensitive_microbes_BF_plot,
                                    self.resistant_microbes_BF_plot), 1 / 60.)

                graph_layout_instance.restart_in_progress_scenario_property = False
                graph_layout_instance.simulation_going_scenario_property = True

            else:
                popup_warning.show_message(
                    global_variables.LANGUAGE["popup_missing_treatment_title"],
                    global_variables.
                    LANGUAGE["popup_missing_treatment_message"])

    def pause_simulation(self, graph_layout_instance, pause_button):

        if pause_button.was_pressed:
            if self.current_scenario == "scenario":
                if not graph_layout_instance.restart_in_progress_scenario_property:
                    # if not paused, cancel schedule
                    if (not graph_layout_instance.pause_scenario_property
                            and graph_layout_instance.
                            simulation_going_scenario_property):
                        self.clock_add_points.cancel()
                        graph_layout_instance.simulation_going_scenario_property = False
                        graph_layout_instance.pause_scenario_property = True
                    # if paused, restart add_points schedule
                    elif (graph_layout_instance.pause_scenario_property
                          and not graph_layout_instance.
                          simulation_going_scenario_property):
                        self.clock_add_points = Clock.schedule_interval(
                            self.add_points(self.data_generator_instance,
                                            self.sensitive_microbes_plot,
                                            self.resistant_microbes_plot,
                                            self.antimicrobial_plot,
                                            self.immune_system_plot,
                                            self.total_microbes_plot,
                                            self.sensitive_microbes_BF_plot,
                                            self.resistant_microbes_BF_plot),
                            1 / 60.)
                        graph_layout_instance.simulation_going_scenario_property = True
                        graph_layout_instance.pause_scenario_property = False
                else:
                    graph_layout_instance.pause_scenario_property = False

            pause_button.was_pressed = False

    def restart_simulation(self, graph_layout_instance, start_button,
                           restart_button, pause_button):

        # buttons
        restart_button.disabled = True
        start_button.state = "normal"
        start_button.disabled = False
        pause_button.disabled = True
        pause_button.was_pressed = True
        pause_button.pause_value = False

        if self.current_scenario == "scenario":
            # re-enable sliders and toggles
            start_button.sliders_toggles_enabled = self.enable_disable(
                "enable")

            # cancel add_points clock
            self.clock_add_points.cancel()

            # reset (x,y) points
            self.sensitive_microbes_plot.points = [(0, 0.001)]
            self.resistant_microbes_plot.points = [(0, 0.001)]
            self.sensitive_microbes_BF_plot.points = [(0, 0.001)]
            self.resistant_microbes_BF_plot.points = [(0, 0.001)]
            self.total_microbes_plot.points = [(0, 0.001)]
            self.immune_system_plot.points = [(0, 0.001)]
            self.antimicrobial_plot.points = [(0, 0)]
            self.death_limit.points = []
            self.growth_limit.points = []
            self.growth_limit_BF.points = []

            # resets xy resizes
            global_variables.MICROBES_ASSORTMENT.get_graph_widget().xmax = 10
            global_variables.MICROBES_ASSORTMENT.get_graph_widget(
            ).x_ticks_major = 1
            global_variables.MICROBES_ASSORTMENT.get_graph_widget(
            ).ymax = 10**3
            global_variables.ANTIMICROBIAL_ASSORTMENT.get_graph_widget(
            ).xmax = 10
            global_variables.ANTIMICROBIAL_ASSORTMENT.get_graph_widget(
            ).x_ticks_major = 1
            global_variables.ANTIMICROBIAL_ASSORTMENT.get_graph_widget(
            ).ymax = 20
            global_variables.ANTIMICROBIAL_ASSORTMENT.get_graph_widget(
            ).y_ticks_major = 4

            # allows pause_simulation to not activate when a restart is made
            graph_layout_instance.restart_in_progress_scenario_property = True
            graph_layout_instance.simulation_going_scenario_property = False

    def save(self, graphs_box_id, directory, popup_warning_id,
             popup_warning_title_and_message):

        # checks if directory exists
        if not os.path.isdir(directory):
            os.mkdir(directory)

        current_datetime = datetime.datetime.now()
        current_datetime = "-".join([str(current_datetime.year), str(current_datetime.month),
                                     str(current_datetime.day)]) + "_" + \
                           "-".join([str(current_datetime.hour), str(current_datetime.minute),
                                     str(current_datetime.second)])

        if self.current_scenario == "scenario":
            # saves screenshot of graph
            graphs_box_id.export_to_png(
                os.path.join(
                    directory,
                    "scenario_screenshot_" + current_datetime + ".png"))

            # save csv file with x-axis and y-axis values for each plot
            with open(os.path.join(
                    directory,
                    "scenario_plot_points_" + current_datetime + ".csv"),
                      "w",
                      newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                # csv header
                csv_writer.writerow([
                    "Time", "Total Microbes Density",
                    "Sensitive Microbes Density (Planktonic)",
                    "Sensitive Microbes Density (Biofilm)",
                    "Resistant Microbes Density (Planktonic)",
                    "Resistant Microbes Density (Biofilm)",
                    "Immune System Density", "Antimicrobial Concentration"
                ])

                # csv rows
                # ignores first value, as it exists only to allow plot instantiation (first y value must not be zero)
                for i in range(len(self.total_microbes_plot.points[1:])):
                    # gets time from total_microbes_plot and y values for each plot
                    csv_writer.writerow([
                        self.total_microbes_plot.points[i +
                                                        1][0],  # x value, time
                        self.total_microbes_plot.points[i + 1][1],  # y value
                        self.sensitive_microbes_plot.points[i +
                                                            1][1],  # y value
                        self.sensitive_microbes_BF_plot.points[
                            i + 1][1],  # y value
                        self.resistant_microbes_plot.points[i +
                                                            1][1],  # y value
                        self.resistant_microbes_BF_plot.points[i + 1]
                        [1],  # y value                                         
                        self.immune_system_plot.points[i + 1][1],  # y value
                        self.antimicrobial_plot.points[i + 1][1]  # y value
                    ])

            # save options used
            with open(
                    os.path.join(
                        directory,
                        "scenario_options_used_" + current_datetime + ".txt"),
                    "w") as options_used_file:
                options_used_file.writelines([
                    global_variables.
                    LANGUAGE["antimicrobial_sensitive_microbes_label"].strip()
                    + ", " +
                    global_variables.LANGUAGE["microbes_initial_density"] +
                    ": " + "%g" % self.sensitive_initial_density + "\n",
                    global_variables.
                    LANGUAGE["antimicrobial_sensitive_microbes_label"].strip()
                    + ", " +
                    global_variables.LANGUAGE["microbes_growth_rate"] + ": " +
                    "%g" % self.sensitive_growth_rate + "\n", global_variables.
                    LANGUAGE["antimicrobial_sensitive_microbes_label"].strip()
                    + ", " +
                    global_variables.LANGUAGE["microbes_attachment_rate"] +
                    ": " + "%g" % self.sensitive_attachment_rate + "\n",
                    global_variables.
                    LANGUAGE["antimicrobial_sensitive_microbes_label"].strip()
                    + ", " + global_variables.
                    LANGUAGE["microbes_antimicrobial_inhibition"] + ": " +
                    "%g" % self.sensitive_antimicrobial_inhibition + "\n",
                    global_variables.
                    LANGUAGE["antimicrobial_sensitive_microbes_label"].strip()
                    + ", " +
                    global_variables.LANGUAGE["microbes_mutation_rate"] +
                    ": " + "%g" % self.sensitive_mutation_rate + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_sensitive_microbes_label_BF"].strip() +
                    ", " +
                    global_variables.LANGUAGE["microbes_initial_density"] +
                    ": " + "%g" % self.sensitive_initial_density_BF + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_sensitive_microbes_label_BF"].strip() +
                    ", " + global_variables.LANGUAGE["microbes_growth_rate"] +
                    ": " + "%g" % self.sensitive_growth_rate_BF + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_sensitive_microbes_label_BF"].strip() +
                    ", " +
                    global_variables.LANGUAGE["microbes_detachment_rate"] +
                    ": " + "%g" % self.sensitive_detachment_rate + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_sensitive_microbes_label_BF"].strip() +
                    ", " + global_variables.
                    LANGUAGE["microbes_antimicrobial_inhibition"] + ": " +
                    "%g" % self.sensitive_antimicrobial_inhibition_BF + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_sensitive_microbes_label_BF"].strip() +
                    ", " +
                    global_variables.LANGUAGE["microbes_mutation_rate"] +
                    ": " + "%g" % self.sensitive_mutation_rate_BF + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_resistant_microbes_label"].strip() +
                    ", " +
                    global_variables.LANGUAGE["microbes_initial_density"] +
                    ": " + "%g" % self.resistant_initial_density + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_resistant_microbes_label"].strip() +
                    ", " + global_variables.LANGUAGE["microbes_growth_rate"] +
                    ": " + "%g" % self.resistant_growth_rate + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_resistant_microbes_label"].strip() +
                    ", " +
                    global_variables.LANGUAGE["microbes_attachment_rate"] +
                    ": " + "%g" % self.resistant_attachment_rate + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_resistant_microbes_label"].strip() +
                    ", " + global_variables.
                    LANGUAGE["microbes_antimicrobial_inhibition"] + ": " +
                    "%g" % self.resistant_antimicrobial_inhibition + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_resistant_microbes_label_BF"].strip() +
                    ", " +
                    global_variables.LANGUAGE["microbes_initial_density"] +
                    ": " + "%g" % self.resistant_initial_density_BF + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_resistant_microbes_label_BF"].strip() +
                    ", " + global_variables.LANGUAGE["microbes_growth_rate"] +
                    ": " + "%g" % self.resistant_growth_rate_BF + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_resistant_microbes_label_BF"].strip() +
                    ", " +
                    global_variables.LANGUAGE["microbes_detachment_rate"] +
                    ": " + "%g" % self.resistant_detachment_rate + "\n",
                    global_variables.LANGUAGE[
                        "antimicrobial_resistant_microbes_label_BF"].strip() +
                    ", " + global_variables.
                    LANGUAGE["microbes_antimicrobial_inhibition"] + ": " +
                    "%g" % self.resistant_antimicrobial_inhibition_BF + "\n",
                    global_variables.LANGUAGE["all_microbes_label"].strip() +
                    ", " + global_variables.
                    LANGUAGE["all_microbes_lymphocyte_inhibition"] + ": " +
                    "%g" % self.lymphocyte_inhibition + "\n",
                    global_variables.LANGUAGE["all_microbes_label"].strip() +
                    ", " +
                    global_variables.LANGUAGE["all_microbes_density_death"] +
                    ": " + "%g" % self.host_death_density + "\n",
                    global_variables.LANGUAGE["all_microbes_label"].strip() +
                    ", " +
                    global_variables.LANGUAGE["growth_limitation_density"] +
                    ": " + "%g" % self.growth_limitation_density + "\n",
                    global_variables.LANGUAGE["all_microbes_label"].strip() +
                    ", " +
                    global_variables.LANGUAGE["growth_limitation_density_BF"] +
                    ": " + "%g" % self.growth_limitation_density_BF + "\n",
                    global_variables.LANGUAGE["all_microbes_label"].strip() +
                    ", " +
                    global_variables.LANGUAGE["all_microbes_natural_death"] +
                    ": " + "%g" % self.natural_death + "\n",
                    global_variables.LANGUAGE["immune_system_label"].strip() +
                    ", " +
                    global_variables.LANGUAGE["immune_system_initial_density"]
                    + ": " + "%g" % self.initial_precursor_cell_density + "\n",
                    global_variables.LANGUAGE["immune_system_label"].strip() +
                    ", " + global_variables.LANGUAGE[
                        "immune_system_proliferation_rate"] + ": " +
                    "%g" % self.immune_cell_proliferation_rate + "\n",
                    global_variables.LANGUAGE["immune_system_label"].strip() +
                    ", " + global_variables.LANGUAGE[
                        "immune_system_half_maximum_growth"] + ": " +
                    "%g" % self.immune_cell_half_maximum_growth + "\n",
                    global_variables.LANGUAGE["immune_system_label"].strip() +
                    ", " + global_variables.LANGUAGE[
                        "immune_system_effector_decay_rate"] + ": " +
                    "%g" % self.effector_decay_rate + "\n",
                    global_variables.LANGUAGE["immune_system_label"].strip() +
                    ", " + global_variables.LANGUAGE[
                        "immune_system_memory_conversion"] + ": " +
                    "%g" % self.memory_cell_conversion_rate + "\n",
                    global_variables.LANGUAGE["antimicrobial_label"].strip() +
                    ", " + global_variables.LANGUAGE[
                        "antimicrobial_mean_concentration"] + ": " +
                    "%g" % self.antimicrobial_mean_concentration + "\n",
                    global_variables.LANGUAGE["antimicrobial_label"].strip() +
                    ", " + global_variables.LANGUAGE["toggle_classic"] + ", " +
                    global_variables.LANGUAGE["treatment_classic_delay"] +
                    ": " + "%g" % self.classic_delay + "\n",
                    global_variables.LANGUAGE["antimicrobial_label"].strip() +
                    ", " + global_variables.LANGUAGE["toggle_classic"] + ", " +
                    global_variables.LANGUAGE["treatment_classic_duration"] +
                    ": " + "%g" % self.classic_duration + "\n",
                    global_variables.LANGUAGE["antimicrobial_label"].strip() +
                    ", " + global_variables.LANGUAGE["toggle_adaptive"] + ", "
                    + global_variables.LANGUAGE["treatment_adaptive_symptoms"]
                    + ": " +
                    "%g" % self.adaptive_symptoms_at_microbes_density + "\n",
                    global_variables.LANGUAGE["antimicrobial_label"].strip() +
                    ", " + global_variables.LANGUAGE["toggle_user"] + ", " +
                    global_variables.LANGUAGE["treatment_user_supp"] + ": " +
                    str(self.user_supp)
                ])

            # popup warning message
            popup_warning_id.show_message(*popup_warning_title_and_message)

    def data_generator(self):

        if self.current_scenario == "scenario":
            # initial values
            current_time_point = 0.0
            sensitive_density = self.sensitive_initial_density
            resistant_density = self.resistant_initial_density
            sensitive_density_BF = self.sensitive_initial_density_BF
            resistant_density_BF = self.resistant_initial_density_BF
            precursor_density = self.initial_precursor_cell_density
            effector_density = 0.0
            memory_cells_density = 0.0

            while True:
                # initial values are yielded at first
                yield (current_time_point, sensitive_density,
                       resistant_density, precursor_density, effector_density,
                       memory_cells_density, sensitive_density_BF,
                       resistant_density_BF)

                antimicrobial_uptake_args = {}
                if self.treatment_type == "Classic":
                    # time is added in calculate_next_time_step()
                    antimicrobial_uptake_args = {
                        "delay": self.classic_delay,
                        "duration": self.classic_duration
                    }
                elif self.treatment_type == "Adaptive":
                    # total_microbes_density is added in calculate_next_time_step()
                    antimicrobial_uptake_args = {
                        "microbes_density_causing_symptoms":
                        self.adaptive_symptoms_at_microbes_density
                    }
                elif self.treatment_type == "User":
                    antimicrobial_uptake_args = {
                        "taking_antimicrobial": self.user_supp
                    }

                (current_time_point, sensitive_density, resistant_density,
                 precursor_density, effector_density, memory_cells_density,
                 sensitive_density_BF,
                 resistant_density_BF) = calculate_next_time_step(
                     current_time_point, sensitive_density, resistant_density,
                     sensitive_density_BF, resistant_density_BF,
                     precursor_density, effector_density, memory_cells_density,
                     self.immune_cell_proliferation_rate,
                     self.lymphocyte_inhibition,
                     self.memory_cell_conversion_rate,
                     self.effector_decay_rate,
                     self.antimicrobial_mean_concentration,
                     self.immune_cell_half_maximum_growth, self.treatment_type,
                     antimicrobial_uptake_args,
                     (self.sensitive_growth_rate,
                      self.sensitive_antimicrobial_inhibition,
                      self.sensitive_attachment_rate,
                      self.sensitive_mutation_rate),
                     (self.resistant_growth_rate,
                      self.resistant_antimicrobial_inhibition,
                      self.resistant_attachment_rate),
                     (self.sensitive_growth_rate_BF,
                      self.sensitive_antimicrobial_inhibition_BF,
                      self.sensitive_detachment_rate,
                      self.sensitive_mutation_rate_BF),
                     (self.resistant_growth_rate_BF,
                      self.resistant_antimicrobial_inhibition_BF,
                      self.resistant_detachment_rate),
                     (self.growth_limitation_density,
                      self.growth_limitation_density_BF), self.natural_death,
                     self.simulation_speed)

    def add_points(self, data_yielder, sensitive_microbes_plot,
                   resistant_microbes_plot, antimicrobial_plot, immune_plot,
                   total_microbes_plot, sensitive_microbes_BF_plot,
                   resistant_microbes_BF_plot):

        def add_points_function(_self, _data_yielder, _sensitive_microbes_plot,
                                _resistant_microbes_plot, _antimicrobial_plot,
                                _immune_plot, _total_microbes_plot,
                                _sensitive_microbes_BF_plot,
                                _resistant_microbes_BF_plot):
            data = next(_data_yielder)

            time = data[0]

            # avoids zero division errors
            sensitive_microbes_density = data[
                1] if data[1] >= 0.001 else 0.000000001
            resistant_microbes_density = data[
                2] if data[2] >= 0.001 else 0.000000001
            sensitive_microbes_density_BF = data[
                6] if data[6] >= 0.001 else 0.000000001
            resistant_microbes_density_BF = data[
                7] if data[7] >= 0.001 else 0.000000001
            immune_cells_density = data[3] + data[4] + data[
                5] if data[3] + data[4] + data[5] >= 0.001 else 0.000000001
            antimicrobial_concentration = _self.antimicrobial_mean_concentration

            # if all microbes are dead or host death threshold is reached, stop generating values
            if (
                    not (sensitive_microbes_density <= 0.001
                         and resistant_microbes_density <= 0.001
                         and sensitive_microbes_density_BF <= 0.001
                         and resistant_microbes_density_BF <= 0.001)
            ) and (sensitive_microbes_density + resistant_microbes_density +
                   sensitive_microbes_density_BF +
                   resistant_microbes_density_BF < _self.host_death_density):
                _sensitive_microbes_plot.points.append(
                    (time, sensitive_microbes_density))
                _resistant_microbes_plot.points.append(
                    (time, resistant_microbes_density))
                _sensitive_microbes_BF_plot.points.append(
                    (time, sensitive_microbes_density_BF))
                _resistant_microbes_BF_plot.points.append(
                    (time, resistant_microbes_density_BF))
                _immune_plot.points.append((time, immune_cells_density))
                _total_microbes_plot.points.append(
                    (time,
                     sensitive_microbes_density + resistant_microbes_density +
                     sensitive_microbes_density_BF +
                     resistant_microbes_density_BF))

                # treatment type logic
                if _self.treatment_type == "Classic":
                    if _self.classic_delay < time < _self.classic_delay + _self.classic_duration:
                        _antimicrobial_plot.points.append(
                            (time, antimicrobial_concentration))
                    else:
                        _antimicrobial_plot.points.append((time, 0))
                elif _self.treatment_type == "Adaptive":
                    if _self.adaptive_symptoms_at_microbes_density <\
                                    sensitive_microbes_density + resistant_microbes_density + sensitive_microbes_density_BF + resistant_microbes_density_BF:
                        _antimicrobial_plot.points.append(
                            (time, antimicrobial_concentration))
                    else:
                        _antimicrobial_plot.points.append((time, 0))
                elif _self.treatment_type == "User":
                    if _self.user_supp:
                        _antimicrobial_plot.points.append(
                            (time, antimicrobial_concentration))
                    else:
                        _antimicrobial_plot.points.append((time, 0))
            else:
                _sensitive_microbes_plot.points.append(
                    (time, sensitive_microbes_density))
                _resistant_microbes_plot.points.append(
                    (time, resistant_microbes_density))
                _sensitive_microbes_BF_plot.points.append(
                    (time, sensitive_microbes_density_BF))
                _resistant_microbes_BF_plot.points.append(
                    (time, resistant_microbes_density_BF))
                _immune_plot.points.append((time, immune_cells_density))
                _total_microbes_plot.points.append(
                    (time,
                     sensitive_microbes_density + resistant_microbes_density +
                     sensitive_microbes_density_BF +
                     resistant_microbes_density_BF))

                # treatment type logic
                if _self.treatment_type == "Classic":
                    if _self.classic_delay < time < _self.classic_delay + _self.classic_duration:
                        _antimicrobial_plot.points.append(
                            (time, antimicrobial_concentration))
                    else:
                        _antimicrobial_plot.points.append((time, 0))
                elif _self.treatment_type == "Adaptive":
                    if _self.adaptive_symptoms_at_microbes_density <\
                                    sensitive_microbes_density + resistant_microbes_density + sensitive_microbes_density_BF + resistant_microbes_density_BF:
                        _antimicrobial_plot.points.append(
                            (time, antimicrobial_concentration))
                    else:
                        _antimicrobial_plot.points.append((time, 0))
                elif _self.treatment_type == "User":
                    if _self.user_supp:
                        _antimicrobial_plot.points.append(
                            (time, antimicrobial_concentration))
                    else:
                        _antimicrobial_plot.points.append((time, 0))
                # cancel clock
                _self.clock_add_points.cancel()

                # checks whether host death or microbes death
                if sensitive_microbes_density + resistant_microbes_density + sensitive_microbes_density_BF + resistant_microbes_density_BF >= _self.host_death_density:
                    title = "popup_host_death_title"
                    message = "popup_host_death_message"
                else:
                    title = "popup_microbes_death_title"
                    message = "popup_microbes_death_message"

                # show popup message
                _self.root.ids.popup_warning.show_message(
                    global_variables.LANGUAGE[title],
                    global_variables.LANGUAGE[message])

        return lambda _: add_points_function(
            self, data_yielder, sensitive_microbes_plot,
            resistant_microbes_plot, antimicrobial_plot, immune_plot,
            total_microbes_plot, sensitive_microbes_BF_plot,
            resistant_microbes_BF_plot)

    def enable_disable(self, what):

        if self.current_scenario == "scenario":
            if what == "disable":
                for i in self.root.slider_ids + self.root.toggle_id.toggle_ids:
                    i.disabled = True
                if self.treatment_type != "User":
                    self.root.toggle_id.options.disabled = True
                return False
            elif what == "enable":
                for i in self.root.slider_ids + self.root.toggle_id.toggle_ids:
                    i.disabled = False
                self.root.toggle_id.options.disabled = False
                return True

    def assign_treatment(self, value):

        self.treatment_type = value

    def on_host_death_density_value(self, *args):

        self.host_death_density = self.host_death_density_value * self.host_death_density_exponent

    def on_host_death_density_exponent(self, *args):

        self.host_death_density = self.host_death_density_value * self.host_death_density_exponent

    def on_growth_limitation_density_value(self, *args):

        self.growth_limitation_density = self.growth_limitation_density_value * self.growth_limitation_density_exponent

    def on_growth_limitation_density_exponent(self, *args):

        self.growth_limitation_density = self.growth_limitation_density_value * self.growth_limitation_density_exponent

    def on_growth_limitation_density_BF_value(self, *args):

        self.growth_limitation_density_BF = self.growth_limitation_density_BF_value * self.growth_limitation_density_BF_exponent

    def on_growth_limitation_density_BF_exponent(self, *args):

        self.growth_limitation_density_BF = self.growth_limitation_density_BF_value * self.growth_limitation_density_BF_exponent

    def on_sensitive_initial_density_value(self, *args):

        self.sensitive_initial_density = self.sensitive_initial_density_value * self.sensitive_initial_density_exponent

    def on_sensitive_initial_density_exponent(self, *args):

        self.sensitive_initial_density = self.sensitive_initial_density_value * self.sensitive_initial_density_exponent

    def on_sensitive_initial_density_BF_value(self, *args):

        self.sensitive_initial_density_BF = self.sensitive_initial_density_BF_value * self.sensitive_initial_density_BF_exponent

    def on_sensitive_initial_density_BF_exponent(self, *args):

        self.sensitive_initial_density_BF = self.sensitive_initial_density_BF_value * self.sensitive_initial_density_BF_exponent

    def on_sensitive_mutation_rate_value(self, *args):

        self.sensitive_mutation_rate = self.sensitive_mutation_rate_value * self.sensitive_mutation_rate_exponent

    def on_sensitive_mutation_rate_exponent(self, *args):

        self.sensitive_mutation_rate = self.sensitive_mutation_rate_exponent * self.sensitive_mutation_rate_exponent

    def on_sensitive_mutation_rate_BF_value(self, *args):

        self.sensitive_mutation_rate_BF = self.sensitive_mutation_rate_BF_value * self.sensitive_mutation_rate_BF_exponent

    def on_sensitive_mutation_rate_BF_exponent(self, *args):

        self.sensitive_mutation_rate_BF = self.sensitive_mutation_rate_BF_exponent * self.sensitive_mutation_rate_BF_exponent

    def on_initial_precursor_cell_density_value(self, *args):

        self.initial_precursor_cell_density = self.initial_precursor_cell_density_value * self.initial_precursor_cell_density_exponent

    def on_initial_precursor_cell_density_exponent(self, *args):

        self.initial_precursor_cell_density = self.initial_precursor_cell_density_value * self.initial_precursor_cell_density_exponent

    def on_antimicrobial_mean_concentration_value(self, *args):

        self.antimicrobial_mean_concentration = self.antimicrobial_mean_concentration_value * self.antimicrobial_mean_concentration_exponent

    def on_antimicrobial_mean_concentration_exponent(self, *args):

        self.antimicrobial_mean_concentration = self.antimicrobial_mean_concentration_value * self.antimicrobial_mean_concentration_exponent

    def on_adaptive_symptoms_at_microbes_density_value(self, *args):

        self.adaptive_symptoms_at_microbes_density = (
            self.adaptive_symptoms_at_microbes_density_value *
            self.adaptive_symptoms_at_microbes_density_exponent)

    def on_adaptive_symptoms_at_microbes_density_exponent(self, *args):

        self.adaptive_symptoms_at_microbes_density = (
            self.adaptive_symptoms_at_microbes_density_value *
            self.adaptive_symptoms_at_microbes_density_exponent)

    def on_pause(self, *args):
        #needed to override so that the default behaviour was inhibited
        pass

    def build(self):
        self.icon = os.path.join("bin", "ui", "icon.ico")
        self.title = "Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance"
        return Builder.load_file(os.path.join('bin', 'ui', 'main_layout.kv'))


def start():

    Simulator().run()
