from __future__ import absolute_import, division, print_function
import utool as ut
#import sys


#INJECTED_MODULES = []


def make_ibs_register_decorator(modname):
    """
    builds variables and functions that controller injectable modules need
    """
    #global INJECTED_MODULES
    if __name__ == '__main__':
        print('WARNING: cannot register controller functions as main')
    else:
        CLASS_INJECT_KEY = ('IBEISController', modname)
    # Create dectorator to inject these functions into the IBEISController
    #register_ibs_aliased_method   = ut.make_class_method_decorator(CLASS_INJECT_KEY)
    register_ibs_unaliased_method = ut.make_class_method_decorator(CLASS_INJECT_KEY)

    # TODO Replace IBEISContoller INEJECTED MODULES with this one
    #INJECTED_MODULES.append(sys.modules[modname])

    def register_ibs_method(func):
        """ registers autogenerated functions with the utool class method injector """
        register_ibs_unaliased_method(func)
        #aliastup = (func, '_injected_' + ut.get_funcname(func))
        #register_ibs_aliased_method(aliastup)
        return func
    return CLASS_INJECT_KEY, register_ibs_method


r"""
Vim add decorator
%s/^\n^@\([^r]\)/\r\r@register_ibs_method\r@\1/gc
%s/^\n\(def .*(ibs\)/\r\r@register_ibs_method\r\1/gc
%s/\n\n\n\n/\r\r\r/gc

# FIND UNREGISTERED METHODS
/^[^@]*\ndef
"""


def sort_module_functions():
    from os.path import dirname, join
    import utool as ut
    import ibeis.control
    #import re
    #regex = r'[^@]*\ndef'
    modfpath = dirname(ibeis.control.__file__)
    fpath = join(modfpath, 'manual_annot_funcs.py')
    text = ut.read_from(fpath, verbose=False)
    lines =  text.splitlines()
    indent_list = [ut.get_indentation(line) for line in lines]
    isfunc_list = [line.startswith('def ') for line in lines]
    isblank_list = [len(line.strip(' ')) == 0 for line in lines]
    isdec_list = [line.startswith('@') for line in lines]

    tmp = ['def' if isfunc else indent for isfunc, indent in  zip(isfunc_list, indent_list)]
    tmp = ['b' if isblank else t for isblank, t in  zip(isblank_list, tmp)]
    tmp = ['@' if isdec else t for isdec, t in  zip(isdec_list, tmp)]
    print('\n'.join([str((t, count + 1)) for (count, t) in enumerate(tmp)]))
    import re
    block_list = re.split('\n\n\n', text, re.MULTILINE)

    for block in block_list:
        print('#====')
        print(block)


def find_unregistered_methods():
    r"""
    CommandLine:
        python -m ibeis.control.controller_inject --test-find_unregistered_methods --enableall

    Example:
        >>> # ENABLE_DOCTEST
        >>> from ibeis.control.controller_inject import *  # NOQA
        >>> result = find_unregistered_methods()
        >>> print(result)
    """
    from os.path import dirname
    import utool as ut
    import ibeis.control
    import re
    #regex = r'[^@]*\ndef'
    modfpath = dirname(ibeis.control.__file__)
    fpath_list = ut.glob(modfpath, 'manual_*_funcs.py')
    #fpath_list += ut.glob(modfpath, '_autogen_*_funcs.py')

    def multiline_grepfile(regex, fpath):
        found_matchtexts = []
        found_linenos   = []
        text = ut.read_from(fpath, verbose=False)
        for match in  re.finditer(regex, text, flags=re.MULTILINE):
            lineno = text[:match.start()].count('\n')
            matchtext = ut.get_match_text(match)
            found_linenos.append(lineno)
            found_matchtexts.append(matchtext)
        return found_matchtexts, found_linenos

    def multiline_grep(regex, fpath_list):
        found_fpath_list      = []
        found_matchtexts_list = []
        found_linenos_list    = []
        for fpath in fpath_list:
            found_matchtexts, found_linenos = multiline_grepfile(regex, fpath)
            # append anything found in this file
            if len(found_matchtexts) > 0:
                found_fpath_list.append(fpath)
                found_matchtexts_list.append(found_matchtexts)
                found_linenos_list.append(found_linenos)
        return found_fpath_list, found_matchtexts_list, found_linenos_list

    def print_mutliline_matches(tup):
        found_fpath_list, found_matchtexts_list, found_linenos_list = tup
        for fpath, found_matchtexts, found_linenos in zip(found_fpath_list, found_matchtexts_list, found_linenos_list):
            print('+======')
            print(fpath)
            for matchtext, lineno in zip(found_matchtexts, found_linenos):
                print('    ' + '+----')
                print('    ' + str(lineno))
                print('    ' + str(matchtext))
                print('    ' + 'L____')

    #print(match)
    print('\n\n GREPING FOR UNDECORATED FUNCTIONS')
    regex = '^[^@\n]*\ndef\\s.*$'
    tup = multiline_grep(regex, fpath_list)
    print_mutliline_matches(tup)

    print('\n\n GREPING FOR UNDECORATED FUNCTION ALIASES')
    regex = '^' + ut.REGEX_VARNAME + ' = ' + ut.REGEX_VARNAME
    tup = multiline_grep(regex, fpath_list)
    print_mutliline_matches(tup)
    #ut.grep('aaa\rdef', modfpath, include_patterns=['manual_*_funcs.py', '_autogen_*_funcs.py'], reflags=re.MULTILINE)


if __name__ == '__main__':
    """
    CommandLine:
        python -m ibeis.control.controller_inject
        python -m ibeis.control.controller_inject --allexamples
        python -m ibeis.control.controller_inject --allexamples --noface --nosrc
    """
    import multiprocessing
    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA
    ut.doctest_funcs()