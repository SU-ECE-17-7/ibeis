# Dependencies: flask, tornado
from __future__ import absolute_import, division, print_function
# HTTP / HTML
import tornado.wsgi
import tornado.httpserver
import flask
from flask import request, redirect, url_for, make_response
import optparse
import logging
import socket
import simplejson as json
# IBEIS
import ibeis
from ibeis.control.SQLDatabaseControl import (SQLDatabaseController,  # NOQA
                                              SQLAtomicContext)
from ibeis.control import _sql_helpers
from ibeis.constants import KEY_DEFAULTS, SPECIES_KEY, Species
import utool
import utool as ut
# Web Internal
from ibeis.web import appfuncs as ap
from ibeis.web import DBWEB_SCHEMA
# Others
from os.path import join
import ibeis.constants as const
import random


BROWSER = ut.get_argflag('--browser')
DEFAULT_PORT = 5000
app = flask.Flask(__name__)


################################################################################


@app.route('/')
def root():
    return ap.template(None)


@app.route('/view')
def view():
    eid_list = app.ibs.get_valid_eids()
    gid_list = app.ibs.get_valid_gids()
    aid_list = app.ibs.get_valid_aids()
    return ap.template('view',
                       eid_list=eid_list,
                       eid_list_str=','.join(map(str, eid_list)),
                       num_eids=len(eid_list),
                       gid_list=gid_list,
                       gid_list_str=','.join(map(str, gid_list)),
                       num_gids=len(gid_list),
                       aid_list=aid_list,
                       aid_list_str=','.join(map(str, aid_list)),
                       num_aids=len(aid_list))


@app.route('/view/encounters')
def view_encounters():
    def encounter_image_processed(eid, gid_list):
        images_reviewed = [ reviewed == 1 for reviewed in app.ibs.get_image_reviewed(gid_list) ]
        return images_reviewed

    def encounter_annot_processed(eid, gid_list):
        aid_list = app.ibs.get_valid_aids(include_only_gid_list=gid_list)
        annots_reviewed = [ reviewed is not None for reviewed in app.ibs.get_annot_yaws(aid_list) ]
        return annots_reviewed

    filtered = True
    eid = request.args.get('eid', '')
    if len(eid) > 0:
        eid_list = eid.strip().split(',')
        eid_list = [ None if eid_ == 'None' or eid_ == '' else int(eid_) for eid_ in eid_list ]
    else:
        eid_list = app.ibs.get_valid_eids()
        filtered = False
    start_time_posix_list = app.ibs.get_encounter_start_time_posix(eid_list)
    datetime_list = [
        ut.unixtime_to_datetime(start_time_posix)
        if start_time_posix is not None else
        'Unknown'
        for start_time_posix in start_time_posix_list
    ]
    gids_list = [ app.ibs.get_valid_gids(eid=eid_) for eid_ in eid_list ]
    images_reviewed_list = [ encounter_image_processed(eid, gid_list) for eid_, gid_list in zip(eid_list, gids_list) ]
    annots_reviewed_list = [ encounter_annot_processed(eid, gid_list) for eid_, gid_list in zip(eid_list, gids_list) ]
    image_processed_list = [ images_reviewed.count(True) for images_reviewed in images_reviewed_list ]
    annot_processed_list = [ annots_reviewed.count(True) for annots_reviewed in annots_reviewed_list ]
    reviewed_list = [ all(images_reviewed) and all(annots_reviewed) for images_reviewed, annots_reviewed in zip(images_reviewed_list, annots_reviewed_list) ]
    encounter_list = zip(
        eid_list,
        app.ibs.get_encounter_enctext(eid_list),
        app.ibs.get_encounter_num_gids(eid_list),
        image_processed_list,
        app.ibs.get_encounter_num_aids(eid_list),
        annot_processed_list,
        start_time_posix_list,
        datetime_list,
        reviewed_list,
    )
    encounter_list.sort(key=lambda t: t[6])
    return ap.template('view', 'encounters',
                       filtered=filtered,
                       eid_list=eid_list,
                       eid_list_str=','.join(map(str, eid_list)),
                       num_eids=len(eid_list),
                       encounter_list=encounter_list,
                       num_encounters=len(encounter_list))


