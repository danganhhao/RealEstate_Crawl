def convertEstateType(estateType):
    switcher = {
        '\r\nBán căn hộ chung cư\r\n': '1',
        '\r\nBán nhà riêng\r\n': '2',
        '\r\nBán nhà biệt thự, liền kề\r\n': '3',
        '\r\nBán nhà mặt phố\r\n': '4',
        '\r\nBán đất nền dự án\r\n': '5',
        '\r\nBán trang trại, khu nghỉ dưỡng\r\n': '6',
        '\r\nBán kho, nhà xưởng\r\n': '7',
        '\r\nBán loại bất động sản khác\r\n': '8',
        '\r\nBán nhà biệt thự, liền kề (nhà trong dự án quy hoạch)\r\n': '3',
        '\r\nBán nhà mặt phố (nhà mặt tiền trên các tuyến phố)\r\n': '4',
        '\r\nBán đất nền dự án (đất trong dự án quy hoạch)\r\n': '5',
        '\r\nBán đất\r\n': '5',
    }
    return switcher.get(estateType, '')


def convertArea(area):
    area = area.replace('\r\n', '').replace('m²', '')
    if area == u'Không xác định':
        area = 0
    return area


def convertPrice(price, area):
    price = price.replace('\r\n', '').replace('\xa0', '')
    if price == u'Thỏa thuận':
        return 0
    price = price.split(' ')
    if price[1] == r'triệu/m²':
        res = int(float(price[0]) * float(area))
    if price[1] == r'triệu':
        res = int(float(price[0]))
    if price[1] == r'tỷ':
        res = int(float(price[0]) * 1000)
    return res
