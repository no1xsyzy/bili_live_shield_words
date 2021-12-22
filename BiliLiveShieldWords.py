# coding: utf-8
# <DATA BEGIN>
import re
# 拼音对应的常用汉字
hz_xi="夕兮吸汐西希析昔茜奚唏栖息悉惜淅犀晰腊锡皙溪嘻嬉窸稀蹊蟋曦习席袭洗喜戏系细隙"
hz_jin_jing="巾今斤金矜津筋禁仅尽紧谨锦劲进近浸烬晋京径经荆惊晶睛鲸井景净竞竟靓敬静境镜颈精浄"
hz_pin_ping="拼贫频品聘乒平评凭坪屏瓶苹萍"
hz_ba="八巴扒叭坝把吧芭爸拔疤笆粑耙罢捌跋靶魃霸"
hz_jiu="九久旧纠臼究鸠玖灸咎疚韭赳柩酒阄救厩就揪啾舅鹫"
hz_jiu_1="九久纠究鸠玖灸韭赳阄揪啾"
hz_bai="白百伯呗佰拝败拜柏掰摆"
hz_du_1="妒杜肚笃毒独度读堵渎犊椟赌渡嘟督睹镀" # 排除：竺都
hz_du_2="都杜肚毒独度堵渡睹镀"
hz_liu_lu="六刘柳浏流留琉硫碌溜馏遛榴瘤卢庐芦陆卤虏炉录鸬赂鹿颅绿鲁禄鲈路噜撸辘戮橹璐鹭露" # 重复：六碌
hz_si_shi="四司丝死寺似私祀伺饲驷食思斯肆嗣厮撕嘶十尸士氏什示矢石史市失仕世式师时识始饰视鸤虱实驶事势使侍诗试施恃柿是蚀拭适室狮拾屎峙舐轼逝硕匙释湿谥弑誓嗜噬螫" # 重复：似食
#hz_wei="卫为韦未危伪伟围纬尾违苇位委味畏威娓维惟唯帷萎偎谓尉喂猥痿微蔚薇魏巍"
hz_wei_1="卫未位味畏维萎谓尉喂蔚"
hz_wei_2="为伟围维唯魏"
hz_wei_3="为未伪纬苇委味畏维惟萎谓尉蔚"
hz_ni="尼拟泥妮昵呢逆倪匿腻溺霓" # 排除：你
hz_ma="马妈吗码玛蚂犸麻嘛骂蟆抹"
#hz_bo="卜伯驳拨波泊勃柏玻剥饽钵铂菠啵脖舶博渤搏箔播薄簸"
hz_fa="乏发伐法罚阀砝"
hz_lun="仑伦论抡沦纶囵轮"
hz_gong="公工功供宫攻恭弓躬龚蚣拱巩汞共贡"
# 常见标点符号
p_marks=".,!?+*/#%&()…@~\"\'\\;:<>|=·。，！？；：￥“”‘’—（）【】\-\^\$\[\]" # 用于正则表达式的[]内
f1="(?<![ 0-9\u4E00-\u9FA5])"
f2="(?![ 0-9\u4E00-\u9FA5])"
f3="(?=[^ 0-9\u4E00-\u9FA5]*$)"
sp="󠀠" #旧版机制分隔符，由U+0592改为U+E0020 (UTF-16)

add_space = lambda x: x.group()+" "

# 部分英文字母的处理规则字典（一般替换为希腊字母或全角字母）
letter={
    "a":"α", "A":"Α",
    "k":"κ", "K":"Κ",
    "l":"ｌ", "L":"Ｌ",
    "o":"ο", "O":"Ｏ",
    "r":"ꭇ", "R":"Ꮢ",
    "t":"τ", "T":"Т",
    "x":"χ", "X":"Χ",
    "y":"у", "Y":"Υ",
}