@app.route('/view/images')
def view_images():
    filtered = True
    eid_list = []
    gid = request.args.get('gid', '')
    eid = request.args.get('eid', '')
    if len(gid) > 0:
        gid_list = gid.strip().split(',')
        gid_list = [ None if gid_ == 'None' or gid_ == '' else int(gid_) for gid_ in gid_list ]
    elif len(eid) > 0:
        eid_list = eid.strip().split(',')
        eid_list = [ None if eid_ == 'None' or eid_ == '' else int(eid_) for eid_ in eid_list ]
        gid_list = ut.flatten([ app.ibs.get_valid_gids(eid=eid) for eid_ in eid_list ])
    else:
        gid_list = app.ibs.get_valid_gids()
        filtered = False
    image_unixtime_list = app.ibs.get_image_unixtime(gid_list)
    datetime_list = [
        ut.unixtime_to_datetime(image_unixtime)
        if image_unixtime is not None
        else
        'Unknown'
        for image_unixtime in image_unixtime_list
    ]
    image_list = zip(
        gid_list,
        [ eid_list_[0] for eid_list_ in app.ibs.get_image_eids(gid_list) ],
        app.ibs.get_image_gnames(gid_list),
        image_unixtime_list,
        datetime_list,
        app.ibs.get_image_gps(gid_list),
        app.ibs.get_image_party_tag(gid_list),
        app.ibs.get_image_contributor_tag(gid_list),
        app.ibs.get_image_notes(gid_list),
        [ reviewed == 1 for reviewed in app.ibs.get_image_reviewed(gid_list) ],
    )
    image_list.sort(key=lambda t: t[2])
    return ap.template('view', 'images',
                       filtered=filtered,
                       eid_list=eid_list,
                       eid_list_str=','.join(map(str, eid_list)),
                       num_eids=len(eid_list),
                       gid_list=gid_list,
                       gid_list_str=','.join(map(str, gid_list)),
                       num_gids=len(gid_list),
                       image_list=image_list,
                       num_images=len(image_list))


@app.route('/view/annotations')
def view_annotations():
    filtered = True
    eid_list = []
    gid_list = []
    aid = request.args.get('aid', '')
    gid = request.args.get('gid', '')
    eid = request.args.get('eid', '')
    if len(aid) > 0:
        aid_list = aid.strip().split(',')
        aid_list = [ None if aid_ == 'None' or aid_ == '' else int(aid_) for aid_ in aid_list ]
    elif len(gid) > 0:
        gid_list = gid.strip().split(',')
        gid_list = [ None if gid_ == 'None' or gid_ == '' else int(gid_) for gid_ in gid_list ]
        aid_list = app.ibs.get_valid_aids(include_only_gid_list=gid_list)
    elif len(eid) > 0:
        eid_list = eid.strip().split(',')
        eid_list = [ None if eid_ == 'None' or eid_ == '' else int(eid_) for eid_ in eid_list ]
        gid_list = ut.flatten([ app.ibs.get_valid_gids(eid=eid_) for eid_ in eid_list ])
        aid_list = app.ibs.get_valid_aids(include_only_gid_list=gid_list)
    else:
        aid_list = app.ibs.get_valid_aids()
        filtered = False
    annotation_list = zip(
        aid_list,
        app.ibs.get_annot_gids(aid_list),
        [ eid_list_[0] for eid_list_ in app.ibs.get_annot_eids(aid_list) ],
        app.ibs.get_annot_image_names(aid_list),
        app.ibs.get_annot_names(aid_list),
        app.ibs.get_annot_exemplar_flags(aid_list),
        app.ibs.get_annot_species_texts(aid_list),
        app.ibs.get_annot_yaw_texts(aid_list),
        app.ibs.get_annot_quality_texts(aid_list),
        [ reviewed is not None for reviewed in app.ibs.get_annot_yaws(aid_list) ],
    )
    annotation_list.sort(key=lambda t: t[0])
    return ap.template('view', 'annotations',
                       filtered=filtered,
                       eid_list=eid_list,
                       eid_list_str=','.join(map(str, eid_list)),
                       num_eids=len(eid_list),
                       gid_list=gid_list,
                       gid_list_str=','.join(map(str, gid_list)),
                       num_gids=len(gid_list),
                       aid_list=aid_list,
                       aid_list_str=','.join(map(str, aid_list)),
                       num_aids=len(aid_list),
                       annotation_list=annotation_list,
                       num_annotations=len(annotation_list))


@app.route('/turk')
def turk():
    eid = request.args.get('eid', None)
    eid = int(eid) if eid is not None else eid
    return ap.template('turk', None, eid=eid)


