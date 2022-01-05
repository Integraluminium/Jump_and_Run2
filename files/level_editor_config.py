from files import get_valid_list, input_box, file_dialog
import pygame
import typing
image_dict = get_valid_list.get_path_dict()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

LOWER_MARGIN = 100
SIDE_MARGIN = 675

ROWS = 16
MAX_COLS = 75
TILE_SIZE = 40

HUD_SIZE = (90, 90)

INDEX_LIST = ['0001', '0005',
              '1000', '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010', '1011',
              '1012', '1013', '1014', '1015', '1016', '1017', '1100', '1101', '1102', '1103', '1104', '1105',
              '1106', '1107', '1108', '1109', '1110', '1111', '1112', '1113', '1114', '1115', '1116', '1200',
              '1201', '1202', '1203', '1204', '1205', '1206', '1207', '1208', '1300', '1301', '1302', '1303',
              '1304', '1305', '1306', '1307', '1308', '1309', '1310', '1311', '1312', '1313', '1314', '1315',
              '1316', '1317', '1318', '1319', '1320', '1321', '1322', '1323', '1324', '1325', '1326', '1327',
              '1328', '1400', '1401', '1402', '1403', '1404', '1405', '1406', '1407', '1408', '1409', '1410',
              '1411', '1412', '1413', '1414', '1415', '1416', '1417', '1500', '1501', '1502', '1503', '1504',
              '1505', '1506', '1507', '1508', '1509', '1510', '1511', '1512', '1513', '1514', '1515', '1516',
              '1517', '1600', '1601', '1602', '1603', '1604', '1605', '1606', '1607', '1608', '1609', '1610',
              '1611', '1612', '1613', '1614', '1615', '1616', '1617', '1700', '1701', '1702', '1703', '1704',
              '1705', '1706', '1707', '1710', '1711', '1712', '1713', '1714', '1715', '1716',
              '1717', '1718', '1719', '1720', '1721', '1722', '1800', '1802', '1803', '1804', '1805', "1810", "1811",
              '1900', '1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908', '1909', '1910', '1911',
              '1912', '1913', '1914', '1915', '1916', '1917', '1918', '1919', '2000', '2001', '2002', '2003',
              '2004', '2005', "2006", '2008', "2009",  '2010', '2013', '2014', '2015',
              '2016', '2017', '2018', '2019', '2020', '2022', '2023', '2024', '2025', '2026', '2027',
              '2028', '2029', '2030']
pattern_dict = {
    "gras": "10",
    "dirt": "11",
    "dirt_en": "12",
    "stone": "13",
    "sand": "14",
    "snow": "15",
    "castle": "16",
    "metal": "17",
    "liquids": "18",
    "sp_tiles": "19",
    "items": "20"
}


def get_boxes(x: int, y: int, w: int, h: int, name: str, font: pygame.font = None) -> input_box.ButtonBox:
    boxes = {
        "exit_box": input_box.ButtonBox(x, y, w, h, {
            "cancel": input_box.Button(round(w * 1 / 3), 100, 150, 34, text="cancel"),
            "exit": input_box.Button(round(w * 2 / 3), 100, 150, 34, text="exit")},
                                        text="Do you really want to exit?"),

        "delete_box": input_box.ButtonBox(x, y, w, h, {
            "cancel": input_box.Button(round(w * 1 / 3), 100, 150, 34, text="cancel"),
            "delete_world": input_box.Button(round(w * 2 / 3), 100, 150, 34, text="delete")},
                                          text="Do you really want to delete this World?"),

        "info_box": input_box.ButtonBox(x, y, w, h * 2, {  # +64
            "text1": input_box.TextField(10, 60 + 7, 70, 32, "author:", font=font),
            "author": input_box.InputField(95, 60, 355, 32, "NotDefined"),
            "text2": input_box.TextField(10, 124 - 3, 70, 32, "current", font=font),
            "text3": input_box.TextField(10, 124 + 14 + 3, 70, 32, "level", font=font),
            "current_level": input_box.InputField(95, 124, 355, 32, "NotDefined", disabled=True),
            "text4": input_box.TextField(10, 188 - 3, 70, 32, "next", font=font),
            "text5": input_box.TextField(10, 188 + 14 + 3, 70, 32, "level", font=font),
            "next_level": input_box.InputField(95, 188, 355, 32, "NotDefined", disabled=True),
            "ok": input_box.Button(round(w * 1 / 2), 252, 150, 34, text="ok")},
                                        text="World data:"),

        "layer_box": input_box.ButtonBox(x, y, w, round(h * 2.3), {
            "text1": input_box.TextField(10, 60 - 3, 150, 32, "Background-tiles"),
            "layer4": input_box.ToggleButton(round(w * 2 / 3), 60, text="layer4", active=True),
            "text2": input_box.TextField(10, 124 - 3, 150, 32, "Layer1 and collision"),
            "layer3": input_box.ToggleButton(round(w * 2 / 3), 124, text="layer3", active=True),
            "text3": input_box.TextField(10, 188 - 3, 150, 32, "Decoration"),
            "layer2": input_box.ToggleButton(round(w * 2 / 3), 188, text="layer2", active=True),
            "text4": input_box.TextField(10, 252 - 3, 150, 32, "front"),
            "layer1": input_box.ToggleButton(round(w * 2 / 3), 252, text="layer1", active=True),
            "cancel": input_box.Button(round(w * 1 / 2), 318, 150, 34, text="ok")
        }, text="Z-Index"),
    }
    return boxes[name]


def get_file_explorer(screen_size: tuple[int, int]) -> file_dialog.FileDialog:
    abs_center_x, abs_center_y = screen_size[0] // 2, screen_size[1] // 2
    file_explorer = file_dialog.FileDialog(abs_center_x, abs_center_y, 620, 400, "./levels")
    return file_explorer
