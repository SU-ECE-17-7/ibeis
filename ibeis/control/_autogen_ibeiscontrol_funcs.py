"""
Autogenerated IBEISController functions

TemplateInfo:
    autogen_time = 18:41:47 2014/11/09

ToRegenerate:
    python ibeis/control/templates.py --dump-autogen-controller
"""
from __future__ import absolute_import, division, print_function
import functools  # NOQA
import six  # NOQA
from six.moves import map, range  # NOQA
from ibeis import constants
from ibeis.control.IBEISControl import IBEISController
import utool  # NOQA
import utool as ut  # NOQA
print, print_, printDBG, rrr, profile = ut.inject(__name__, '[autogen_ibsfuncs]')

# Create dectorator to inject these functions into the IBEISController
register_ibs_aliased_method   = ut.make_class_method_decorator((IBEISController, 'autogen'))
register_ibs_unaliased_method = ut.make_class_method_decorator((IBEISController, 'autogen'))


def register_ibs_method(func):
    aliastup = (func, 'autogen_' + ut.get_funcname(func))
    register_ibs_unaliased_method(func)
    register_ibs_aliased_method(aliastup)
    return func

# AUTOGENED CONSTANTS:
ANNOT_ROWID                 = 'annot_rowid'
CHIP_ROWID                  = 'chip_rowid'
CONFIG_ROWID                = 'config_rowid'
FEATWEIGHT_FORGROUND_WEIGHT = 'featweight_forground_weight'
FEATWEIGHT_ROWID            = 'featweight_rowid'
FEAT_ROWID                  = 'feature_rowid'
RESIDUAL_ROWID              = 'residual_rowid'
RESIDUAL_VECTOR             = 'residual_vector'
RVECS                       = 'rvecs'

# =========================
# 0_PL.TADDER METHODS
# =========================


@register_ibs_method
#@adder
def add_feat_featweights(ibs, fid_list, qreq_=None):
    """ feat.featweight.add(fid_list)

    CRITICAL FUNCTION MUST EXIST FOR ALL DEPENDANTS
    Adds / ensures / computes a dependant property

    Args:
         fid_list

    Returns:
        returns config_rowid of the current configuration

    TemplateInfo:
        Tadder_pl_dependant
        parent = feat
        leaf = featweight

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis
        >>> ibs = ibeis.opendb('testdb1')
        >>> fid_list = ibs.get_valid_fids()
        >>> qreq_ = None
        >>> featweight_rowid_list = ibs.add_feat_featweights(fid_list, qreq_=qreq_)
    """
    from ibeis.model.preproc import preproc_featweight
    # Get requested configuration id
    config_rowid = ibs.get_featweight_config_rowid(qreq_=qreq_)
    # Find leaf rowids that need to be computed
    featweight_rowid_list = get_feat_featweight_rowids_(
        ibs, fid_list, qreq_=qreq_)
    # Get corresponding "dirty" parent rowids
    dirty_fid_list = utool.get_dirty_items(fid_list, featweight_rowid_list)
    if len(dirty_fid_list) > 0:
        if utool.VERBOSE:
            print('[ibs] adding %d / %d featweight' %
                  (len(dirty_fid_list), len(fid_list)))
        # Dependant columns do not need true from_superkey getters.
        # We can use the Tgetter_pl_dependant_rowids_ instead
        get_rowid_from_superkey = functools.partial(
            ibs.get_feat_featweight_rowids_, qreq_=qreq_)
        fgweight_list = preproc_featweight.add_featweight_params_gen(
            ibs, fid_list)
        params_iter = ((fid, config_rowid, fgweight)
                       for fid, fgweight in
                       zip(fid_list, fgweight_list))
        colnames = [
            'feature_rowid', 'config_rowid', 'featweight_forground_weight']
        featweight_rowid_list = ibs.dbcache.add_cleanly(
            constants.FEATURE_WEIGHT_TABLE, colnames, params_iter, get_rowid_from_superkey)
    return featweight_rowid_list


