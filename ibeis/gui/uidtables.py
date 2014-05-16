from __future__ import absolute_import, division, print_function
from itertools import izip
import utool
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView
(print, print_, printDBG, rrr, profile) = utool.inject(__name__, '[uidtables]', DEBUG=False)

from ibeis.control import DB_SCHEMA

USER_MODE = utool.get_flag('--usermode')

# Define which columns are usable in tables:
# Specified in (type, header, fancy_header) format
COLUMN_DEFS = [
    (int,   'gid',        'Image ID'),
    (int,   'rid',        'ROI ID'),
    (int,   'nid',        'Name ID'),
    (int,   'eid',        'Encounter ID'),
    (int,   'nRids',      '#ROIs'),
    (int,   'nGt',        '#GT'),
    (int,   'nFeats',     '#Features'),
    (int,   'rank',       'Rank'),
    (float, 'unixtime',   'unixtime'),
    (str,   'enctext',    'Encounter'),
    (str,   'gname',      'Image Name'),
    (str,   'name',       'Name'),
    (str,   'notes',      'Notes'),
    (str,   'match_name', 'Matching Name'),
    (str,   'bbox',       'BBOX (x, y, w, h)'),  # Non editables are safe as strs
    (str,   'score',      'Confidence'),
    (str,   'theta',      'Theta'),
    (bool,  'aif',        'All Detected'),
]


def _datatup_cols(ibs, tblname, cx2_score=None):
    '''
    Returns maps which map which maps internal column names
    to lazy evaluation functions which compute the data (hence the lambdas)
    '''
    printDBG('[gui] _datatup_cols()')
    # Return requested columns
    # TODO: Use partials here?
    if tblname == NAME_TABLE:
        cols = {
            'nid':    lambda nids: nids,
            'name':   lambda nids: ibs.get_names(nids),
            'nRids':  lambda nids: ibs.get_name_num_rois(nids),
            'notes':  lambda nids: ibs.get_name_notes(nids),
        }
    elif tblname == IMAGE_TABLE:
        cols = {
            'gid':      lambda gids: gids,
            'eid':      lambda gids: ibs.get_image_eids(gids),
            'enctext':  lambda gids: map(utool.tupstr, ibs.get_image_enctext(gids)),
            'aif':      lambda gids: ibs.get_image_aifs(gids),
            'gname':    lambda gids: ibs.get_image_gnames(gids),
            'nRids':    lambda gids: ibs.get_image_num_rois(gids),
            'unixtime': lambda gids: ibs.get_image_unixtime(gids),
            'notes':    lambda nids: ibs.get_image_notes(nids),
        }
    elif tblname in [ROI_TABLE, QRES_TABLE]:
        # ROI_TBL_COLS \subset RES_TBL_COLS
        cols = {
            'rid':    lambda rids: rids,
            'name':   lambda rids: ibs.get_roi_names(rids),
            'gname':  lambda rids: ibs.get_roi_gnames(rids),
            'nGt':    lambda rids: ibs.get_roi_num_groundtruth(rids),
            'theta':  lambda rids: map(utool.theta_str, ibs.get_roi_thetas(rids)),
            'bbox':   lambda rids: map(str, ibs.get_roi_bboxes(rids)),
            'nFeats': lambda rids: ibs.get_roi_num_feats(rids),
            'notes':  lambda rids: ibs.get_roi_notes(rids),
        }
        if tblname == QRES_TABLE:
            # But result table has extra cols
            cols.update({
                'rank':   lambda cxs:  range(1, len(cxs) + 1),
            })
    else:
        cols = {}
    return cols

col_type_list        = [tup[0] for tup in COLUMN_DEFS]
col_header_list      = [tup[1] for tup in COLUMN_DEFS]
col_fancyheader_list = [tup[2] for tup in COLUMN_DEFS]

# Mappings from (internal) header to (user-seen) fancy header
fancy_headers = dict(izip(col_header_list, col_fancyheader_list))
# Mapping from fancy header to header
reverse_fancy = dict(izip(col_fancyheader_list, col_header_list))
# Mapping from header to type
header_typemap = dict(izip(col_header_list, col_type_list))

# Different python types uuids can be


# We are basically just using int as the UID type now
# We aren't even messing with UUIDs here anymore
# TODO: Clean this section of code up!
UID_TYPE = int

schema_qt_typemap = {
    'INTEGER': int,
    'UUID': str,
}

# Specialize table uid types
QT_IMAGE_UID_TYPE = schema_qt_typemap[DB_SCHEMA.IMAGE_UID_TYPE]
QT_ROI_UID_TYPE   = schema_qt_typemap[DB_SCHEMA.ROI_UID_TYPE]
QT_NAME_UID_TYPE  = schema_qt_typemap[DB_SCHEMA.NAME_UID_TYPE]


