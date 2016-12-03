# -*- coding: utf-8 -*-


async def login(request):
    request.broadcast({'test': 'test'})


async def logout(request):
    request.send_message({'test': 'test2'})


async def authenticate(request):
    pass


async def register(request):
    pass


async def update_profile(request):
    pass


async def get_profile(request):
    pass
