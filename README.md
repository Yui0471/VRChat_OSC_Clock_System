# VRChat OSC Clock System

本データはVRChat想定のアバターにセットアップし、OSC送信を介してPCのローカル時間をアバターに表示させるものです。
時刻表示の他、汎用的なデジタルディスプレイとしても使用できます。(タイマーやカウントダウンなど)  


安定版はBoothにて配布しています。  
細かい説明などはこちらを参照してください。  
https://wind-garden.booth.pm/items/3305793


# DEMO

[![thumbnail](https://pbs.twimg.com/ext_tw_video_thumb/1503126781372428290/pu/img/Gy-_ce05jCOU7y_P.jpg)](https://twitter.com/Yui0471/status/1503126841082593280/video/1)

[![thumbnail](https://pbs.twimg.com/media/FM2wWncaUAEF1nf?format=jpg&name=small)](https://twitter.com/Yui0471/status/1499048736651366400)

[![thumbnail](https://pbs.twimg.com/ext_tw_video_thumb/1499353688879792134/pu/img/IlerDZ5EB0G2FJcb.jpg)](https://twitter.com/Yui0471/status/1499353831645548552/video/1)


# Requirement

* Windows 10 以降想定


## Pythonを使用する場合

* Python 3.8以上
* python-osc 1.8.0

```bash
pip install python-osc
```

# Development Environment

* Windows 10 Home 21H1
* Python 3.8.2
* python-osc 1.8.0
* PyInstaller 4.9
* Visual Studio Code 1.65.2


# Note

適用前に必ずプロジェクトのバックアップを行ってください。  
使用方法に関してはReadMeを参照してください。  
また、本リポジトリは気ままな個人製作ですので仕様がコロコロ変わったりします。  
あとコードがぐちゃぐちゃです。初心者なのでゆるしてね。  


# Author

* 風庭ゆい
* 開発協力 : 味醂, Rounz


# License

* 本データの使用によって生じた何らかのトラブル、損失について、製作者である風庭ゆいは一切の責任を負わないものとします。  
* 改造は自由です。  
* 本データの再配布、販売を禁止します。  
* 本データを使用する際のクレジット表記は必要ありません。  
* 本データをダウンロードした時点で、本規約に同意したものとします。  
* 内部で使用しているライブラリの関係上、GUIアプリケーションのみ[LGPL3.0](https://ja.wikipedia.org/wiki/GNU_Lesser_General_Public_License)が適用されます。  


最終更新 : 2022/04/06
