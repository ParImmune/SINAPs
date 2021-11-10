#! /usr/bin/env python3

#######################################################################################################################~
#
# SINAPs V1.0 - Analyzer - Functions
#
#######################################################################################################################~

#######################################################################################################################~
#
# Copyright Par'Immune 2021 - GPL-3.0-only
#
# SINAPs is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#######################################################################################################################~

import pytraj as pt
import numpy as np
from itertools import combinations
from Bio.PDB import *
import glob

#######################################################################################################################~

# VARIABLES
BACKBONE = ["CA", "C", "H", "O", "N"]
RESIDUES = ["ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","HIE","HID","HIP","ILE","LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL"]
ARO_RES = ["TYR", "PHE", "TRP"]
parameter_aro_distance = 7

#######################################################################################################################~

def TRAJ_loader(traj, parm):
    trajout = pt.load(traj, parm)
    return trajout

def PDB_loader(traj):
    trajout = pt.load(traj)
    return trajout

#######################################################################################################################~

def representative_SINAPs(traj, traj_name, representative_frame, representative_complexity, path, representative_nb):
    # Definition de la frame qui sera utilisée
    if representative_frame == "first":
        representative_frame_nb = [0]
    elif representative_frame == "last":
        representative_frame_nb = [traj.n_frames - 1]
    elif representative_frame.isnumeric():
        representative_frame_nb = int(representative_frame) - 1
    else:
        representative_frame_nb = [0]

    # Frame representative - save PDB
    if representative_complexity == 1:
        pt.write_traj("{0}/{1}_{2}.pdb".format(path, representative_nb, traj_name), traj, frame_indices=representative_frame_nb,
                      overwrite=True)
    else:
        pt.write_traj("{0}/{1}_{2}.pdb".format(path, representative_nb, traj_name), traj["(@CA,C,O,N)|(!:ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,HIE,HID,HIP,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL)"], frame_indices=representative_frame_nb,
                      overwrite=True)

#######################################################################################################################~

def alignment_SINAPs(path):
    representative_list = glob.glob("{0}/Representative*.pdb".format(path))
    pdb_parser = PDBParser(QUIET=True)

    # Reference PDB
    structure_reference = pdb_parser.get_structure("reference", representative_list[0])
    model_reference = structure_reference[0]
    residues_reference = {}
    for chain_reference in model_reference:
        for i in chain_reference:
            try:
                i["CA"]
            except:
                continue
            else:
                residues_reference[i.get_id()[1]] = i["CA"]

    # Samples PDB
    for nb_pdb in range(1, len(representative_list)):
        pdb_sample = representative_list[nb_pdb]
        structure_sample = pdb_parser.get_structure("sample", pdb_sample)
        model_sample = structure_sample[0]
        residues_sample = {}
        for chain_sample in model_sample:
            for i in chain_sample:
                try:
                    i["CA"]
                except:
                    continue
                else:
                    residues_sample[i.get_id()[1]] = i["CA"]

        # Intersection & CA to align
        keys_to_align = list(residues_reference.keys() & residues_sample.keys())

        CA_reference = [residues_reference[i] for i in keys_to_align]
        CA_sample = [residues_sample[i] for i in keys_to_align]

        # Superimposer
        pdb_superimposer = Superimposer()
        pdb_superimposer.set_atoms(CA_reference, CA_sample)
        pdb_superimposer.apply(model_sample.get_atoms())

        # Output
        pdb_io = PDBIO()
        pdb_io.set_structure(structure_sample)
        pdb_io.save("{0}".format(representative_list[nb_pdb]))


#######################################################################################################################~

