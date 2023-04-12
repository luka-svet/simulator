# Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance
#
# Copyright 2018-2019 Pedro HC David <https://github.com/Kronopt> and SimulATe contributors
# Copyright 2019-2023 Luka Svet <luka.svet@kuleuven.be>
#
# The following code is a derivative work of the code from the Mercurial project,
# which is licensed under GPLv3. This code therefore is also licensed under the terms
# of the GNU General Public License, version 3.


def microbes_densityPS_eq(previous_density, growth_rate_PS,
                          lymphocyte_inhibition, total_immune_cells,
                          antimicrobial_inhibition_PS, antimicrobial_uptake,
                          antimicrobial_concentration, mutation_rate_PS,
                          density_PR, maximum_density_P, death_rate,
                          attachment_rate_PS, detachment_rate_BS, density_BS):

    if previous_density >= 0.001:
        return previous_density * (
            growth_rate_PS *
            (1 - (previous_density + density_PR) / maximum_density_P) -
            death_rate - attachment_rate_PS - mutation_rate_PS -
            antimicrobial_uptake * antimicrobial_inhibition_PS *
            antimicrobial_concentration - lymphocyte_inhibition *
            total_immune_cells) + detachment_rate_BS * density_BS
    elif density_BS >= 0.001:
        return detachment_rate_BS * density_BS
    else:
        return 0


def microbes_densityBS_eq(previous_density, growth_rate_BS,
                          lymphocyte_inhibition, total_immune_cells,
                          antimicrobial_inhibition_BS, antimicrobial_uptake,
                          antimicrobial_concentration, mutation_rate_BS,
                          density_BR, maximum_density_B, death_rate,
                          attachment_rate_PS, detachment_rate_BS, density_PS):

    if previous_density >= 0.001:
        return previous_density * (
            growth_rate_BS *
            (1 - (previous_density + density_BR) / maximum_density_B) -
            death_rate - detachment_rate_BS - mutation_rate_BS -
            antimicrobial_uptake * antimicrobial_inhibition_BS *
            antimicrobial_concentration - lymphocyte_inhibition *
            total_immune_cells) + attachment_rate_PS * density_PS
    elif density_PS >= 0.001:
        return attachment_rate_PS * density_PS
    else:
        return 0


def microbes_densityPR_eq(previous_density, growth_rate_PR,
                          lymphocyte_inhibition, total_immune_cells,
                          antimicrobial_inhibition_PR, antimicrobial_uptake,
                          antimicrobial_concentration, mutation_rate_PS,
                          density_PS, maximum_density_P, death_rate,
                          attachment_rate_PR, detachment_rate_BR, density_BR):

    if previous_density >= 0.001:
        return previous_density * (
            growth_rate_PR *
            (1 - (previous_density + density_PS) / maximum_density_P) -
            death_rate - attachment_rate_PR - antimicrobial_uptake *
            antimicrobial_inhibition_PR * antimicrobial_concentration -
            lymphocyte_inhibition * total_immune_cells) + (
                detachment_rate_BR * density_BR +
                mutation_rate_PS * density_PS)
    elif (density_BR >= 0.001 and density_PS >= 0.001):
        return detachment_rate_BR * density_BR + mutation_rate_PS * density_PS
    elif density_BR >= 0.001:
        return detachment_rate_BR * density_BR
    elif density_PS >= 0.001:
        return mutation_rate_PS * density_PS
    else:
        return 0


def microbes_densityBR_eq(previous_density, growth_rate_BR,
                          lymphocyte_inhibition, total_immune_cells,
                          antimicrobial_inhibition_BR, antimicrobial_uptake,
                          antimicrobial_concentration, mutation_rate_BS,
                          density_BS, maximum_density_B, death_rate,
                          attachment_rate_PR, detachment_rate_BR, density_PR):

    if previous_density >= 0.001:
        return previous_density * (
            growth_rate_BR *
            (1 - (previous_density + density_BS) / maximum_density_B) -
            death_rate - detachment_rate_BR - antimicrobial_uptake *
            antimicrobial_inhibition_BR * antimicrobial_concentration -
            lymphocyte_inhibition * total_immune_cells) + (
                attachment_rate_PR * density_PR +
                mutation_rate_BS * density_BS)
    elif (density_PR >= 0.001 and density_BS >= 0.001):
        return attachment_rate_PR * density_PR + mutation_rate_BS * density_BS
    elif density_PR >= 0.001:
        return attachment_rate_PR * density_PR
    elif density_BS >= 0.001:
        return mutation_rate_BS * density_BS
    else:
        return 0


