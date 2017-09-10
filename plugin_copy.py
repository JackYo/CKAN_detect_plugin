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
        return {'success': False,
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

'''
    plugins.implements(plugins.IResourceView)
    plugins.implements(p.IConfigurer, inherit=True)
    plugins.implements(p.IRoutes, inherit=True)
    
    def update_config(self, config):
        '''
        Set up the resource library, public directory and
        template directory for the view
        '''
        toolkit.add_template_directory(config, u'templates')

    def form_template(context, data_dict):
        return u'templates/package/resource_edit.html'

    def before_map(self,map):
        return map
'''

class IDetectPlugin(plugins.SingletonPlugin):
    #plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IResourceController)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IValidators) 
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IPackageController)
    plugins.implements(plugins.IResourceView)
    plugins.implements(plugins.IConfigurer, inherit=True)

    def update_config(self, config):
        '''
        Set up the resource library, public directory and
        template directory for the view
        '''
        toolkit.add_template_directory(config, u'templates')

    def form_template(context, data_dict):
        return u'templates/package/resource_edit.html'

        u'''
        Returns a string representing the location of the template to be rendered when the edit view form is displayed
        The path will be relative to the template directory you registered using the add_template_directory() 
        on the update_config method, for instance views/my_view_form.html.
        '''

  
    # IResourceController
    def before_create(self, context, resource):
        u'''
        Extensions will receive this before a resource is created.
        :param context: The context object of the current request, this
            includes for example access to the ``model`` and the ``user``.
        :type context: dictionary
        :param resource: An object representing the resource to be added
            to the dataset (the one that is about to be created).
        :type resource: dictionary
        '''
        pass
    
    # IDatasetForm
    def new_template(self):
        u'''Return the path to the template for the new dataset page.
        The path should be relative to the plugin's templates dir, e.g.
        ``'package/new.html'``.
        :rtype: string
        '''
        
    # IDatasetForm
    def validate(self, context, data_dict, schema, action):
        u'''Customize validation of datasets.
        When this method is implemented it is used to perform all validation
        for these datasets. The default implementation calls and returns the
        result from ``ckan.plugins.toolkit.navl_validate``.
        This is an adavanced interface. Most changes to validation should be
        accomplished by customizing the schemas returned from
        ``show_package_schema()``, ``create_package_schema()``
        and ``update_package_schama()``. If you need to have a different
        schema depending on the user or value of any field stored in the
        dataset, or if you wish to use a different method for validation, then
        this method may be used.
        :param context: extra information about the request
        :type context: dictionary
        :param data_dict: the dataset to be validated
        :type data_dict: dictionary
        :param schema: a schema, typically from ``show_package_schema()``,
          ``create_package_schema()`` or ``update_package_schama()``
        :type schema: dictionary
        :param action: ``'package_show'``, ``'package_create'`` or
          ``'package_update'``
        :type action: string
        :returns: (data_dict, errors) where data_dict is the possibly-modified
          dataset and errors is a dictionary with keys matching data_dict
          and lists-of-string-error-messages as values
        :rtype: (dictionary, dictionary)
        '''
    # IValidators
    def get_validators(self):
        u'''Return the validator functions provided by this plugin.
        Return a dictionary mapping validator names (strings) to
        validator functions. For example::
            {'valid_shoe_size': shoe_size_validator,
             'valid_hair_color': hair_color_validator}
        These validator functions would then be available when a
        plugin calls :py:func:`ckan.plugins.toolkit.get_validator`.
        '''
        pass

    # IActions
    u'''
    Allow adding of actions to the logic layer.
    '''
    def get_actions(self):
        u'''
        Should return a dict, the keys being the name of the logic
        function and the values being the functions themselves.
        By decorating a function with the `ckan.logic.side_effect_free`
        decorator, the associated action will be made available by a GET
        request (as well as the usual POST request) through the action API.
        By decrorating a function with the 'ckan.plugins.toolkit.chained_action,
        the action will be chained to another function defined in plugins with a
        "first plugin wins" pattern, which means the first plugin declaring a
        chained action should be called first. Chained actions must be
        defined as action_function(original_action, context, data_dict)
        where the first parameter will be set to the action function in
        the next plugin or in core ckan. The chained action may call the
        original_action function, optionally passing different values,
        handling exceptions, returning different values and/or raising
        different exceptions to the caller.
        '''
        pass


    # IPackageController
    u'''
    Hook into the package controller.
    (see IGroupController)
    '''
    def read(self, entity):
        u'''Called after IGroupController.before_view inside package_read.
        '''
        pass

    def create(self, entity):
        u'''Called after group had been created inside package_create.
        '''
        pass

    def edit(self, entity):
        u'''Called after group had been updated inside package_update.
        '''
        pass

    def delete(self, entity):
        u'''Called before commit inside package_delete.
        '''
        pass

    def after_create(self, context, pkg_dict):
        u'''
            Extensions will receive the validated data dict after the package
            has been created (Note that the create method will return a package
            domain object, which may not include all fields). Also the newly
            created package id will be added to the dict.
        '''
        pass

    def after_update(self, context, pkg_dict):
        u'''
            Extensions will receive the validated data dict after the package
            has been updated (Note that the edit method will return a package
            domain object, which may not include all fields).
        '''
        pass

    def after_delete(self, context, pkg_dict):
        u'''
            Extensions will receive the data dict (tipically containing
            just the package id) after the package has been deleted.
        '''
        pass

    def after_show(self, context, pkg_dict):
        u'''
            Extensions will receive the validated data dict after the package
            is ready for display (Note that the read method will return a
            package domain object, which may not include all fields).
        '''
        pass


    def get_auth_functions(self):
        return {'group_create': group_create}