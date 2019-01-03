from pypinyin import lazy_pinyin
import os
import Levenshtein
import sys
import re
import copy

script, dir_decode_result, path_errors_log = sys.argv
threshold_dist = 10
default_instruction = "DEFAULT"
pinyin_table =  "pinyin_table_TTS_man" #"standard_pinyin_table"  #"pinyin_table_audio_AI"

# get pinyin of instructions from file "pinyin_instructions"
pinyin_instruction = dict()
with open(pinyin_table, "r") as f:
    for line in f.readlines():
        instruction, pinyin = line.strip().split(",")
        if pinyin in pinyin_instruction.keys() and (instruction != pinyin_instruction[pinyin]):
            print("Pinyin conflict:"+ instruction + "|" + pinyin_instruction[pinyin])
        pinyin_instruction[pinyin] = instruction

# calculate Levenshtein distance
#threshold_values = []
def get_predicted_instruction(_text):
    _pinyin_text = lazy_pinyin(_text)
    _pinyin_raw = copy.deepcopy(_pinyin_text)
   # 首字母大写
    for i,p in enumerate(_pinyin_text):
        _pinyin_text[i] = p.capitalize() #把第一个字母转化为大写，其余小写
    #pinyin_text = "".join(pinyin_text)
    #pred_pinyin[utt_id]['pinyin'] = pinyin_text

    pattern0 = re.compile(r"[地第的定][零一二两三四五六七八九十百千]+[行航]")
    pattern1 = re.compile(r"[一二两三四五六七八九][千][零一二两三四五六七八九十百]+[行航]")
    pattern2 = re.compile(r"[地第的定].+[行航]")
        
    res0 = re.findall(pattern0, _text)
    res1 = re.findall(pattern1, _text)
    res2 = re.search(pattern2, _text)

    if res0:
        #part_ins = res[0].replace("的", "第")
        part_ins = re.sub(r"[的定地]+", "第", res0[0])
        part_ins = re.sub(r"[行航]", "行", part_ins)

        if "二百" or "二千" in part_ins:
            part_ins = part_ins.replace("二百", "两百")
            part_ins = part_ins.replace("二千", "两千")
        #sim_instruction = "选择" + part_ins 
        text_new = "选择" + part_ins
        _pinyin_text = lazy_pinyin(text_new)
        for i in range(len(_pinyin_text)):
            _pinyin_text[i] = _pinyin_text[i].capitalize()
        # "运行"等不该转换
        if text_new[-1] == "行":
            _pinyin_text[-1] = "Hang"
        #min_dist = -1
        #break
    elif res1:
        text_new = "选择第" + res1[0]
        if "二百" or "二千" in text:
            text = text.replace("二百", "两百")
            text = text.replace("二千", "两千")
        text_new = "选择第" + res1[0]
        for i in range(len(_pinyin_text)):
            _pinyin_text[i] = _pinyin_text[i].capitalize()
        # "运行"等不该转换
        if text_new[-1] == "行":
            _pinyin_text[-1] = "Hang"
        
        #if "二百" or "二千" in sim_instruction:
        #    sim_instruction = sim_instruction.replace("二百", "两百")
        #    sim_instruction = sim_instruction.replace("二千", "两千")

        #min_dist = -1
        #break
        
    #res0 = re.search(pattern0, _text)
    elif res2:
        # "运行"等不该转换
        if _text[-1] == "行":
            _pinyin_text[-1] = "Hang"
        s, e = res2.span()
        for i in range(s, e):
            if _pinyin_text[i] == "De":
                _pinyin_text[i] = "Di"
            if _pinyin_text[i] in ["Ai", "Wan", "Tai", "An"]:
                _pinyin_text[i] = "Er"
            if _pinyin_text[i] in ["Lun","Luo", "Lu"]:
                _pinyin_text[i] = "Liu"
            if (_pinyin_text[i] == "Qin") and (i+1 < e) and (_pinyin_text[i+1] == "Ai"):
                _pinyin_text[i] = "Qian"
                _pinyin_text[i+1] = "Er"
            if _pinyin_text[i] == "Ci":
                _pinyin_text[i] = "Si"
            if _pinyin_text[i] == "Qiu":
                _pinyin_text[i] = "Jiu"

    _pinyin_text = "".join(_pinyin_text)
    if "DiDi" in _pinyin_text:
        _pinyin_text = _pinyin_text.replace("DiDi", "Di")


    min_dist = 1000
    sim_instruction = None
    sim_pinyin = None
    #pred_dist[utt_id] = dict()
    for pinyin, instruction in pinyin_instruction.items():
        #print(pinyin_text)
        #print(pinyin)
        #if pinyin_text == "xianjidedeliangqianqibaisanshijiuhang":
        #    if instruction == "选择第两千七百三十九行" or instruction == "选择第两千七百三十六行": 
        #       print(instruction, pinyin)
        #       dist_tmp = Levenshtein.distance(pinyin_text, pinyin)
        #       print(dist_tmp)
        dist_tmp = Levenshtein.distance(_pinyin_text, pinyin)
        #if min_dist or min_dist==0:
        if dist_tmp < min_dist:
            min_dist = dist_tmp
            sim_instruction = instruction
            sim_pinyin = pinyin
        """
        else:
            min_dist = dist_tmp
            sim_instruction = instruction
            sim_pinyin = pinyin
        """
    if min_dist > threshold_dist or len(_pinyin_text) < 3:
        sim_instruction = default_instruction

    result = {
             "min_dist": min_dist,
             "sim_instruction": sim_instruction,
             "sim_pinyin": sim_pinyin,
             "pinyin_text": _pinyin_text,
             "pinyin_raw": _pinyin_raw}
    #return min_dist, sim_instruction, sim_pinyin, _pinyin_text, _pinyin_raw
    return result
