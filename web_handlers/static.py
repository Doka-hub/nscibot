from aiohttp import web

static_app = web.Application()

static_app.add_routes([web.static('/', 'static')])
