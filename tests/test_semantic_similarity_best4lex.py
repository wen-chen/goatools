#!/usr/bin/env python
"""Computing basic semantic similarities between GO terms."""

from __future__ import print_function

import os
import itertools
from goatools.base import get_godag
from goatools.associations import dnld_assc
from goatools.semantic import TermCounts
from goatools.semantic import get_info_content
from goatools.semantic import resnik_sim
from goatools.semantic import lin_sim

def test_semantic_similarity():
    """Computing basic semantic similarities between GO terms."""
    goids = [
        "GO:0140101",
        "GO:0140097",
        "GO:0140096",
        "GO:0140098",
        "GO:0015318",
        "GO:0140110",
    ]
    # Get all the annotations from arabidopsis.
    associations = [
        ('human', 'goa_human.gaf'),
        ('yeast', 'gene_association.sgd'),
    ]


    cwd = os.getcwd()  # current working directory
    godag = get_godag(os.path.join(os.getcwd(), "go-basic.obo"), loading_bar=None)
    for species, assc_name in associations:  # Limit test numbers for speed
        print()
        # Get all the annotations for the current species
        assc_gene2gos = dnld_assc(os.path.join(cwd, assc_name), godag, prt=None)
        # Calculate the information content of the single term, GO:0048364
        termcounts = TermCounts(godag, assc_gene2gos)

        # Print information values for each GO term
        for goid in sorted(goids):
            infocontent = get_info_content(goid, termcounts)
            print('{SPECIES} Information content {INFO:8.6f} {GO} {NAME}'.format(
                SPECIES=species, GO=goid, INFO=infocontent, NAME=godag[goid].name))

        # Print semantic similarities between each pair of GO terms
        print("GO #1      GO #2      Resnik Lin")
        print("---------- ---------- ------ -------")
        for go_a, go_b in itertools.combinations(sorted(goids), 2):
            # Resnik's similarity measure is defined as the information content of the most
            # informative common ancestor. That is, the most specific common parent-term in the GO.
            sim_r = resnik_sim(go_a, go_b, godag, termcounts)
            # Lin similarity score (GO:0048364, GO:0044707) = -0.607721957763
            sim_l = lin_sim(go_a, go_b, godag, termcounts)
            print('{GO1} {GO2} {RESNIK:6.4f} {LIN:7.4f}'.format(
                GO1=go_a, GO2=go_b, RESNIK=sim_r, LIN=sim_l))
            assert sim_r, "FATAL RESNIK SCORE"
            assert sim_l, "FATAL LIN SCORE"




if __name__ == '__main__':
    test_semantic_similarity()
