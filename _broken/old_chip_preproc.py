# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from six.moves import zip, range, filter  # NOQA
from os.path import exists, relpath
import utool as ut
import vtool as vt
import functools

# TODO in template version
#def read_chip_fpath(ibs, cid_list, **kwargs):
#    """ T_ExternFileGetter """
#    cfpath_list = ibs.get_chip_fpath(cid_list, **kwargs)
#    # --- generalize params
#    rowid_list = cid_list
#    readfunc = vt.imread
#    fpath_list = cfpath_list
#    # --- generalize func
#    """
#    # a missing external resource should delete its rowid from its native table
#    # it is the parent responcibility to recompute the desired child
#    # configuration.
#    """
#    data_list = ut.alloc_nones(len(fpath_list))
#    failed_index_list = []
#    for index, fpath in enumerate(fpath_list):
#        try:
#            data = readfunc(fpath)
#            data_list[index] = data
#        except IOError:
#            failed_index_list.append(index)
#    failed_rowids    = ut.take(rowid_list, failed_index_list)
#    failed_fpaths    = ut.take(fpath_list, failed_index_list)
#    exists_list      = [exists(fpath) for fpath in failed_fpaths]
#    missing_rowids   = ut.compress(failed_rowids, exists_list)  # NOQA
#    corrupted_rowids = ut.filterfalse_items(failed_rowids, exists_list)  # NOQA
#    # FINISHME


#--------------------------
# OLD FUNCTIONALITY TO DEPRICATE
#--------------------------

def compute_or_read_annotation_chips(ibs, aid_list, ensure=True, config2_=None,
                                     verbose=False, eager=True):
    r"""
    SUPER HACY FUNCTION. NEED TO DEPRICATE

    ----------------------
    Found 1 line(s) in 'ibeis/algo/preproc/preproc_chip.py':
    preproc_chip.py :  25 |def compute_or_read_annotation_chips(ibs, aid_list,
    ensure=True):
    ----------------------
    Found 1 line(s) in 'ibeis/control/manual_chip_funcs.py':
    manual_chip_funcs.py : 313 |    chip_list =
    preproc_chip.compute_or_read_annotation_chips(ibs, aid_list, ensure=ensure)

    """
    if ensure:
        try:
            ut.assert_all_not_None(aid_list, 'aid_list')
        except AssertionError as ex:
            ut.printex(ex, key_list=['aid_list'])
            raise
    nTotal = len(aid_list)
    cfpath_list = make_annot_chip_fpath_list(ibs, aid_list, config2_=config2_)
    mk_cpath_iter = functools.partial(ut.ProgressIter, cfpath_list,
                                      nTotal=nTotal, enabled=verbose, freq=100)
    try:
        if ensure:
            cfpath_iter = mk_cpath_iter(lbl='reading ensured chips')
            chip_list = [vt.imread(cfpath) for cfpath in cfpath_iter]
            #for cfpath in cfpath_iter:
            #    yield vt.imread(cfpath)
        else:
            cfpath_iter = mk_cpath_iter(lbl='reading existing chips')
            chip_list = [None if cfpath is None else vt.imread(cfpath) for cfpath in cfpath_iter]
            #for cfpath in cfpath_iter:
            #    yield None if cfpath is None else vt.imread(cfpath)
    except IOError as ex:
        if not ut.QUIET:
            ut.printex(ex, '[preproc_chip] Handing Exception: ', iswarning=True)
        ibs.add_annot_chips(aid_list)
        try:
            cfpath_iter = mk_cpath_iter(lbl='reading fallback1 chips')
            chip_list = [vt.imread(cfpath) for cfpath in cfpath_iter]
        except IOError:
            print('[preproc_chip] cache must have been deleted from disk')
            # TODO: WE CAN SEARCH FOR NON EXISTANT PATHS HERE AND CALL
            # ibs.delete_annot_chips
            compute_and_write_chips_lazy(ibs, aid_list)
            # Try just one more time
            cfpath_iter = mk_cpath_iter(lbl='reading fallback2 chips')
            chip_list = [vt.imread(cfpath) for cfpath in cfpath_iter]

    return chip_list


