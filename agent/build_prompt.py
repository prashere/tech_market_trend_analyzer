import tiktoken

encoding = tiktoken.encoding_for_model('gpt-4o')


def count_tokens(text):
    return len(encoding.encode(text))


def get_full_text_from_df(article_metadata, articles_df):
    match = articles_df[articles_df['url'] == article_metadata['url']]
    if not match.empty:
        return match.iloc[0]['full_text']
    else:
        return None


def build_cluster_prompt(cluster_articles, articles_df, max_tokens=7000):
    base_prompt = (
        "You are a market analyst specializing in technology and AI trends.\n"
        "Analyze the following articles grouped by a common topic.\n"
        "Identify key developments, differences in viewpoints, emerging trends, and strategic moves.\n"
        "Provide a detailed, insightful analysis rather than a simple summary.\n\n"
        "Please output the analysis as a JSON object with the following keys:\n"
        "- title: A concise title for this cluster\n"
        "- key_developments: List key developments\n"
        "- emerging_trends: List emerging trends\n"
        "- differences_in_viewpoints: Note differing opinions or perspectives\n"
        "- strategic_moves: Describe strategic company moves\n\n"
        "Articles:\n"
    )

    prompt = base_prompt
    tokens_used = count_tokens(base_prompt)

    for i, article in enumerate(cluster_articles):
        full_text = get_full_text_from_df(article, articles_df)
        if not full_text:
            full_text = article.get('summary', '')

        article_text = (
            f"{i+1}. Title: {article['title']}\n"
            f"Summary: {article['summary']}\n"
            f"Full Text: {full_text[:1000]}...\n\n"  # truncate long texts
        )

        article_tokens = count_tokens(article_text)
        if tokens_used + article_tokens > max_tokens:
            break

        prompt += article_text
        tokens_used += article_tokens

    prompt += (
        "\nProvide the analysis strictly in the JSON format described above.\n"
        "Ensure the JSON is properly formatted and parsable."
    )

    return prompt
