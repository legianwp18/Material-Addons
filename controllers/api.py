import json

from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError
import ast
import werkzeug.wrappers
import datetime
import logging

_logger = logging.getLogger(__name__)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, bytes):
        return str(o)

def valid_response(data, status=200):
    data = {"count": len(data) if not isinstance(data, str) else 1, "data": data}
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(data, default=default),
    )

def invalid_response(typ, message=None, status=401):
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(
            {"type": typ, "message": str(message) if str(message) else "wrong arguments (missing validation)",},
            default=datetime.datetime.isoformat,
        ),
    )

class ApiController (http.Controller):

    @http.route(["/api/v1/post_product_material"], type="http", auth="none", methods=["POST"], csrf=False)
    def post(self, **payload):
        payload = request.httprequest.data.decode()
        payload = json.loads(payload)
        values = {}
        try:
            for k, v in payload.items():
                if "__api__" in k:
                    values[k[7:]] = ast.literal_eval(v)
                else:
                    values[k] = v
            resource = request.env["product.material"].create(values)
        except Exception as e:
            request.env.cr.rollback()
            return invalid_response("params", e)
        else:
            data = resource.read()
            if resource:
                return valid_response(data)
            else:
                return valid_response(data)

    @http.route(["/api/v1/get_product_material", "/api/v1/get_product_material/<id>"], type="http", auth="none", method=['GET'], csrf=False)
    def get(self, id=None, **payload):
        try:
            data = request.env["product.material"].search_read()

            if id:
                domain = [("id", "=", int(id))]
                data = request.env["product.material"].search_read(
                    domain=domain
                )
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        except AccessError as e:
            return invalid_response("Access error", "Error: %s" % e.name)

    @http.route(["/api/v1/put_product_material/<id>"], type="http", auth="none", methods=["PUT"], csrf=False)
    def put(self, id=None, **payload):
        values = {}
        payload = request.httprequest.data.decode()
        payload = json.loads(payload)
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response("invalid object id", "invalid literal %s for id with base " % id)
        try:
            record = request.env["product.material"].browse(_id)
            for k, v in payload.items():
                if "__api__" in k:
                    values[k[7:]] = ast.literal_eval(v)
                else:
                    values[k] = v
            record.write(values)
        except Exception as e:
            request.env.cr.rollback()
            return invalid_response("exception", e)
        else:
            return valid_response(record.read())

    @http.route(["/api/v1/delete_product_material/<id>"], type="http", auth="none", methods=["DELETE"], csrf=False)
    def delete(self, id=None, **payload):
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response("invalid object id", "invalid literal %s for id with base " % id)
        try:
            record = request.env["product.material"].search([("id", "=", _id)])
            if record:
                record.unlink()
            else:
                return invalid_response("missing_record", "record object with id %s could not be found" % _id, 404, )
        except Exception as e:
            request.env.cr.rollback()
            return invalid_response("exception", e.name, 503)
        else:
            return valid_response("record %s has been successfully deleted" % record.id)