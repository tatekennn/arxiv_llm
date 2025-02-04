import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# 検索条件
BASE_QUERY = "Decision Transformer"
# 過去何日以内の論文を対象とするか
TERM_DAYS = 34
# 論文の評価テーマ
THEME = "Decision Transformerのtarget returnのよる報酬構造"

# arXiv検索の詳細フィルター（必要に応じて変更してください）
TITLE_FILTER = ""        # 例: "Deep Learning"
AUTHOR_FILTER = ""       # 例: "Smith"
ABSTRACT_FILTER = "Decision Transformer"
INCLUDE_FILTER = ""
EXCLUDE_FILTER = ""

# API設定（必要に応じて）
ARXIV_MAX_RESULTS = 5

# OpenAI API設定（適切なAPIキーの設定が必要です）
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ログ設定
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"