def SINAPs_HB(traj, param_HB_distance, param_HB_angle, frequency_cutoff = 0.01, water = 0):
    output_HB = []

    if float(frequency_cutoff) >= 1:
        frequency_cutoff = float(frequency_cutoff)/100
    else:
        frequency_cutoff = float(frequency_cutoff)

    if water == 0:
        HB = pt.search_hbonds(traj, distance=param_HB_distance, angle=param_HB_angle)
    else:
        HB = pt.search_hbonds(traj, distance=param_HB_distance, angle=param_HB_angle, solvent_acceptor=":HOH,WAT", solvent_donor = ":HOH,WAT")

    #####

    nb_HB = len(HB.values) - 1

    HB_id = np.array([]) ; HB_acc = np.array([]) ; HB_don = np.array([]) ; HB_type = np.array([])

    for i in range(nb_HB):
        HB_temp = HB.get_amber_mask()[1][i].split(" ")
        HB_acc = np.append(HB_acc, HB_temp[0])
        HB_don = np.append(HB_don, HB_temp[2])

        if HB_temp[0].split("@")[1] in BACKBONE and HB_temp[2].split("@")[1] in BACKBONE:
            HB_type_temp = "1"  # BB/BB
        elif HB_temp[0].split("@")[1] in BACKBONE or HB_temp[2].split("@")[1] in BACKBONE:
            HB_type_temp = "2"  # BB/SC
        else:
            HB_type_temp = "3"  # SC/SC

        HB_type = np.append(HB_type, HB_type_temp)
        HB_id = np.append(HB_id, HB_temp[0].split("@")[0][1:] + "-" + HB_temp[2].split("@")[0][1:] + "-" + HB_type_temp)

    HB_id_unique = np.unique(HB_id)

    # Fusion des HB avec des DonH differents
    for i in range(len(HB_id_unique)):
        # Recup index des doublons potentiels & Ajout 1 à tous les index pour HB.data
        index_temp = np.where(HB_id == HB_id_unique[i])[0]
        data_temp = np.array(HB.data[index_temp+1])

        if len(data_temp) == 1:
            HB_frequency = round(np.sum(data_temp) / traj.n_frames, 3)
        else:
            HB_frequency = round(len(np.where(data_temp.sum(axis=0) > 0)[0]) / traj.n_frames, 3)

        if HB_frequency >= float(frequency_cutoff):
            output_HB.append([HB_acc[index_temp[0]], HB_don[index_temp[0]], HB_type[index_temp[0]], HB_id[index_temp[0]], HB_frequency])

    return output_HB

#######################################################################################################################~

def SINAPs_output_HB(traj1, traj2, output_HB_traj1, output_HB_traj2, path, prefix):
    output_liste = []
    HB1_list = [elem[3] for elem in output_HB_traj1]
    HB2_list = [elem[3] for elem in output_HB_traj2]

    ###########################################

    ligands1 = [] ; ligands2 = []

    for i in range(traj1.top.n_residues):
        if traj1.top.residue(i).name not in RESIDUES:
            ligands1.append(i + 1)

    for i in range(traj2.top.n_residues):
        if traj2.top.residue(i).name not in RESIDUES:
            ligands2.append(i + 1)

    ###########################################

    for i in range(len(HB1_list)):
        HB1 = HB1_list[i]
        if HB1 in HB2_list:
            output_liste.append(output_HB_traj1[i][:2] + output_HB_traj2[HB2_list.index(HB1)][:2] + output_HB_traj1[i][2:] + [output_HB_traj2[HB2_list.index(HB1)][4]])
        else:
            output_liste.append(output_HB_traj1[i][:2] + [-1, -1] + output_HB_traj1[i][2:] + [-1])

    ###########################################

    for i in range(len(HB2_list)):
        HB2 = HB2_list[i]
        if HB2 not in HB1_list:
            output_liste.append([-1, -1] + output_HB_traj2[i][0:4] + [-1] + [output_HB_traj2[i][4]])

    ###########################################

    topo1 = traj1["(@CA,C,O,N)|(!:ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,HIE,HID,HIP,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL)"].top
    topo2 = traj2["(@CA,C,O,N)|(!:ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,HIE,HID,HIP,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL)"].top

    ###########################################

    with open("{0}/Results_HB_{1}.csv".format(path, prefix), "w") as write_output:
        for hbond in output_liste:
            if hbond[6] == -1:   # Freq traj1
                traj1_acceptor = -1 ; pos_traj1_acceptor = -1
                traj1_donor = -1 ; pos_traj1_donor = -1
            else:
                # ACCEPTOR 1
                if hbond[0].split("@")[1] not in BACKBONE and int(hbond[0].split("@")[0][1:]) not in ligands1 and int(hbond[0].split("@")[0][1:]) not in ligands2:
                    traj1_acceptor = "{0}@CA".format(hbond[0].split("@")[0])
                else:
                    traj1_acceptor = hbond[0]

                # DONOR 1
                if hbond[1].split("@")[1] not in BACKBONE and int(hbond[1].split("@")[0][1:]) not in ligands1 and int(hbond[1].split("@")[0][1:]) not in ligands2:
                    traj1_donor = "{0}@CA".format(hbond[1].split("@")[0])
                else:
                    traj1_donor = hbond[1]

                pos_traj1_acceptor = pt.select_atoms(topo1, traj1_acceptor)[0]
                pos_traj1_donor = pt.select_atoms(topo1, traj1_donor)[0]


            if hbond[7] == -1:   # Freq traj2
                traj2_acceptor = -1 ; pos_traj2_acceptor = -1
                traj2_donor = -1 ; pos_traj2_donor = -1
            else:
                # ACCEPTOR 2
                if hbond[2].split("@")[1] not in BACKBONE and int(hbond[2].split("@")[0][1:]) not in ligands1 and int(hbond[2].split("@")[0][1:]) not in ligands2:
                    traj2_acceptor = "{0}@CA".format(hbond[2].split("@")[0])
                else:
                    traj2_acceptor = hbond[2]

                # DONOR 2
                if hbond[3].split("@")[1] not in BACKBONE and int(hbond[3].split("@")[0][1:]) not in ligands1 and int(hbond[3].split("@")[0][1:]) not in ligands2:
                    traj2_donor = "{0}@CA".format(hbond[3].split("@")[0])
                else:
                    traj2_donor = hbond[3]

                pos_traj2_acceptor = pt.select_atoms(topo2, traj2_acceptor)[0]
                pos_traj2_donor = pt.select_atoms(topo2, traj2_donor)[0]

            write_output.write("{0} {1} {2} {3} {4} {5} {6} {7} {8}\n".format("{0}/{1}".format(traj1_acceptor, traj2_acceptor), "{0}/{1}".format(traj1_donor, traj2_donor), pos_traj1_acceptor, pos_traj1_donor, pos_traj2_acceptor, pos_traj2_donor, hbond[4], hbond[6], hbond[7]))