@register_ibs_method
#@adder
def add_feat_residuals(ibs, fid_list, qreq_=None):
    """ feat.residual.add(fid_list)

    CRITICAL FUNCTION MUST EXIST FOR ALL DEPENDANTS
    Adds / ensures / computes a dependant property

    Args:
         fid_list

    Returns:
        returns config_rowid of the current configuration

    TemplateInfo:
        Tadder_pl_dependant
        parent = feat
        leaf = residual

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis
        >>> ibs = ibeis.opendb('testdb1')
        >>> fid_list = ibs.get_valid_fids()
        >>> qreq_ = None
        >>> residual_rowid_list = ibs.add_feat_residuals(fid_list, qreq_=qreq_)
    """
    from ibeis.model.preproc import preproc_residual
    # Get requested configuration id
    config_rowid = ibs.get_residual_config_rowid(qreq_=qreq_)
    # Find leaf rowids that need to be computed
    residual_rowid_list = get_feat_residual_rowids_(ibs, fid_list, qreq_=qreq_)
    # Get corresponding "dirty" parent rowids
    dirty_fid_list = utool.get_dirty_items(fid_list, residual_rowid_list)
    if len(dirty_fid_list) > 0:
        if utool.VERBOSE:
            print('[ibs] adding %d / %d residual' %
                  (len(dirty_fid_list), len(fid_list)))
        # Dependant columns do not need true from_superkey getters.
        # We can use the Tgetter_pl_dependant_rowids_ instead
        get_rowid_from_superkey = functools.partial(
            ibs.get_feat_residual_rowids_, qreq_=qreq_)
        residual_vector_list, rvecs_list = preproc_residual.add_residual_params_gen(
            ibs, fid_list)
        params_iter = ((fid, config_rowid, residual_vector, rvecs)
                       for fid, residual_vector, rvecs in
                       zip(fid_list, residual_vector_list, rvecs_list))
        colnames = ['feature_rowid', 'config_rowid', 'residual_vector']
        residual_rowid_list = ibs.dbcache.add_cleanly(
            constants.RESIDUAL_TABLE, colnames, params_iter, get_rowid_from_superkey)
    return residual_rowid_list


# =========================
# 0_PL.TGETTER_ROWIDS METHODS
# =========================


@register_ibs_method
#@getter
def get_feat_featweight_rowids(ibs, fid_list, qreq_=None, ensure=False):
    """ featweight_rowid_list <- feat.featweight.rowids[fid_list]

    get featweight rowids of feat under the current state configuration
    if ensure is True, this function is equivalent to add_feat_featweights

    Args:
        fid_list (list):
        ensure (bool): default false

    Returns:
        list: featweight_rowid_list

    TemplateInfo:
        Tgetter_pl_dependant_rowids
        parent = feat
        leaf = featweight

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis
        >>> ibs = ibeis.opendb('testdb1')
        >>> fid_list = ibs.get_valid_fids()
        >>> qreq_ = None
        >>> ensure = False
        >>> featweight_rowid_list = ibs.get_feat_featweight_rowids(fid_list, qreq_, ensure)
    """
    if ensure:
        featweight_rowid_list = add_feat_featweights(ibs, fid_list, qreq_=qreq_)
    else:
        featweight_rowid_list = get_feat_featweight_rowids_(
            ibs, fid_list, qreq_=qreq_)
    return featweight_rowid_list


@register_ibs_method
#@getter
def get_feat_residual_rowids(ibs, fid_list, qreq_=None, ensure=False):
    """ residual_rowid_list <- feat.residual.rowids[fid_list]

    get residual rowids of feat under the current state configuration
    if ensure is True, this function is equivalent to add_feat_residuals

    Args:
        fid_list (list):
        ensure (bool): default false

    Returns:
        list: residual_rowid_list

    TemplateInfo:
        Tgetter_pl_dependant_rowids
        parent = feat
        leaf = residual

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis
        >>> ibs = ibeis.opendb('testdb1')
        >>> fid_list = ibs.get_valid_fids()
        >>> qreq_ = None
        >>> ensure = False
        >>> residual_rowid_list = ibs.get_feat_residual_rowids(fid_list, qreq_, ensure)
    """
    if ensure:
        residual_rowid_list = add_feat_residuals(ibs, fid_list, qreq_=qreq_)
    else:
        residual_rowid_list = get_feat_residual_rowids_(
            ibs, fid_list, qreq_=qreq_)
    return residual_rowid_list


