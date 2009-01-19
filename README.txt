repoze.what.plugins.config -- repoze.what with pasterconfig
===========================================================

.. topic:: Overview

  ``repoze.what.plugins.config`` allows you to configure ``repoze.who`` and 
  ``repoze.what`` using ``pastedeploy``. repoze.who and repoze.what are 
  WSGI middleware frameworks for authentication and authorization, 
  respectively. ``paster`` and ``pastedeploy`` allows you to configure your WSGI 
  application via INI files.


Installing repoze.what.plugins.config
=====================================

You can install repoze.what.plugins.config using git::

    git clone git://github.com/jdinuncio/repoze.what.plugins.config.git
    cd repoze.what.plugins.config
    python setup.py install


Using repoze.what.plugins.config
================================

``repoze.what.plugins.config`` offers a config entry point for pastedeploy to
instantiate a ``repoze.who+repoze.what`` middleware. You can use it 
as a filter in the paster INI file::

    [filter:what]
    use = egg:repoze.what.plugins.config#config
    config_file = %(here)s/what.ini
    who_config_file = %(here)s/who.ini

The ``what.ini`` file has the same format of a who INI file, with the following 
additions:

* You can define what plugins.
* There is a special section ``what`` with  ``group_adapters`` and 
  ``permission_adapters`` entries.

You can combine who.ini and what.ini in one file. If you decide to do this,
remember that a ``repoze.what`` modprovider will be implicitly added to
your ``repoze.who`` configuration.

Example of use
==============

Here is a valid what.ini config file::

    [plugin:basicauth]
    use = repoze.who.plugins.basicauth:make_plugin
    realm = 'zbfg'

    [plugin:htpasswd]
    use = repoze.who.plugins.htpasswd:make_plugin
    check_fn = repoze.who.plugins.htpasswd:plain_check
    filename = %(here)s/passwd

    [plugin:ini_group]
    use = repoze.what.plugins.ini:INIGroupAdapter
    filename = group.ini

    [plugin:ini_permission]
    use = repoze.what.plugins.ini:INIPermissionsAdapter
    filename = permissions.ini

    [general]
    request_classifier = repoze.who.classifiers:default_request_classifier
    challenge_decider = repoze.who.classifiers:default_challenge_decider
    remote_user_key = REMOTE_USER

    [identifiers]
    plugins = basicauth

    [authenticators]
    plugins = htpasswd

    [challengers]
    plugins = basicauth

    [what]
    group_adapters = ini_group
    permission_adapters = ini_permission