#######################################################################################################################~

def SINAPs_SB(traj, param_SB_distance, param_SB_angle, frequency_cutoff = 0.01):
    output_SB = []

    if float(frequency_cutoff) >= 1:
        frequency_cutoff = float(frequency_cutoff)/100
    else:
        frequency_cutoff = float(frequency_cutoff)

    SB = pt.search_hbonds(traj, distance=param_SB_distance, angle=param_SB_angle, options="acceptormask :GLU,ASP donormask :LYS,ARG")
    nb_SB = len(SB.values) - 1

    SB_id = np.array([]) ; SB_acc = np.array([]) ; SB_don = np.array([])

    for i in range(nb_SB):
        SB_temp = SB.get_amber_mask()[1][i].split(" ")
        SB_acc = np.append(SB_acc, SB_temp[0])
        SB_don = np.append(SB_don, SB_temp[2])
        SB_id = np.append(SB_id, SB_temp[0].split("@")[0][1:] + "-" + SB_temp[2].split("@")[0][1:])

    SB_id_unique = np.unique(SB_id)

    # Fusion des SB avec des DonH differents
    for i in range(len(SB_id_unique)):
        # Recup index des doublons potentiels & Ajout 1 à tous les index pour SB.data
        index_temp = np.where(SB_id == SB_id_unique[i])[0]
        data_temp = np.array(SB.data[index_temp+1])

        if len(data_temp) == 1:
            SB_frequency = round(np.sum(data_temp) / traj.n_frames, 3)
        else:
            SB_frequency = round(len(np.where(data_temp.sum(axis=0) > 0)[0]) / traj.n_frames, 3)

        if SB_frequency >= float(frequency_cutoff):
            output_SB.append([SB_acc[index_temp[0]], SB_don[index_temp[0]], SB_id[index_temp[0]], SB_frequency])

    return output_SB

#######################################################################################################################~

