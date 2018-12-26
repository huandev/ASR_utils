# -*- coding:utf-8 -*-
"""
python2
1.对uttid排序
2.构建特征文件
usage: 
	path_wavs:data_TTS/wav/standardTTS
	path_create:data_TTS/fbank/test
"""
import os
import sys

instructions = ["开始测试","暂停","退出","选择第一行","运行","停止","单次触发","正常模式","放大水平时基","放大垂直分辨率","放大采样间隔","放大存储深度","缩小水平时基","缩小垂直分辨率","缩小采样间隔","缩小存储深度","打开时钟工具","打开电源工具","打开通用信号工具","打开I方C工具","打开MIIM工具","打开SPI工具","打开localbus工具","打开DDR工具","打开flash工具","打开时序工具","选择第一行"]

def create_files_wav(dir_wavs, dir_create, prefix_utt=None):
    if "00030" in dir_wavs:
        print("Don't change 00030, it's sample of cvte")
        return
    path_text = os.path.join(dir_create, "text")
    path_wavscp = os.path.join(dir_create, "wav.scp")
    path_utt2spk = os.path.join(dir_create, "utt2spk")

    f_text = open(path_text, "w")
    f_wavscp = open(path_wavscp, "w")
    f_utt2spk = open(path_utt2spk, "w")
    if not prefix_utt:
        #print(dir_wavs)
        prefix_utt = dir_wavs.strip().split('/')[2]
        #print(prefix_utt)
    map_utt = {}
    for filename in os.listdir(dir_wavs):
        # print("\n" + filename)
        transcription = filename.strip().split("_")[0]
        if transcription == "词汇表":
            transcription = "".join(instructions)
        utterance_id = prefix_utt + "_" + filename.replace(".wav", "")
        extended_filename = os.path.join(dir_wavs, filename)
        # print(extended_filename)
        if utterance_id not in map_utt:
            map_utt[utterance_id] = {"transcription": transcription, "extended_filename": extended_filename}
    
    # 按utterance_id排序
    for utterance_id in sorted(map_utt.keys()):
        
        transcription = map_utt[utterance_id]["transcription"]
        extended_filename = map_utt[utterance_id]["extended_filename"]
        
        f_text.write(utterance_id + "	" + transcription + "\n")
        f_wavscp.write(utterance_id + "   " + extended_filename + "\n")
        f_utt2spk.write(utterance_id + "   " + utterance_id + "\n")
    

        #f_text.write(utterance_id + "	" + transcription + "\n")
        #f_wavscp.write(utterance_id + "   " + os.path.join(dir_wavs, filename) + "\n")
        #f_utt2spk.write(utterance_id + "   " + utterance_id + "\n")
    
    f_text.close()
    print(path_text + " created successfully")
    f_wavscp.close()
    print(path_wavscp + " created successfully")
    f_utt2spk.close()
    print(path_utt2spk + " created successfully")
    # 通过 utt2spk 创建 spk2utt 文件
    # utils/utt2spk_to_spk2utt.pl data/fbank/test/utt2spk > data/fbank/test/spk2utt
    path_spk2utt = os.path.join(dir_create, "spk2utt")
    _cmd = "utils/utt2spk_to_spk2utt.pl " + path_utt2spk +"  > " + path_spk2utt
    print(_cmd)
    os.system(_cmd)
    print(path_spk2utt + " created successfully")
    
    # 移除旧测试数据产生的cmvn.scp,否则后续执行steps/make_mfcc.sh的时候会检查cmvn.scp与utt2spk的一致性,产生冲突
    path_cmvnscp = os.path.join(dir_create, "cmvn.scp")
    if os.path.exists(path_cmvnscp):
        _cmd2 = "rm " + path_cmvnscp
        print(_cmd2)
        os.system(_cmd2)
        print(path_cmvnscp + " removed")
    

if __name__ == "__main__":
    script, path_wavs, path_create = sys.argv
    create_files_wav(dir_wavs=path_wavs, dir_create=path_create)


        

