import base64


def pic2py(picture_names: list, py_name):
    write_data = []
    for picture_name in picture_names:
        filename = picture_name.replace('.', '_')
        with open("%s" % picture_name, 'rb') as r:
            b64str = base64.b64encode(r.read())
        # 注意这边 b64str 一定要加上.decode()
        write_data.append('%s = "%s"\n' % (filename, b64str.decode()))

    with open(f'{py_name}.py', 'w+') as w:
        for data in write_data:
            w.write(data)


# 需要转码的图片：
pics1 = ["./qrcode.jpg"]
pics2 = ["./logo.ico"]
# 将pics里面的图片写到 image.py 中
pic2py(pics1, 'image_jpg')
pic2py(pics2, 'image_ico')