# =========================
# 0_PL.TGETTER_ROWIDS_ METHODS
# =========================


@register_ibs_method
#@getter
def get_feat_featweight_rowids_(ibs, fid_list, qreq_=None):
    """
    equivalent to get_feat_featweight_rowids_ except ensure cannot be specified

    You basically save a stack frame by calling this, because
    get_feat_featweight_rowids just calls this function if ensure is False
    """
    colnames = (FEATWEIGHT_ROWID,)
    config_rowid = ibs.get_featweight_config_rowid(qreq_=qreq_)
    andwhere_colnames = (FEAT_ROWID, CONFIG_ROWID,)
    params_iter = ((fid, config_rowid,) for fid in fid_list)
    featweight_rowid_list = ibs.dbcache.get_where2(
        constants.FEATURE_WEIGHT_TABLE, colnames, params_iter, andwhere_colnames)
    return featweight_rowid_list


@register_ibs_method
#@getter
def get_feat_residual_rowids_(ibs, fid_list, qreq_=None):
    """
    equivalent to get_feat_residual_rowids_ except ensure cannot be specified

    You basically save a stack frame by calling this, because
    get_feat_residual_rowids just calls this function if ensure is False
    """
    colnames = (RESIDUAL_ROWID,)
    config_rowid = ibs.get_residual_config_rowid(qreq_=qreq_)
    andwhere_colnames = (FEAT_ROWID, CONFIG_ROWID,)
    params_iter = ((fid, config_rowid,) for fid in fid_list)
    residual_rowid_list = ibs.dbcache.get_where2(
        constants.RESIDUAL_TABLE, colnames, params_iter, andwhere_colnames)
    return residual_rowid_list


# =========================
# 1_RL.TADDER METHODS
# =========================


@register_ibs_method
#@adder
def add_annot_featweights(ibs, aid_list, qreq_=None):
    """ featweight_rowid_list <- annot.featweight.ensure(aid_list)

    Adds / ensures / computes a dependant property
    returns config_rowid of the current configuration

    CONVENIENCE FUNCTION

    Args:
        aid_list

    TemplateInfo:
        Tadder_rl_dependant
        root = annot
        leaf = featweight

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis
        >>> ibs = ibeis.opendb('testdb1')
        >>> aid_list = ibs.get_valid_aids()
        >>> qreq_ = None
        >>> featweight_rowid_list = ibs.add_annot_featweights(aid_list, qreq_=qreq_)
    """
    fid_list = ibs.get_annot_fids(aid_list, qreq_=qreq_, ensure=True)
    featweight_rowid_list = add_feat_featweights(ibs, fid_list, qreq_=qreq_)
    return featweight_rowid_list


@register_ibs_method
#@adder
def add_annot_residuals(ibs, aid_list, qreq_=None):
    """ residual_rowid_list <- annot.residual.ensure(aid_list)

    Adds / ensures / computes a dependant property
    returns config_rowid of the current configuration

    CONVENIENCE FUNCTION

    Args:
        aid_list

    TemplateInfo:
        Tadder_rl_dependant
        root = annot
        leaf = residual

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis
        >>> ibs = ibeis.opendb('testdb1')
        >>> aid_list = ibs.get_valid_aids()
        >>> qreq_ = None
        >>> residual_rowid_list = ibs.add_annot_residuals(aid_list, qreq_=qreq_)
    """
    fid_list = ibs.get_annot_fids(aid_list, qreq_=qreq_, ensure=True)
    residual_rowid_list = add_feat_residuals(ibs, fid_list, qreq_=qreq_)
    return residual_rowid_list


# =========================
# 1_RL.TDELETER METHODS
# =========================