# 屏蔽词列表
words =  [ 
    ### 一般屏蔽词（易变动）
    "即位", "在任", "下台", "倒台", "候选", "选举", 
    "总理", "总统", "纪委", "政府", "国会", "议会",
    "修正", "特权", "政策", "提案", "出访", "审查", 
    "天安", "安门", "赤字", "民众", "中共", "国歌", "金砖",
    "生事", "闹事", "闹剧", "游行", "颠覆", "煽动", "乱暴", "暴乱", "动乱", "暴动",
    "分裂", "抗议", "罢工", "冷战", "圣战", "革命", "起义", "抗争", "厌世", "人肉",
    "国难", "歧视",
    "军队", "部队", "萨德", "履带", "卫兵", "警察", "八路", "番号", "军人", "兵团",
    "囚禁", "施虐", "虐待", "捆绑", "割腕", "剥削", "匕首", "鞭尸", "自残", "灌肠",
    "中出", "高潮", "被透", "走光", "诱惑", "双飞", "梆硬", "女同", "男同", "工口",
    "喘气", "喘息", "娇喘", "呻吟", "处男", "绅士", "性癖", "黄游", "抖m" , "h漫" ,
    "胖次", "罩杯", "嘿咻", "吹气", "掏耳", "助眠", "耳语", "蛋大", "脏病", "开冲",
    "重口", "勃起", "出轨", "黑化", "叫鸡", "痴汉", "进裙", "鸡儿", "爽爆",
    "肉便", "玩逼", "看腿", "跳蛋", "御姐", "迷途", "无码", "果体", "裙底", "换妻",
    "脱光", "丝袜", "漏点", "媚药", "很太", "热舞",
    "肥猪", "下贱", "你妈", "月半", "送妈", "嘴臭", "拉屎", "撤硕", "低俗", "憨批",
    "刁大", "禽兽", "畜生", "吃屎",
    "美国", "米国", "台湾", "香港", "澳门", "日吹",
    "油管", "推特", "新浪", "抖音", "优酷", "淘宝",
    "皇帝", "皇宫", "庙堂", "磕头", "安乐", "包养", "清真", "还愿", "黑魂", "如龙",
    "赌博", "扑克", "彩票", "发票", "博彩", "菠菜", "借贷", "贷款", "传销", "贿赂",
    "新冠", "防疫", "硫酸", "甲烷", "煤气", "氨水", "氨气", "包粉", "白粉",
    "四六", "五四", "七一", "七五", "九八",
    "即为", "试看", "豪迈", "触摸", "初心", "慎重", "三尺", "鲍鱼", "河蟹", 
    "代打", "躺平", "要素", "上街", "读错", "下乡", "闪灵", "集资",
    "百年", "鸡脖", "庆典", "广场", "秃鹰", "细腻", "泼墨", "发酵", "快排", "终共",
    "一哥", "动森", "鸣人", "映画", "老母", "青蛙", "口误", "连睡", "内设", "平总",
    "黑幕", "猎奇", "冲塔", "逆行", "太安", "弹舌", "螳臂", "挡车", "全套", "自重", 
    "牛芝", "比心", "横幅", "饭友", "尚气", "赛艇", "催人", "催吐",
    "小熊", "汪洋", "吼哇", "吼啊", "之那", "膜导", "长者", "郭嘉", "果加", "菓加",
    "与正", "蒂亚", "稻上", "飞草", "熊学", "伐龙", "家明", "马云", "唐可", "泽东",
    "小瓶", "晓平", "超良", "虫也", "虫合", "换声", "代开", "国动", "气弹", "网球",
    "追思", "佐助", "腊肉", "抑郁", "发漂", "咧嘴",
    "ロリ", "はま", "ハマ", "しな", "シナ", "くま", "エロ",

    "hw", "gc", "qd", "rh", "cjp", "cnm", "gay", "ghs", "kui", "lsp", "nmb", "nmd", "ply", "roc", "tmd", "usl", "wic", "wjb", "xxd",
    "boki", "dang", "drug", "frog", "fuck", "knee", "kuma", "loli", "nmsl", "rori", "sina", "tank", "yuan",
    "bajiu", "bitch", "ching", "luoli", "obama", "ruler", "sager", "secom", "shina", "hentai", "huanqi", "panzer", "reddit", "signal", "tiktok", "twitch",
    "excited", "youtube", "exciting", "onedrive", "zhongguo", "revolution", "neverforget",
    "586", "604", "809", "817", "881", "918", "1926", "1953", "1979", "1989", "j8", "g20", "r19", "5km", "100kg",
    "不想活", "自由门", "咖啡因", "死灵魂", "白衬衫", "生理期", "空气炮", "黑历史", "一本道",
    "被传染", "网易云", "爱奇艺", "支付宝", "劈腿男", "缘之空", "一起死", "稻田上", "安眠药", "接班人", 
    "纪念日", "为自由", "李医生", "右大人", "绞肉机", "不唱歌", "女菩萨", "毕业歌", "老鼠台", 
    "梦大师", "脱衣服", "我要射", "来一发", "小柜子", "奇酷比", "比基尼", "【萝莉", "就这？", "逃生2" ,
    "性骚扰", "妖妖灵", "蛋炒饭", "异教徒", "跑得快", "牺牲品", "劳动法", "斯大林", "未成年", "小红书",
    "麻酥酥", "兼职加", "水好多", "滚出去", "黄段子", "给我滚", "没衣服", "玻璃心", "黎明杀", "不过审",
    "色蝴蝶", "色天使", "振动棒", "震动棒", "战车道", "臂当车", "小黄油", "小黄书", "炸学校", "你全家",
    "小幸运", "换平台", "顶不住", "顶得住", "按回车", "找爸爸", "欧金金", "拼多多", "熊出没", "上床了",
    "有神明", "一直播", "看名字", "报警了", "金小姐",
    "四一二", "五三五", "八一七", "九一八", "九九六", "一九二六", "一九五三", 
    "自由之门", "继续前进", "并肩同行", "焕然一新", "二氧化碳", "阿里巴巴", "恐怖分子", "恐怖份子", "田所浩二", "蒙古上单",
    "身经百战", "黑框眼镜", "谈笑风生", "无可奉告", "微小的事", "活不下去", "飘飘欲仙", "分割人生", "坟头蹦迪", "b站员工" ,
    "我是黄金", "没有敌人", "少女之心", "奥斯曼人", "孩子的鞋", "花花公子", "不想回忆", "最大限度", "那个男人", "那位大人", 
    "脑子瓦特", "恐怖漫画", "乡关何处", "有容乃大", "是全裸的", "最后一课", "狼吞虎咽", "时间机器", "疲劳驾驶", "区别对待",
    "的混合物", "波涛汹涌", "报复社会", "官方签约", "我还活着", "贤者模式", "恐怖游戏",
    "黑暗之魂", "求生之路", "上古卷轴", "侠盗飞车", "尸体派对", "动物之森",
    "31年", "80年代", "110吗", "1月23", "7月1日", "7月5日", "7月13", "8月17日", "12月28", 
    "命运共同体", "克里斯托弗", "你是你我是我", "南无阿弥陀佛", "热爱105度", #汉字格式的日期也会被屏蔽，这里没写出来

    ### 字符间隔相关
    "奥#1数#1[魔默]", "一#1口#1[气吃喝]", "收#1[妹弟女]#1[妹弟儿]", "下#1面#2[松紧]", "回#1来#3谢", "观#1众#3v", "还#1没#3封", "姐#1姐#5[逼b]", "妹#1妹#5[逼b]", "弟#1弟#6大", 
    "射#2出#1来", "v#2p#2n", "湿#2视#2频", "[01]#2找#2[01]",
    "[逼b]#3看#1吗", "搜#3这#1个", "投#3比#1赛", "看#3头#1像", "戴#3绿#1帽", "h#3动#1[画漫]", "6#3月#24",
    "同#3性#3恋", "道#3上#3飞", "名#3字#3看", "我#3是#3处", "下#3面#3好", "习#3d#3d", "看#3洗#3澡", "少#3女#3[下自]", "直#3播#3[日草艹操曰]",
    "射#4身#1上", "童#4收#1养", "买#4烟#1花", "删#4评#1论", "改#4中#1国", "花#4全#1裸", "v#4b#3o", "天#4安#4门", "萝#4莉#4控", "正#4太#4控", 
    "加#4速#4器", "习#4大#4大", "[你尼]#4[妈马吗码蚂玛犸嘛母m家]#4[币比逼必猪狗b]",
    "手#5指#5插", "徐#5上#5爽", "许#5艾#5莉", "谢#5日#5双", "下#5面#5痒", "[马周]#5上#5[文梦]", "[鲁撸露]#5一#5发", "[徐许]#5[上玩]#5[碧双霜]",
    "[日草艹操干曰死烧解透跳杀]#6[你尼我他她它]#5[妈马吗码蚂玛犸嘛母m家]", "文#6古#6花", "看#6地#6方", "不#6钱#6[啊3]", "[.]#6c#6c", "[谢x]#6s#6w",
    "准#1备#3纸#1巾", "那#1个#4奶#1奶", "羊#1羊#4结#1婚", "学#1生#4学#1生", "妈#1妈#6唱#1歌", "不#1论#6生#1死", "找#1工#1作#3加",
    "[01]#2还#1是#2[01]", "你#3画#3我#3猜", "闭#3关#3锁#3国", "不#3穿#3衣#3服",
    "清#6透#6世#6界", "n#2t#2t#1o#1p", "w#4e#4i#4b#4o", "一#6个#6人#6寂#6寞", "不#1要#6这#1种#1事#1情", "123456789#30",
    
    "吉#1[尔儿]", "野#1[爹妈]", "射#1[爆爽]", "暴#1[饮食]", "就#1[职職]", "腐#1[败敗]", "称#1[王皇帝]", "微#1[博搏勃]", "奶#1[头汁水]", "涩#1[气批片p]", "精#1[美日湛子]", 
    "乳#1[头首量水摇]", "魂#1[一二三123]", "大#1[麻吊弔胸波奶胃]", "点#1[人1cfl]", "死#1[吧妈法ね]", "色#1[图情皮批逼戒狼b]",
    "[逼b]#1里", "[批阴]#1毛", "[吞吃]#1精", "[左右]#1倾", "[狂猛]#1吃", "[愚暴]#1民", "[红紅]#1[魔通]", 
    "[两二2]#1会", "[玩双晕]#1奶", "[处下熟]#1女", "[调传宗]#1教", "[鸡己几寄性]#1[吧巴八8⑧]", "[湿射硬]#1了", "[欧猫毛]#1派", "[人我给]#1日",
    "[贫小平双]#1乳", "[条包孢窑梯秃矮]#1子", "[杀去爽干操草爹妈饿]#1死", "[插吸]#1[你他她它]", "[.。·]#1[cf]",
    "网#2恋", "巨#2乳", "自#2尽", "涩#2情", "逼#2真", "翻#2墙", "蓝#2灯", "渣#2男", "人#2权", "[逼b]#2[黑毛]", "黑#2[逼b]", "[傻沙煞撒]#2[逼比笔]",
    "支#3那", "去#3搜", "百#3d", "共#3产", "毛#3东", "手#3银", "涩#3图", "肉#3棒", "伪#3娘", "邪#3教", "果#3聊", "裸#3体", "粉#3奶", "内#3射", "子#3宫",
    "自#3[杀殺]", "鸡#3[巴八8⑧]", "[涩色]#3网", "被#3[日草艹操曰]", "[习習吊弔]#3大", "[草艹操]#3b", "[下压]#3注", "[黄色h]#3片", "[做作坐座]#3爱", 
    "六#4四", "八#4九", "车#4震", "援#4交", "后#4入", "流#4世", "主#4席", "黄#4网", "赤#4毒", "近#4评", "孤#4儿", "倒#4车", "[阴陰]#4道", 
    "明#4[泽z]", "近#4苹", "[小进]#4平", "[连再]#4任", "[看好]#4胸", "吃#4[比逼币笔]", "[日草艹操干曰吃]#4[姐妹奶姨吊弔]", 
    "留#5水", "性#5爱", "威#5雄",
    "罗#6莉", "宽#6衣", "彭#6s", "[彭澎p]#6帅", "萝#6[利俐]", "[逼b]#6紧", "[习習]#6[近进]", "加#6v",
    "幼#8[比逼b]",
    
    ### 拼音/部首组合相关
    "[%s]#1[一1]#1下"%(hz_du_2),
    "[%s]#3大#1大"%(hz_xi),
    "[%s]#3没#1了"%(hz_ma),
    "[%s干]#3[一1]#4下"%(hz_bai), # 顺带处理"干#3一#3下"
    "[两量凉梁良粮粱]#4[加家架假甲嫁佳贾驾茄夹+]#4[和河何呵喝核合盒贺禾荷]", #待补充
    "[裸棵菓粿踝]#1聊",
    "[%s]#1[%s]"%(hz_wei_1,hz_ni),
    "[%s]#1尼"%(hz_wei_2),
    "[%s]#3博"%(hz_wei_3),
    "[%s]#1都"%(hz_bai),
    "[%scx]#2[%s呼砰怦秤抨]"%(hz_xi,hz_pin_ping),
    "[%s]#2p"%(hz_xi),
    "[%s8⑧]#3[%s]"%(hz_ba,hz_jiu),
    "[%s]#3[9⑨]"%(hz_ba),
    "[%scx]#3[%s青蜻箐]"%(hz_xi,hz_jin_jing),
    "[%s青蜻箐斥芹斩析祈折所]#3[%s呼乎砰怦秤抨p]"%(hz_jin_jing,hz_pin_ping), 
    "[%s6⑥]#3[%s舍捨]"%(hz_liu_lu,hz_si_shi),
    "[%s]#3[4④]"%(hz_liu_lu),
    "x#3[%s]"%(hz_jiu_1),
    "康#6[买卖麦脉埋迈霾]",
    "[%s洪哄烘]#17"%(hz_gong),
    
    ### 以下屏蔽词已做其它处理（见rules）
    # "hk", "tw", "xi", "zf", "abs", "sex", "tam", "xjp", "xyz", "anal", "arms", "asmr", "fldf", "ntop", "baidu", "antifa", "tmmsme", "yayeae",
    # "isis", "mama", "mimi", "ilibilib", "pilipili", "dilidili", "niconico",
    # "弯弯", "绿绿", "湾湾", "内内", "色色", "啪啪", "啪#2啪#2啪", "鸡#2鸡", "光#3光", "共#4共", "点点点", "大大大大大", "嘀哩嘀哩", "加速加速",
    # "书记", "想死", "干妈", "垃圾", "64", "73", "89", "404", "535", "7\.5", "1\.23",
   
    ### 字母+汉字（仅作简单处理）
    "si法", "你ma", "mei药", "媚yao", "吃shi", "lu#2发",  "看#3id", "加#4qq", "[微薇]#4bo", "dio#3[大小]", "diao#3[大小]", "ri#1[我你]", 

    ### 以下词汇屏蔽已失效
    # "领袖", "领导", "大会", "会议", "伞兵", "疫情", "和谐", "许愿", "退钱", "厕所", "巨人", 
    # "神社", "人妻", "改变", "签约", "失望", "控制", "节奏", "赤裸", "天城", "成都", "爸爸", "没封", "电竞",
    # "黑手", "集会", "光荣", "虾膜", "成人", "中央", "万岁", "萝莉", "没了", "死了",
    # "痒", "爬", "奠", "6年", "71", "1921", "av", "g7", "ma", "sb", "tg", 
    # "小学生", "不习惯", "发不出", "就去泡", "莉莉安", "风平浪静", "老不死的",
]

