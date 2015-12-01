# -*- coding: utf-8 -*-
"""
Autogenerated IBEISController functions

TemplateInfo:
    autogen_time = 12:00:13 2015/12/01
    autogen_key = annotmatch

ToRegenerate:
    python -m ibeis.templates.template_generator --key annotmatch --Tcfg with_web_api=False with_api_cache=False with_deleters=True no_extern_deleters=True --diff
    python -m ibeis.templates.template_generator --key annotmatch --Tcfg with_web_api=False with_api_cache=False with_deleters=True no_extern_deleters=True --write
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import functools  # NOQA
import six  # NOQA
from six.moves import map, range, zip  # NOQA
from ibeis import constants as const
import utool as ut
from ibeis.control import controller_inject
from ibeis.control import accessor_decors  # NOQA
print, rrr, profile = ut.inject2(__name__, '[autogen_annotmatch]')


if ut.VERYVERBOSE:
    import itertools
    x = itertools.count().next
    print('DEBUG: PRE IMPORTING _AUTOGEN ANNOTMATCH FUNCS %s' % (x(),))

# Create dectorator to inject functions in this module into the IBEISController
CLASS_INJECT_KEY, register_ibs_method = controller_inject.make_ibs_register_decorator(__name__)


if ut.VERYVERBOSE:
    print('DEBUG: POST1 IMPORTING _AUTOGEN ANNOTMATCH FUNCS %s' % (x(),))


register_api   = controller_inject.get_ibeis_flask_api(__name__)
register_route = controller_inject.get_ibeis_flask_route(__name__)

if ut.VERYVERBOSE:
    print('DEBUG: IMPORTING _AUTOGEN ANNOTMATCH FUNCS %s' % (x(),))


def testdata_annotmatch(defaultdb='testdb1'):
    import ibeis
    ibs = ibeis.opendb(defaultdb=defaultdb)
    config2_ = None  # qreq_.qparams
    #from ibeis.hots import query_config
    #config2_ = query_config.QueryParams(cfgdict=dict())
    return ibs, config2_

# AUTOGENED CONSTANTS:
ANNOTMATCH_CONFIDENCE      = 'annotmatch_confidence'
ANNOTMATCH_IS_HARD         = 'annotmatch_is_hard'
ANNOTMATCH_IS_NONDISTINCT  = 'annotmatch_is_nondistinct'
ANNOTMATCH_IS_PHOTOBOMB    = 'annotmatch_is_photobomb'
ANNOTMATCH_IS_SCENERYMATCH = 'annotmatch_is_scenerymatch'
ANNOTMATCH_NOTE            = 'annotmatch_note'
ANNOTMATCH_REVIEWED        = 'annotmatch_reviewed'
ANNOTMATCH_REVIEWER        = 'annotmatch_reviewer'
ANNOTMATCH_ROWID           = 'annotmatch_rowid'
ANNOTMATCH_TRUTH           = 'annotmatch_truth'
ANNOT_ROWID1               = 'annot_rowid1'
ANNOT_ROWID2               = 'annot_rowid2'
CONFIG_ROWID               = 'config_rowid'
FEATWEIGHT_ROWID           = 'featweight_rowid'

if ut.VERYVERBOSE:
    print('DEBUG: IMPORTING _AUTOGEN ANNOTMATCH FUNCS %s' % (x(),))

@register_ibs_method
def _get_all_annotmatch_rowids(ibs):
    r""" all_annotmatch_rowids <- annotmatch.get_all_rowids()

    Returns:
        list_ (list): unfiltered annotmatch_rowids

    TemplateInfo:
        Tider_all_rowids
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> ibs._get_all_annotmatch_rowids()
    """
    all_annotmatch_rowids = ibs.db.get_all_rowids(const.ANNOTMATCH_TABLE)
    return all_annotmatch_rowids


if ut.VERYVERBOSE:
    print('DEBUG: ADD IMPORTING _AUTOGEN ANNOTMATCH FUNCS %s' % (x(),))

@register_ibs_method
def add_annotmatch(ibs, aid1_list, aid2_list, annotmatch_truth_list=None, annotmatch_confidence_list=None, annotmatch_is_hard_list=None, annotmatch_is_scenerymatch_list=None, annotmatch_is_photobomb_list=None, annotmatch_is_nondistinct_list=None, annotmatch_note_list=None, annotmatch_reviewed_list=None, annotmatch_reviewer_list=None):
    r"""
    Returns:
        returns annotmatch_rowid_list of added (or already existing annotmatchs)

    TemplateInfo:
        Tadder_native
        tbl = annotmatch
    """
    # WORK IN PROGRESS
    colnames = (ANNOT_ROWID1, ANNOT_ROWID2, ANNOTMATCH_TRUTH, ANNOTMATCH_CONFIDENCE, ANNOTMATCH_IS_HARD, ANNOTMATCH_IS_SCENERYMATCH,
                ANNOTMATCH_IS_PHOTOBOMB, ANNOTMATCH_IS_NONDISTINCT, ANNOTMATCH_NOTE, ANNOTMATCH_REVIEWED, ANNOTMATCH_REVIEWER,)
    if annotmatch_truth_list is None:
        annotmatch_truth_list = [None] * len(aid1_list)
    if annotmatch_confidence_list is None:
        annotmatch_confidence_list = [None] * len(aid1_list)
    if annotmatch_is_hard_list is None:
        annotmatch_is_hard_list = [None] * len(aid1_list)
    if annotmatch_is_scenerymatch_list is None:
        annotmatch_is_scenerymatch_list = [None] * len(aid1_list)
    if annotmatch_is_photobomb_list is None:
        annotmatch_is_photobomb_list = [None] * len(aid1_list)
    if annotmatch_is_nondistinct_list is None:
        annotmatch_is_nondistinct_list = [None] * len(aid1_list)
    if annotmatch_note_list is None:
        annotmatch_note_list = [None] * len(aid1_list)
    if annotmatch_reviewed_list is None:
        annotmatch_reviewed_list = [None] * len(aid1_list)
    if annotmatch_reviewer_list is None:
        annotmatch_reviewer_list = [None] * len(aid1_list)
    params_iter = (
        (aid1, aid2, annotmatch_truth, annotmatch_confidence, annotmatch_is_hard, annotmatch_is_scenerymatch,
         annotmatch_is_photobomb, annotmatch_is_nondistinct, annotmatch_note, annotmatch_reviewed, annotmatch_reviewer,)
        for (aid1, aid2, annotmatch_truth, annotmatch_confidence, annotmatch_is_hard, annotmatch_is_scenerymatch, annotmatch_is_photobomb, annotmatch_is_nondistinct, annotmatch_note, annotmatch_reviewed, annotmatch_reviewer,) in
        zip(aid1_list, aid2_list, annotmatch_truth_list, annotmatch_confidence_list, annotmatch_is_hard_list, annotmatch_is_scenerymatch_list,
            annotmatch_is_photobomb_list, annotmatch_is_nondistinct_list, annotmatch_note_list, annotmatch_reviewed_list, annotmatch_reviewer_list)
    )
    get_rowid_from_superkey = ibs.get_annotmatch_rowid_from_superkey
    # FIXME: encode superkey paramx
    superkey_paramx = (0, 1)
    annotmatch_rowid_list = ibs.db.add_cleanly(
        const.ANNOTMATCH_TABLE, colnames, params_iter, get_rowid_from_superkey, superkey_paramx)
    return annotmatch_rowid_list


if ut.VERYVERBOSE:
    print('DEBUG: DEL IMPORTING _AUTOGEN ANNOTMATCH FUNCS %s' % (x(),))

@register_ibs_method
def delete_annotmatch(ibs, annotmatch_rowid_list, config2_=None):
    r""" annotmatch.delete(annotmatch_rowid_list)

    delete annotmatch rows

    Args:
        annotmatch_rowid_list

    Returns:
        int: num_deleted

    TemplateInfo:
        Tdeleter_native_tbl
        tbl = annotmatch

    Example:
        >>> # DISABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()[:2]
        >>> num_deleted = ibs.delete_annotmatch(annotmatch_rowid_list)
        >>> print('num_deleted = %r' % (num_deleted,))
    """
    #from ibeis.model.preproc import preproc_annotmatch
    # NO EXTERN IMPORT
    if ut.VERBOSE:
        print('[ibs] deleting %d annotmatch rows' % len(annotmatch_rowid_list))
    # Prepare: Delete externally stored data (if any)
    #preproc_annotmatch.on_delete(ibs, annotmatch_rowid_list, config2_=config2_)
    # NO EXTERN DELETE
    # Finalize: Delete self
    ibs.db.delete_rowids(const.ANNOTMATCH_TABLE, annotmatch_rowid_list)
    num_deleted = len(ut.filter_Nones(annotmatch_rowid_list))
    return num_deleted


if ut.VERYVERBOSE:
    print('DEBUG: GET IMPORTING _AUTOGEN ANNOTMATCH FUNCS %s' % (x(),))

@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_aid1(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" aid1_list <- annotmatch.aid1[annotmatch_rowid_list]

    gets data from the "native" column "aid1" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: aid1_list

    TemplateInfo:
        Tgetter_table_column
        col = aid1
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> aid1_list = ibs.get_annotmatch_aid1(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(aid1_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOT_ROWID1,)
    aid1_list = ibs.db.get(const.ANNOTMATCH_TABLE, colnames,
                           id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return aid1_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_aid2(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" aid2_list <- annotmatch.aid2[annotmatch_rowid_list]

    gets data from the "native" column "aid2" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: aid2_list

    TemplateInfo:
        Tgetter_table_column
        col = aid2
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> aid2_list = ibs.get_annotmatch_aid2(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(aid2_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOT_ROWID2,)
    aid2_list = ibs.db.get(const.ANNOTMATCH_TABLE, colnames,
                           id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return aid2_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_confidence(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_confidence_list <- annotmatch.annotmatch_confidence[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_confidence" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_confidence_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_confidence
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_confidence_list = ibs.get_annotmatch_confidence(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_confidence_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_CONFIDENCE,)
    annotmatch_confidence_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_confidence_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_is_hard(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_is_hard_list <- annotmatch.annotmatch_is_hard[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_is_hard" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_is_hard_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_is_hard
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_is_hard_list = ibs.get_annotmatch_is_hard(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_is_hard_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_IS_HARD,)
    annotmatch_is_hard_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_is_hard_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_is_nondistinct(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_is_nondistinct_list <- annotmatch.annotmatch_is_nondistinct[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_is_nondistinct" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_is_nondistinct_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_is_nondistinct
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_is_nondistinct_list = ibs.get_annotmatch_is_nondistinct(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_is_nondistinct_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_IS_NONDISTINCT,)
    annotmatch_is_nondistinct_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_is_nondistinct_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_is_photobomb(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_is_photobomb_list <- annotmatch.annotmatch_is_photobomb[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_is_photobomb" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_is_photobomb_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_is_photobomb
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_is_photobomb_list = ibs.get_annotmatch_is_photobomb(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_is_photobomb_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_IS_PHOTOBOMB,)
    annotmatch_is_photobomb_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_is_photobomb_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_is_scenerymatch(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_is_scenerymatch_list <- annotmatch.annotmatch_is_scenerymatch[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_is_scenerymatch" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_is_scenerymatch_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_is_scenerymatch
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_is_scenerymatch_list = ibs.get_annotmatch_is_scenerymatch(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_is_scenerymatch_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_IS_SCENERYMATCH,)
    annotmatch_is_scenerymatch_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_is_scenerymatch_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_note(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_note_list <- annotmatch.annotmatch_note[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_note" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_note_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_note
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_note_list = ibs.get_annotmatch_note(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_note_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_NOTE,)
    annotmatch_note_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_note_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_reviewed(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_reviewed_list <- annotmatch.annotmatch_reviewed[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_reviewed" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_reviewed_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_reviewed
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_reviewed_list = ibs.get_annotmatch_reviewed(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_reviewed_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_REVIEWED,)
    annotmatch_reviewed_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_reviewed_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_reviewer(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_reviewer_list <- annotmatch.annotmatch_reviewer[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_reviewer" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_reviewer_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_reviewer
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_reviewer_list = ibs.get_annotmatch_reviewer(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_reviewer_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_REVIEWER,)
    annotmatch_reviewer_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_reviewer_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_rowid(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_rowid_list <- annotmatch.annotmatch_rowid[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_rowid" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_rowid_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_rowid
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_rowid_list = ibs.get_annotmatch_rowid(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_rowid_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_ROWID,)
    annotmatch_rowid_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_rowid_list


@register_ibs_method
def get_annotmatch_rowid_from_superkey(ibs, aid1_list, aid2_list, eager=True, nInput=None):
    r""" annotmatch_rowid_list <- annotmatch[aid1_list, aid2_list]

    Args:
        superkey lists: aid1_list, aid2_list

    Returns:
        annotmatch_rowid_list

    TemplateInfo:
        Tgetter_native_rowid_from_superkey
        tbl = annotmatch
    """
    colnames = (ANNOTMATCH_ROWID,)
    # FIXME: col_rowid is not correct
    params_iter = zip(aid1_list, aid2_list)
    andwhere_colnames = [ANNOT_ROWID1, ANNOT_ROWID2]
    annotmatch_rowid_list = ibs.db.get_where2(
        const.ANNOTMATCH_TABLE, colnames, params_iter, andwhere_colnames, eager=eager, nInput=nInput)
    return annotmatch_rowid_list


@register_ibs_method
@accessor_decors.getter_1to1
def get_annotmatch_truth(ibs, annotmatch_rowid_list, eager=True, nInput=None):
    r""" annotmatch_truth_list <- annotmatch.annotmatch_truth[annotmatch_rowid_list]

    gets data from the "native" column "annotmatch_truth" in the "annotmatch" table

    Args:
        annotmatch_rowid_list (list):

    Returns:
        list: annotmatch_truth_list

    TemplateInfo:
        Tgetter_table_column
        col = annotmatch_truth
        tbl = annotmatch

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control._autogen_annotmatch_funcs import *  # NOQA
        >>> ibs, config2_ = testdata_annotmatch()
        >>> annotmatch_rowid_list = ibs._get_all_annotmatch_rowids()
        >>> eager = True
        >>> annotmatch_truth_list = ibs.get_annotmatch_truth(annotmatch_rowid_list, eager=eager)
        >>> assert len(annotmatch_rowid_list) == len(annotmatch_truth_list)
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_TRUTH,)
    annotmatch_truth_list = ibs.db.get(
        const.ANNOTMATCH_TABLE, colnames, id_iter, id_colname='rowid', eager=eager, nInput=nInput)
    return annotmatch_truth_list