@register_ibs_method
#@deleter
#@cache_invalidator(constants.ANNOTATION_TABLE)
def delete_annot_featweight(ibs, aid_list, qreq_=None):
    """ annot.featweight.delete(aid_list)

    Args:
        aid_list

    TemplateInfo:
        Tdeleter_rl_depenant
        root = annot
        leaf = featweight
    """
    if utool.VERBOSE:
        print('[ibs] deleting %d annots leaf nodes' % len(aid_list))
    # Delete any dependants
    _featweight_rowid_list = ibs.get_annot_featweight_rowids(
        aid_list, qreq_=qreq_, ensure=False)
    featweight_rowid_list = ut.filter_Nones(_featweight_rowid_list)
    ibs.delete_featweight(featweight_rowid_list)


@register_ibs_method
#@deleter
#@cache_invalidator(constants.ANNOTATION_TABLE)
def delete_annot_residual(ibs, aid_list, qreq_=None):
    """ annot.residual.delete(aid_list)

    Args:
        aid_list

    TemplateInfo:
        Tdeleter_rl_depenant
        root = annot
        leaf = residual
    """
    if utool.VERBOSE:
        print('[ibs] deleting %d annots leaf nodes' % len(aid_list))
    # Delete any dependants
    _residual_rowid_list = ibs.get_annot_residual_rowids(
        aid_list, qreq_=qreq_, ensure=False)
    residual_rowid_list = ut.filter_Nones(_residual_rowid_list)
    ibs.delete_residual(residual_rowid_list)


# =========================
# 1_RL.TGETTER METHODS
# =========================


@register_ibs_method
#@getter
def get_annot_featweight_all_rowids(ibs, aid_list):
    """ featweight_rowid_list <- annot.featweight.all_rowids([aid_list])

    Gets featweight rowids of annot under the current state configuration.

    Args:
        aid_list (list):

    Returns:
        list: featweight_rowid_list

    TemplateInfo:
        Tgetter_rl_dependant_all_rowids
        root = annot
        leaf = featweight
    """
    # FIXME: broken
    colnames = (FEAT_ROWID,)
    featweight_rowid_list = ibs.dbcache.get(
        constants.FEATURE_WEIGHT_TABLE, colnames, aid_list,
        id_colname=ANNOT_ROWID)
    return featweight_rowid_list


@register_ibs_method
#@getter
def get_annot_featweight_rowids(ibs, aid_list, qreq_=None, ensure=False):
    """ featweight_rowid_list = annot.featweight.rowids[aid_list]

    Get featweight rowids of annot under the current state configuration.

    Args:
        aid_list (list):

    Returns:
        list: featweight_rowid_list

    TemplateInfo:
        Tgetter_rl_dependant_rowids
        root        = annot
        leaf_parent = feat
        leaf        = featweight

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis
        >>> ibs = ibeis.opendb('testdb1')
        >>> aid_list = ibs.get_valid_aids()
        >>> qreq_ = None
        >>> ensure = False
        >>> featweight_rowid_list1 = ibs.get_annot_featweight_rowids(aid_list, qreq_, ensure)
        >>> print(featweight_rowid_list1)
        >>> ensure = True
        >>> featweight_rowid_list2 = ibs.get_annot_featweight_rowids(aid_list, qreq_, ensure)
        >>> print(featweight_rowid_list2)
        >>> ensure = False
        >>> featweight_rowid_list3 = ibs.get_annot_featweight_rowids(aid_list, qreq_, ensure)
        >>> print(featweight_rowid_list3)
    """
    if ensure:
        # Ensuring dependant columns is equivalent to adding cleanly
        return ibs.add_annot_featweights(aid_list, qreq_=qreq_)
    else:
        # Get leaf_parent rowids
        fid_list = ibs.get_annot_fids(aid_list, qreq_=qreq_, ensure=False)
        colnames = (FEATWEIGHT_ROWID,)
        config_rowid = ibs.get_featweight_config_rowid(qreq_=qreq_)
        andwhere_colnames = (FEAT_ROWID, CONFIG_ROWID,)
        params_iter = [(fid, config_rowid,) for fid in fid_list]
        featweight_rowid_list = ibs.dbcache.get_where2(
            constants.FEATURE_WEIGHT_TABLE, colnames, params_iter, andwhere_colnames)
        return featweight_rowid_list


