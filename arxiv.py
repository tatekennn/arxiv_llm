# main.py
"""
メイン実行スクリプト
"""

import logging
from config import BASE_QUERY, TERM_DAYS, THEME, TITLE_FILTER, AUTHOR_FILTER, ABSTRACT_FILTER, INCLUDE_FILTER, EXCLUDE_FILTER
from arxiv_utils import build_search_query, get_recent_papers
from gpt_utils import filter_and_summarize_papers
from openai import OpenAI

def setup_logging():
    import logging
    from config import LOG_FORMAT
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def main():
    setup_logging()
    logging.info("プログラム開始：arXiv APIから論文を取得中...")
    
    # クエリを動的に生成
    search_query = build_search_query(
        base_query=BASE_QUERY,
        title=TITLE_FILTER,
        author=AUTHOR_FILTER,
        abstract=ABSTRACT_FILTER,
        include=INCLUDE_FILTER,
        exclude=EXCLUDE_FILTER
    )
    
    # arXivから論文を取得
    papers = get_recent_papers(search_query, TERM_DAYS)
    if not papers:
        logging.info("指定された期間内に新しい論文は見つかりませんでした。")
        return
    
    # OpenAIクライアントの初期化
    # ※ APIキーは .env から設定されている前提です
    client = OpenAI()
    logging.info("GPTによるフィルタリングと要約を開始します...")
    
    filtered_papers = filter_and_summarize_papers(client, papers, THEME)
    
    if not filtered_papers:
        logging.info("テーマに一致する論文はありませんでした。")
    else:
        logging.info(f"テーマに一致する論文数: {len(filtered_papers)}")
        for i, paper in enumerate(filtered_papers, start=1):
            print(f"論文 {i}:")
            print(f"タイトル: {paper['title']}")
            print(f"URL: {paper['url']}")
            print(f"理由: {paper['reason']}")
            print("要約:")
            print(paper['summary'])
            print("-" * 40)

if __name__ == "__main__":
    main()