if ut.VERYVERBOSE:
    print('DEBUG: SET IMPORTING _AUTOGEN ANNOTMATCH FUNCS %s' % (x(),))

@register_ibs_method
@accessor_decors.setter
def set_annotmatch_confidence(ibs, annotmatch_rowid_list, annotmatch_confidence_list, duplicate_behavior='error'):
    r""" annotmatch_confidence_list -> annotmatch.annotmatch_confidence[annotmatch_rowid_list]

    Args:
        annotmatch_rowid_list
        annotmatch_confidence_list

    TemplateInfo:
        Tsetter_native_column
        tbl = annotmatch
        col = annotmatch_confidence
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_CONFIDENCE,)
    ibs.db.set(const.ANNOTMATCH_TABLE, colnames, annotmatch_confidence_list,
               id_iter, duplicate_behavior=duplicate_behavior)


@register_ibs_method
@accessor_decors.setter
def set_annotmatch_is_hard(ibs, annotmatch_rowid_list, annotmatch_is_hard_list, duplicate_behavior='error'):
    r""" annotmatch_is_hard_list -> annotmatch.annotmatch_is_hard[annotmatch_rowid_list]

    Args:
        annotmatch_rowid_list
        annotmatch_is_hard_list

    TemplateInfo:
        Tsetter_native_column
        tbl = annotmatch
        col = annotmatch_is_hard
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_IS_HARD,)
    ibs.db.set(const.ANNOTMATCH_TABLE, colnames, annotmatch_is_hard_list,
               id_iter, duplicate_behavior=duplicate_behavior)