@register_ibs_method
#@getter
def get_annot_residual_all_rowids(ibs, aid_list):
    """ residual_rowid_list <- annot.residual.all_rowids([aid_list])

    Gets residual rowids of annot under the current state configuration.

    Args:
        aid_list (list):

    Returns:
        list: residual_rowid_list

    TemplateInfo:
        Tgetter_rl_dependant_all_rowids
        root = annot
        leaf = residual
    """
    # FIXME: broken
    colnames = (FEAT_ROWID,)
    residual_rowid_list = ibs.dbcache.get(
        constants.RESIDUAL_TABLE, colnames, aid_list,
        id_colname=ANNOT_ROWID)
    return residual_rowid_list


@register_ibs_method
#@getter
def get_annot_residual_rowids(ibs, aid_list, qreq_=None, ensure=False):
    """ residual_rowid_list = annot.residual.rowids[aid_list]

    Get residual rowids of annot under the current state configuration.

    Args:
        aid_list (list):

    Returns:
        list: residual_rowid_list

    TemplateInfo:
        Tgetter_rl_dependant_rowids
        root        = annot
        leaf_parent = feat
        leaf        = residual

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis
        >>> ibs = ibeis.opendb('testdb1')
        >>> aid_list = ibs.get_valid_aids()
        >>> qreq_ = None
        >>> ensure = False
        >>> residual_rowid_list1 = ibs.get_annot_residual_rowids(aid_list, qreq_, ensure)
        >>> print(residual_rowid_list1)
        >>> ensure = True
        >>> residual_rowid_list2 = ibs.get_annot_residual_rowids(aid_list, qreq_, ensure)
        >>> print(residual_rowid_list2)
        >>> ensure = False
        >>> residual_rowid_list3 = ibs.get_annot_residual_rowids(aid_list, qreq_, ensure)
        >>> print(residual_rowid_list3)
    """
    if ensure:
        # Ensuring dependant columns is equivalent to adding cleanly
        return ibs.add_annot_residuals(aid_list, qreq_=qreq_)
    else:
        # Get leaf_parent rowids
        fid_list = ibs.get_annot_fids(aid_list, qreq_=qreq_, ensure=False)
        colnames = (RESIDUAL_ROWID,)
        config_rowid = ibs.get_residual_config_rowid(qreq_=qreq_)
        andwhere_colnames = (FEAT_ROWID, CONFIG_ROWID,)
        params_iter = [(fid, config_rowid,) for fid in fid_list]
        residual_rowid_list = ibs.dbcache.get_where2(
            constants.RESIDUAL_TABLE, colnames, params_iter, andwhere_colnames)
        return residual_rowid_list


# =========================
# 2_NATIVE.TCFG METHODS
# =========================


@register_ibs_method
#@ider
def get_featweight_config_rowid(ibs, qreq_=None):
    """ featweight_cfg_rowid = featweight.config_rowid()

    returns config_rowid of the current configuration
    Config rowids are always ensured

    Returns:
        featweight_cfg_rowid

    TemplateInfo:
        Tcfg_rowid_getter
        leaf = featweight

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis; ibs = ibeis.opendb('testdb1')
        >>> featweight_cfg_rowid = ibs.get_featweight_config_rowid()
    """
    if qreq_ is not None:
        featweight_cfg_suffix = qreq_.qparams.featweight_cfgstr
        # TODO store config_rowid in qparams
    else:
        featweight_cfg_suffix = ibs.cfg.featweight_cfg.get_cfgstr()
    featweight_cfg_rowid = ibs.add_config(featweight_cfg_suffix)
    return featweight_cfg_rowid