def compute_and_write_chips_lazy(ibs, aid_list, config2_=None):
    r"""
    Spanws compute chip procesess if a chip does not exist on disk

    DEPRICATE

    This is regardless of if it exists in the SQL database

    Args:
        ibs (IBEISController):
        aid_list (list):
    """
    if ut.VERBOSE:
        print('[preproc_chip] compute_and_write_chips_lazy')
    # Mark which aid's need their chips computed
    cfpath_list = make_annot_chip_fpath_list(ibs, aid_list, config2_=config2_)
    missing_flags = [not exists(cfpath) for cfpath in cfpath_list]
    invalid_aids = ut.compress(aid_list, missing_flags)
    if ut.VERBOSE:
        print('[preproc_chip] %d / %d chips need to be computed' %
              (len(invalid_aids), len(aid_list)))
    chip_result_list = list(compute_and_write_chips(ibs, invalid_aids))
    chip_fpath_list = ut.get_list_column(chip_result_list, 0)
    return chip_fpath_list


#  ^^ OLD FUNCS ^^

def compute_or_read_chip_images(ibs, cid_list, ensure=True, config2_=None):
    """Reads chips and tries to compute them if they do not exist

    Args:
        ibs (IBEISController):
        cid_list (list):
        ensure (bool):

    Returns:
        chip_list

    CommandLine:
        python -m ibeis.algo.preproc.preproc_chip --test-compute_or_read_chip_images

    Example:
        >>> # SLOW_DOCTEST
        >>> from ibeis.algo.preproc.preproc_chip import *  # NOQA
        >>> from ibeis.algo.preproc import preproc_chip
        >>> import numpy as np
        >>> ibs, aid_list = testdata_ibeis()
        >>> cid_list = ibs.get_annot_chip_rowids(aid_list, ensure=True)
        >>> chip_list = compute_or_read_chip_images(ibs, cid_list)
        >>> result = np.array(list(map(np.shape, chip_list))).sum(0).tolist()
        >>> print(result)
        [1434, 2274, 12]

    Example:
        >>> # SLOW_DOCTEST
        >>> from ibeis.algo.preproc.preproc_chip import *  # NOQA
        >>> import numpy as np
        >>> ibs, aid_list = testdata_ibeis()
        >>> cid_list = ibs.get_annot_chip_rowids(aid_list, ensure=True)
        >>> # Do a bad thing. Remove from disk without removing from sql
        >>> on_delete(ibs, cid_list)
        >>> # Now compute_or_read_chip_images should catch the bad thing
        >>> # we did and correct for it.
        >>> chip_list = compute_or_read_chip_images(ibs, cid_list)
        >>> result = np.array(list(map(np.shape, chip_list))).sum(0).tolist()
        >>> print(result)
        [1434, 2274, 12]
    """
    cfpath_list = ibs.get_chip_fpath(cid_list)
    try:
        if ensure:
            try:
                ut.assert_all_not_None(cid_list, 'cid_list')
            except AssertionError as ex:
                ut.printex(ex, key_list=['cid_list'])
                raise
            else:
                chip_list = [vt.imread(cfpath) for cfpath in cfpath_list]
        else:
            chip_list = [None if cfpath is None else vt.imread(cfpath) for cfpath in cfpath_list]
    except IOError as ex:
        if not ut.QUIET:
            ut.printex(ex, '[preproc_chip] Handing Exception: ', iswarning=True)
        # Remove bad annotations from the sql database
        aid_list = ibs.get_chip_aids(cid_list)
        valid_list    = [cid is not None for cid in cid_list]
        valid_aids    = ut.compress(aid_list, valid_list)
        valid_cfpaths = ut.compress(cfpath_list, valid_list)
        invalid_aids  = ut.filterfalse_items(valid_aids, map(exists, valid_cfpaths))
        ibs.delete_annot_chips(invalid_aids)
        # Try readding things
        new_cid_list = ibs.add_annot_chips(aid_list)
        cfpath_list = ibs.get_chip_fpath(new_cid_list)
        chip_list = [vt.imread(cfpath) for cfpath in cfpath_list]
    return chip_list