@app.route('/turk/detection')
def turk_detection():
    try:
        eid = request.args.get('eid', None)
        eid = int(eid) if eid is not None else eid
        gid = request.args.get('gid', None)
        if gid is not None:
            gid = int(gid)
        else:
            with SQLAtomicContext(app.db):
                gid_list = app.ibs.get_valid_gids(eid=eid)
                reviewed_list = app.ibs.get_image_reviewed(gid_list)
                flag_list = [ reviewed == 0 for reviewed in reviewed_list ]
                gid_list_ = ut.filter_items(gid_list, flag_list)
                if len(gid_list_) == 0:
                    gid = None
                else:
                    # gid = gid_list_[0]
                    gid = random.choice(gid_list_)
        previous = request.args.get('previous', None)
        finished = gid is None
        review = 'review' in request.args.keys()
        display_instructions = request.cookies.get('detection_instructions_seen', 0) == 0
        display_species_examples = False  # request.cookies.get('detection_example_species_seen', 0) == 0
        if not finished:
            gpath = app.ibs.get_image_paths(gid)
            image = ap.open_oriented_image(gpath)
            image_src = ap.embed_image_html(image, filter_width=False)
            # Get annotations
            width, height = app.ibs.get_image_sizes(gid)
            scale_factor = 700.0 / float(width)
            aid_list = app.ibs.get_image_aids(gid)
            annot_bbox_list = app.ibs.get_annot_bboxes(aid_list)
            annot_thetas_list = app.ibs.get_annot_thetas(aid_list)
            species_list = app.ibs.get_annot_species_texts(aid_list)
            # Get annotation bounding boxes
            annotation_list = []
            for annot_bbox, annot_theta, species in zip(annot_bbox_list, annot_thetas_list, species_list):
                temp = {}
                temp['left']   = int(scale_factor * annot_bbox[0])
                temp['top']    = int(scale_factor * annot_bbox[1])
                temp['width']  = int(scale_factor * (annot_bbox[2]))
                temp['height'] = int(scale_factor * (annot_bbox[3]))
                temp['label']  = species
                temp['angle']  = float(annot_theta)
                annotation_list.append(temp)
            if len(species_list) > 0:
                species = max(set(species_list), key=species_list.count)  # Get most common species
            elif app.default_species is not None:
                species = app.default_species
            else:
                species = KEY_DEFAULTS[SPECIES_KEY]
        else:
            gpath = None
            species = None
            image_src = None
            annotation_list = []
        return ap.template('turk', 'detection',
                           eid=eid,
                           gid=gid,
                           species=species,
                           image_path=gpath,
                           image_src=image_src,
                           previous=previous,
                           finished=finished,
                           annotation_list=annotation_list,
                           display_instructions=display_instructions,
                           display_species_examples=display_species_examples,
                           review=review)
    except:
        return redirect(url_for('error404'))


@app.route('/turk/viewpoint')
def turk_viewpoint():
    try:
        eid = request.args.get('eid', None)
        eid = int(eid) if eid is not None else eid
        aid = request.args.get('aid', None)
        if aid is not None:
            aid = int(aid)
        else:
            with SQLAtomicContext(app.db):
                gid_list = app.ibs.get_valid_gids(eid=eid)
                aid_list = app.ibs.get_valid_aids(include_only_gid_list=gid_list)
                reviewed_list = app.ibs.get_annot_yaws(aid_list)
                flag_list = [ reviewed is None for reviewed in reviewed_list ]
                aid_list_ = ut.filter_items(aid_list, flag_list)
                if len(aid_list_) == 0:
                    aid = None
                else:
                    # aid = aid_list_[0]
                    aid = random.choice(aid_list_)
        previous = request.args.get('previous', None)
        value = request.args.get('value', None)
        review = 'review' in request.args.keys()
        finished = aid is None
        display_instructions = request.cookies.get('viewpoint_instructions_seen', 0) == 0
        if not finished:
            gid       = app.ibs.get_annot_gids(aid)
            gpath     = app.ibs.get_annot_chip_fpaths(aid)
            image     = ap.open_oriented_image(gpath)
            image_src = ap.embed_image_html(image)
        else:
            gid       = None
            gpath     = None
            image_src = None
        return ap.template('turk', 'viewpoint',
                           eid=eid,
                           gid=gid,
                           aid=aid,
                           value=value,
                           image_path=gpath,
                           image_src=image_src,
                           previous=previous,
                           finished=finished,
                           display_instructions=display_instructions,
                           review=review)
    except:
        return redirect(url_for('error404'))