@register_ibs_method
@accessor_decors.setter
def set_annotmatch_is_nondistinct(ibs, annotmatch_rowid_list, annotmatch_is_nondistinct_list, duplicate_behavior='error'):
    r""" annotmatch_is_nondistinct_list -> annotmatch.annotmatch_is_nondistinct[annotmatch_rowid_list]

    Args:
        annotmatch_rowid_list
        annotmatch_is_nondistinct_list

    TemplateInfo:
        Tsetter_native_column
        tbl = annotmatch
        col = annotmatch_is_nondistinct
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_IS_NONDISTINCT,)
    ibs.db.set(const.ANNOTMATCH_TABLE, colnames, annotmatch_is_nondistinct_list,
               id_iter, duplicate_behavior=duplicate_behavior)


@register_ibs_method
@accessor_decors.setter
def set_annotmatch_is_photobomb(ibs, annotmatch_rowid_list, annotmatch_is_photobomb_list, duplicate_behavior='error'):
    r""" annotmatch_is_photobomb_list -> annotmatch.annotmatch_is_photobomb[annotmatch_rowid_list]

    Args:
        annotmatch_rowid_list
        annotmatch_is_photobomb_list

    TemplateInfo:
        Tsetter_native_column
        tbl = annotmatch
        col = annotmatch_is_photobomb
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_IS_PHOTOBOMB,)
    ibs.db.set(const.ANNOTMATCH_TABLE, colnames, annotmatch_is_photobomb_list,
               id_iter, duplicate_behavior=duplicate_behavior)