def generate_chip_properties(ibs, aid_list, config2_=None):
    r"""
    Computes parameters for SQLController adding

    computes chips if they do not exist.
    generates values for add_annot_chips sqlcommands

    Args:
        ibs (IBEISController):
        aid_list (list):
        config2_ (QueryParams):

    CommandLine:
        python -m ibeis.algo.preproc.preproc_chip --test-generate_chip_properties

    Example:
        >>> # ENABLE DOCTEST
        >>> from ibeis.algo.preproc.preproc_chip import *  # NOQA
        >>> from os.path import basename
        >>> import ibeis
        >>> ibs = ibeis.opendb('testdb1')
        >>> aid_list = ibs.get_valid_aids()[0:1]
        >>> params_iter = generate_chip_properties(ibs, aid_list)
        >>> params_list = list(params_iter)
        >>> (chip_uri, width, height,) = params_list[0]
        >>> fname_ = ut.regex_replace('auuid=.*_CHIP', 'auuid={uuid}_CHIP', chip_uri)
        >>> result = (fname_, width, height)
        >>> print(result)
        ('chip_avuuid=8687dcb6-1f1f-fdd3-8b72-8f36f9f41905_CHIP(sz450).png', 545, 372)

        ('chip_aid=1_auuid={uuid}_CHIP(sz450).png', 545, 372)
    """
    try:
        # the old function didn't even call this
        print('[generate_chip_properties] Requested params for %d chips ' % (len(aid_list)))
        chip_dir = ibs.get_chipdir()
        chip_result_list = compute_and_write_chips(ibs, aid_list, config2_=config2_)
        for chip_result, aid in zip(chip_result_list, aid_list):
            cfpath, width, height = chip_result
            chip_uri = relpath(cfpath, chip_dir)
            # Can be made faster by getting size from generator
            #pil_chip = vt.open_pil_image(cfpath)
            #width, height = pil_chip.size
            if ut.DEBUG2:
                print('Yeild Chip Param: aid=%r, cpath=%r' % (aid, cfpath))
            yield (chip_uri, width, height,)
    except IOError as ex:
        ut.printex(ex, 'ERROR IN PREPROC CHIPS')


#---------------
# Chip computing
#---------------


def gen_chip(tup):
    r"""
    Parallel worker. Crops chip out of an image, applies filters, etc

    THERE MAY BE AN ERROR IN HERE DUE TO IMWITE BEING INSIDE A PARALLEL FUNCTION
    BUT IT MAY BE SOMETHING ELSE?

    Either way we probably shouldn't call imwrite inside here
    """
    #print('generating chip')
    cfpath, gfpath, bbox, theta, new_size, filter_list = tup
    chipBGR = vt.compute_chip(gfpath, bbox, theta, new_size, filter_list)
    #if DEBUG:
    #print('write chip: %r' % cfpath)
    height, width = chipBGR.shape[0:2]
    vt.imwrite(cfpath, chipBGR)
    return cfpath, width, height


def gen_chip2(tup):
    r"""
    Parallel worker. Crops chip out of an image, applies filters, etc
    """
    #print('generating chip')
    cfpath, gfpath, bbox, theta, new_size, filter_list = tup
    chipBGR = vt.compute_chip(gfpath, bbox, theta, new_size, filter_list)
    #if DEBUG:
    #print('write chip: %r' % cfpath)
    height, width = chipBGR.shape[0:2]
    #vt.imwrite(cfpath, chipBGR)
    return chipBGR, cfpath, width, height


def get_filter_list(chipcfg_dict):
    from vtool import image_filters as gfilt_tool
    filter_list = []
    if chipcfg_dict.get('adapteq'):
        filter_list.append(gfilt_tool.adapteq_fn)
    if chipcfg_dict.get('histeq'):
        filter_list.append(gfilt_tool.histeq_fn)
    #if chipcfg_dict.get('maxcontrast'):
        #filter_list.append(maxcontr_fn)
    #if chipcfg_dict.get('rank_eq'):
        #filter_list.append(rankeq_fn)
    #if chipcfg_dict.get('local_eq'):
        #filter_list.append(localeq_fn)
    if chipcfg_dict.get('grabcut'):
        filter_list.append(gfilt_tool.grabcut_fn)
    return filter_list