def qt_cast(qtinput):
    """ Cast from Qt types to Python types """
    #printDBG('Casting qtinput=%r' % (qtinput,))
    if isinstance(qtinput, QtCore.QVariant):
        if qtinput.typeName() == 'bool':
            qtoutput = bool(qtinput.toBool())
        if qtinput.typeName() == 'QString':
            qtoutput = str(qtinput.toString())
    elif isinstance(qtinput, QtCore.QString):
        qtoutput = str(qtinput)
    #elif isinstance(qtinput, (int, long, str, float)):
    elif isinstance(qtinput, (int, str)):
        return qtinput
    else:
        raise ValueError('Unknown QtType: type(qtinput)=%r, qtinput=%r' % (type(qtinput), qtinput))
    return qtoutput

# Table names (should reflect SQL tables)
IMAGE_TABLE = 'gids'
ROI_TABLE   = 'rids'
NAME_TABLE  = 'nids'
QRES_TABLE  = 'qres'


# TABLE DEFINITIONS
# tblname, fancyname, headers, editable_headers
TABLE_DEF = [
    (IMAGE_TABLE, 'Image Table',
     ['gid', 'gname', 'nRids', 'aif', 'notes', 'enctext', 'unixtime'],
     ['notes', 'aif']),

    (ROI_TABLE, 'ROIs Table',
     ['rid', 'name', 'gname', 'nGt', 'nFeats', 'bbox', 'theta', 'notes'],
     ['name', 'notes']),

    (NAME_TABLE, 'Name Table',
     ['nid', 'name', 'nRids', 'notes'],
     ['name', 'notes']),

    (QRES_TABLE, 'Query Results Table',
     ['rank', 'score', 'name', 'rid'],
     ['name']),
]

tblname_list      = [tup[0] for tup in TABLE_DEF]
fancytblname_list = [tup[1] for tup in TABLE_DEF]
tblheaders_list    = [tup[2] for tup in TABLE_DEF]
tbleditables_list  = [tup[3] for tup in TABLE_DEF]

# A list of default internal headers to display
table_headers    = dict(izip(tblname_list, tblheaders_list))
table_editable   = dict(izip(tblname_list, tbleditables_list))
fancy_tablenames = dict(izip(tblname_list, fancytblname_list))

if USER_MODE:
    table_headers[ROI_TABLE] = ['rid', 'name', 'gname', 'nGt', 'notes']


def _get_datatup_list(ibs, tblname, index_list, header_order, extra_cols):
    '''
    Used by guiback to get lists of datatuples by internal column names.
    '''
    #printDBG('[gui] _get_datatup_list()')
    cols = _datatup_cols(ibs, tblname)
    #printDBG('[gui] cols=%r' % cols)
    cols.update(extra_cols)
    #printDBG('[gui] cols=%r' % cols)
    unknown_header = lambda indexes: ['ERROR!' for gx in indexes]
    get_tup = lambda header: cols.get(header, unknown_header)(index_list)
    unziped_tups = [get_tup(header) for header in header_order]
    #printDBG('[gui] unziped_tups=%r' % unziped_tups)
    datatup_list = [tup for tup in izip(*unziped_tups)]
    #printDBG('[gui] datatup_list=%r' % datatup_list)
    return datatup_list


def make_header_lists(tbl_headers, editable_list, prop_keys=[]):
    col_headers = tbl_headers[:] + prop_keys
    col_editable = [False] * len(tbl_headers) + [True] * len(prop_keys)
    for header in editable_list:
        col_editable[col_headers.index(header)] = True
    return col_headers, col_editable


def _get_table_headers_editable(tblname):
    headers = table_headers[tblname]
    editable = table_editable[tblname]
    printDBG('headers = %r ' % headers)
    printDBG('editable = %r ' % editable)
    col_headers, col_editable = make_header_lists(headers, editable)
    return col_headers, col_editable


def _get_table_datatup_list(ibs, tblname, col_headers, col_editable, extra_cols={},
                            index_list=None, prefix_cols=[], **kwargs):
    enctext = kwargs.get('enctext')
    if index_list is None:
        if enctext is None or enctext == '' or enctext == 'None':
            eid = None
        else:
            eid = ibs.get_encounter_eids(enctext)
        index_list = ibs.get_valid_ids(tblname, eid=eid)
    printDBG('[tables] len(index_list) = %r' % len(index_list))
    # Prefix datatup
    prefix_datatup = [[prefix_col.get(header, 'error')
                       for header in col_headers]
                      for prefix_col in prefix_cols]
    body_datatup = _get_datatup_list(ibs, tblname, index_list,
                                     col_headers, extra_cols)
    datatup_list = prefix_datatup + body_datatup
    return datatup_list


