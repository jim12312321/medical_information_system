def respond_decide(source_text):
    return '回覆測試'

def resp_json_gen(result, source, source_text, responseMedia):
    d = {}
    d['result'] = result
    d['source'] = source
    d['sourceText'] = source_text
    d['responseMedia'] = responseMedia

    return d