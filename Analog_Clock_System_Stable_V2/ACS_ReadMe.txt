【Analog Clock System Stable Version 2.1】

最終更新 : 2022/04/17 風庭ゆい
開発協力 : 味醂, Rounz


【はじめに】----------------------------

　本データはVRChat想定のアバターにセットアップし、
　OSC送信を介してPCのローカル時間をアバターに表示させるものです。
　時刻表示の他、汎用的なデジタルディスプレイとしても使用できます。
　(現在開発検討中)

　細かいセットアップガイドはこちらをご覧ください。
　https://note.com/yui0471/n/nd82e028b5eb6


【利用規約】----------------------------

・本データの使用によって生じた何らかのトラブル、損失について
　製作者である風庭ゆいは一切の責任を負わないものとします。

・改造は自由です。

・本データの再配布、販売を禁止します。

・本データを使用する際のクレジット表記は必要ありません。


【同梱ファイル】----------------------------

　Analog_Clock_system_Stable_V2

　・ACS_OSC_Clock-Simple.exe
　　OSC送信を担当するアプリケーションです。
　　１秒おきに現在時刻を送信します。
　　起動と同時にOSC送信を開始します。

　・ACS_OSC_Clock-GUI.exe
　　OSC送信を担当するアプリケーションです。
　　Simpleと機能が同じですが送信先などの設定をを変更できます。

　・Analog_Clock_Stable_V2.unitypackage
　　アバターセットアップ用UnityPackageです。
　　以下に記述するセットアップにて使用します。

　・ReadMe.txt
　　本ファイルです。

　・texture
　　改変用テクスチャファイルです。


【基本仕様】----------------------------

　マテリアル数：4
　パラメータ数：4
　メモリ占有数：25
　テクスチャ数：1

　Unity2019.4.31.f1 動作確認済
　VRCSDK3-AVATAR-2022.02.16.19.13_Public 動作確認済


　・パラメータについて

　　-AC_hh (float): 時針を制御します。float0.00~0.60で針の向きを変更できます。
　　-AC_mh (float): 分針を制御します。float0.00~0.60で針の向きを変更できます。
　　-AC_sc (float): 秒針を制御します。float0.00~0.60で針の向きを変更できます。

　　-AC_ONOFF (bool): オブジェクト自体のIsActiveを操作します。

　アプリケーションの仕様上、1秒未満の誤差が発生する場合があります。
　また、VRChatの仕様上、ローカルからグローバルへの反映に数秒かかります。


【セットアップ方法】----------------------------

1.VRCSDK3とアバターのパッケージ、その他必要なアセットをインポートしてください。

2.同梱の[Analog_Clock_System_Stable_V2.unitypackage]をインポートします。

3.Asset以下にYuis_Miniature_Garden/Analog_Clockファイルがセットアップされますので参照してください。

4.[Analog_Clock.prefab]ファイルをヒエラルキーにドラッグアンドドロップし、
　アバターのルートオブジェクトの子に置いてください。

※ルートオブジェクトの子以外の場所(孫やArmature以下のボーンなど)に置くと、
　アニメーションの参照がMissingになり正常に動作しません。

5.Analog_Clockオブジェクトを表示させたい位置へ移動させ、
　追従させたいボーンの子に[Analog_Clock_constraint_Point]を移動させます。

6.Analog_Clockオブジェクトに[Parent Constraint]コンポーネントがあるので、
　[Zero]をクリックして位置を初期化します。

7.[FX_Layer_Sample]ファイルがありますので、
　そこからアバターのFXレイヤーのLayer及びParametersへコピーを行ってください。
　※ParametersはEXParameter_Sampleに型の表記がありますのでそちらを参照してください。

8.[EXParameter_Sample]ファイルがありますので、
　各項目をアバターのExpressionParametersへ追加してください。

9.[EXMenu_Sample]ファイルがありますので、
　そちらを参考にアバターのEXMenuへボタンを追加してください。

10.[Analog_Clock]オブジェクトのチェックを外し、非表示状態にします。

9.セットアップ完了です。VRChatへアップロードを行ってください。


【使い方】----------------------------

1.VRChatが起動しているPCでACS_OSC_Clock-Simple.exeまたはACS_OSC_Clock-GUI.exeを実行します。
　※Simple版は起動している間OSCを送信し続けます。
　※GUI版は画面の操作でOSC送信を開始します。

2.セットアップ済みのアバターに着替えて、EXMenuからOSCを有効化しておきます。

3.VRChatがOSCを受信し、アバターのディスプレイ部分に現在時刻が表示されます。

4.アプリケーション終了時はCtrl+Cを押下またはウインドウのxボタンで終了します。


【更新履歴】----------------------------

〇2022/03/13 【Alphatest Version 1.0】
-とりあえず作ってみた

〇2022/03/14 【Alphatest Version 1.1】
-テクスチャの大幅変更
-テクスチャデータを同梱、編集可能に

〇2022/03/15 【Betatest Version 1.0】
-betaへ移行
-アプリケーションの表示を変更

〇2022/03/16 【Betatest Version 1.1】
-アプリケーション内の処理を大幅変更、最適化(Rounzさんありがとう)
-DDSとファイル名が被らないように修正

〇2022/03/16 【Stable Version 2.0】
-安定版リリース
-Boothにて配布開始
-各種テクスチャファイルの同梱

〇2022/03/28 【Stable Version 2.0.1】
-シェーダーがMissingになる問題を修正
-デフォルトシェーダーをUnlit/TransparentCutoutに統一

〇2022/04/17 【Stable Version 2.1】
-アプリケーションのGUI版を同梱


【開発環境】----------------------------

-Windows 10 Home 21H1 Build 19041-SP0
-Python 3.8.2
-python-osc 1.8.0
-PyInstaller 4.9
-Visual Studio Code 1.65.2