#print(threshold_values)
#print(max(threshold_values))


def get_true_label():
    # get true label
    """
    head -3 test_filt.txt 
    audio_2_停止_1_audio2 停止 
    audio_2_停止_2_audio2 停止 
    audio_2_停止_3_audio2 停止 
    """
    true_chars = dict()
    #path_true_chars = os.path.join("results","decode_test_" + name_result, "scoring_kaldi/test_filt.txt")
    path_true_chars = os.path.join(dir_decode_result, "scoring_kaldi/test_filt.txt")
    #path_true_chars = "results/decode_test_audio_2/scoring_kaldi/test_filt.txt"
    #print("results/decode_test_audio_2/scoring_kaldi/test_filt.txt")
    with open(path_true_chars, "r") as f2:
        for line in f2.readlines():
            #print(line)
            line_tmp = line.strip().split(" ")
            utt_id = line_tmp[0]
            if len(line_tmp) > 1:
                chars = line_tmp[1:]
                text = "".join(chars)
            else:
                text = ""
            true_chars[utt_id] = text
    return true_chars


def evaluate():
    # get predicted chars
    pred_text = dict()
    """
    head -3 7.txt
    audio_2_停止_1_audio2 那个 亭子 
    audio_2_停止_2_audio2 停止 
    audio_2_停止_3_audio2 亭子  
    """
    #path_pred_chars = os.path.join("results","decode_test_" + name_result, "scoring_kaldi/penalty_0.0/7.txt")
    path_pred_chars = os.path.join(dir_decode_result, "scoring_kaldi/penalty_0.0/7.txt")
    with open(path_pred_chars, "r") as f:
        for line in f.readlines():
            line_tmp = line.strip().split(" ")
            utt_id = line_tmp[0]
            #pred_pinyin[utt_id] = dict()
            if len(line_tmp) > 1:
                chars = line_tmp[1:]
                text = "".join(chars)
            else:
                text = ""
            pred_text[utt_id] = text

    pred_dist = dict()
    # get predicted instruction
    for utt_id, text in pred_text.items():
        #pinyin_text = v['pinyin']
        #pinyin_raw = copy.deepcopy(v['pinyin'])
        #text = v['text']
        pred_dist[utt_id] = dict()
        #min_dist, sim_instruction, sim_pinyin, pinyin_text, pinyin_raw = get_predicted_instruction(text)    
        r = get_predicted_instruction(text)
        min_dist = r["min_dist"]
        sim_instruction = r["sim_instruction"]
        sim_pinyin = r["sim_pinyin"]
        pinyin_text = r["pinyin_text"]
        pinyin_raw = r["pinyin_raw"]
        #print("utt_id: {}".format(utt_id))
        #print("pinyin_text is {} pinyin of instruction is {}".format(pinyin_text, sim_pinyin))
        #print("The most similar instruction is {} and the distance is {}\n".format(sim_instruction, min_dist))
        pred_dist[utt_id]["instruction"] = sim_instruction
        pred_dist[utt_id]["pinyin"] = pinyin_text
        pred_dist[utt_id]["dist"] = min_dist
        pred_dist[utt_id]["text"] = text
        pred_dist[utt_id]["pinyin_raw"] = pinyin_raw

    print("------------------------------Evaluate----------------------------------")
    true_chars = get_true_label()
    count_error = 0
    count_ignore = 0
    f_save_errors = open(path_errors_log, "w")
    for utt_id, v in pred_dist.items():
        sim_instruction = v["instruction"]
        pinyin = v["pinyin"]
        pinyin_raw = v["pinyin_raw"]
        dist = v["dist"]
        text = v["text"]
        if sim_instruction == default_instruction:
            count_ignore += 1
        elif true_chars[utt_id] != sim_instruction:
            f_save_errors.write(utt_id + "\n")
            print("utt_id:{}. It's pinyin is {}. It's raw pinyin is {}.It's text is {}.".format(utt_id, pinyin, pinyin_raw, text))
            print("Predicted instruction is: {}. True instruction is {}".format(sim_instruction, true_chars[utt_id]))
            print("Distance is: {} \n".format(dist))
            count_error += 1

    count = len(pred_dist.keys())

    precision = 1 - float(count_error) / (count - count_ignore)       
    print("Total records: {} | Error records: {} | Ignored records: {}".format(count, count_error, count_ignore))
    print("precision is {}".format(precision))

if __name__ == "__main__":
    evaluate()

