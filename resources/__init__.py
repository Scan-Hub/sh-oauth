# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.health_check import HealthCheck
from resources.iapi import iapi_resources
from resources.user import UserResource
from resources.wallet import WalletResource
from resources.firebase import FirebaseResource

api_resources = {
    '/wallet': WalletResource,
    '/user': UserResource,
    '/common/health_check': HealthCheck,
    '/firebase': FirebaseResource,
    **{f'/iapi{k}': val for k, val in iapi_resources.items()}
}
