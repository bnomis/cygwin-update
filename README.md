# cygwin-update

This is a simple script for Macs that will update your cygwin mirror using rsync while you are sleeping.

It installs a simple service (via launchd) which downloads the latest setup.exe and runs rsync for the architecture of your choice.

The `cygwin.py` script makes a number of assumptions, including the following:

* The repository is cloned in to `/var/root/src`.
* Logging is to `/var/root/logs/cygwin.log`.
* Update time is 00:10AM.
* Where the files should be saved.
* User and Group for chown after the sync.
* The only architecure to download is x86_64.
* It pre-defines a source rsync mirror.

These assumptions probably do not match with your needs, so you'll need to edit the `cygwin.py` and `org.cygwin.update.plist` files to suit.

## Choosing A Mirror

There's a script included called `mirrors.py` to help you in choosing which source mirrors to use. The script will:

1. Download a list of rsync mirrors from cygwin.org.
2. Time the download of a file from each mirror.
3. Print out ordered results with the fastest mirror first.


## Install

The script needs to be run as root, so become root before installing.

1. Clone this repository.
2. Edit the `cygwin.py` and `org.cygwin.update.plist` files to suit. (See above.)
3. Run the `install.py` script.

## Uninstall

1. Run the `uninstall.py` script.

## Mounting Disks and Running When No-one is Logged In

Mac OS X will, by default, unmount all external disks when there is no user logged in on the console. So, if your syncing to an external disk when logged out the `cygwin.py` script will fail. The unmounting behaviour can be changed by editting the file `/Library/Preferences/SystemConfiguration/autodiskmount.plist` to look like the following. A suitable version of this file is included here for your copying pleasure.


```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>AutomountDisksWithoutUserLogin</key><true />
</dict>
</plist>
```

