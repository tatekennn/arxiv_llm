# arxiv_utils.py
"""
arXiv API関連の処理をまとめたモジュール
"""

from datetime import datetime, timedelta, timezone
import arxiv
import logging
from config import ARXIV_MAX_RESULTS

def build_search_query(base_query, title=None, author=None, abstract=None, include=None, exclude=None):
    """
    arXivの検索クエリを動的に構築する
    """
    query = base_query
    if title:
        query += f' AND ti:"{title}"'
    if author:
        query += f' AND au:"{author}"'
    if abstract:
        query += f' AND abs:"{abstract}"'
    if include:
        query += f' AND {include}'
    if exclude:
        query += f' NOT {exclude}'
    logging.debug(f"Generated query: {query}")
    return query

def get_recent_papers(query, term_days):
    """
    arXiv APIで指定期間内の論文を取得する
    """
    search = arxiv.Search(
        query=query,
        max_results=ARXIV_MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=term_days)
    papers = []
    logging.info(f"取得開始：{cutoff_date}以降の論文を対象")
    try:
        for result in search.results():
            if result.updated >= cutoff_date:
                papers.append({
                    "title": result.title,
                    "abstract": result.summary,
                    "url": result.entry_id
                })
        logging.info(f"取得した論文数: {len(papers)}")
    except Exception as e:
        logging.error("arXiv APIから論文を取得中にエラーが発生しました", exc_info=e)
    return papers