def SINAPs_output_SB(traj1, traj2, output_SB_traj1, output_SB_traj2, path, prefix):
    # output_SB = ACC / DON / ID / FREQ
    output_liste = []
    SB1_list = [elem[2] for elem in output_SB_traj1]
    SB2_list = [elem[2] for elem in output_SB_traj2]

    for i in range(len(SB1_list)):
        SB1 = SB1_list[i]
        if SB1 in SB2_list:
            output_liste.append(output_SB_traj1[i] + [output_SB_traj2[SB2_list.index(SB1)][3]])
        else:
            output_liste.append(output_SB_traj1[i] + [-1])

    for i in range(len(SB2_list)):
        SB2 = SB2_list[i]
        if SB2 not in SB1_list:
            output_liste.append(output_SB_traj2[i][0:3] + [-1] + [output_SB_traj2[i][3]])

    ###########################################

    # LIGANDS TRAJ1
    ligands1 = []
    for i in range(traj1.top.n_residues):
        if traj1.top.residue(i).name not in RESIDUES:
            ligands1.append(i + 1)

    # LIGANDS TRAJ2
    ligands2 = []
    for i in range(traj2.top.n_residues):
        if traj2.top.residue(i).name not in RESIDUES:
            ligands2.append(i + 1)

    ###########################################

    topo1 = traj1["(@CA,C,O,N)|(!:ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,HIE,HID,HIP,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL)"].top
    topo2 = traj2["(@CA,C,O,N)|(!:ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,HIE,HID,HIP,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL)"].top

    ###########################################

    # TRANSFORMATION CHAINES LAT EN CA
    with open("{0}/Results_SB_{1}.csv".format(path, prefix), "w") as write_output:
        for SB in output_liste:
            acceptor = "{0}@CA".format(SB[0].split("@")[0])
            donor = "{0}@CA".format(SB[1].split("@")[0])

            if SB[3] == -1:
                pos_traj1_acceptor = -1
                pos_traj1_donor = -1
            else:
                pos_traj1_acceptor = pt.select_atoms(topo1, acceptor)[0]
                pos_traj1_donor = pt.select_atoms(topo1, donor)[0]

            if SB[4] == -1:
                pos_traj2_acceptor = -1
                pos_traj2_donor = -1
            else:
                pos_traj2_acceptor = pt.select_atoms(topo2, acceptor)[0]
                pos_traj2_donor = pt.select_atoms(topo2, donor)[0]

            write_output.write("{0} {1} {2} {3} {4} {5} {6} {7}\n".format(acceptor, donor, pos_traj1_acceptor, pos_traj1_donor, pos_traj2_acceptor, pos_traj2_donor, SB[3], SB[4]))


#######################################################################################################################~

