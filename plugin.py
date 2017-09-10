# encoding: utf-8

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def group_create(context, data_dict=None):
    # Get the user name of the logged-in user.
    user_name = context['user']

    # Get a list of the members of the 'curators' group.
    try:
        members = toolkit.get_action('member_list')(
            data_dict={'id': 'curators', 'object_type': 'user'})
    except toolkit.ObjectNotFound:
        # The curators group doesn't exist.
        return {'success': True,
                'msg': "The curators groups doesn't exist, so only sysadmins "
                       "are authorized to create groups."}

    # 'members' is a list of (user_id, object_type, capacity) tuples, we're
    # only interested in the user_ids.
    member_ids = [member_tuple[0] for member_tuple in members]

    # We have the logged-in user's user name, get their user id.
    convert_user_name_or_id_to_id = toolkit.get_converter(
        'convert_user_name_or_id_to_id')
    try:
        user_id = convert_user_name_or_id_to_id(user_name, context)
    except toolkit.Invalid:
        # The user doesn't exist (e.g. they're not logged-in).
        return {'success': False,
                'msg': 'You must be logged-in as a member of the curators '
                       'group to create new groups.'}

    # Finally, we can test whether the user is a member of the curators group.
    if user_id in member_ids:
        return {'success': True}
    else:
        return {'success': False,
                'msg': 'Only curators are allowed to create groups'}


class TestPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)

    def get_auth_functions(self):
        return {'group_create': group_create}

    def before_map(self,map):
        return map

    
    #def update_config(self, config):
        '''
        Set up the resource library, public directory and
        template directory for the view
        '''
    #    toolkit.add_template_directory(config, u'templates')

    #def form_template(context, data_dict):
    #    return u'templates/package/resource_edit.html'
