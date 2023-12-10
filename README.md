# video2Subtitle 批量视频生成多语言字幕

## 注意
因为faster-whisper中使用CTranslate2，（因为CTranslate2的问题，导致生成英语是正常的，翻译成中文是错误的），所以使用了谷歌翻译，后面可能会改成chatgpt        
所以需要你有代理 因为使用的是谷歌翻译       
需要你安装                
cuda 11.8                            
https://developer.download.nvidia.com/compute/cuda/11.8.0/network_installers/cuda_11.8.0_windows_network.exe                


## 如何使用
```python start.py      ```                  
会生成整个文件夹的视频字幕 包括子目录
init.py里更改配置


- 默认只会处理mp4文件，后面可能会适配其他文件
- 默认会生成双语言字幕分开生成，原始语言和中文
- 默认先转成原始语言，然后才会通过谷歌翻译成中文

     
>init.py里还有一个可以批量翻译文件名的方法可以使用，默认注释掉了