def SINAPs_aro_aro(traj, P_dist_min, P_dist_max, P_angle_max, TS_dist_min, TS_dist_max):
    traj_residues = np.array([i.name for i in traj.top.residues])
    traj_aro = []

    ########################################~

    P_dist_min = float(P_dist_min)
    P_dist_max = float(P_dist_max)
    P_angle_max = float(P_angle_max)
    TS_dist_min = float(TS_dist_min)
    TS_dist_max = float(TS_dist_max)

    ########################################~

    # TYROSINE
    traj_TYR = np.where("TYR" == traj_residues)[0]
    for i in traj_TYR:
        traj_aro.append(":{0}@CG,CD1,CD2,CE1,CE2,CZ".format(i + 1))

    # PHENYLALANINE
    traj_PHE = np.where("PHE" == traj_residues)[0]
    for i in traj_PHE:
        traj_aro.append(":{0}@CG,CD1,CD2,CE1,CE2,CZ".format(i + 1))

    # HISTIDINE
    traj_HIS = np.where("HIS" == traj_residues)[0]
    for i in traj_HIS:
        traj_aro.append(":{0}@CG,ND1,CD2,CE1,NE2".format(i + 1))

    # TRYPTOPHAN
    traj_TRP = np.where("TRP" == traj_residues)[0]
    for i in traj_TRP:
        traj_aro.append(":{0}@CG,CD1,CD2,NE1,CE2,CE3,CZ2,CZ3,CH2".format(i + 1))

    ########################################~

    aro_analysis = {}

    ########################################~

    for combination_aro in combinations(traj_aro, 2):
        # Distances
        temp_distance = pt.distance(traj, "{0} {1}".format(combination_aro[0], combination_aro[1]))

        if temp_distance.any() == None:
            continue

        temp_distance_min = min(temp_distance)

        if temp_distance_min > float(TS_dist_max):
            continue
        else:
            temp_corrplane1 = pt.vector.corrplane(traj, combination_aro[0])
            temp_corrplane2 = pt.vector.corrplane(traj, combination_aro[1])
            temp_centers_vector = pt.vector.vector(traj, "{0} {1}".format(combination_aro[0], combination_aro[1]))

            # Planar angle
            temp_planar_angle = []
            for i,j in zip(temp_corrplane1, temp_corrplane2):
                temp_cos = np.dot(i, j) / (np.linalg.norm(i) * np.linalg.norm(j))
                temp_angle = np.rad2deg(np.arccos(np.clip(temp_cos, -1, 1)))
                if temp_angle > 90:
                    temp_planar_angle.append(180 - temp_angle)
                else:
                    temp_planar_angle.append(temp_angle)

            # Orientation angle
            temp_orientation_angle = []
            for i, j in zip(temp_corrplane1, temp_centers_vector):
                temp_cos = np.dot(i, j) / (np.linalg.norm(i) * np.linalg.norm(j))
                temp_angle = np.rad2deg(np.arccos(np.clip(temp_cos, -1, 1)))
                if temp_angle > 90:
                    temp_orientation_angle.append(180 - temp_angle)
                else:
                    temp_orientation_angle.append(temp_angle)

            # Summary
            summary = {"Frames":0, "Pi-Stacking":0, "T-Shape":0, "L-Shape":0}
            for distance_frame, planar_frame, orientation_frame in zip(temp_distance, temp_planar_angle, temp_orientation_angle):
                # Pi-Stacking
                if 0 <= planar_frame < 20:
                    if P_dist_min < distance_frame < P_dist_max:
                        if 0 <= orientation_frame < P_angle_max:
                            summary["Frames"] += 1
                            summary["Pi-Stacking"] += 1
                        else:
                            summary["Frames"] += 1
                    else:
                        summary["Frames"] += 1

                elif 60 < planar_frame <= 90:
                    if TS_dist_min < distance_frame < TS_dist_max:
                        if 60 <= orientation_frame < 90:
                            summary["Frames"] += 1
                            summary["T-Shape"] += 1
                        elif 30 <= orientation_frame < 60:
                            summary["Frames"] += 1
                            summary["L-Shape"] += 1
                        elif 0 <= orientation_frame < 30:
                            summary["Frames"] += 1
                            summary["T-Shape"] += 1
                        else:
                            summary["Frames"] += 1
                    else:
                        summary["Frames"] += 1

                else:
                    summary["Frames"] += 1

            aro_analysis["{0} {1}".format(combination_aro[0].split("@")[0], combination_aro[1].split("@")[0])] = summary

    return aro_analysis


#######################################################################################################################~