#IMMUNE SYSTEM


def naive_precursor_cells_density_eq(previous_density, proliferation_rate,
                                     microbes_density,
                                     immune_response_half_max_growth):

    return (-1 * proliferation_rate) * previous_density * (
        microbes_density /
        (immune_response_half_max_growth + microbes_density))


def effector_cells_density_eq(previous_density, proliferation_rate,
                              naive_precursor_cells_density, microbes_density,
                              immune_response_half_max_growth, effector_decay):

    return (2 * proliferation_rate * naive_precursor_cells_density +
            proliferation_rate * previous_density) * (
                microbes_density /
                (immune_response_half_max_growth + microbes_density)
            ) - effector_decay * previous_density * (
                1 - (microbes_density /
                     (immune_response_half_max_growth + microbes_density)))


def memory_cells_density_eq(previous_density, converted_effectors,
                            effector_cells_density, effector_decay,
                            microbes_density, immune_response_half_max_growth):

    return converted_effectors * effector_cells_density * effector_decay * (
        1 - (microbes_density /
             (immune_response_half_max_growth + microbes_density)))


def antimicrobial_uptake_eq(treatment_type, **kwargs):

    if treatment_type == "Classic":
        delay = kwargs["delay"]
        duration = kwargs["duration"]
        time = kwargs["time"]

        # treatment occurs between delay and duration + delay
        return int(delay <= time <= delay + duration)  # 0 or 1

    elif treatment_type == "Adaptive":
        microbes_density_causing_symptoms = kwargs[
            "microbes_density_causing_symptoms"]
        total_microbes_density = kwargs["total_microbes_density"]

        # treatment occurs every time the microbes reach a density above the set threshold
        return int(total_microbes_density >=
                   microbes_density_causing_symptoms)  # 0 or 1

    elif treatment_type == "User":
        return int(kwargs["taking_antimicrobial"])  # 0 or 1


