### 通过节点端获取到区块数据，解析到本地数据库

> demo 基于[BTM](https://github.com/Bytom/bytom/wiki)节点。

> 应用到 其它的钱包类型 可修改demo内对应的方法即可【主要文件位于-./DB/db.py】，数据库部分直接更改配置即可。

> BTC修改请参考[btc-rpc示例](https://github.com/jgarzik/python-bitcoinrpc)

+ demo仅仅将数据解析到本地数据库（MongoDB），你可以扩展支持节点其它命令。

+ demo解析在节点端完成，关于本地手动解析数据请参考：[electrumx](https://github.com/kyuupichan/electrumx)，推荐手动解析交易数据。  

+ BTM请求节点属于JSON而非JSON-RPC，BTC是JSON-RPC。修改时注意数据结构差异。

+ 关于BTC不支持IPV6，请参考：[bitCoin-IPv6-issues](https://github.com/bitcoin/bitcoin/issues/8491)

+ BTC默认不建立index,'./bitcoin-cli getrawtransaction'该命令仅支持查询自己钱包的信息，通过'./bitcoind -reindex -txindex'命令来建立index后支持查询区块所有交易信息（耗时较长）

+ BTC参考：[BTC-RPC命令](https://blog.csdn.net/yyxyong/article/details/78878899)