def compute_and_write_chips(ibs, aid_list, config2_=None):
    r"""
    Starts the compute chip process

    Args:
        ibs (IBEISController):  ibeis controller object
        aid_list (list):  list of annotation rowids
        config2_ (dict): (default = None)

    CommandLine:
        python -m ibeis.algo.preproc.preproc_chip --test-compute_and_write_chips

    FIXME: THERE IS A FREEZE THAT HAPPENS HERE
        ./reset_dbs.py
        python -m ibeis.expt.harness --exec-precompute_test_configuration_features -t custom --expt-preload

    Example:
        >>> # SLOW_DOCTEST
        >>> from ibeis.algo.preproc.preproc_chip import *  # NOQA
        >>> from os.path import basename
        >>> config2_ = None
        >>> ibs, aid_list = testdata_ibeis()
        >>> # delete chips
        >>> ibs.delete_annot_chips(aid_list)
        >>> # ensure they were deleted
        >>> cid_list = ibs.get_annot_chip_rowids(aid_list, ensure=False)
        >>> assert all([cid is None for cid in cid_list]), 'should be gone'
        >>> chip_result_list = list(compute_and_write_chips(ibs, aid_list))
        >>> cfpath_list = ut.get_list_column(chip_result_list, 0)
        >>> cfname_list = ut.lmap(basename, cfpath_list)
        >>> print(cfname_list)
        >>> # cids should still be None. IBEIS does not know we computed chips
        >>> cid_list = ibs.get_annot_chip_rowids(aid_list, ensure=False)
        >>> assert all([cid is None for cid in cid_list]), 'should be gone'
        >>> # Now this function should have been executed again implictly
        >>> cid_list = ibs.get_annot_chip_rowids(aid_list, ensure=True)
        >>> assert ibs.get_chip_fpath(cid_list) == cfpath_list, 'should be what we had before'

    Ignore:
        >>> from ibeis.algo.preproc.preproc_chip import *  # NOQA
        from os.path import basename
        import ibeis
        ibs = ibeis.opendb('GZ_Master1')
        aid_list = [1915]
        extract_chip_from_img(imgBGR, bbox, theta, new_size)
        gfpath_list = ibs.get_annot_image_paths(aid_list)
        bbox_list   = ibs.get_annot_bboxes(aid_list)
        theta_list  = ibs.get_annot_thetas(aid_list)
        bbox_size_list = ut.get_list_column(bbox_list, [2, 3])
        newsize_list = vt.get_scaled_sizes_with_area(target_area, bbox_size_list)
        gfpath = gfpath_list[0]
        img = vt.imread(gfpath)
        dim_size = 450
        dim_size = 500
        target_area = dim_size ** 2
        bbox = bbox_list[0]
        theta = theta_list[0]
        new_size = newsize_list[0]
        #new_size = bbox[2:4]
        chipBGR = vt.compute_chip(gfpath, bbox, theta, new_size, {})
        import plottool as pt
        print('chipBGR.shape = %r' % (chipBGR.shape,))
        print('chipBGR.shape = %r' % (np.sqrt(np.prod(chipBGR.shape[0:2])),))
        pt.imshow(chipBGR, fnum=1)
        pt.imshow(img, fnum=2)
        pt.iup()
        pt.present()

    """
    ut.ensuredir(ibs.get_chipdir())
    # CONFIG INFO
    # Get chip configuration information
    if config2_ is not None:
        chip_cfg_dict  = config2_.get('chip_cfg_dict')
        dim_size = config2_.get('dim_size')
        assert dim_size is not None
        assert chip_cfg_dict is not None
    else:
        # use ibs if config2_ is None
        dim_size = ibs.cfg.chip_cfg.dim_size
        chip_cfg_dict = ibs.cfg.chip_cfg.to_dict()
    # Get chip dest information (output path),
    # source information (image, annotation_bbox, theta)
    # Get how big to resize each chip, etc...
    nChips = len(aid_list)
    filter_list = get_filter_list(chip_cfg_dict)
    cfpath_list = make_annot_chip_fpath_list(ibs, aid_list, config2_=config2_)
    gfpath_list = ibs.get_annot_image_paths(aid_list)
    bbox_list   = ibs.get_annot_bboxes(aid_list)
    theta_list  = ibs.get_annot_thetas(aid_list)
    #target_area = dim_size ** 2
    bbox_size_list = ut.get_list_column(bbox_list, [2, 3])

    scale_func_dict = {
        'width': vt.get_scaled_size_with_width,
        'root_area': vt.get_scaled_size_with_area,
    }
    resize_dim = chip_cfg_dict['resize_dim']
    scale_func = scale_func_dict[resize_dim]
    if resize_dim == 'root_area':
        target_dim_size = dim_size ** 2
    else:
        target_dim_size = dim_size
    newsize_list = [scale_func(target_dim_size, w, h) for (w, h) in bbox_size_list]

    #newsize_list = vt.get_scaled_sizes_with_area(target_area, bbox_size_list)
    invalid_aids = [aid for aid, (w, h) in zip(aid_list, bbox_size_list) if w == 0 or h == 0]
    filtlist_iter = (filter_list for _ in range(nChips))
    # Check for invalid chips
    if len(invalid_aids) > 0:
        msg = ("REMOVE INVALID (BAD WIDTH AND/OR HEIGHT) AIDS TO COMPUTE AND WRITE CHIPS")
        msg += ("INVALID AIDS: %r" % (invalid_aids, ))
        print(msg)
        raise Exception(msg)
    # Define "Asynchronous" generator
    arg_iter = zip(cfpath_list, gfpath_list, bbox_list, theta_list,
                            newsize_list, filtlist_iter)
    arg_list = list(arg_iter)
    #ut.embed()
    # We have to force serial here until we can figure out why parallel chip
    # generation causes a freeze
    # utool has a unstable test that reproduces this reliably (BECAUSE OF
    # CV2.WARP_AFFINE WITH BIG OUTPUT)
    if ut.VERBOSE:
        print('Computing %d chips' % (len(cfpath_list)))

    DO_IMWRITE_IN_WORKER = False
    if DO_IMWRITE_IN_WORKER:
        # Compute and write chips in asychronous process
        chip_result_iter = ut.util_parallel.generate(gen_chip, arg_list,
                                                     ordered=True,
                                                     force_serial=True,
                                                     freq=10)
        #chip_result_list = list(chip_result_iter)
        for _ in chip_result_iter:
            yield _
    else:
        # Compute chips in asychronous process. Write here
        chip_result_iter = ut.util_parallel.generate(gen_chip2, arg_list,
                                                     ordered=True,
                                                     force_serial=True,
                                                     freq=10)
        #chip_result_list = []
        for chipBGR, cfpath, width, height in chip_result_iter:
            vt.imwrite(cfpath, chipBGR)
            del chipBGR
            yield (cfpath, width, height)
    #print(ut.util_parallel.__POOL__)
    if not ut.VERBOSE:
        print('Done computing chips')
    #return chip_result_list


