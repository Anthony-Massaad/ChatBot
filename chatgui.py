import PySimpleGUI as Sg
import re
from setup import Chatty

## CONSTANTS ## 
IS_BOT = True
MAX_STRINGS_INPUT = 24
MAX_OUTPUT_STRING = 86


def format_sentence(sentence: list, is_bot: bool) -> None:
    """
    Format the sentence accordingly depending on whether '
    the sentence is from the bot or user
    :param sentence: list, split list of input
    :param is_bot: bool, true if bot otherwise false
    :return: Nothing
    """
    partial_sentence = ""
    for word in sentence:
        if len(partial_sentence) + len(word) > MAX_STRINGS_INPUT:
            print_output(partial_sentence, is_bot)
            partial_sentence = ""
        partial_sentence += word + " "
    partial_sentence = partial_sentence[:-1]
    print_output(partial_sentence, is_bot)


def print_output(partial_sentence: str, is_bot: bool) -> None:
    """
    Print the output accordingly to whether it is a bot or not
    :param partial_sentence: str, part of the sentence input
    :param is_bot: boolean, true if bot otherwise false
    :return: Nothing
    """
    if is_bot:
        print(partial_sentence, flush=True)
        return
    print(partial_sentence.rjust((MAX_OUTPUT_STRING//2)+len(partial_sentence)), flush=True)


if __name__ == "__main__":
    chatty = Chatty()
    # theme set up and window layout
    Sg.theme("DarkAmber")
    layout = [
        [Sg.Multiline(size=(50, 30), disabled=True, reroute_stdout=True, echo_stdout_stderr=True)],
        [Sg.InputText(size=(45, 5), key="main", do_not_clear=False), Sg.Button("Send", bind_return_key=True)],
    ]
    # Create the Window
    window = Sg.Window('Chatty', layout).Finalize()
    while True:
        event, values = window.read()
        if event in (None, 'Close Window'):  # if user closes window or clicks cancel
            break
        if event == "Send":
            user_input = values["main"]
            response = chatty.get_response(user_input)
            format_sentence(re.split(r"\s", "You:"), not IS_BOT)
            format_sentence(re.split(r"\s", user_input), not IS_BOT)
            format_sentence(re.split(r"\s", "Chatty:"), IS_BOT)
            format_sentence(re.split(r"\s", response), IS_BOT)

    window.close()