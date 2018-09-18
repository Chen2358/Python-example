Markdown 文本解析器，并且支持输出 HTML 格式与 PDF 格式的文件。

依赖

（1）wkhtmltopdf

wkhtmltopdf 是一款能将 HTML 文件转化为 PDF 文件的工具，支持 UNIX 平台与Windows 平台。官方文档 https://wkhtmltopdf.org/index.html

sudo apt-get install wkhtmltopdf

（2）docopt

sudo pip3 install docopt

运行

python3 md2pdf.py doc_template.md -p template.pdf

扩展

使用命令 wkhtmltopdf [url] [outputfile] 即可完成将网页转化为PDF打印。比如 wkhtmltopdf https://www.shiyanlou.com shiyanlou.pdf