def on_delete(ibs, cid_list, config2_=None):
    r"""
    Cleans up chips on disk.  Called on delete from sql controller.

    CommandLine:
        python -m ibeis.algo.preproc.preproc_chip --test-on_delete

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.algo.preproc.preproc_chip import *  # NOQA
        >>> from ibeis.algo.preproc import preproc_chip
        >>> ibs, aid_list = preproc_chip.testdata_ibeis()
        >>> cid_list = ibs.get_annot_chip_rowids(aid_list, ensure=True)
        >>> ut.assert_eq(len(ut.filter_Nones(cid_list)), len(cid_list), var1_name='nchips')
        >>> # Run test function
        >>> nRemoved1 = preproc_chip.on_delete(ibs, cid_list)
        >>> ut.assert_eq(nRemoved1, len(cid_list), var1_name='nRemoved1', var2_name='target')
        >>> nRemoved2 = preproc_chip.on_delete(ibs, cid_list)
        >>> ut.assert_eq(nRemoved2, 0, var1_name='nRemoved2', var2_name='target')
        >>> # We have done a bad thing at this point. SQL still thinks chips exist
        >>> cid_list2 = ibs.get_annot_chip_rowids(aid_list, ensure=False)
        >>> ibs.delete_chips(cid_list2)
    """
    chip_fpath_list = ibs.get_chip_fpath(cid_list)
    nRemoved = ut.remove_existing_fpaths(chip_fpath_list, lbl='chips')
    return nRemoved

