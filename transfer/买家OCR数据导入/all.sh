#!/usr/bin/env bash

if [ $# -ne 3 ]; then
    echo 'usage: ./all data_dir 行业代码 备注'
    exit
fi


data_dir=$1
cat ${data_dir}/*.txt > data.txt

sed -i 's/：/:/g' data.txt

titles=('公司名称' '国家/地区' '国家或地区' '国家' '电话' 'tel' '联系人' '传真' 'fax' '地址' '邮编' 'e-mail' 'email' '网址' 'web' '职位' '进口产品' '进口商品' '主要进口商品(中文)' '采购产品')
for title in "${titles[@]}"; do
sed -i -e "s/$title/\n$title/ig" data.txt
done

python3 buyer_ocr.py "$2" "$3"
#python3 export.py
