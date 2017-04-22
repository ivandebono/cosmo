#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 1 Feb 2017

@author: Ivan Debono

Display essential Fisher matrix quantities in column form

INPUT
fisher : Fisher matrix structure from cosmo

SCREEN OUTPUT 
Parameter name | Parameter fiducial value | Marginalised error
"""


def display_fisher(fisher):

    print("{: >20} {: >20} {: >20}".format('Parameter','Fiducial value','sigma_marg'))
    for i,j,k in zip(fisher['parameters'],fisher['p'],fisher['sigma_marg']): print("{: >20} {: >20} {: >20}".format(i,j,k))