def emit_populate_table(back, tblname, *args, **kwargs):
    printDBG('>>>>>>>>>>>>>>>>>>>>>')
    printDBG('[uidtbls] _populate_table(%r)' % tblname)
    col_headers, col_editable = _get_table_headers_editable(tblname)
    #printDBG('[uidtbls] col_headers = %r' % col_headers)
    #printDBG('[uidtbls] col_editable = %r' % col_editable)
    enctext = kwargs.get('enctext', '')
    datatup_list = _get_table_datatup_list(back.ibs, tblname, col_headers,
                                           col_editable, *args, **kwargs)
    #printDBG('[uidtbls] datatup_list = %r' % datatup_list)
    row_list = range(len(datatup_list))
    # Populate with fancyheaders.
    col_fancyheaders = [fancy_headers.get(key, key) for key in col_headers]
    col_types = [header_typemap.get(key) for key in col_headers]
    printDBG('[uidtbls] populateTableSignal.emit(%r, len=%r)' % (tblname, len(col_fancyheaders)))
    back.populateTableSignal.emit(tblname,
                                  col_fancyheaders,
                                  col_editable,
                                  col_types,
                                  row_list,
                                  datatup_list,
                                  enctext)


def _type_from_data(data):
    """ If type is not given make an educated guess """
    if utool.is_bool(data) or data == 'True' or data == 'False':
        return bool
    elif utool.is_int(data):
        return int
    elif utool.is_float(data):
        return float
    else:
        return str


def populate_item_table(tbl,
                        col_fancyheaders,
                        col_editable,
                        col_types,
                        row_list,
                        datatup_list):
    # TODO: for chip table: delete metedata column
    # RCOS TODO:
    # I have a small right-click context menu working
    # Maybe one of you can put some useful functions in these?
    # RCOS TODO: How do we get the clicked item on a right click?
    # RCOS TODO:
    # The data tables should not use the item model
    # Instead they should use the more efficient and powerful
    # QAbstractItemModel / QAbstractTreeModel

    hheader = tbl.horizontalHeader()

    sort_col = hheader.sortIndicatorSection()
    sort_ord = hheader.sortIndicatorOrder()
    tbl.sortByColumn(0, Qt.AscendingOrder)  # Basic Sorting
    tblWasBlocked = tbl.blockSignals(True)
    tbl.clear()
    tbl.setColumnCount(len(col_fancyheaders))
    tbl.setRowCount(len(row_list))
    tbl.verticalHeader().hide()
    tbl.setHorizontalHeaderLabels(col_fancyheaders)
    tbl.setSelectionMode(QAbstractItemView.SingleSelection)
    tbl.setSelectionBehavior(QAbstractItemView.SelectRows)
    tbl.setSortingEnabled(False)
    # Add items for each row and column
    for row in iter(row_list):
        datatup = datatup_list[row]
        for col, data in enumerate(datatup):
            #type_ = _type_from_data(data)
            type_ = col_types[col]
            item = QtGui.QTableWidgetItem()
            try:
                if data is None:
                    # Default case to handle None inputs
                    item.setText(str(data))
                elif type_ == bool:
                    check_state = Qt.Checked if bool(data) else Qt.Unchecked
                    item.setCheckState(check_state)
                    item.setData(Qt.DisplayRole, bool(data))
                elif type_ == int:
                    item.setData(Qt.DisplayRole, int(data))
                elif type_ == float:
                    item.setData(Qt.DisplayRole, float(data))
                elif type_ == str:
                    item.setText(str(data))
                elif type_ == list:
                    item.setText(str(data))
                else:
                    raise Exception('Unknown datatype:' + repr(type_) +
                                    'has the type of this column been defined?')
                # Mark as editable or not
                if col_editable[col] and type_ != bool:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    item.setBackground(QtGui.QColor(250, 240, 240))
                else:
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignHCenter)
                tbl.setItem(row, col, item)
            except Exception as ex:
                utool.printex(ex, key_list=['type_', 'data', 'col', 'row',
                                            'tblname', 'col_types'])
                raise

    #printDBG(dbg_col2_dtype)
    tbl.setSortingEnabled(True)
    tbl.sortByColumn(sort_col, sort_ord)  # Move back to old sorting
    tbl.show()
    tbl.blockSignals(tblWasBlocked)


def populate_encounter_tab(front, enctext):
    #print('[uidtbls] populate_encounter_tab')
    front.ui.ensureEncounterTab(front, enctext)
