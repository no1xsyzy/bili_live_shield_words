## B站直播弹幕反屏蔽处理（随缘更新中）

识别并处理B站直播弹幕中的全局屏蔽字，目前主要用于提高VTB直播时的同传/歌词弹幕的存留率。

### 注意事项
+ 收集的屏蔽词绝大部分来自于歌词和同传内容。部分涉党政黄赌毒的屏蔽词没列出来，也没必要处理。
+ 这里只列出简体字，对应的繁体字同样会被屏蔽。
+ B站屏蔽词是在变化的，例如"改变", "签约"有段时间曾经是屏蔽字，现在不是了，但以后仍可能再次被屏蔽。
+ 如果发送了含全局屏蔽字的弹幕，那么API返回的msg一般为f或fire；如果发送了含房间屏蔽字的弹幕，则msg为k。
+ 代码不规范/冗余/处理方法差，望见谅。

### 代码使用示例
<code>
  from BiliLiveAntiShield import BiliLiveAntiShield # 导入反屏蔽类
  anti_shield=BiliLiveAntiShield() # 创建对象
  result=anti_shield.deal("初心 asmr") # 执行反屏蔽处理
  print(result) # 打印处理结果
</code>

输出结果：```初`心 αsmr```