@register_ibs_method
#@ider
def get_residual_config_rowid(ibs, qreq_=None):
    """ residual_cfg_rowid = residual.config_rowid()

    returns config_rowid of the current configuration
    Config rowids are always ensured

    Returns:
        residual_cfg_rowid

    TemplateInfo:
        Tcfg_rowid_getter
        leaf = residual

    Example:
        >>> # ENABLE_DOCTEST
        >>> import ibeis; ibs = ibeis.opendb('testdb1')
        >>> residual_cfg_rowid = ibs.get_residual_config_rowid()
    """
    if qreq_ is not None:
        residual_cfg_suffix = qreq_.qparams.residual_cfgstr
        # TODO store config_rowid in qparams
    else:
        residual_cfg_suffix = ibs.cfg.residual_cfg.get_cfgstr()
    residual_cfg_rowid = ibs.add_config(residual_cfg_suffix)
    return residual_cfg_rowid


# =========================
# 2_NATIVE.TDELETER METHODS
# =========================


@register_ibs_method
#@deleter
#@cache_invalidator(constants.FEATURE_WEIGHT_TABLE)
def delete_featweight(ibs, featweight_rowid_list):
    """ featweight.delete(featweight_rowid_list)

    delete featweight rows

    Args:
        featweight_rowid_list

    TemplateInfo:
        Tdeleter_native_tbl
        tbl = featweight

    Tdeleter_native_tbl
    """
    from ibeis.model.preproc import preproc_featweight
    if utool.VERBOSE:
        print('[ibs] deleting %d featweight rows' % len(featweight_rowid_list))
    # Prepare: Delete externally stored data (if any)
    preproc_featweight.on_delete(ibs, featweight_rowid_list)
    # Finalize: Delete self
    ibs.dbcache.delete_rowids(
        constants.FEATURE_WEIGHT_TABLE, featweight_rowid_list)


@register_ibs_method
#@deleter
#@cache_invalidator(constants.RESIDUAL_TABLE)
def delete_residual(ibs, residual_rowid_list):
    """ residual.delete(residual_rowid_list)

    delete residual rows

    Args:
        residual_rowid_list

    TemplateInfo:
        Tdeleter_native_tbl
        tbl = residual

    Tdeleter_native_tbl
    """
    from ibeis.model.preproc import preproc_residual
    if utool.VERBOSE:
        print('[ibs] deleting %d residual rows' % len(residual_rowid_list))
    # Prepare: Delete externally stored data (if any)
    preproc_residual.on_delete(ibs, residual_rowid_list)
    # Finalize: Delete self
    ibs.dbcache.delete_rowids(constants.RESIDUAL_TABLE, residual_rowid_list)


# =========================
# 2_NATIVE.TGET_FROM_SUPERKEY METHODS
# =========================


@register_ibs_method
#@getter
def get_featweight_rowid_from_superkey(ibs, feature_rowid_list, config_rowid_list):
    """ featweight_rowid_list <- featweight[feature_rowid_list, config_rowid_list]

    Args:
        superkey lists: feature_rowid_list, config_rowid_list

    Returns:
        featweight_rowid_list

    TemplateInfo:
        Tgetter_native_rowid_from_superkey
        tbl = featweight
    """
    colnames = (FEATWEIGHT_ROWID),
    # FIXME: col_rowid is not correct
    params_iter = zip(feature_rowid_list, config_rowid_list)
    andwhere_colnames = [feature_rowid_list, config_rowid_list]
    featweight_rowid_list = ibs.dbcache.get_where2(
        constants.FEATURE_WEIGHT_TABLE, colnames, params_iter, andwhere_colnames)
    return featweight_rowid_list


@register_ibs_method
#@getter
def get_residual_rowid_from_superkey(ibs, feature_rowid_list, config_rowid_list):
    """ residual_rowid_list <- residual[feature_rowid_list, config_rowid_list]

    Args:
        superkey lists: feature_rowid_list, config_rowid_list

    Returns:
        residual_rowid_list

    TemplateInfo:
        Tgetter_native_rowid_from_superkey
        tbl = residual
    """
    colnames = (RESIDUAL_ROWID),
    # FIXME: col_rowid is not correct
    params_iter = zip(feature_rowid_list, config_rowid_list)
    andwhere_colnames = [feature_rowid_list, config_rowid_list]
    residual_rowid_list = ibs.dbcache.get_where2(
        constants.RESIDUAL_TABLE, colnames, params_iter, andwhere_colnames)
    return residual_rowid_list


