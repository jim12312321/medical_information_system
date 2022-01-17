def respond_decide(source_text, senario):
    # Senario
    # * crash
    # * faint
    # * fire
    # * init
    if senario == 'crash':
        # 車禍
        if "安全處" in source_text:
            if "都在" in source_text:
                # 車禍，人員都在安全處
                return "確認人員都在安全處，請放置告示牌"
            else:
                # 車禍，有人員不在安全處
                # 先引導人員到安全處避難
                return "請將人員安置於安全處，並請放置告示牌"
        elif "醫護" in source_text or "急救箱" in source_text:
            if "沒有" in source_text:
                # 車禍，現場無急救箱
                return "已確認現場無緊急醫護箱"
            else:
                # 車禍，現場有急救箱
                return "已確認現場有醫護箱，請適當處理傷者"
        elif "意識" in source_text:
            if "無" in source_text:
                # 車禍，現場有無意識傷者
                return "確認現場有無意識傷者，請進一步確認是否還有呼吸心跳，若需要請實施 CPR"
            else:
                # 車禍，現場傷者皆還有意識
                return "已確認現場傷者皆有意識"
        elif "重傷" in source_text:
            if "有" in source_text:
                # 車禍，確認現場有人重傷
                # 等救護人員到場處理
                return "已確認現場有人重傷，請不要任意移動傷者，待救護人員到場後處理"
            else:
                # 車禍，確認現場無人重傷
                # 一樣等候處理
                return "已確認現場無人員重傷，請等待救護人員與警方到場處理"
        else:
            # 無法判斷
            return "無法判斷您的狀況，轉由接線生接聽"
    elif senario == 'faint':
        # 昏迷/失去意識
        if "呼吸" in source_text or "心跳" in source_text:
            if "喪失" in source_text or "無" in source_text or "沒有" in source_text:
                # 昏迷，無呼吸心跳
                # 使用 AED / 施做 CPR
                return "已確認無呼吸心跳，請檢查現場是否有 AED 設備，並立即使用"
            else:
                # 昏迷，有呼吸心跳
                # 等候傷者恢復意識
                return "確認人員有呼吸心跳"
        elif "平躺" in source_text:
            if "不是" in source_text:
                # 昏迷，傷者非平躺
                return "請將人員平躺於地面，並抬高傷者腳部"
            else:
                # 昏迷，傷者平躺
                return "確認人員目前平躺，請抬高傷者腳部"
        elif "陰涼處" in source_text:
            if "不在" in source_text:
                # 昏迷，傷者不在陰涼處
                # 移動傷者
                return "請將傷者移動至陰涼處"
            else:
                # 昏迷，傷者在陰涼處
                return "已確認傷者在陰涼處"
        elif "呼吸困難" in source_text:
            if "有" in source_text:
                # 昏迷，傷者呼吸困難
                # 嘗試解除呼吸困難針狀
                return "已確認傷者呼吸困難，請確認是否有任何物體阻礙傷者呼吸，並移除"
            else:
                # 昏迷，傷者無呼吸困難
                return "已確認傷者無呼吸困難"
        elif "恢復意識" in source_text:
            if "無" in source_text or "尚未" in source_text:
                # 昏迷，傷者依然無恢復意識
                # 現場持續監控
                return "已確認傷者尚未恢復意識，請繼續監控傷者呼吸心跳，並等待救護人員到場"
            else:
                # 昏迷，傷者恢復意識
                return "已確認傷者恢復意識，請稍後救護人員到場"
        else:
            # 無法判斷
            return "無法判斷您的狀況，轉由接線生接聽"
    elif senario == 'fire':
        # 火災現場
        if "受困" in source_text:
            if "有人" in source_text:
                return "已確認有人受困於現場"
            else:
                return "已確認現場無人受困"
        elif "易燃物" in source_text:
            if "沒有" in source_text or "無" in source_text:
                return "已確認現場有易燃物，若有辦法請嘗試移除現場的易燃物"
            else:
                return "已確認現場無易燃物"
        elif "緊急出口" in source_text:
            if "沒有" in source_text or "無" in source_text:
                return "已確認現場無緊急出口，請確保現場還有其他可使用的出入口供人員逃生"
            else:
                return "已確認現場有緊急出口，若有人受困於內請確認人員是否有順利逃生"
        elif "緩降機" in source_text:
            if "沒有" in source_text or "無" in source_text:
                return "已確認現場無緩降機"
            else:
                return "已確認現場有緩降機，請確認是否有人員緩降逃生"
        else:
            # 無法判斷
            return "無法判斷您的狀況，轉由接線生接聽"
        return "火災"
    elif senario == 'init':
        if "車禍" in source_text:
            return "確認案件種類: 車禍"
        elif "昏迷" in source_text or "昏倒" in source_text:
            return "確認案件種類: 失去意識"
        elif "火災" in source_text or "失火" in source_text:
            return "確認案件種類: 火災"
        else:
            return "無法判別案件種類，請重新嘗試"
    else:
        # Unable to decide
        # Refer to 119
        return "對話內容無法辨識，轉由接線生接聽"

def resp_json_gen(result, source, source_text, responseMedia):
    d = {}
    d['result'] = result
    d['source'] = source
    d['sourceText'] = source_text
    d['responseMedia'] = responseMedia

    return d