#---------------
# Chip filenames
#---------------


def make_annot_chip_fpath_list(ibs, aid_list, config2_=None):
    chipdir = ibs.get_chipdir()
    chip_uri_list = make_annot_chip_uri_list(ibs, aid_list, config2_=config2_)
    cfpath_list = [ut.unixjoin(chipdir, chip_uri) for chip_uri in chip_uri_list]
    return cfpath_list


def make_annot_chip_uri_list(ibs, aid_list, config2_=None):
    r"""
    Build chip file paths based on the current IBEIS configuration

    A chip depends on the chip config and the parent annotation's bounding box.
    (and technically the parent image (should we put that in the file path?)

    Args:
        ibs (IBEISController):
        aid_list (list):
        suffix (None):

    Returns:
        cfpath_list

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.algo.preproc.preproc_chip import *  # NOQA
        >>> from os.path import basename
        >>> ibs, aid_list = testdata_ibeis()
        >>> aid_list = aid_list[0:1]
        >>> chip_uri_list = make_annot_chip_uri_list(ibs, aid_list)
        >>> #fname = '\n'.join(map(basename, cfpath_list))
        >>> fname = '\n'.join(chip_uri_list)
        >>> result = fname
        >>> print(result)
        chip_avuuid=8687dcb6-1f1f-fdd3-8b72-8f36f9f41905_CHIP(sz450).png

    chip_aid=1_bbox=(0,0,1047,715)_theta=0.0tau_gid=1_CHIP(sz450).png
    """
    cfname_fmt = get_chip_fname_fmt(ibs, config2_=config2_)
    annot_visual_uuid_list  = ibs.get_annot_visual_uuids(aid_list)
    cfname_list = [cfname_fmt.format(avuuid=avuuid) for avuuid in annot_visual_uuid_list]
    return cfname_list


def get_chip_fname_fmt(ibs, config2_=None):
    r"""Returns format of chip file names

    Args:
        ibs (IBEISController):

    Returns:
        cfname_fmt

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.algo.preproc.preproc_chip import *  # NOQA
        >>> from ibeis.algo.preproc import preproc_chip
        >>> ibs, aid_list = preproc_chip.testdata_ibeis()
        >>> cfname_fmt = get_chip_fname_fmt(ibs)
        >>> result = cfname_fmt
        >>> print(result)
        chip_avuuid={avuuid}_CHIP(sz450).png

    chip_aid=%d_bbox=%s_theta=%s_gid=%d_CHIP(sz450).png
    """
    if config2_ is not None:
        chip_cfgstr = config2_.get('chip_cfgstr')
        assert chip_cfgstr is not None
    else:
        chip_cfgstr = ibs.cfg.chip_cfg.get_cfgstr()   # algo settings cfgstr
    chip_ext = ibs.cfg.chip_cfg['chipfmt']  # png / jpeg (BUGS WILL BE INTRODUCED IF THIS CHANGES)
    suffix = chip_cfgstr + chip_ext
    # Chip filenames are a function of annotation_rowid and cfgstr
    # TODO: Use annot uuids, use verts info as well
    #cfname_fmt = ('aid_%d' + suffix)
    #cfname_fmt = ''.join(['chip_auuid_%s' , suffix])
    #cfname_fmt = ''.join(['chip_aid=%d_auuid=%s' , suffix])
    # TODO: can use visual_uuids instead
    #cfname_fmt = ''.join(['chip_aid=%d_bbox=%s_theta=%s_gid=%d' , suffix])
    cfname_fmt = ''.join(['chip_avuuid={avuuid}' , suffix])
    return cfname_fmt


#-------------
# Testing
#-------------

def testdata_ibeis():
    r"""testdata function """
    import ibeis
    ibs = ibeis.opendb('testdb1')
    aid_list = ibs.get_valid_aids()[0::4]
    return ibs, aid_list