@app.route('/submit/detection', methods=['POST'])
def submit_detection():
    eid = request.args.get('eid', None)
    eid = int(eid) if eid is not None else eid
    gid = int(request.form['detection-gid'])
    turk_id = request.cookies.get('turk_id', -1)
    aid_list = app.ibs.get_image_aids(gid)
    # Make new annotations
    width, height = app.ibs.get_image_sizes(gid)
    scale_factor = float(width) / 700.0
    # Get aids
    app.ibs.delete_annots(aid_list)
    annotation_list = json.loads(request.form['detection-annotations'])
    bbox_list = [
        (
            int(scale_factor * annot['left']),
            int(scale_factor * annot['top']),
            int(scale_factor * annot['width']),
            int(scale_factor * annot['height']),
        )
        for annot in annotation_list
    ]
    theta_list = [
        float(annot['angle'])
        for annot in annotation_list
    ]
    species_list = [
        annot['label']
        for annot in annotation_list
    ]
    app.ibs.add_annots([gid] * len(annotation_list), bbox_list, theta_list=theta_list, species_list=species_list)
    app.ibs.set_image_reviewed([gid], [1])
    print('[web] turk_id: %s, gid: %d, bbox_list: %r, species_list: %r' % (turk_id, gid, annotation_list, species_list))
    refer = request.args.get('refer', '')
    if len(refer) > 0:
        return redirect(ap.decode_refer_url(refer))
    else:
        return redirect(url_for('turk_detection', eid=eid, previous=gid))


@app.route('/submit/viewpoint', methods=['POST'])
def submit_viewpoint():
    eid = request.args.get('eid', None)
    eid = int(eid) if eid is not None else eid
    aid = int(request.form['viewpoint-aid'])
    value = int(request.form['viewpoint-value'])
    turk_id = request.cookies.get('turk_id', -1)
    def convert_old_viewpoint_to_yaw(view_angle):
        ''' we initially had viewpoint coordinates inverted

        Example:
            >>> import math
            >>> TAU = 2 * math.pi
            >>> old_viewpoint_labels = [
            >>>     ('left'       , 0.000 * TAU,),
            >>>     ('frontleft'  , 0.125 * TAU,),
            >>>     ('front'      , 0.250 * TAU,),
            >>>     ('frontright' , 0.375 * TAU,),
            >>>     ('right'       , 0.500 * TAU,),
            >>>     ('backright'  , 0.625 * TAU,),
            >>>     ('back'       , 0.750 * TAU,),
            >>>     ('backleft'   , 0.875 * TAU,),
            >>> ]
            >>> fmtstr = 'old %15r %.2f -> new %15r %.2f'
            >>> for lbl, angle in old_viewpoint_labels:
            >>>     print(fmtstr % (lbl, angle, lbl, convert_old_viewpoint_to_yaw(angle)))
        '''
        if view_angle is None:
            return None
        yaw = (-view_angle + (const.TAU / 2)) % const.TAU
        return yaw
    yaw = convert_old_viewpoint_to_yaw(ut.deg_to_rad(value))
    app.ibs.set_annot_yaws([aid], [yaw], input_is_degrees=False)
    print('[web] turk_id: %s, aid: %d, yaw: %d' % (turk_id, aid, yaw))
    # Return HTML
    refer = request.args.get('refer', '')
    if len(refer) > 0:
        return redirect(ap.decode_refer_url(refer))
    else:
        return redirect(url_for('turk_viewpoint', eid=eid, previous=aid))


@app.route('/ajax/cookie')
def set_cookie():
    response = make_response('true')
    try:
        response.set_cookie(request.args['name'], request.args['value'])
        print('Set Cookie: %r -> %r' % (request.args['name'], request.args['value'], ))
        return response
    except:
        print('COOKIE FAILED: %r' % (request.args, ))
        return make_response('false')


@app.route('/ajax/image/src/<gid>')
def image_src(gid=None):
    # gpath = app.ibs.get_image_paths(gid)
    gpath = app.ibs.get_image_thumbpath(gid)
    return ap.return_src(gpath)


