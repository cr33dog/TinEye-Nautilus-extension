#!/usr/bin/env python
# Based on Open Terminal example by Martin Enlund
import os,sys
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

import gtk
import nautilus
import gconf

BROWSER_KEY = '/desktop/gnome/applications/browser/exec'
URL = 'http://www.tineye.com/search'
#URL = 'http://127.0.0.1:5000'

def error_dialog(message, dialog_title = "Error..."):
   """The extension's error dialog"""
   dialog = gtk.MessageDialog(flags=gtk.DIALOG_MODAL,
                              type=gtk.MESSAGE_ERROR,
                              buttons=gtk.BUTTONS_OK,
                              message_format=message)
   dialog.set_title(dialog_title)
   dialog.run()
   dialog.destroy()

# function almost entirely lifted from Chris AtLee's poster example
def post_tineye(file):

    # Register the streaming http handlers with urllib2
    register_openers()

    # headers contains the necessary Content-Type and Content-Length
    # datagen is a generator object that yields the encoded parameters
    datagen, headers = multipart_encode({"image": open(file, "rb"),})

    # Create the Request object
    request = urllib2.Request(URL, datagen, headers)
    # Actually do the request, and get the response
    try:
        f = urllib2.urlopen(request)
    except:
        error_dialog("Could not post image to tineye.com")
        sys.exit()
    #print f.read()
    #error_dialog(f.read())
    return(f.url)

class SearchTinEyeExtension(nautilus.MenuProvider):
    def __init__(self):
        self.client = gconf.client_get_default()
        
    def _search_tineye(self, file):
        filename = urllib2.unquote(file.get_uri()[7:])
        browser = self.client.get_string(BROWSER_KEY)

        url = post_tineye(filename) 
        os.system('%s "%s"' % (browser, url))
    def menu_activate_cb(self, menu, file):
        self._search_tineye(file)
        
    def menu_background_activate_cb(self, menu, file): 
        self._search_tineye(file)
       
    def get_file_items(self, window, files):
        if len(files) != 1:
            return
        
        file = files[0]
        #if file.is_directory() or file.get_uri_scheme() != 'file':
        #    return
        
        item = nautilus.MenuItem('NautilusPython::search_tineye_item',
                                 'Search TinEye' ,
                                 'Search TinEye for  %s' % file.get_name())
        item.connect('activate', self.menu_activate_cb, file)
        return item,

#    def get_background_items(self, window, file):
#        item = nautilus.MenuItem('NautilusPython::openterminal_item',
#                                 'Open Terminal Here',
#                                 'Open Terminal In This Directory')
#        item.connect('activate', self.menu_background_activate_cb, file)
#        return item,
