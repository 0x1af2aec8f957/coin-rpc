from DB.config import db, config
from request.http_s import Proxy
from log.config import LOG

# curl -X POST decode-raw-transaction -d '{"raw_transaction": "070100010161015fc8215913a270d3d953ef431626b19a89adf38e2486bb235da732f0afed515299ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8099c4d59901000116001456ac170c7965eeac1cc34928c9f464e3f88c17d8630240b1e99a3590d7db80126b273088937a87ba1e8d2f91021a2fd2c36579f7713926e8c7b46c047a43933b008ff16ecc2eb8ee888b4ca1fe3fdf082824e0b3899b02202fb851c6ed665fcd9ebc259da1461a1e284ac3b27f5e86c84164aa518648222602013effffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80bbd0ec980101160014c3d320e1dc4fe787e9f13c1464e3ea5aae96a58f00013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8084af5f01160014bb93cdb4eca74b068321eeb84ac5d33686281b6500"}'
# curl -X POST get-unconfirmed-transaction -d '{"tx_id": "382090f24fbfc2f737fa7372b9d161a43f00d1c597a7130a56589d1f469d04b5"}'

request = Proxy()


class Dbf:
    def __init__(self):
        self.db = db
        self.conf = config  # 记录同步的配置信息

    def get_blockCount(self):  # 高度
        height = request.get_response('/get-block-count')['data']['block_count']  # 获取最新的区块高度
        _height = self.conf.find_one({'record': 'height'})['height'] if self.conf.find_one(
            {'record': 'height'}) else 0  # 本地已经同步的高度
        return {'status': height > _height, 'height': _height + 1}

    def get_blockHash(self, height=1):  # 获取hash
        if self.conf.find_one({'record': 'height'}):  # 记录本地同步的高度
            self.conf.update({'record': 'height'}, {"$set": {"height": height}})
        else:
            self.conf.insert({'record': 'height', 'height': height})
        hash = request.get_response('/get-block', {"block_height": height})['data']['hash']
        return hash

    def get_block(self, hash):  # 获取区块信息[兼容btc]
        response = request.get_response('/get-block', {"block_hash": hash})['data']
        hash = response['hash']
        pre_hash = response['previous_block_hash']
        transactions = response['transactions']
        version = response['version']
        height = response['height']
        return {'height': height, 'hash': hash, 'pre_hash': pre_hash, 'transactions': transactions, 'version': version}

    def write(self):  # 写入本地数据库
        while self.get_blockCount()['status']:
            block_count = self.get_blockCount()
            if block_count['status']:
                block = self.get_block(self.get_blockHash(block_count['height']))
                self.db.block.insert(block)
                LOG.info(f"write DB block_height {block['height']} success")
            else:
                LOG.error(f"write DB block_height {block['height']} fail")
                break

    # @classmethod
    def find(self, **kwargs):  # 查询本地数据的数据
        return self.db.block.find(kwargs)
