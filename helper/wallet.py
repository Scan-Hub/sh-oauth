# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback

from eth_account.messages import defunct_hash_message
from web3 import Web3

from enums.chain import Chain
from lib import dt_utcnow
from models import UserModel

web3 = Web3()


class WalletHelper:

    @staticmethod
    def get_address_of(signature, msg, chain):
        _address = ''
        _msg_hash = defunct_hash_message(text=msg)

        _address = web3.eth.account.recoverHash(
            _msg_hash,
            signature=signature
        )
        return _address.lower()

    @staticmethod
    def _get_sign_msg(address, nonce):
        return f"I'm signing to ScanHub using nonce {nonce} at address {address}"

    @classmethod
    def get_sign_msg(cls, address):
        _nonce = cls.get_nonce()
        return cls._get_sign_msg(address=address, nonce=_nonce), _nonce

    @staticmethod
    def get_nonce():
        return int(dt_utcnow().timestamp())

    @classmethod
    def verify(cls, signature, address, nonce, chain=Chain.TRON):
        try:
            _msg = cls._get_sign_msg(address=address, nonce=nonce)
            _real_address = cls.get_address_of(msg=_msg, signature=signature, chain=chain)
            if not _real_address or _real_address != address:
                return False
            _user = UserModel.user_of_address(address=address, upsert=True)
            return _user
        except:
            traceback.print_exc()
            return False