@register_ibs_method
@accessor_decors.setter
def set_annotmatch_is_scenerymatch(ibs, annotmatch_rowid_list, annotmatch_is_scenerymatch_list, duplicate_behavior='error'):
    r""" annotmatch_is_scenerymatch_list -> annotmatch.annotmatch_is_scenerymatch[annotmatch_rowid_list]

    Args:
        annotmatch_rowid_list
        annotmatch_is_scenerymatch_list

    TemplateInfo:
        Tsetter_native_column
        tbl = annotmatch
        col = annotmatch_is_scenerymatch
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_IS_SCENERYMATCH,)
    ibs.db.set(const.ANNOTMATCH_TABLE, colnames, annotmatch_is_scenerymatch_list,
               id_iter, duplicate_behavior=duplicate_behavior)


@register_ibs_method
@accessor_decors.setter
def set_annotmatch_note(ibs, annotmatch_rowid_list, annotmatch_note_list, duplicate_behavior='error'):
    r""" annotmatch_note_list -> annotmatch.annotmatch_note[annotmatch_rowid_list]

    Args:
        annotmatch_rowid_list
        annotmatch_note_list

    TemplateInfo:
        Tsetter_native_column
        tbl = annotmatch
        col = annotmatch_note
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_NOTE,)
    ibs.db.set(const.ANNOTMATCH_TABLE, colnames, annotmatch_note_list,
               id_iter, duplicate_behavior=duplicate_behavior)