def calculate_next_time_step(
        current_time_point, sensitive_microbes_density,
        resistant_microbes_density, sensitive_microbes_density_BF,
        resistant_microbes_density_BF, naive_precursor_cells_density,
        effector_cells_density, memory_cells_density,
        immune_cells_proliferation_rate, lymphocyte_inhibition,
        converted_effectors, effector_cells_decay, antimicrobial_concentration,
        immune_response_half_max_growth, antimicrobial_treatment_type,
        antimicrobial_uptake_args, bs_variables, br_variables, bs_variablesBF,
        br_variablesBF, limitation_variables, microbes_natural_death,
        time_step):

    total_microbes_density = sensitive_microbes_density + resistant_microbes_density + sensitive_microbes_density_BF + resistant_microbes_density_BF

    if antimicrobial_treatment_type == 'Classic':
        antimicrobial_uptake_args["time"] = current_time_point
    if antimicrobial_treatment_type == "Adaptive":
        antimicrobial_uptake_args[
            "total_microbes_density"] = total_microbes_density

    antimicrobial_uptake = antimicrobial_uptake_eq(
        antimicrobial_treatment_type, **antimicrobial_uptake_args)
    total_immune_cells = naive_precursor_cells_density + effector_cells_density + memory_cells_density

    k1PS = microbes_densityPS_eq(
        sensitive_microbes_density, bs_variables[0], lymphocyte_inhibition,
        total_immune_cells, bs_variables[1], antimicrobial_uptake,
        antimicrobial_concentration, bs_variables[3],
        resistant_microbes_density, limitation_variables[0],
        microbes_natural_death, bs_variables[2], bs_variablesBF[2],
        sensitive_microbes_density_BF)

    k2PS = microbes_densityPS_eq(
        sensitive_microbes_density + (time_step / 2) * k1PS, bs_variables[0],
        lymphocyte_inhibition, total_immune_cells, bs_variables[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variables[3],
        resistant_microbes_density, limitation_variables[0],
        microbes_natural_death, bs_variables[2], bs_variablesBF[2],
        sensitive_microbes_density_BF)

    k3PS = microbes_densityPS_eq(
        sensitive_microbes_density + (time_step / 2) * k2PS, bs_variables[0],
        lymphocyte_inhibition, total_immune_cells, bs_variables[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variables[3],
        resistant_microbes_density, limitation_variables[0],
        microbes_natural_death, bs_variables[2], bs_variablesBF[2],
        sensitive_microbes_density_BF)

    k4PS = microbes_densityPS_eq(
        sensitive_microbes_density + time_step * k3PS, bs_variables[0],
        lymphocyte_inhibition, total_immune_cells, bs_variables[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variables[3],
        resistant_microbes_density, limitation_variables[0],
        microbes_natural_death, bs_variables[2], bs_variablesBF[2],
        sensitive_microbes_density_BF)

    new_bs = sensitive_microbes_density + (time_step / 6) * (k1PS + 2 * k2PS +
                                                             2 * k3PS + k4PS)

    k1BS = microbes_densityBS_eq(
        sensitive_microbes_density_BF, bs_variablesBF[0],
        lymphocyte_inhibition, total_immune_cells, bs_variablesBF[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variablesBF[3],
        resistant_microbes_density_BF, limitation_variables[1],
        microbes_natural_death, bs_variables[2], bs_variablesBF[2],
        sensitive_microbes_density)

    k2BS = microbes_densityBS_eq(
        sensitive_microbes_density_BF + (time_step / 2) * k1BS,
        bs_variablesBF[0], lymphocyte_inhibition, total_immune_cells,
        bs_variablesBF[1], antimicrobial_uptake, antimicrobial_concentration,
        bs_variablesBF[3], resistant_microbes_density_BF,
        limitation_variables[1], microbes_natural_death, bs_variables[2],
        bs_variablesBF[2], sensitive_microbes_density)

    k3BS = microbes_densityBS_eq(
        sensitive_microbes_density_BF + (time_step / 2) * k2BS,
        bs_variablesBF[0], lymphocyte_inhibition, total_immune_cells,
        bs_variablesBF[1], antimicrobial_uptake, antimicrobial_concentration,
        bs_variablesBF[3], resistant_microbes_density_BF,
        limitation_variables[1], microbes_natural_death, bs_variables[2],
        bs_variablesBF[2], sensitive_microbes_density)

    k4BS = microbes_densityBS_eq(
        sensitive_microbes_density_BF + time_step * k3BS, bs_variablesBF[0],
        lymphocyte_inhibition, total_immune_cells, bs_variablesBF[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variablesBF[3],
        resistant_microbes_density_BF, limitation_variables[1],
        microbes_natural_death, bs_variables[2], bs_variablesBF[2],
        sensitive_microbes_density)

    new_bsBF = sensitive_microbes_density_BF + (time_step / 6) * (
        k1BS + 2 * k2BS + 2 * k3BS + k4BS)

    k1PR = microbes_densityPR_eq(
        resistant_microbes_density, br_variables[0], lymphocyte_inhibition,
        total_immune_cells, br_variables[1], antimicrobial_uptake,
        antimicrobial_concentration, bs_variables[3],
        sensitive_microbes_density, limitation_variables[0],
        microbes_natural_death, br_variables[2], br_variablesBF[2],
        resistant_microbes_density_BF)

    k2PR = microbes_densityPR_eq(
        resistant_microbes_density + (time_step / 2) * k1PR, br_variables[0],
        lymphocyte_inhibition, total_immune_cells, br_variables[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variables[3],
        sensitive_microbes_density, limitation_variables[0],
        microbes_natural_death, br_variables[2], br_variablesBF[2],
        resistant_microbes_density_BF)

    k3PR = microbes_densityPR_eq(
        resistant_microbes_density + (time_step / 2) * k2PR, br_variables[0],
        lymphocyte_inhibition, total_immune_cells, br_variables[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variables[3],
        sensitive_microbes_density, limitation_variables[0],
        microbes_natural_death, br_variables[2], br_variablesBF[2],
        resistant_microbes_density_BF)

    k4PR = microbes_densityPR_eq(
        resistant_microbes_density + time_step * k3PR, br_variables[0],
        lymphocyte_inhibition, total_immune_cells, br_variables[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variables[3],
        sensitive_microbes_density, limitation_variables[0],
        microbes_natural_death, br_variables[2], br_variablesBF[2],
        resistant_microbes_density_BF)

    new_br = resistant_microbes_density + (time_step / 6) * (k1PR + 2 * k2PR +
                                                             2 * k3PR + k4PR)

    k1BR = microbes_densityBR_eq(
        resistant_microbes_density_BF, br_variablesBF[0],
        lymphocyte_inhibition, total_immune_cells, br_variablesBF[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variablesBF[3],
        sensitive_microbes_density_BF, limitation_variables[1],
        microbes_natural_death, br_variables[2], br_variablesBF[2],
        resistant_microbes_density)

    k2BR = microbes_densityBR_eq(
        resistant_microbes_density_BF + (time_step / 2) * k1BR,
        br_variablesBF[0], lymphocyte_inhibition, total_immune_cells,
        br_variablesBF[1], antimicrobial_uptake, antimicrobial_concentration,
        bs_variablesBF[3], sensitive_microbes_density_BF,
        limitation_variables[1], microbes_natural_death, br_variables[2],
        br_variablesBF[2], resistant_microbes_density)

    k3BR = microbes_densityBR_eq(
        resistant_microbes_density_BF + (time_step / 2) * k2BR,
        br_variablesBF[0], lymphocyte_inhibition, total_immune_cells,
        br_variablesBF[1], antimicrobial_uptake, antimicrobial_concentration,
        bs_variablesBF[3], sensitive_microbes_density_BF,
        limitation_variables[1], microbes_natural_death, br_variables[2],
        br_variablesBF[2], resistant_microbes_density)

    k4BR = microbes_densityBR_eq(
        resistant_microbes_density_BF + time_step * k3BR, br_variablesBF[0],
        lymphocyte_inhibition, total_immune_cells, br_variablesBF[1],
        antimicrobial_uptake, antimicrobial_concentration, bs_variablesBF[3],
        sensitive_microbes_density_BF, limitation_variables[1],
        microbes_natural_death, br_variables[2], br_variablesBF[2],
        resistant_microbes_density)

    new_brBF = resistant_microbes_density_BF + (time_step / 6) * (
        k1BR + 2 * k2BR + 2 * k3BR + k4BR)

    k1n = naive_precursor_cells_density_eq(naive_precursor_cells_density,
                                           immune_cells_proliferation_rate,
                                           total_microbes_density,
                                           immune_response_half_max_growth)

    k2n = naive_precursor_cells_density_eq(
        naive_precursor_cells_density + (time_step / 2) * k1n,
        immune_cells_proliferation_rate, total_microbes_density,
        immune_response_half_max_growth)

    k3n = naive_precursor_cells_density_eq(
        naive_precursor_cells_density + (time_step / 2) * k2n,
        immune_cells_proliferation_rate, total_microbes_density,
        immune_response_half_max_growth)

    k4n = naive_precursor_cells_density_eq(
        naive_precursor_cells_density + time_step * k3n,
        immune_cells_proliferation_rate, total_microbes_density,
        immune_response_half_max_growth)

    new_n = naive_precursor_cells_density + (time_step / 6) * (k1n + 2 * k2n +
                                                               2 * k3n + k4n)

    k1e = effector_cells_density_eq(effector_cells_density,
                                    immune_cells_proliferation_rate,
                                    naive_precursor_cells_density,
                                    total_microbes_density,
                                    immune_response_half_max_growth,
                                    effector_cells_decay)

    k2e = effector_cells_density_eq(
        effector_cells_density + (time_step / 2) * k1e,
        immune_cells_proliferation_rate, naive_precursor_cells_density,
        total_microbes_density, immune_response_half_max_growth,
        effector_cells_decay)

    k3e = effector_cells_density_eq(
        effector_cells_density + (time_step / 2) * k2e,
        immune_cells_proliferation_rate, naive_precursor_cells_density,
        total_microbes_density, immune_response_half_max_growth,
        effector_cells_decay)

    k4e = effector_cells_density_eq(effector_cells_density + time_step * k3e,
                                    immune_cells_proliferation_rate,
                                    naive_precursor_cells_density,
                                    total_microbes_density,
                                    immune_response_half_max_growth,
                                    effector_cells_decay)

    new_e = effector_cells_density + (time_step / 6) * (k1e + 2 * k2e +
                                                        2 * k3e + k4e)

    k1m = memory_cells_density_eq(memory_cells_density, converted_effectors,
                                  effector_cells_density, effector_cells_decay,
                                  total_microbes_density,
                                  immune_response_half_max_growth)

    k2m = memory_cells_density_eq(memory_cells_density + (time_step / 2) * k1m,
                                  converted_effectors, effector_cells_density,
                                  effector_cells_decay, total_microbes_density,
                                  immune_response_half_max_growth)

    k3m = memory_cells_density_eq(memory_cells_density + (time_step / 2) * k2m,
                                  converted_effectors, effector_cells_density,
                                  effector_cells_decay, total_microbes_density,
                                  immune_response_half_max_growth)

    k4m = memory_cells_density_eq(memory_cells_density + time_step * k3m,
                                  converted_effectors, effector_cells_density,
                                  effector_cells_decay, total_microbes_density,
                                  immune_response_half_max_growth)

    new_m = memory_cells_density + (time_step / 6) * (k1m + 2 * k2m + 2 * k3m +
                                                      k4m)

    new_time_point = current_time_point + time_step
    return new_time_point, new_bs, new_br, new_n, new_e, new_m, new_bsBF, new_brBF
