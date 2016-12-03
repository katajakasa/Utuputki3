# -*- coding: utf-8 -*-

from . import auth
from . import events
from . import player
from . import queue

handlers = {
    'auth.login': auth.login,
    'auth.logout': auth.logout,
    'auth.authenticate': auth.authenticate,
    'auth.register': auth.register,
    'auth.update_profile': auth.update_profile,
    'auth.get_profile': auth.get_profile,
    'events.add': events.add,
    'events.edit': events.edit,
    'events.get': events.get,
    'events.get_all': events.get_all,
    'player.add': player.add,
    'player.edit': player.edit,
    'player.get': player.get,
    'player.get_all': player.get_all,
    'player.set_state': player.set_state,
    'queue.get_all': queue.get_all,
    'queue.add': queue.add
}
