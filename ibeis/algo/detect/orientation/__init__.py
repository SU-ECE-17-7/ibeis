# -*- coding: utf-8 -*-
# Autogenerated on 15:41:06 2016/04/18
# flake8: noqa
from __future__ import absolute_import, division, print_function, unicode_literals
from ibeis.algo.detect.orientation import model
from ibeis.algo.detect.orientation import orientation
#from ibeis.algo.detect.orientation import tester
#from ibeis.algo.detect.orientation import utils
import utool
print, rrr, profile = utool.inject2(__name__, '[ibeis.algo.detect.__init__]')


def reassign_submodule_attributes(verbose=True):
    """
    why reloading all the modules doesnt do this I don't know
    """
    import sys
    if verbose and '--quiet' not in sys.argv:
        print('dev reimport')
    # Self import
    import ibeis.algo.detect.orientation
    # Implicit reassignment.
    seen_ = set([])
    for tup in IMPORT_TUPLES:
        if len(tup) > 2 and tup[2]:
            continue  # dont import package names
        submodname, fromimports = tup[0:2]
        submod = getattr(ibeis.algo.detect.orientation, submodname)
        for attr in dir(submod):
            if attr.startswith('_'):
                continue
            if attr in seen_:
                # This just holds off bad behavior
                # but it does mimic normal util_import behavior
                # which is good
                continue
            seen_.add(attr)
            setattr(ibeis.algo.detect.orientation, attr, getattr(submod, attr))


def reload_subs(verbose=True):
    """ Reloads ibeis.algo.detect.orientation and submodules """
    if verbose:
        print('Reloading submodules')
    rrr(verbose=verbose)
    def wrap_fbrrr(mod):
        def fbrrr(*args, **kwargs):
            """ fallback reload """
            if verbose:
                print('No fallback relaod for mod=%r' % (mod,))
            # Breaks ut.Pref (which should be depricated anyway)
            # import imp
            # imp.reload(mod)
        return fbrrr
    def get_rrr(mod):
        if hasattr(mod, 'rrr'):
            return mod.rrr
        else:
            return wrap_fbrrr(mod)
    def get_reload_subs(mod):
        return getattr(mod, 'reload_subs', wrap_fbrrr(mod))
    get_rrr(model)(verbose=verbose)
    get_rrr(orientation)(verbose=verbose)
    get_rrr(tester)(verbose=verbose)
    get_rrr(utils)(verbose=verbose)
    rrr(verbose=verbose)
    try:
        # hackish way of propogating up the new reloaded submodule attributes
        reassign_submodule_attributes(verbose=verbose)
    except Exception as ex:
        print(ex)
rrrr = reload_subs

IMPORT_TUPLES = [
    ('model', None),
    ('orientation', None),
    ('tester', None),
    ('utils', None),
]
"""
Regen Command:
    cd /Users/bluemellophone/code/ibeis/ibeis/algo/detect/orientation
    makeinit.py --modname=ibeis.algo.detect.orientation
"""
