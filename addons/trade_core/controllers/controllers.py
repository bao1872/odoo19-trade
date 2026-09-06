# from odoo import http


# class TradeCore(http.Controller):
#     @http.route('/trade_core/trade_core', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trade_core/trade_core/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trade_core.listing', {
#             'root': '/trade_core/trade_core',
#             'objects': http.request.env['trade_core.trade_core'].search([]),
#         })

#     @http.route('/trade_core/trade_core/objects/<model("trade_core.trade_core"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trade_core.object', {
#             'object': obj
#         })