# =========================
# 2_NATIVE.TGETTER_NATIVE METHODS
# =========================


@register_ibs_method
#@getter
def get_featweight_fgweight(ibs, featweight_rowid_list):
    """ fgweight_list <- featweight.fgweight[featweight_rowid_list]

    gets data from the "native" column "fgweight" in the "featweight" table

    Args:
        featweight_rowid_list (list):

    Returns:
        list: fgweight_list

    TemplateInfo:
        Tgetter_table_column
        col = fgweight
        tbl = featweight
    """
    id_iter = featweight_rowid_list
    colnames = (FEATWEIGHT_FORGROUND_WEIGHT,)
    fgweight_list = ibs.dbcache.get(
        constants.FEATURE_WEIGHT_TABLE, colnames, id_iter, id_colname='rowid')
    return fgweight_list


@register_ibs_method
#@getter
def get_residual_vector(ibs, residual_rowid_list):
    """ vector_list <- residual.vector[residual_rowid_list]

    gets data from the "native" column "vector" in the "residual" table

    Args:
        residual_rowid_list (list):

    Returns:
        list: vector_list

    TemplateInfo:
        Tgetter_table_column
        col = vector
        tbl = residual
    """
    id_iter = residual_rowid_list
    colnames = (RESIDUAL_VECTOR,)
    vector_list = ibs.dbcache.get(
        constants.RESIDUAL_TABLE, colnames, id_iter, id_colname='rowid')
    return vector_list


@register_ibs_method
#@getter
def get_residual_rvecs(ibs, residual_rowid_list):
    """ rvecs_list <- residual.rvecs[residual_rowid_list]

    gets data from the "native" column "rvecs" in the "residual" table

    Args:
        residual_rowid_list (list):

    Returns:
        list: rvecs_list

    TemplateInfo:
        Tgetter_table_column
        col = rvecs
        tbl = residual
    """
    id_iter = residual_rowid_list
    colnames = (RVECS,)
    rvecs_list = ibs.dbcache.get(
        constants.RESIDUAL_TABLE, colnames, id_iter, id_colname='rowid')
    return rvecs_list


# =========================
# 2_NATIVE.TIDER_ALL_ROWIDS METHODS
# =========================


@register_ibs_method
#@ider
def _get_all_featweight_rowids(ibs):
    """ all_featweight_rowids <- featweight.get_all_rowids()

    Returns:
        list_ (list): unfiltered featweight_rowids

    TemplateInfo:
        Tider_all_rowids
        tbl = featweight
    """
    all_featweight_rowids = ibs.dbcache.get_all_rowids(
        constants.FEATURE_WEIGHT_TABLE)
    return all_featweight_rowids


@register_ibs_method
#@ider
def _get_all_residual_rowids(ibs):
    """ all_residual_rowids <- residual.get_all_rowids()

    Returns:
        list_ (list): unfiltered residual_rowids

    TemplateInfo:
        Tider_all_rowids
        tbl = residual
    """
    all_residual_rowids = ibs.dbcache.get_all_rowids(constants.RESIDUAL_TABLE)
    return all_residual_rowids


# =========================
# 2_NATIVE.TSETTER_NATIVE METHODS
# =========================


@register_ibs_method
#@setter
def set_featweight_fgweight(ibs, featweight_rowid_list, fgweight_list):
    """ fgweight_list -> featweight.fgweight[featweight_rowid_list]

    Args:
        featweight_rowid_list
        fgweight_list

    TemplateInfo:
        Tsetter_native_column
        tbl = featweight
        col = fgweight
    """
    id_iter = featweight_rowid_list
    colnames = (FEATWEIGHT_FORGROUND_WEIGHT,)
    ibs.dbcache.set(
        constants.FEATURE_WEIGHT_TABLE, colnames, fgweight_list, id_iter)


