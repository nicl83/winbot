from pprint import pprint
qemu_keys = ['unmapped', 'pause', 'ro', 'kp_comma', 'kp_equals', 'power', 'hiragana', 'henkan', 'yen', 'sleep', 'wake', 'audionext', 'audioprev', 'audiostop', 'audioplay', 'audiomute', 'volumeup', 'volumedown', 'mediaselect', 'mail', 'calculator', 'computer', 'ac_home', 'ac_back', 'ac_forward', 'ac_refresh', 'ac_bookmarks', 'muhenkan', 'katakanahiragana', 'lang1', 'lang2', 'shift', 'shift_r', 'alt', 'alt_r', 'ctrl', 'ctrl_r', 'menu', 'esc', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'minus', 'equal', 'backspace', 'tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'bracket_left', 'bracket_right', 'ret', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'semicolon', 'apostrophe', 'grave_accent', 'backslash', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'comma', 'dot', 'slash', 'asterisk', 'spc', 'caps_lock', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'num_lock', 'scroll_lock', 'kp_divide', 'kp_multiply', 'kp_subtract', 'kp_add', 'kp_enter', 'kp_decimal', 'sysrq', 'kp_0', 'kp_1', 'kp_2', 'kp_3', 'kp_4', 'kp_5', 'kp_6', 'kp_7', 'kp_8', 'kp_9', 'less', 'f11', 'f12', 'print', 'home', 'pgup', 'pgdn', 'end', 'left', 'up', 'down', 'right', 'insert', 'delete', 'stop', 'again', 'props', 'undo', 'front', 'copy', 'open', 'paste', 'find', 'cut', 'lf', 'help', 'meta_l', 'meta_r', 'compose']
mapped_keys = {}

for key in qemu_keys:
    print(f"""\
The next key is {key}.
Press the key you believe is associated with that name, then press Enter.
To skip this one, just press Enter.\
    """)
    mapped = input()
    if mapped != "":
        mapped_keys[mapped] = key
    print("""\
If it is possible to get an additional symbol by pressing that key,
please do so, followed by enter.
As before, to skip, simply press Enter.\
    """)
    mapped_upper = input()
    if mapped_upper != "":
        mapped_keys[mapped_upper] = ["shift", key]
    
pprint(mapped_keys)