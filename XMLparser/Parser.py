import xml.etree.ElementTree as ET
import re
import sys

import CppGenerator

# var1 = sys.argv[1]
# tree = ET.parse(var1)
while True:
    file = input('파일명을 입력하세요 : ')
    if file == 'exit':
        break
    pattern = '\w+[.][x][m][l]'
    p = re.compile(pattern)
    m = p.match(file)

    if m:
        tree = ET.parse(file)
        root = tree.getroot()

        types = []
        publishers = []
        subscribers = []
        for type in root.findall('.//types'):
            tempType = {}
            for child in type:
                if child.tag == 'struct':
                    tempType['struct'] = child.get('name')
                    members = []
                    for member in child:
                        members.append(member.attrib)
                    tempType['member'] = members
                else:
                    name = child.get('name')
                    value = child.get('value')
                    typeSt = child.get('type')
                    temp = [name, value, typeSt];
                    if name is "MAX_NAME_LEN":
                        tempType['MAX_NAME_LEN'] = temp
                    else:
                        tempType['MAX_MSG_LEN'] = temp
                    types.append(tempType)

        for pub in root.findall('.//publisher'):
            tempPub = {}
            tempPub['name'] = pub.get('name')
            tempPub['topic'] = pub[0].get('topic_ref')
            tempPub['msg'] = pub[0].text
            publishers.append(tempPub)

        for sub in root.findall('.//subscriber'):
            tempSub = {}
            tempSub['name'] = sub.get('name')
            tempSub['topic'] = sub[0].get('topic_ref')
            tempSub['msg'] = sub[0].text
            subscribers.append(tempSub)

        gen = CppGenerator.generator(types, publishers, subscribers)
        gen.make_pub()
        gen.make_sub()
        exit(0)
    else:
        print('잘못 된 파일 형식입니다.')
