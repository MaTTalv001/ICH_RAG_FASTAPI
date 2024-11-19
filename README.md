# ICH ガイドライン RAG ツール

## 概要

本ツールは、ICH ガイドラインの効率的な情報検索を実現する RAG（Retrieval-Augmented Generation）システムです。AI による回答生成と、参照元ガイドラインへのリンク提供により、ガイドラインの横断的な情報アクセスを支援します。

## 機能

本システムは以下の 3 つの主要機能を提供します：

1. **データ収集機能**  
   ICH ガイドラインの自動ダウンロードとテキストデータ・メタデータの構造化保存

2. **ベクトル化機能**  
   ダウンロードしたガイドラインのベクトルデータベース化と永続化

3. **検索・回答生成機能**  
   RAG による高精度な情報検索と回答生成

## システム構成

- **Streamlit UI**: 管理機能およびユーザーインターフェース（localhost:8501）
- **FastAPI**: RAG 機能に特化した RESTful API（localhost:8000）

両サービスは共通のデータストアを使用し、シームレスな連携を実現しています。

## 環境構築

### 前提条件

- Docker
- Git

### セットアップ手順

1. リポジトリのクローン

```bash
git clone [repository-url]
```

2. 環境変数の設定

- `.env.template`をコピーして`.env`を作成
- 必要な LLM 用 API キーを設定

3. ガイドラインデータの準備

- `dataset/ich.csv`に必要なガイドライン情報を登録
- PMDA ウェブサイトを参照し、適宜更新

4. システムの起動

```bash
docker compose up --build
```

## 使用方法

### 初期セットアップ（管理者向け）

1. Streamlit UI にアクセス（http://localhost:8501）
2. 管理者モードでガイドラインのダウンロードを実行
3. ベクトル化処理を実行

※初期設定には一定の処理時間が必要です

### RAG 機能の利用

#### Streamlit UI

- ユーザーモードでの対話的な情報検索が可能

#### FastAPI

リクエスト例：

```bash
curl -X POST "http://localhost:8000/rag" \
     -H "Content-Type: application/json" \
     -d '{"question": "ICHガイドラインにおける安定性試験について教えてください"}'
```

レスポンス例：

```json
{
  "answer": "安定性試験は医薬品の品質保証において重要な...",
  "sources": [
    {
      "title": "安定性試験ガイドライン",
      "code": "Q1A(R2)",
      "category": "Quality",
      "source_file": "example.pdf",
      "preview": "安定性試験の基本的な考え方について..."
    }
  ]
}
```