@register_ibs_method
@accessor_decors.setter
def set_annotmatch_reviewed(ibs, annotmatch_rowid_list, annotmatch_reviewed_list, duplicate_behavior='error'):
    r""" annotmatch_reviewed_list -> annotmatch.annotmatch_reviewed[annotmatch_rowid_list]

    Args:
        annotmatch_rowid_list
        annotmatch_reviewed_list

    TemplateInfo:
        Tsetter_native_column
        tbl = annotmatch
        col = annotmatch_reviewed
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_REVIEWED,)
    ibs.db.set(const.ANNOTMATCH_TABLE, colnames, annotmatch_reviewed_list,
               id_iter, duplicate_behavior=duplicate_behavior)


@register_ibs_method
@accessor_decors.setter
def set_annotmatch_reviewer(ibs, annotmatch_rowid_list, annotmatch_reviewer_list, duplicate_behavior='error'):
    r""" annotmatch_reviewer_list -> annotmatch.annotmatch_reviewer[annotmatch_rowid_list]

    Args:
        annotmatch_rowid_list
        annotmatch_reviewer_list

    TemplateInfo:
        Tsetter_native_column
        tbl = annotmatch
        col = annotmatch_reviewer
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_REVIEWER,)
    ibs.db.set(const.ANNOTMATCH_TABLE, colnames, annotmatch_reviewer_list,
               id_iter, duplicate_behavior=duplicate_behavior)


@register_ibs_method
@accessor_decors.setter
def set_annotmatch_truth(ibs, annotmatch_rowid_list, annotmatch_truth_list, duplicate_behavior='error'):
    r""" annotmatch_truth_list -> annotmatch.annotmatch_truth[annotmatch_rowid_list]

    Args:
        annotmatch_rowid_list
        annotmatch_truth_list

    TemplateInfo:
        Tsetter_native_column
        tbl = annotmatch
        col = annotmatch_truth
    """
    id_iter = annotmatch_rowid_list
    colnames = (ANNOTMATCH_TRUTH,)
    ibs.db.set(const.ANNOTMATCH_TABLE, colnames, annotmatch_truth_list,
               id_iter, duplicate_behavior=duplicate_behavior)


if ut.VERYVERBOSE:
    print('DEBUG: END IMPORTING _AUTOGEN ANNOTMATCH FUNCS %s' % (x(),))

if __name__ == '__main__':
    r"""
    CommandLine:
        python -m ibeis.control._autogen_annotmatch_funcs
        python -m ibeis.control._autogen_annotmatch_funcs --allexamples
    """
    import multiprocessing
    multiprocessing.freeze_support()
    import utool as ut
    ut.doctest_funcs()
