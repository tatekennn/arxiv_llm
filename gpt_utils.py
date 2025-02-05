# gpt_utils.py
"""
GPT-4を利用して論文のテーマ適合性評価と要約を行うモジュール
"""

import logging
from config import OPENAI_MODEL

def evaluate_paper_theme(client, paper, theme):
    """
    論文のタイトルと要約からテーマ適合性を評価する
    """
    prompt_theme = f"""
あなたは研究テーマを評価する専門家です。以下の論文のタイトルと要約を読んで、この論文が次のテーマ「{theme}」に一致しているかを判定してください。
一致している場合は「はい」、一致していない場合は「いいえ」と回答し、その理由を簡単に述べてください。

タイトル: {paper['title']}
要約: {paper['abstract']}
"""
    try:
        response_theme = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "あなたは研究評価の専門家です。"},
                {"role": "user", "content": prompt_theme}
            ]
        )
        answer_theme = response_theme.choices[0].message.content.strip()
        logging.debug(f"テーマ評価結果: {answer_theme}")
        return answer_theme
    except Exception as e:
        logging.error("テーマ評価中にエラーが発生しました", exc_info=e)
        return ""

def summarize_paper(client, paper):
    """
    論文のタイトルと要約から、主な内容を3点で箇条書きにて要約する
    """
    prompt_summary = f"""
あなたは論文を要約する専門家です。以下の論文のタイトルと要約を読んで、主な内容を3つのポイントで短く要約してください。
箇条書きでお願いします。

タイトル: {paper['title']}
要約: {paper['abstract']}
"""
    try:
        response_summary = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "あなたは論文要約の専門家です。"},
                {"role": "user", "content": prompt_summary}
            ]
        )
        summary = response_summary.choices[0].message.content.strip()
        logging.debug(f"論文要約結果: {summary}")
        return summary
    except Exception as e:
        logging.error("論文要約中にエラーが発生しました", exc_info=e)
        return ""

def filter_and_summarize_papers(client, papers, theme):
    """
    論文リストに対して、テーマ適合性の評価と要約を実施する
    """
    filtered_papers = []
    for paper in papers:
        logging.info(f"論文評価開始: {paper['title']}")
        answer_theme = evaluate_paper_theme(client, paper, theme)
        if "はい" in answer_theme:
            summary = summarize_paper(client, paper)
            filtered_papers.append({
                **paper,
                "reason": answer_theme,
                "summary": summary
            })
        else:
            logging.info(f"テーマ不一致: {paper['title']} -> {answer_theme}")
    return filtered_papers
