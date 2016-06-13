#!/user/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from copy import deepcopy


class Hungarian():

    def __init__(self, mat, is_maximize=True):
        self.orgn_mat = deepcopy(mat)
        self.mat = deepcopy(mat)
        self.match = np.zeros(self.mat.shape[0]) - 1
        if is_maximize:
            self.__convert_mat_for_maximize()
        self.calc()

    def __convert_mat_for_maximize(self):
        max = self.mat.max()
        self.mat = max - self.mat

    def calc(self):
        self.__sub_min_element()
        while np.any(self.match == -1):
            self.__detect_matching()

    def __sub_min_element(self):
        ncol, nrow = self.mat.shape
        for i in range(ncol):
            min = self.mat[i].min()
            self.mat[i] = self.mat[i] - min
        for i in range(nrow):
            min = self.mat[:,i].min()
            self.mat[:,i] = self.mat[:,i] - min

    def __detect_matching(self):
        ncol, nrow = self.mat.shape
        col, row = np.where(self.mat == 0)
        for c, r in zip(col, row):
            if self.match[c] != -1:
                continue
            nnonzero = np.count_nonzero(self.mat[c])
            can_allocate = [ True \
                             if v == 0 and i not in self.match \
                             else False \
                             for i, v in enumerate(self.mat[c]) ]
            nzero = can_allocate.count(True)
            if nzero == 1:
                self.match[c] = r

    def get_matrix(self):
        return self.mat

    def get_matching(self):
        return self.match

if __name__ == '__main__':
    #mat = np.array([[7, 4, 6],
    #                [2, 6, 8],
    #                [6, 9, 1]])
    mat = np.array([[7, 4, 6, 8],
                    [2, 6, 8, 9],
                    [6, 9, 1, 10],
                    [1, 5, 7, 9]])
    ins_hngr = Hungarian(mat)
    print(ins_hngr.get_matrix())
    print(ins_hngr.get_matching())