@register_ibs_method
#@setter
def set_residual_vector(ibs, residual_rowid_list, vector_list):
    """ vector_list -> residual.vector[residual_rowid_list]

    Args:
        residual_rowid_list
        vector_list

    TemplateInfo:
        Tsetter_native_column
        tbl = residual
        col = vector
    """
    id_iter = residual_rowid_list
    colnames = (RESIDUAL_VECTOR,)
    ibs.dbcache.set(constants.RESIDUAL_TABLE, colnames, vector_list, id_iter)


@register_ibs_method
#@setter
def set_residual_rvecs(ibs, residual_rowid_list, rvecs_list):
    """ rvecs_list -> residual.rvecs[residual_rowid_list]

    Args:
        residual_rowid_list
        rvecs_list

    TemplateInfo:
        Tsetter_native_column
        tbl = residual
        col = rvecs
    """
    id_iter = residual_rowid_list
    colnames = (RVECS,)
    ibs.dbcache.set(constants.RESIDUAL_TABLE, colnames, rvecs_list, id_iter)


# =========================
# RL.TGETTER_DEPENDANT METHODS
# =========================


@register_ibs_method
#@getter
def get_annot_fgweights(ibs, aid_list, qreq_=None, ensure=False):
    """ featweight_rowid_list <- annot.featweight.rowids[aid_list]

    Get fgweight data of the annot table using the dependant featweight table

    Args:
        aid_list (list):

    Returns:
        list: fgweight_list

    TemplateInfo:
        Tgetter_rl_pclines_dependant_column
        root = annot
        col  = fgweight
        leaf = featweight
    """
    # Get leaf rowids
    cid_list = ibs.get_annot_cids(aid_list, qreq_=qreq_, ensure=ensure)
    fid_list = ibs.get_chip_fids(cid_list, qreq_=qreq_, ensure=ensure)
    featweight_rowid_list = ibs.get_feat_featweight_rowids(
        fid_list, qreq_=qreq_, ensure=ensure)
    # Get col values
    fgweight_list = ibs.get_featweight_fgweight(featweight_rowid_list)
    return fgweight_list


@register_ibs_method
#@getter
def get_annot_vec_list(ibs, aid_list, qreq_=None, ensure=False):
    """ residual_rowid_list <- annot.residual.rowids[aid_list]

    Get vector data of the annot table using the dependant residual table

    Args:
        aid_list (list):

    Returns:
        list: vector_list

    TemplateInfo:
        Tgetter_rl_pclines_dependant_column
        root = annot
        col  = vector
        leaf = residual
    """
    # Get leaf rowids
    cid_list = ibs.get_annot_cids(aid_list, qreq_=qreq_, ensure=ensure)
    fid_list = ibs.get_chip_fids(cid_list, qreq_=qreq_, ensure=ensure)
    residual_rowid_list = ibs.get_feat_residual_rowids(
        fid_list, qreq_=qreq_, ensure=ensure)
    # Get col values
    vector_list = ibs.get_residual_vector(residual_rowid_list)
    return vector_list


@register_ibs_method
#@getter
def get_annot_rvec_lists(ibs, aid_list, qreq_=None, ensure=False):
    """ residual_rowid_list <- annot.residual.rowids[aid_list]

    Get rvecs data of the annot table using the dependant residual table

    Args:
        aid_list (list):

    Returns:
        list: rvecs_list

    TemplateInfo:
        Tgetter_rl_pclines_dependant_column
        root = annot
        col  = rvecs
        leaf = residual
    """
    # Get leaf rowids
    cid_list = ibs.get_annot_cids(aid_list, qreq_=qreq_, ensure=ensure)
    fid_list = ibs.get_chip_fids(cid_list, qreq_=qreq_, ensure=ensure)
    residual_rowid_list = ibs.get_feat_residual_rowids(
        fid_list, qreq_=qreq_, ensure=ensure)
    # Get col values
    rvecs_list = ibs.get_residual_rvecs(residual_rowid_list)
    return rvecs_list

if __name__ == '__main__':
    """
    CommandLine:
        python ibeis\control\_autogen_ibeiscontrol_funcs.py
        python ibeis\control\_autogen_ibeiscontrol_funcs.py --allexamples
    """
    import multiprocessing
    multiprocessing.freeze_support()
    import utool as ut
    ut.doctest_funcs()
