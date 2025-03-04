=====================
User roles by company
=====================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:412b244590f18253b21a2f15b15c2cbbc8ec3decfc64dbf12973646123cb3193
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fserver--backend-lightgray.png?logo=github
    :target: https://github.com/OCA/server-backend/tree/16.0/base_user_role_company
    :alt: OCA/server-backend
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/server-backend-16-0/server-backend-16-0-base_user_role_company
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/server-backend&target_branch=16.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

Enable User Roles depending on the Companies selected.

A company specific Role will only be enabled
if it is set for **all** the currently selected companies.

For example, if a user is "Sales Manager" only for Company A,
it will see that role enabled only if Company A is selected.
If the user selects Company A and Company B,
then the "Sales Manager" role won't be enabled.

**Table of contents**

.. contents::
   :local:

Configuration
=============

Roles are set on the User form.

The "Company" additional column allows to set a Role as only valid for specific companies.

There is also a "Active Role" techincal field, only visible in developer mode.
It shows what roles are active, after applying the company selection rules.

Usage
=====

Select the active companies from the web client widget, near the top right corner.
When doing so, the User's security Groups are recomputed, based on the Roles.

When the user changes the company selection, only the groups available to all active companies will be activated.

For example:

* A "SALES PERSON" and a "SALES MANAGER" roles are created.

* A user is assigned to the roles:
    * "SALES PERSON", with no specific company assigned (meaning all)
    * "SALES MANAGER" only to "My Company (Chicago)"

* When selecting active companies from the UI widget:
    * If only "My Company (San Francisco)" is active, "SALES PERSON" will be active.
    * If only "My Company (Chicago)" is active, "SALES PERSON" and "SALES MANAGER" will be active.
    * If both "My Company (San Francisco)" and "My Company (Chicago)" is active, "SALES PERSON" will be active.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/server-backend/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/server-backend/issues/new?body=module:%20base_user_role_company%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Open Source Integrators

Contributors
~~~~~~~~~~~~

`Open Source Integrators <http://opensourceintegrators.com>`_

  * Daniel Reis <dreis@opensourceintegrators.com>
  * Chandresh Thakkar <cthakkr@opensourceintegrators.com>
  * Urvisha Desai <udesai@opensourceintegrators.com>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/server-backend <https://github.com/OCA/server-backend/tree/16.0/base_user_role_company>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
