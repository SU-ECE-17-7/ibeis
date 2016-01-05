# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import utool as ut
import six
from ibeis.algo.hots import hstypes
print, rrr, profile = ut.inject2(__name__, '[old_chip_match]')


class _OldStyleChipMatchSimulator(object):
    # SIMULATE OLD CHIPMATCHES UNTIL TRANSFER IS COMPLETE
    # TRY NOT TO USE THESE AS THEY WILL BE MUCH SLOWER THAN
    # NORMAL.
    _oldfields = ('aid2_fm', 'aid2_fsv', 'aid2_fk', 'aid2_score', 'aid2_H')

    @classmethod
    def from_cmtup_old(cls, cmtup_old, qaid=None, fsv_col_lbls=None,
                       daid_list=None):
        """ convert QueryResult styles fields to ChipMatch style fields """

        (aid2_fm_, aid2_fsv_, aid2_fk_, aid2_score_, aid2_H_) = cmtup_old
        assert len(aid2_fsv_) == len(aid2_fm_), 'bad old cmtup_old'
        assert len(aid2_fk_) == len(aid2_fm_), 'bad old cmtup_old'
        assert (aid2_score_ is None or
                len(aid2_score_) == 0 or
                len(aid2_score_) == len(aid2_fm_)), 'bad old cmtup_old'
        assert aid2_H_ is None or len(aid2_H_) == len(aid2_fm_), (
            'bad old cmtup_old')
        if daid_list is None:
            daid_list = list(six.iterkeys(aid2_fm_))

        # WARNING: dict_take will not copy these default items
        # Maybe these should be separate instances for different items?
        _empty_fm  = np.empty((0, 2), dtype=hstypes.FM_DTYPE)
        _empty_fsv = np.empty((0, 1), dtype=hstypes.FS_DTYPE)
        _empty_fk  = np.empty((0), dtype=hstypes.FK_DTYPE)
        # convert dicts to lists
        fm_list    = ut.dict_take(aid2_fm_, daid_list, _empty_fm)
        fsv_list   = ut.dict_take(aid2_fsv_, daid_list, _empty_fsv)
        fk_list    = ut.dict_take(aid2_fk_, daid_list, _empty_fk)
        no_scores = (aid2_score_ is None or
                      (len(aid2_score_) == 0 and len(daid_list) > 0))
        score_list = (
            None if no_scores else
            np.array(ut.dict_take(aid2_score_, daid_list, np.nan))
        )
        H_list = (
            None if aid2_H_ is None else
            ut.dict_take(aid2_H_, daid_list, None)
        )
        fsv_col_lbls = fsv_col_lbls
        cm = cls(qaid, daid_list, fm_list, fsv_list, fk_list, score_list,
                 H_list, fsv_col_lbls)
        return cm

    def __iter__(cm):
        for field in cm._oldfields:
            yield getattr(cm, field)

    def __getitem__(cm, index):
        if isinstance(index, six.string_types):
            return cm.__dict__[index]
        else:
            return getattr(cm, cm._oldfields[index])

    def _asdict(cm):
        return ut.odict(
            [(field, None if  getattr(cm, field) is None else getattr(cm, field).copy())
                for field in cm._oldfields])

    @property
    def aid2_fm(cm):
        return ut.AlignedListDictProxy(cm.daid2_idx, cm.daid_list, cm.fm_list)

    @property
    def aid2_fsv(cm):
        return ut.AlignedListDictProxy(cm.daid2_idx, cm.daid_list, cm.fsv_list)

    @property
    def aid2_fk(cm):
        return ut.AlignedListDictProxy(cm.daid2_idx, cm.daid_list, cm.fk_list)

    @property
    def aid2_H(cm):
        return (None if cm.H_list is None else
                ut.AlignedListDictProxy(cm.daid2_idx, cm.daid_list, cm.H_list))

    @property
    def aid2_score(cm):
        return ({} if cm.score_list is None else
                ut.AlignedListDictProxy(cm.daid2_idx, cm.daid_list, cm.score_list))

    # qres compatibility

    @property
    def filtkey_list(cm):
        """ for compatibility with qres """
        return cm.fsv_col_lbls

    @property
    def aid2_fs(cm):
        if cm.fs_list is None:
            fs_list = cm.get_fsv_prod_list()
        else:
            fs_list = cm.fs_list
        return ut.AlignedListDictProxy(cm.daid2_idx, cm.daid_list, fs_list)

    @property
    def nid2_name_score(cm):
        return ({} if cm.score_list is None else
                ut.AlignedListDictProxy(cm.nid2_nidx, cm.unique_nids, cm.name_score_list))

    def get_nscoretup(cm):
        return cm.get_ranked_nids_and_aids()

    def tokwargs(cm):
        """
        Can be unpacked and passed as kwargs
        **cm.tokwargs()
        """
        return ut.KwargsWrapper(cm)