# 反屏蔽处理规则字典，键为正则匹配表达式（字符串, pat），值为处理结果（字符串或函数, rep）
rules = {
    ### 连续半角空格处理
    " +" :" ",
    ### 单字/特殊字符
    "(?<![花牡虾海车香])蛤(?![蜊蚧子蜃])":"Ha", "蛤": "Ge", "^苟$": "苟"+sp,
    "翠": "翆", "尻": "𡱧", "淫":"Yin", "岿": "巍", "屌": "吊", "党": "Dαng", "虵": "蛇", "醜": "醜 1",
    "[àáâãäåÀÁÂÃÄÅāǎ]": "a", "[èéêëÈÉÊËēě]": "e", "[ìíîïÌÍÎÏīǐ]": "i", "[òóõôöÒÓÔÕÖōǒ]": "o", "[ùúûüÙÚÛÜūǔ]": "u", "[ǖǘǚǜü]": "v",
    "⑤": "(5)", "⑥": "(6)", "⑧": "(8)", "⑨": "(9)", "⑩": "(10)", "０": "0", "５": "5", "６": "6", "９": "9", "×": "x", "♀": "",
    "Ⅰ": "I", "Ⅱ": "II", "Ⅲ": "III", "Ⅳ": "IV",
    ### 英文非常规处理规则
    "(?i)(h ?)(k)": lambda x: x.group(1) + letter[x.group(2)],
    "(?ia)(?<!\\w)(t)( ?w| ?a ?m)(?! ?\\w)": lambda x: letter[x.group(1)] + x.group(2),
    "(?ia)(?<!\\w)(x ?)(i)(?! ?\\w)": lambda x: x.group(1)+sp+x.group(2),
    "(?ia)(?<!\\w)(z ?)(f)(?! ?\\w)": lambda x: x.group(1)+sp+x.group(2),
    "(?i)(a)(rm ?s| ?b ?s| ?n ?a ?l| ?n ?t ?i ?f ?a)": lambda x: letter[x.group(1)] + x.group(2),
    "(?i)i ?s ?(?=i ?s)": lambda x: x.group() + sp,
    "(?i)m ?([ai]) ?(?=m ?\\1)": lambda x: x.group() + sp,
    "(?i)([dp]) ?i ?l ?i ?(?=\\1 ?i ?l ?i)": lambda x: x.group() + sp,
    "(?i)i ?l ?i ?b ?(?=i ?l ?i ?b)": lambda x: x.group() + sp,
    "(?i)n ?i ?c ?o ?(?=n ?i ?c ?o)": lambda x: x.group() + sp,
    "(?i)([.,。，·] ?)(c.?n|c.?o.?m|t ?k)": lambda x: x.group(1) + sp*2 + x.group(2),
    "(?i)(a)(.*?j)(.*?p)": lambda x:
        (letter[x.group(1)] + x.group()[1:])
        if measure(x.group(2),7) and measure(x.group(3),7) else x.group(),
    "(?i)(a)(.*?s)(.*?m)(.*?r)": lambda x: #asmr四个字母任意顺序排列均会被屏蔽，这里只考虑常见情况
        (letter[x.group(1)] + x.group()[1:])
        if measure(x.group(2),4) and measure(x.group(3),4) and measure(x.group(4),4) else x.group(),
    "(?i)(f.*?)(l)(.*?d)(.*?f)": lambda x:
        (x.group(1)+letter[x.group(2)]+x.group(3)+x.group(4))
        if measure(x.group(1),7) and measure(x.group(3),7) and measure(x.group(4),7) else x.group(),
    "(?i)(s.*?)(e.*?)(x)": lambda x:
        (x.group(1)+x.group(2)+letter[x.group(3)])
        if measure(x.group(1),3) and measure(x.group(2),3) else x.group(),
    "(?i)(x)(.*?j)(.*?p)": lambda x:
        (letter[x.group(1)]+x.group(2)+x.group(3))
        if measure(x.group(2),5) and measure(x.group(3),5) else x.group(),
    "(?i)(x)(.*?y)(.*?z)": lambda x:
        (letter[x.group(1)]+x.group(2)+x.group(3))
        if measure(x.group(2),7) and measure(x.group(3),7) else x.group(),
    "(?i)(n.*?)(t.*?)(o)(.*p)": lambda x:
        (x.group(1)+x.group(2)+letter[x.group(3)]+x.group(4))
        if measure(x.group(1),4) and measure(x.group(2),2) and measure(x.group(4),2) else x.group(),
    "(?i)r(?=( ?[^ ]){0,5} ?i( ?[^ ]){0,5} ?o( ?[^ ]){0,5} ?t( ?[^ ]){0,5} ?s)":                 lambda x: letter[x.group()], # r#6i#6o#6t#6s
    "(?i)y(?=( ?[^ ]){0,3} ?a( ?[^ ]){0,3} ?y( ?[^ ]){0,3} ?e( ?[^ ]){0,3} ?a( ?[^ ]){0,3} ?e)": lambda x: letter[x.group()], # y#4a#4y#4e#4a#4e
    "(?i)t(?=( ?[^ ]){0,5} ?m( ?[^ ]){0,5} ?m( ?[^ ]){0,5} ?s( ?[^ ]){0,5} ?m( ?[^ ]){0,5} ?e)": lambda x: letter[x.group()], # t#6m#6m#6s#6m#6e
    ### 中文/数字非常规处理规则
    "(年|月|天|小 ?时|分 ?钟|分) ?(前)": lambda x: x.group(1)+sp+x.group(2),
    "([草艹操日][ %s]*)([你我他她它]|[比笔逼]|时光)"%p_marks: lambda x: x.group(1)+sp+x.group(2),
    "(点 ?){2}(?=点)": lambda x: x.group()+sp,
    "(大 ?){4}(?=大)": lambda x: x.group()+sp,
    "([啪绿弯湾内色])(?= ?\\1)": lambda x: x.group(1) + sp,
    "加 ?速 ?(?=加 ?速)": lambda x: x.group() + sp,
    "嘀 ?哩 ?(?=嘀 ?哩)": lambda x: x.group() + sp,
    "鸡.*?(?=鸡)": lambda x: fill(x.group(),3),
    "光.*?(?=光)": lambda x: fill(x.group(),4),
    "共.*?(?=共)": lambda x: fill(x.group(),5),
    "啪.*?(?=啪 ?[^ ]? ?啪)": lambda x: fill(x.group(),3),
    "越(?=( ?[^ ]){0,8} ?共)": "Yue",
    "(想 ?)(死)(?! ?你)": lambda x: x.group(1)+sp+x.group(2),
    "(书 ?)(记)(?! ?舞)": lambda x: x.group(1)+sp+x.group(2), # "藤原书记"不是屏蔽词
    "(?<!老)(干 ?)(妈)": lambda x: x.group(1)+sp+x.group(2),
    "(猎 ?)(人)(?=.*?电 ?影)": lambda x: x.group(1)+sp+x.group(2),
    "([买卖].*?硬 ?)(币)": lambda x: x.group(1)+sp+x.group(2),
    "[习習](?=.*?(平|苹果))": lambda x: "Χi",
    "(?i)([习習].*?)(a)(pp)": lambda x: x.group(1)+letter[x.group(2)]+x.group(3),
    "7\.5": "７.5", "1\.23": "１.23",
    "(?a)(?<!\\w)(6[ %s]*)(4)(?! ?\\w)"%p_marks: lambda x: x.group(1)+"４",
    "(?a)(?<!\\w)(7 ?)(3)(?! ?\\w)": lambda x: x.group(1)+"３",
    "(?a)(?<!\\w)(8)( ?[^ \n\r]? ?9)(?! ?\\w)": lambda x: "８"+x.group(2),
    "(?a)(?<!\\w)(4 ?0 ?)(4)(?! ?\\w)": lambda x: x.group(1)+"４",
    "(?a)(?<!\\w)(5[ %s]*)(3)([ %s]*5)(?! ?\\w)"%(p_marks,p_marks): lambda x: x.group(1)+"３"+x.group(3),
    "(?i)(六|6|⑥|l ?i ?u)(.*?)(四|肆|4|④|s ?i)": lambda x: (x.group(1)+fill(x.group(2),4)+x.group(3)) if x.group(1)+x.group(3)!="64" else x.group(),
    "(?i)([%s贝呗]|b ?a ?i)(?=.*?([%s]|d ?u))"%(hz_bai,hz_du_1): lambda x: "Ⲃei" if x.group() in "贝呗" else "Ⲃai",
    "(?i)(b)(.*?a)(.*?i)(.*?[%s都])"%(hz_du_1): lambda x: 
        ("Ⲃ"+x.group(2)+x.group(3)+x.group(4))
        if measure(x.group(2),4) and measure(x.group(3),4) and measure(x.group(4),4) else x.group(),
    "(?i)([%s] ?|f ?a? ?)([%s会能弄]|l ?u ?n)"%(hz_fa,hz_lun): lambda x: x.group(1)+sp+x.group(2),
    "([干日草艹操曰黄h].*?)(视.*?)(频)": lambda x: x.group(1)+fill(x.group(2),2)+x.group(3), # "[干日草艹操曰]#7视#1频" "[黄h]#3视#1频"
    "([日草艹曰操].*?)(公.*?)(主)": lambda x: x.group(1)+fill(x.group(2),2)+x.group(3), # "操#3公#1主" "[日草艹曰]#9公#1主"
    "([大小妈姐妹哥弟一二三四五六七八九].*?)([小姐妹哥弟一二三四五六七八九].*?)([在来做进])": lambda x:
        (x.group(1)+fill(x.group(2),5+r_pos(x.group(2),"小姐妹哥弟一二三四五六七八九"))+x.group(3))
        if measure(x.group(1),5) and measure(x.group(2),5+r_pos(x.group(2),"小姐妹哥弟一二三四五六七八九")) else x.group(),
    "(?i)([%sail百].*?)([就上去还点被了射让].*?)([来射车有点出被入].*)"%(hz_du_1): lambda x:
        (x.group(1)+fill(x.group(2),5+r_pos(x.group(2),"就上去还点被了射让"))+x.group(3))
        if measure(x.group(1),7) and measure(x.group(2),5+r_pos(x.group(2),"就上去还点被了射让"))
        and not measure(x.group(3),4) else x.group(),
    "([马就].*?)([想上].*?)([鲁撸噜门们])": lambda x:
        (fill(x.group(1),6+r_pos(x.group(1),"马就"))+x.group(2)+x.group(3))
        if measure(x.group(1),6+r_pos(x.group(1),"马就")) and measure(x.group(2),6) else x.group(),
    ### 保护型处理规则
    "[习習]": lambda x: x.group()+sp,
    "妖(?=.*?[a-zA-Z_])": "女夭",
    "(?i)r(?= ?i.*?[你我他她它].*?[妈吗马嘛母m])": lambda x: letter[x.group()],
    "(?i)t(?= ?a.*?[妈吗马嘛母家])": lambda x: letter[x.group()],
    
    ### 新版屏蔽字，旧版机制分隔符不适用（太乱了，啥时候整理一下）
    "脸(?=[^ 0-9]?[很挺][^ 0-9]?大)": add_space,
    "下(?=[^ 0-9]{0,2}[一条][^ 0-9]{0,2}狗)": add_space,
    "[嘴脸鼻眼脑舌](?=[^ 0-9]{0,6}[胖矮丑烦笨傻蠢歪睁])": add_space,
    "[你您他她这个](?=[^ 0-9]{0,3}[脸嘴鼻脑舌货猴胖矮丑烦笨傻蠢歪睁])": add_space,
    "睁(?=[^ ]{0,3}[开嘴脸鼻眼脑舌])": add_space,
    "(?<![大是])猩猩%s"%(f2): "猩 猩",
    "%s猴子%s"%(f1,f3): "猴 子",
    "%s死%s"%(f1,"(?=[^ 2-79\u4E00-\u9FA5]*$)"): "Si",
    "老太婆": "老 太婆",
    "咖喱 ?人": "咖喱/ 人",
    "全 ?家 ?炸": "全 家/炸",
    "孤勇者": "孤 勇者",
    "(?i)你是个P": "你 是个P",
    "彩笔": "彩 笔",
    "一狗": "一 狗",
    "狒狒": "狒 狒",
    "母韵": "母 韵",
    "闭嘴": "闭 嘴",
    "双亲": "双 亲",
    "太笨": "太 笨",
    "渣女": "渣 女",
    "股间": "股 间",
    "尼嚎": "你好",
    "快死": "快 "+sp+"死",
    "牲畜": "牲 1畜",
    "人妖": "人 1妖",
    "智障": "智 1障",
    "垃(?=[^ 0-9]?[垃圾家])": add_space,
    "全(?=[^ 0-9]?家)": add_space,
    "大(?=[^ 0-9]?[妈舌])": add_space,
    "矮(?=[^ 0-9]?子)": add_space,
    "嘴(?=[^ 0-9]?跟)": add_space,
    "小(?=[^ 0-9]?偷)": add_space,
    "变(?=[^ 0-9]?态)": add_space,
    "难(?=[^ 0-9]?[看听])": add_space,
    "%s作(?=[文者啊吧吗么]%s)"%(f1,f3): add_space,
    "没(?=[^ 0-9]?([妈马吗码蚂玛犸嘛]|眼睛|脑子|头脑))": add_space,
    "[妈马吗码蚂玛犸嘛](?=[^ 0-9]?没)": add_space,
    "[一三七](?=[^ 0-9]?丑)": add_space,
    "([有经尿][^ 0-9]{0,3})(病)": lambda x: x.group(1)+" bing ",
    "[%s你您](?=[^ 0-9]?[%s])"%(hz_ni,hz_ma): add_space,
    "[%s](?=[^ 0-9]?[%s您])"%(hz_ma,hz_ni): add_space,
    "[日草艹操干曰死烧解透跳杀](?=.*?[你尼我他她它].*?[妈马吗码蚂玛犸嘛母m家])": add_space,
    "好多(?=[^ 0-9]?猴)": add_space,
    "恶(?=[^ ]?[心丑])": add_space,
    "心(?=[^ ]?[恶丑])": add_space,
    "滚(?=[^ ]?[滚开])": add_space,
    "丑(?=[^ ]?[恶死女男吧吗嘛啊呢哦么])": add_space,
    "死(?=[^ ]?[心狗吧吗嘛啊呢哦么宅])": add_space,
    "[病笨傻](?=[^ 0-9]{0,2}[样人吧吗嘛啊呢哦么了])": add_space,
    "[猪狗](?=[^ ]{0,2}种)": lambda x: x.group()+" / ",
    "%s笨(?=[笨蛋]%s)"%(f1,f3): add_space,
    "%s断(?=[手脖]%s)"%(f1,f3): add_space,
    "%s村(?=人%s)"%(f1,f3): add_space,
    "%s爹(?=妈%s)"%(f1,f3): add_space,
    "(?i)[笨傻](?=.{0,2}[逼比笔币b])": lambda x: x.group()+" 1",
    "(?<!愚)蠢(?! )": add_space,
    "雑(?! )": add_space,
    "[0-9](?=.*?字母表)": add_space,
    "脸(?=.*?像)" : add_space,
    "%s(吃的)(?=吗%s)"%(f1,f3): add_space,
    "残(?=[疾障\u0800-\u4E00])": add_space, # 后接日文时进行保护性处理
}

def get_len(string):
    '''获取正则表达式串string的字段宽度'''
    return len(re.sub(r"\[.+?\]","~",string))

def measure(string,length):
    '''判断字符串string中非空格字符数是否小于length'''
    return get_len(string)-string.count(" ")<length

def fill(string,length):
    '''填补字符串string，使其中的非空格字符数等于length'''
    dots=sp*(length-get_len(string)+string.count(" "))
    return string+dots

def r_pos(string,targets):
    '''查找字符串targets中的字符在字符串string中最后一次出现的位置'''
    r_str=string.replace(" ","")[::-1]
    for index,char in enumerate(r_str):
        if char in targets: return len(r_str)-index-1
# <DATA END>
