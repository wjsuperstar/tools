# -*- coding: utf8 -*-
import xlrd
import cantools
import codecs


_default_message_key_map = [
    # dbc name / excel header
    ('frame_id', '报文标识符'),
    ('name', '报文名称'),
    ('length', '长度'),
    #('signals', ''),
    ('comment', '报文描述'),
    ('senders', ''),
    ('send_type', '报文发送类型'),
    ('cycle_time', '报文周期时间'),
    ('dbc_specifics', ''),
    #('is_extended_frame', ''),
    ('bus_name', ''),
    ('signal_groups', ''),
    ('strict', ''),
    ('protocol', '')
]

_default_signal_key_map = [
    # dbc name / excel header
    ('name', '信号名称'),
    #('start', '位'),
    ('length', '信号长度'),
    ('byte_order', ''),
    ('is_signed', ''),
    ('initial', '初始值'),
    ('scale', '精度'),
    ('offset', '偏移量'),
    ('minimum', '物理最小值'),
    ('maximum', '物理最大值'),
    ('unit', '单位'),
    ('choices', ''),
    ('dbc_specifics', ''),
    ('comment', '信号描述'),
    ('receivers', ''),
    ('is_multiplexer', ''),
    ('multiplexer_ids', ''),
    ('multiplexer_signal', ''),
    ('is_float', ''),
    ('decimal', ''),
    ('spn', '可疑参数编号')
]


def iter_message(rows):
    for line, cells in enumerate(rows):
        if line == 0:
            continue

        if cells[0].value != '':
            signals = list()
            for _l, _cells in enumerate(rows[line+1:]):
                if _cells[0].value != '':
                    break
                signals.append(_cells)
            yield line, cells, signals


def get_sheet_header_map(sheet):
    # for cell in sheet.row(0):
    #     print(f"('{cell.value}', '')".replace('\n', '\\n'))
    return {cell.value: idx for idx, cell in enumerate(sheet.row(0))}


def get_row_by_header_map(row, header_name, header_map):
    for full_header_name, col in header_map.items():
        if full_header_name.find(header_name) < 0:
            continue

        return row[col].value
    return None


def convert(sheet, output, message_key_map=None, signal_key_map=None):
    header_map = get_sheet_header_map(sheet)
    rows = list(sheet.get_rows())
    if message_key_map is None:
        message_key_map = _default_message_key_map

    if signal_key_map is None:
        signal_key_map = _default_signal_key_map

    message_by_id = dict()
    messages_list = list()
    nodes_set = dict()
    for row, message, signals in iter_message(rows):
        message_items = dict()
        omit_message = False
        for dbc_name, excel_header in message_key_map:
            if not excel_header:
                continue

            cell_value = get_row_by_header_map(message, excel_header, header_map)
            if dbc_name == 'name':
                cell_value = cell_value.replace('/', '_')
                node_name = cell_value.split('_')[0]
                if node_name not in nodes_set:
                    nodes_set[node_name] = cantools.db.Node(name=node_name, comment='')
                message_items['senders'] = [node_name]

            if dbc_name == 'frame_id':
                frame_id = int(cell_value, 16)
                message_items[dbc_name] = frame_id
                if frame_id > 0x1ff:
                    message_items['is_extended_frame'] = True
            elif dbc_name == 'length':
                if cell_value == 'Var':
                    message_items[dbc_name] = 8
                    omit_message = True
                    break
                else:
                    message_items[dbc_name] = int(cell_value)
            else:
                message_items[dbc_name] = cell_value

        if omit_message is True:
            continue

        signals_list = list()
        for idx, signal_row in enumerate(signals):
            #print(' ' * 4, idx, signal_row)
            signal_items = dict()

            for dbc_name, excel_header in signal_key_map:
                if not excel_header:
                    continue
                cell_value = get_row_by_header_map(signal_row, excel_header, header_map)

                if dbc_name == 'length':
                    cell_value = int(cell_value)

                signal_items[dbc_name] = cell_value

            cell_value = get_row_by_header_map(signal_row, '字节', header_map)
            if isinstance(cell_value, str):
                if '\n' in cell_value:
                    cell_value = cell_value.split('\n')[0]

                if '-' in cell_value:
                    byte_idx = int(cell_value.split('-')[0])
                else:
                    byte_idx = int(cell_value)
            else:
                byte_idx = int(cell_value)

            cell_value = get_row_by_header_map(signal_row, '位', header_map)
            if isinstance(cell_value, str):
                if '\n' in cell_value:
                    cell_value = cell_value.split('\n')[0]

                if '-' in cell_value:
                    bit_idx = int(cell_value.split('-')[1])
                else:
                    bit_idx = int(cell_value)
            else:
                bit_idx = int(cell_value)
            signal_items['start'] = (byte_idx - 1) * 8 + (bit_idx - 1)

            signal = cantools.db.Signal(**signal_items)
            #print(' ' * 4, idx, signal)
            signals_list.append(signal)

        message = cantools.db.Message(**message_items, signals=signals_list, strict=False)
        if message.frame_id not in message_by_id:
            message_by_id[message.frame_id] = [message]
            messages_list.append(message)
        else:
            message_by_id[message.frame_id].append(message)

        #print(message)

    database = cantools.db.Database(messages=messages_list, nodes=list(nodes_set.values()), strict=False)

    with codecs.open(output, 'w+', encoding='utf8') as dbc:
        txt = database.as_dbc_string()
        dbc.write(txt)

    for frame_id, messages in message_by_id.items():
        if len(messages) > 1:
            print("冲突的消息ID: 0x{:x}".format(frame_id))
            for message in messages:
                print(' ' * 4, message)


if __name__ == '__main__':
    import optparse

    parser = optparse.OptionParser()
    parser.add_option("-i", "--input-excel", dest="input", help="input excel file", metavar="FILE")
    parser.add_option("-s", "--sheet", dest="sheet", help="sheet name")
    parser.add_option("-o", "--output-dbc", dest="output", help="output dbc file", metavar="FILE")
    options, args = parser.parse_args()
    print(options, args)

    assert options.input is not None, "需要提供输入文件！"
    assert options.sheet is not None, "需要提供表格名称！"

    workbook = xlrd.open_workbook(options.input)
    sheet = workbook.sheet_by_name(options.sheet)
    convert(sheet, options.output, None, None)

