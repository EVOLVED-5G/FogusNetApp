import PySimpleGUI as sg
import subprocess
import sys

"""
    Jumpcutter GUI

    This is a front-end GUI for a command line tool named jumpcutter.

    jumpcutter is a command line based tool written by Carykh.  You'll find the repo here:
    https://github.com/carykh/jumpcutter

    The design of this GUI was made in a way that should not have required any changes to the
    jumpcutter.py file.  However, there appears to be a bug in the original code. The sample rate
    argument was specified as a float, but this later causes a crash in the program, so a single
    change was made to line 68, changing the parameter from a float to an int.  You can get around
    this change by not specifying a default value in this GUI.  Rather than specifying 44100, leave it blank
    which will cause the parameter to be skipped.

    This kind of GUI can be applied to a large number of other commandline programs.

    NOTE - it has not yet been tested on Linux.  It's only been tested on Windows.  Hoping to get it
    tested out on Linux shortly.

    KNOWN Problem - filenames with spaces.  Working on it.  For now, make a temp folder and make sure everything
    has no spaces and you'll be fine.  YouTube download wasn't working on the video I tried

    Copyright 2020 PySimpleGUI.org
"""


def FText(text, in_key=None, default=None, tooltip=None, input_size=None, text_size=None):
    """
    A "Fixed-sized Text Input".  Returns a row with a Text and an Input element.
    """
    if input_size is None:
        input_size = (20, 1)
    if text_size is None:
        text_size = (20, 1)
    return [sg.Text(text, size=text_size, justification='r', tooltip=tooltip, font='Any 12'),
            sg.Input(default_text=default, key=in_key, size=input_size, tooltip=tooltip, font='Any 12')]


def main():
    # This version of the GUI uses this large dictionary to drive 100% of the creation of the
    #   layout that collections the parameters for the command line call.  It's really simplistic
    #   at the moment with a tuple containing information about each entry.
    # The definition of the GUI.  Defines:
    #   PSG Input Key
    #   Tuple of items needed to build a line in the layout
    #       0 - The text to display next to input
    #       1 - The default value for the input
    #       2 - Size of input field (None for default)
    #       3 - Tooltip string
    #       4 - List of additional elements to include on the same row

    input_defintion = {
        '-IP-': ('NetApp IP', 'localhost', None, "IP of NetApp endpoint", []),
        '-PORT-': ('NetApp Port', '8000', None, "Port of NetApp endpoint", []),
        '-TIMES-': ('Times', 1, None, "Times of subscription responses", []),
    }

    # the command that will be invoked with the parameters
    command_to_run = r'curl -sS --request GET http://?:?/netappserver/api/v1/monitoring/subscribe/?/ | jq '

    # Find longest input descrption
    text_len = max([len(input_defintion[key][0]) for key in input_defintion])
    # Top part of layout that's not table driven
    layout = []
    # Computed part of layout that's based on the dictionary of attributes (the table driven part)
    for key in input_defintion:
        layout_def = input_defintion[key]
        line = FText(layout_def[0], in_key=key, default=layout_def[1], tooltip=layout_def[3], input_size=layout_def[2],
                     text_size=(text_len, 1))
        if layout_def[4]:
            line += layout_def[4]
        layout += [line]
    # Bottom part of layout that's not table driven
    layout += [[sg.Text('Constructed Command Line:')],
               [sg.Text(size=(80, 1), key='-COMMAND LINE-', text_color='yellow', font='Any 10')],
               [sg.MLine(size=(100, 15), reroute_stdout=True, reroute_stderr=True, reroute_cprint=True, write_only=True,
                         font='Any 10', autoscroll=True, key='-ML-')],
               [sg.Button('Start'), sg.Button('Exit')]]

    window = sg.Window('FOGUS NetApp', layout, size=(900, 500), finalize=True, resizable=True, icon='/app/logo.png')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        command = command_to_run
        if event == 'Start':
            for key in values:
                command = command.replace('?', values[key], 1)
            window['-COMMAND LINE-'].update(command)
            runCommand(cmd=command, window=window)
            sg.cprint('*' * 20 + 'DONE' + '*' * 20, background_color='green', text_color='white')
    window.close()


def runCommand(cmd, timeout=None, window=None):
    """ run shell command
    @param cmd: command to execute
    @param timeout: timeout for command execution
    @param window: the PySimpleGUI window that the output is going to (needed to do refresh on)
    @return: (return code from command, command output)
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if sys.version_info < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.refresh() if window else None  # yes, a 1-line if, so shoot me

    retval = p.wait(timeout)
    return retval, output


if __name__ == '__main__':
    # sg.theme('Dark Grey 11')
    main()