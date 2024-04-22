"""
============
This module contains the required_param function for checking request
body parameters flagged as required.
:copyright: (C) 2024 by Prayer Application.
"""

from functools import wraps
from flask import request, jsonify
import json
import traceback

class Decorators:
    """
    This class contains decorators for the application
    """

    @staticmethod
    def required_params(self, *required_parameters):
            """
            Utility function for checking request body parameters flagged as required
            """

            def wrapper(f):
                @wraps(f)
                def wrapped(*args, **kwargs):
                    print("request--->{}".format(request))
                    print("request.args--->{}".format(request.args))
                    print("request.values--->{}".format(request.values))
                    print("request.form--->{}".format(request.form))
                    print("request.data--->{}".format(request.data))
                    try:
                        # extract the json body into a python dict
                        if request.form:
                            request_data = request.form.to_dict()
                        
                        elif request.files:
                            request_data = request.files.to_dict()
                        
                        else:
                            request_data = json.loads(request.data.decode('utf-8'))
                    except Exception as e:
                        traceback.print_exc()
                        response = {"code": "01", "msg": "Malformed JSON Body passed", "data": {}}
                        return jsonify(**response), 200

                
                    missing_params = []
                    for param in required_parameters:
                        if param not in request_data:
                            missing_params.append(param)

                    # display the missing parameters
                    if len(missing_params) > 0:
                        response = {"code": "01",
                                    "msg": "The following required parameters are missing: {}".format(missing_params),
                                    "data": {}}
                        return jsonify(**response), 200
                    return f(*args, **kwargs)

                return wrapped

            return wrapper