==================
foglamp-north-http
==================

FogLAMP North Plugin to send data over HTTP protocol

*******************************
Packaging for http north plugin
*******************************

This repo contains the scripts used to create a foglamp-north-http debian package.

The make_deb script
===================

.. code-block:: console

  $ ./make_deb help
  make_deb help {x86|arm} [clean|cleanall]
  This script is used to create the Debian package of foglamp north http
  Arguments:
   x86      - Build an x86_64 package
   arm      - Build an armv7l package
   clean    - Remove all the old versions saved in format .XXXX
   cleanall - Remove all the versions, including the last one
  $


Building a Package
==================

Select the architecture to use, *x86* or *arm*.
Finally, run the ``make_deb`` command:


.. code-block:: console

    $ ./make_deb arm
    The package root directory is            : /home/pi/foglamp-north-http
    The FogLAMP north HTTP plugin version is : 1.0.0
    The Package will be built in             : /home/pi/foglamp-north-http/packages/Debian/build
    The architecture is set as               : armhf
    The package name is                      : foglamp-north-http-1.0.0-armhf

    Populating the package and updating version file...Done.
    Building the new package...
    dpkg-deb: building package 'foglamp-north-http' in 'foglamp-north-http-1.0.0-armhf.deb'.
    Building Complete.
    $


The result will be:

.. code-block:: console

  $ ls -l packages/Debian/build/
    total 12
    drwxr-xr-x 4 pi pi 4096 Jun 14 10:03 foglamp-north-http-1.0.0-armhf
    -rw-r--r-- 1 pi pi 4522 Jun 14 10:03 foglamp-north-http-1.0.0-armhf.deb
  $


Cleaning the Package Folder
===========================

Use the ``clean`` option to remove all the old packages and the files used to make the package.
Use the ``cleanall`` option to remove all the packages and the files used to make the package.