@app.route('/ajax/annotation/src/<aid>')
def annotation_src(aid=None):
    gpath = app.ibs.get_annot_chip_fpaths(aid)
    return ap.return_src(gpath)


@app.route('/api')
@app.route('/api/<function>.json', methods=['GET', 'POST'])
def api(function=None):
    template = {
        'status': {
            'success': False,
            'code': '',
        },
    }
    print('Function:', function)
    print('POST:', dict(request.form))
    print('GET:',  dict(request.args))
    if function is None:
        template['status']['success'] = True
        template['status']['code'] = 'USAGE: /api/[ibeis_function_name].json'
    else:
        function = function.lower()
        if ap.check_valid_function_name(function):
            function = 'app.ibs.%s' % function
            exists = True
            try:
                func = eval(function)
                ret = func()
            except AttributeError:
                exists = False
            if exists:
                template['status']['success'] = True
                template['function'] = function
                template['return'] = ret
            else:
                template['status']['success'] = False
                template['status']['code'] = 'ERROR: Specified IBEIS function not visible or implemented'
        else:
            template['status']['success'] = False
            template['status']['code'] = 'ERROR: Specified IBEIS function not valid Python function'
    return json.dumps(template)


@app.route('/404')
def error404():
    return ap.template(None, '404')


################################################################################


def init_database(app, reset_db):
    database_dir = utool.get_app_resource_dir('ibeis', 'web')
    database_filename = 'app.sqlite3'
    database_filepath = join(database_dir, database_filename)
    utool.ensuredir(database_dir)
    if reset_db:
        utool.remove_file(database_filepath)
    app.dbweb_version_expected = '1.0.0'
    app.db = SQLDatabaseController(database_dir, database_filename)
    _sql_helpers.ensure_correct_version(
        app.ibs,
        app.db,
        app.dbweb_version_expected,
        DBWEB_SCHEMA
    )


def start_tornado(app, port=5000, browser=BROWSER, blocking=False, reset_db=True):
    def _start_tornado():
        http_server = tornado.httpserver.HTTPServer(
            tornado.wsgi.WSGIContainer(app))
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    # Open the web internal database
    init_database(app, reset_db=reset_db)
    # Initialize the web server
    logging.getLogger().setLevel(logging.INFO)
    try:
        app.server_ip_address = socket.gethostbyname(socket.gethostname())
        app.port = port
    except:
        app.server_ip_address = '127.0.0.1'
        app.port = port
    url = 'http://%s:%s' % (app.server_ip_address, app.port)
    print('[web] Tornado server starting at %s' % (url,))
    if browser:
        import webbrowser
        webbrowser.open(url)
    # Blocking
    _start_tornado()
    # if blocking:
    #     _start_tornado()
    # else:
    #     import threading
    #     threading.Thread(target=_start_tornado).start()


def start_from_terminal():
    '''
    Parse command line options and start the server.
    '''
    parser = optparse.OptionParser()
    parser.add_option(
        '-p', '--port',
        help='which port to serve content on',
        type='int', default=DEFAULT_PORT)
    parser.add_option(
        '--db',
        help='specify an IBEIS database',
        type='str', default='testdb0')

    opts, args = parser.parse_args()
    app.ibs = ibeis.opendb(db=opts.db)
    start_tornado(app, opts.port)


def start_from_ibeis(ibs, port=DEFAULT_PORT):
    '''
    Parse command line options and start the server.
    '''
    dbname = ibs.get_dbname()
    if dbname == 'CHTA_Master':
        app.default_species = Species.CHEETAH
    elif dbname == 'ELPH_Master':
        app.default_species = Species.ELEPHANT_SAV
    elif dbname == 'GIR_Master':
        app.default_species = Species.GIRAFFE
    elif dbname == 'GZ_Master':
        app.default_species = Species.ZEB_GREVY
    elif dbname == 'LION_Master':
        app.default_species = Species.LION
    elif dbname == 'PZ_Master':
        app.default_species = Species.ZEB_PLAIN
    elif dbname == 'WD_Master':
        app.default_species = Species.WILDDOG
    elif dbname == 'NNP_Master':
        app.default_species = Species.ZEB_PLAIN
    elif dbname == 'GZC':
        app.default_species = Species.ZEB_PLAIN
    else:
        app.default_species = None
    print('DEFAULT SPECIES: %r' % (app.default_species))
    app.ibs = ibs
    start_tornado(app, port)


if __name__ == '__main__':
    start_from_terminal()
