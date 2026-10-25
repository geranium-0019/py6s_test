# Py6S atmospheric correction experiments

PlanetScope画像の取得、DNからTOA放射輝度・反射率への変換、VIIRSの大気情報抽出、Py6Sによる係数計算を試す研究用コードです。

## 実行環境

元の研究環境はPython 3.10です。公開用の依存構成はPillowのセキュリティ修正版に対応するためPython 3.12を使用します。既存環境を上書きせず、別の環境を作成してください。

```bash
conda create -n py6s-public -c conda-forge python=3.12 sixs pip
conda activate py6s-public
python -m pip install --upgrade 'pip>=26.2'
python -m pip install -r requirements.txt
python -m ipykernel install --user --name py6s-public --display-name py6s-public
cp .env.example .env
```

`.env` の `PL_API_KEY` に自身のPlanet APIキーを設定し、JupyterまたはVS Codeで上記カーネルを選択します。6S実行ファイルがPATH上に必要です。`requirements.txt` は直接依存のバージョン記録であり、完全な環境ロックではありません。

## 処理の流れ

ノートブックは `notebooks/` を作業ディレクトリとして実行し、先にリポジトリ直下に `data/` を作成してください。

1. `download_Planet_images.ipynb`: 自身のアクセス権限でPlanet画像を取得。
2. `dn2toa.ipynb`: 取得した画像とXMLからTOA値を計算。
3. `download_VIIRS_images.ipynb`: VIIRSを検索し、大気パラメータを抽出。ダウンロードセルはコメント化されているため、必要に応じて有効化します。NASA Earthdata認証は自身の環境で設定してください。
4. `scripts/extract_metadata.py`: XMLと大気パラメータJSONから入力値を抽出。
5. `atmospheric_correction.ipynb`: 入力値を設定して6Sの係数を計算。

日時・範囲・ファイル名・大気値はサンプルの固定値です。対象データに合わせて更新してください。ダウンロードや変換処理は同名の出力を上書きするため、必要な結果は別途保存してください。

## 公開前の確認

- 認証情報は `.env` 等でローカル管理し、コードや出力に記載しないでください。
- 保存前にJupyterの「すべての出力をクリア」を実行してください。画像もノートブック内部に保存されるため、`data/` の除外だけでは公開を防げません。
- `python scripts/check_notebooks.py` と `git diff --cached` で変更を確認してください。
- GitHub Actionsで秘密情報、ノートブック出力、依存関係の既知の脆弱性を検査します。検査は漏洩の完全な防止を保証しません。
- 衛星データや生成画像を公開する際は、自身の契約・利用条件で公開可能なものに限ってください。このリポジトリはデータの再配布権限を付与しません。

コードのライセンスはまだ指定していません。再利用の許諾条件は作者への確認が必要です。

## 秘密情報を誤って公開した場合

まず提供元で認証情報を失効・再発行してください。ファイルの削除だけでは過去のGit履歴から消えません。必要に応じて履歴や公開済み成果物も整理してください。秘密情報を含むIssueは作成しないでください。