def output_aro_SINAPs(output_aro_traj1, output_aro_traj2, traj1, traj2, path, suffix):
    with open("{0}/Results_Aro_{1}.csv".format(path, suffix), "w") as write_output:
        names = ["AA1", "AA2",
                 "Pos_AA1_Traj1", "Pos_AA2_Traj1", "Pos_AA1_Traj2", "Pos_AA2_Traj2",
                 "Freq_Aro_Traj1", "Freq_Aro_Traj2",
                 "Freq_PiStacking_Traj1", "Freq_PiStacking_Traj2",
                 "Freq_LT_Shapes_Traj1", "Freq_LT_Shapes_Traj2",
                 "Freq_T_Shape_Traj1", "Freq_T_Shape_Traj2",
                 "Freq_L_Shape_Traj1", "Freq_L_Shape_Traj2"]
        write_output.write(" ".join(names) + "\n")

        traj1_keys = list(output_aro_traj1.keys())
        traj2_keys = list(output_aro_traj2.keys())

        topo1 = traj1["(@CA,C,O,N)|(!:ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,HIE,HID,HIP,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL)"].top
        topo2 = traj2["(@CA,C,O,N)|(!:ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,HIE,HID,HIP,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL)"].top

        for aro in np.unique(traj1_keys + traj2_keys):
            AA1 = aro.split(" ")[0] + "@CA"
            AA2 = aro.split(" ")[1] + "@CA"

            # Traj1
            try: output_aro_traj1[aro]
            except:
                    pos_traj1_AA1 = -1 ; pos_traj1_AA2 = -1
                    Aro_traj1 = -1 ; Pi_Stacking_traj1 = -1 ; LT_Shape_traj1 = -1 ; T_Shape_traj1 = -1 ; L_Shape_traj1 = -1
            else:
                Aro_traj1 = (output_aro_traj1[aro]["Pi-Stacking"] + output_aro_traj1[aro]["T-Shape"] + output_aro_traj1[aro]["L-Shape"]) / output_aro_traj1[aro]["Frames"]

                if Aro_traj1 == 0:
                    pos_traj1_AA1 = -1 ; pos_traj1_AA2 = -1
                    Aro_traj1 = -1 ; Pi_Stacking_traj1 = -1 ; LT_Shape_traj1 = -1 ; T_Shape_traj1 = -1 ; L_Shape_traj1 = -1
                else:
                    pos_traj1_AA1 = pt.select_atoms(topo1, AA1)[0]
                    pos_traj1_AA2 = pt.select_atoms(topo1, AA2)[0]
                    Pi_Stacking_traj1 = output_aro_traj1[aro]["Pi-Stacking"] / output_aro_traj1[aro]["Frames"]
                    LT_Shape_traj1 = (output_aro_traj1[aro]["T-Shape"] + output_aro_traj1[aro]["L-Shape"]) / output_aro_traj1[aro]["Frames"]
                    T_Shape_traj1 = output_aro_traj1[aro]["T-Shape"] / output_aro_traj1[aro]["Frames"]
                    L_Shape_traj1 = output_aro_traj1[aro]["L-Shape"] / output_aro_traj1[aro]["Frames"]

            # Traj2
            try: output_aro_traj2[aro]
            except:
                pos_traj2_AA1 = -1 ; pos_traj2_AA2 = -1
                Aro_traj2 = -1 ; Pi_Stacking_traj2 = -1 ; LT_Shape_traj2 = -1 ; T_Shape_traj2 = -1 ; L_Shape_traj2 = -1
            else:
                Aro_traj2 = (output_aro_traj2[aro]["Pi-Stacking"] + output_aro_traj2[aro]["T-Shape"] + output_aro_traj2[aro]["L-Shape"]) / output_aro_traj2[aro]["Frames"]

                if Aro_traj1 == 0:
                    pos_traj2_AA1 = -1 ; pos_traj2_AA2 = -1
                    Aro_traj2 = -1 ; Pi_Stacking_traj2 = -1 ; LT_Shape_traj2 = -1 ; T_Shape_traj2 = -1 ; L_Shape_traj2 = -1
                else:
                    pos_traj2_AA1 = pt.select_atoms(topo2, AA1)[0]
                    pos_traj2_AA2 = pt.select_atoms(topo2, AA2)[0]
                    Pi_Stacking_traj2 = output_aro_traj2[aro]["Pi-Stacking"] / output_aro_traj2[aro]["Frames"]
                    LT_Shape_traj2 = (output_aro_traj2[aro]["T-Shape"] + output_aro_traj2[aro]["L-Shape"]) / output_aro_traj2[aro]["Frames"]
                    T_Shape_traj2 = output_aro_traj2[aro]["T-Shape"] / output_aro_traj2[aro]["Frames"]
                    L_Shape_traj2 = output_aro_traj2[aro]["L-Shape"] / output_aro_traj2[aro]["Frames"]

            if (Aro_traj1 <= 0) & (Aro_traj2 <= 0):
                continue
            else:
                # Summary
                summary = [Aro_traj1, Aro_traj2,
                           Pi_Stacking_traj1, Pi_Stacking_traj2,
                           LT_Shape_traj1, LT_Shape_traj2,
                           T_Shape_traj1, T_Shape_traj2,
                           L_Shape_traj1, L_Shape_traj2]

                summary = [AA1, AA2] + \
                          [str(pos_traj1_AA1), str(pos_traj1_AA2), str(pos_traj2_AA1), str(pos_traj2_AA2)] + \
                          [str(round(i, 4)) for i in summary]

                write_output.write(" ".join(summary) + "\n")

#######################################################################################################################~
